# -*- coding: utf8 -*-
# written by charlie robin / charlierobin.com / 2017

import c4d, ControllerBaseClass

class VisibilityController( ControllerBaseClass.ControllerBaseClass ):

    PLUGIN_NAME = "Visibility Controller"
    PLUGIN_ID = 1039286
    
    def Init( self, node ):
    
        result = super( VisibilityController, self ).Init( node )
        
        node[ c4d.SMALL_FAR_AWAY_VISIBILITY_DISTANCE ] = 100.0
        
        return True
        
    def Execute( self, tag, doc, object, bt, priority, flags ):
    
        result = super( VisibilityController, self ).Execute( tag, doc, object, bt, priority, flags )
        if result != c4d.EXECUTIONRESULT_OK: return c4d.EXECUTIONRESULT_OK
        
        if not tag[ c4d.SMALL_FAR_AWAY_VISIBILITY_VISIBILITY_EDITOR ]: 
            if not tag[ c4d.SMALL_FAR_AWAY_VISIBILITY_VISIBILITY_RENDER ]: 
                if not tag[ c4d.SMALL_FAR_AWAY_VISIBILITY_GENERATOR_FLAG ]:
        
                    self.MessageToUser( tag, "You’ve not got any options checked below (visibility, generator), so at the moment this tag is not doing anything" )
        
        if self.calculatedDistance >= tag[ c4d.SMALL_FAR_AWAY_VISIBILITY_DISTANCE ]:
                
            if tag[ c4d.SMALL_FAR_AWAY_VISIBILITY_VISIBILITY_EDITOR ]:
                object.SetEditorMode( c4d.MODE_OFF )
            else:
                object.SetEditorMode( c4d.MODE_UNDEF )
            
            if tag[ c4d.SMALL_FAR_AWAY_VISIBILITY_VISIBILITY_RENDER ]:
                object.SetRenderMode( c4d.MODE_OFF )
            else:
                object.SetRenderMode( c4d.MODE_UNDEF )
            
            if tag[ c4d.SMALL_FAR_AWAY_VISIBILITY_GENERATOR_FLAG ]:
                object.SetDeformMode( False )
            else:
                object.SetDeformMode( True )
            
        else:
        
            object.SetEditorMode( c4d.MODE_UNDEF )
            object.SetRenderMode( c4d.MODE_UNDEF )
            object.SetDeformMode( True )
       
        return c4d.EXECUTIONRESULT_OK
    
