# @author Piotr Nikiel <piotr.nikiel@gmail.com>

import sys
import os
sys.path.insert(0, 'FrameworkInternals')

from transformDesign import transformDesign

def runGenerator(className):
    output_header = os.path.join('UaoForQuasar','generated','{0}.h'.format(className))
    output_body = os.path.join('UaoForQuasar','generated','{0}.cpp'.format(className))
    additionalParam='className={0}'.format(className)
    transformDesign(
        xsltTransformation=os.path.join('UaoForQuasar', 'xslt', 'designToClassHeader.xslt'), 
        outputFile=output_header, 
        overwriteProtection=0, 
        astyleRun=True, 
        additionalParam=additionalParam)

    transformDesign(
        xsltTransformation=os.path.join('UaoForQuasar', 'xslt', 'designToClassBody.xslt'), 
        outputFile=output_body, 
        overwriteProtection=0, 
        astyleRun=True, 
        additionalParam=additionalParam)
    
def main():
    className = sys.argv[1]
    runGenerator(className)
    
if __name__=="__main__":
    main()
    
    

