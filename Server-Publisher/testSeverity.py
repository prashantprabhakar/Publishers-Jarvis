import serverProviderConfig


def check_severity(value):
	for key in serverProviderConfig.severity:
		if value>= serverProviderConfig.severity[key]['min'] and value< serverProviderConfig.severity[key]['max']:
			print key

def main():
	value = 3.5
	check_severity(value)

if __name__ == '__main__':
	main()

