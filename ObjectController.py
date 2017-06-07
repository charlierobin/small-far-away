# -*- coding: utf8 -*-
# written by charlie robin / charlierobin.com / 2017

import c4d, ControllerWithLevels

OBJECT_NAMES = "objectNames"
DISTANCES = ControllerWithLevels.DISTANCES

class ObjectController( ControllerWithLevels.ControllerWithLevels ):

    PLUGIN_NAME = "Object Controller"
    PLUGIN_ID = 1039265

    def __init__( self ):
        
        super( ObjectController, self ).__init__()
        
        self.InitParameter( OBJECT_NAMES, ControllerWithLevels.TYPE_STRING )
        self.InitParameter( DISTANCES, ControllerWithLevels.TYPE_FLOAT32 )
        
    def AppendNew( self, counter ):
    
        self.parameterArrays[ OBJECT_NAMES ].append( "New object name value " + str( counter ) )
    
    def DescriptionItemsBeforeDistance( self, node, description, singleID, groupID, newParameterID, index ):
    
        # OBJECT NAME STRING
            
        newID = newParameterID
        newParameterID = newParameterID + 1
    
        self.parameterIDArrays[ OBJECT_NAMES ].append( newID )
    
        descid = c4d.DescID( c4d.DescLevel( newID, c4d.DTYPE_STRING, node.GetType() ) )
    
        addParameter = singleID is None
    
        if not addParameter: addParameter = descid.IsPartOf( singleID )[ 0 ]
       
        if addParameter:
        
            bc = self.String()
            
            bc.SetString( c4d.DESC_NAME, "Object " + str( index + 1 ) )
            bc.SetString( c4d.DESC_SHORT_NAME, "Object" )
        
            description.SetParameter( descid, bc, groupID )
    
        return newParameterID

    def Execute( self, tag, doc, object, bt, priority, flags ):
        
        result = super( ObjectController, self ).Execute( tag, doc, object, bt, priority, flags )
        if result != c4d.EXECUTIONRESULT_OK: return c4d.EXECUTIONRESULT_OK

        if not tag[ c4d.SMALL_FAR_AWAY_OBJECT_CONTROLLER_DEFAULT_OBJECT ]:
            
            self.MessageToUser( tag, "No default object specified" )
            return c4d.EXECUTIONRESULT_OK
        
        if self.NumberOfLevels() == 0: self.MessageToUser( tag, "No levels specified" )
            
        nameOfObjectToMakeActive = tag[ c4d.SMALL_FAR_AWAY_OBJECT_CONTROLLER_DEFAULT_OBJECT ]
        defaultObject = self.FindFirstFirstLevelChildCalled( nameOfObjectToMakeActive, object )
           
        level = self.GetLevel()
        
        if level > -1: nameOfObjectToMakeActive = self.parameterArrays[ OBJECT_NAMES ][ level ]
           
        if defaultObject is None:
            self.MessageToUser( tag, "Default object “" + tag[ c4d.SMALL_FAR_AWAY_OBJECT_CONTROLLER_DEFAULT_OBJECT ] + "” not found" )
        else:
            if nameOfObjectToMakeActive == tag[ c4d.SMALL_FAR_AWAY_OBJECT_CONTROLLER_DEFAULT_OBJECT ]:
                self.SetObjectAllOn( defaultObject )
            else:
                self.SetObjectAllOff( defaultObject )
        
        for name in self.parameterArrays[ OBJECT_NAMES ]:
            levelObject = self.FindFirstFirstLevelChildCalled( name, object )
            if levelObject is None:
                self.MessageToUser( tag, "“" + name + "” not found" )
            else:
                if name == nameOfObjectToMakeActive:
                    self.SetObjectAllOn( levelObject )
                else:
                    self.SetObjectAllOff( levelObject )
        
        return c4d.EXECUTIONRESULT_OK
