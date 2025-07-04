Web VPython 3.2

"""
Spring Block Launcher / Oscillator

Our project is a combination of a simple harmonic spring-block oscillator and various other scenarios. 
The initial conditions for the oscillation can be set by the user using sliders and buttons, including the number of springs, their k constants, and if the springs are in parallel or series. 
Pressing the start button initiates the simple harmonic motion of the block. 
After the start button has been pressed, the launch button can be pressed to release the block from the spring system. 
The block will then collide with another block of equal mass in an elastic collision. 
The other block will then either fall off a cliff of adjustable height; go onto a ramp of adjustable angle; or enter a loop of adjustable radius. 
The user can choose which scenario the block will enter through a dropdown menu. 
In each senerio, the user will see a wall at the end of the platforms as well as a wall that spawns in as the block travels into the preset.
These walls are sticky and if a block touches them, the block will stop and stick to the walls, transfering all the energy into it.
This is to prevent the block from traveling too far out in view and any other complications.
The user will also be able to adjust the coefficient of friction between the surface and the blocks, which would alter the outcome of the launch.
There are graphs of the mechanical energy of the system and the x-position of the block. 

Special Notes:
The maximum value of the initial velocity slider is dynamically set so that the block never goes further than x=0.
The loop always allows the block to complete a full loop. (physically inaccurate)


Yihan Li and David Schwartzberg
"""
