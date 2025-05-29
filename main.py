Web VPython 3.2

scene = canvas(width=600, height=500)

#graph set up
g1 = graph(width=300, height=350, title="Kinetic and Potential Energy of Box", xtitle="time(s)", ytitle="Energy(KJ)", align='right')
KE_graph = gcurve(color=color.blue, graph=g1)
U_graph = gcurve(color=color.red, graph=g1)
g2 = graph(width=300, height=350, title="X Position of Box", xtitle="time(s)", ytitle="Position(meters)", align='right')
path_graph = gcurve(color=color.purple, graph=g2)
for x in arange(0, 2*pi, pi/20):
        KE_graph.plot(x, sin(x))
        U_graph.plot(x, cos(x))
        path_graph.plot(x, sin(x))

def spring_slider_function(evt):
    spring_slider_text.text = f"Number of Springs: {evt.value}"

spring_slider = slider(bind=spring_slider_function, min=1, max=5, step=1, value=2, length=200, id="spring_slider")
spring_slider_text = wtext(text=f"Number of Springs: {spring_slider.value}")

def spring_mode_button_function(evt):
    global is_series_mode
    is_series_mode = not is_series_mode
    spring_mode_button.text = "Series" if is_series_mode else "Parallel"
    print(is_series_mode)
 
scene.append_to_caption("     ")
is_series_mode = True # True = series, False = parallel
spring_mode_button = button(bind=spring_mode_button_function, text="Series")


#presets dropdown
def presetselect(evt):
    pass
presetlist = ['Cliff', 'Upwards Slope', 'Downwards Slope', 'Loop', 'Coaster']
scene.append_to_caption("     ")
menu(bind=presetselect, choices=presetlist)
    

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
    
