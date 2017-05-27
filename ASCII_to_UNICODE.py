#MenuTitle: G_LatToUnicode
# -*- coding: utf-8 -*-
__doc__="""
Converts glyphs from AXt Encoding to modern Unicode.
Attention: this script is not yet finished.
Please add suggestions in the Github Wiki:
https://github.com/mekkablue/Glyphs-Scripts/wiki/AXt-Converter
Thx!
"""

nameChangeString = """
Note: You can put comments here too.
Only lines containing a dash (-) followed by a greater sign (>) will be interpreted.

a -> an-georgian
b -> ban-georgian
g -> gan-georgian
d -> don-georgian
e -> en-georgian
v -> vin-georgian
z -> zen-georgian
T -> tan-georgian
i -> in-georgian
k -> kan-georgian
l -> las-georgian
m -> man-georgian
n -> nar-georgian
o -> on-georgian
p -> par-georgian
J -> zhar-georgian
r -> rae-georgian
s -> san-georgian
t -> tar-georgian
u -> un-georgian
f -> phar-georgian
q -> khar-georgian
R -> ghan-georgian
y -> qar-georgian
S -> shin-georgian
C -> chin-georgian
c -> can-georgian
Z -> jil-georgian
w -> cil-georgian
W -> char-georgian
x -> xan-georgian
j -> jhan-georgian
h -> hae-georgian

"""


import GlyphsApp
Font = Glyphs.font

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


def glyphRename( source, target ):
	"""Renames source to target."""
	thisGlyph = Font.glyphs[ source ]
	existingGlyphNames = [ g.name for g in Font.glyphs ]
	targetString = freeGlyphName( target, existingGlyphNames )
	
	try:
		thisGlyph.name = targetString
		print "Renamed glyph: %s >>> %s" % (source, targetString)
	except Exception, e:
		if "NoneType" in e:
			e = "No glyph with that name."
		print "ERROR: Failed to rename %s to %s. (%s)" % (source, targetString, e)


# parse lines of nameChangeString:
for line in nameChangeString.splitlines():
	try:
		nameList = line.split("->")
		srcName = nameList[0].strip()
		tgtName = nameList[1].strip()
		if srcName != tgtName:
			glyphRename( srcName, tgtName )
	except:
		pass

print """
Try this recipe in Font > Generate glyphs:


"""
