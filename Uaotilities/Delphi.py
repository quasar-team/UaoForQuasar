#!/usr/bin/env python
# encoding: utf-8
'''
Delphi.py

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
from Oracle import Oracle
from transform_filters import cap_first

Pythia = Oracle()


class Delphi():

    def readPronouncementToType(self, dataType):
        """ Helper for read pronouncement based on the datatype """
        if dataType == 'UaString':
            return "out = UaVariant(dataValues[0].Value).toString();"
        else:
            return '''\
                UaStatus conversionStatus = (UaVariant(dataValues[0].Value)).{toType} (out);
                if (! conversionStatus.isGood())
                {{
                throw std::runtime_error(std::string(\"OPC-UA read: read succeeded but conversion to native type failed (was it NULL value?): \") + UaStatus(dataValues[0].StatusCode).toString().toUtf8() );
                }}\
                '''.format(toType=Pythia.data_type_to_variant_converter(dataType))
