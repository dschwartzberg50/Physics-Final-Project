Web VPython 3.2

scene = canvas(width=600, height=500)

#graph set up
g1 = graph(width=300, height=350, title="Kinetic and Potential Energy of Box", xtitle="time(s)", ytitle="Energy(KJ)", align='right')
KE_graph = gcurve(color=color.blue, graph=g1)
U_graph = gcurve(color=color.red, graph=g1)
g2 = graph(width=300, height=350, title="X Position of Box", xtitle="time(s)", ytitle="Position(meters)", align='right')
path_graph = gcurve(color=color.purple, graph=g2)
for x in arange(0, 2*pi, pi/20):
        rate(30)
        KE_graph.plot(x, sin(x))
        U_graph.plot(x, cos(x))
        path_graph.plot(x, sin(x))

#presets dropdown
def presetselect(evt):
        console.log(evt)
        if evt.index < 1:
                pass
        elif evt.index is 1:
                pointer.color=color.yellow
        elif evt.index is 2:
                pointer.color=color.magenta
        elif evt.index is 3:
                pointer.color=color.cyan
        elif evt.index is 4:
                pointer.color=color.red
        elif evt.index is 5:
                pointer.color=color.blue
presetlist = ['Cliff', 'Upwards Slope', 'Downwards Slope', 'Loop', 'Coaster']
menu(bind=presetselect, choices=presetlist)
    
# line = curve(pos=[pivot.pos, ball.pos], color=color.red)

block = box(pos=vec(4, 0, 0), length=1, height=1, width=1)
dt = 0.01

mass = 20
k = 1
vel = 0
block_x = block.pos.x
x_equilibrium = 2
    
#block=box()
#dt, mass, k, vel, block_x, x_equilibrium = 0,0,0,0,0

spring_visual = helix(pos=vec(x_equilibrium, 0, 0), axis=block.pos-vec(x_equilibrium, 0, 0), color=color.red)


sphere(pos=vec(x_equilibrium,0,0), radius=0.1)
    
myevt = scene.pause()
    
while (True):
    rate(1/dt)

    F = -k*(block.pos.x - x_equilibrium)
    acc = F / mass
    vel += acc
    block_x += vel
    
    block.pos = vec(block_x, 0, 0)
    
    
    spring_visual.pos=vec(x_equilibrium, 0, 0)
    spring_visual.axis=block.pos-vec(x_equilibrium, 0, 0)
    
