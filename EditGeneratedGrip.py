import re

not3 = True

def openCode(doc):
    code = open(doc, 'r')
    code = code.read()
    return code

def saveCode(doc, code):
    output = open(doc,"w")
    output.write(code)

def editCode(doc):
    code = openCode(doc)
    if not3:
        code = re.sub('im2, ', '', code)
    code = re.sub('\n from enum import Enum', '', code)
    saveCode(doc, code)
