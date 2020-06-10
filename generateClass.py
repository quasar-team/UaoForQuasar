#!/usr/bin/env python
# encoding: utf-8
'''
generateClass.py

@author:     Piotr Nikiel <piotr.nikiel@gmail.com>
@author:     Paris Moschovakos <paris.moschovakos@cern.ch>

@copyright:  2020 CERN

@license:
Copyright (c) 2020, CERN.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT  HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS  OR IMPLIED  WARRANTIES, INCLUDING, BUT NOT  LIMITED TO, THE IMPLIED
WARRANTIES  OF  MERCHANTABILITY  AND  FITNESS  FOR  A  PARTICULAR  PURPOSE  ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL,  SPECIAL, EXEMPLARY, OR  CONSEQUENTIAL DAMAGES
(INCLUDING, BUT  NOT LIMITED TO,  PROCUREMENT OF  SUBSTITUTE GOODS OR  SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS  INTERRUPTION) HOWEVER CAUSED AND ON
ANY  THEORY  OF  LIABILITY,   WHETHER IN  CONTRACT, STRICT  LIABILITY,  OR  TORT
(INCLUDING  NEGLIGENCE OR OTHERWISE)  ARISING IN ANY WAY OUT OF  THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
@contact:    quasar-developers@cern.ch
'''

import sys
import os
from colorama import Fore, Style

sys.path.insert(0, 'FrameworkInternals')

from transformDesign import transformDesign
import quasar_basic_utils

uao_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(uao_path, 'Uaotilities'))

from Delphi import Delphi

# As of June 2020 the default engine for code generation is Jinja2. A fallback mode is 
# kept temporarely and can be enabled by using the following switch
XSLT_GENERATOR = False

def runGenerator(className,uaoDirectory='UaoForQuasar', namespace='UaoClient', xsltGenerator=XSLT_GENERATOR):
    output_header = os.path.join(uaoDirectory,'generated','{0}.h'.format(className))
    output_body = os.path.join(uaoDirectory,'generated','{0}.cpp'.format(className))


    if xsltGenerator:
        print(Fore.RED + 'Using XSLT engine' + Style.RESET_ALL)
        templatesPath = 'xslt'
        transformPostfix = 'xslt'
    else:
        print(Fore.GREEN + 'Using Jinja2 engine' + Style.RESET_ALL)
        templatesPath = 'templates'
        transformPostfix = 'jinja'

    adyton = Delphi()

    additionalParam = {
        'className'             : className, 
        'namespace'             : namespace,
        'readPronouncement'     : adyton.readPronouncement,
        'writePronouncement'    : adyton.writePronouncement}

    try:
        transformDesign(
            xsltTransformation=os.path.join(uaoDirectory, templatesPath, 'designToClassHeader.' + transformPostfix),
            outputFile=output_header, 
            requiresMerge=False, 
            astyleRun=True, 
            additionalParam=additionalParam)

        transformDesign(
            xsltTransformation=os.path.join(uaoDirectory, templatesPath, 'designToClassBody.' + transformPostfix),
            outputFile=output_body, 
            requiresMerge=False, 
            astyleRun=True, 
            additionalParam=additionalParam)

    except:
        quasar_basic_utils.quasaric_exception_handler()
    
def main():
    className = sys.argv[1]
    runGenerator(className)
    
if __name__=="__main__":
    main()
    
    
