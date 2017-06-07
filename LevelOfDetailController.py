# -*- coding: utf8 -*-
# written by charlie robin / charlierobin.com / 2017

import c4d, ControllerBaseClass

class LevelOfDetailController( ControllerBaseClass.ControllerBaseClass ):
    
    PLUGIN_NAME = "Level of Detail Controller"
    PLUGIN_ID = 1039269
    
    def Init( self, node ):
        
        result = super( LevelOfDetailController, self ).Init( node )
        
        node[ c4d.SMALL_FAR_AWAY_LOD_MIN_DISTANCE ] = 100.0
        node[ c4d.SMALL_FAR_AWAY_LOD_MAX_DISTANCE ] = 1000.0
        
        node[ c4d.SMALL_FAR_AWAY_LOD_MIN ] = 0.1
        node[ c4d.SMALL_FAR_AWAY_LOD_MAX ] = 1.0
        
        return True
    
    def Execute( self, tag, doc, object, bt, priority, flags ):
        
        result = super( LevelOfDetailController, self ).Execute( tag, doc, object, bt, priority, flags )
        if result != c4d.EXECUTIONRESULT_OK: return c4d.EXECUTIONRESULT_OK
        
        if self.calculatedDistance <= tag[ c4d.SMALL_FAR_AWAY_LOD_MIN_DISTANCE ]: 
            levelOfDetail = tag[ c4d.SMALL_FAR_AWAY_LOD_MAX ]
        elif self.calculatedDistance >= tag[ c4d.SMALL_FAR_AWAY_LOD_MAX_DISTANCE ]: 
            levelOfDetail = tag[ c4d.SMALL_FAR_AWAY_LOD_MIN ]
        else:
            
            dLOD = tag[ c4d.SMALL_FAR_AWAY_LOD_MAX ] - tag[ c4d.SMALL_FAR_AWAY_LOD_MIN ]
            dDistance = tag[ c4d.SMALL_FAR_AWAY_LOD_MAX_DISTANCE ] - tag[ c4d.SMALL_FAR_AWAY_LOD_MIN_DISTANCE ]
            
            unit = dLOD / dDistance
            
            levelOfDetail = tag[ c4d.SMALL_FAR_AWAY_LOD_MAX ]
            levelOfDetail = levelOfDetail - ( ( self.calculatedDistance - tag[ c4d.SMALL_FAR_AWAY_LOD_MIN_DISTANCE ] ) * unit )
        
        tag[ c4d.SMALL_FAR_AWAY_LOD ] = str( round( levelOfDetail * 100, 1 ) ) + " %"
        
        displayTag = self.GetFirstTagOfType( object, c4d.Tdisplay )
        
        if displayTag is None:
            self.MessageToUser( tag, "This tag only works when applied to an object with a Display tag on it (and which has “Level of Detail” enabled)" )
        else:
            if not displayTag[ c4d.DISPLAYTAG_AFFECT_LEVELOFDETAIL ]:
                self.MessageToUser( tag, "The Display tag does not have “Level of Detail” enabled – you won’t see anything unless you turn this on" )
                
            displayTag[c4d.DISPLAYTAG_LEVELOFDETAIL] = levelOfDetail
        
        return c4d.EXECUTIONRESULT_OK
    
