from core.utils import *

class Application:

    path = ""
    applications = {}
    utils = Utils()

    def getAppsFromXML(self,application_file):
    	file = (open(application_file).read()).splitlines()
    	items = []
    	results = []

    	for line in file:
    		if "web-uri" in line:
    			server = (line.split("<")[1]).split(">")[1]
    			path = "%s/%s" % (("/".join((application_file.split("/")[:-2]))),server)
    			items.append(path)
    		if "context-root" in line:
    			items.append((line.split("<")[1]).split(">")[1])

    	c = 0
    	for item in items:
    		if(c % 2) == 0:
    			server = item
    			path = items[c+1]
    			line = "%s;%s" % (server,path)
    			if line not in results:
    				results.append("%s;%s" % (server,path))
    		c +=1

    	return results

    def loadRoutesFromAPP(self,path):
        results = {}
        classes = []
        servlets = []
        urls = []
        file_path = "%s/WEB-INF/web.xml" % path
        try:
            file = (open(file_path,"r").read()).splitlines()

            #regexp
            # <servlet-mapping>(.|\n)*?<\/servlet-mapping>
            #

            for line in file:
                try:
                    data = (line.split(">")[1]).split("<")[0]
                    if ("servlet-name" in line) and (data not in servlets):
                    	servlets.append(data)
                    if ("servlet-class" in line) and (data not in classes):
                    	classes.append(data)
                    if ("url-pattern" in line) and (data not in urls):
                    	urls.append(data)
                except:
                    pass
        except:
            return False

        results["classes"] = classes
        results["servlets"] = servlets
        results["urls"] = urls
        results["path"] = path
        return results

    def __init__(self,path):
        self.path = path

    def getApplications(self):
        folder = self.path
        applications = self.applications
        for file in self.utils.getAllFilesFolders(folder):
            if "/application.xml" in file:
                virtual_apps = self.getAppsFromXML(file)
                for virtual_app in virtual_apps:
                    application = virtual_app.split(";")[1]
                    location = virtual_app.split(";")[0]
                    app_routes = self.loadRoutesFromAPP(location)
                    applications[application] = app_routes
        return applications
