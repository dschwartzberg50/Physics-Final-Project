Web VPython 3.2

scene = canvas(width=600, height=500)

# line = curve(pos=[pivot.pos, ball.pos], color=color.red)

block = box(pos=vec(4, 0, 0), length=1, height=1, width=1)
dt = 0.01

mass = 20
k = 4
vel = 0
block_x = block.pos.x
x_equilibrium = 2
    
#block=box()
#dt, mass, k, vel, block_x, x_equilibrium = 0,0,0,0,0
    


sphere(pos=vec(x_equilibrium,0,0), radius=0.1)
    
myevt = scene.pause()
    
while (True):
    rate(1/dt)

    F = -k*(block.pos.x - x_equilibrium)
    acc = F / mass
    vel += acc
    block_x += vel
    
    block.pos = vec(block_x, 0, 0)
    
