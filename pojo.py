
class Class:
    def __init__(self, name, mappingName):
        self.name = name
        self.mappingName = mappingName
        self.children = []

    def add(self, child):
        self.children.append(child)

    def get(self, childMappingName, isFunction=True):
        for c in self.children:
            if isFunction and not isinstance(c, Function):
                continue
            if not isFunction and not isinstance(c, MemberVar):
                continue
            if c.mappingName == childMappingName:
                return c

    def __str__(self):
        childrenWords = ""
        for child in self.children:
            childrenWords += "%s," % child
        return "{name: %s, mappingName: %s, [%s]}" % (self.name, self.mappingName, childrenWords)

class MemberVar:
    def __init__(self, type, name, mappingName, oldLocation=None, newLocation=None):
        self.type = type
        self.name = name
        self.mappingName = mappingName
        self.oldLocation = oldLocation
        self.newLocation = newLocation

    def __str__(self):
        return "{type: %s, name: %s, mappingName: %s}" % (self.type, self.name, self.mappingName)

class Function:
    def __init__(self, type, name, arguments, mappingName, oldLocation=None, newLocation=None):
        self.type = type
        self.name = name
        self.arguments = arguments
        self.mappingName = mappingName
        self.oldLocation = oldLocation
        self.newLocation = newLocation

    def __str__(self):
        return "{type: %s, name: %s, args: %s, mappingName: %s, oldLoc: %s, newLoc: %s}" % \
            (self.type, self.name, self.arguments, self.mappingName, self.oldLocation, self.newLocation)
