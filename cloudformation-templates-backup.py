import json
import os
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 
from subprocess import Popen, PIPE, call

def function_create_cmds(cmd):
    proc = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
    (output, error) = proc.communicate()
    return output

## AWS regions list
## 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-north-1', 'ap-east-1', 'ap-northeast-1', 'ap-northeast-2', 'ap-northeast-3', 'ap-southeast-1', 'ap-southeast-2', 'ap-south-1', 'me-south-1', 'sa-east-1'
## pick your aws regions and set aws_regions

aws_regions = ['us-east-1','us-east-2']
aws_commands =[]

for region in aws_regions:
	os.system('aws configure set default.region ' + region)
	with open('stacks/anka_' + region + '_stacks.json') as json_file:
		data = json.load(json_file)
		for p in data['StackSummaries']:
			print('Name: ' + p['StackName'])
			awsCmd = 'aws cloudformation get-template --stack-name ' + p['StackName'] + ' > templates/' +  p['StackName'] + '.json'
			aws_commands.append(awsCmd)
			##os.system(awsCmd)
			print('')
	pool = ThreadPool(32) 
	results = pool.map(function_create_cmds, aws_commands)
	pool.close() 
	pool.join() 
	print(results)
