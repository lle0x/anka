#!/bin/bash

cd "${0%/*}"

echo "-------------------------------------------"
date

echo "Step 0. Updating Cloudformation stacks list"
python3 list-stacks.py

echo "Step 1. Forcing drift status check"
python3 drift-status-check.py > reports/drift-status-checks.txt 2>&1

echo "Step 2. Creating Drift status report"
python3 drift-status-report.py

echo "Step 3. Saving Cloudformation stacks list"
python3 list-stacks.py

declare -a regions=("us-east-1" "us-east-2")

commitmessage="report update: $(date +%F)."

for i in "${regions[@]}"
do
	commitmessage=$commitmessage" [$i]"
	echo "-------------------------------------------" | tee reports/"$i"_mini-report.txt
	echo "Drift status summary" | tee -a reports/"$i"_mini-report.txt
	total=$(cat reports/"$i"_drift-status-report.txt | grep 'Drift Status:' | wc -l)
	echo "Stacks total: $total" | tee -a reports/"$i"_mini-report.txt
	commitmessage=$commitmessage" T:"$total
	drifted=$(cat reports/"$i"_drift-status-report.txt | grep 'Drift Status: DRIFTED' | wc -l)
	echo "DRIFTED: $drifted" | tee -a reports/"$i"_mini-report.txt
	commitmessage=$commitmessage" D:"$drifted
	notchecked=$(cat reports/"$i"_drift-status-report.txt | grep 'Drift Status: NOT_CHECKED' | wc -l)
	echo "NOT_CHECKED: $notchecked" | tee -a reports/"$i"_mini-report.txt
	commitmessage=$commitmessage" n:"$notchecked
	insync=$(cat reports/"$i"_drift-status-report.txt | grep 'Drift Status: IN_SYNC' | wc -l)
	echo "IN_SYNC: $insync" | tee -a reports/"$i"_mini-report.txt
	commitmessage=$commitmessage" I:"$insync
	date | tee -a reports/"$i"_mini-report.txt
	echo "-------------------------------------------"
	echo $commitmessage
done

echo "Step 4. Creating DRIFTED cloudformation stack list"
date
python3 drifted-stacks-report.py

echo "Step 5. Updating DRIFTED cloudformation stack resources"
date
git rm stacks/drifted/*
mkdir stacks/drifted/
for i in "${regions[@]}"
do
	aws configure set default.region "$i"
	python3 drifted-resources-report.py > reports/"$i"_drifted-resources-report.log 2>&1
	find stacks/output/ -type f -size 0 -exec rm {} \;
	mv stacks/output/*.json stacks/drifted/
done

echo "Step 6. Updating Cloudformation Templates backup"
date
python3 cloudformation-templates-backup.py > reports/cloudformation-templates-report.txt

echo "-------------------------------------------"
echo "Step 7. Creating git commit.."
date
git add templates/ stacks/drifted/ stacks/anka_*.json reports

# to setup git push via ssh
# git remote set-url origin git@bitbucket.org:your-org/anka-your-org.git
# create ssh key
# ssh-keygen
# eval `ssh-agent`
# ssh-add ~/.ssh/id_rsa
# cat ~/.ssh/id_rsa.pub
# copy and paste this output to your bitbucket profile [ssh key]

#commit_message="report update: $(date +%F). Stacks total: $total. DRIFTED: $drifted. NOT_CHECKED: $notchecked. IN_SYNC: $insync"
git commit --verbose -m "$commitmessage"
ssh -T git@bitbucket.org
git push --verbose

date

cd "$OLDPWD"
