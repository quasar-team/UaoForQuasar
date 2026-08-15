

// generated: 2019-01-17T14:41:35.144+01:00

#ifndef UAO_CLIENT_CALCULATEDVARIABLE_H_
#define UAO_CLIENT_CALCULATEDVARIABLE_H_

#include <iostream>
#include <uaclientsdk.h>

namespace UaoClient
{

using namespace UaClientSdk;



class CalculatedVariable
{

public:

    CalculatedVariable(
        UaClientSdk::UaSession* session,
        UaNodeId objId
    );

// getters, setters for all variables
    OpcUa_Double readValue (
        UaStatus      *out_status=nullptr,
        UaDateTime    *sourceTimeStamp=nullptr,
        UaDateTime    *serverTimeStamp=nullptr);


private:

    UaClientSdk::UaSession* m_session;
    UaNodeId                m_objId;

};



}

#endif
