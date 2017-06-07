# -*- coding: utf8 -*-

import c4d, ControllerBaseClass

class EnhancedOpenGLController( ControllerBaseClass.ControllerBaseClass ):

    PLUGIN_NAME = "Enhanced OpenGL Controller"
    PLUGIN_ID = 1039370
    
    def Init( self, node ):
    
        result = super( EnhancedOpenGLController, self ).Init( node )
        
        node[ c4d.SMALL_FAR_AWAY_E_OPENGL_DISTANCE ] = 100.0
        
        return True
        
    def Execute( self, tag, doc, object, bt, priority, flags ):
    
        result = super( EnhancedOpenGLController, self ).Execute( tag, doc, object, bt, priority, flags )
        if result != c4d.EXECUTIONRESULT_OK: return c4d.EXECUTIONRESULT_OK
        
        displayTag = self.GetFirstTagOfType( object, c4d.Tdisplay )
        
        if displayTag is None:
            self.MessageToUser( tag, "This tag only works when applied to an object with a Display tag on it" )
        else:
            if not displayTag[ c4d.DISPLAYTAG_AFFECT_HQ_OGL ]:
                self.MessageToUser( tag, "The Display tag does not have “Use Enhanced OpenGL” option enabled – you won’t see anything unless you turn this on" )
        
            if self.calculatedDistance >= tag[ c4d.SMALL_FAR_AWAY_E_OPENGL_DISTANCE ]:
                displayTag[ c4d.DISPLAYTAG_HQ_OGL ] = False
            else:
                displayTag[ c4d.DISPLAYTAG_HQ_OGL ] = True
       
        return c4d.EXECUTIONRESULT_OK
    
