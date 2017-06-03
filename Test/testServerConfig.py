# configurations of server provider config file
base_url = 'http://localhost/jarvis/api/event/'
#headres
header = {'content-type': 'application/json'}
#request timeout in seconds
request_timeout = 10
#sleep time is in seconds
sleep_time = 3
# repeat time in minutes
repeat_time = 0.05
# severity configuration
severity_param = 'physicalUsed%'
severity = { 'info':{'min': 0, 'max': 3}, 'warning':{'min': 3 ,  'max': 5}, 'severe':{'min': 5 , 'max': float('inf')}}