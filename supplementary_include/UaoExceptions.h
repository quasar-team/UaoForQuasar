/*
 * UaoExceptions.h
 *
 *  Created on: 15 Apr 2019
 *      Author: pnikiel
 */

#ifndef SUPPLEMENTARY_INCLUDE_UAOEXCEPTIONS_H_
#define SUPPLEMENTARY_INCLUDE_UAOEXCEPTIONS_H_

#include <stdexcept>
#include <statuscode.h>

namespace UaoClient
{

namespace Exceptions
{

class BadStatusCode: public std::runtime_error
{
    public:
    BadStatusCode (const std::string& what, OpcUa_StatusCode statusCode);

    OpcUa_StatusCode statusCode() const { return m_statusCode; }

    private:
    OpcUa_StatusCode m_statusCode;

};

}

}



#endif /* SUPPLEMENTARY_INCLUDE_UAOEXCEPTIONS_H_ */
