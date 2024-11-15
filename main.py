# main.py

from vex import *
import time
print("Running main.py")
# utils.py

from vex import *
import time

# Initialize devices
brain = Brain()
controller_1 = Controller(PRIMARY)
left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_6_1, True)
left_motor_b = Motor(Ports.PORT2, GearSetting.RATIO_6_1, True)
left_motor_c = Motor(Ports.PORT3, GearSetting.RATIO_6_1, True)
 
right_motor_a = Motor(Ports.PORT11, GearSetting.RATIO_6_1, False)
right_motor_b = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
right_motor_c = Motor(Ports.PORT13, GearSetting.RATIO_6_1, False)
 
left_drive_smart = MotorGroup(left_motor_a, left_motor_b, left_motor_c)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b, right_motor_c)
High_scoring = Motor(Ports.PORT5)
intake = Motor(Ports.PORT6)
mogo_p = DigitalOut(brain.three_wire_port.a)
intake_p = DigitalOut(brain.three_wire_port.b)

# Constants
MSEC_PER_SEC = 1000

# Global variables
reverse_drive = False
intake_running = False
high_scoring_running = False
current_direction = FORWARD
high_scoring_mode = False
# Constants
STALL_THRESHOLD = 5       # Adjust as needed
STALL_COUNT = 10
RETRY_LIMIT = 3
RETRY_INTERVAL = 500      # in milliseconds
REVERSE_TIME = 500        # in milliseconds
MSEC_PER_SEC = 1000

# Global variables
intake_stalled = False
retry_count = 0
last_retry_time = 0
consecutive_stall_count = 0
intake_running = False
current_direction = FORWARD
high_scoring_running = False
high_score_stall = False  # Set this accordingly in your main code if needed

# Function to set the state of the high scoring motor
def set_high_scoring_motor_state(state, direction=FORWARD):
    global high_scoring_running
    if state:
        High_scoring.spin(direction)
    else:
        High_scoring.stop()
    high_scoring_running = state

# Function to set the state of the intake motor
def set_intake_motor_state(state, direction=FORWARD):
    global intake_running, current_direction
    if state:
        intake.spin(direction)
        current_direction = direction
    else:
        intake.stop()
    intake_running = state

# Stall detection and handling for the intake motor
def stall_detection_and_handling():
    global consecutive_stall_count, intake_stalled, retry_count, last_retry_time
    current_time = time.ticks_ms()
    if intake_running:
        current_velocity = intake.velocity(PERCENT)
        if abs(current_velocity) <= STALL_THRESHOLD:
            consecutive_stall_count += 1
        else:
            consecutive_stall_count = 0

        if consecutive_stall_count >= STALL_COUNT and not intake_stalled:
            intake_stalled = True
            consecutive_stall_count = 0
            retry_count = 0
            last_retry_time = current_time
    else:
        intake_stalled = False
        consecutive_stall_count = 0

# Retry mechanism for the intake motor when stalled
def retry_mechanism():
    global intake_stalled, retry_count, last_retry_time, current_direction, high_score_stall
    current_time = time.ticks_ms()
    if intake_stalled:
        if retry_count < RETRY_LIMIT and current_time - last_retry_time > RETRY_INTERVAL:
            if high_score_stall:
                # High score stall handling
                intake.spin(REVERSE)
                wait(REVERSE_TIME, MSEC)
                High_scoring.spin(FORWARD)
                wait(100, MSEC)  # Move high scoring motor forward briefly
                High_scoring.stop()
                intake.stop()
                intake_stalled = False
            else:
                # Regular stall handling
                if current_direction == FORWARD:
                    intake.spin(REVERSE)
                else:
                    intake.spin(FORWARD)
                wait(REVERSE_TIME, MSEC)
                retry_count += 1
                last_retry_time = current_time
                intake.spin(current_direction)
                intake_stalled = False

from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code


# wait for rotation sensor to fully initialize
wait(30, MSEC)


#list definitions
pos_list = [(3.385, 110.743), (5.289, 111.357), (7.196, 111.958), (9.109, 112.541), (11.03, 113.097), (12.956, 113.638), (14.887, 114.157), (16.826, 114.647), (18.77, 115.119), (20.719, 115.568), (22.675, 115.983), (24.636, 116.375), (26.602, 116.743), (28.574, 117.078), (30.551, 117.379), (32.532, 117.651), (34.518, 117.892), (36.507, 118.1), (38.5, 118.263), (40.496, 118.39), (42.494, 118.479), (44.493, 118.528), (46.493, 118.534), (48.492, 118.496), (50.491, 118.411), (52.486, 118.275), (54.477, 118.087), (56.463, 117.847), (58.441, 117.553), (60.41, 117.204), (62.368, 116.796), (64.313, 116.33), (66.242, 115.803), (68.153, 115.215), (70.044, 114.564), (71.911, 113.846), (73.751, 113.064), (75.564, 112.218), (77.345, 111.309), (79.093, 110.338), (80.805, 109.305), (82.48, 108.212), (84.115, 107.061), (85.704, 105.846), (87.249, 104.577), (88.75, 103.255), (90.206, 101.884), (91.616, 100.466), (92.979, 99.003), (94.292, 97.494), (95.557, 95.945), (96.775, 94.359), (97.948, 92.739), (99.076, 91.088), (100.159, 89.407), (101.199, 87.698), (102.192, 85.962), (103.144, 84.203), (104.055, 82.423), (104.927, 80.623), (105.761, 78.806), (106.559, 76.972), (107.32, 75.122), (108.047, 73.259), (108.741, 71.384), (109.403, 69.496), (110.033, 67.598), (110.632, 65.69), (111.203, 63.773), (111.745, 61.848), (112.261, 59.916), (112.751, 57.977), (113.216, 56.032), (113.657, 54.081), (114.075, 52.125), (114.471, 50.165), (114.845, 48.2), (115.199, 46.232), (115.533, 44.26), (115.847, 42.285), (116.143, 40.307), (116.421, 38.326), (116.681, 36.343), (116.926, 34.358), (117.154, 32.371), (117.366, 30.382), (117.564, 28.392), (117.747, 26.401), (117.916, 24.408), (118.072, 22.414), (118.215, 20.419), (118.345, 18.423), (118.464, 16.427), (118.571, 14.43), (118.667, 12.432), (118.752, 10.434), (118.827, 8.435), (118.892, 6.436), (118.948, 4.437), (118.994, 2.438), (119.032, 0.438), (119.062, -1.562), (118.923, -3.556), (118.753, -5.549), (118.568, -7.54), (118.371, -9.53), (118.166, -11.52), (117.943, -13.507), (117.709, -15.494), (117.466, -17.479), (117.202, -19.461), (116.927, -21.442), (116.641, -23.422), (116.335, -25.398), (116.014, -27.372), (115.681, -29.344), (115.33, -31.313), (114.959, -33.278), (114.574, -35.241), (114.173, -37.2), (113.751, -39.155), (113.309, -41.106), (112.849, -43.052), (112.371, -44.994), (111.873, -46.931), (111.349, -48.861), (110.805, -50.786), (110.239, -52.704), (109.651, -54.615), (109.039, -56.52), (108.404, -58.416), (107.74, -60.303), (107.05, -62.18), (106.334, -64.047), (105.591, -65.904), (104.82, -67.749), (104.02, -69.582), (103.19, -71.402), (102.33, -73.207), (101.439, -74.998), (100.515, -76.772), (99.56, -78.529), (98.571, -80.267), (97.548, -81.986), (96.492, -83.684), (95.401, -85.36), (94.275, -87.013), (93.114, -88.641), (91.917, -90.244), (90.686, -91.819), (89.415, -93.364), (88.11, -94.879), (86.77, -96.364), (85.395, -97.816), (83.987, -99.236), (82.545, -100.622), (81.067, -101.969), (79.557, -103.28), (78.016, -104.555), (76.446, -105.794), (74.846, -106.994), (73.215, -108.152), (71.559, -109.273), (69.878, -110.356), (68.173, -111.401), (66.442, -112.404), (64.691, -113.369), (62.919, -114.298), (61.13, -115.191), (59.321, -116.044), (57.496, -116.861), (55.656, -117.645), (53.802, -118.396), (51.935, -119.112), (50.055, -119.795), (48.165, -120.449), (46.265, -121.073), (44.356, -121.67), (42.438, -122.237), (40.513, -122.777), (38.58, -123.294), (36.642, -123.787), (34.698, -124.258), (32.749, -124.706), (30.795, -125.133), (28.838, -125.542), (26.876, -125.932), (24.911, -126.306), (22.944, -126.664), (20.973, -127.006), (19.0, -127.334), (17.025, -127.65), (15.049, -127.954), (13.07, -128.247), (11.09, -128.53), (9.109, -128.804), (7.127, -129.07), (5.144, -129.328), (3.16, -129.579), (0.279, -129.936), (0.279, -129.936), (0.279, -129.936)]

#try first 20 points
pos_list = pos_list[:10]
start_pos_size = len(pos_list)

# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

#gyro start
gyro = Inertial(Ports.PORT19)
gyro.set_rotation(0, DEGREES)
gyro.set_heading(0, DEGREES)
 
gyro.calibrate()
 
gear_ratio = 3/4
tolerance = 1
lookahead = 1
current_x = pos_list[0][0]
current_y = pos_list[0][1]
previous_right_encoder = 0
previous_left_encoder = 0
forward_velocity = 80
turn_velocity_k = 1.5
left_velocity = 5
right_velocity = 5
#forward_velocity/100
wheel_circumference = 8.6393798
feet_to_unit = 2.5
gear_ratio = 3/4


def leftEncoder():
    return left_drive_smart.position(DEGREES)
 
def rightEncoder():
    return right_drive_smart.position(DEGREES)
 
def update_position():
    global current_x, current_y, current_angle, previous_left_encoder, previous_right_encoder
   
    # Calculate the distance traveled by each wheel
    left_encoder = ((leftEncoder() / 360) * wheel_circumference * gear_ratio) * feet_to_unit
    right_encoder = ((rightEncoder() / 360) * wheel_circumference * gear_ratio) * feet_to_unit
    delta_left = left_encoder - previous_left_encoder
    delta_right = right_encoder - previous_right_encoder
   
    # Update previous encoder values
    previous_left_encoder = left_encoder
    previous_right_encoder = right_encoder
   
    current_angle = math.radians(gyro.heading(DEGREES))
   
    # Calculate the robot's linear change
    delta_d = (delta_left + delta_right) / 2
   
    current_x += delta_d * math.cos(current_angle)
    current_y += delta_d * math.sin(current_angle)
 
 
def calculate_lookahead_point(n):
    global pos_list, current_x, current_y, start_pos_size, forward_velocity

    if len(pos_list) == 0:
        return "done"

    min_distance = float('inf')
    min_index = -1  # To keep track of the nearest valid point index

    num_points = min(n, len(pos_list))  # Number of points to check

    for i in range(num_points):
        dx = pos_list[i][0] - current_x
        dy = pos_list[i][1] - current_y
        distance = math.sqrt(dx**2 + dy**2)

        if distance <= lookahead:
            pos_list = pos_list[i+1:]
            print("x: "+ str(current_x)+" y: " + str(current_y) + " pos x: " + str(pos_list[0][0]) + "pos y: " + str(pos_list[0][1]) + "size: " + str(len(pos_list)))
            forward_velocity = forward_velocity * (len(pos_list)/start_pos_size) + 5
            return

        if distance >= lookahead and distance < min_distance:
            min_distance = distance
            min_index = i
            if min_index != 0:
                print("Other points are closer")
                print("x: "+ str(current_x)+" y: " + str(current_y) + " pos x: " + str(pos_list[i][0]) + "pos y: " + str(pos_list[i][1]) + "size: " + str(len(pos_list)))
                

 #   if min_index > 0:
        # Pop all points before the nearest valid point
        # pos_list = pos_list[min_index:]
        #forward_velocity = forward_velocity * (len(pos_list)/start_pos_size) + 5
 
def calculate_drive_speeds(forward_velocity, turn_velocity_k):
    global pos_list, current_x, current_y, current_angle, left_velocity, right_velocity
    current_angle = math.radians(gyro.heading(DEGREES))  # Get the current heading in radians
    dx = pos_list[0][0] - current_x  # Calculate the difference in x
    dy = pos_list[0][1] - current_y  # Calculate the difference in y

    # Calculate the angle to the target point
    point_angle = math.atan2(dy, dx)
    
    # Calculate the angle difference between the current heading and the target point
    point_angle_diff = point_angle - current_angle

    # Normalize the angle difference to be within the range [-π, π]
    if point_angle_diff > math.pi:
        point_angle_diff -= 2 * math.pi
    elif point_angle_diff < -math.pi:
        point_angle_diff += 2 * math.pi

    # Calculate the wheel velocities
    left_velocity = forward_velocity + (point_angle_diff) * turn_velocity_k
    right_velocity = forward_velocity - (point_angle_diff) * turn_velocity_k

    # Clamp the velocities to the range [-100, 100]
    left_velocity = max(min(left_velocity, 100), -100)
    right_velocity = max(min(right_velocity, 100), -100)

def autonomous_sample(): 
    global pos_list, current_x, current_y, current_angle, left_velocity, right_velocity, running
    wait(3, SECONDS)
 
    running = True

    while running:
        #print("left vel: " +str(left_velocity) +" right_vel: " +str(right_velocity))
        #print()
        calculate_lookahead_point(3)
        if pos_list == []:
            running = False
            break
        calculate_drive_speeds(forward_velocity, turn_velocity_k)
        # print("x: "+ str(current_x)+" y: " + str(current_y) + " pos x: " + str(pos_list[0][0]) + "pos y: " + str(pos_list[0][1]) + "size: " + str(len(pos_list)))
        #print("left vel: " +str(left_velocity) +" right_vel: " +str(right_velocity))
        left_drive_smart.set_velocity(left_velocity, PERCENT)
        left_drive_smart.spin(FORWARD)
        right_drive_smart.set_velocity(right_velocity, PERCENT)
        right_drive_smart.spin(FORWARD)
        update_position()
    #left_drive_smart.set_velocity(0, PERCENT)
    #left_drive_smart.stop()
    #right_drive_smart.set_velocity(0, PERCENT)
    #right_drive_smart.stop()

# driver.py 

# Function to display joystick positions (optional)
def display_joystick_positions():
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    #joystick_positions = f"{int(controller_1.axis3.position())} {int(controller_1.axis2.position())}"
    #brain.screen.print(joystick_positions)
    wait(0.1, SECONDS)

# Function to set drive motor velocities based on controller input
def set_drive_motor_velocities():
    global reverse_drive
    if controller_1.buttonUp.pressing():
        reverse_drive = not reverse_drive
        print("Reversing drive direction " + str(reverse_drive))
        while controller_1.buttonUp.pressing():
            wait(10, MSEC)

    if reverse_drive:
        # Reverse joystick inputs
        left_joystick_y = -controller_1.axis2.position()
        right_joystick_y = -controller_1.axis3.position()
    else:
        # Normal control
        left_joystick_y = controller_1.axis3.position()
        right_joystick_y = controller_1.axis2.position()

    # Set velocities for left and right drive motors
    left_drive_smart.set_velocity(left_joystick_y, PERCENT)
    if abs(left_joystick_y) < 5:
        left_drive_smart.stop()
    else:
        print("Velocity: " + str(left_joystick_y) + " " + str(right_joystick_y))
        left_drive_smart.spin(FORWARD)

    right_drive_smart.set_velocity(right_joystick_y, PERCENT)
    if abs(right_joystick_y) < 5:
        right_drive_smart.stop()
    else:
        right_drive_smart.spin(FORWARD)

# Function to toggle the high scoring motor
def toggle_high_scoring_motor():
    global high_scoring_running
    if controller_1.buttonL1.pressing():
        wait(100, MSEC)  # Debounce delay
        high_scoring_running = not high_scoring_running
        set_high_scoring_motor_state(high_scoring_running, FORWARD)
        while controller_1.buttonL1.pressing():
            wait(10, MSEC)

    if controller_1.buttonL2.pressing():
        wait(100, MSEC)  # Debounce delay
        high_scoring_running = not high_scoring_running
        set_high_scoring_motor_state(high_scoring_running, REVERSE)
        while controller_1.buttonL2.pressing():
            wait(10, MSEC)

# Function to toggle the intake motor
def toggle_intake_motor():
    global intake_running
    if controller_1.buttonR1.pressing():
        wait(100, MSEC)  # Debounce delay
        intake_running = not intake_running
        set_intake_motor_state(intake_running, FORWARD)
        while controller_1.buttonR1.pressing():
            wait(10, MSEC)

    if controller_1.buttonR2.pressing():
        wait(100, MSEC)  # Debounce delay
        intake_running = not intake_running
        set_intake_motor_state(intake_running, REVERSE)
        while controller_1.buttonR2.pressing():
            wait(10, MSEC)

# Function to handle digital outputs based on controller buttons
def handle_digital_outputs():
    if controller_1.buttonA.pressing():
        mogo_p.set(False)
    if controller_1.buttonY.pressing():
        mogo_p.set(True)
    if controller_1.buttonX.pressing():
        intake_p.set(False)
    if controller_1.buttonB.pressing():
        intake_p.set(True)

# Function to toggle high scoring mode
def toggle_high_scoring_mode():
    global high_scoring_mode
    if controller_1.buttonDown.pressing():
        wait(100, MSEC)  # Debounce delay
        high_scoring_mode = not high_scoring_mode
        print("High scoring mode: " + str(high_scoring_mode))
        while controller_1.buttonDown.pressing():
            wait(10, MSEC)




# Autonomous function
def autonomous():
    # Autonomous code
    # For example, move forward for a certain distance
    autonomous_sample()

# Driver control function
def drivercontrol():
    # Main control loop for driver control
    while True:
        set_drive_motor_velocities()
        toggle_high_scoring_motor()
        toggle_intake_motor()
        toggle_high_scoring_mode()
        handle_digital_outputs()
        stall_detection_and_handling()
        retry_mechanism()
        wait(20, MSEC)

# Create a Competition object
competition = Competition(drivercontrol, autonomous)

def main():
    # Any initialization code before the match starts
    autonomous()
    #drivercontrol()

if __name__ == "__main__":
    main()