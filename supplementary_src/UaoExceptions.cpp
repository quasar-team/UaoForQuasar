/*
 * UaoExceptions.cpp
 *
 *  Created on: 15 Apr 2019
 *      Author: pnikiel
 */

#include <sstream>

namespace UaoClient
{
namespace Exceptions
{

template<typename T>
static std::string toHexString (const T t, unsigned int width=0, char zeropad=' ')
{
        std::ostringstream oss;
        oss << std::hex;
        if (width > 0)
        {
            oss.width(width);
            oss.fill(zeropad);
        }
        oss << (unsigned long)t << std::dec;
        return oss.str ();
}

BadStatusCode::BadStatusCode (const std::string& what, OpcUa_StatusCode statusCode):
    std::runtime_error(
            "BadStatusCode exception: "+
            what+
            " [statuscode=0x"+
            toHexString(statusCode)+
            " explanation='"+
            UaStatus(statusCode).toString().toUtf8()+
            "']"),
    m_statusCode(statusCode)
{

}

}
}
