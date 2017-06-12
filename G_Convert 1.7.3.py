#MenuTitle: G_Convert 1.7.3
# -*- coding: utf-8 -*-

__doc__="""
Convert georgian letters to each other.
"""
import vanilla
import GlyphsApp
Font = Glyphs.font

geo_asciiLat = "a, b, g, d, e, v, z, T, i, k, l, m, n, o, p, J, r, s, t, u, f, q, R, y, S, C, c, Z, w, W, x, j, h"
geo_asciiRus_Mkhed = "agrave, aacute, atilde, adieresis, aring, acircumflex, ccedilla, ucircumflex, egrave, ecircumflex, edieresis, igrave, iacute, icircumflex, idieresis, ae, eth, ntilde, ograve, oacute, ocircumflex, udieresis, eacute, thorn, oslash, divide, odieresis, yacute, ugrave, ydieresis, otilde, uacute, questiondown"
geo_asciiRus_Mtavr = "Agrave, Aacute, Atilde, Adieresis, Aring, Acircumflex, Ccedilla, Ucircumflex, Egrave, Ecircumflex, Edieresis, Igrave, Iacute, Icircumflex, Idieresis, AE, Eth, Ntilde, Ograve, Oacute, Ocircumflex, Udieresis, Eacute, Thorn, Oslash, multiply, Odieresis, Yacute, Ugrave, germandbls, Otilde, Uacute, cedilla"

geo_uni_mkhed = "an-georgian, ban-georgian, gan-georgian, don-georgian, en-georgian, vin-georgian, zen-georgian, tan-georgian, in-georgian, kan-georgian, las-georgian, man-georgian, nar-georgian, on-georgian, par-georgian, zhar-georgian, rae-georgian, san-georgian, tar-georgian, un-georgian, phar-georgian, khar-georgian, ghan-georgian, qar-georgian, shin-georgian, chin-georgian, can-georgian, jil-georgian, cil-georgian, char-georgian, xan-georgian, jhan-georgian, hae-georgian"
geo_uni_mtavr = "An-georgian, Ban-georgian, Gan-georgian, Don-georgian, En-georgian, Vin-georgian, Zen-georgian, Tan-georgian, In-georgian, Kan-georgian, Las-georgian, Man-georgian, Nar-georgian, On-georgian, Par-georgian, Zhar-georgian, Rae-georgian, San-georgian, Tar-georgian, Un-georgian, Phar-georgian, Khar-georgian, Ghan-georgian, Qar-georgian, Shin-georgian, Chin-georgian, Can-georgian, Jil-georgian, Cil-georgian, Char-georgian, Xan-georgian, Jhan-georgian, Hae-georgian"

geo_uni_asomtavr = "An-oldgeorgian, Ban-oldgeorgian, Gan-oldgeorgian, Don-oldgeorgian, En-oldgeorgian, Vin-oldgeorgian, Zen-oldgeorgian, Tan-oldgeorgian, In-oldgeorgian, Kan-oldgeorgian, Las-oldgeorgian, Man-oldgeorgian, Nar-oldgeorgian, On-oldgeorgian, Par-oldgeorgian, Zhar-oldgeorgian, Rae-oldgeorgian, San-oldgeorgian, Tar-oldgeorgian, Un-oldgeorgian, Phar-oldgeorgian, Khar-oldgeorgian, Ghan-oldgeorgian, Qar-oldgeorgian, Shin-oldgeorgian, Chin-oldgeorgian, Can-oldgeorgian, Jil-oldgeorgian, Cil-oldgeorgian, Char-oldgeorgian, Xan-oldgeorgian, Jhan-oldgeorgian, Hae-oldgeorgian"
geo_uni_khuc = "an-oldgeorgian, ban-oldgeorgian, gan-oldgeorgian, don-oldgeorgian, en-oldgeorgian, vin-oldgeorgian, zen-oldgeorgian, tan-oldgeorgian, in-oldgeorgian, kan-oldgeorgian, las-oldgeorgian, man-oldgeorgian, nar-oldgeorgian, on-oldgeorgian, par-oldgeorgian, zhar-oldgeorgian, rae-oldgeorgian, san-oldgeorgian, tar-oldgeorgian, un-oldgeorgian, phar-oldgeorgian, khar-oldgeorgian, ghan-oldgeorgian, qar-oldgeorgian, shin-oldgeorgian, chin-oldgeorgian, can-oldgeorgian, jil-oldgeorgian, cil-oldgeorgian, char-oldgeorgian, xan-oldgeorgian, jhan-oldgeorgian, hae-oldgeorgian"


def freeGlyphName( glyphName, glyphNameList ):
	"""
	Returns the first unused version of glyphName.
	If necessary, adds a 3-digit extension to the name
	or increases the existing number extension by one.
	"""
	
	if glyphName in glyphNameList:
		try:
			# increase the .000 extension
			increasedGlyphName = glyphName[:-3] + ( "%.3d" % int( glyphName[-3:] ) + 1 )
			print "ATTENTION: %s already exists, trying to bump the extension ..." % ( glyphName )
			return freeGlyphName( increasedGlyphName, glyphNameList )
		except:
			# has no .000 extension yet:
			increasedGlyphName = glyphName + ".001"
			print "ATTENTION: %s already exists, trying %s ..." % ( glyphName, increasedGlyphName )
			return freeGlyphName( increasedGlyphName, glyphNameList )

	return glyphName
	
class InstanceMaker( object ):

	"""GUI for injecting instances."""
	def __init__( self ):
		self.w = vanilla.FloatingWindow( (400, 250), "Georgian Symbol Convertor 1.7.3", autosaveName="ge.edu.geolab.InstanceMaker.mainwindow" )
		#self.w.width('600')

		self.w.text_1		= vanilla.TextBox( (14, 14, 300, 14), "Convert Georgian characters", sizeStyle='regular' )

		# Standard
		self.w.selMode		= vanilla.RadioGroup((14+40+170, 14, 170, 17), ["Standard", "Custom"], isVertical=False, sizeStyle='regular', callback=self.selectConvertMode)
		self.w.selMode.set(0)

		self.w.text_src		= vanilla.TextBox( (14, 14+45, 75, 14), "From", sizeStyle='regular' )
		self.w.popup_src	= vanilla.PopUpButton((15+40, 14+45, 130, 17), [ "ascii_Lat", "ascii_Rus_mkhed", "ascii_Rus_mtavr"], sizeStyle='regular' )
		
		self.w.text_tgt		= vanilla.TextBox( (14+170+15, 14+45, 75, 14), "To", sizeStyle='regular' )
		self.w.popup_tgt	= vanilla.PopUpButton((15+40+170, 14+45, 130, 17), [ "uni_mkhedruli", "uni_mtavruli", "uni_asomtavr", "uni_khucuri" ], sizeStyle='regular' )

		# Custom
		self.w.text_custom_src		= vanilla.TextBox( (14, 14+120-75, 75, 14), "From", sizeStyle='regular' )
		self.w.text_custom_src.show(False)
		self.w.custom_src   		= vanilla.EditText( (14, 14+140-75, -14, 40), "", sizeStyle='small' )
		self.w.custom_src.show(False)

		self.w.text_custom_tgt		= vanilla.TextBox( (14, 14+185-75, 75, 14), "To", sizeStyle='regular' )
		self.w.text_custom_tgt.show(False)
		self.w.custom_tgt   		= vanilla.EditText( (14, 14+205-75, -14, 40), "", sizeStyle='small' )
		self.w.custom_tgt.show(False)

		#self.w.customTo     = vanilla.EditText( (14, 14+150, -5, -5), "", sizeStyle='small')

		self.w.createButton = vanilla.Button((-80-15, -20-15, -15, -15), "Start", sizeStyle='regular', callback=self.runMyCode )

		self.w.setDefaultButton( self.w.createButton )

		

		self.w.open()
		#self.UpdateSample( self )
		self.w.makeKey()

		
		
	def getComboSrc( self ):
		srcString = self.w.popup_src.getItems()[self.w.popup_src.get()]
		if srcString == "ascii_Lat":
			srcSelValue = geo_asciiLat.split(", ")
		elif srcString == "ascii_Rus_mkhed":
			srcSelValue = geo_asciiRus_Mkhed.split(", ")
		elif srcString == "ascii_Rus_mtavr":
			srcSelValue = geo_asciiRus_Mtavr.split(", ")
		return srcSelValue

		print srcString

	def getComboTgt( self ):
		tgtString = self.w.popup_tgt.getItems()[self.w.popup_tgt.get()]
		if tgtString == "uni_mkhedruli":
			tgtSelValue = geo_uni_mkhed.split(", ")
		elif tgtString == "uni_mtavruli":
			tgtSelValue = geo_uni_mtavr.split(", ")
		elif tgtString == "uni_asomtavr":
			tgtSelValue = geo_uni_asomtavr.split(", ")
		elif tgtString == "uni_khucuri":
			tgtSelValue = geo_uni_khuc.split(", ")
		return tgtSelValue

		print tgtString

	#def getCustomSrc( self ):

				

	def selectConvertMode(self, sender):
		rValue = self.w.selMode.get()

		
		# if Standard mode is active show Sandart selections and hide Custom
		if rValue == 0:
			print "true"

			# Custom
			self.w.custom_src.show(False)
			self.w.text_custom_src.show(False)

			self.w.custom_tgt.show(False)
			self.w.text_custom_tgt.show(False)

			# Standard
			self.w.text_src.show(True)
			self.w.popup_src.show(True)
			
			self.w.text_tgt.show(True)
			self.w.popup_tgt.show(True)


		# if Custom mode is active show Custom selections and hide Standard
		elif rValue == 1:
			print "false"

			# Custom
			self.w.custom_src.show(True)
			self.w.text_custom_src.show(True)

			self.w.custom_tgt.show(True)
			self.w.text_custom_tgt.show(True)

			# Standard
			self.w.text_src.show(False)
			self.w.popup_src.show(False)
			
			self.w.text_tgt.show(False)
			self.w.popup_tgt.show(False)
		
	def runMyCode(self, sender):

		rValue = self.w.selMode.get()

		if rValue == 0:
			srcArray = self.getComboSrc()
			tgtArray = self.getComboTgt()

			print srcArray
			print tgtArray
		elif rValue == 1:
			srcArray = str(self.w.custom_src.get())
			srcArray = srcArray.split(", ")

			tgtArray = str(self.w.custom_tgt.get())
			tgtArray = tgtArray.split(", ")

			print srcArray
			print tgtArray


		for i in range(0, len(srcArray)):
			"""Renames source to target."""
			thisGlyph = Font.glyphs[ srcArray[i] ]
			existingGlyphNames = [ g.name for g in Font.glyphs ]
			targetString = freeGlyphName( tgtArray[i], existingGlyphNames )
			
			try:
				thisGlyph.name = targetString
				print "Renamed glyph: %s >>> %s" % (srcArray[i], targetString)
			except Exception, e:
				if "NoneType" in e:
					e = "No glyph with that name."
				print "ERROR: Failed to rename %s to %s. (%s)" % (srcArray[i], targetString, e)



InstanceMaker()


