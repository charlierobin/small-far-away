# -*- coding: utf8 -*-
# written by charlie robin / charlierobin.com / 2017

import c4d, ControllerWithLevels

OBJECT_NAMES = "objectNames"
DISTANCES = ControllerWithLevels.DISTANCES

class InstanceController( ControllerWithLevels.ControllerWithLevels ):

    PLUGIN_NAME = "Instance Controller"
    PLUGIN_ID = 1039267

    def __init__( self ):
        
        super( InstanceController, self ).__init__()
        
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
        
        result = super( InstanceController, self ).Execute( tag, doc, object, bt, priority, flags )
        if result != c4d.EXECUTIONRESULT_OK: return c4d.EXECUTIONRESULT_OK
        
        if object.GetType() != c4d.Oinstance:
            self.MessageToUser( tag, "This tag only works when applied to Instance objects" )
            return c4d.EXECUTIONRESULT_OK
        
        if not tag[ c4d.SMALL_FAR_AWAY_INSTANCE_CONTROLLER_CONTAINER ]:
            
            self.MessageToUser( tag, "No container null specified" )
            return c4d.EXECUTIONRESULT_OK
            
        if not tag[ c4d.SMALL_FAR_AWAY_INSTANCE_CONTROLLER_DEFAULT_OBJECT ]:
            
            self.MessageToUser( tag, "No default object specified" )
            return c4d.EXECUTIONRESULT_OK
        
        containerObject = self.FindFirstTopLevelObjectCalled( tag[ c4d.SMALL_FAR_AWAY_INSTANCE_CONTROLLER_CONTAINER ], doc )
        
        if not containerObject:
            
            self.MessageToUser( tag, "Container “" + tag[ c4d.SMALL_FAR_AWAY_INSTANCE_CONTROLLER_CONTAINER ] + "” not found" )
            return c4d.EXECUTIONRESULT_OK
        
        if self.NumberOfLevels() == 0: self.MessageToUser( tag, "No levels specified" )
        
        searchFor = tag[ c4d.SMALL_FAR_AWAY_INSTANCE_CONTROLLER_DEFAULT_OBJECT ]
        
        level = self.GetLevel()
        
        if level > -1: searchFor = self.parameterArrays[ OBJECT_NAMES ][ level ]

        objectFound = self.FindFirstFirstLevelChildCalled( searchFor, containerObject )
        
        if objectFound:
        
            object[ c4d.INSTANCEOBJECT_LINK ] = objectFound
        
        else:
            
            self.MessageToUser( tag, "“" + searchFor + "” not found" )
            
            
        return c4d.EXECUTIONRESULT_OK
    
