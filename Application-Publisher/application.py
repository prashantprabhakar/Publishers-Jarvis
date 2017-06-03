#!/usr/bin/env python
import subprocess
import json
import requests
import applicationProviderConfig
import schedule
import sys

sys.path.insert(0, '../CommonUtils/')
import custom_severity

def job():
	try:
		ps = subprocess.Popen(['ps', 'aux' , '--sort=-%mem'], stdout=subprocess.PIPE).communicate()[0]
		processes = ps.split('\n')

		data = []

		key_names = ['user', 'id', 'cpu', 'mem', 'time', 'cmd', 'source', 'status', 'message']
		additional_values = ['Application', 'Running', 'Process stats']
		nfields = len(processes[0].split()) - 1
		for row in processes[1:applicationProviderConfig.no_of_processes+1]:
			# print(row)
			process_data = row.split(None,nfields)
			selected_process_data = process_data[0:4]+ process_data[9:]+additional_values
			data.append(dict(zip(key_names,selected_process_data)))
			try:
				#print data
				severity_threshold = data[-1][applicationProviderConfig.severity_param]
				severity_level = custom_severity.check_severity(float(severity_threshold),applicationProviderConfig )	
				# severity is always null
				data[-1].update({'severity': severity_level})					
			except:
				print "Unable to get severity"
				
		post_url = applicationProviderConfig.base_url + data[0].get('source')
		
		try:
			resp = requests.post(post_url, data=json.dumps(data), headers=applicationProviderConfig.header, timeout=applicationProviderConfig.request_timeout)		
			print resp
		except:		
			print "Unable to post data. Please check config or if server is down."		
			#main()
	except:
		print "Job failure. Exception occured"


def main():
	schedule.clear()
	schedule.every(applicationProviderConfig.repeat_time).minutes.do(job)
	while 1:
		schedule.run_pending()
		

if __name__ == '__main__':
	main()

	

	