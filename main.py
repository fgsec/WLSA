#!/usr/bin/env python3

from termcolor import colored
from core.application import *
from core.analyzer import *
from core.utils import *

import argparse, pprint, sys, os

def main():
		u = Utils()
		u.showBanner()
		pp = pprint.PrettyPrinter(indent=3,width=120)

		detected_items = {}

		parser = argparse.ArgumentParser(description='Analyze WebLogic Applications for Security Stuff')
		parser.add_argument('-folder', type=str, required=True, help='Folder Location')
		parser.add_argument('--debug', type=int, help='Enable logging information (--debug 1)')
		args = parser.parse_args()
		if os.path.isdir(args.folder):
			u.sprint("Checking folder and gathering information",'info')
			app = Application(args.folder)
			applications = app.getApplications()
			if applications:
				total_applications = len(applications.keys())
				u.sprint("Found %i applications" % (total_applications),'title')
				# Iterate over Applications
				for application in applications.keys():
					u.sprint("%s" % application,"info")
					try:
						pp.pprint(applications[application]["path"])
					except:
						pass
					analyzer = Analyzer(application,applications[application])
					results = analyzer.getResults()

					# Create view based on Detections
					for result in results.keys():
						if len(results[result]):
							for item in results[result]:
								if item not in detected_items.keys():
									detected_items[item] = []
								else:
									new_entry = "%s => %s" % (application,result)
									if new_entry not in detected_items[item]:
										detected_items[item].append(new_entry)
					#pp.pprint(applications)
					pp.pprint(results)

			#pp.pprint(applications)
			pp.pprint(detected_items)
		else:
			u.sprint("Error, check informed folder!",'danger')

if __name__ == '__main__':
	os.system("clear")
	main()
	print("\n\n")
