/*
 * ClientSessionFactory.cpp
 *
 *  Created on: 5 Jun 2017
 *      Author: pnikiel
 */

#include <UaoExceptions.h>
#include <ClientSessionFactory.h>
#include <LogIt.h>
#include <unistd.h>
#include <limits.h>

UaClientSdk::UaSession* ClientSessionFactory::connect(const UaString& sUrl)
{
	UaClientSdk::UaSession* session (nullptr);

	UaClientSdk::SessionSecurityInfo security;

    session = new UaClientSdk::UaSession();

    UaClientSdk::SessionConnectInfo sessionConnectInfo;
    sessionConnectInfo.sApplicationName = "Client_Cpp_SDK@myComputer";
    sessionConnectInfo.sApplicationUri  = "Client_Cpp_SDK@myComputer";
    sessionConnectInfo.sProductUri      = "Client_Cpp_SDK";
    /*********************************************************************
     Connect to OPC UA Server
    **********************************************************************/
    UaStatus status = session->connect(
        sUrl,                // URL of the Endpoint - from discovery or config
        sessionConnectInfo,  // General settings for connection
        security, // Security settings
        nullptr );        // Callback interface

    /*********************************************************************/
    if ( status.isBad() )
    {
    	std::cout << "Error in connect" << std::endl;
    	return 0;
    }
    else
    {
    	//std::cout << "Connected!" << std::endl;
    	return session;
    }
}

UaClientSdk::UaSession* ClientSessionFactory::tryConnect(
        const UaString& sUrl,
        unsigned int numAttempts,
        unsigned int delayBetweenAttemptsMs)
{
    if (numAttempts<1)
        throw std::runtime_error("It is better to attempt at least once, check your arguments!");

    UaClientSdk::UaSession* session(nullptr);
    UaClientSdk::SessionSecurityInfo security;

    // establishing hostname
    char hostNameVanilla [HOST_NAME_MAX+1] = {0};
    std::string hostName;
    if (gethostname(hostNameVanilla, sizeof hostNameVanilla / sizeof (hostNameVanilla[0])) == 0)
        hostName = hostNameVanilla;
    else
    {
        LOG(Log::WRN) << "Didn't manage to resolve host name, will fake it!";
        hostName = "someUnresolvedHostName";
    }

    // prep a random number to generate URI
    unsigned int randomNumber = rand();

    // preparing session connect info
    UaClientSdk::SessionConnectInfo sessionConnectInfo;
    sessionConnectInfo.sApplicationName = ("UaoClient@"+hostName).c_str();
    sessionConnectInfo.sApplicationUri = sessionConnectInfo.sApplicationName + "#" + std::to_string(randomNumber).c_str();
    sessionConnectInfo.sProductUri = "UaoClient";

    // prep callback interface
    UaClientSdk::UaSessionCallback* callback = new MyCallBack();

    // connecting
    UaStatus status;
    session = new UaClientSdk::UaSession();
    unsigned int connectAttempts = 1;
    do
    {
        status = session->connect(
            sUrl,
            sessionConnectInfo,
            security,
            callback);
        if (status.isGood())
        {
            LOG(Log::INF) << "Connected to " << sUrl.toUtf8() << " after " << connectAttempts << " connect attempts.";
            return session;
        }
        else
        {
            if (connectAttempts < numAttempts)
            {
                LOG(Log::WRN) << "Will retry to connect to " << sUrl.toUtf8() << " (so far after " << connectAttempts << " attempts) in " << delayBetweenAttemptsMs << "ms";
                usleep(delayBetweenAttemptsMs * 1000);
            }
        }
        connectAttempts++;
    }
    while (connectAttempts < numAttempts);
    LOG(Log::ERR) << "Failed to connect to " << sUrl.toUtf8() << " after " << connectAttempts << " attempts, bailing out.";
    delete session;
    delete callback;
    throw UaoClient::Exceptions::BadStatusCode("tryConnect()", status.statusCode());
}
