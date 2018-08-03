
import os, re

from debug import *
from pojo import *

class Parser:
    def __init__(self, mappingFile):
        self.finalDict = parse(mappingFile)

    def translate(self, fullCode):
        # fullCode such as android.support.design.widget.TabLayout.g(xxyy)
        if DEBUG:
            print('translate "%s"' % fullCode)

        m = re.match('(.*)\.([^\.]+)(\(.*\))', fullCode)
        if not m:
            return fullCode

        className = m.group(1)
        functionName = m.group(2)
        others = m.group(3)
        if className not in self.finalDict:
            return fullCode
        classC = self.finalDict[className]
        actualClassName = classC.name
        actualFunctionName = functionName
        actualFunction = classC.get(functionName, isFunction=True)
        if actualFunction:
            actualFunctionName = actualFunction.name

        if others:
            return "%s.%s%s" % (actualClassName, actualFunctionName, others)
        else:
            return "%s.%s" % (actualClassName, actualFunctionName)


def parse(mappingFile):
    assert os.path.exists(mappingFile), "mappingFile %s is not exists" % mappingFile

    print('parsing')

    finalResult = {} # mappingName -> Class

    classParser = ClassParser()
    memberParser = MemberParser()
    functionParser = FunctionParser()

    currentClass = None
    with open(mappingFile, 'r') as f:
        for line in f:
            c = classParser.match(line)
            if c:
                if currentClass:
                    finalResult[currentClass.mappingName] = currentClass
                if DEBUG:
                    print('match a class %s' % c)
                currentClass = c
                continue
            f = functionParser.match(line)
            if f:
                assert currentClass, "mapping file should start with a class"
                currentClass.add(f)
                if DEBUG:
                    print('match a function %s' % f)
                continue
            m = memberParser.match(line)
            if m:
                assert currentClass, "mapping file should start with a class"
                currentClass.add(m)
                if DEBUG:
                    print('match a member %s' % m)
                continue

    if currentClass:
        finalResult[currentClass.mappingName] = currentClass

    # print it
    if DEBUG:
        print(finalResult)
    print('parse end')
    return finalResult

class ClassParser:
    def __init__(self):
        self.machine = re.compile('^([^ ]+) -> ([^:]+):')

    def match(self, line):
        m = self.machine.match(line)
        if not m:
            return None
        name = m.group(1)
        mappingName = m.group(2)
        return Class(name, mappingName)

class MemberParser:
    def __init__(self):
        self.machine = re.compile('^ {4}([^ ]+) ([^ ]+) -> (.*)')

    def match(self, line):
        m = self.machine.match(line)
        if not m:
            return None
        type = m.group(1)
        name = m.group(2)
        mappingName = m.group(3)
        return MemberVar(type, name, mappingName)

class FunctionParser:
    def __init__(self):
        self.machine = re.compile('^ {4}(([0-9]+):)?(([0-9]+):)?([^ ]+) ([^ ]+)\((.*)\) -> (.*)')

    def match(self, line):
        m = self.machine.match(line)
        if not m:
            return None
        oldLocation = m.group(2)
        newLocation = m.group(4)
        type = m.group(5)
        name = m.group(6)
        arguments = m.group(7)
        mappingName = m.group(8)
        return Function(type, name, arguments, mappingName, oldLocation, newLocation)
