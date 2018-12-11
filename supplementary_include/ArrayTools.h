/* © Copyright CERN, 2018.  All rights not expressly granted are reserved.
 * ArrayTools.h
 *
 *  Created on: Jan 15, 2018
 *      Author: mludwig, pnikiel
 *
 *  This file is part of Quasar.
 *
 *  Quasar is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Lesser General Public Licence as published by
 *  the Free Software Foundation, either version 3 of the Licence.
 *
 *  Quasar is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Lesser General Public Licence for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public License
 *  along with Quasar.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef UAO_CLIENT_OPCUA_SCA_ARRAYUTILS_H_
#define UAO_CLIENT_OPCUA_SCA_ARRAYUTILS_H_

#include <vector>
#include <uavariant.h>

namespace UaoClientForOpcUaSca
{

/* Note: Boolean and Byte converters are not done through overloading because in the UASDK they both resolve to the same primitive type (unsigned char). */

namespace ArrayTools
{


	void convertBooleanVectorToUaVariant( const std::vector<OpcUa_Boolean>& input, UaVariant& output );
	void convertByteVectorToUaVariant( const std::vector<OpcUa_Byte>& input, UaVariant& output);
	void convertVectorToUaVariant( const std::vector <OpcUa_SByte>& input, UaVariant& output  );
	void convertVectorToUaVariant( const std::vector <OpcUa_Int16>& input, UaVariant& output  );
	void convertVectorToUaVariant( const std::vector <OpcUa_UInt16>& input, UaVariant& output  );
	void convertVectorToUaVariant( const std::vector <OpcUa_Int32>& input, UaVariant& output );
	void convertVectorToUaVariant( const std::vector <OpcUa_UInt32>& input, UaVariant& output );
	void convertVectorToUaVariant( const std::vector <OpcUa_Int64>& input, UaVariant& output  );
	void convertVectorToUaVariant( const std::vector <OpcUa_UInt64>& input, UaVariant& output  );
	void convertVectorToUaVariant( const std::vector <OpcUa_Float>& input, UaVariant& output );
	void convertVectorToUaVariant( const std::vector <OpcUa_Double>& input, UaVariant& output  );
	void convertVectorToUaVariant( const std::vector <UaString>& input, UaVariant& output );

	UaStatus convertUaVariantToBooleanVector( const UaVariant& input, std::vector <OpcUa_Boolean> &vect );
	UaStatus convertUaVariantToByteVector( const UaVariant& input, std::vector <OpcUa_Byte> &vect );
	UaStatus convertUaVariantToVector( const UaVariant& input, std::vector <OpcUa_SByte> &vect );
	UaStatus convertUaVariantToVector( const UaVariant& input, std::vector <OpcUa_Int16> &vect );
	UaStatus convertUaVariantToVector( const UaVariant& input, std::vector <OpcUa_UInt16> &vect );
	UaStatus convertUaVariantToVector( const UaVariant& input, std::vector <OpcUa_Int32> &vect );
	UaStatus convertUaVariantToVector( const UaVariant& input, std::vector <OpcUa_UInt32> &vect );
	UaStatus convertUaVariantToVector( const UaVariant& input, std::vector <OpcUa_Int64> &vect );
	UaStatus convertUaVariantToVector( const UaVariant& input, std::vector <OpcUa_UInt64> &vect );
	UaStatus convertUaVariantToVector( const UaVariant& input, std::vector <OpcUa_Float> &vect );
	UaStatus convertUaVariantToVector( const UaVariant& input, std::vector <OpcUa_Double> &vect );
	UaStatus convertUaVariantToVector( const UaVariant& input, std::vector <UaString> &vect );

	std::vector<std::string> convertStdStringsToUaStrings( const std::vector<std::string>& input );
}

}
#endif /* UAO_CLIENT_OPCUA_SCA_ARRAYUTILS_H_ */
