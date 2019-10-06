import json

aws_regions = ['us-east-1','us-east-2']

for region in aws_regions:
	with open('stacks/anka_' + region + '_stacks.json') as json_file:
		data = json.load(json_file)
		f= open("reports/"+ region + "_drift-status-report.txt","w+")
		for p in data['StackSummaries']:
			print('Name: ' + p['StackName'])
			f.write('Name: ' + p['StackName'] + '\r\n')
			print('Drift Status: ' + p['DriftInformation']['StackDriftStatus'])
			f.write('Drift Status: ' + p['DriftInformation']['StackDriftStatus'] + '\r\n')
			print('')
		f.close()
