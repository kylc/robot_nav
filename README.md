Robot Navigation
================

A 2-dimensional robot navigation library using potential fields for use on the
Oregon State University Robotics Club Aerial Team's quadcopter.

Algorithm
---------

At each step below, calculate the repelling force of the walls and any
obstacles.  Sum them with the attracting force of the target unknowns.

1. Raytrace a circle around the current location at a constant radius, locating
   all contiguous points of unknown occupancy.  For each contiguous arc, mark
   the center of the arc as a target point.  We now have a list of targets.

2. Add the unknown points as children to the current node of the waypoint tree.

3. Explore the tree depth-first.

4. If the final target is found, traverse the tree directly back to the root
   node.

Example
-------

![example](assets/figure_1.png)
