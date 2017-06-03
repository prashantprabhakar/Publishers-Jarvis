from subprocess import call
from pymongo import MongoClient
import subprocess
import ast

#ps = subprocess.Popen(['mongostat'], stdout=subprocess.PIPE).communicate()[0]
# x = call(['mongostat' , '--json', '-n1'])
# print x
# client = MongoClient()
# x  = client.admin.command("mongostat")
# print x


proc = subprocess.Popen(['mongostat', '-O', 'connections.current,connections.totalCreated,uptime,network.bytesIn,network.bytesOut','-n1', '--json'],stdout=subprocess.PIPE).communicate()[0]
proc1 = ast.literal_eval(proc)


for key in proc1:
	key =  proc1.get(key)
	print key
	new_data = { 'insert/sec': key.get('insert'), \
				 'update/sec' : key.get('update'), \
				 'delete/sec' : key.get('delete'), \
				 'query/sec' : key.get('query'), \
				 'currentConnections': key.get('connections.current'), \
				 'totalConnections' : key.get('connections.totalCreated'), \
				 'uptime' : key.get('uptime'), \
				 'bytesSent' : key.get('networkbytesOut'), \
				 'bytesReceived' : key.get('network.byteOut')
	            }

print new_data