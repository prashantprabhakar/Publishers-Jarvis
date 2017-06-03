#!/usr/bin/env python
import MySQLdb
import json
import requests
import dbProviderConfig
import schedule
import time
import sys
import logging
import subprocess
import ast

# Mongo
import pymongo

logging.basicConfig(filename = dbProviderConfig.log_file, level = logging.DEBUG)
sys.path.insert(0, '../CommonUtils/')
import custom_severity

def get_mySql_stats():
	try:
		conn = create_mySql_dbConnection()
		if(conn is None) :
			logging.error("Unable to make database connection. Check configurations")
			return

		cursor = conn.cursor()
		cursor.execute("SHOW GLOBAL STATUS")

		rs = cursor.fetchall()
		result = dict(rs)
		#print result

		# change key values,status, message
		# and additional compulsory fields like id,source,
		
		dataWithStringValues= { 'bytesReceived':int(result['Bytes_received']), \
				 				'bytesSent': int(result['Bytes_sent']), \
				 				'query/sec': int(result['Com_select'])/float(result['Uptime']), \
				 				'update/sec':int(result['Com_update'])/float(result['Uptime']), \
				 				'delete/sec': int(result['Com_delete'])/float(result['Uptime']), \
				  				'uptime': int(result['Uptime']), \
				  				'threadsConnected':int(result['Threads_connected']), \
				  				'threadsCreated': int(result['Threads_created']), \

				  			   }
		
		#converting values to int from 
		#iterateItems is not used in python3 use items() if migrate to python3
		data = dict((k,int(v)) for k,v in dataWithStringValues.iteritems())
		#dict_with_ints = dict((k,int(v)) for k,v in dict_with_strs.iteritems())

		try:
			severity_threshold = data[dbProviderConfig.severity_param]			
			severity_level = custom_severity.check_severity(severity_threshold,dbProviderConfig )			
			data.update({'severity': severity_level})	
		except:
			logging.error("Unable to get severity. Check if severity is defined correctly in configurations")
			print "Unable to get severity"	

		# get teh ip and port for id
		cursor.execute( "SHOW GLOBAL VARIABLES LIKE 'PORT'")
		mySqlPort = cursor.fetchone()[1]			
		
		try:
			data.update({'id':time.time(),'source': 'Database','status': 'Running','message': 'MySql Database stats'})
		except:
			logging.critical("Unable to get Id. ")
			
		# post data to http://10.10.20.131:8080/Jarvis/api/event
		try:
			resp = post_data(data)
			print resp
		except:
			logging.critical("Unable to post MySql data.")
			print "Request Exception occured +1"	
		
		close_mySql_dbConnection(cursor,conn)
		
	except:
		logging.critical("Unknown exception ocured. Can't post Mysql Data to server.")
		print "Job failure. Exception occured"


def create_mySql_dbConnection():
	try:
		return MySQLdb.connect(host = dbProviderConfig.mySqlDb['host'], user= dbProviderConfig.mySqlDb['userName'], passwd= dbProviderConfig.mySqlDb['password'])
	except:
		logging.error("Can not connect to database. Please check config")
		print "Can not connect to database. Please check config"
		return None


def close_mySql_dbConnection(cursor, conn):
	try:
		cursor.close()
		del cursor
		conn.close()
	except:
		logging.error("Unable to close Db Connection.")
		print "Unable to close db connection"


def get_mongodb_stats():
	try:
		proc = subprocess.Popen(['mongostat', '-O', 'connections.current,connections.totalCreated,uptime,network.bytesIn,network.bytesOut','-n1', '--json'],stdout=subprocess.PIPE).communicate()[0]
		proc1 = ast.literal_eval(proc)


		for key in proc1:
			res =  proc1.get(key)		
			data = { 'id' : key, \
					 'status' : 'Running', \
					 'message' : 'MongoDB Stats', \
					 'source' : 'Database',
					 'query/sec': res.get('insert'), \
					 'update/sec' : res.get('update'), \
					 'delete/sec' : res.get('delete'), \
					 'threadsConnected': res.get('connections.current'), \
					 'threadsCreated' : res.get('connections.totalCreated'), \
					 'uptime' : res.get('uptime'), \
					 'bytesSent' : res.get('networkbytesOut'), \
					 'bytesReceived' : res.get('network.byteOut')
			        }
			try:
				severity_threshold = data[dbProviderConfig.severity_param]			
				severity_level = custom_severity.check_severity(severity_threshold,dbProviderConfig )			
				data.update({'severity': severity_level})	
			except:
				logging.error("Unable to get severity. Check if severity is defined correctly in configurations")
				print "Unable to get severity"
		
		#post data to server
		try:
			resp = post_data(data)
			print resp
		except:
			logging.critical("Unable to post MySql data.")
			print "Request Exception occured"

	except:
		logging.critical("Unknown exception ocured. Can't post Mongo Data to server.")
		print "Job failure. Exception occured"


def post_data(data):	
	post_url = dbProviderConfig.base_url + dbProviderConfig.source	
	print post_url
	resp = requests.post(post_url, data=json.dumps(data), headers=dbProviderConfig.header, timeout=dbProviderConfig.request_timeout)
	return resp
	

def main():
	schedule.clear()
	schedule.every(dbProviderConfig.repeat_time).minutes.do(get_mySql_stats)
	schedule.every(dbProviderConfig.repeat_time).minutes.do(get_mongodb_stats)
	while 1:
		schedule.run_pending()		

	    
if __name__ == '__main__':
	main()
