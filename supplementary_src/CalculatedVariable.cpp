

// generated: 2019-01-17T14:41:35.954+01:00



#include <iostream>
#include <CalculatedVariable.h>
#include <uaclient/uasession.h>
#include <stdexcept>
#include <UaoClientArrayTools.h>

namespace UaoClient
{


CalculatedVariable::
CalculatedVariable
(
    UaSession* session,
    UaNodeId objId
) :
    m_session(session),
    m_objId (objId)
{

}



OpcUa_Double CalculatedVariable::readValue (
    UaStatus *out_status,
    UaDateTime *sourceTimeStamp,
    UaDateTime *serverTimeStamp)
{

    ServiceSettings   ss;
    UaReadValueIds    nodesToRead;
    UaDataValues      dataValues;
    UaDiagnosticInfos diagnosticInfos;

    UaNodeId nodeId ( UaString(m_objId.identifierString()), m_objId.namespaceIndex() );

    nodesToRead.create(1);
    nodeId.copyTo( &nodesToRead[0].NodeId );
    nodesToRead[0].AttributeId = OpcUa_Attributes_Value;

    dataValues.create (1);

    UaStatus status = m_session->read(
                          ss,
                          0 /*max age*/,
                          OpcUa_TimestampsToReturn_Both,
                          nodesToRead,
                          dataValues,
                          diagnosticInfos
                      );
    if (status.isBad())
        throw std::runtime_error(std::string("OPC-UA read failed:")+status.toString().toUtf8());
    if (out_status)
        *out_status = dataValues[0].StatusCode;
    else
    {
        if (! UaStatus(dataValues[0].StatusCode).isGood())
            throw std::runtime_error(std::string("OPC-UA read: variable status is not good") + UaStatus(dataValues[0].StatusCode).toString().toUtf8() );
    }

    OpcUa_Double out;


    UaStatus conversionStatus = (UaVariant(dataValues[0].Value)).toDouble (out);
    if (! conversionStatus.isGood())
    {
        throw std::runtime_error(std::string("OPC-UA read: read succeeded but conversion to native type failed (was it NULL value?): ") + UaStatus(dataValues[0].StatusCode).toString().toUtf8() );
    }


    if (sourceTimeStamp)
        *sourceTimeStamp = dataValues[0].SourceTimestamp;
    if (serverTimeStamp)
        *serverTimeStamp = dataValues[0].ServerTimestamp;

    return out;
}



}


