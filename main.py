Web Vpython 3.2

scene = canvas(width=600, height=500, title="Spring Oscillator!\n")
scene.camera.pos = vec(10, 0, 20)

# disables everything except for launch button
def start_button_function(evt):
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
    if spring_mode_button.is_series_mode:
        for series_line in lines_list:
            series_line.visible = False
    else:
        for c1, c2 in lines_list:
            c1.visible = False
            c2.visible = False
        
    # set the first n springs to be visible
    for i in range(evt.value):
        springs_list[i].visible = True
    
    if spring_mode_button.is_series_mode: # series only stuff
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
    else: # parallel only stuff
        for i in range(evt.value):
            c1, c2 = lines_list[i] # tuple of curves
            c1.visible = True
            c2.visible = True
    
    # set the new attributes of the block
    global block, spring_length, horizontal_spacing, vertical_spacing, spring_radius
    v1 = evt.value if (spring_mode_button.is_series_mode) else 1
    total_length = horizontal_spacing + v1*(horizontal_spacing + spring_length)
    block.pos.x = total_length + block.length/2
    
    v2 = evt.value if (not spring_mode_button.is_series_mode) else 1
    block.height = v2*(vertical_spacing + 2*spring_radius)
    block.pos.y = (block.height - 2*spring_radius) / 2
    
    # set the x-position of the equilibrium point (always the initial x-position of the block)
    global equilibrium_point_height_above_block
    equilibrium_point.pos = block.pos + vec(0, block.height/2 + equilibrium_point_height_above_block, 0)
    
    # calculate and set the maximum intiial velocity of the block so it doesn't go past x=0
    k = calculate_equivalent_k()
    block.max_initial_vel = sqrt(k/block.mass * (block.pos.x**2))
    initial_velocity_slider_function(initial_velocity_slider)

spring_slider = slider(bind=spring_slider_function, min=1, max=5, step=1, value=1, length=200, pos=scene.caption_anchor)
spring_slider_text = wtext(text=f"Number of Springs: {spring_slider.value}", pos=scene.caption_anchor)

def spring_mode_button_function(evt):
    spring_mode_button.is_series_mode = not spring_mode_button.is_series_mode
    spring_mode_button.text = "Series" if spring_mode_button.is_series_mode else "Parallel"
    
    # make everything invisible
    global series_springs_list, parallel_springs_list, series_lines_list, parallel_lines_list
    for spring in series_springs_list:
        spring.visible = False
    for spring in parallel_springs_list:
        spring.visible = False
    for series_line in series_lines_list:
        series_line.visible = False
    for c1, c2 in parallel_lines_list:
        c1.visible = False
        c2.visible = False
    spring_slider_function(spring_slider)
 
scene.append_to_caption("     ")
spring_mode_button = button(bind=spring_mode_button_function, text="Series", pos=scene.caption_anchor)
spring_mode_button.is_series_mode = True
# is_series_mode: True = series, False = parallel

# make the spring visuals 

max_springs = 5
spring_length = 2.5
spring_radius = 1
curve_thickness = 0.05
num_coils = 3.5 # must be 0.5 + n because half a coil looks good ! 
horizontal_spacing = 0.8 
vertical_spacing = 0.8 # for parallel only

def create_series_curve_points(i, d, l):
    r = spring_radius
    left_point = vec(i*(d+l), 0, 0)
    right_point = left_point + vec(d,0,0)
    out_point1 = left_point + vec(0, 0, -r)
    out_point2 = right_point + vec(0, 0, r)
    curve_points = [out_point1, left_point, right_point, out_point2]
    if i == 0:
        curve_points.pop(0)
    
    return curve_points

# initialize the series springs
series_springs_list = []
for i in range(max_springs):
    series_springs_list.append(
        helix(pos=vec(horizontal_spacing + i * (spring_length + horizontal_spacing), 0, 0), 
              axis=vec(spring_length, 0, 0), 
              coils=num_coils,
              radius=spring_radius, 
              k=1,
              color=color.red,
              visible=False
          )  
    )    
series_lines_list = []
for i in range(max_springs+1):
    curve_points = create_series_curve_points(i, horizontal_spacing, spring_length)
    series_lines_list.append(
        curve(pos=curve_points,
              radius=curve_thickness,
              color=color.red,
              visible=False
          )
    )
    
def create_parallel_curve_points(i, h, d, l, right):
    curve_points = create_series_curve_points(1 if right else 0, horizontal_spacing, spring_length)
    if right:
        curve_points.pop()
    
    r = spring_radius
    for j in range(len(curve_points)):
        curve_points[j] += vec(0, i * (2*r + h), 0)
    return curve_points

# initialize the parallel springs
parallel_springs_list = []
for i in range(max_springs):
    parallel_springs_list.append(
        helix(pos=vec(horizontal_spacing, i * (2*spring_radius + vertical_spacing), 0), 
              axis=vec(spring_length, 0, 0), 
              coils=num_coils,
              radius=spring_radius, 
              k=1,
              color=color.red,
              visible=False
          )  
    )  
parallel_lines_list = []
for i in range(max_springs):
    points1 = create_parallel_curve_points(i, vertical_spacing, horizontal_spacing, spring_length, False)
    c1 = curve(
        pos=points1,
        radius=curve_thickness,
        color=color.red,
        visible=False
    )
    points2 = create_parallel_curve_points(i, vertical_spacing, horizontal_spacing, spring_length, True)
    c2 = curve(
        pos=points2,
        radius=curve_thickness,
        color=color.red,
        visible=False
    )
    parallel_lines_list.append(
       (c1, c2) # tuple of both curves
    )

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
            new_points = create_series_curve_points(i, d, l)
            
            assert this_curve.npoints == len(new_points)
            for point_index in range(this_curve.npoints):
                this_curve.modify(point_index, pos=new_points[point_index], color=color.red, radius=curve_thickness)

        for i, spring in enumerate(springs_list):
            spring.length = l
            spring.pos.x = d + i * (l+d)
        
        spring_length = l
        horizontal_spacing = d
        
    else:
        pass

def calculate_equivalent_k():
    global series_springs_list, parallel_springs_list, spring_slider
    springs_list = series_springs_list if spring_mode_button.is_series_mode else parallel_springs_list
    n = spring_slider.value
    if spring_mode_button.is_series_mode:
        return 1 / sum(1/spring.k for spring in springs_list[:n])
    else:
        return sum(spring.k for spring in springs_list[:n])
        
#presets dropdown
def presetselect(evt):
        console.log(evt)
        if evt.index < 1:
                pass
        elif evt.index == 1:
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
        elif evt.index == 2:
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
    
    block.vel = block.max_initial_vel * initial_velocity_slider.value # slider ranges from 0-1, acting as a percentage
    initial_velocity_slider_text.text = f"Initial Velocity: {evt.value}"
    
initial_velocity_slider = slider(bind=initial_velocity_slider_function, min=0, max=0.95, step=0.01, value=0.5, length=200, pos=scene.caption_anchor)
initial_velocity_slider_text = wtext(text=f"Initial Velocity: {initial_velocity_slider.value}", pos=scene.caption_anchor)

# need a mass slider
wall = box(pos=vec(0,0,0), height=10, width=5,length=0.1)
block = box(pos=vec(4, 0, 0), length=1, height=2*spring_radius, width=1, mass=20, vel=-1, max_initial_vel=-1)
dt = 0.01
t = 0

equilibrium_point_height_above_block = 1
equilibrium_point = sphere(pos=block.pos + vec(0, equilibrium_point_height_above_block, 0), radius=0.5, color=color.green)

# graphs setup
time_interval = 1/2 # <- set this value 
max_t_points = int(time_interval / dt)

energy_graph = graph(width=300, height=350, title="Energy vs Time", xtitle="Time", ytitle="Energy")
K_curve = gcurve(graph=energy_graph, label="Kinetic Energy", color=color.green)
K_data = []
U_curve = gcurve(graph=energy_graph, label="Potential Energy", color=color.red)
U_data = []

pos_graph = graph(width=300, height=350, title="Position vs Time", xtitle="Time", ytitle="Position")
pos_curve = gcurve(graph=pos_graph, label="Position", color=color.blue)
pos_data = []

# UI elements setup
spring_slider_function(spring_slider)
initial_velocity_slider_function(initial_velocity_slider)
spring_slider.visible = False

# assumed that: no sliders can be moved after the program has started
# initial while loop for spring-oscillatory motion    
while (True):
    rate(1/dt)
    
    update_launch_button()
    if (launch_button.launched): break
    if (not start_button.disabled): continue
        
    # these are used for multiple things, calculate them early
    k = calculate_equivalent_k()
    delta_x = block.pos.x - equilibrium_point.pos.x

    # update graphs
    # kinetic energy 
    if not (len(K_data) < max_t_points):
        K_data.pop(0)
    K_data.append( (t, 1/2 * block.mass * (block.vel**2)) )
    K_curve.data = K_data
    
    # potential energy
    if not (len(U_data) < max_t_points):
        U_data.pop(0)
    U_data.append( (t, 1/2 * k * delta_x**2) )
    U_curve.data = U_data
    
    # position
    if not (len(pos_data) < max_t_points):
        pos_data.pop(0)
    pos_data.append( (t, delta_x))
    pos_curve.data = pos_data
    
    t += dt
    
    # euler's method
    force = -k * delta_x
    acc = force / block.mass
    block.vel += acc
    block.pos.x += block.vel
    
    modify_springs()
    
# second while loop for projectile motion after block has been launched
while (True):
    rate(1/dt)
    
    block.pos.x += block.vel
    pass
