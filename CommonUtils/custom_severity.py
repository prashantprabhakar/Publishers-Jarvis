#!/usr/bin/env python

def check_severity(value, configFile):
	for key in configFile.severity:		
		if value>= configFile.severity[key]['min'] and value< configFile.severity[key]['max']:
			return key
def main():
	print "Called custom_severity"
	
if __name__ == '__main__':
	main()

