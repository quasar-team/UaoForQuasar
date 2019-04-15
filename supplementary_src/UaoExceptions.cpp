/*
 * UaoExceptions.cpp
 *
 *  Created on: 15 Apr 2019
 *      Author: pnikiel
 */

#include <UaoExceptions.h>
#include <sstream>

namespace UaoClient
{
namespace Exceptions
{

std::string BadStatusCode::what() const
{
    std::stringstream ss;
    ss << "BadStatusCode exception: " <<  what();
    ss << " [statuscode=" << std::hex << m_statusCode;
    ss << " explanation='" << UaStatus(m_statusCode).toString() << "']";
    return ss.str();
}

}
}
