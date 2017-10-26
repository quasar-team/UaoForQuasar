/*
 * ClientSession.h
 *
 *  Created on: 5 Jun 2017
 *      Author: pnikiel
 */

#ifndef DEVICE_INCLUDE_CLIENTSESSIONFACTORY_H_
#define DEVICE_INCLUDE_CLIENTSESSIONFACTORY_H_

#include <uaclient/uasession.h>


class MyCallBack : public UaClientSdk::UaSessionCallback
{
	virtual void connectionStatusChanged(OpcUa_UInt32, UaClientSdk::UaClient::ServerStatus)
	{
		// from here print about connection status
	}

};

class ClientSessionFactory
{
public:

	static UaClientSdk::UaSession* connect(const UaString& sUrl);

};

#endif /* DEVICE_INCLUDE_CLIENTSESSIONFACTORY_H_ */
