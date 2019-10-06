import os

aws_regions = ['us-east-1','us-east-2']

for region in aws_regions:
	print('Setting default region name to ' + region)
	awsCmd = 'aws configure set default.region ' + region
	os.system(awsCmd)
	print('Getting Cloudformation stack list [' + region + ']')
	awsCmd = 'aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE > stacks/anka_' + region + '_stacks.json'
	os.system(awsCmd)
