import pygame
from pygame.locals import *
import random
import time

pygame.init()
pygame.mixer.init()

# create the window
width = 1400  # Further enlarged window width
height = 1000  # Further enlarged window height
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

# the game colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)
black = (0, 0, 0)

# road and marker sizes
road_width = 900  # Adjusted for larger window
marker_width = 10
marker_height = 50

# lane coordinates (equally spaced)
lane_width = road_width / 3  # Equal lane width
left_lane = width / 2 - road_width / 3  # Properly positioned left lane
center_lane = width / 2  # Center lane is in the middle of the window
right_lane = width / 2 + road_width / 3  # Properly positioned right lane
lanes = [left_lane, center_lane, right_lane]

# road and edge markers
road_left = (width - road_width) // 2  # Center the road
road = (road_left, 0, road_width, height)
left_edge_marker = (road_left - marker_width, 0, marker_width, height)
right_edge_marker = (road_left + road_width, 0, marker_width, height)

# for animating movement of the lane markers
lane_marker_move_y = 0

# player's starting coordinates
player_x = center_lane
player_y = height - 150  # Adjust for larger window

# frame settings
clock = pygame.time.Clock()
fps = 120

# game settings
gameover = False
speed = 2
score = 0
level = None
paused = False
start_time = None
level_time = None
current_level_index = 0  # Track level index for progression

# Define levels
levels = [
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
        new_width = image.get_rect().width * image_scale
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
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# load the vehicle images
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('the_game_images/' + image_filename)
    vehicle_images.append(image)
    
# load the crash image
crash = pygame.image.load('the_game_images/crash.png')
crash_rect = crash.get_rect()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def countdown():
    for i in range(3, 0, -1):
        screen.fill(green)
        draw_text(str(i), pygame.font.Font(None, 144), white, screen, width // 2, height // 2)
        pygame.display.update()
        time.sleep(1)

def choose_level():
    global level, start_time, level_time, current_level_index, speed
    
    # Initialize level selection
    choosing = True
    selected_level = current_level_index  # Start with current level selected
    
    while choosing:
        screen.fill(green)
        draw_text('Choose Level', pygame.font.Font(None, 80), white, screen, width // 2, height // 2 - 200)
        
        # Draw level options with the selected one highlighted
        level_font = pygame.font.Font(None, 56)
        
        # Create a background for level selection area
        level_bg_rect = pygame.Rect(width // 2 - 200, height // 2 - 100, 400, 300)
        pygame.draw.rect(screen, (50, 150, 50), level_bg_rect)
        pygame.draw.rect(screen, white, level_bg_rect, 3)
        
        # Draw instructions for scrolling
        instruction_font = pygame.font.Font(None, 32)
        instructions = "Use UP/DOWN arrows to select, ENTER to confirm"
        draw_text(instructions, instruction_font, white, screen, width // 2, height // 2 + 250)
        
        # Draw level options left-justified with consistent spacing
        y_pos = height // 2 - 70
        for i, lvl in enumerate(levels):
            level_text = f"{i+1}. {lvl['name']}"
            
            # Highlight selected level
            if i == selected_level:
                # Draw selection background
                select_rect = pygame.Rect(width // 2 - 180, y_pos - 20, 360, 50)
                pygame.draw.rect(screen, (100, 200, 100), select_rect)
                color = black  # Text color for selected item
            else:
                color = white  # Text color for unselected items
            
            # Left justify text but still center the block of text
            text_surface = level_font.render(level_text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.left = width // 2 - 150
            text_rect.centery = y_pos
            screen.blit(text_surface, text_rect)
            
            y_pos += 80  # Increased spacing between options
        
        pygame.display.update()

        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False
                
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    selected_level = (selected_level - 1) % len(levels)
                elif event.key == K_DOWN:
                    selected_level = (selected_level + 1) % len(levels)
                elif event.key == K_RETURN:
                    # Set the level
                    current_level_index = selected_level
                    level = levels[selected_level]["name"].lower()
                    level_time = levels[selected_level]["time"]
                    speed = levels[selected_level]["speed"]  # Set speed based on level
                    choosing = False
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    return False

    countdown()
    start_time = time.time()
    return True

# Calculate lane movement distance based on the new lane positioning
lane_move_distance = lane_width

# game loop
running = True
if not choose_level():
    running = False

while running:
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        # move the player's car using the left/right arrow keys
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= lane_move_distance
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += lane_move_distance
            elif event.key == K_SPACE:
                paused = not paused
                
            # check if there's a side swipe collision after changing lanes
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    gameover = True
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
            
    if not paused and not gameover:
        # draw the grass
        screen.fill(green)
        
        # draw the road
        pygame.draw.rect(screen, gray, road)
        
        # draw the edge markers
        pygame.draw.rect(screen, yellow, left_edge_marker)
        pygame.draw.rect(screen, yellow, right_edge_marker)
        
        # draw the lane markers - centered in each lane
        lane_marker_move_y += speed * 2
        if lane_marker_move_y >= marker_height * 2:
            lane_marker_move_y = 0
            
        # Properly position the lane markers in the middle of each lane
        for y in range(marker_height * -2, height, marker_height * 2):
            # Position markers in the center of each boundary between lanes
            marker_x1 = left_lane + lane_width / 2 - marker_width / 2
            marker_x2 = center_lane + lane_width / 2 - marker_width / 2
            marker_x3 = right_lane - lane_width / 2 - marker_width / 2
            
            pygame.draw.rect(screen, white, (marker_x1, y + lane_marker_move_y, marker_width, marker_height))
            pygame.draw.rect(screen, white, (marker_x2, y + lane_marker_move_y, marker_width, marker_height))
            pygame.draw.rect(screen, white, (marker_x3, y + lane_marker_move_y, marker_width, marker_height))
            
        # draw the player's car
        player_group.draw(screen)
        
        # add a vehicle
        vehicle_limit = levels[current_level_index]["vehicle_limit"]
        if len(vehicle_group) < vehicle_limit:
            add_vehicle = True
            for vehicle in vehicle_group:
                if vehicle.rect.top < vehicle.rect.height * 1.5:
                    add_vehicle = False
                    
            if add_vehicle:
                lane = random.choice(lanes)
                image = random.choice(vehicle_images)
                vehicle = Vehicle(image, lane, height / -2)
                vehicle_group.add(vehicle)
        
        # make the vehicles move
        for vehicle in vehicle_group:
            vehicle.rect.y += speed
            
            # remove vehicle once it goes off screen
            if vehicle.rect.top >= height:
                vehicle.kill()
                score += 1
                if score > 0 and score % 5 == 0:
                    speed += 0.5  # Gradually increase speed
        
        # draw the vehicles
        vehicle_group.draw(screen)
        
        # display the score and timer with proper positioning
        font = pygame.font.Font(pygame.font.get_default_font(), 32)  # Larger font size
        
        # Score display - properly positioned away from the road
        score_x = road_left // 2
        text = font.render(f'Score: {score}', True, white)
        text_rect = text.get_rect()
        text_rect.center = (score_x, height - 100)
        screen.blit(text, text_rect)

        # Timer display with seconds - positioned below score
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, level_time - elapsed_time)
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        timer_text = font.render(f'Time: {minutes:02d}:{seconds:02d}', True, white)
        timer_rect = timer_text.get_rect()
        timer_rect.center = (score_x, height - 50)
        screen.blit(timer_text, timer_rect)
        
        # check if there's a head on collision
        if pygame.sprite.spritecollide(player, vehicle_group, True):
            gameover = True
            crash_rect.center = [player.rect.center[0], player.rect.top]
                
        # display game over
        if gameover:
            screen.blit(crash, crash_rect)
            pygame.draw.rect(screen, red, (0, 50, width, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 32)  # Larger font
            text = font.render('Game over. Play again? (Enter Y or N)', True, white)
            text_rect = text.get_rect()
            text_rect.center = (width / 2, 100)
            screen.blit(text, text_rect)
        
        # check if time is up (win condition)
        if elapsed_time >= level_time:
            gameover = True
            pygame.draw.rect(screen, green, (0, 50, width, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 32)  # Larger font
            
            # If there's a next level available, offer to progress
            if current_level_index < len(levels) - 1:
                text = font.render(f'Level Complete! Press N for next level or Q to quit', True, white)
            else:
                text = font.render('All Levels Complete! Play again? (Y/N)', True, white)
                
            text_rect = text.get_rect()
            text_rect.center = (width / 2, 100)
            screen.blit(text, text_rect)
        
        pygame.display.update()

    # Handle game over state
    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                gameover = False
                running = False
                
            if event.type == KEYDOWN:
                # Win condition - time completed
                if elapsed_time >= level_time:
                    if current_level_index < len(levels) - 1 and event.key == K_n:
                        # Move to next level
                        gameover = False
                        speed = levels[current_level_index + 1]["speed"]  # Set speed for next level
                        score = 0
                        vehicle_group.empty()
                        player.rect.center = [player_x, player_y]
                        current_level_index += 1
                        level = levels[current_level_index]["name"].lower()
                        level_time = levels[current_level_index]["time"]
                        countdown()
                        start_time = time.time()
                    elif event.key == K_y:
                        # Restart from level selection
                        gameover = False
                        speed = 2
                        score = 0
                        vehicle_group.empty()
                        player.rect.center = [player_x, player_y]
                        if not choose_level():
                            running = False
                    elif event.key == K_q or event.key == K_n or event.key == K_ESCAPE:
                        gameover = False
                        running = False
                # Game over condition
                else:
                    if event.key == K_y:
                        # Restart from level selection
                        gameover = False
                        speed = 2
                        score = 0
                        vehicle_group.empty()
                        player.rect.center = [player_x, player_y]
                        if not choose_level():
                            running = False
                    elif event.key == K_n:
                        gameover = False
                        running = False

pygame.quit()