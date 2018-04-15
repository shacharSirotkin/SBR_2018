import re

class FormatProfilerOutput:
    def __init__(self, outputCSVFile):
        self.outputCSVWriter = outputCSVFile

    def format(self, profilerOutputString, fileName, numberOfExps):
        writer = self.outputCSVWriter
        foundPattern = re.search("(\d+) function calls \((\d+) primitive calls\) in (.*?) seconds",
                                 profilerOutputString)
        writer.writerow([fileName, foundPattern.group(1), foundPattern.group(2), foundPattern.group(3), numberOfExps])
