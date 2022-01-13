# Small, Far Away
A simple suite of level of detail plug-ins for Cinema 4D. Implemented as tags. Some are applied to any object type, others only work when applied to particular object types, some only work when there is a Cinema 4D “Display” tag applied.

## New notes as of January 2022:

At some point the previous versions of these will have stopped working when Cinema 4D went from Python 2 to Python 3.

I’ve now updated them (basically, some small changes to do with Python iterators/dicts) and tested with my version of Cinema 4D R25.117 on Macintosh.

The EnhancedOpenGLController is no more, as Enhanced OpenGL is no longer a thing in Cinema 4D.

The Polygon Reduction tag used to work with the reduction deformer, but that is also no longer around, so I've changed it to work with the Polygon Reduction Generator instead.

As mentioned, I’m only able to test this on my system and with the version of Cinema 4D which I’m using, which means I’ve no idea what the impact will be on older releases.

## Object Controller Tag

Swaps out higher polygon count objects and replaces them with lower count versions. Can be applied to any object type.

## Instance Controller Tag

As above, but only works when applied to a Cinema 4D instance. Changes the source of the instance.

## Visibility Controller Tag

Can be applied to any object type. Turn off generators/visibility as objects get further away from the camera.

## Polygon Reduction Controller

Apply increasingly aggressive polygon reduction strength as distance between object and camera increases. Only works when applied to a Polygon Reduction object.

## Texture Controller Tag

Turn off materials/textures as objects get further away from the camera. Needs the Cinema 4D Display tag on the same object/hierarchy.

## Enhanced OpenGL Controller Tag

Turn off enhanced OpenGL features for objects more than a certain distance away from the camera. Needs the Cinema 4D Display tag on the same object/hierarchy.

## Shading Mode/Style Controller

Also requires the Cinema 4D Display tag on the same object/hierarchy. Allows simpler/faster shading styles to be applied to objects as they get further away.

## Level of Detail Controller

Applied to any object with a “Display” tag. Sets objects further away to display with a lower level of detail.

Some of the tags operate using minimum distance/minimum value/maximum distance/maximum value, scaling the actual reduction value in between the minimum and maximum. Others operate using levels/distance bands, so a particular setting is only applied when between the distances specified by that level.

http://charlierobin.com/small-far-away
