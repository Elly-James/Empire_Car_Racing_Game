import pygame
from pygame.locals import *
import random
import time

pygame.init()
pygame.mixer.init()

# creating the window of the game
# this are the dimensions of the window where the game is played

width_of_window = 1400  
height_of_window = 1000  
screen_dimensions = (width_of_window, height_of_window)
the_game_screen = pygame.display.set_mode(screen_dimensions)
pygame.display.set_caption('The Empire Car Racing Game')

# the game colors
game_road_color = (100, 100, 100)
the_grass_color = (76, 208, 56)
game_over_color = (200, 0, 0)
game_text_color = (255, 255, 255)
road_lane_marks_color = (255, 232, 0)
highlighted_text_color = (0, 0, 0)

# road and marker sizes
game_road_width = 900  # Adjusted for larger window
road_lane_marker_width = 10
road_lane_marker_height = 50

# lane coordinates (equally spaced)
road_lane_width = game_road_width / 3  # Equal lane width
game_road_left_lane = width_of_window / 2 - game_road_width / 3  # Properly positioned left lane
game_road_middle_lane = width_of_window / 2  # Center lane is in the middle of the window
game_road_right_lane = width_of_window / 2 + game_road_width / 3  # Properly positioned right lane
game_road_lanes = [game_road_left_lane , game_road_middle_lane, game_road_right_lane]

# road and edge markers
road_left_edge = (width_of_window - game_road_width) // 2  # Center the road
road = (road_left_edge, 0, game_road_width, height_of_window)
left_road_edge_marker= (road_left_edge - road_lane_marker_width, 0, road_lane_marker_width, height_of_window)
right_road_edge_marker = (road_left_edge + game_road_width, 0, road_lane_marker_width, height_of_window)

# for animating movement of the lane markers
lane_marker_offset_y = 0

# player's starting coordinates
player_start_x = game_road_middle_lane
player_start_y = height_of_window - 150  # Adjust for larger window

# frame settings
my_game_clock = pygame.time.Clock()
frame_rate = 120

# game settings
is_the_gameover = False
my_game_speed = 2
player_score = 0
current_level = None
is_the_game_paused = False
level_start_time = None
level_duration = None
user_selected_level_index = 0  # Track level index for progression

# Define levels
the_game_levels = [
    {"name": "Easy", "time": 60, "speed": 2, "vehicle_limit": 3},
    {"name": "Medium", "time": 90, "speed": 3, "vehicle_limit": 5},
    {"name": "Hard", "time": 120, "speed": 4, "vehicle_limit": 7}
]

# Load music
pygame.mixer.music.load('thegamemusic.mp3')
pygame.mixer.music.play(-1)  # Loop indefinitely

class Vehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # scale the image down so it's not wider than the lane
        image_scale = 65 / image.get_rect().width  # Larger for bigger window
        new_width = image.get_rect().width* image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
class PlayerVehicle(Vehicle):
    
    def __init__(self, x, y):
        image = pygame.image.load('the_game_images/car.png')
        super().__init__(image, x, y)
        
# sprite groups
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# create the player's car
game_player_car = PlayerVehicle(player_start_x, player_start_y)
player_group.add(game_player_car)

# load the vehicle images
game_vehicle_image_files = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
game_enemy_vehicle_images = []
for image_filename in game_vehicle_image_files:
    image = pygame.image.load('the_game_images/' + image_filename)
    game_enemy_vehicle_images.append(image)
    
# load the crash image
crash_image = pygame.image.load('the_game_images/crash.png')
crash_image_rect = crash_image.get_rect()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def countdown():
    for i in range(3, 0, -1):
        the_game_screen.fill(the_grass_color)
        draw_text(str(i), pygame.font.Font(None, 144), game_text_color, the_game_screen, width_of_window // 2, height_of_window // 2)
        pygame.display.update()
        time.sleep(1)

def choose_level():
    global current_level, level_start_time, level_duration, user_selected_level_index, my_game_speed
    
    # Initialize level selection
    choosing = True
    selected_level = user_selected_level_index  # Start with current level selected
    
    while choosing:
        the_game_screen.fill(the_grass_color)
        draw_text('Welcome To The Empire Car Racing Game', pygame.font.Font(None, 80), game_text_color, the_game_screen, width_of_window // 2, height_of_window // 2 - 250)

        draw_text('Select your level', pygame.font.Font(None, 80), game_text_color, the_game_screen, width_of_window // 2, height_of_window // 2 - 150)
        
        # Draw level options with the selected one highlighted
        level_font = pygame.font.Font(None, 56)
        
        # Create a background for level selection area
        level_bg_rect = pygame.Rect(width_of_window // 2 - 200, height_of_window // 2 - 100, 400, 300)
        pygame.draw.rect(the_game_screen, (50, 150, 50), level_bg_rect)
        pygame.draw.rect(the_game_screen, game_text_color, level_bg_rect, 3)
        
        # Draw instructions for scrolling
        instruction_font = pygame.font.Font(None, 32)
        instructions = "Use UP/DOWN arrows keys to select, press ENTER key to confirm"
        draw_text(instructions, instruction_font, game_text_color, the_game_screen, width_of_window // 2, height_of_window // 2 + 250)
        
        # Draw level options left-justified with consistent spacing
        y_pos = height_of_window // 2 - 70
        for i, lvl in enumerate(the_game_levels):
            level_text = f"{i+1}. {lvl['name']}"
            
            # Highlight selected level
            if i == selected_level:
                # Draw selection background
                select_rect = pygame.Rect(width_of_window // 2 - 180, y_pos - 20, 360, 50)
                pygame.draw.rect(the_game_screen, (100, 200, 100), select_rect)
                color = highlighted_text_color  # Text color for selected item
            else:
                color = game_text_color  # Text color for unselected items
            
            # Left justify text but still center the block of text
            text_surface = level_font.render(level_text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.left = width_of_window // 2 - 150
            text_rect.centery = y_pos
            the_game_screen.blit(text_surface, text_rect)
            
            y_pos += 80  # Increased spacing between options
        
        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False
                
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    selected_level = (selected_level - 1) % len(the_game_levels)
                elif event.key == K_DOWN:
                    selected_level = (selected_level + 1) % len(the_game_levels)
                elif event.key == K_RETURN:
                    # Set the level
                    user_selected_level_index = selected_level
                    current_level = the_game_levels[selected_level]["name"].lower()
                    level_duration = the_game_levels[selected_level]["time"]
                    my_game_speed = the_game_levels[selected_level]["speed"]  # Set speed based on level
                    choosing = False
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    return False

    countdown()
    level_start_time = time.time()
    return True

# Calculate lane movement distance based on the new lane positioning
lane_move_distance = road_lane_width

# game loop
running = True
if not choose_level():
    running = False

while running:
    my_game_clock.tick(frame_rate)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        # move the player's car using the left/right arrow keys
        if event.type == KEYDOWN:
            if event.key == K_LEFT and game_player_car.rect.center[0] > game_road_left_lane :
                game_player_car.rect.x -= lane_move_distance
            elif event.key == K_RIGHT and game_player_car.rect.center[0] < game_road_right_lane:
                game_player_car.rect.x += lane_move_distance
            elif event.key == K_SPACE:
                is_the_game_paused = not is_the_game_paused
                
            # check if there's a side swipe collision after changing lanes
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(game_player_car, vehicle):
                    is_the_gameover = True
                    if event.key == K_LEFT:
                        game_player_car.rect.left = vehicle.rect.right
                        crash_image_rect.center = [game_player_car.rect.left, (game_player_car.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        game_player_car.rect.right = vehicle.rect.left
                        crash_image_rect.center = [game_player_car.rect.right, (game_player_car.rect.center[1] + vehicle.rect.center[1]) / 2]
            
    if not is_the_game_paused and not is_the_gameover:
        # draw the grass
        the_game_screen.fill(the_grass_color)
        
        # draw the road
        pygame.draw.rect(the_game_screen, game_road_color, road)
        
        # draw the edge markers
        pygame.draw.rect(the_game_screen, road_lane_marks_color, left_road_edge_marker)
        pygame.draw.rect(the_game_screen, road_lane_marks_color, right_road_edge_marker)
        
        # draw the lane markers - centered in each lane
        lane_marker_offset_y += my_game_speed * 2
        if lane_marker_offset_y >= road_lane_marker_height * 2:
            lane_marker_offset_y = 0
            
        # Properly position the lane markers in the middle of each lane
        for y in range(road_lane_marker_height * -2, height_of_window, road_lane_marker_height * 2):
            # Position markers in the center of each boundary between lanes
            marker_x1 = game_road_left_lane  + road_lane_width / 2 - road_lane_marker_width / 2
            marker_x2 = game_road_middle_lane + road_lane_width / 2 - road_lane_marker_width / 2
            marker_x3 = game_road_right_lane - road_lane_width / 2 - road_lane_marker_width / 2
            
            pygame.draw.rect(the_game_screen, game_text_color, (marker_x1, y + lane_marker_offset_y, road_lane_marker_width, road_lane_marker_height))
            pygame.draw.rect(the_game_screen, game_text_color, (marker_x2, y + lane_marker_offset_y, road_lane_marker_width, road_lane_marker_height))
            pygame.draw.rect(the_game_screen, game_text_color, (marker_x3, y + lane_marker_offset_y, road_lane_marker_width, road_lane_marker_height))
            
        # draw the player's car
        player_group.draw(the_game_screen)
        
        # add a vehicle
        vehicle_limit = the_game_levels[user_selected_level_index]["vehicle_limit"]
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
        
        # make the vehicles move
        for vehicle in vehicle_group:
            vehicle.rect.y += my_game_speed
            
            # remove vehicle once it goes off screen
            if vehicle.rect.top >= height_of_window:
                vehicle.kill()
                player_score += 1
                if player_score > 0 and player_score % 5 == 0:
                    my_game_speed += 0.5  # Gradually increase speed
        
        # draw the vehicles
        vehicle_group.draw(the_game_screen)
        
        # display the score and timer with proper positioning
        font = pygame.font.Font(pygame.font.get_default_font(), 32)  # Larger font size
        
        # Score display - properly positioned away from the road
        score_x = road_left_edge // 2
        text = font.render(f'Score: {player_score}', True, game_text_color)
        text_rect = text.get_rect()
        text_rect.center = (score_x, height_of_window - 100)
        the_game_screen.blit(text, text_rect)

        # Timer display with seconds - positioned below score
        time_elapsed = int(time.time() - level_start_time)
        time_remaining = max(0, level_duration - time_elapsed)
        minutes_remaining = time_remaining  // 60
        seconds_remaining = time_remaining  % 60
        time_display_text = font.render(f'Time: {minutes_remaining:02d}:{seconds_remaining:02d}', True, game_text_color)
        time_display_rect = time_display_text.get_rect()
        time_display_rect.center = (score_x, height_of_window - 50)
        the_game_screen.blit(time_display_text, time_display_rect)
        
        # check if there's a head on collision
        if pygame.sprite.spritecollide(game_player_car, vehicle_group, True):
            is_the_gameover = True
            crash_image_rect.center = [game_player_car.rect.center[0], game_player_car.rect.top]
                
        # display game over
        if is_the_gameover:
            the_game_screen.blit(crash_image, crash_image_rect)
            pygame.draw.rect(the_game_screen, game_over_color, (0, 50, width_of_window, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 32)  # Larger font
            text = font.render('Game over. Play again? (Enter Y or N)', True, game_text_color)
            text_rect = text.get_rect()
            text_rect.center = (width_of_window / 2, 100)
            the_game_screen.blit(text, text_rect)
        
        # check if time is up (win condition)
        if time_elapsed >= level_duration:
            is_the_gameover = True
            pygame.draw.rect(the_game_screen, the_grass_color, (0, 50, width_of_window, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 32)  # Larger font
            
            # If there's a next level available, offer to progress
            if user_selected_level_index < len(the_game_levels) - 1:
                text = font.render(f'Level Complete! Press N for next level or Q to quit', True, game_text_color)
            else:
                text = font.render('All Levels Complete! Play again? (Y/N)', True, game_text_color)
                
            text_rect = text.get_rect()
            text_rect.center = (width_of_window / 2, 100)
            the_game_screen.blit(text, text_rect)
        
        pygame.display.update()

    # Handle game over state
    while is_the_gameover:
        my_game_clock.tick(frame_rate)
        for event in pygame.event.get():
            if event.type == QUIT:
                is_the_gameover = False
                running = False
                
            if event.type == KEYDOWN:
                # Win condition - time completed
                if time_elapsed >= level_duration:
                    if user_selected_level_index < len(the_game_levels) - 1 and event.key == K_n:
                        # Move to next level
                        is_the_gameover = False
                        my_game_speed = the_game_levels[user_selected_level_index + 1]["speed"]  # Set speed for next level
                        player_score = 0
                        vehicle_group.empty()
                        game_player_car.rect.center = [player_start_x, player_start_y]
                        user_selected_level_index += 1
                        current_level = the_game_levels[user_selected_level_index]["name"].lower()
                        level_duration = the_game_levels[user_selected_level_index]["time"]
                        countdown()
                        level_start_time = time.time()
                    elif event.key == K_y:
                        # Restart from level selection
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
                # Game over condition
                else:
                    if event.key == K_y:
                        # Restart from level selection
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

pygame.quit()