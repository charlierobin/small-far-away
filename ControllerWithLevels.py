# -*- coding: utf8 -*-
# written by charlie robin / charlierobin.com / 2017

import c4d, copy, ControllerBaseClass

ADD_BUTTON = 1005

GROUP_OFFSET = 1500
FIRST_DYNAMIC_PARAMETER = 1501

TYPE_STRING = "String"
TYPE_FLOAT32 = "Float32"
TYPE_LONG = "Long"

DISTANCES = "distances"

LAST = -1

SLIDER_DEFAULT_MAX = 10000.0
LAST_SLIDER_MULTIPLY_FACTOR = 2.0
MINIMUM_DEFAULT_DISTANCE = 200
DISTANCE_INCREMENT = 10

class ControllerWithLevels( ControllerBaseClass.ControllerBaseClass ):

    def __init__( self ):
	
        super( ControllerWithLevels, self ).__init__()
		
        self.parameterArrays = {}
        self.parameterTypes = {}
        
        # these ones below are re-initialised every time in GetDDescription() method
        
        self.parameterIDArrays = {}

        self.deleteButtonsParameterIDs = []
        self.upButtonsParameterIDs = []
        self.downButtonsParameterIDs = []
        
        self.newItemCounter = 1
        
    def InitParameter( self, name, type ):
    
        self.parameterArrays[ name ] = []
        self.parameterTypes[ name ] = type
       	self.parameterIDArrays[ name ] = []

    def NumberOfLevels( self ):
        
        return len( self.parameterArrays.values()[ 0 ] )  # what if none specified? - out of bounds

    def GetLevel( self ):
    
        highestIndex = -1
        
        for index in xrange( self.NumberOfLevels() ):
            if self.calculatedDistance > self.parameterArrays[ DISTANCES ][ index ]:
                highestIndex = index
    
        return highestIndex
        
    def GetLengthOf( self, name ):
    
        return len( self.parameterArrays[ name ] )

    def CopyTo( self, dest, snode, dnode, flags, trn ):

        for name, array in self.parameterArrays.iteritems(): dest.parameterArrays[ name ] = copy.copy( array )
        return True
        
    def Read( self, node, hf, level ):

        self.parameterArrays = {}
        self.parameterTypes = {}
        
        numberOfParameters = hf.ReadInt32()

        for idx in xrange( numberOfParameters ):

            name = hf.ReadString()
            type = hf.ReadString()
            array = []
            count = hf.ReadInt32()

            if type == TYPE_FLOAT32:
                for idx in xrange( count ): array.append( hf.ReadFloat32() )
            elif type == TYPE_LONG:
                for idx in xrange( count ): array.append( hf.ReadInt32() )
            else:
                for idx in xrange( count ): array.append( hf.ReadString() )
                
            self.parameterArrays[ name ] = array
            self.parameterTypes[ name ] = type
            
        return True 
        
    def Write( self, node, hf ):

        numberOfParameters = len( self.parameterArrays )
        hf.WriteInt32( numberOfParameters )
        
        for name, array in self.parameterArrays.iteritems():
        
            hf.WriteString( name )
            hf.WriteString( self.parameterTypes[ name ] )
        
            hf.WriteInt32( len( array ) )

            if self.parameterTypes[ name ] == TYPE_FLOAT32:
                for value in array: hf.WriteFloat32( value )
            elif self.parameterTypes[ name ] == TYPE_LONG:
                for value in array: hf.WriteInt32( value )
            else:
                for value in array: hf.WriteString( value )

        return True
        
    def AppendNew( self, counter ):
    
        pass # override this method in subclasses
    
    def GetDParameter( self, node, id, flags ):

        paramID = id[ 0 ].id

        for name, array in self.parameterIDArrays.iteritems():

            if paramID in array:
            
                data = self.parameterArrays[ name ][ array.index( paramID ) ]
                return ( True, data, flags | c4d.DESCFLAGS_GET_PARAM_GET )

        return False
    
    def SetDParameter( self, node, id, data, flags ):

        paramID = id[ 0 ].id
    
        for name, array in self.parameterIDArrays.iteritems():

            if paramID in array:
            
                self.parameterArrays[ name ][ array.index( paramID ) ] = data            
                return ( True, flags | c4d.DESCFLAGS_SET_PARAM_SET )

        return False
    
    def Message( self, node, type, data ):
    
        if type == c4d.MSG_DESCRIPTION_COMMAND:
    
            paramID = data[ 'id' ][ 0 ].id
    
            if paramID in self.upButtonsParameterIDs:
    
                # add 1 because first button does not have "move up" function, 
                # therefore first button in array is in fact second button etc
                
                i1 = 1 + self.upButtonsParameterIDs.index( paramID )
                i2 = i1 - 1
               
                for name, array in self.parameterArrays.iteritems():
                    if name != DISTANCES: array[ i1 ], array[ i2 ] = array[ i2 ], array[ i1 ]
                
            if paramID in self.downButtonsParameterIDs:
    
                i1 = self.downButtonsParameterIDs.index( paramID )
                i2 = i1 + 1
            
                for name, array in self.parameterArrays.iteritems():
                    if name != DISTANCES: array[ i1 ], array[ i2 ] = array[ i2 ], array[ i1 ]
              
            if paramID in self.deleteButtonsParameterIDs:
    
                for name, array in self.parameterArrays.iteritems():
                    del array[ self.deleteButtonsParameterIDs.index( paramID ) ]
                
                self.MessageToUser( node, "Item removed" )
               
            if paramID == ADD_BUTTON:
    
                self.AppendNew( self.newItemCounter )
                
                self.newItemCounter = self.newItemCounter + 1
                highestValue = 0.0
                
                if len( self.parameterArrays[ DISTANCES ] ) > 0:
                    highestValue = self.parameterArrays[ DISTANCES ][ LAST ] + DISTANCE_INCREMENT
                else:
                    highestValue = self.calculatedDistance
                
                if highestValue == 0: highestValue = MINIMUM_DEFAULT_DISTANCE
                
                self.parameterArrays[ DISTANCES ].append( highestValue )
                self.MessageToUser( node, "Item added" )
                
        return True

    def Button( self ):

        bc = c4d.GetCustomDataTypeDefault( c4d.DTYPE_BUTTON )
        bc.SetInt32( c4d.DESC_CUSTOMGUI, c4d.CUSTOMGUI_BUTTON )
    
        return bc
        
    def Separator( self ):
    
        bc = c4d.GetCustomDataTypeDefault( c4d.DTYPE_SEPARATOR )
        bc.SetInt32( c4d.DESC_CUSTOMGUI, c4d.DTYPE_SEPARATOR )
        bc.SetBool( c4d.DESC_SEPARATORLINE, True )
    
        return bc
    
    def Long( self ):
    
        bc = c4d.GetCustomDataTypeDefault( c4d.DTYPE_LONG )
        bc.SetInt32( c4d.DESC_ANIMATE, c4d.DESC_ANIMATE_ON )
        bc.SetBool( c4d.DESC_REMOVEABLE, False )
        
        return bc
        
    def RealSlider( self ):
    
        bc = c4d.GetCustomDataTypeDefault( c4d.DTYPE_REAL )
        bc.SetInt32( c4d.DESC_CUSTOMGUI, c4d.CUSTOMGUI_REALSLIDER )
        bc.SetFloat( c4d.DESC_MIN, 0.0 )
        bc.SetFloat( c4d.DESC_MAX, 10000.0 )
        bc.SetFloat( c4d.DESC_MINSLIDER, 0.0 )
        bc.SetFloat( c4d.DESC_MAXSLIDER, 10000.0 )
        bc.SetFloat( c4d.DESC_STEP, 0.01 )
        bc.SetInt32( c4d.DESC_UNIT, c4d.DESC_UNIT_FLOAT )
        bc.SetInt32( c4d.DESC_ANIMATE, c4d.DESC_ANIMATE_ON )
        bc.SetBool( c4d.DESC_REMOVEABLE, False )

        return bc
        
    def String( self ):

        bc = c4d.GetCustomDataTypeDefault( c4d.DTYPE_STRING )
        bc.SetInt32( c4d.DESC_ANIMATE, c4d.DESC_ANIMATE_ON )
        bc.SetBool( c4d.DESC_REMOVEABLE, False )
    
        return bc

    def Group( self ):
    
        bc = c4d.GetCustomDataTypeDefault( c4d.DTYPE_GROUP )
        bc.SetString( c4d.DESC_NAME, "Levels" )
        bc.SetInt32( c4d.DESC_COLUMNS, 1 )
        bc.SetInt32( c4d.DESC_DEFAULT, 1 )
        
        return bc

    def DescriptionItemsBeforeDistance( self, node, description, singleID, groupID, newParameterID, index ):
    
        return newParameterID

    def DescriptionItemsAfterDistance( self, node, description, singleID, groupID, newParameterID, index ):
    
        return newParameterID

    def GetDDescription( self, node, description, flags ):
    
        if not description.LoadDescription( node.GetType() ): return False

        singleID = description.GetSingleDescID()
    
        groupID = c4d.DescID( c4d.DescLevel( GROUP_OFFSET, c4d.DTYPE_GROUP, node.GetType() ) )

        addDynamicGroup = singleID is None
    
        if not addDynamicGroup: addDynamicGroup = groupID.IsPartOf( singleID )[ 0 ]

        if addDynamicGroup: description.SetParameter( groupID, self.Group(), c4d.DescID( c4d.DescLevel( ( c4d.ID_OBJECTPROPERTIES ) ) ) )


        newParameterID = FIRST_DYNAMIC_PARAMETER

        self.parameterIDArrays = {}
        
        for name, array in self.parameterArrays.iteritems(): self.parameterIDArrays[ name ] = []
        
        self.deleteButtonsParameterIDs = []
        self.upButtonsParameterIDs = []
        self.downButtonsParameterIDs = []

        for index in xrange( self.NumberOfLevels() ):

            sliderMin = 0.0
            sliderMax = SLIDER_DEFAULT_MAX
        
            if self.NumberOfLevels() > 1:
        
                if index > 0: sliderMin = self.parameterArrays[ DISTANCES ][ index - 1 ]
                if index < self.NumberOfLevels() - 1: sliderMax = self.parameterArrays[ DISTANCES ][ index + 1 ]
                if index == self.NumberOfLevels() - 1: sliderMax = LAST_SLIDER_MULTIPLY_FACTOR * self.parameterArrays[ DISTANCES ][ index ]
            
            newParameterID = self.DescriptionItemsBeforeDistance( node, description, singleID, groupID, newParameterID, index )
            
            # DISTANCE SLIDER REAL (FLOAT)
        
            newID = newParameterID
            newParameterID = newParameterID + 1
    
            self.parameterIDArrays[ DISTANCES ].append( newID )
    
            descid = c4d.DescID( c4d.DescLevel( newID, c4d.DTYPE_REAL, node.GetType() ) )
    
            addParameter = singleID is None
    
            if not addParameter: addParameter = descid.IsPartOf( singleID )[ 0 ]
       
            if addParameter:
        
                bc = self.RealSlider()
            
                bc.SetString( c4d.DESC_NAME, "Distance " + str( index + 1 ) )
                bc.SetString( c4d.DESC_SHORT_NAME, "Distance" )
                
                bc.SetFloat( c4d.DESC_MIN, sliderMin )
                bc.SetFloat( c4d.DESC_MAX, sliderMax)
        
                bc.SetFloat( c4d.DESC_MINSLIDER, sliderMin )
                bc.SetFloat( c4d.DESC_MAXSLIDER, sliderMax )
                    
                description.SetParameter( descid, bc, groupID )
            
            newParameterID = self.DescriptionItemsAfterDistance( node, description, singleID, groupID, newParameterID, index )
             
            # MOVE UP BUTTON
        
            if index > 0:
        
                newID = newParameterID
                newParameterID = newParameterID + 1
            
                self.upButtonsParameterIDs.append( newID )
            
                descid = c4d.DescID( c4d.DescLevel( newID, c4d.DTYPE_BUTTON, node.GetType() ) )
            
                addParameter = singleID is None
            
                if not addParameter: addParameter = descid.IsPartOf( singleID )[ 0 ]
               
                if addParameter:
                
                    bc = self.Button()
                
                    bc.SetString( c4d.DESC_NAME, "Up" )
                    bc.SetString( c4d.DESC_SHORT_NAME, "Up" )
                               
                    description.SetParameter( descid, bc, groupID )         
                
                
                
            # MOVE DOWN BUTTON
        
            if index < self.NumberOfLevels() - 1:
            
                newID = newParameterID
                newParameterID = newParameterID + 1
            
                self.downButtonsParameterIDs.append( newID )
            
                descid = c4d.DescID( c4d.DescLevel( newID, c4d.DTYPE_BUTTON, node.GetType() ) )
            
                addParameter = singleID is None
            
                if not addParameter: addParameter = descid.IsPartOf( singleID )[ 0 ]
               
                if addParameter:
                
                    bc = self.Button()
                    
                    bc.SetString( c4d.DESC_NAME, "Down" )
                    bc.SetString( c4d.DESC_SHORT_NAME, "Down" )
                               
                    description.SetParameter( descid, bc, groupID )
                
                
                
            
            
            # DELETE BUTTON
            
            newID = newParameterID
            newParameterID = newParameterID + 1
        
            self.deleteButtonsParameterIDs.append( newID )
        
            descid = c4d.DescID( c4d.DescLevel( newID, c4d.DTYPE_BUTTON, node.GetType() ) )
        
            addParameter = singleID is None
        
            if not addParameter: addParameter = descid.IsPartOf( singleID )[ 0 ]
           
            if addParameter:
            
                bc = self.Button()
                
                bc.SetString( c4d.DESC_NAME, "Remove" )
                bc.SetString( c4d.DESC_SHORT_NAME, "Remove" )
                           
                description.SetParameter( descid, bc, groupID )
            
                



            #SEPARATOR 
               
            newID = newParameterID
            newParameterID = newParameterID + 1

            descid = c4d.DescID( c4d.DescLevel( newID, c4d.DTYPE_SEPARATOR, node.GetType() ) )
        
            addParameter = singleID is None
        
            if not addParameter: addParameter = descid.IsPartOf( singleID )[ 0 ]
           
            if addParameter:
            
                bc = self.Separator()
            
                description.SetParameter( descid, bc, groupID )
            
            

        return ( True, flags | c4d.DESCFLAGS_DESC_LOADED )
        
        
    
    
    
    
    
    
    
    