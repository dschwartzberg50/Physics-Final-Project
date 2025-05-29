Web VPython 3.2

scene = canvas(width=600, height=500, title="Spring Oscillator!\n")

def start_button_function(evt):
    start_button.started = True
    start_button.disabled = True
    launch_button.disabled = False
start_button = button(bind=start_button_function, text='Start', background=color.green, pos=scene.title_anchor, disabled=False, started=False)

def launch_button_function(evt):
    launch_button.launched = True
    launch_button.disabled = True
launch_button = button(bind=launch_button_function, text='Launch', background=color.blue, pos=scene.title_anchor, disabled=True, launched=False)

#graph set up
KE_and_U_graph = graph(width=300, height=350, title="Kinetic and Potential Energy of Box", xtitle="time(s)", ytitle="Energy(KJ)", align='right')
KE_curve = gcurve(color=color.blue, graph=KE_and_U_graph)
U_curve = gcurve(color=color.red, graph=KE_and_U_graph)
position_graph = graph(width=300, height=350, title="X Position of Box", xtitle="time(s)", ytitle="Position(meters)", align='right')
position_curve = gcurve(color=color.purple, graph=position_graph)
for x in arange(0, 2*pi, pi/20):
        KE_curve.plot(x, sin(x))
        U_curve.plot(x, cos(x))
        position_curve.plot(x, sin(x))

def spring_slider_function(evt):
    spring_slider_text.text = f"Number of Springs: {evt.value}"

spring_slider = slider(bind=spring_slider_function, min=1, max=5, step=1, value=2, length=200, id="spring_slider", pos=scene.caption_anchor)
spring_slider_text = wtext(text=f"Number of Springs: {spring_slider.value}", pos=scene.caption_anchor)

def spring_mode_button_function(evt):
    spring_mode_button.is_series_mode = not spring_mode_button.is_series_mode
    spring_mode_button.text = "Series" if spring_mode_button.is_series_mode else "Parallel"
 
scene.append_to_caption("     ")
spring_mode_button = button(bind=spring_mode_button_function, text="Series", pos=scene.caption_anchor, is_series_mode=True)
# is_series_mode: True = series, False = parallel

#presets dropdown
def presetselect(evt):
    pass
presetlist = ['Cliff', 'Upwards Slope', 'Downwards Slope', 'Loop', 'Coaster']
scene.append_to_caption("     ")
menu(bind=presetselect, choices=presetlist, pos=scene.caption_anchor)
    

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

# initial while loop for spring-oscillatory motion    
while (True):
    rate(1/dt)
#    print(f"{running=}, {launched=}")
    
    if (launch_button.launched): break
    if (not start_button.started): continue

    F = -k*(block.pos.x - x_equilibrium)
    acc = F / mass
    vel += acc
    block_x += vel
    
    block.pos = vec(block_x, 0, 0)
    
    
    spring_visual.pos=vec(x_equilibrium, 0, 0)
    spring_visual.axis=block.pos-vec(x_equilibrium, 0, 0)
    
    
# second while loop for projectile motion after block has been launched
while (True):
    rate(1/dt)
    pass
