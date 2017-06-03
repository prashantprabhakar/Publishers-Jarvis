# configurations of mySql Database provider config file

# mySql Db details:
mySqlDb = { 'host':'127.0.0.1', 'userName':'root', 'password':'Gemini@123' }

 
# base url on which script will post the data
base_url = 'http://10.10.20.131:8080/jarvis/api/event/'
#headres
header = {'content-type': 'application/json'}
#request timeout in seconds
request_timeout = 10
# repeat time in minutes
repeat_time = 0.1
# source name
source = 'Database'

#logging details:
log_file = 'mySqlProvider_log'
log_level = 'logging.DEBUG'


# severity configuration
severity_param = 'uptime'
severity = { 'info':{'min': 1, 'max': 2}, 'warning':{'min': 3 ,  'max': 4}, 'severe':{'min': 4 , 'max': float('inf')}}