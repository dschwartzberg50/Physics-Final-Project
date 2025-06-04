Web VPython 3.2

scene = canvas(width=600, height=500, title="Spring Oscillator!\n")
scene.camera.pos = vec(10, 0, 20)

# disables everything except for launch button
def start_button_function(evt):
    start_button.started = True
    start_button.disabled = True
    spring_slider.disabled = True
    initial_velocity_slider.disabled = True
    spring_mode_button.disabled = True
    # put other UI elements here later to be disabled
    
    launch_button.disabled = False
start_button = button(bind=start_button_function, text='Start', background=color.green, pos=scene.title_anchor, disabled=False, started=False)

def update_launch_button():
    global launch_button, block
    launch_button.disabled = not (block.vel > 0)
    
def launch_button_function(evt):
    if not (block.vel > 0): return
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
    
    global series_springs_list
    global parallel_springs_list
    springs_list = series_springs_list if spring_mode_button.is_series_mode else parallel_springs_list
    lines_list = series_lines_list if spring_mode_button.is_series_mode else parallel_lines_list
    
    # makes the first n springs visible
    
    # set everything invisible by default
    for spring in springs_list:
        spring.visible = False
    for series_line in lines_list:
        series_line.visible = False
        
    # set the first n springs to be visible
    for i in range(evt.value):
        springs_list[i].visible = True
    # note: the first curve should always be visible
    # set the first n curves to be visible after i=0
    for i in range(evt.value+1):
        lines_list[i].visible = True
        # make the last segment visible in case it was previously invisible
        this_curve = lines_list[i]
        this_curve.modify(this_curve.npoints-1, visible=True)
    
    # make the last segment of the last visible curve not visible
    last_curve = lines_list[evt.value]
    last_curve.modify(last_curve.npoints-1, visible=False)
        
    # set the position of the block
    global block, spring_length, horizontal_spacing
    total_length = horizontal_spacing + evt.value*(horizontal_spacing + spring_length)
    block.pos.x = total_length + block.length/2
    
    equilibrium_point.pos.x = block.pos.x

spring_slider = slider(bind=spring_slider_function, min=1, max=5, step=1, value=1, length=200, pos=scene.caption_anchor)
spring_slider_text = wtext(text=f"Number of Springs: {spring_slider.value}", pos=scene.caption_anchor)

box(pos=vec(0,0,0), height=10, width=0.1,length=0.1)

# future: need to made the spring layout and make everything visisble / invisible
def spring_mode_button_function(evt):
    spring_mode_button.is_series_mode = not spring_mode_button.is_series_mode
    spring_mode_button.text = "Series" if spring_mode_button.is_series_mode else "Parallel"
 
scene.append_to_caption("     ")
spring_mode_button = button(bind=spring_mode_button_function, text="Series", pos=scene.caption_anchor, is_series_mode=True)
spring_mode_button.is_series_mode = True
# is_series_mode: True = series, False = parallel

max_springs = 5
init_spring_length = 2.5
spring_radius = 1
curve_thickness = 0.05
num_coils = 3.5
# initialize the series springs
series_springs_list = []
horizontal_spacing = 0.8 # this is constant
spring_length = init_spring_length
for i in range(max_springs):
    series_springs_list.append(
        helix(pos=vec(horizontal_spacing + i * (init_spring_length + horizontal_spacing), 0, 0), 
              axis=vec(init_spring_length, 0, 0), 
              coils=num_coils,
              radius=spring_radius, 
              k=1,
              color=color.red
          )  
    )
    
def create_connecting_curve_points(i, d, l):
    r = spring_radius
    left_point = vec(i*(d+l), 0, 0)
    right_point = left_point + vec(d,0,0)
    out_point1 = left_point + vec(0, 0, -r)
    out_point2 = right_point + vec(0, 0, r)
    curve_points = [out_point1, left_point, right_point, out_point2]
    if i == 0:
        curve_points.pop(0)
    
    return curve_points
    
# initialize the lines between the springs and block
series_lines_list = []
for i in range(max_springs+1):
    curve_points = create_connecting_curve_points(i, horizontal_spacing, init_spring_length)
    series_lines_list.append(
        curve(pos=curve_points,
              radius=curve_thickness,
              color=color.red)
    )

parallel_springs_list = []
parallel_lines_list = []
# initialize the parallel springs
#parallel_springs_list = []
#vertical_spacing = 3
#for i in range(max_springs):
#    parallel_springs_list.append(
#        helix(pos=vec(0, vertical_spacing * i, 0), axis=block.pos, color=color.red)
#    )

# modify the springs based on the block's position
def modify_springs():
    global spring_mode_button, series_springs_list, parallel_springs_list, spring_slider, horizontal_spacing, spring_length
    is_series_mode = spring_mode_button.is_series_mode
    springs_list = series_springs_list if is_series_mode else parallel_springs_list
    n = spring_slider.value
    
    if is_series_mode:
        global series_lines_list
        d0 = horizontal_spacing
        l0 = spring_length
        
        d = (block.pos.x - block.length/2) / (n+1 + n * (l0/d0))
        l = l0/d0 * d
        
        for i, this_curve in enumerate(series_lines_list):
            new_points = create_connecting_curve_points(i, d, l)
            
            assert this_curve.npoints == len(new_points)
            for point_index in range(this_curve.npoints):
                this_curve.modify(point_index, pos=new_points[point_index], color=color.red, radius=curve_thickness)

        for i, spring in enumerate(springs_list):
            spring.length = l
            spring.pos.x = d + i * (l+d)
        
    else:
        pass

def calculate_equivalent_k(is_series_mode, springs_list, n):
    if is_series_mode:
        return 1 / sum(1/spring.k for spring in springs_list[:n])
    else:
        return sum(spring.k for spring in springs_list[:n])
        
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
            slopeslider = slider(min=(-pi/3), max=(pi/3), value=pi/4, length=300, bind=slopefunc)
            wtext(text='angle')
            origin = vec(12, -0.5, 0)
            def slopefunc(evt):
                console.log(evt)
                direction = vec(cos(evt.value), sin(evt.value), 0) 
                slopeangle.axis = (direction * 20)                       
                slopeangle.pos = (origin + 0.5 * slopeangle.axis) 
                    
            slope = box(pos=vec(7, -.5, 0), length=10, height=.1, width=1, color=color.white)
            slopeangle = box(pos=vec(19, 6.5, 0), length=20, height=.1, width=1,axis=vec(1,1,0), color=color.white)
        elif evt.index is 3:
            #loop
            loopslider = slider(min=(3), max=(10), value=6, length=300, bind=loopfunc)
            wtext(text='loop radius')
            loop = box(pos=vec(7, -.5, 0), length=10, height=.1, width=1, color=color.white)
            loopradius = helix(pos=vec(12, (3),-1), axis=vec(0,0,1), coils = 1, color=color.white, radius=4, thickness= 1)
            loopradius.rotate (axis = vec(0, 0, 1), angle = (pi/2), origin = vec(loopradius.pos+loopradius.axis/2))
            loop2 = box(pos=vec(17, -.5, -1), length=10, height=.1, width=1, color=color.white)
            def loopfunc(evt):
                console.log(evt)
                loopradius.radius= evt.value
                loopradius.pos= vec(12,evt.value-1,-1)
                
            slope = box(pos=vec(7, -.5, 0), length=10, height=.1, width=1, color=color.white)
            slopeangle = box(pos=vec(19, 6.5, 0), length=20, height=.1, width=1,axis=vec(1,1,0), color=color.white)
presetlist = ['Pick a preset :)','Cliff', 'Slope', 'Loop', 'Coaster']
menu(bind=presetselect, choices=presetlist)

# wip
"""
def initial_position_slider_function(evt):
    global block
    block.pos.x = evt.value
    initial_position_slider_Text.text = f"Initial Position: {block.pos.x}"
    modify_springs()

# min can't be 0 for the position
initial_position_slider = slider(bind=initial_position_slider_function, min=0.5, max=10, value=2, length=200, pos=scene.caption_anchor)
initial_position_slider_text = wtext(text=f"Initial Position: {initial_position_slider.value}", pos=scene.caption_anchor)
"""

def initial_velocity_slider_function(evt):
    global block
    block.vel = evt.value
    initial_velocity_slider_text.text = f"Initial Velocity: {evt.value}"
    
initial_velocity_slider = slider(bind=initial_velocity_slider_function, min=0, max=3, value=1, length=200, pos=scene.caption_anchor)
initial_velocity_slider_text = wtext(text=f"Initial Velocity: {initial_velocity_slider.value}", pos=scene.caption_anchor)

block = box(pos=vec(4, 0, 0), length=1, height=1, width=1, mass=20, vel=1)
dt = 0.01

equilibrium_point = sphere(pos=block.pos + vec(0,2,0), radius=0.5, color=color.green)

# setup
spring_slider_function(spring_slider)
initial_velocity_slider_function(initial_velocity_slider)

# assumed that: no sliders can be moved after the program has started
# initial while loop for spring-oscillatory motion    
while (True):
    rate(1/dt)
    
    update_launch_button()
    if (launch_button.launched): break
    if (not start_button.started): continue

    k = calculate_equivalent_k(
        spring_mode_button.is_series_mode, 
        series_springs_list if spring_mode_button.is_series_mode else parallel_springs_list,
        spring_slider.value
    ) 
    force = -k * (block.pos.x - equilibrium_point.pos.x)
    acc = force / block.mass
    block.vel += acc
    block.pos.x += block.vel
    
    modify_springs()
    
    
# second while loop for projectile motion after block has been launched
while (True):
    rate(1/dt)
    
    block.pos.x += block.vel
    pass
