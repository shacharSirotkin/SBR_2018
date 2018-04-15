import xml.etree.ElementTree as ET
from os import listdir
from os.path import isfile, join

domainsFoldersDict = {1: "/Users/ran/PycharmProjects/PlanRecognition/Domains/full-20-1-5-1-2-3",
                      2: "/Users/ran/PycharmProjects/PlanRecognition/Domains/full-20-1-5-1-5-1",
                      3: "/Users/ran/PycharmProjects/PlanRecognition/Domains/full-20-1-5-2-3-3",
                      4: "/Users/ran/PycharmProjects/PlanRecognition/Domains/full-20-1-5-3-2-1",
                      5: "/Users/ran/PycharmProjects/PlanRecognition/Domains/full-100",
                      6: "/Users/ran/PycharmProjects/PlanRecognition/Domains/1-5-2-3-2-full-100_baseline",
                      7: "/Users/ran/PycharmProjects/PlanRecognition/Domains/1-5-2-3-4-full-100_or",
                      8: "/Users/ran/PycharmProjects/PlanRecognition/Domains/1-5-2-5-2-full-100_and",
                      9: "/Users/ran/PycharmProjects/PlanRecognition/Domains/1-5-3-3-2-full-100_depth"}

folder = domainsFoldersDict[7]

domainfiles = [join(folder, f) for f in listdir(folder) if (isfile(join(folder, f)) and f.endswith("txt"))]

for file in domainfiles:
    if "DS_Store" not in file:
        elementTree = ET.parse(file)
        root = elementTree.getroot()
        nonTerminalsNode = root[0][0]
        allGoals = root.findall('.//Recipe[@lhs="root"]')
        for goalRecipeNode in allGoals:
            goalLetter = goalRecipeNode.find("Letter").get("id")
            goalNode = nonTerminalsNode.find('.//Letter[@id=' + "\"" + goalLetter + "\"" + ']')
            goalNode.set("goal", "yes")
        if root.find("Recipes") != None:
            recipesNode = root.find("Recipes")
            for node in allGoals:
                recipesNode.remove(node)
        elementTree.write(file.replace(".txt", "") + ".xml", encoding="ISO-8859-1", xml_declaration=True)
