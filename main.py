Web Vpython 3.2

def hex_to_color(color_string):
    color_string = color_string.lstrip("#")
    
    rgb_list = []
    for i in range(3):
        n = color_string[2*i:2*i + 2]
        rgb_list.append(int(n, 16) / 255)
    
    return vec(*rgb_list)
    
scene = canvas(width=600, height=660, align="left")
scene.camera.pos = vec(20, -5, 45)
# TODO: adjust initial camera angle a bit
# maybe make the camera follow block2

left_margin = "  "
slider_length = 200

# start button
def start_button_function(evt):
    start_button.disabled = True
    spring_mode_button.disabled = True
    spring_slider.disabled = True
    for spring_constant_slider in spring_constants_sliders:
        spring_constant_slider.disabled = True
    mass_slider.disabled = True
    initial_velocity_slider.disabled = True
    friction_slider.disabled = True
    preset_menu.disabled = True
    cliffheightslider.disabled = True
    slopeslider.disabled = True
    loopslider.disabled = True
    
    # only UI element that gets enabled after start
    launch_button.disabled = False
scene.append_to_caption(left_margin)
start_button = button(bind=start_button_function, text="Start", background=color.green, pos=scene.caption_anchor)

# launch button
def launch_button_function(evt):
    launch_button.about_to_launch = True
    launch_button.disabled = True
scene.append_to_caption(" ")
launch_button = button(bind=launch_button_function, text="Launch", background=color.blue, pos=scene.caption_anchor)
launch_button.about_to_launch = False
launch_button.launched = False

# TODO: reset button doesn't work if you press start and then launch
# TODO: reset button doesn't work after launching and then reset

# reset button; also used to initialize all sliders, buttons, and objects
def reset_button_function(evt):
    start_button.disabled = False
    
    launch_button.disabled = True
    launch_button.about_to_launch = False
    launch_button.launched = False
    
    spring_mode_button.disabled = False
    spring_mode_button.is_series_mode = False # this is swapped once the function is called
    spring_mode_button_function(spring_mode_button)
    
    spring_slider.disabled = False
    spring_slider.value = 1
    spring_slider_function(spring_slider)
    
    for spring_constants_slider in spring_constants_sliders:
        spring_constants_slider.value = 1
        spring_constant_slider_function(spring_constants_slider)

    mass_slider.disabled = False
    mass_slider.value = 5
    mass_slider_function(mass_slider)
    
    initial_velocity_slider.disabled = False
    initial_velocity_slider.value = 0.5
    initial_velocity_slider_function(initial_velocity_slider)
    
    friction_slider.disabled = False
    friction_slider.value = 0
    friction_slider_function(friction_slider)
    
    horizontal_spacing = INIT_HORIZONTAL_SPACING
    
    # TODO: this breaks on reset for some reason
    for i, series_spring in enumerate(series_springs_list):
        series_spring.pos = vec(horizontal_spacing + i * (INIT_SPRING_LENGTH + horizontal_spacing), 0, 0)
        series_spring.axis = vec(INIT_SPRING_LENGTH, 0, 0)

    for i, this_curve in enumerate(series_lines_list):
        curve_points = create_series_curve_points(i, horizontal_spacing, INIT_SPRING_LENGTH)
        for point_index in range(this_curve.npoints):
            this_curve.modify(point_index, pos=curve_points[point_index], color=color.red, radius=CURVE_THICKNESS)
    
    for i, parallel_spring in enumerate(parallel_springs_list):
        parallel_spring.pos = vec(horizontal_spacing, i * (2*SPRING_RADIUS + VERTICAL_SPACING), 0)
        series_spring.axis = vec(INIT_SPRING_LENGTH, 0, 0)
    
    for i, (c1, c2) in enumerate(parallel_lines_list):
        points1 = create_parallel_curve_points(i, VERTICAL_SPACING, horizontal_spacing, INIT_SPRING_LENGTH, False)
        for point_index in range(c1.npoints):
            c1.modify(point_index, pos=points1[point_index], color=color.red, radius=CURVE_THICKNESS)
        points2 = create_parallel_curve_points(i, VERTICAL_SPACING, horizontal_spacing, INIT_SPRING_LENGTH, True)
        for point_index in range(c2.npoints):
            c2.modify(point_index, pos=points2[point_index], color=color.red, radius=CURVE_THICKNESS)
        
    preset_menu.disabled = False
    preset_menu.index = 0
    preset_select(preset_menu)
    
    cliffheightslider.value = 30
    cliffheightfunc(cliffheightslider)
    
    slopeslider.value = pi/4
    slopefunc(slopeslider)
    
    loopslider.value = 10
    loopfunc(loopslider)
    
    set_visisble_springs()
    set_block_attributes()
    set_equilibrium_position()
    set_max_displacement_arrow()
    
    block2.up = vec(0, 1, 0)
    block2.pos.y = -(VERTICAL_SPACING + 2*SPRING_RADIUS)/2 + block2.height
    block2.vel = vec(0, 0, 0)
    block2.fell = False
    
    global energy_graph
    energy_graph.delete()
    energy_graph = graph(width=300, height=350, title="Energy vs Time", xtitle="Time", ytitle="Energy", align="left")
    
    global K_curve
    K_curve.delete()
    K_curve = gcurve(graph=energy_graph, label="Kinetic Energy", color=color.green)
    K_data = []
    
    global U_curve
    U_curve.delete()
    U_curve = gcurve(graph=energy_graph, label="Potential Energy", color=color.red)
    U_data = []
    
    global pos_graph
    pos_graph.delete()
    pos_graph = graph(width=300, height=350, title="Position vs Time", xtitle="Time", ytitle="Position", align="left")
    
    global pos_curve
    pos_curve.delete()
    pos_curve = gcurve(graph=pos_graph, label="Position", color=color.blue)
    pos_data = []
    
    global t
    t = 0
    
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

    spring_slider_function(spring_slider)
scene.append_to_caption(left_margin)
spring_mode_button = button(bind=spring_mode_button_function, text="Series", pos=scene.caption_anchor)
spring_mode_button.is_series_mode = True

scene.append_to_caption("\n")

# TODO: adjust the parameters of all the sliders

# spring slider (# of springs)
def spring_slider_function(evt):
    spring_slider_text.text = f"Number of Springs: {evt.value:.0f}"
        
    set_visisble_springs()
    
    set_block_attributes()
    
    set_equilibrium_position()
    
    set_max_displacement_arrow()
    
    initial_velocity_slider_function(initial_velocity_slider)
    
    # set the first n spring constant sliders to be on
    for i in range(len(spring_constants_sliders)):
        spring_constants_sliders[i].disabled = (not (i < evt.value))
spring_slider = slider(bind=spring_slider_function, min=1, max=5, step=1, length=slider_length, pos=scene.caption_anchor)
spring_slider_text = wtext(text="", pos=scene.caption_anchor)

# sliders for spring constants (k values)
def spring_constant_slider_function(evt):
    spring_constants_texts[evt.id].text = f"Spring #{(evt.id)+1}: k={evt.value:.1f}"
    
    # adjust the color maybe ?!?! TODO
    pass
spring_constants_sliders = []
spring_constants_texts = []
for i in range(spring_slider.max):
    scene.append_to_caption("\n")
    
    spring_constants_sliders.append(
        slider(bind=spring_constant_slider_function, min=1, max=5, step=0.1, value=1, length=slider_length, pos=scene.caption_anchor)
    )
    spring_constants_sliders[i].disabled = True
    spring_constants_sliders[i].id = i
    
    spring_constants_texts.append(
        wtext(text="", pos=scene.caption_anchor)
    )
    
def calculate_equivalent_k():
    n = spring_slider.value
    if spring_mode_button.is_series_mode:
        return 1 / sum(1/spring_slider.value for spring_slider in spring_constants_sliders)
    else:
        return sum(spring_slider.value for spring_slider in spring_constants_sliders)

def calculate_maximum_displacement():
    k = calculate_equivalent_k()
    return sqrt(mass_slider.value / k * (block.vel**2))
    
def calculate_maximum_initial_velocity():
    k = calculate_equivalent_k()
    max_displacement = equilibrium_point.pos.x - 1 # arbitrary max displacement
    return sqrt(k/mass_slider.value * max_displacement**2)
    
def calculate_single_spring_length():
    springs_list = get_springs_list()
    return springs_list[0].length

def calculate_total_spring_length():
    n = spring_slider.value if spring_mode_button.is_series_mode else 1
    spring_length = calculate_single_spring_length()
    return horizontal_spacing + n*(horizontal_spacing + spring_length)
    
scene.append_to_caption("\n")
scene.append_to_caption("\n")

# mass of block slider
def mass_slider_function(evt):
    mass_slider_text.text = f"Mass: {mass_slider.value:.0f}"
mass_slider = slider(bind=mass_slider_function, min=5, max=20, step=1, length=slider_length, pos=scene.caption_anchor)
mass_slider_text = wtext(text="", pos=scene.caption_anchor)

scene.append_to_caption("\n")

# initial velocity slider
def initial_velocity_slider_function(evt):
    block.vel = calculate_maximum_initial_velocity() * initial_velocity_slider.value
    initial_velocity_slider_text.text = f"Initial Velocity: {block.vel:.2f}"    
        
    set_max_displacement_arrow()
initial_velocity_slider = slider(bind=initial_velocity_slider_function, min=0, max=1, step=0.01, length=slider_length, pos=scene.caption_anchor)
initial_velocity_slider_text = wtext(text=f"", pos=scene.caption_anchor)

scene.append_to_caption("\n")

# coefficient of friction slider
def friction_slider_function(evt):
    friction_slider_text.text = f"Coefficient of Friction: {evt.value:.2f}"
friction_slider = slider(bind=friction_slider_function, min=0, max=0.9, step=0.01, length=slider_length, pos=scene.caption_anchor)
friction_slider_text = wtext(text=f"", pos=scene.caption_anchor)

scene.append_to_caption("\n")
scene.append_to_caption("\n")

# creation of both spring lists

# constants
INIT_SPRING_LENGTH = 2.5
SPRING_RADIUS = 1
CURVE_THICKNESS = 0.05
NUM_COILS = 3.5 # must be 0.5 + n because half a coil looks good ! 
VERTICAL_SPACING = 0.8 # for parallel only
# non-constant
INIT_HORIZONTAL_SPACING = 0.8
horizontal_spacing = INIT_HORIZONTAL_SPACING

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
    
def get_springs_list():
    return series_springs_list if spring_mode_button.is_series_mode else parallel_springs_list

def get_lines_list():
    return series_lines_list if spring_mode_button.is_series_mode else parallel_lines_list
    
# sets the visibility of each spring/curve
# does not change the attributes of any of the springs
def set_visisble_springs():
    # set everything invisible by default
    for spring in series_springs_list:
        spring.visible = False
    for spring in parallel_springs_list:
        spring.visible = False
    for series_line in series_lines_list:
        series_line.visible = False
    for c1, c2 in parallel_lines_list:
        c1.visible = False
        c2.visible = False
    
    springs_list = get_springs_list()
    lines_list = get_lines_list()
        
    # set the first n springs to be visible
    for i in range(spring_slider.value):
        springs_list[i].visible = True
    
    if spring_mode_button.is_series_mode: # series only stuff
        # note: the first curve should always be visible
        # set the first n curves to be visible after i=0
        for i in range(spring_slider.value+1):
            lines_list[i].visible = True
            # make the last segment visible in case it was previously invisible
            this_curve = lines_list[i]
            this_curve.modify(this_curve.npoints-1, visible=True)
        
        # make the last segment of the last visible curve not visible
        last_curve = lines_list[spring_slider.value]
        last_curve.modify(last_curve.npoints-1, visible=False)
    else: # parallel only stuff
        for i in range(spring_slider.value):
            c1, c2 = lines_list[i] # tuple of curves
            c1.visible = True
            c2.visible = True
    
# set both blocks' position to be in the correct spots for the given spring mode and amount of springs
# also sets the correct height for block 1 in parallel mode
def set_block_attributes():
    # block 1: x
    total_length = calculate_total_spring_length()
    block.pos.x = total_length + block.length/2
    
    # block 1: height
    n = spring_slider.value if (not spring_mode_button.is_series_mode) else 1
    block.height = n*(VERTICAL_SPACING + 2*SPRING_RADIUS)
    
    # block 1: y
    block.pos.y = (block.height - 2*SPRING_RADIUS) / 2
    
    # block 2: x
    A = calculate_maximum_displacement()
    block2.pos.x = block.pos.x + (A + RIGHT_DISTANCE)
    
def set_equilibrium_position():
    equilibrium_point.pos = block.pos + vec(0, block.height/2 + HEIGHT_ABOVE_BLOCK, 0)
    
def set_max_displacement_arrow():
    max_displacement_arrow.pos = equilibrium_point.pos
    max_displacement_arrow.axis = vec(calculate_maximum_displacement(), 0, 0)

# modify the springs based on the block's position
def modify_springs():
    global horizontal_spacing
    springs_list = get_springs_list()
    n = spring_slider.value
    
    d0 = horizontal_spacing
    l0 = springs_list[0].length
    
    if spring_mode_button.is_series_mode:
        global series_lines_list
        
        d = (block.pos.x - block.length/2) / (n+1 + n * (l0/d0))
        l = l0/d0 * d
        
        for i, this_curve in enumerate(series_lines_list):
            new_points = create_series_curve_points(i, d, l)
            
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

# menu for scenarios
preset_list = ["Cliff", "Slope", "Loop", "Coaster"]
def preset_select(evt):
    # make everything invisible / disabled
    cliffheight.visible = False
    endofcliff.visible = False
    slopeangle.visible = False
    loopradius.visible = False
    loop2.visible = False
    cliffheightslider.disabled = True
    loopslider.disabled = True
    slopeslider.disabled = True
    
    if evt.index == 0:
        cliffheight.visible = True
        endofcliff.visible = True
        cliffheightslider.disabled = False
    elif evt.index == 1:
        slopeangle.visible = True
        slopeslider.disabled = False
    elif evt.index == 2:
        loopslider.disabled = False
        loopradius.visible = True
        loop2.visible = True
scene.append_to_caption(left_margin)
preset_menu = menu(bind=preset_select, choices=preset_list)

scene.append_to_caption("\n")

# initialize the objects for the scenarios
ground = box(pos=vec(15, -1, 0), length=30, height=.1, width=1, color=color.white)
cliffheight = box(pos=vec(30, -16, 0), length=.1, height=30, width=1, color=color.white)
endofcliff = box(pos=vec(60, -31, 0), length=60, height=.1, width=1, color=color.white)
slopeangle = box(pos=vec(46, 15, 0), length=45, height=.1, width=1,axis=vec(1,1,0), color=color.white)
loopradius = helix(pos=vec(30, (4.5),-1), axis=vec(0,0,1), coils = 1, color=color.white, radius=6, thickness= 1)
loopradius.rotate(axis=vec(0, 0, 1), angle=(pi/2), origin=vec(loopradius.pos+loopradius.axis/2))
loop2 = box(pos=vec(45, -1, -1), length=30, height=.1, width=1, color=color.white)

# cliff height slider
def cliffheightfunc(evt):
    cliff_height_slider_text.text = f"Height: {evt.value:.0f}"
    
    cliffheight.height = evt.value
    cliffheight.pos.y = -evt.value/2-1
    endofcliff.pos.y = -evt.value-1
cliffheightslider = slider(bind=cliffheightfunc, min=5, max=50, step=1, length=slider_length, pos=scene.caption_anchor) 
cliff_height_slider_text = wtext(text=f"", pos=scene.caption_anchor)

scene.append_to_caption("\n")

# slope angle slider
def slopefunc(evt):
    slope_angle_slider_text.text = f"Angle (degrees): {degrees(evt.value):.0f}"
    direction = vec(cos(evt.value), sin(evt.value), 0) 
    slopeangle.axis = (direction * 90)    

    origin = vec(30, -1, 0)       
    slopeangle.pos = (origin + 0.5 * slopeangle.axis) 
slopeslider = slider(bind=slopefunc, min=(-pi/3), max=(pi/3), length=slider_length, pos=scene.caption_anchor)
slope_angle_slider_text = wtext(text="", pos=scene.caption_anchor)

scene.append_to_caption("\n")

# radius of loop slider
def loopfunc(evt):
    loop_radius_slider_text.text = f"Radius: {evt.value:.0f}"
    loopradius.radius= evt.value
    loopradius.pos= vec(31,evt.value-1,-1)
loopslider = slider(bind=loopfunc, min=6, max=20, step=1, length=slider_length, pos=scene.caption_anchor)
loop_radius_slider_text = wtext(text="", pos=scene.caption_anchor)

wall = box(pos=vec(0,12.5/2,0), height=15, width=5, length=0.1)
block = box(length=1, height=2*SPRING_RADIUS, width=1)
block.vel = 0

HEIGHT_ABOVE_BLOCK = 1
equilibrium_point = sphere(radius=0.5, color=color.green)

max_displacement_arrow = arrow(round=True, shaftwidth=0.3, color=hex_to_color("#fc037b"))

RIGHT_DISTANCE = 2
block2 = box(size=(SPRING_RADIUS)*vec(1, 1, 1))
block2.vel = vec(0, 0, 0)
block2.fell = False

scene.camera.follow(block2)

dt = 1
t = 0

GRAVITY = 0.1

# graphs setup
MAX_T_POINTS = 100

energy_graph = graph()
K_curve = gcurve()
K_data = []
U_curve = gcurve()
U_data = []

pos_graph = graph()
pos_curve = gcurve()
pos_data = []

# initializes everything to have its intended intial value and/or state
reset_button_function(reset_button)

def get_state():
    if not (start_button.disabled): return 0
    if not (launch_button.disabled): return 1
    if launch_button.about_to_launch: return 2
    if launch_button.launched:
        if not (block2.vel.x > 0): return 3
        else: return 4
        
    return None
    
def run1(state):
    global t
    k = calculate_equivalent_k()
    delta_x = block.pos.x - equilibrium_point.pos.x
    
    # update graphs
    # kinetic energy 
    if not (len(K_data) < MAX_T_POINTS):
        K_data.pop(0)
    K_data.append( (t, 1/2 * mass_slider.value * (block.vel**2)) )
    K_curve.data = K_data
    
    # potential energy
    if not (len(U_data) < MAX_T_POINTS):
        U_data.pop(0)
    U_data.append( (t, 1/2 * k * delta_x**2) )
    U_curve.data = U_data
    
    # position
    if not (len(pos_data) < MAX_T_POINTS):
        pos_data.pop(0)
    pos_data.append( (t, delta_x))
    pos_curve.data = pos_data
    
    # euler's method
    force = -k * delta_x
    acc = force / mass_slider.value
    block.vel += acc * dt
    block.pos.x += block.vel * dt
    
    # update the entire spring setup
    modify_springs()
    
    if state == 2:
        launch_button.disabled = True
        if launch_button.about_to_launch and block.vel > 0 and block.pos.x >= equilibrium_point.pos.x:
            launch_button.about_to_launch = False
            launch_button.launched = True
            
def run2():
    # simulate collision
    if block.pos.x + block.length/2 >= block2.pos.x - block2.length/2:
        block2.vel.x = block.vel
        block.vel = 0
    
    block.pos.x += block.vel * dt
    block2.pos.x += block2.vel.x * dt

# TODO: implement friction
def run3():
    if preset_menu.index == 0: # cliff
        # past the cliff's ledge
        if not block2.fell and block2.pos.x - block2.length/2 > ground.length:
            acc = -GRAVITY
            block2.vel.y += acc * dt
        
        print(block2.fell)
        if not block2.fell and block2.pos.y <= endofcliff.pos.y:
            block2.pos.y = endofcliff.pos.y + block2.height/2
            block2.vel.y = 0
            block2.fell = True
        
        block2.pos += block2.vel * dt
    elif preset_menu.index == 1: # slope
        # # past the horizontal runway
        # vel = block2.vel
        # if block2.pos.x - block2.length/2 > ground.length:
        #     block2.up = slopeangle.up
        # 
        #     vel = rotate(vel, angle=slopeslider.value, axis=vec(0, 0, 1))
        # block2.pos += vel * dt
        block.pos.x += block.vel  # pre-slope horizontal motion
    
        if block.pos.x > 60:
            theta = slopeslider.value
            a = -gravity * sin(theta)*.01  # acceleration along the slope
            block.vel += a * dt        # update velocity along slope
    
            dx = block.vel * dt * cos(theta)  # x component
            dy = block.vel * dt * sin(theta)  # y component
    
            block.pos.x += dx
            block.pos.y += dy*144
            
        # TODO fix the values here
        
    elif preset_menu.index == 2: # loop
        
        pass
    else:
        pass

while (True):
    rate(100)
    
    state = get_state()
    
    # before pressing start
    if state == 0:
        pass
    # after pressing start, before launch
    elif state == 1 or state == 2:
        run1(state)
    # after launching, before collision
    elif state == 3:
        run2()
    # after collision
    elif state == 4:
        run3()
    else:
        pass
        
    t += dt


# unreachable
