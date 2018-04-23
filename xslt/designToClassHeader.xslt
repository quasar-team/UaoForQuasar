<?xml version="1.0" encoding="UTF-8"?>
<!-- author pnikiel -->
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

	
	<xsl:template name="classBody">

class <xsl:value-of select="$className"/> 
{

public:

  <xsl:value-of select="$className"/>(
    UaSession* session,
    UaNodeId objId
    );

// getters, setters for all variables
<xsl:for-each select="d:cachevariable">
  <xsl:value-of select="@dataType"/><xsl:text> </xsl:text>read<xsl:value-of select="fnc:capFirst(@name)"/> (
  	UaStatus      *out_status=nullptr,
  	UaDateTime    *sourceTimeStamp=nullptr,
    UaDateTime    *serverTimeStamp=nullptr);
  <xsl:if test="@addressSpaceWrite!='forbidden'">
  void write<xsl:value-of select="fnc:capFirst(@name)"/> (
  	<xsl:value-of select="@dataType"/> &amp; data,
  	UaStatus                                 *out_status=nullptr);
  </xsl:if>
</xsl:for-each>

<xsl:for-each select="d:sourcevariable">
	<xsl:if test="@addressSpaceRead!='forbidden'">
		<xsl:value-of select="@dataType"/><xsl:text> </xsl:text>read<xsl:value-of select="fnc:capFirst(@name)"/> (
		UaStatus     *out_status=nullptr,
		UaDateTime   *sourceTimeStamp=nullptr,
        UaDateTime   *serverTimeStamp=nullptr);
	</xsl:if>

  	<xsl:if test="@addressSpaceWrite!='forbidden'">
  		void write<xsl:value-of select="fnc:capFirst(@name)"/> (
  		<xsl:value-of select="@dataType"/> &amp; data,
  	    UaStatus                                 *out_status=nullptr);
  	</xsl:if>
</xsl:for-each>

<xsl:for-each select="d:method">
  void <xsl:value-of select="@name"/>(
    	<xsl:for-each select="d:argument">
  		<xsl:value-of select="fnc:fixDataTypePassingMethod(@dataType,d:array)"/> &amp; in_<xsl:value-of select="@name"/><xsl:if test="position() &lt; count(../d:argument)+count(../d:returnvalue)">,</xsl:if>
  		
  	</xsl:for-each>
  	<xsl:for-each select="d:returnvalue">
  		<xsl:value-of select="fnc:quasarDataTypeToCppType(@dataType,d:array)"/> &amp; out_<xsl:value-of select="@name"/><xsl:if test="position() &lt; count(../d:returnvalue)">,</xsl:if>
  	</xsl:for-each>
  
  );
</xsl:for-each>

private:

  UaSession  * m_session;
  UaNodeId     m_objId;

};

	</xsl:template>
	
	<xsl:template match="/">	
	
	// generated: <xsl:value-of select="current-dateTime()"/>

	#include &lt;iostream&gt;
    #include &lt;uaclient/uaclientsdk.h&gt;
    
    using namespace UaClientSdk;
	
	<xsl:if test="not(/d:design/d:class[@name=$className])">
		<xsl:message terminate="yes">Class not found.</xsl:message>
	</xsl:if>
	<xsl:for-each select="/d:design/d:class[@name=$className]">
	<xsl:call-template name="classBody"/>
	</xsl:for-each>
	</xsl:template>



</xsl:transform>
