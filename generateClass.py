# @author Piotr Nikiel <piotr.nikiel@gmail.com>

import sys
import os
sys.path.insert(0, 'FrameworkInternals')

uao_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(uao_path, 'Uaotilities'))

from Delphi import Delphi

from transformDesign import transformDesign
import quasar_basic_utils

def runGenerator(className,uaoDirectory='UaoForQuasar', namespace='UaoClient'):
    output_header = os.path.join(uaoDirectory,'generated','{0}.h'.format(className))
    output_body = os.path.join(uaoDirectory,'generated','{0}.cpp'.format(className))

    # Those 2 are here only for debugging and backwards compatibility. 
    output_body_jinja = os.path.join(uaoDirectory,'generated','{0}_jinja.cpp'.format(className))
    #output_header_xslt = os.path.join(uaoDirectory,'generated','{0}_xslt.h'.format(className))

    adyton = Delphi()

    additionalParam = {
        'className'             : className, 
        'namespace'             : namespace,
        'readPronouncement'     : adyton.readPronouncement,
        'writePronouncement'    : adyton.writePronouncement}

    try:
        transformDesign(
            xsltTransformation=os.path.join(uaoDirectory, 'templates', 'designToClassHeader.jinja'),
            outputFile=output_header, 
            requiresMerge=False, 
            astyleRun=True, 
            additionalParam=additionalParam)

        transformDesign(
            xsltTransformation=os.path.join(uaoDirectory, 'templates', 'designToClassBody.jinja'),
            outputFile=output_body_jinja, 
            requiresMerge=False, 
            astyleRun=True, 
            additionalParam=additionalParam)

        transformDesign(
            xsltTransformation=os.path.join(uaoDirectory, 'xslt', 'designToClassBody.xslt'), 
            outputFile=output_body, 
            requiresMerge=False, 
            astyleRun=True, 
            additionalParam=additionalParam)

        #transformDesign(
        #    xsltTransformation=os.path.join(uaoDirectory, 'xslt', 'designToClassHeader.xslt'), 
        #    outputFile=output_header_xslt, 
        #    requiresMerge=False, 
        #    astyleRun=True, 
        #    additionalParam=additionalParam)

    except:
        quasar_basic_utils.quasaric_exception_handler()
    
def main():
    className = sys.argv[1]
    runGenerator(className)
    
if __name__=="__main__":
    main()
    
    

