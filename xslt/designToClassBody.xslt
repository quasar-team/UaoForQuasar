<?xml version="1.0" encoding="UTF-8"?>
<!-- Author: pnikiel -->

<xsl:transform version="2.0" xmlns:xml="http://www.w3.org/XML/1998/namespace" 
	xmlns:xs="http://www.w3.org/2001/XMLSchema" 
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:d="http://cern.ch/quasar/Design"
	xmlns:fnc="http://cern.ch/quasar/MyFunctions"
	xsi:schemaLocation="http://www.w3.org/1999/XSL/Transform schema-for-xslt20.xsd ">
	<xsl:include href="../../Design/CommonFunctions.xslt" />
	<xsl:output method="text"></xsl:output>
	<xsl:param name="className"/>
	<xsl:param name="xsltFileName"/>


	<xsl:template name="readInvocation">
	<xsl:param name="variableName"/>
	<xsl:param name="dataType"/>
	<xsl:value-of select="$dataType"/><xsl:text> </xsl:text> <xsl:value-of select="$className"/>::read<xsl:value-of select="fnc:capFirst($variableName)"/> (UaStatus *out_status)
	  {
	  
	    ServiceSettings   ss;
	    UaReadValueIds    nodesToRead;
	    UaDataValues      dataValues;
	    UaDiagnosticInfos diagnosticInfos;
	    
	    UaNodeId nodeId ( UaString(m_objId.identifierString()) + UaString(".<xsl:value-of select="$variableName"/>"), 2  );
	   
	    nodesToRead.create(1);
	    nodeId.copyTo( &amp;nodesToRead[0].NodeId );
	    nodesToRead[0].AttributeId = OpcUa_Attributes_Value;
	
	    dataValues.create (1);
	    
	  	UaStatus status = m_session->read(
			ss,
			0 /*max age*/,
			OpcUa_TimestampsToReturn_Both,
			nodesToRead,
			dataValues,
			diagnosticInfos
	  	);
	  	if (status.isBad())
	  	   throw std::runtime_error("OPC-UA read failed");
	  	if (! UaStatus(dataValues[0].StatusCode).isGood())
	  	{
	  		if (out_status)
	  			*out_status = dataValues[0].StatusCode;
	  		else
	  			throw std::runtime_error(std::string("OPC-UA read: variable status is not good") + UaStatus(dataValues[0].StatusCode).toString().toUtf8() );
	  	}
	  	<xsl:value-of select="$dataType"/> out;
	  	(UaVariant(dataValues[0].Value)).<xsl:value-of select="fnc:dataTypeToVariantConverter(@dataType)"/> (out);
	  	return out;
	    }
	
	</xsl:template>
	
	<xsl:template name="writeInvocation">
		<xsl:param name="variableName"/>
		<xsl:param name="dataType"/>
		void  <xsl:value-of select="$className"/>::write<xsl:value-of select="fnc:capFirst($variableName)"/> (<xsl:value-of select="$dataType"/> &amp; data)
	    {
	  	ServiceSettings   ss;
	    UaWriteValues    nodesToWrite;
	    UaDataValues      dataValues;
	    UaDiagnosticInfos diagnosticInfos;
	    UaStatusCodeArray results;
	   	        
	    UaNodeId nodeId ( UaString(m_objId.identifierString()) + UaString(".<xsl:value-of select="$variableName"/>"), 2  );
	   
	    nodesToWrite.create(1);
	    nodeId.copyTo( &amp;nodesToWrite[0].NodeId );
	    nodesToWrite[0].AttributeId = OpcUa_Attributes_Value;
		
		UaVariant v ( data );
		<xsl:if test="@dataType = 'UaByteString'">
			v.setByteString( data, false );
		</xsl:if>
		
	    dataValues.create (1);
	    v.copyTo( &amp;nodesToWrite[0].Value.Value );
	    
	  	UaStatus status = m_session->write(
			ss,
			nodesToWrite,
			results,
			diagnosticInfos
	  	);
	  	if (status.isBad())
	  	   throw std::runtime_error(std::string("OPC-UA write failed:") + status.toString().toUtf8() );
	  	if (results[0] != OpcUa_Good)
	  		throw std::runtime_error(std::string("OPC-UA write failed for "+std::string(nodeId.toString().toUtf8())+": one of results not good: ") + UaStatus(results[0]).toString().toUtf8() );
	
	    }	
	</xsl:template>
	
	<xsl:template name="classBody">
	
	  <xsl:value-of select="$className"/>::
	  <xsl:value-of select="$className"/>
	  (
    UaSession* session,
    UaNodeId objId
    ) :
    m_session(session),
    m_objId (objId)
    {
    
    }
	


<xsl:for-each select="d:cachevariable">
	<xsl:call-template name="readInvocation">
		<xsl:with-param name="variableName"><xsl:value-of select="@name"/></xsl:with-param>
		<xsl:with-param name="dataType"><xsl:value-of select="@dataType"/></xsl:with-param>
	</xsl:call-template>

	<xsl:if test="@addressSpaceWrite!='forbidden'">
		<xsl:call-template name="writeInvocation">
			<xsl:with-param name="variableName"><xsl:value-of select="@name"/></xsl:with-param>
			<xsl:with-param name="dataType"><xsl:value-of select="@dataType"/></xsl:with-param>	
		</xsl:call-template>
	</xsl:if>
</xsl:for-each>

<xsl:for-each select="d:sourcevariable">
	<xsl:if test="@addressSpaceRead!='forbidden'">
		<xsl:call-template name="readInvocation">
			<xsl:with-param name="variableName"><xsl:value-of select="@name"/></xsl:with-param>
			<xsl:with-param name="dataType"><xsl:value-of select="@dataType"/></xsl:with-param>
		</xsl:call-template>
	</xsl:if>
	<xsl:if test="@addressSpaceWrite!='forbidden'">
		<xsl:call-template name="writeInvocation">
			<xsl:with-param name="variableName"><xsl:value-of select="@name"/></xsl:with-param>
			<xsl:with-param name="dataType"><xsl:value-of select="@dataType"/></xsl:with-param>
		</xsl:call-template>	
	</xsl:if>
</xsl:for-each>

<xsl:for-each select="d:method">
  void <xsl:value-of select="$className"/>::<xsl:value-of select="@name"/> (
  	<xsl:for-each select="d:argument">
  		<xsl:value-of select="@dataType"/> &amp; in_<xsl:value-of select="@name"/><xsl:if test="position() &lt; count(../d:argument)+count(../d:returnvalue)">,</xsl:if>
  		
  	</xsl:for-each>
  	<xsl:for-each select="d:returnvalue">
  		<xsl:value-of select="@dataType"/> &amp; in_<xsl:value-of select="@name"/><xsl:if test="position() &lt; count(../d:returnvalue)">,</xsl:if>
  	</xsl:for-each>
  )
  {
  	
  	ServiceSettings serviceSettings;
  	CallIn callRequest;
  	CallOut co;
  	
  	callRequest.objectId = m_objId;
  	callRequest.methodId = UaNodeId( UaString(m_objId.identifierString()) + UaString(".<xsl:value-of select="@name"/>"), 2 );

  	
  	UaVariant v;
  	
  	<xsl:if test="d:argument">
  	callRequest.inputArguments.create( <xsl:value-of select="count(d:argument)"/> );
	  	<xsl:for-each select="d:argument">
	  	<xsl:choose>
	  		<xsl:when test="@dataType='UaByteString'">
	  			v.setByteString( in_<xsl:value-of select="@name"/>, false );
	  		</xsl:when>
	  		<xsl:otherwise>
	  			<xsl:message terminate="yes">not-implememnted</xsl:message>
	  		</xsl:otherwise>
	  	</xsl:choose>
	  	v.copyTo( &amp;callRequest.inputArguments[ <xsl:value-of select="position()-1"/> ] );
	  	</xsl:for-each>
  	</xsl:if>
  	
  	
  	UaStatus status =
  	m_session->call(
  			serviceSettings,
  			callRequest,
  			co
  		);
  	if (status.isBad())
  		throw std::runtime_error(std::string("bad-status: ")+status.toString().toUtf8());
  	
  	<xsl:for-each select="d:returnvalue">
	   	v = co.outputArguments[<xsl:value-of select="position()-1"/>];
 	 	v.toByteString(in_<xsl:value-of select="@name"/>); 	
  	</xsl:for-each>	

  
  }

</xsl:for-each>

	</xsl:template>
	
	<xsl:template match="/">	

	#include &lt;iostream&gt;
	#include &lt;<xsl:value-of select="$className"/>.h&gt;
	#include &lt;uaclient/uasession.h&gt;
	#include &lt;stdexcept&gt;
	
	<xsl:if test="not(/d:design/d:class[@name=$className])">
		<xsl:message terminate="yes">Class not found.</xsl:message>
	</xsl:if>
	<xsl:for-each select="/d:design/d:class[@name=$className]">
	<xsl:call-template name="classBody"/>
	</xsl:for-each>
	</xsl:template>



</xsl:transform>
