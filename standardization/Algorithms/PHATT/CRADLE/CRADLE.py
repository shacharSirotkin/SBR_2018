import cProfile
import codecs
import csv
import os
import pstats
import sys
import xml.etree.ElementTree as ET
from StringIO import StringIO
from os import listdir
from os.path import isfile, join

from matplotlib.backends.backend_pdf import PdfPages

import Explanation
import PL
from Algorithm import ExplainAndCompute
from FormatProfilerOutput import FormatProfilerOutput
from NT import NT
from Rule import Rule
from Sigma import Sigma

sys.path.append("Source")

inputsFolderName = "/Users/ran/Desktop/Plan_recognition/"
outputsFolderName = "/Users/ran/Desktop/Plan_Recognition/PHATT_OUTPUTS/"

domainsFoldersDict = {1 : "Domains/full-20-1-5-1-2-3",
               2 : "Domains/full-20-1-5-1-5-1",
               3 : "Domains/full-20-1-5-2-3-3",
               4 : "Domains/full-20-1-5-3-2-1",
               5 : "Domains/full-100",
               6 : "Domains/1-5-2-3-2-full-100_baseline",
               7 : "Domains/1-5-2-3-4-full-100_or",
               8 : "Domains/1-5-2-5-2-full-100_and",
               9: "Domains/1-5-3-3-2-full-100_depth",
               10: "Domains/temp"}

observationsFoldersDict = {1 : "Observations/full-20-1-5-1-2-3",
               2 : "Observations/full-20-1-5-1-5-1",
               3 : "Observations/full-20-1-5-2-3-3",
               4 : "Observations/full-20-1-5-3-2-1",
               5 : "Observations/full-100",
               6 : "Observations/1-5-2-3-2-full-100_baseline",
               7: "Observations/1-5-2-3-4-full-100_or",
               8: "Observations/1-5-2-5-2-full-100_and",
               9: "Observations/1-5-3-3-2-full-100_depth",
               10: "Observations/temp"}

def getLetter(listOfLetters, name):
    for letter in listOfLetters:
        if letter.get()==name:
            return letter
    return None

def readDomain(DomainFileName):
    tree = ET.parse(DomainFileName)
    root = tree.getroot()
    
    #Read NTs
    ntNodes = root[0][0]
    NTs=[]
    Goals=[]
    for child in ntNodes:
        name = child.get('id')
        params = []
        if child.find("Params") != None:
            for param in child[0]:
                params.append(param.get('name'))
        newLetter=NT(name, params)
        NTs.append(newLetter)
        if child.get('goal') != None and child.get('goal')=='yes':
            Goals.append(newLetter)

    print "Goals " + str(Goals)
        
    #Read Sigmas
    sigmaNodes = root[0][1]
    Sigmas=[]
    for child in sigmaNodes:
        name = child.get('id')
        params = []
        if child.find("Params") != None:
            for param in child[0]:
                params.append(param.get('name'))
        Sigmas.append(Sigma(name, params))
    
    
    #Read Rules
    Rules=[]
    ruleNodes = root[1]
    
    for ruleNode in ruleNodes:
        #ruleProb = ruleNode.get('prob')
        ruleA = getLetter(NTs, ruleNode.get('lhs'))
        ruleOrders = []
        ruleEquals = []
        ruleRhs = []
        if ruleNode.find('Order')!=None:
            for orderConst in ruleNode.find('Order'):
                ruleOrders.append((int(orderConst.get('firstIndex'))-1, int(orderConst.get('secondIndex'))-1))
        if ruleNode.find('Equals')!=None:
            for equalConst in ruleNode.find('Equals'):
                ruleEquals.append((int(equalConst.get('firstIndex'))-1, equalConst.get('firstParam'), int(equalConst.get('secondIndex'))-1, equalConst.get('secondParam')))
        for child in ruleNode.findall('Letter'):
            letter = getLetter(NTs, child.get('id'))
            if letter==None:
                letter = getLetter(Sigmas, child.get('id'))
            ruleRhs.insert(int(child.get('index'))-1 , letter)
        Rules.append(Rule(ruleA, ruleRhs, ruleOrders, ruleEquals))
        
    myPL = PL.PL(Sigmas, NTs, Goals, Rules)
    return myPL            
    
def readObservations(pl,ObservasionsfileName):
    tree = ET.parse(ObservasionsfileName)
    root = tree.getroot()
    observations = []
    for observation in root:
        letter = getLetter(pl._Sigma, observation.get('id'))
        letter = Sigma(letter.get(), letter.getParamList())
        for param in observation:
            letter.setParam(param.get('name'), param.get('val'))
        observations.append(letter)
    print observations
    return observations
    
'''def main():
        #Usage
    if len(sys.argv) != 3:
        print "Usage: SLIM.py     <domain file>    <observations file> \n"
        sys.exit()
    try:
        planLibrary = readDomain()
        print planLibrary
    except:
        print "Usage: Domain File Corrupt\n"
        sys.exit()
    
    try:
        observations = readObservations(planLibrary)
    except:
        print "Usage: Observations File Corrupt\n"
        sys.exit()

    profile.runctx('myMain(planLibrary, observations)', globals(), locals())'''

    
def myMain(planLibrary, observations, writer, observationsFile, folderName):
    fileName = observationsFile
    writer.write("file name: " + fileName + "\n-------------------------------------------------------------------------------------\n")
    '''print planLibrary
    print "Observations:\n", observations
    print "\n-------------------------------------------------------------------------------------\n" '''

    writer.write(str(planLibrary))
    writer.write("Observations:\n" + str(observations) + "\n")

    exps = ExplainAndCompute(planLibrary, observations)

    difference = 0

    for exp in exps:
        leaves = []
        for tree in exp.getTrees():
            leaves.extend(tree.getLeaves())
        if str(leaves) != str(observations):
            print str(leaves)
            difference += 1

    
    if len(exps)==0:
        writer.write("No Explnanations")
        #print "No Explnanations"
    
    explanations = 0
    noFrontier = 0

    exps.sort(key=Explanation.Explanation.getExpProbability)
    domainAndFileName = ("_").join((observationsFile.strip(".xml").split("/"))[-2:])
    pp = PdfPages(folderName + "/" + domainAndFileName + ".pdf")
    root = ET.Element("xml")
    listID = [1,0]
    for exp in exps:
        expAsXML = exp.explanationAsXML(root)
        exp.plotExplanation(listID, pp)
        indent(expAsXML)
        listID[0] += 1
    pp.close()
    tree = ET.ElementTree(root)
    tree.write(folderName + "/" + domainAndFileName + ".xml")

    firstflag = True
    while not len(exps)==0:
        exp = exps.pop()
        #if firstflag:
        firstflag = False
        if exp.getFrontierSize()==0:
            noFrontier += 1
            
        explanations+=1

    '''print "Explanations: ", explanations
    print "No Frontier Explanations: ", noFrontier
    print "\n-------------------------------------------------------------------------------------\n"'''

    writer.write("Number Of Explanations: " + str(explanations) + "\n")
    writer.write("No Frontier Explanations: " + str(noFrontier) + "\n")
    writer.write("Difference: " + str(difference))
    writer.write("\n-------------------------------------------------------------------------------------\n")

    return explanations

    #sys.exit()

# Ran - running the program without main

#@timeout(1800)
def runInstance(domainfiles, observationsfiles, profilerOutput, i, logTextFileName, folderName):
        profile = cProfile.Profile()
        planLibrary = readDomain(domainfiles[i])
        observations = readObservations(planLibrary, observationsfiles[i])
        numberOfExps = profile.runcall(myMain, planLibrary, observations, logTextFileName, observationsfiles[i], folderName)
        output = StringIO()
        stats = pstats.Stats(profile, stream=output)
        stats.print_stats("calls")
        profilerOutput.format(output.getvalue(), observationsfiles[i], numberOfExps)


def runDomain(NumberOFDomain, writer, folderName):
            profilerOutput = FormatProfilerOutput(writer)
            domainFolder = inputsFolderName + domainsFoldersDict[NumberOFDomain]
            obsFolder = inputsFolderName + observationsFoldersDict[NumberOFDomain]
            domainfiles = [join(domainFolder, f) for f in
                           listdir(domainFolder) if
                           (isfile(join(domainFolder, f)) and f.endswith("xml"))]
            observationsfiles = [join(obsFolder, f) for f in
                                 listdir(obsFolder) if
                                 (isfile(join(obsFolder, f)) and f.endswith("xml"))]
            textFile = codecs.open(folderName + "profilePlanRecognitionCradleTXT" + domainsFoldersDict[NumberOFDomain].split("/")[-1] + ".txt", "w")
            for i in xrange(len(domainfiles)):
                runInstance(domainfiles, observationsfiles, profilerOutput, i, textFile, folderName)
            textFile.close()

def main():
    for NumberOFDomain in [9]:
        folderName = outputsFolderName + domainsFoldersDict[NumberOFDomain].split("/")[-1] + "/"
        if not os.path.exists(folderName):
            os.makedirs(folderName)
        with codecs.open(folderName + "profilePlanRecognitionCradleCSV" + domainsFoldersDict[NumberOFDomain].split("/")[-1] + ".csv", "w") as csvFile:
            fields = ['file name', 'function calls', 'primitive calls', "time", "number of exlanations"]
            writer = csv.writer(csvFile)
            writer.writerow(fields)
            runDomain(NumberOFDomain, writer, folderName)

def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem

if __name__ == '__main__': main()