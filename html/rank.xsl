<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    version="1.0">
<xsl:output method="html" indent="yes" version="4.0"/>
<xsl:template match="/pr">
  <html>
    <head><link rel="stylesheet" 
	        type="text/css" 
	        href="style.css" />
    <title>Page Rank</title>
    </head>
    <body><h1>Page Rank</h1>
      <TABLE>
	<TH>Nom</TH><TH>Page Rank</TH>
	<xsl:apply-templates/>
      </TABLE></body>
  </html>
</xsl:template>
<xsl:template match="site">
  <TR><TD><xsl:value-of select="nom"/></TD>
  <TD><xsl:value-of select="page_rank"/></TD></TR>
</xsl:template>
</xsl:stylesheet> 