#!/usr/bin/env python
import psutil
import testServerConfig
import json
import requests
import schedule
import time
import socket
import sys
import logging

logging.basicConfig(filename = 'testServerlog', level = logging.DEBUG)

sys.path.insert(0, '../CommonUtils/')
import custom_severity

def job():
	try:
		physical = psutil.virtual_memory()
		swap = psutil.swap_memory()
		disk = psutil.disk_usage('/')

		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(("8.8.8.8", 80))
			id = s.getsockname()[0]
		except:
			print "Unable to get ip. Check if connected to internet"
			logging.error('Unable to get ip. Check if connected to internet')

		try:
			data = { 'id': id+":"+(str)(time.time()), \
					 'source': 'Server',\
					 'status':'Running', \
					 'message':'Server stats', \
					 'totalPhysical' : physical[0], \
					 'avilablePhysicalMem' : physical[1], \
					 'physicalUsed%' : physical[2], \
					 'physicalFree' : physical[3], \
					 'physicalActive': physical[4] , \
					 'swapTotal' : swap[0], \
					 'swpaUsed' : swap[1], \
					 'swapFree': swap[2], \
					 'swapUsesd%': swap[3], \
					 'totalDisk': disk[0], \
					 'usedDisk': disk[1], \
					 'freeDisk': disk[2], \
					 'diskUsed%': disk[3]}
		except:
			print "Unable ot get data"

		try:
			severity_threshold = data[testServerConfig.severity_param]
			severity_level = custom_severity.check_severity(severity_threshold,testServerConfig )			
			data.update({'severity': severity_level})
			
		except:
			print "Unable to get severity"
		
				
		post_url = testServerConfig.base_url + data.get('source')
		try:
			resp = requests.post(post_url, data=json.dumps(data), headers=testServerConfig.header, timeout=testServerConfig.request_timeout)
			print resp
		except requests.exceptions.RequestException:
			print "Request Exception"			

		#print data
	
	except:
		print "Job failure. Exception occured"	



def main():
	schedule.clear()
	logging.debug('This message should go to the log file')
	logging.info('So should this')
	logging.warning('And this, too')
	schedule.every(testServerConfig.repeat_time).minutes.do(job)
	while 1:
		schedule.run_pending()
		

if __name__ == '__main__':
	main()

