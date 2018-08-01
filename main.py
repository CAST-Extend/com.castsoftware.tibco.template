from lxml.doctestcompare import strip
from _ast import Or
from sqlalchemy.sql.expression import true
import cast.analysers.ua
import cast.analysers.log as Print
import xml.etree.ElementTree as ET
from cast.analysers import CustomObject,Bookmark,create_link
import re
from numpy.core.defchararray import endswith
#from pydoc import classname
import cast.application


# from fileinput import filename

#AngularJS_NgModule=CustomObject()

CondType_Rule='';
Act_invalid=[]
CondType_Rule=[]
class TibcoExtension(cast.analysers.ua.Extension):
    def __init__(self):
        self.k = 1
        self.filename=""
        self.file = "" 
        self.name=""
        cnt= 0
    
    def start_analysis(self):

        #self.intermediate_file_providers= self.get_intermediate_file("Class.txt")
        #self.intermediate_file_Functions= self.get_intermediate_file("Functions.txt")
        Print.info("Start Analysis!")
        pass

    def masterdata(self):
        Cond_tree = ET.parse('Rule_Data/ConditionType.xml')
        Cond_root = Cond_tree.getroot()
        conditionType = Cond_root.find('conditionType')
        CondType_Rule = conditionType.text
        CondType_Rule = CondType_Rule.split(',')
        # CondType_Rule = '\t'.join(CondType_Rule)
        print(CondType_Rule)
        Print.info("CondType_Rule invalid list -- " + str(CondType_Rule))
        Act_tree = ET.parse('Rule_Data/Activities')
        Act_root = Act_tree.getroot()
        Act_invalid = Act_root.find('Invalid')
        Act_invalid = Act_invalid.text
        Act_invalid = Act_invalid.split(',')
        print(Act_invalid)
        Print.info("Activity invalid list -- " + str(Act_invalid))
        return Act_invalid

    def start_file(self, file):
        Print.info("Start f!"+str(file))
        contentList = []
        fList=[]
        # self.file = file
        # self.filename = "D:/CASTTOOL/RuleDevelopment/Tibco/com.castsoftware.uc.tibco/com.castsoftware.uc.tibco/TibcoTest/TibcoSample/AdapterQueueStarter.process";
        self.filename = file.get_path();
        self.file = file;
        Print.info("###############printing file name############")
        Print.info("FileName--" + str(self.filename))
        file_ref = open(self.filename, encoding='UTF_8')
        # contentList=[];
        for i in file_ref:
            contentList.append(str(i));
        Print.info("contentList >> "+ str(contentList))
        fList=contentList
        '''
        for i in file_ref:
            fList.append(str(i).strip().lower())
            '''
        Print.info("Flist >> " + str(fList))
        Tibco_Process = CustomObject();
        self.saveObject(Tibco_Process, str(self.filename), self.filename + str(self.filename), "Tibco_Process",
                        self.file,
                        self.filename + "Tibco_Process")
        Tibco_Process.save();

        # Tibco_Process.save_position(Bookmark(self.file, indexOfClass + 1, 1, indexOfClass + 1, -1));
        Print.info("object saved" + self.filename)
        Print.info(str(fList))
        for line in range(0, len(fList)):
            if ("<pd:conditiontype" in fList[line]):
                # print(fList[line])
                if any(s in fList[line] for s in CondType_Rule):
                    Print.info("valid condition type>>" + fList[line] + " Line #" + str(line + 1))
                else:
                    Print.info("invalid condition type>>" + fList[line] + " Line #" + str(line + 1))
            if ("<pd:transition" in fList[line]):
                Print.info(fList[line])
                Act_invalid=self.masterdata()
                Print.info("Act_invalid >> "+str(Act_invalid))
                if any(s in fList[line + 1] for s in Act_invalid):
                    Print.info("activity type cannot be migrated>>" + fList[line + 1] + " Line #"+ str(line + 1))
                    Tibco_Process.save_position(Bookmark(self.file, line + 1, 1, line + 1, -1));
                    Tibco_Process.save_violation("Tibco_CustomMetrics.Activitycannotbemigrated",
                                                 Bookmark(file, 1, 1, -1, -1), additional_bookmarks=None)

                    Print.info('Tibco  Violation  Saved for demo')
                else:
                    Print.info("activity type can be migrated>>"+ fList[line + 1] + " Line #" + str(line + 1))
                    Tibco_Process.save_position(Bookmark(self.file, line + 1, 1, line + 1, -1));
                    Tibco_Process.save_violation("Tibco_CustomMetrics.Activitycannotbemigrated",
                                                 Bookmark(file, 1, 1, -1, -1), additional_bookmarks=None)
                    Print.info('Tibco  Violation  Saved for demo')
        pass
        #return contentList;
        
    def findIndex(self,content,tag,index):
        Print.info("aws"+str(index));
        for i in content:
            if re.search(tag,i):
                return index;
            index+=1;       
        return -1; 


    def end_file(self,file):
        #Print.info.debug("declartions" + str(tsDeclarationsList))
        #cast.analysers.log.debug("End file!")
        pass
        
        
    def end_analysis(self):
        #Print.info(str(finalData))
        #self.intermediate_file_Functions.write(str(finalData));
        pass
    def saveObject(self,obj_reference,name,fullname,obj_type,parent,guid): 
        obj_reference.set_name(name)
        cast.analysers.log.debug("Obj_Name--------!" +str(name))
        obj_reference.set_fullname(fullname)
        obj_reference.set_type(obj_type)
        cast.analysers.log.debug("Obj_Type--------!" +str(obj_type))
        obj_reference.set_parent(parent)
        cast.analysers.log.debug("Obj_parent--------!" +str(parent))
        obj_reference.set_guid(guid) 
        cast.analysers.log.debug("Obj_guid--------!" +str(guid))
        Print.info('Tibco  object  Saved '+ name)
        pass