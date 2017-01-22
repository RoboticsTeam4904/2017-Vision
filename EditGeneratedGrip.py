import re

def openCode(doc):
    code = open(doc, 'r')
    code = code.read()
    return code

def saveCode(doc, code):
    output = open(doc,"w")
    output.write(code)

def editCode(doc, withOpenCV3=True):
    code = openCode(doc)
    if withOpenCV3:
        code = re.sub('    contours, hierarchy =cv2.findContours', 'im2, contours, hierarchy =cv2.findContours', code)
        #code = re.sub(r'im2, ?contours, hierarchy =cv2.findContours', 'im2, contours, hierarchy =cv2.findContours', code)
    else:
        code = re.sub('im2, contours, hierarchy =cv2.findContours', 'contours, hierarchy =cv2.findContours', code)
    code = re.sub('import numpy\nimport math\nfrom enum import Enum', '#import numpy\n#import math\n#from enum import Enum', code)
    code = re.sub('class GripPipeline:', 'class GripVisionPipeline:', code)
    saveCode(doc, code)

# editCode('grip.py')
