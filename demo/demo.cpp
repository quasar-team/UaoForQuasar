/*
 * demo.cpp
 *
 *  Created on: 25 Oct 2017
 *      Author: pnikiel
 *
 *    This is a small demo program
 *    that illustrates how you can use your
 *    generated client.
 */

// the following file is provided with UaoForQuasar
#include <ClientSessionFactory.h>

// the following comes from generation
// you might need to use another class
#include <HilariousClass.h>

#include <uaplatformlayer.h>
#include <iostream>

int main()
{
    UaPlatformLayer::init();

    UaClientSdk::UaSession* session = ClientSessionFactory::connect("opc.tcp://127.0.0.1:4841");
    if (!session)
        return -1;

    HilariousClass hc (session, UaNodeId("hc1",2));
    while(1)
    {
        std::cout << "value=" << hc.readHilariousVariable() << std::endl;
        usleep(1000000);
    }
}




