
## Install python:
* ##### Install Required Packages
	$ sudo apt-get install build-essential checkinstall
	$ sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

* ##### Download Python 2.7.13
	$ cd /usr/src
	$  wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz
	$ tar xzf Python-2.7.13.tgz

* ##### Compile Python Source
	$ cd Python-2.7.13
	$ sudo ./configure
	$ sudo make altinstall

* ##### Check the Python Version
	$ python2.7 -V



Note: This project is tested with python 2.7

## Install pip
	$ sudo apt-get install python-pip

## Install dependencies - common
	$ pip install requests
	$ pip install schedule
	$ pip install json
	$ pip install logging

## To run mySqlDb.py
* #### Install dependencies
		$ pip install MySQLdb
		$ pip install subprocess
		$ pip install ast

* ####  Modify mySqlDbProviderConfig.py to add configurations:
		mySqlUser : username of  mySqlDB
		mySqlHost : host on which mySqlDb is running
		mySqlPassword : password of mySqlUser
		base_url : url on which data needs to be posted
		header : request header
		request_timeout : timeout of request
		repeat_time : time (in minutes) after which scripts runs repetedly

* #### Run the script by:
		$ ./mySqlDb.py


## To run Application.py:
* #### Install dependencies:
		$ pip install subprocess

* ####  Modify applicationProviderConfig.py to add configurations
		no_of_processes : no of top heavy processes you want in output
		base_url : url on which data needs to be posted
		header : request header
		request_timeout : timeout of request
		repeat_time : time (in minutes) after which scripts runs repetedly

* ####  Run the script by:
		$ ./application.py


## To run Server.py:
* #### Install dependencies
		$ pip install psutil 

* #### Modify serverProvider.py to add configurations
		base_url : url on which data needs to be posted
		header : request header
		request_timeout : timeout of request
		repeat_time : time (in minutes) after which scripts runs repetedly

* #### Run the script by:
		$ ./server.py

