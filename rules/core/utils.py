from termcolor import colored
from datetime import datetime
import os

class Utils:

    version = "0.1"
    log_file = "./output_log.txt"

    def getAllFilesFolders(self,path):
    	files = []
    	for r, d, f in os.walk(path):
    		for file in f:
    			files.append(os.path.join(r, file))
    	return files

    def logOutput(self,message):
        try:
            dateTimeObj = datetime.now()
            log_file = open(self.log_file,"a")
            log_file.write("[%s] %s \n" % (dateTimeObj,message))
        except:
            pass

    def getVersion(self):
        return self.version

    def showBanner(self):
        banner = " _     _  ___      _______  _______\n| | _ | ||   |    |       ||   _   |\n| || || ||   |    |  _____||  |_|  |\n|       ||   |    | |_____ |       |\n|       ||   |___ |_____  ||       |\n|   _   ||       | _____| ||   _   |\n|__| |__||_______||_______||__| |__|\n\n"
        print(colored("%s" % banner, 'red'), colored("@Fgsec - Version %s\n" % self.getVersion(), 'yellow'))

    def sprint(self,text,type):

        type_icon = {"info":"[#]","danger":"[!]","title":"[@]"}
        type_color = {"info":"green","danger":"red","title":"yellow"}
        print(colored(type_icon[type],type_color[type]), end = '')
        print(" %s" % text)

        self.logOutput("%s %s" % (type_icon[type],text)) # log messages
