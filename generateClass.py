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
from os import path
from colorama import Fore, Style
import argparse

uao_path = os.path.abspath(os.path.dirname(__file__))
quasar_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), os.pardir))

try:
    sys.path.insert(0, os.path.join(quasar_path, 'FrameworkInternals'))
except OSError:
    if not path.exists(os.path.join(quasar_path, 'FrameworkInternals')):
        sys.exit(
            'Please check that UaoForQuasar is directly deployed in a quasar project')

import quasar_basic_utils
from transformDesign import transformDesign

sys.path.insert(0, os.path.join(uao_path, 'Uaotilities'))

from Delphi import Delphi

def runGenerator(className, uaoDirectory='UaoForQuasar', namespace='UaoClient'):
    output_header = os.path.join(
        uaoDirectory, 'generated', '{0}.h'.format(className))
    output_body = os.path.join(
        uaoDirectory, 'generated', '{0}.cpp'.format(className))

    print(Fore.GREEN + 'Using Jinja2 engine' + Style.RESET_ALL)
    templatesPath = 'templates'
    transformPostfix = 'jinja'

    adyton = Delphi()

    additionalParam = {
        'className': className,
        'namespace': namespace,
        'readPronouncementToType': adyton.readPronouncementToType}

    try:
        design_path = os.path.join(quasar_path, 'Design', 'Design.xml')
        transformDesign(
            transform_path=os.path.join(
                uaoDirectory, templatesPath, 'designToClassHeader.' + transformPostfix),
            designXmlPath=design_path,
            outputFile=output_header,
            requiresMerge=False,
            astyleRun=True,
            additionalParam=additionalParam)

        transformDesign(
            transform_path=os.path.join(
                uaoDirectory, templatesPath, 'designToClassBody.' + transformPostfix),
            designXmlPath=design_path,
            outputFile=output_body,
            requiresMerge=False,
            astyleRun=True,
            additionalParam=additionalParam)

    except:
        quasar_basic_utils.quasaric_exception_handler()


def main():
    parser = argparse.ArgumentParser(
        description='Creates OPC-UA clients for C++, see: https://github.com/quasar-team/UaoForQuasar')
    parser.add_argument('--namespace', default='UaoClient', help="C++ namespace")
    parser.add_argument('quasar_class', help="quasar class which you want to get generated")

    args = parser.parse_args()

    runGenerator(args.quasar_class, namespace = args.namespace)


if __name__ == "__main__":
    main()
