import os
import sys
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
	with open('reports/'+ region +'_drifted-stacks.txt') as f:
		drifted_stacks = f.read().splitlines()
		for stack in drifted_stacks:
			print('Stack Name: ' + stack)
			awsCmd = 'aws cloudformation describe-stack-resource-drifts --stack-name ' + stack + ' --stack-resource-drift-status-filters "MODIFIED" "DELETED" > stacks/output/' + stack + '.json'
			aws_commands.append(awsCmd)
			##os.system(awsCmd)
			print('')

	pool = ThreadPool(32)
	results = pool.map(function_create_cmds, aws_commands)
	pool.close()
	pool.join()
	print(results)
	aws_commands =[]
