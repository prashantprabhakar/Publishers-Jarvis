# configurations of server provider config file
base_url = 'http://10.10.20.131:8080/jarvis/api/event/'
#headres
header = {'content-type': 'application/json'}
#request timeout in seconds
request_timeout = 10
#sleep time is in seconds
sleep_time = 3
# repeat time in minutes
repeat_time = 0.1

#logging config
log_file = 'serverProvider_log'
log_level = 'logging.DEBUG'

# severity configuration
severity_param = 'physicalUsed%'
severity = { 'info':{'min': 0, 'max': 3}, 'warning':{'min': 3 ,  'max': 5}, 'severe':{'min': 5 , 'max': float('inf')}}