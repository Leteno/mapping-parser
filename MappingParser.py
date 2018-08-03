
import os, re

from pojo import *

CLASS_STEP = 1
MEMBER_STEP = 2
def parse(mappingFile):
    assert os.path.exists(mappingFile), "mappingFile %s is not exists" % mappingFile

    finalResult = {} # mappingName -> Class

    classParser = ClassParser()
    memberParser = MemberParser()
    functionParser = FunctionParser()

    currentClass = None
    with open(mappingFile, 'r') as f:
        for line in f:
            print(line)
            c = classParser.match(line)
            if c:
                if currentClass:
                    finalResult[currentClass.mappingName] = currentClass
                print('match a class %s' % c)
                currentClass = c
                continue
            f = functionParser.match(line)
            if f:
                assert currentClass, "mapping file should start with a class"
                currentClass.add(f)
                print('match a function %s' % f)
                continue
            m = memberParser.match(line)
            if m:
                assert currentClass, "mapping file should start with a class"
                currentClass.add(m)
                print('match a member %s' % m)
                continue

    # print it
    for x in finalResult:
#        print(x)
        pass
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
  

import sys
parse(sys.argv[1])
