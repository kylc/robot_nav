Potential Field Navigation
==========================

Output from the onboard Microsoft Kinect camera is used to generate a depth map
of the camera's immediate field of view.  This depth map is then incorporated
into a progressively generated 3D map of the robot's surroundings.  Using this
3D map, the robot can intelligently navigate its way through unfamiliar
environments.

This is accomplished with a technique called potential field navigation.  The
theory is that objects within the environment can be labeled with either
attractive or repulsive forces of various values based on their danger,
distance, or other factors.  Then, a simple sum of these forces will yield the
optimal direction vector.

The implementation takes a horizontal slice of the 3D map in the XY-plane.
Processing only 2-dimensional data greatly reduces computational complexity
which allows us to perform the calculations in real-time.  Dropping the Z-axis
is acceptable because the robot shouldn't be concerned with objects above or
below, only objects in its plane.  The implementation then searches for
unexplored regions in its immediate vicinity, assigning them attractive forces.
It does the same for obstacles, but assigns them a repelling force.  The sum of
these forces is then passed to the flight controller.
