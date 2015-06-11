#!/usr/bin/env python
#title           :kml_editor.py
#description     :Create a KML file based on information stored in a database.
#author          :Kevin Ballantyne
#date            :20150206
#version         :0.1
#usage           :python kml_editor.py
#notes           :
#python_version  :2.7.5  
#==============================================================================

import os
import sys
import pykml
import sqlite3
from pykml.factory import KML_ElementMaker as KML
from lxml import etree
import traceback
import re

def create_style(id_name, poly_colour, line_colour="FF000000", line_width="2"):

	# create a KML document with a folder and a default style
	stylename = "ballooon_style"
	balloon_text = """
	<font size="5"><b>$[name]</b></font><br>
	<br>
	<table width="500" border="1" cellspacing="0" cellpadding="6">
     <col width="150">
     <col width="350">

     <tr align="left" valign="top">
       <td><b>Dates:</b></td>
       <td>$[dates]</td>
     </tr>

     <tr align="left" valign="top">
       <td><b>Status:</b></td>
       <td>$[status]</td>
     </tr>

     <tr align="left" valign="top">
       <td><b>History:</td>
       <td>$[history]</td>
     </tr>
	 
	 <tr align="left" valign="top">
       <td><b>1912 Address:</td>
       <td>$[addrss]</td>
     </tr>
	 
	 <tr align="left" valign="top">
       <td><b>Sources:</td>
       <td>$[sources]</td>
     </tr>

</table><br>

<table width="500" border="1" cellspacing="0" cellpadding="6">

     <tr align="center" valign="top">
        <td><b>Photos</b></td>
     </tr>

     <tr align="left" valign="top">
       <td>$[photos]</td>
     </tr>

</table>"""

	out_style = KML.Style(
					KML.IconStyle(
						KML.scale(1.1),
						KML.Icon(
							KML.href("http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png"),
						),
						KML.hotSpot(x="20",y="2",xunits="pixels",yunits="pixels"),
					),
					KML.LineStyle(
						KML.color(line_colour),
						KML.width(line_width),
					),
					KML.PolyStyle(
						KML.color(poly_colour),
					),
					KML.BalloonStyle(
						KML.text(balloon_text),
					), 
					id=id_name,
				)
				
	#print "out_style: " + str(out_style)
	
	return out_style
	
def create_stylemap(id_name, style1_id, style2_id, key1="normal", key2="highlight"):
	out_smap = KML.StyleMap(
					KML.Pair(
						KML.key(key1),
						KML.styleUrl("#" + style1_id),
					),
					KML.Pair(
						KML.key(key2),
						KML.styleUrl("#" + style2_id),
					),
					id=id_name,
				)
				
	#print "out_smap: " + str(out_smap)
	#print "out_smap: " + str(type(out_smap))
	
	return out_smap

def convert_to_kml(db_file):
	conn = sqlite3.connect(db_file)
	c = conn.cursor()

	c.execute('SELECT * FROM former_buildings')
	results = c.fetchall()
	
	out_kml = KML.kml()
	
	out_doc = KML.Document(
		KML.name("Former Ottawa Buildings"), 
		KML.description('''<br>Colour Legend:
<br>
<br>
<table width="400" border="1" cellspacing="0" cellpadding="6">
     <col width="200">
     <col width="50">
     <tr align="center" valign="top">
       <td><b>Land Use Type</td>
       <td><b>Colour</td>
     </tr>
     <tr align="left" valign="top">
       <td>Residential Dwellings</td>
       <td bgcolor="FFFF00"></td>
     </tr>
     <tr align="left" valign="top">
       <td>Hotels</td>
       <td bgcolor="FF9900"></td>
     </tr>
     <tr align="left" valign="top">
       <td>Commercial</td>
       <td bgcolor="FF0000"></td>
     </tr>
     <tr align="left" valign="top">
       <td>Industrial Building</td>
       <td bgcolor="A020F0"></td>
     </tr>
     <tr align="left" valign="top">
       <td>Institutional</td>
       <td bgcolor="0000FF"></td>
     </tr>
     <tr align="left" valign="top">
       <td>Health</td>
       <td bgcolor="33CCFF"></td>
     </tr>
     <tr align="left" valign="top">
       <td>Religious Establishments</td>
       <td bgcolor="2F7F4F"></td>
     </tr>
     <tr align="left" valign="top">
       <td>Recreational Facilities</td>
       <td bgcolor="00FF00"></td>
     </tr>
     <tr align="left" valign="top">
       <td>Transportation Buildings</td>
       <td bgcolor="808080"></td>
     </tr>
</table>
<br>Designed by Kevin Ballantyne
<br>Copyright 2015'''),
	)
				
	out_doc.append(create_style("residential_normal", "9900FFFF"))
	out_doc.append(create_style("residential_hl", "FF00FFFF"))
	out_doc.append(create_stylemap("residential_map", "residential_normal", "residential_hl"))
		
	out_doc.append(create_style("hotel_normal", "990099FF"))
	out_doc.append(create_style("hotel_hl", "FF0099FF"))
	out_doc.append(create_stylemap("hotel_map", "hotel_normal", "hotel_hl"))
		
	out_doc.append(create_style("comm_normal", "990000FF"))
	out_doc.append(create_style("comm_hl", "FF0000FF"))
	out_doc.append(create_stylemap("comm_map", "comm_normal", "comm_hl"))
		
	out_doc.append(create_style("industrial_normal", "99F000A0"))
	out_doc.append(create_style("industrial_hl", "FFF000A0"))
	out_doc.append(create_stylemap("industrial_map", "industrial_normal", "industrial_hl"))
	
	out_doc.append(create_style("institute_normal", "99FF0000"))
	out_doc.append(create_style("institute_hl", "FFFF0000"))
	out_doc.append(create_stylemap("institute_map", "institute_normal", "institute_hl"))
	
	out_doc.append(create_style("health_normal", "99FFCC33"))
	out_doc.append(create_style("health_hl", "FFFFCC33"))
	out_doc.append(create_stylemap("health_map", "health_normal", "health_hl"))
	
	out_doc.append(create_style("relig_normal", "994F7F2F"))
	out_doc.append(create_style("relig_hl", "FF4F7F2F"))
	out_doc.append(create_stylemap("relig_map", "relig_normal", "relig_hl"))
	
	out_doc.append(create_style("rec_normal", "9900FF00"))
	out_doc.append(create_style("rec_hl", "FF00FF00"))
	out_doc.append(create_stylemap("rec_map", "rec_normal", "rec_hl"))
	
	out_doc.append(create_style("trans_normal", "99808080"))
	out_doc.append(create_style("trans_hl", "FF808080"))
	out_doc.append(create_stylemap("trans_map", "trans_normal", "trans_hl"))
	
	for record in results:
		id_num = record[0]
		# name = record[1]
		# classification = record[2]
		# dates = record[3]
		# if dates is None or dates == "": dates = "n/a"
		# status = record[4]
		# if status is None or status == "": status = "n/a"
		# history = record[5]
		# if history is None or history == "": history = "n/a"
		# coords = record[6]
		
		print "record: " + str(record)
		#answer = raw_input("Press enter to continue...")
		
		name = convert_to_xmlvalid(record[1])
		classification = record[2]
		dates = record[3]
		if dates is None or dates == "": dates = "n/a"
		status = record[4]
		if status is None:
			status = "n/a"
		else:
			status = convert_to_xmlvalid(status)
			if status == "": status = "n/a"
		history = record[5]
		if history is None:
			history = "n/a"
		else:
			history = convert_to_xmlvalid(history)
			if history == "": history = "n/a"
		coords = record[6]
		addrss = record[7]
		if addrss is None:
			addrss = "n/a"
		else:
			addrss = convert_to_xmlvalid(addrss)
			if addrss == "": addrss = "n/a"
		
		print "Record: " + str(record[0])
		print "Name: " + str(name)
		print "Classification: " + str(classification)
		print "Dates: " + str(dates)
		print "Status: " + str(status)
		print "History: " + str(history)
		print "Coordinates: " + str(coords)
		print "1912 Address: " + str(addrss)
		print "\n"
		#answer = raw_input("Press enter to continue...")
		
		if classification == "residential":
			style_url = "#residential_map"
		elif classification == "hotel":
			style_url = "#hotel_map"
		elif classification == "commercial":
			style_url = "#comm_map"
		elif classification == "industrial":
			style_url = "#industrial_map"
		elif classification == "institute":
			style_url = "#institute_map"
		elif classification == "health":
			style_url = "#health_map"
		elif classification == "religious":
			style_url = "#relig_map"
		elif classification == "recreational":
			style_url = "#rec_map"
		elif classification == "transportation":
			style_url = "#trans_map"
			
		photo_html = get_photo_html(c, id_num)
		source_text = get_sources(c, id_num)
		
		print "name: " + str(name)
		
		out_doc.append(
			KML.Placemark(
				KML.name(name.encode('utf-8')),
				KML.styleUrl(style_url),
				KML.ExtendedData(
					KML.Data(
						KML.value(str(name)),
						name="name"
					), 
					KML.Data(
						KML.value(str(dates)),
						name="dates"
					), 
					KML.Data(
						KML.value(str(status)),
						name="status"
					), 
					KML.Data(
						KML.value(str(history)),
						name="history"
					), 
					KML.Data(
						KML.value(str(addrss)),
						name="addrss"
					), 
					KML.Data(
						KML.value(str(source_text)),
						name="sources"
					), 
					KML.Data(
						KML.value(str(photo_html)),
						name="photos"
					), 
					#KML.Data(value=str(status), name="status"), 
					#KML.Data(value=str(history), name="history"), 
					#KML.Data(value=str(photo_html), name="photos"), 
				),
				KML.Polygon(
					KML.tessellate("1"),
					KML.outerBoundaryIs(
						KML.LinearRing(
							KML.coordinates(coords),
						),
					),
				),
			),
		)
		
	out_kml.append(out_doc)
	
	kml_text = etree.tostring(out_kml, pretty_print=True)
	
	kml_fn = os.path.splitext(db_file)
	
	kml_file = open(kml_fn[0] + ".kml", 'w')
	kml_file.write(kml_text + "\n")
	
def convert_to_xmlvalid(in_str):
	#print "in_str: " + str(in_str.replace(u"\u00C9", "&Eacute;"))
	if in_str is None or in_str == "": return "n/a"
	out_str = in_str.replace(u"\u0022", "&quot;")
	out_str = out_str.replace(u"\u0026", "&amp;")
	out_str = out_str.replace(u"\u0027", "&apos;")
	out_str = out_str.replace(u"\u003C", "&lt;")
	out_str = out_str.replace(u"\u003E", "&gt;")
	out_str = out_str.replace(u"\u00A0", "&nbsp;")
	out_str = out_str.replace(u"\u00A1", "&iexcl;")
	out_str = out_str.replace(u"\u00A2", "&cent;")
	out_str = out_str.replace(u"\u00A3", "&pound;")
	out_str = out_str.replace(u"\u00A4", "&curren;")
	out_str = out_str.replace(u"\u00A5", "&yen;")
	out_str = out_str.replace(u"\u00A6", "&brvbar;")
	out_str = out_str.replace(u"\u00A7", "&sect;")
	out_str = out_str.replace(u"\u00A8", "&uml;")
	out_str = out_str.replace(u"\u00A9", "&copy;")
	out_str = out_str.replace(u"\u00AA", "&ordf;")
	out_str = out_str.replace(u"\u00AB", "&laquo;")
	out_str = out_str.replace(u"\u00AC", "&not;")
	out_str = out_str.replace(u"\u00AD", "&shy;")
	out_str = out_str.replace(u"\u00AE", "&reg;")
	out_str = out_str.replace(u"\u00AF", "&macr;")
	out_str = out_str.replace(u"\u00B0", "&deg;")
	out_str = out_str.replace(u"\u00B1", "&plusmn;")
	out_str = out_str.replace(u"\u00B2", "&sup2;")
	out_str = out_str.replace(u"\u00B3", "&sup3;")
	out_str = out_str.replace(u"\u00B4", "&acute;")
	out_str = out_str.replace(u"\u00B5", "&micro;")
	out_str = out_str.replace(u"\u00B6", "&para;")
	out_str = out_str.replace(u"\u00B7", "&middot;")
	out_str = out_str.replace(u"\u00B8", "&cedil;")
	out_str = out_str.replace(u"\u00B9", "&sup1;")
	out_str = out_str.replace(u"\u00BA", "&ordm;")
	out_str = out_str.replace(u"\u00BB", "&raquo;")
	out_str = out_str.replace(u"\u00BC", "&frac14;")
	out_str = out_str.replace(u"\u00BD", "&frac12;")
	out_str = out_str.replace(u"\u00BE", "&frac34;")
	out_str = out_str.replace(u"\u00BF", "&iquest;")
	out_str = out_str.replace(u"\u00C0", "&Agrave;")
	out_str = out_str.replace(u"\u00C1", "&Aacute;")
	out_str = out_str.replace(u"\u00C2", "&Acirc;")
	out_str = out_str.replace(u"\u00C3", "&Atilde;")
	out_str = out_str.replace(u"\u00C4", "&Auml;")
	out_str = out_str.replace(u"\u00C5", "&Aring;")
	out_str = out_str.replace(u"\u00C6", "&AElig;")
	out_str = out_str.replace(u"\u00C7", "&Ccedil;")
	out_str = out_str.replace(u"\u00C8", "&Egrave;")
	out_str = out_str.replace(u"\u00C9", "&Eacute;")
	out_str = out_str.replace(u"\u00CA", "&Ecirc;")
	out_str = out_str.replace(u"\u00CB", "&Euml;")
	out_str = out_str.replace(u"\u00CC", "&Igrave;")
	out_str = out_str.replace(u"\u00CD", "&Iacute;")
	out_str = out_str.replace(u"\u00CE", "&Icirc;")
	out_str = out_str.replace(u"\u00CF", "&Iuml;")
	out_str = out_str.replace(u"\u00D0", "&ETH;")
	out_str = out_str.replace(u"\u00D1", "&Ntilde;")
	out_str = out_str.replace(u"\u00D2", "&Ograve;")
	out_str = out_str.replace(u"\u00D3", "&Oacute;")
	out_str = out_str.replace(u"\u00D4", "&Ocirc;")
	out_str = out_str.replace(u"\u00D5", "&Otilde;")
	out_str = out_str.replace(u"\u00D6", "&Ouml;")
	out_str = out_str.replace(u"\u00D7", "&times;")
	out_str = out_str.replace(u"\u00D8", "&Oslash;")
	out_str = out_str.replace(u"\u00D9", "&Ugrave;")
	out_str = out_str.replace(u"\u00DA", "&Uacute;")
	out_str = out_str.replace(u"\u00DB", "&Ucirc;")
	out_str = out_str.replace(u"\u00DC", "&Uuml;")
	out_str = out_str.replace(u"\u00DD", "&Yacute;")
	out_str = out_str.replace(u"\u00DE", "&THORN;")
	out_str = out_str.replace(u"\u00DF", "&szlig;")
	out_str = out_str.replace(u"\u00E0", "&agrave;")
	out_str = out_str.replace(u"\u00E1", "&aacute;")
	out_str = out_str.replace(u"\u00E2", "&acirc;")
	out_str = out_str.replace(u"\u00E3", "&atilde;")
	out_str = out_str.replace(u"\u00E4", "&auml;")
	out_str = out_str.replace(u"\u00E5", "&aring;")
	out_str = out_str.replace(u"\u00E6", "&aelig;")
	out_str = out_str.replace(u"\u00E7", "&ccedil;")
	out_str = out_str.replace(u"\u00E8", "&egrave;")
	out_str = out_str.replace(u"\u00E9", "&eacute;")
	out_str = out_str.replace(u"\u00EA", "&ecirc;")
	out_str = out_str.replace(u"\u00EB", "&euml;")
	out_str = out_str.replace(u"\u00EC", "&igrave;")
	out_str = out_str.replace(u"\u00ED", "&iacute;")
	out_str = out_str.replace(u"\u00EE", "&icirc;")
	out_str = out_str.replace(u"\u00EF", "&iuml;")
	out_str = out_str.replace(u"\u00F0", "&eth;")
	out_str = out_str.replace(u"\u00F1", "&ntilde;")
	out_str = out_str.replace(u"\u00F2", "&ograve;")
	out_str = out_str.replace(u"\u00F3", "&oacute;")
	out_str = out_str.replace(u"\u00F4", "&ocirc;")
	out_str = out_str.replace(u"\u00F5", "&otilde;")
	out_str = out_str.replace(u"\u00F6", "&ouml;")
	out_str = out_str.replace(u"\u00F7", "&divide;")
	out_str = out_str.replace(u"\u00F8", "&oslash;")
	out_str = out_str.replace(u"\u00F9", "&ugrave;")
	out_str = out_str.replace(u"\u00FA", "&uacute;")
	out_str = out_str.replace(u"\u00FB", "&ucirc;")
	out_str = out_str.replace(u"\u00FC", "&uuml;")
	out_str = out_str.replace(u"\u00FD", "&yacute;")
	out_str = out_str.replace(u"\u00FE", "&thorn;")
	out_str = out_str.replace(u"\u00FF", "&yuml;")
	out_str = out_str.replace(u"\u0152", "&OElig;")
	out_str = out_str.replace(u"\u0153", "&oelig;")
	out_str = out_str.replace(u"\u0160", "&Scaron;")
	out_str = out_str.replace(u"\u0161", "&scaron;")
	out_str = out_str.replace(u"\u0178", "&Yuml;")
	out_str = out_str.replace(u"\u0192", "&fnof;")
	out_str = out_str.replace(u"\u02C6", "&circ;")
	out_str = out_str.replace(u"\u02DC", "&tilde;")
	out_str = out_str.replace(u"\u0391", "&Alpha;")
	out_str = out_str.replace(u"\u0392", "&Beta;")
	out_str = out_str.replace(u"\u0393", "&Gamma;")
	out_str = out_str.replace(u"\u0394", "&Delta;")
	out_str = out_str.replace(u"\u0395", "&Epsilon;")
	out_str = out_str.replace(u"\u0396", "&Zeta;")
	out_str = out_str.replace(u"\u0397", "&Eta;")
	out_str = out_str.replace(u"\u0398", "&Theta;")
	out_str = out_str.replace(u"\u0399", "&Iota;")
	out_str = out_str.replace(u"\u039A", "&Kappa;")
	out_str = out_str.replace(u"\u039B", "&Lambda;")
	out_str = out_str.replace(u"\u039C", "&Mu;")
	out_str = out_str.replace(u"\u039D", "&Nu;")
	out_str = out_str.replace(u"\u039E", "&Xi;")
	out_str = out_str.replace(u"\u039F", "&Omicron;")
	out_str = out_str.replace(u"\u03A0", "&Pi;")
	out_str = out_str.replace(u"\u03A1", "&Rho;")
	out_str = out_str.replace(u"\u03A3", "&Sigma;")
	out_str = out_str.replace(u"\u03A4", "&Tau;")
	out_str = out_str.replace(u"\u03A5", "&Upsilon;")
	out_str = out_str.replace(u"\u03A6", "&Phi;")
	out_str = out_str.replace(u"\u03A7", "&Chi;")
	out_str = out_str.replace(u"\u03A8", "&Psi;")
	out_str = out_str.replace(u"\u03A9", "&Omega;")
	out_str = out_str.replace(u"\u03B1", "&alpha;")
	out_str = out_str.replace(u"\u03B2", "&beta;")
	out_str = out_str.replace(u"\u03B3", "&gamma;")
	out_str = out_str.replace(u"\u03B4", "&delta;")
	out_str = out_str.replace(u"\u03B5", "&epsilon;")
	out_str = out_str.replace(u"\u03B6", "&zeta;")
	out_str = out_str.replace(u"\u03B7", "&eta;")
	out_str = out_str.replace(u"\u03B8", "&theta;")
	out_str = out_str.replace(u"\u03B9", "&iota;")
	out_str = out_str.replace(u"\u03BA", "&kappa;")
	out_str = out_str.replace(u"\u03BB", "&lambda;")
	out_str = out_str.replace(u"\u03BC", "&mu;")
	out_str = out_str.replace(u"\u03BD", "&nu;")
	out_str = out_str.replace(u"\u03BE", "&xi;")
	out_str = out_str.replace(u"\u03BF", "&omicron;")
	out_str = out_str.replace(u"\u03C0", "&pi;")
	out_str = out_str.replace(u"\u03C1", "&rho;")
	out_str = out_str.replace(u"\u03C2", "&sigmaf;")
	out_str = out_str.replace(u"\u03C3", "&sigma;")
	out_str = out_str.replace(u"\u03C4", "&tau;")
	out_str = out_str.replace(u"\u03C5", "&upsilon;")
	out_str = out_str.replace(u"\u03C6", "&phi;")
	out_str = out_str.replace(u"\u03C7", "&chi;")
	out_str = out_str.replace(u"\u03C8", "&psi;")
	out_str = out_str.replace(u"\u03C9", "&omega;")
	out_str = out_str.replace(u"\u03D1", "&thetasym;")
	out_str = out_str.replace(u"\u03D2", "&upsih;")
	out_str = out_str.replace(u"\u03D6", "&piv;")
	out_str = out_str.replace(u"\u2002", "&ensp;")
	out_str = out_str.replace(u"\u2003", "&emsp;")
	out_str = out_str.replace(u"\u2009", "&thinsp;")
	out_str = out_str.replace(u"\u200C", "&zwnj;")
	out_str = out_str.replace(u"\u200D", "&zwj;")
	out_str = out_str.replace(u"\u200E", "&lrm;")
	out_str = out_str.replace(u"\u200F", "&rlm;")
	out_str = out_str.replace(u"\u2013", "&ndash;")
	out_str = out_str.replace(u"\u2014", "&mdash;")
	out_str = out_str.replace(u"\u2018", "&lsquo;")
	out_str = out_str.replace(u"\u2019", "&rsquo;")
	out_str = out_str.replace(u"\u201A", "&sbquo;")
	out_str = out_str.replace(u"\u201C", "&ldquo;")
	out_str = out_str.replace(u"\u201D", "&rdquo;")
	out_str = out_str.replace(u"\u201E", "&bdquo;")
	out_str = out_str.replace(u"\u2020", "&dagger;")
	out_str = out_str.replace(u"\u2021", "&Dagger;")
	out_str = out_str.replace(u"\u2022", "&bull;")
	out_str = out_str.replace(u"\u2026", "&hellip;")
	out_str = out_str.replace(u"\u2030", "&permil;")
	out_str = out_str.replace(u"\u2032", "&prime;")
	out_str = out_str.replace(u"\u2033", "&Prime;")
	out_str = out_str.replace(u"\u2039", "&lsaquo;")
	out_str = out_str.replace(u"\u203A", "&rsaquo;")
	out_str = out_str.replace(u"\u203E", "&oline;")
	out_str = out_str.replace(u"\u2044", "&frasl;")
	out_str = out_str.replace(u"\u20AC", "&euro;")
	out_str = out_str.replace(u"\u2111", "&image;")
	out_str = out_str.replace(u"\u2118", "&weierp;")
	out_str = out_str.replace(u"\u211C", "&real;")
	out_str = out_str.replace(u"\u2122", "&trade;")
	out_str = out_str.replace(u"\u2135", "&alefsym;")
	out_str = out_str.replace(u"\u2190", "&larr;")
	out_str = out_str.replace(u"\u2191", "&uarr;")
	out_str = out_str.replace(u"\u2192", "&rarr;")
	out_str = out_str.replace(u"\u2193", "&darr;")
	out_str = out_str.replace(u"\u2194", "&harr;")
	out_str = out_str.replace(u"\u21B5", "&crarr;")
	out_str = out_str.replace(u"\u21D0", "&lArr;")
	out_str = out_str.replace(u"\u21D1", "&uArr;")
	out_str = out_str.replace(u"\u21D2", "&rArr;")
	out_str = out_str.replace(u"\u21D3", "&dArr;")
	out_str = out_str.replace(u"\u21D4", "&hArr;")
	out_str = out_str.replace(u"\u2200", "&forall;")
	out_str = out_str.replace(u"\u2202", "&part;")
	out_str = out_str.replace(u"\u2203", "&exist;")
	out_str = out_str.replace(u"\u2205", "&empty;")
	out_str = out_str.replace(u"\u2207", "&nabla;")
	out_str = out_str.replace(u"\u2208", "&isin;")
	out_str = out_str.replace(u"\u2209", "&notin;")
	out_str = out_str.replace(u"\u220B", "&ni;")
	out_str = out_str.replace(u"\u220F", "&prod;")
	out_str = out_str.replace(u"\u2211", "&sum;")
	out_str = out_str.replace(u"\u2212", "&minus;")
	out_str = out_str.replace(u"\u2217", "&lowast;")
	out_str = out_str.replace(u"\u221A", "&radic;")
	out_str = out_str.replace(u"\u221D", "&prop;")
	out_str = out_str.replace(u"\u221E", "&infin;")
	out_str = out_str.replace(u"\u2220", "&ang;")
	out_str = out_str.replace(u"\u2227", "&and;")
	out_str = out_str.replace(u"\u2228", "&or;")
	out_str = out_str.replace(u"\u2229", "&cap;")
	out_str = out_str.replace(u"\u222A", "&cup;")
	out_str = out_str.replace(u"\u222B", "&int;")
	out_str = out_str.replace(u"\u2234", "&there4;")
	out_str = out_str.replace(u"\u223C", "&sim;")
	out_str = out_str.replace(u"\u2245", "&cong;")
	out_str = out_str.replace(u"\u2248", "&asymp;")
	out_str = out_str.replace(u"\u2260", "&ne;")
	out_str = out_str.replace(u"\u2261", "&equiv;")
	out_str = out_str.replace(u"\u2264", "&le;")
	out_str = out_str.replace(u"\u2265", "&ge;")
	out_str = out_str.replace(u"\u2282", "&sub;")
	out_str = out_str.replace(u"\u2283", "&sup;")
	out_str = out_str.replace(u"\u2284", "&nsub;")
	out_str = out_str.replace(u"\u2286", "&sube;")
	out_str = out_str.replace(u"\u2287", "&supe;")
	out_str = out_str.replace(u"\u2295", "&oplus;")
	out_str = out_str.replace(u"\u2297", "&otimes;")
	out_str = out_str.replace(u"\u22A5", "&perp;")
	out_str = out_str.replace(u"\u22C5", "&sdot;")
	out_str = out_str.replace(u"\u2308", "&lceil;")
	out_str = out_str.replace(u"\u2309", "&rceil;")
	out_str = out_str.replace(u"\u230A", "&lfloor;")
	out_str = out_str.replace(u"\u230B", "&rfloor;")
	out_str = out_str.replace(u"\u2329", "&lang;")
	out_str = out_str.replace(u"\u232A", "&rang;")
	out_str = out_str.replace(u"\u25CA", "&loz;")
	out_str = out_str.replace(u"\u2660", "&spades;")
	out_str = out_str.replace(u"\u2663", "&clubs;")
	out_str = out_str.replace(u"\u2665", "&hearts;")
	out_str = out_str.replace(u"\u2666", "&diams;")
	
	return out_str
	
def get_photo_html(sql_cursor, building_id):
	print "SELECT photo_table.* FROM former_buildings INNER JOIN photo_table ON former_buildings.photo_key=photo_table.photo_key + '%' AND former_buildings.id=" + str(building_id)
	print "SELECT photo_table.* FROM former_buildings JOIN photo_table ON former_buildings.photo_key LIKE substr(photo_table.photo_key, 0, 4) AND former_buildings.id=" + str(building_id)

	sql_cursor.execute("SELECT photo_table.* FROM former_buildings JOIN photo_table ON former_buildings.key LIKE substr(photo_table.photo_key, 0, 4) AND former_buildings.id=" + str(building_id))
	
	results = sql_cursor.fetchall()
	
	out_html = '''<table width="500" border="1" cellspacing="0" cellpadding="6">
	'''
	
	for index, record in enumerate(results):
		photo_id = record[0]
		build_id = record[1]
		caption = convert_to_xmlvalid(record[2])
		source = convert_to_xmlvalid(record[3])
		if source is None or source == "": source = "n/a"
		src_url = record[4]
		photo_url = record[5]
		print "photo_id: " + str(photo_id)
		print "building_id: " + str(build_id)
		print "caption: " + str(caption)
		print "source: " + str(source)
		print "src_url: " + str(src_url)
		print "photo_url: " + str(photo_url)
		print "\n"
		
		out_html += '''<tr align="left" valign="top">
		<td>
		Photo %s: %s''' % (index + 1, caption)
		if not source == "n/a": out_html += " (source: %s)<br>" % source
		out_html += "\n"
		if src_url is not None and not src_url == "": out_html += "<a href=\"%s\"/>\n" % src_url
		out_html += '''<img src="%s" title="%s" border="1" width="500"/>
		</a>
		</td>
		</tr>''' % (photo_url, caption)
		
	out_html += "\n</table>"
	
	#print "photo_html: " + str(out_html.encode('utf-8'))
	
	return out_html
	
def get_sources(sql_cursor, building_id):
	print "SELECT source_table.* FROM former_buildings JOIN source_table ON former_buildings.key LIKE substr(source_table.source_key, 0, 4) AND former_buildings.id=" + str(building_id)

	sql_cursor.execute("SELECT source_table.* FROM former_buildings JOIN source_table ON former_buildings.key LIKE substr(source_table.source_key, 0, 4) AND former_buildings.id=" + str(building_id))
	
	results = sql_cursor.fetchall()
	
	out_text = ""
	
	for index, record in enumerate(results):
		source_key = record[0]
		source_name = convert_to_xmlvalid(record[1])
		source_url = record[2]
		
		if index == 0:
			if not str(source_url) == "None" and not str(source_url) == "":
				out_text += "%s: %s" % (source_name, source_url)
			else:
				out_text += "%s" % source_name
		else:
			if not str(source_url) == "None" and not str(source_url) == "":
				out_text += "<br>%s: %s" % (source_name, source_url)
			else:
				out_text += "<br>%s" % source_name
		
	return out_text

def main():
	try:
		argv = sys.argv
		
		if len(argv) > 1:
			db_file = argv[1]
			print "db_file: " + str(db_file)
			
		convert_to_kml(db_file)
	except:
		print "Exception in user code:"
        traceback.print_exc(file=sys.stdout)
	
if __name__ == '__main__':
	sys.exit(main())
