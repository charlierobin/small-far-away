# -*- coding: utf8 -*-
# written by charlie robin / charlierobin.com / 2017

import c4d, math, re

TRACK_OBJECT = 1001
DISTANCE_DISPLAY = 1002
MESSAGES = 1004

NEWLINE = "\n"

COMMAND_CLEAR_CONSOLE = 13957
COMMAND_SHOW_CONSOLE = 12305

class ControllerBaseClass( c4d.plugins.TagData ):

    def __init__( self ):
	
        self.calculatedDistance = 0

    def Init( self, node ):
        
        pd = node[ c4d.EXPRESSION_PRIORITY ]
        
        if pd is not None:
            
            pd.SetPriorityValue( c4d.PRIORITYVALUE_CAMERADEPENDENT, True )
            node[ c4d.EXPRESSION_PRIORITY ] = pd        
        
        return True
    
    def Execute( self, tag, doc, object, bt, priority, flags ):
        
        self.ClearUserMessages( tag )
        
        if not tag[ TRACK_OBJECT ]:
            
            tag[ TRACK_OBJECT ] = self.FindFirstTopLevelObjectCalled("Camera", doc)
            
            if not tag[ TRACK_OBJECT ]:
                
                tag[ DISTANCE_DISPLAY ] = "(please set a tracking object - usually a camera, but can be anything)"
                
                # must return c4d.EXECUTIONRESULT_OK or a couple of other options from Execute,
                # but this method always overriden by subclasses, they use None to tell if track object
                # not set, skip if not. They return c4d.EXECUTIONRESULT_OK
                
                return None
        
        self.calculatedDistance = self.Distance( object.GetMg().off, tag[ TRACK_OBJECT ].GetMg().off )
        
        tag[ DISTANCE_DISPLAY ] = str( self.calculatedDistance )
        
        return c4d.EXECUTIONRESULT_OK
    
    def Distance( self, p1, p2 ):
    
        x = p2.x - p1.x
        y = p2.y - p1.y
        z = p2.z - p1.z
        
        return math.sqrt( x*x + y*y + z*z )    
    
    def ClearUserMessages( self, op ):
        
        op[ MESSAGES ] = ""
        
    def MessageToUser( self, op, text ):
        
        if not op[ MESSAGES ]: op[ MESSAGES ] = ""
        
        op[ MESSAGES ] = op[ MESSAGES ] + text + NEWLINE
    
    def FindFirstTopLevelObjectCalled( self, searchString, doc ):
    
        # TODO check out BaseDocument.SearchObject( name )
    
        found = None
        nextObject = doc.GetFirstObject()
        
        while nextObject:
    
            if nextObject.GetName() == searchString: 
                found = nextObject
                break
                
            nextObject = nextObject.GetNext()
            
        return found
    
    def FindFirstFirstLevelChildCalled( self, searchString, object ):

        found = None
        nextChild = object.GetDown()
        
        while nextChild:
    
            if nextChild.GetName() == searchString: 
                found = nextChild
                break
                
            nextChild = nextChild.GetNext()
            
        return found
    
    def FindFirstFirstLevelChildCalledWithRegEx( self, searchString, object ):

        found = None
        nextChild = object.GetDown()
        
        while nextChild:
            
            matchObj = re.search( searchString, nextChild.GetName(), re.I )
            
            if matchObj: 
                found = nextChild
                break
                
            nextChild = nextChild.GetNext()

        return found
    
    def FindAllFirstLevelChildrenCalled( self, regex, object ):
            
        found = []
        
        nextChild = object.GetDown()
            
        while nextChild:
    
            matchObj = re.search( regex, nextChild.GetName(), re.I )
            
            if matchObj: 
                
                found = nextChild
                                
            nextChild = nextChild.GetNext()              

        return found
    
    def GetChildren( self, object ):
    
        children = []
    
        nextChild = object.GetDown()
        
        while nextChild:

            children.append( nextChild )

            nextChild = nextChild.GetNext()     
            
        return children
        
    def SetObjectAllOn( self, object ):
    
        object.SetEditorMode( c4d.MODE_UNDEF )
        object.SetRenderMode( c4d.MODE_UNDEF )
        object.SetDeformMode( True )
            
    def SetObjectAllOff( self, object ):
    
        object.SetEditorMode( c4d.MODE_OFF )
        object.SetRenderMode( c4d.MODE_OFF )
        object.SetDeformMode( False )
 
    def GetFirstTagOfType( self, object, type ):
    
        foundTag = None
        
        for possibleTag in object.GetTags():
            
            if possibleTag.GetType() == type:
                
                foundTag = possibleTag
                break
                
        return foundTag
        
        