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

	/** Throws a BadStatusCode exception with respective status code if given
	 * number of attempts didn't result in a connection.
	 */
	static UaClientSdk::UaSession* tryConnect(
	        const UaString& sUrl,
	        unsigned int numAttempts=10,
	        unsigned int delayBetweenAttemptsMs=1000);

};

#endif /* DEVICE_INCLUDE_CLIENTSESSIONFACTORY_H_ */