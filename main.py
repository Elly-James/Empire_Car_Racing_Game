# ===============LIBRARY==IMPORTS=================================

# Here at the begining of everything, we are importing the libraries for this game which we would need
# pygame is used to create the game, random for generating random numbers, and time which is used for timing 
# The pygame.locals import *, it includes contants like QUIT to handle events of the game


import pygame
from pygame.locals import *
import random
import time

#=================GAME==INITIALIZATION===============================

# Here we are initializing the pygame and the mixer module for playing the music of the game

pygame.init()
pygame.mixer.init()


#===================GAME==WINDOW==SETUP=========================

# Here we are setting up the window dimensions where the game is going to be played
# set_mode() sets the size of the display surface of the game
# set_captions() assigns the title of the game window

width_of_window = 1400  
height_of_window = 1000  
screen_dimensions = (width_of_window, height_of_window)
the_game_screen = pygame.display.set_mode(screen_dimensions)
pygame.display.set_caption('The Empire Car Racing Game')



#=================COLORS=OF==THE==GAME===================

# Defines the varoius game color


game_road_color = (100, 100, 100)
the_grass_color = (76, 208, 56)
game_over_color = (200, 0, 0)
game_text_color = (255, 255, 255)
road_lane_marks_color = (255, 232, 0)
highlighted_text_color = (0, 0, 0)


# ===============ROAD==CONFIGURATION===========================

# Here we are defining the width and height of the road, and the width of the road lane markers
# The road and lane dimensions are calculated based on the window size  to ensure proper alignment


game_road_width = 900  
road_lane_marker_width = 10
road_lane_marker_height = 50

# making sure the road lanes be properly spaced with equal width

road_lane_width = game_road_width / 3  
# properly positioning the lane on the left
game_road_left_lane = width_of_window / 2 - game_road_width / 3  
# properly positioning the middle lane on the center of the window
game_road_middle_lane = width_of_window / 2  

# properly positioning the lane on the right of the window
game_road_right_lane = width_of_window / 2 + game_road_width / 3  

# all the road lanes are stored in this list for easy access
game_road_lanes = [game_road_left_lane , game_road_middle_lane, game_road_right_lane]

#=================ROAD==LANES==MARKERS========================

# Here we are defining the positions of the road lane markers on the road
# road_left_edge is the X- coordinate of the left edge of the road
# road_right_edge is the Y-coordinate of the right edge of the road
# left_road_edge_marker and right_road_edge_marker are rectangles representing the left and right edges markers

road_left_edge = (width_of_window - game_road_width) // 2  

road = (road_left_edge, 0, game_road_width, height_of_window)

left_road_edge_marker= (road_left_edge - road_lane_marker_width, 0, road_lane_marker_width, height_of_window)

right_road_edge_marker = (road_left_edge + game_road_width, 0, road_lane_marker_width, height_of_window)


# This is the lane marker animation that tracks the vertical offset for animating lane markers
# Used to create the illusion for the movement for lane markers
lane_marker_offset_y = 0



#=================PLAYER==SETTINGS========================

# Here we are defining the player's car starting position 
# player_start_x  is the X-coordinate  (middle lane)
# player_start_y is the Y-coordinate (near the bottom of the screen)

player_start_x = game_road_middle_lane
player_start_y = height_of_window - 150  

#=================FRAME==SETTINGS========================

# Here we are defining the frame rate for the game where
# pygame.time.Clock() manages the game loops frame rate.
# frame_rate = 120 ensures the game runs smoothly at 120 frames per second (FPS)

my_game_clock = pygame.time.Clock()
frame_rate = 120

#=================GAME==SETTINGS========================


# Here we are tracking the game state and its settings

is_the_gameover = False # determines whether the game is over
my_game_speed = 2 # the speed of the vehicle
player_score = 0  # the score of the player
current_level = None  # the current level of the game
is_the_game_paused = False  # whether the game is paused
level_start_time = None # start time of the current level
level_duration = None  # duration of the current level
user_selected_level_index = 0  # index of the current level



#=================GAME==LEVELS========================

# Here we are defining the levels of the game
# Each level has its name, duration, speed and vehicle limit

the_game_levels = [
    {"name": "Easy", "time": 60, "speed": 2, "vehicle_limit": 3},
    {"name": "Medium", "time": 90, "speed": 3, "vehicle_limit": 5},
    {"name": "Hard", "time": 120, "speed": 4, "vehicle_limit": 7}
]


# ===============GAME==MUSIC======================================

# Here we are loading the music for the game which continuously loops the background music of the game

pygame.mixer.music.load('thegamemusic.mp3') # loads the music
pygame.mixer.music.play(-1)  # plays the music in an infinite loop



# ===============VEHICLE==CLASS======================================

# Here in this class it represents vehicle (enemy car) in the game
# pygame.sprite.Sprite is a base class in pygame for game objects
# scaling is used to scale the vehicle image to resize it to fit into the lane width
# we are also setting the position of the vehicle

class Vehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # here we are scaling the image so that it shouldn't be bigger than the lane
        image_scale = 65 / image.get_rect().width  

        new_width = image.get_rect().width* image_scale
        new_height = image.get_rect().height * image_scale

        # resizes the image to new dimensions specified by new_height and new_width
        # pygame.transform.scale is a pygame method used to resize an image, and the image is the original that needs to be resized

        self.image = pygame.transform.scale(image, (new_width, new_height))
        
        # gets and assigns the rectangular bounding area of the image
        self.rect = self.image.get_rect()

        # sets the center of the rectangu

        self.rect.center = [x, y]




#==================PLAYER==VEHICLE==CLASS==========================

# Here we are creating the player's car class which inherits from Vehicle class
# It loads the player car image and initializes its position
        
class PlayerVehicle(Vehicle):
    
    def __init__(self, x, y):
        image = pygame.image.load('the_game_images/car.png')
        super().__init__(image, x, y)
        


#=================SPRITE==GROUPS======================================

# Here we are creating groups for the player and the enemy vehicles
# pygame.sprite.Group()- Groups for managing multiple sprites

player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

#=================PLAYER==CAR======================================

# Here we are creating the player's car object and adding it to the player_group


game_player_car = PlayerVehicle(player_start_x, player_start_y)
player_group.add(game_player_car)



#=================LOADING==VEHICLE==IMAGES============================

# Here we are loading the images of enemy vehicles
# Stores the loaded images in game_enemy_vehicle_images

game_vehicle_image_files = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
game_enemy_vehicle_images = []
for image_filename in game_vehicle_image_files:
    image = pygame.image.load('the_game_images/' + image_filename)
    game_enemy_vehicle_images.append(image)
    

#=================LOADING==CRASH==IMAGE=============================

# Here we are loading the image for crash
# Used to display a crash animation when the player collides with an enemy vehicle

crash_image = pygame.image.load('the_game_images/crash.png')
crash_image_rect = crash_image.get_rect()



#=================DRAWING==TEXT==FUNCTION============================

# Here this function is used to draw text to the screen
# It renders text with specified font, color and position

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    # sets the center of the text rectangle to the given coordinates x,y

    textrect.center = (x, y)

    # draws the textobject on the surface at the position of the text rectangle

    surface.blit(textobj, textrect)



#=================COUNTDOWN==FUNCTION============================

# Here this function is used to display a countdown before the game starts


def countdown():
    for i in range(3, 0, -1):  # loops from 3 down to 1 inclusive

        the_game_screen.fill(the_grass_color) # fills the game screen with the background color

        # draws the countdown num i on the screen, converts the num to str and sets the font style and size accordingly
        # also the color is set, specifies the screen to draw on and centers the text horizontally and vertically
        draw_text(str(i), pygame.font.Font(None, 144), game_text_color, the_game_screen, width_of_window // 2, height_of_window // 2)

        # updates the display to show the changes
        # pauses for 1 sec before displaying the next number in the countdown
        pygame.display.update()
        time.sleep(1)


# ==============CHOOSE==LEVEL==FUNCTION===============================

# Here this function is used to choose the level of the game


def choose_level():

    # declaring the varibales as global to allow modification of them anywhere in the function

    global current_level, level_start_time, level_duration, user_selected_level_index, my_game_speed

    # initializing the level selection of the game
    
    choosing = True

    # makes the game start with the previously selected level
    selected_level = user_selected_level_index  
    
    while choosing:

        # cleas the screen and sets the background color
        the_game_screen.fill(the_grass_color)

        # displays title and the instructions for selecting game level
        draw_text('Welcome To The Empire Car Racing Game', pygame.font.Font(None, 80), game_text_color, the_game_screen, width_of_window // 2, height_of_window // 2 - 250)

        draw_text('Select your level', pygame.font.Font(None, 80), game_text_color, the_game_screen, width_of_window // 2, height_of_window // 2 - 150)
        
        # draws the level options on the screen and highlights the selected ones
        level_font = pygame.font.Font(None, 56)
        
        # draws a rectangular background box for the level options
        level_bg_rect = pygame.Rect(width_of_window // 2 - 200, height_of_window // 2 - 100, 400, 300)
        pygame.draw.rect(the_game_screen, (50, 150, 50), level_bg_rect)
        pygame.draw.rect(the_game_screen, game_text_color, level_bg_rect, 3)
        
        # Displays the instructions for how to navigate the menu and the instructions of the game

        instruction_font = pygame.font.Font(None, 32)

        # Main Heading for the instructions


        instructions1 = "INSTRUCTIONS"
        draw_text(instructions1, instruction_font, (0,0,0), the_game_screen, width_of_window // 2, height_of_window // 2 + 220)

        # INstruction for the selecting the level
        instructions2 = "1. Use UP/DOWN arrows keys to select, press ENTER key to confirm"
        draw_text(instructions2, instruction_font, game_text_color, the_game_screen, width_of_window // 2, height_of_window // 2 + 260)

        # instructions for the game play

        instructions3 = "2. In the game, use space bar to pause the game and to unpause game"
        draw_text(instructions3, instruction_font, game_text_color, the_game_screen, width_of_window // 2, height_of_window // 2 + 300)

        instructions3 = "3. Use the left and right chevron buttons to change lanes for the car"
        draw_text(instructions3, instruction_font, game_text_color, the_game_screen, width_of_window // 2, height_of_window // 2 + 340)

        instructions3 = "4. Avoid colliding with other cars, and get as many points as possible"
        draw_text(instructions3, instruction_font, game_text_color, the_game_screen, width_of_window // 2, height_of_window // 2 + 380)

        # Display the level options with the selected one highlighted
        
        
        y_pos = height_of_window // 2 - 70 # start position for the level options

        for i, lvl in enumerate(the_game_levels): # loops through all levels
            level_text = f"{i+1}. {lvl['name']}" # displays the level name with numbering them
            
            # if the current level is selected, higlight the selected level with a background box 
            if i == selected_level:
                # Draw selection background
                select_rect = pygame.Rect(width_of_window // 2 - 180, y_pos - 20, 360, 50)

                pygame.draw.rect(the_game_screen, (100, 200, 100), select_rect) # highlighting color

                color = highlighted_text_color  # us the given color for the selected text level
            else:
                color = game_text_color  # default coloring for the unselected text level
            
            
            # rendering and positioning of the level text
             
            text_surface = level_font.render(level_text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.left = width_of_window // 2 - 150
            text_rect.centery = y_pos
            the_game_screen.blit(text_surface, text_rect)
            
            y_pos += 80  # space out level options vertically aligned
        
        pygame.display.update()  # this updates the screen to show the changes 

        

        # the below is uded to handle user inputs like the arrow keys and enter 
        for event in pygame.event.get():
            if event.type == QUIT: # if the user closes the window 
                pygame.quit()  # quit the game
                return False
                
            if event.type == KEYDOWN:
                if event.key == K_UP:  # move up in the level list

                    selected_level = (selected_level - 1) % len(the_game_levels)

                elif event.key == K_DOWN: # used to move down in the level list
                    selected_level = (selected_level + 1) % len(the_game_levels)
                elif event.key == K_RETURN: # confirms the selctions
                    

                    # saving the selected level and its properties

                    user_selected_level_index = selected_level
                    current_level = the_game_levels[selected_level]["name"].lower()
                    level_duration = the_game_levels[selected_level]["time"]
                    my_game_speed = the_game_levels[selected_level]["speed"]  # setting the speed of the selected level

                    choosing = False  # exit the selection loop
                elif event.key == K_ESCAPE: # quits the game when escape button is pressed

                    pygame.quit()
                    return False

    countdown()  # launches the countdown timer before the game starts

    level_start_time = time.time()  # records the start time of the level
    return True # indicates successful level selection



# calculates the lane movement distance based on the lane width of the road

lane_move_distance = road_lane_width





#======================GAME==LOOP====================================

# Handles the player input e.g moving the car, pausing the game
# updates the game state e.g collision
# Handles the game-over and level completion logic

running = True

# this checks if the game should start by calling the function choose_level, if the function returns returns false the game stops immediately

if not choose_level():
    running = False

# this is the main loop of our game, it runs as long as running is true

while running:
    my_game_clock.tick(frame_rate) # this controls the speed of the game in FPS

    # Handles the user input e.g if the user quits the game it stops running
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        # the below is used to move the player car and pausing the game
        # if left or right arrow keys are pressed the car moves left or right
        # pressing the space bar pauses the game



        if event.type == KEYDOWN:
            if event.key == K_LEFT and game_player_car.rect.center[0] > game_road_left_lane :
                game_player_car.rect.x -= lane_move_distance
            elif event.key == K_RIGHT and game_player_car.rect.center[0] < game_road_right_lane:
                game_player_car.rect.x += lane_move_distance
            elif event.key == K_SPACE:
                is_the_game_paused = not is_the_game_paused
                
            

            # this checks if there is any collision of the player car with the other vehicles, if so the game ends where is the game over = true

            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(game_player_car, vehicle):
                    is_the_gameover = True

                    # handles the crash by positioning the car after collision

                    if event.key == K_LEFT:
                        game_player_car.rect.left = vehicle.rect.right
                        crash_image_rect.center = [game_player_car.rect.left, (game_player_car.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        game_player_car.rect.right = vehicle.rect.left
                        crash_image_rect.center = [game_player_car.rect.right, (game_player_car.rect.center[1] + vehicle.rect.center[1]) / 2]



    
            
    if not is_the_game_paused and not is_the_gameover:
        

        # this ensures the drawing of the grass, the road and the lane markers

        the_game_screen.fill(the_grass_color)
        
        pygame.draw.rect(the_game_screen, game_road_color, road)
        
        pygame.draw.rect(the_game_screen, road_lane_marks_color, left_road_edge_marker)
        pygame.draw.rect(the_game_screen, road_lane_marks_color, right_road_edge_marker)
        
        # drawing the lane markers centered in each lane

        lane_marker_offset_y += my_game_speed * 2
        if lane_marker_offset_y >= road_lane_marker_height * 2:
            lane_marker_offset_y = 0

        
            
        # positions the lane markers 
        for y in range(road_lane_marker_height * -2, height_of_window, road_lane_marker_height * 2):


            # positions the road lane markers at the boundaries well

            marker_x1 = game_road_left_lane  + road_lane_width / 2 - road_lane_marker_width / 2
            marker_x2 = game_road_middle_lane + road_lane_width / 2 - road_lane_marker_width / 2
            marker_x3 = game_road_right_lane - road_lane_width / 2 - road_lane_marker_width / 2
            
            pygame.draw.rect(the_game_screen, game_text_color, (marker_x1, y + lane_marker_offset_y, road_lane_marker_width, road_lane_marker_height))
            pygame.draw.rect(the_game_screen, game_text_color, (marker_x2, y + lane_marker_offset_y, road_lane_marker_width, road_lane_marker_height))
            pygame.draw.rect(the_game_screen, game_text_color, (marker_x3, y + lane_marker_offset_y, road_lane_marker_width, road_lane_marker_height))
            
        # this draws the player car

        player_group.draw(the_game_screen)
        
        # this adds a vehicle 
        vehicle_limit = the_game_levels[user_selected_level_index]["vehicle_limit"]

        # adds vehicles to the game, randomly ensuring the vehicle count stays below the vehicle_limit
        if len(vehicle_group) < vehicle_limit:
            should_add_vehicle = True
            for vehicle in vehicle_group:
                if vehicle.rect.top < vehicle.rect.height * 1.5:
                    should_add_vehicle = False
                    
            if should_add_vehicle:
                random_lane_center = random.choice(game_road_lanes)
                image = random.choice(game_enemy_vehicle_images)
                vehicle = Vehicle(image, random_lane_center, height_of_window / -2)
                vehicle_group.add(vehicle)
        
        # moves the vehicles down the screen with the  speed determined by  my_game_speed

        for vehicle in vehicle_group:
            vehicle.rect.y += my_game_speed
            
            # this ensures the vehicle disppears once it goes off the screen

            if vehicle.rect.top >= height_of_window:
                vehicle.kill()
                player_score += 1
                if player_score > 0 and player_score % 5 == 0:
                    my_game_speed += 0.5  # this gradual increase of the speed

        
        # drawing the vehicles to the screen
        vehicle_group.draw(the_game_screen)
        
        # displays the score and timer for the game

        font = pygame.font.Font(pygame.font.get_default_font(), 32)  
        
        # positioning the score not to overlap into the road

        score_x = road_left_edge // 2
        text = font.render(f'Score: {player_score}', True, game_text_color)
        text_rect = text.get_rect()
        text_rect.center = (score_x, height_of_window - 100)
        the_game_screen.blit(text, text_rect)

        # Displaying the timer  of the game just below the score

        time_elapsed = int(time.time() - level_start_time)
        time_remaining = max(0, level_duration - time_elapsed)
        minutes_remaining = time_remaining  // 60
        seconds_remaining = time_remaining  % 60
        time_display_text = font.render(f'Time: {minutes_remaining:02d}:{seconds_remaining:02d}', True, game_text_color)
        time_display_rect = time_display_text.get_rect()
        time_display_rect.center = (score_x, height_of_window - 50)
        the_game_screen.blit(time_display_text, time_display_rect)
        
        # checks for any collisions on the game when playing

        if pygame.sprite.spritecollide(game_player_car, vehicle_group, True):
            is_the_gameover = True
            crash_image_rect.center = [game_player_car.rect.center[0], game_player_car.rect.top]
                
        #  displays game over when thre is a collision and the message for the game over

        if is_the_gameover:
            the_game_screen.blit(crash_image, crash_image_rect)
            pygame.draw.rect(the_game_screen, game_over_color, (0, 50, width_of_window, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 32)  

            text = font.render('Game over. Play again? (Enter Y or N)', True, game_text_color)
            text_rect = text.get_rect()
            text_rect.center = (width_of_window / 2, 100)
            the_game_screen.blit(text, text_rect)
        
        # the player car wins if there is no collisions and the timer is up 

        if time_elapsed >= level_duration:
            is_the_gameover = True
            pygame.draw.rect(the_game_screen, the_grass_color, (0, 50, width_of_window, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 32)  
            
            # Enables the player to progress to the next level when they have finished and won the current level

            if user_selected_level_index < len(the_game_levels) - 1:
                text = font.render(f'Level Complete! Press N for next level or Q to quit', True, game_text_color)
            else:
                text = font.render('All Levels Complete! Play again? (Y/N)', True, game_text_color)
                
            text_rect = text.get_rect()
            text_rect.center = (width_of_window / 2, 100)
            the_game_screen.blit(text, text_rect)
        
        pygame.display.update() # updates the game screen for the changes





#================================================================

    # handles the game over state of the game

    while is_the_gameover:
        my_game_clock.tick(frame_rate)
        for event in pygame.event.get():
            if event.type == QUIT:
                is_the_gameover = False
                running = False
                
            if event.type == KEYDOWN:
               # checks if the level timer is over, if yes, the game ends and the player proceeds to the next level or restart

                if time_elapsed >= level_duration:
                    if user_selected_level_index < len(the_game_levels) - 1 and event.key == K_n:
                       
                       # moving to the next level of the game

                        is_the_gameover = False
                        my_game_speed = the_game_levels[user_selected_level_index + 1]["speed"]  # setting up speed for the next level

                        player_score = 0
                        vehicle_group.empty()
                        game_player_car.rect.center = [player_start_x, player_start_y]
                        user_selected_level_index += 1
                        current_level = the_game_levels[user_selected_level_index]["name"].lower()
                        level_duration = the_game_levels[user_selected_level_index]["time"]
                        countdown()
                        level_start_time = time.time()
                    elif event.key == K_y:

                        # restart the game from the beginning
                        is_the_gameover = False
                        my_game_speed = 2
                        player_score = 0
                        vehicle_group.empty()
                        game_player_car.rect.center = [player_start_x, player_start_y]
                        if not choose_level():
                            running = False
                    elif event.key == K_q or event.key == K_n or event.key == K_ESCAPE:
                        is_the_gameover = False
                        running = False

                    # in a game over condition
                else:
                    if event.key == K_y:
                        

                        # restart the game from the beginning

                        is_the_gameover = False
                        my_game_speed = 2
                        player_score = 0
                        vehicle_group.empty()
                        game_player_car.rect.center = [player_start_x, player_start_y]
                        if not choose_level():
                            running = False
                    elif event.key == K_n:
                        is_the_gameover = False
                        running = False

pygame.quit() # quits the game when the loop ends

#================================================================