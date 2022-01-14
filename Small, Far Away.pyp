import c4d, copy, os, sys, math, re
from c4d import bitmaps, documents, plugins

# path = c4d.storage.GeGetC4DPath( c4d.C4D_PATH_PREFS ) + "/symbolcache"
# if os.path.exists( path ): os.remove( path )

folder = os.path.dirname( __file__ )
if folder not in sys.path: sys.path.insert( 0, folder )

import ObjectController
from ObjectController import ObjectController

import PolygonReductionController
from PolygonReductionController import PolygonReductionController

import LevelOfDetailController
from LevelOfDetailController import LevelOfDetailController

import InstanceController
from InstanceController import InstanceController

import VisibilityController
from VisibilityController import VisibilityController

import ShadingModeAndStyleController
from ShadingModeAndStyleController import ShadingModeAndStyleController

import TextureController
from TextureController import TextureController

if __name__ == "__main__":
         
    theBitmap = bitmaps.BaseBitmap()
    theDirectoryPath, theFileName = os.path.split( __file__ )
    theBitmap.InitWith( os.path.join( theDirectoryPath, "res", "icon.tif" ) )

    plugins.RegisterTagPlugin( id = PolygonReductionController.PLUGIN_ID, 
                               str = PolygonReductionController.PLUGIN_NAME,
                               g = PolygonReductionController,
                               description = "PolygonReductionController", 
                               icon = theBitmap,
                               info = c4d.TAG_EXPRESSION | c4d.TAG_VISIBLE )
    
    plugins.RegisterTagPlugin( id = LevelOfDetailController.PLUGIN_ID, 
                               str = LevelOfDetailController.PLUGIN_NAME,
                               g = LevelOfDetailController,
                               description = "LevelOfDetailController", 
                               icon = theBitmap,
                               info = c4d.TAG_EXPRESSION | c4d.TAG_VISIBLE )
    
    plugins.RegisterTagPlugin( id = VisibilityController.PLUGIN_ID, 
                               str = VisibilityController.PLUGIN_NAME,
                               g = VisibilityController,
                               description = "VisibilityController", 
                               icon = theBitmap,
                               info = c4d.TAG_EXPRESSION | c4d.TAG_VISIBLE )
                               
    plugins.RegisterTagPlugin( id = TextureController.PLUGIN_ID, 
                               str = TextureController.PLUGIN_NAME,
                               g = TextureController,
                               description = "TextureController", 
                               icon = theBitmap,
                               info = c4d.TAG_EXPRESSION | c4d.TAG_VISIBLE )
                               
    plugins.RegisterTagPlugin( id = ObjectController.PLUGIN_ID, 
                               str = ObjectController.PLUGIN_NAME,
                               g = ObjectController,
                               description = "ObjectController", 
                               icon = theBitmap,
                               info = c4d.TAG_EXPRESSION | c4d.TAG_VISIBLE | c4d.TAG_MULTIPLE )
                           
    plugins.RegisterTagPlugin( id = InstanceController.PLUGIN_ID, 
                               str = InstanceController.PLUGIN_NAME,
                               g = InstanceController,
                               description = "InstanceController", 
                               icon = theBitmap,
                               info = c4d.TAG_EXPRESSION | c4d.TAG_VISIBLE )
                                   
    plugins.RegisterTagPlugin( id = ShadingModeAndStyleController.PLUGIN_ID, 
                               str = ShadingModeAndStyleController.PLUGIN_NAME,
                               g = ShadingModeAndStyleController,
                               description = "ShadingModeAndStyleController", 
                               icon = theBitmap,
                               info = c4d.TAG_EXPRESSION | c4d.TAG_VISIBLE )
                                   
   