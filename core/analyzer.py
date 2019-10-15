
import shutil, os, subprocess, yaml
from core.utils import *

class Analyzer:

    application_name = None
    application_struct = None
    jad_folder = "./jadfiles"
    findings = []

    utils = Utils()

    def __init__(self, name, struct):

        self.application_name = name
        self.application_struct = struct

        if self.createJADAPPFolder(name):
            # Decompile Classes
            try:
                classes = self.application_struct["classes"]
                folder_path = "%s/WEB-INF/classes/" % self.application_struct["path"]
                for classf in classes:
                    classfile = "%s%s.class" % (folder_path,classf.replace(".",'/'))
                    if os.path.isfile(classfile):
                        decompiler = self.decompileClass(classfile)
                        if decompiler[0]:
                            #self.utils.sprint("Decompiled without error (%s)" % classf,'info')
                            pass
                        else:
                            #self.utils.sprint("Error Decompiling (%s) - Return: %s" % (classf,decompiler[1]),'danger')
                            pass
                    else:
                        #self.utils.sprint("Cannot find class: %s (%s)" % (classf,classfile),'danger')
                        pass
            except Exception as e:
                self.utils.sprint("Error (%s) processing class from %s" % (e,name),'danger')

            self.runSearcher()
            #self.doCleanup()


    def searchClassWord(self,class_file,word):
        lines = class_file.splitlines()
        for line in lines:
            if word in line:
                return True

    def runSearcher(self):
        folder = self.jad_folder
        application_name = self.application_name
        application_folder = "%s/%s" % (folder,application_name)
        search_rule_file = "./rules/searcher.yaml"
        findings = {}

        try:
            yaml_file = open(search_rule_file,"r").read()
        except Exception as e:
            print("error")

        classes = self.utils.getAllFilesFolders(application_folder)

        for classf in classes:
            class_file = open(classf,"r").read()
            cname = classf.split("/")[-1]
            findings[cname] = []
            searches = yaml.load(yaml_file,Loader=yaml.FullLoader)
            for search in searches:
                if search["type"] == "string":
                    for search_item in search["match"]:
                        if self.searchClassWord(class_file,search_item):
                            if search["name"] not in findings:
                                findings[cname].append("%s" % (search["name"]))

        self.findings = findings

    def createJADAPPFolder(self,name):
        try:
            application_folder = "%s/%s" % (self.jad_folder,name)
            if os.path.isdir(self.jad_folder) == False:
                os.mkdir(self.jad_folder)
            if os.path.isdir(application_folder) == False:
                os.mkdir("%s/%s" % (self.jad_folder,name))
            return True
        except OSError:
            self.utils.sprint("Error creating Folder (%s), check permissions!" % application_folder,'danger')
        return False

    def getResults(self):
        return self.findings

    def decompileClass(self,class_path):
        result = []
        class_name = (class_path.split("/")[-1]).split(".")[0]
        application_folder = "%s/%s" % (self.jad_folder,self.application_name)
        output = subprocess.Popen(['jad', '-o', '-d', application_folder,class_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout,stderr = output.communicate()
        if stdout is not None:
            if "Generating" in str(stdout):
                result = [True,None]
                try:
                    os.rename("%s/%s.jad" % (application_folder,class_name), "%s/%s.java" % (application_folder,class_name))
                except:
                    pass
            else:
                message = "Stdout: %s \n Stderr: %s \n" % (stdout,stderr)
                result = [False,message]
        return result

    def doCleanup(self):
        try:
            if os.path.isdir(self.jad_folder):
                shutil.rmtree(self.jad_folder)
        except OSError:
            self.utils.sprint("Error cleanning folder!",'danger')
