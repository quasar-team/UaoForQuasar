

// generated: 2019-01-17T14:41:35.144+01:00

#include <iostream>
#include <uaclient/uaclientsdk.h>

namespace UaoClient
{

using namespace UaClientSdk;



class CalculatedVariable
{

public:

    CalculatedVariable(
        UaSession* session,
        UaNodeId objId
    );

// getters, setters for all variables
    OpcUa_Double readValue (
        UaStatus      *out_status=nullptr,
        UaDateTime    *sourceTimeStamp=nullptr,
        UaDateTime    *serverTimeStamp=nullptr);


private:

    UaSession  * m_session;
    UaNodeId     m_objId;

};



}

