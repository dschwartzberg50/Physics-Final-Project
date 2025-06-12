Web Vpython 3.2

def hex_to_color(color_string):
    color_string = color_string.lstrip("#")
    
    rgb_list = []
    for i in range(3):
        n = color_string[2*i:2*i + 2]
        rgb_list.append(int(n, 16) / 255)
    
    return vec(*rgb_list)
    
scene = canvas(width=600, height=700, align="left")
scene.camera.pos = vec(10, 0, 20)

left_margin = "   "
slider_length = 200

# start button
def start_button_function(evt):
    # disable all UI elements to control the intial conditions
    start_button.disabled = True
    spring_slider.disabled = True
    initial_velocity_slider.disabled = True
    spring_mode_button.disabled = True
    preset_menu.disabled = True
    
    # enable the user to press the launch button
    launch_button.disabled = False
scene.append_to_caption(left_margin)
start_button = button(bind=start_button_function, text='Start', background=color.green, pos=scene.caption_anchor)
start_button.disabled = False
start_button.started = False

# launch button
def launch_button_function(evt):
    launch_button.about_to_launch = True
    launch_button.disabled = True
scene.append_to_caption(" ")
launch_button = button(bind=launch_button_function, text='Launch', background=color.blue, pos=scene.caption_anchor)
launch_button.disabled = True
launch_button.launched = False
launch_button.about_to_launch = False

# reset button (TODO)
def reset_button_function(evt):
    # block.pos = INIT_BLOCK_POS
    
    pass
scene.append_to_caption(" ")
reset_button = button(bind=reset_button_function, text="Reset", background=color.yellow, pos=scene.caption_anchor)

scene.append_to_caption("\n")
scene.append_to_caption("\n")

# spring mode button (series/parallel)
def spring_mode_button_function(evt):
    spring_mode_button.is_series_mode = not spring_mode_button.is_series_mode
    spring_mode_button.text = "Series" if spring_mode_button.is_series_mode else "Parallel"
    if spring_mode_button.is_series_mode:
        spring_mode_button.text = "Series"
        spring_mode_button.background = color.orange
    else:
        spring_mode_button.text = "Parallel"
        spring_mode_button.background = hex_to_color("#34a1eb")

    # make everything invisible
    for spring in series_springs_list:
        spring.visible = False
    for spring in parallel_springs_list:
        spring.visible = False
    for series_line in series_lines_list:
        series_line.visible = False
    for c1, c2 in parallel_lines_list:
        c1.visible = False
        c2.visible = False
    
    # this makes the correct springs visible
    spring_slider_function(spring_slider)
scene.append_to_caption(left_margin)
spring_mode_button = button(bind=spring_mode_button_function, text="Series", pos=scene.caption_anchor)
spring_mode_button.is_series_mode = True

scene.append_to_caption("\n")

# spring slider (# of springs)
def spring_slider_function(evt):
    spring_slider_text.text = f"Number of Springs: {evt.value}"
    
    # choose the corresponding list of springs/curves
    springs_list = series_springs_list if spring_mode_button.is_series_mode else parallel_springs_list
    lines_list = series_lines_list if spring_mode_button.is_series_mode else parallel_lines_list
    
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
    v1 = evt.value if (spring_mode_button.is_series_mode) else 1
    spring_length = springs_list[0].length
    total_length = horizontal_spacing + v1*(horizontal_spacing + spring_length)
    block.pos.x = total_length + block.length/2
    
    v2 = evt.value if (not spring_mode_button.is_series_mode) else 1
    block.height = v2*(VERTICAL_SPACING + 2*SPRING_RADIUS)
    block.pos.y = (block.height - 2*SPRING_RADIUS) / 2
    
    # set the x-position of the equilibrium point (always the initial x-position of the block)
    equilibrium_point.pos = block.pos + vec(0, block.height/2 + equilibrium_point_height_above_block, 0)
    
    # calculate and set the maximum intiial velocity of the block so it doesn't go past x=0
    k = calculate_equivalent_k()
    block.max_initial_vel = sqrt(k/block.mass * (block.pos.x**2))
    initial_velocity_slider_function(initial_velocity_slider)
    
    # set the first n spring constant sliders to be on
    for i in range(len(spring_constants_sliders)):
        spring_constants_sliders[i].disabled = (not (i < evt.value))
scene.append_to_caption(left_margin)
spring_slider = slider(bind=spring_slider_function, min=1, max=5, step=1, value=1, length=slider_length, pos=scene.caption_anchor)
spring_slider_text = wtext(text=f"Number of Springs: {spring_slider.value}", pos=scene.caption_anchor)

# sliders for spring constants (k values)
def spring_constant_slider_function(evt):
    spring_constants_texts[evt.id].text = f"Spring #{(evt.id)+1}: k={evt.value}"
    
    global series_springs_list, parallel_springs_list
    springs_list = series_springs_list if spring_mode_button.is_series_mode else parallel_springs_list
    
    # adjust the color maybe ?!?! TODO
    pass
spring_constants_sliders = []
spring_constants_texts = []
for i in range(spring_slider.max):
    scene.append_to_caption("\n" + left_margin)
    
    spring_constants_sliders.append(
        slider(bind=spring_constant_slider_function, min=1, max=5, step=0.1, value=1, length=slider_length, pos=scene.caption_anchor)
    )
    spring_constants_sliders[i].disabled = True
    spring_constants_sliders[i].id = i
    
    spring_constants_texts.append(
        wtext(text=f"Spring #{i+1}: k={spring_constants_sliders[i].value}", pos=scene.caption_anchor)
    )
    
def calculate_equivalent_k():
    n = spring_slider.value
    if spring_mode_button.is_series_mode:
        return 1 / sum(1/spring_slider.value for spring_slider in spring_constants_sliders)
    else:
        return sum(spring_slider.value for spring_slider in spring_constants_sliders)

scene.append_to_caption("\n")

# creation of both spring lists

# constants
INIT_SPRING_LENGTH = 2.5
SPRING_RADIUS = 1
CURVE_THICKNESS = 0.05
NUM_COILS = 3.5 # must be 0.5 + n because half a coil looks good ! 
VERTICAL_SPACING = 0.8 # for parallel only
# non-constant
horizontal_spacing = 0.8

# returns a list of curve points to be used as the intermediate segments between springs (and the wall/block) in series mode
def create_series_curve_points(i, d, l):
    left_point = vec(i*(d+l), 0, 0)
    right_point = left_point + vec(d, 0, 0)
    out_point1 = left_point + vec(0, 0, -SPRING_RADIUS)
    out_point2 = right_point + vec(0, 0, SPRING_RADIUS)
    curve_points = [out_point1, left_point, right_point, out_point2]
    if i == 0:
        curve_points.pop(0)
    
    return curve_points

series_springs_list = []
for i in range(spring_slider.max):
    series_springs_list.append(
        helix(
            pos=vec(horizontal_spacing + i * (INIT_SPRING_LENGTH + horizontal_spacing), 0, 0), 
            axis=vec(INIT_SPRING_LENGTH, 0, 0), 
            coils=NUM_COILS,
            radius=SPRING_RADIUS, 
            color=color.red,
            visible=False
        )
    )
series_lines_list = []
for i in range(spring_slider.max+1):
    curve_points = create_series_curve_points(i, horizontal_spacing, INIT_SPRING_LENGTH)
    series_lines_list.append(
        curve(
            pos=curve_points,
            radius=CURVE_THICKNESS,
            color=color.red,
            visible=False
          )
    )
    
# returns a list of curve points to be used as the intermediate segments between each spring and the wall/block in parallel mode
def create_parallel_curve_points(i, h, d, l, right):
    curve_points = create_series_curve_points(1 if right else 0, horizontal_spacing, INIT_SPRING_LENGTH)
    if right:
        curve_points.pop()
    
    for j in range(len(curve_points)):
        curve_points[j] += vec(0, i * (2*SPRING_RADIUS + h), 0)
    return curve_points

parallel_springs_list = []
for i in range(spring_slider.max):
    parallel_springs_list.append(
        helix(
            pos=vec(horizontal_spacing, i * (2*SPRING_RADIUS + VERTICAL_SPACING), 0), 
            axis=vec(INIT_SPRING_LENGTH, 0, 0), 
            coils=NUM_COILS,
            radius=SPRING_RADIUS,
            color=color.red,
            visible=False
        )
    )
parallel_lines_list = []
for i in range(spring_slider.max):
    points1 = create_parallel_curve_points(i, VERTICAL_SPACING, horizontal_spacing, INIT_SPRING_LENGTH, False)
    c1 = curve(
        pos=points1,
        radius=CURVE_THICKNESS,
        color=color.red,
        visible=False
    )
    points2 = create_parallel_curve_points(i, VERTICAL_SPACING, horizontal_spacing, INIT_SPRING_LENGTH, True)
    c2 = curve(
        pos=points2,
        radius=CURVE_THICKNESS,
        color=color.red,
        visible=False
    )
    parallel_lines_list.append(
       (c1, c2) # tuple of both curves
    )
    
# modify the springs based on the block's position
def modify_springs():
    global horizontal_spacing
    springs_list = series_springs_list if spring_mode_button.is_series_mode else parallel_springs_list
    n = spring_slider.value
    
    d0 = horizontal_spacing
    l0 = springs_list[0].length
    
    if spring_mode_button.is_series_mode:
        global series_lines_list
        
        d = (block.pos.x - block.length/2) / (n+1 + n * (l0/d0))
        l = l0/d0 * d
        
        for i, this_curve in enumerate(series_lines_list):
            new_points = create_series_curve_points(i, d, l)
            
            assert this_curve.npoints == len(new_points)
            for point_index in range(this_curve.npoints):
                this_curve.modify(point_index, pos=new_points[point_index], color=color.red, radius=CURVE_THICKNESS)

        for i, spring in enumerate(springs_list):
            spring.length = l
            spring.pos.x = d + i * (l+d)
        
    else:
        # this might be a little broken
        global parallel_lines_list
        
        l = (block.pos.x - block.length/2) / (2*d0/l0 + 1)
        d = d0/l0 * l
        
        for i, (c1, c2) in enumerate(parallel_lines_list):
            points1 = create_parallel_curve_points(i, VERTICAL_SPACING, d, l, False)
            for point_index in range(c1.npoints):
                c1.modify(point_index, pos=points1[point_index], color=color.red, radius=CURVE_THICKNESS)
                
            points2 = create_parallel_curve_points(i, VERTICAL_SPACING, d, l, True)
            for point_index in range(c2.npoints):
                c2.modify(point_index, pos=points2[point_index], color=color.red, radius=CURVE_THICKNESS)

        for i, spring in enumerate(springs_list):
            spring.length = l
            spring.pos = vec(horizontal_spacing, i * (2*SPRING_RADIUS + VERTICAL_SPACING), 0)
            
    horizontal_spacing = d
    
#presets dropdown
scene.append_to_caption("     ")
def presetselect(evt):
        if evt.index < 1:
                pass
        elif evt.index == 1:
            cliffheight.visible = True
            endofcliff.visible = True
            slopeangle.visible = False
            loopradius.visible = False
            loop2.visible = False
            cliffheightslider.disabled = False
            loopslider.disabled = True
            slopeslider.disabled = True
        elif evt.index == 2:
            cliffheight.visible = False
            endofcliff.visible = False
            slopeangle.visible = True
            loopradius.visible = False
            loop2.visible = False
            cliffheightslider.disabled = True
            loopslider.disabled = True
            slopeslider.disabled = False
        elif evt.index == 3:
            cliffheightslider.disabled = True
            loopslider.disabled = False
            slopeslider.disabled = True
            cliffheight.visible = False
            endofcliff.visible = False
            slopeangle.visible = False
            loopradius.visible = True
            loop2.visible = True
            
                    
presetlist = ['Pick a preset :)','Cliff', 'Slope', 'Loop', 'Coaster']
preset_menu = menu(bind=presetselect, choices=presetlist)

#set up shapes
start = box(pos=vec(15, -1, 0), length=30, height=.1, width=1, color=color.white)
cliffheight = box(pos=vec(30, -16, 0), length=.1, height=30, width=1, color=color.white)
endofcliff = box(pos=vec(60, -31, 0), length=60, height=.1, width=1, color=color.white)
slopeangle = box(pos=vec(46, 15, 0), length=45, height=.1, width=1,axis=vec(1,1,0), color=color.white)
loopradius = helix(pos=vec(30, (4.5),-1), axis=vec(0,0,1), coils = 1, color=color.white, radius=6, thickness= 1)
loopradius.rotate (axis = vec(0, 0, 1), angle = (pi/2), origin = vec(loopradius.pos+loopradius.axis/2))
loop2 = box(pos=vec(45, -1, -1), length=30, height=.1, width=1, color=color.white)
#cliff
def cliffheightfunc(evt):
    cliffheight.height = evt.value
    cliffheight.pos.y = -evt.value/2-1
    endofcliff.pos.y = -evt.value-1
#slope                    
origin = vec(30, -1, 0)
def slopefunc(evt):
    direction = vec(cos(evt.value), sin(evt.value), 0) 
    slopeangle.axis = (direction * 45)                       
    slopeangle.pos = (origin + 0.5 * slopeangle.axis) 
#loop
def loopfunc(evt):
                loopradius.radius= evt.value
                loopradius.pos= vec(31,evt.value-1,-1)
#sliders
scene.append_to_caption('\n')
cliffheightslider = slider( bind=cliffheightfunc, min=5, max=50, value = 30, length = 500, pos=scene.caption_anchor) 
wtext(text='height')
scene.append_to_caption('\n')
slopeslider = slider(min=(-pi/3), max=(pi/3), value=pi/4, length=500, bind=slopefunc, pos=scene.caption_anchor)
wtext(text='angle')
scene.append_to_caption('\n')
loopslider = slider(min=(6), max=(20), value=10, length=500, bind=loopfunc, pos=scene.caption_anchor)
wtext(text='loop radius')
cliffheight.visible = False
endofcliff.visible = False
slopeangle.visible = False
loopradius.visible = False
loop2.visible = False
cliffheightslider.disabled = True
loopslider.disabled = True
slopeslider.disabled = True

def initial_velocity_slider_function(evt):
    global block
    
    block.vel = block.max_initial_vel * initial_velocity_slider.value # slider ranges from 0-1, acting as a percentage
    initial_velocity_slider_text.text = f"Initial Velocity: {evt.value}"
    
initial_velocity_slider = slider(bind=initial_velocity_slider_function, min=0, max=0.95, step=0.01, value=0.5, length=slider_length, pos=scene.caption_anchor)
initial_velocity_slider_text = wtext(text=f"Initial Velocity: {initial_velocity_slider.value}", pos=scene.caption_anchor)

# need a mass slider
wall = box(pos=vec(0,12.5/2,0), height=15, width=5,length=0.1)
block = box(pos=vec(4, 0, 0), length=1, height=2*SPRING_RADIUS, width=1, mass=20, vel=-1, max_initial_vel=-1)
dt = 0.01
t = 0

equilibrium_point_height_above_block = 1
equilibrium_point = sphere(pos=block.pos + vec(0, equilibrium_point_height_above_block, 0), radius=0.5, color=color.green)

# graphs setup
time_interval = 1/2 # <- set this value 
max_t_points = int(time_interval / dt)

energy_graph = graph(width=300, height=350, title="Energy vs Time", xtitle="Time", ytitle="Energy", align="right")
K_curve = gcurve(graph=energy_graph, label="Kinetic Energy", color=color.green)
K_data = []
U_curve = gcurve(graph=energy_graph, label="Potential Energy", color=color.red)
U_data = []

pos_graph = graph(width=300, height=350, title="Position vs Time", xtitle="Time", ytitle="Position", align="right")
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
    
    if (launch_button.about_to_launch and block.vel > 0 and block.pos.x >= equilibrium_point.pos.x): break
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
    
    # update the entire spring setup
    modify_springs()
    
launch_button.disabled = True
    
# second while loop for projectile motion after block has been launched
while (True):
    rate(1/dt)
    
    block.pos.x += block.vel
    pass
