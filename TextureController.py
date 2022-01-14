# -*- coding: utf8 -*-

import c4d, ControllerBaseClass

class TextureController( ControllerBaseClass.ControllerBaseClass ):

    PLUGIN_NAME = "Texture Controller"
    PLUGIN_ID = 1039369
    
    def Init( self, node ):
    
        result = super( TextureController, self ).Init( node )
        
        node[ c4d.SMALL_FAR_AWAY_TEXTURE_DISTANCE ] = 100.0
        
        return True
        
    def Execute( self, tag, doc, object, bt, priority, flags ):
    
        result = super( TextureController, self ).Execute( tag, doc, object, bt, priority, flags )
        if result != c4d.EXECUTIONRESULT_OK: return c4d.EXECUTIONRESULT_OK
        
        displayTag = self.GetFirstTagOfType( object, c4d.Tdisplay )
        
        if displayTag is None:
            
            # self.MessageToUser( tag, "This tag only works when applied to an object with a Display tag on it" )
            
            doc.StartUndo()
            
            object.MakeTag(c4d.Tdisplay)
            
            displayTag = self.GetFirstTagOfType( object, c4d.Tdisplay )
            
            displayTag[ c4d.DISPLAYTAG_AFFECT_TEXTURES ] = True
            
            c4d.EventAdd()
            
            doc.EndUndo()
            
        else:
            if not displayTag[ c4d.DISPLAYTAG_AFFECT_TEXTURES ]:
                self.MessageToUser( tag, "The Display tag does not have “Use Textures” option enabled – you won’t see anything unless you turn this on" )
        
            if self.calculatedDistance >= tag[ c4d.SMALL_FAR_AWAY_TEXTURE_DISTANCE ]:
                displayTag[ c4d.DISPLAYTAG_TEXTURES ] = False
            else:
                displayTag[ c4d.DISPLAYTAG_TEXTURES ] = True
       
        return c4d.EXECUTIONRESULT_OK
    

