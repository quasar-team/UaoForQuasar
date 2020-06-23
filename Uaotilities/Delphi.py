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

    def readPronouncement(self, className, variableName, dataType):
        output = dataType + " " + className + "::read" + cap_first(variableName) + " (\n"
        output += "UaStatus *out_status,\n"
        output += "UaDateTime *sourceTimeStamp,\n"
        output += "UaDateTime *serverTimeStamp)\n"
        output += "{\n\n"
        output += "ServiceSettings   ss;\n"
        output += "UaReadValueIds    nodesToRead;\n"
        output += "UaDataValues      dataValues;\n"
        output += "UaDiagnosticInfos diagnosticInfos;\n\n"
        output += "UaNodeId nodeId ( UaString(m_objId.identifierString()) + UaString(\"." + variableName + "\"), m_objId.namespaceIndex() );\n\n"
        output += "nodesToRead.create(1);\n"
        output += "nodeId.copyTo( &nodesToRead[0].NodeId );\n"
        output += "nodesToRead[0].AttributeId = OpcUa_Attributes_Value;\n\n"
        output += "dataValues.create (1);\n\n"
        output += "UaStatus status = m_session->read(\n"
        output += "ss,\n"
        output += "0 /*max age*/,\n"
        output += "OpcUa_TimestampsToReturn_Both,\n"
        output += "nodesToRead,\n"
        output += "dataValues,\n"
        output += "diagnosticInfos\n"
        output += ");\n"
        output += "if (status.isBad())\n"
        output += "throw Exceptions::BadStatusCode(\"OPC-UA read failed\", status.statusCode());\n"
        output += "if (out_status)\n"
        output += "*out_status = dataValues[0].StatusCode;\n"
        output += "else\n"
        output += "{\n"
        output += "if (! UaStatus(dataValues[0].StatusCode).isGood())\n"
        output += "throw Exceptions::BadStatusCode(\"OPC-UA read: variable status is not good\", dataValues[0].StatusCode );\n"
        output += "}\n\n"
        output += dataType + " out;\n\n\n";
        if dataType == 'UaString':
            output += "out = UaVariant(dataValues[0].Value).toString();\n"
        else:
            output += "UaStatus conversionStatus = (UaVariant(dataValues[0].Value))." + Pythia.data_type_to_variant_converter(dataType) + " (out);\n"
            output += "if (! conversionStatus.isGood())\n"
            output += "{\n"
            output += "throw std::runtime_error(std::string(\"OPC-UA read: read succeeded but conversion to native type failed (was it NULL value?): \") + UaStatus(dataValues[0].StatusCode).toString().toUtf8() );\n"
            output += "}\n"
        output += "\n\n"
        output += "if (sourceTimeStamp)\n"
        output += "*sourceTimeStamp = dataValues[0].SourceTimestamp;\n"
        output += "if (serverTimeStamp)\n"
        output += "*serverTimeStamp = dataValues[0].ServerTimestamp;\n\n"
        output += "return out;\n"
        output += "}\n"
        return output

    def writePronouncement(self, className, variableName, dataType):
        output = "void  " + className + "::write" + cap_first(variableName) + " (\n"
        output += dataType + " & data,\n"
        output += "UaStatus *out_status)\n"
        output += "{\n"
        output += "ServiceSettings   ss;\n"
        output += "UaWriteValues    nodesToWrite;\n"
        output += "UaDataValues      dataValues;\n"
        output += "UaDiagnosticInfos diagnosticInfos;\n"
        output += "UaStatusCodeArray results;\n\n"
        output += "UaNodeId nodeId ( UaString(m_objId.identifierString()) + UaString(\"." + variableName + "\"), m_objId.namespaceIndex()  );\n\n"
        output += "nodesToWrite.create(1);\n"
        output += "nodeId.copyTo( &nodesToWrite[0].NodeId );\n"
        output += "nodesToWrite[0].AttributeId = OpcUa_Attributes_Value;\n\n"
        output += "UaVariant v ( data );\n\n"
        if dataType == 'UaByteString':
            output += "v.setByteString( data, false );\n\n"
        output += "\n"
        output += "dataValues.create (1);\n"
        output += "v.copyTo( &nodesToWrite[0].Value.Value );\n\n"
        output += "UaStatus status = m_session->write(\n"
        output += "ss,\n"
        output += "nodesToWrite,\n"
        output += "results,\n"
        output += "diagnosticInfos\n"
        output += ");\n"
        output += "if (out_status)\n"
        output += "{\n"
        output += "*out_status = status;\n"
        output += "}\n"
        output += "else\n"
        output += "{\n"
        output += "if (status.isBad())\n"
        output += "throw Exceptions::BadStatusCode(\"OPC-UA write failed\", status.statusCode() );\n"
        output += "if (results[0] != OpcUa_Good)\n"
        output += "throw Exceptions::BadStatusCode (\"OPC-UA write failed\", results[0] );\n"
        output += "}\n\n"
        output += "}"
        return output

