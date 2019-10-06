import json
import os
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from subprocess import Popen, PIPE, call

def function_create_cmds(cmd):
    proc = Popen(cmd , shell=True, stdout=PIPE, stderr=PIPE)
    (output, error) = proc.communicate()
    return output

aws_regions = ['us-east-1','us-east-2']
aws_commands =[]

for region in aws_regions:
	os.system('aws configure set default.region ' + region)
	with open('stacks/anka_'+ region +'_stacks.json') as json_file:
		data = json.load(json_file)
		for p in data['StackSummaries']:
			print('Name: ' + p['StackName'])
			awsCmd = 'aws cloudformation detect-stack-drift --stack-name ' + p['StackName']
			aws_commands.append(awsCmd)
			### os.system(awsCmd)
			print('')
	pool = ThreadPool(32)
	results = pool.map(function_create_cmds, aws_commands)
	pool.close()
	pool.join()
	print(results)

