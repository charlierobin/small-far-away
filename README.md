# small-far-away
A simple suite of level of detail plug-ins for Cinema 4D. Implemented as tags. Some are applied to any object type, others only work when applied to particular object types, some only work when there is a Cinema 4D “Display” tag applied.

Object Controller Tag
Swap out higher polygon count objects and replace them with lower count versions. Can be applied to any object type.

Instance Controller Tag
As above, but only works when applied to a Cinema 4D instance. Changes the source of the instance.

Visibility Controller Tag
Can be applied to any object type. Turn off generators/visibility as objects get further away from the camera.

Polygon Reduction Controller
Apply increasingly aggressive polygon reduction strength as distance between object and camera increases. Only works when applied to a Polygon Reduction object.

Texture Controller Tag
Turn off materials/textures as objects get further away from the camera. Needs the Cinema 4D Display tag on the same object/hierarchy.

Enhanced OpenGL Controller Tag
Turn off enhanced OpenGL features for objects more than a certain distance away from the camera. Needs the Cinema 4D Display tag on the same object/hierarchy.

Shading Mode/Style Controller
Also requires the Cinema 4D Display tag on the same object/hierarchy. Allows simpler/faster shading styles to be applied to objects as they get further away.

Level of Detail Controller
Applied to any object with a “Display” tag. Sets objects further away to display with a lower level of detail.

Some of the tags operate using minimum distance/minimum value/maximum distance/maximum value, scaling the actual reduction value in between the minimum and maximum. Others operate using levels/distance bands, so a particular setting is only applied when between the distances specified by that level.

Please note that at the moment these are all only good with release 18.

http://charlierobin.com/small-far-away
