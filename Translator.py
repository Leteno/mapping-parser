
import re

import MappingParser

class Translator:
    def __init__(self, mappingFile):
        self.parser = MappingParser.Parser(mappingFile)
        self.fullCodeRetriver = re.compile(r'\b[^\( ]+\([^\)]+\)')

    def translate(self, fullContent):
        result = ""
        start = 0
        m = self.fullCodeRetriver.search(fullContent, start)
        while m:

            # letters before
            letterStart = m.start()
            result += fullContent[start:letterStart]

            # letters
            letters = m.group(0)
            translations = self.parser.translate(letters)
            result += translations

            # letters after
            # pass

            start = m.end()
            m = self.fullCodeRetriver.search(fullContent, start)

        #  the rest
        result += fullContent[start:]

        return result
