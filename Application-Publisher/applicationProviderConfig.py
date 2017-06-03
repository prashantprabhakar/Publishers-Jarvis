# configurations of application provider config file
no_of_processes = 3
#base url on which script will post data
base_url = 'http://10.10.20.131.:8080/jarvis/api/event/bulk/'
#headres
header = {'content-type': 'application/json'}
#request timeout in seconds
request_timeout = 10
# repeat time in minutes
repeat_time = 0.1
# severity configuration
severity_param = 'cpu'
severity = { 'info':{'min': 0, 'max': 3}, 'warning':{'min': 3 ,  'max': 5}, 'severe':{'min': 5 , 'max': float('inf')}}