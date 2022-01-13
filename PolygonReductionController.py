# -*- coding: utf8 -*-
# written by charlie robin / charlierobin.com / 2017

import c4d, ControllerBaseClass

class PolygonReductionController( ControllerBaseClass.ControllerBaseClass ):
    
    PLUGIN_NAME = "Polygon Reduction Controller"
    PLUGIN_ID = 1039266
    
    OPOLYREDUX = 465002101
    STRENGTH = 1000
    
    def Init( self, node ):
        
        result = super( PolygonReductionController, self ).Init( node )
        
        node[ c4d.SMALL_FAR_AWAY_POLYGON_REDUCTION_MIN_DISTANCE ] = 100.0
        node[ c4d.SMALL_FAR_AWAY_POLYGON_REDUCTION_MAX_DISTANCE ] = 1000.0
        
        node[ c4d.SMALL_FAR_AWAY_POLYGON_REDUCTION_MIN_REDUCTION_STRENGTH ] = 0.1
        node[ c4d.SMALL_FAR_AWAY_POLYGON_REDUCTION_MAX_REDUCTION_STRENGTH ] = 0.9
        
        # TODO ... falloffs (only linear at the moment ... perspective?)
        
        return True
    
    def Execute( self, tag, doc, object, bt, priority, flags ):
        
        result = super( PolygonReductionController, self ).Execute( tag, doc, object, bt, priority, flags )
        
        if result != c4d.EXECUTIONRESULT_OK: return c4d.EXECUTIONRESULT_OK
        
        if object.GetType() != OPOLYREDUX:
            self.MessageToUser( tag, "This tag only works when applied to Polygon Reduction generators" )
            return c4d.EXECUTIONRESULT_OK
        
        if self.calculatedDistance <= tag[ c4d.SMALL_FAR_AWAY_POLYGON_REDUCTION_MIN_DISTANCE ]: 
            reductionStrength = tag[ c4d.SMALL_FAR_AWAY_POLYGON_REDUCTION_MIN_REDUCTION_STRENGTH ]
        elif self.calculatedDistance >= tag[ c4d.SMALL_FAR_AWAY_POLYGON_REDUCTION_MAX_DISTANCE ]: 
            reductionStrength = tag[ c4d.SMALL_FAR_AWAY_POLYGON_REDUCTION_MAX_REDUCTION_STRENGTH ]
        else:
            dStrength = tag[ c4d.SMALL_FAR_AWAY_POLYGON_REDUCTION_MAX_REDUCTION_STRENGTH ] - tag[ c4d.SMALL_FAR_AWAY_POLYGON_REDUCTION_MIN_REDUCTION_STRENGTH ]
            dDistance = tag[ c4d.SMALL_FAR_AWAY_POLYGON_REDUCTION_MAX_DISTANCE ] - tag[ c4d.SMALL_FAR_AWAY_POLYGON_REDUCTION_MIN_DISTANCE ]
            
            unit = dStrength / dDistance
            
            reductionStrength = tag[ c4d.SMALL_FAR_AWAY_POLYGON_REDUCTION_MIN_REDUCTION_STRENGTH ]
            reductionStrength = reductionStrength + ( ( self.calculatedDistance - tag[ c4d.SMALL_FAR_AWAY_POLYGON_REDUCTION_MIN_DISTANCE ] ) * unit )
        
        tag[ c4d.SMALL_FAR_AWAY_POLYGON_REDUCTION_REDUCTION_STRENGTH ] = str( reductionStrength )
        
        object[ STRENGTH ] = reductionStrength
        
        return c4d.EXECUTIONRESULT_OK
    
    