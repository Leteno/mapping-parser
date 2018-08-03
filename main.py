
import os

from Translator import *

def test():
    translator = Translator('template.mapping')
    filename = 'template.dat'
    f = open(filename, 'r')
    assert f, "error when open %s" % filename
    content = f.read()
    print('before: \n%s\n' % content)
    translation = translator.translate(content)
    print('after: \n%s\n' % translation)

test()
