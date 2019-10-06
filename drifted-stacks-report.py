import json

aws_regions = ['us-east-1','us-east-2']

for region in aws_regions:
	with open('stacks/anka_' + region + '_stacks.json') as json_file:
		data = json.load(json_file)
		f= open("reports/"+ region + "_drifted-stacks.txt","w+")
		for p in data['StackSummaries']:
			if p['DriftInformation']['StackDriftStatus'] == 'DRIFTED':
				print(p['StackName'])
				f.write(p['StackName'] + '\r\n')
		f.close()

