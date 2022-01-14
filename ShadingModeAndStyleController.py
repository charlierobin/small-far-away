# -*- coding: utf8 -*-
# written by charlie robin / charlierobin.com / 2017

import c4d, ControllerWithLevels, os

SDISPLAYMODE = "SDISPLAYMODE"
WDISPLAYMODE = "WDISPLAYMODE"
DISTANCES = ControllerWithLevels.DISTANCES

class ShadingModeAndStyleController( ControllerWithLevels.ControllerWithLevels ):
    
    PLUGIN_NAME = "Shading Mode and Style Controller"
    PLUGIN_ID = 1039368
    
    def __init__( self ):
        
        super( ShadingModeAndStyleController, self ).__init__()
    
        self.InitParameter( SDISPLAYMODE, ControllerWithLevels.TYPE_LONG )
        self.InitParameter( WDISPLAYMODE, ControllerWithLevels.TYPE_LONG )
        self.InitParameter( DISTANCES, ControllerWithLevels.TYPE_FLOAT32 )
  
    def Init( self, node ):
        
        result = super( ShadingModeAndStyleController, self ).Init( node )
        
        node[ c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_SDISPLAYMODE_DEFAULT ] = c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_SDISPLAYMODE_GOURAUD_SHADING
        node[ c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_WDISPLAYMODE_DEFAULT ] = c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_WDISPLAYMODE_WIRE
        
        # TODO ... some smarter stuff on add to object?
        # eg: look for another tag, if tracking object defined take it (saves user a little time)
        
        return True
        
    def AppendNew( self, counter ):
    
        self.parameterArrays[ SDISPLAYMODE ].append( c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_SDISPLAYMODE_GOURAUD_SHADING )
        self.parameterArrays[ WDISPLAYMODE ].append( c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_WDISPLAYMODE_WIRE )
    
    def PopupSDISPLAYMODE( self ):
    
        bc = c4d.GetCustomDatatypeDefault( c4d.DTYPE_LONG )
        
        bc.SetInt32( c4d.DESC_CUSTOMGUI, c4d.CUSTOMGUI_CYCLE )
        bc.SetInt32( c4d.DESC_MIN, 0 )
        bc.SetInt32( c4d.DESC_MAX, 7 )
    
        cycle = c4d.BaseContainer()
        
        cycle.SetString( c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_SDISPLAYMODE_GOURAUD_SHADING, "Gouraud Shading" )
        cycle.SetString( c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_SDISPLAYMODE_GOURAUD_SHADING_LINES, "Gouraud Shading (Lines)" )
        cycle.SetString( c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_SDISPLAYMODE_QUICK_SHADING, "Quick Shading" )
        cycle.SetString( c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_SDISPLAYMODE_QUICK_SHADING_LINES, "Quick Shading (Lines)" )
        cycle.SetString( c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_SDISPLAYMODE_CONSTANT_SHADING, "Constant Shading" )
        cycle.SetString( c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_SDISPLAYMODE_CONSTANT_SHADING_LINES, "Constant Shading (Lines)" )
        cycle.SetString( c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_SDISPLAYMODE_HIDDEN, "Hidden Line" )
        cycle.SetString( c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_SDISPLAYMODE_LINES, "Lines" )
        
        bc.SetContainer( c4d.DESC_CYCLE, cycle )
    
        return bc
        
    def PopupWDISPLAYMODE( self ):
    
        bc = c4d.GetCustomDatatypeDefault( c4d.DTYPE_LONG )
        
        bc.SetInt32( c4d.DESC_CUSTOMGUI, c4d.CUSTOMGUI_CYCLE )
        bc.SetInt32( c4d.DESC_MIN, 0 )
        bc.SetInt32( c4d.DESC_MAX, 3 )
    
        cycle = c4d.BaseContainer()
        
        cycle.SetString( c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_WDISPLAYMODE_WIRE, "Wireframe" )
        cycle.SetString( c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_WDISPLAYMODE_ISOPARM, "Isoparms" )
        cycle.SetString( c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_WDISPLAYMODE_BOX, "Box" )
        cycle.SetString( c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_WDISPLAYMODE_SKELETON, "Skeleton" )

        bc.SetContainer( c4d.DESC_CYCLE, cycle )
    
        return bc
    
    def DescriptionItemsBeforeDistance( self, node, description, singleID, groupID, newParameterID, index ):
    
        # SDISPLAYMODE POPUP MENU
            
        newID = newParameterID
        newParameterID = newParameterID + 1
    
        self.parameterIDArrays[ SDISPLAYMODE ].append( newID )
    
        descid = c4d.DescID( c4d.DescLevel( newID, c4d.DTYPE_LONG, node.GetType() ) )
    
        addParameter = singleID is None
    
        if not addParameter: addParameter = descid.IsPartOf( singleID )[ 0 ]
       
        if addParameter:
        
            bc = self.PopupSDISPLAYMODE()
            
            bc.SetString( c4d.DESC_NAME, "SDISPLAYMODE " + str( index + 1 ) )
            bc.SetString( c4d.DESC_SHORT_NAME, "Shading Mode" )
        
            description.SetParameter( descid, bc, groupID )
    
        # WDISPLAYMODE POPUP MENU
            
        newID = newParameterID
        newParameterID = newParameterID + 1
    
        self.parameterIDArrays[ WDISPLAYMODE ].append( newID )
    
        descid = c4d.DescID( c4d.DescLevel( newID, c4d.DTYPE_LONG, node.GetType() ) )
    
        addParameter = singleID is None
    
        if not addParameter: addParameter = descid.IsPartOf( singleID )[ 0 ]
       
        if addParameter:
        
            bc = self.PopupWDISPLAYMODE()
            
            bc.SetString( c4d.DESC_NAME, "WDISPLAYMODE " + str( index + 1 ) )
            bc.SetString( c4d.DESC_SHORT_NAME, "Style" )
        
            description.SetParameter( descid, bc, groupID )
    
        return newParameterID
  
    def Execute( self, tag, doc, object, bt, priority, flags ):
        
        result = super( ShadingModeAndStyleController, self ).Execute( tag, doc, object, bt, priority, flags )
        if result != c4d.EXECUTIONRESULT_OK: return c4d.EXECUTIONRESULT_OK
        
        if self.NumberOfLevels() == 0: self.MessageToUser( tag, "No levels specified" )
        
        SDISPLAYMODE_final = tag[ c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_SDISPLAYMODE_DEFAULT ]
        WDISPLAYMODE_final = tag[ c4d.SMALL_FAR_AWAY_SHADING_MODE_CONTROLLER_WDISPLAYMODE_DEFAULT ]
        
        level = self.GetLevel()
        
        if level > -1:
            SDISPLAYMODE_final = self.parameterArrays[ SDISPLAYMODE ][ level ]
            WDISPLAYMODE_final = self.parameterArrays[ WDISPLAYMODE ][ level ]
         
        displayTag = self.GetFirstTagOfType( object, c4d.Tdisplay )
        
        if displayTag is None:
            
            # self.MessageToUser( tag, "This tag only works when applied to an object with a Display tag on it" )
            
            doc.StartUndo()
            
            object.MakeTag(c4d.Tdisplay)
            
            displayTag = self.GetFirstTagOfType( object, c4d.Tdisplay )
            
            displayTag[ c4d.DISPLAYTAG_AFFECT_DISPLAYMODE ] = True
            
            c4d.EventAdd()
            
            doc.EndUndo()
            
        else:
            if not displayTag[ c4d.DISPLAYTAG_AFFECT_DISPLAYMODE ]:
                self.MessageToUser( tag, "The Display tag does not have “Use Shading Mode/Style” enabled – you won’t see anything unless you turn this on" )

            displayTag[c4d.DISPLAYTAG_SDISPLAYMODE] = SDISPLAYMODE_final
            displayTag[c4d.DISPLAYTAG_WDISPLAYMODE] = WDISPLAYMODE_final

        return c4d.EXECUTIONRESULT_OK
  