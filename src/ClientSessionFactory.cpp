/*
 * ClientSessionFactory.cpp
 *
 *  Created on: 5 Jun 2017
 *      Author: pnikiel
 */

#include <ClientSessionFactory.h>

#include <iostream>

UaClientSdk::UaSession* ClientSessionFactory::connect(const UaString& sUrl)
{
	UaClientSdk::UaSession* session;

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
        new MyCallBack () );        // Callback interface

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


