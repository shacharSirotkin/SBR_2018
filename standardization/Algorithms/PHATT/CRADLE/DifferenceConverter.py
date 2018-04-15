import codecs
import csv
import os.path

inputFolderPHATT = "/Users/ran/Desktop/Plan_Recognition/PHATT_OUTPUTS/"
inputFolderSBR = "/Users/ran/Desktop/Plan_Recognition/SBR_OUTPUTS/"
inputDomains = ["full-20-1-5-1-2-3",
                "full-20-1-5-1-5-1",
                "full-20-1-5-2-3-3",
                "full-20-1-5-3-2-1",
                "full-100",
                "1-5-2-3-2-full-100_baseline",
                "1-5-2-3-4-full-100_or",
                "1-5-2-5-2-full-100_and",
                "1-5-3-3-2-full-100_depth"]

for inputDomain in inputDomains:
    # print inputDomain
    try:
        SBRExpNum = []
        PHATTExpNum = []
        Diff = []
        fileName = []
        outputCSVFile = "/Users/ran/Desktop/Plan_Recognition/finalCSV_" + inputDomain + ".csv"
        with open(outputCSVFile, 'wb') as csvfile:
            Diffwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            if os.path.isfile(
                                                            inputFolderPHATT + inputDomain + "/" + "profilePlanRecognitionCradleTXT" + inputDomain + ".txt"):
                textFileDiffPHATT = codecs.open(
                    inputFolderPHATT + inputDomain + "/" + "profilePlanRecognitionCradleTXT" + inputDomain + ".txt",
                    "r", "utf-8")
                with open(
                                                                inputFolderPHATT + inputDomain + "/" + "profilePlanRecognitionCradleCSV" + inputDomain + ".csv",
                                                                'rb') as csvFilePHATT:
                    csvFilePHATTReader = csv.reader(csvFilePHATT)
                    csvFilePHATTReader.next()
                    for row in csvFilePHATTReader:
                        if row[4] != "":
                            PHATTExpNum.append(row[4])
                with open(inputFolderSBR + inputDomain + "/" + inputDomain + "_time.csv", 'rb') as csvFileSBR:
                    csvFileSBRReader = csv.reader(csvFileSBR)
                    for row in csvFileSBRReader:
                        SBRExpNum.append(row[3])
                        fileName.append(row[0])
                for row in textFileDiffPHATT:
                    if "Difference" in row:
                        Diff.append(row.replace("Difference: ", "").replace("\n", ""))
            Diffwriter.writerow(["file name", "SBR number of exps", "PHATT number of exps without interleaving"])
            for i in xrange(0, len(Diff)):
                if SBRExpNum[i] != str(int(PHATTExpNum[i]) - int(Diff[i])):
                    print fileName[i] + " " + SBRExpNum[i] + " " + str(int(PHATTExpNum[i]) - int(Diff[i]))
                Diffwriter.writerow([fileName[i], SBRExpNum[i], str(int(PHATTExpNum[i]) - int(Diff[i]))])
    except:
        IndexError, StopIteration
