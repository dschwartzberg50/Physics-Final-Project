Web VPython 3.2

scene = canvas(width=600, height=500, title="Spring Oscillator!\n")
scene.camera.pos = vec(10, 0, 20)

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
     

def change_springs():
    global visual_springs_list
    n_springs = spring_slider.value
    is_series_mode = spring_mode_button.is_series_mode
    
    if is_series_mode:
        for i, spring in enumerate(series_springs_list):
            print(i, spring)
        pass
    else:
        for i, spring in enumerate(parallel_springs_list):
            pass
        vertical_space = 5
        helix(pos=vec(x_equilibrium, 0, 0), axis=block.pos-vec(x_equilibrium, 0, 0), color=color.red)

def spring_slider_function(evt):
    spring_slider_text.text = f"Number of Springs: {evt.value}"
    change_springs()
    
spring_slider = slider(bind=spring_slider_function, min=1, max=5, step=1, value=1, length=200, id="spring_slider", pos=scene.caption_anchor)
spring_slider_text = wtext(text=f"Number of Springs: {spring_slider.value}", pos=scene.caption_anchor)

def spring_mode_button_function(evt):
    spring_mode_button.is_series_mode = not spring_mode_button.is_series_mode
    spring_mode_button.text = "Series" if spring_mode_button.is_series_mode else "Parallel"
    change_springs()
 
scene.append_to_caption("     ")
spring_mode_button = button(bind=spring_mode_button_function, text="Series", pos=scene.caption_anchor, is_series_mode=True)
spring_mode_button.is_series_mode = False
# is_series_mode: True = series, False = parallel
    

block = box(pos=vec(4, 0, 0), length=1, height=1, width=1)
dt = 0.01

mass = 20
k = 1
vel = 0
block_x = block.pos.x
x_equilibrium = 2


max_springs = 5
init_spring_length = 2.5
spring_radius = 1
curve_thickness = 0.05
num_coils = 4.5
# initialize the series springs
series_springs_list = []
horizontal_spacing = 1 # this is constant
for i in range(max_springs):
    series_springs_list.append(
        helix(pos=vec(horizontal_spacing + i * (init_spring_length + horizontal_spacing), 0, 0), 
              axis=vec(init_spring_length, 0, 0), 
              coils=num_coils,
              radius=spring_radius, 
              color=color.red)  
    )
    
# initialize the lines between the springs and block
series_lines_list = []
for i in range(max_springs+1):
    left_point = vec(i*(horizontal_spacing+init_spring_length), 0, 0)
    right_point = left_point + vec(horizontal_spacing,0,0)
    out_point1 = left_point + vec(0, 0, -spring_radius)
    out_point2 = right_point + vec(0, 0, spring_radius)
    curve_points = [out_point1, left_point, right_point, out_point2]
    if i == 0:
        curve_points.pop(0)
    if i == max_springs:
        curve_points.pop()
    series_lines_list.append(
        curve(pos=curve_points,
              radius=curve_thickness,
              color=color.red)
    )

# initialize the parallel springs
#parallel_springs_list = []
#vertical_spacing = 3
#for i in range(max_springs):
#    parallel_springs_list.append(
#        helix(pos=vec(0, vertical_spacing * i, 0), axis=block.pos, color=color.red)
#    )

#presets dropdown
def presetselect(evt):
        console.log(evt)
        if evt.index < 1:
                pass
        elif evt.index is 1:
                #cliff
                cliffheightslider = slider( bind=cliffheightfunc, min=5, max=25 )
                wtext(text='height')
                def cliffheightfunc(evt):
                    console.log(evt)
                    cliffheight.height = evt.value
                    cliffheight.pos.y = -evt.value/2-.5
                    endofcliff.pos.y = -evt.value-.5
                cliff = box(pos=vec(7, -.5, 0), length=10, height=.1, width=1, color=color.white)
                cliffheight = box(pos=vec(12, -5.5, 0), length=.1, height=10, width=1, color=color.white)
                endofcliff = box(pos=vec(22, -10.5, 0), length=20, height=.1, width=1, color=color.white)
        elif evt.index is 2:
            #slope
            slopeslider = slider(min=(-pi/2), max=pi/2, value=pi/4, length=300, bind=slopefunc)
            wtext(text='angle')
            origin = vec(12, -0.5, 0)
            def slopefunc(evt):
                console.log(evt)
                direction = vec(cos(evt.value), sin(evt.value), 0) 
                slopeangle.axis = (direction * 20)                       
                slopeangle.pos = (origin + 0.5 * slopeangle.axis) 
                    
            slope = box(pos=vec(7, -.5, 0), length=10, height=.1, width=1, color=color.white)
            slopeangle = box(pos=vec(19, 6.5, 0), length=20, height=.1, width=1,axis=vec(1,1,0), color=color.white)
presetlist = ['Pick a preset :)','Cliff', 'Slope', 'Loop', 'Coaster']
menu(bind=presetselect, choices=presetlist)

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
    
    
    
# second while loop for projectile motion after block has been launched
while (True):
    rate(1/dt)
    pass
