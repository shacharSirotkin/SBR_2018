import re
import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join

observationsFoldersDict = {1: "/Users/ran/PycharmProjects/PlanRecognition/Observations/full-20-1-5-1-2-3",
                           2: "/Users/ran/PycharmProjects/PlanRecognition/Observations/full-20-1-5-1-5-1",
                           3: "/Users/ran/PycharmProjects/PlanRecognition/Observations/full-20-1-5-2-3-3",
                           4: "/Users/ran/PycharmProjects/PlanRecognition/Observations/full-20-1-5-3-2-1",
                           5: "/Users/ran/PycharmProjects/PlanRecognition/Observations/full-100",
                           6: "/Users/ran/PycharmProjects/PlanRecognition/Observations/1-5-2-3-2-full-100_baseline",
                           7: "/Users/ran/PycharmProjects/PlanRecognition/Observations/1-5-2-3-4-full-100_or",
                           8: "/Users/ran/PycharmProjects/PlanRecognition/Observations/1-5-2-5-2-full-100_and",
                           9: "/Users/ran/PycharmProjects/PlanRecognition/Observations/1-5-3-3-2-full-100_depth"}

folder = observationsFoldersDict[7]
domainfiles = [join(folder, f) for f in listdir(folder) if (isfile(join(folder, f)) and f.endswith("txt"))]

for file in domainfiles:
    if "DS_Store" not in file:
        observationsNode = ET.Element("Observations")
        print file
        for line in open(file):
            if line not in ['\n', '\r\n']:
                ET.SubElement(observationsNode, "Observation", {"id": re.sub("(\r\n|\n|\r)", "", line.split(" ")[1])})
        elementTree = ET.ElementTree(observationsNode)
        elementTree.write(file.replace(".txt", "") + ".xml", encoding="ISO-8859-1", xml_declaration=True)
