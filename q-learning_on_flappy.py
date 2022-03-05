import pygame, sys, random
import matplotlib.pyplot as plt
import numpy as np


# =============================================================================
# GAME VARIABLES
# =============================================================================
screen_width=376
screen_height=624

floor_height=100
floor_width=screen_width

bird_width=40
bird_height=28

bird_pos_x=60
bird_pos_y=290

pipe_width=65
pipe_height=400
pipe_gap=170
    
score_display_x=190
score_display_y=60

high_score_display_x=190
high_score_display_y=500

game_over_display_x=190
game_over_display_y=270


pipe_pos_x_to_add_pipes=40

gravity = 0.15

flap=5
# =============================================================================
# FUNCTIONS FOR Q-learning
# =============================================================================
def to_jump(x, y):
    if (Q[x][y][1] > Q[x][y][0]):
        return True
    return False


def get_states(birdxpos, birdypos, bttm_pipes):
    x = min(screen_width, bttm_pipes.bottomleft[0])
    y = bttm_pipes.bottomleft[1] - birdypos
    return int(x/40), int(y/40)


def Q_update(x_prev, y_prev, jump, reward, x_new, y_new, Q):
    learning_rate=0.6
    gamma=0.9
    if jump:
        Q[x_prev][y_prev][1] = (1-learning_rate)* Q[x_prev][y_prev][1] + learning_rate * (
                    reward + gamma * max(Q[x_new][y_new][0], Q[x_new][y_new][1]))
    else:
        Q[x_prev][y_prev][0] =(1-learning_rate)* Q[x_prev][y_prev][0] + learning_rate * (
                    reward + gamma * max(Q[x_new][y_new][0], Q[x_new][y_new][1]))


# =============================================================================
# FUNCTIONS FOR Flappy
# =============================================================================

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, screen_height - floor_height))
    screen.blit(floor_surface, (floor_x_pos + screen_width, screen_height - floor_height))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (screen_width+pipe_width/2, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (screen_width+pipe_width/2, random_pipe_pos - pipe_gap))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= screen_height:
           screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
            
def delete_pipes(pipe_list):
    new=[]
    for pipe in pipe_list:
        if pipe.centerx > -pipe_width/2:
            new.append(pipe)
    return new

def check_collision(pipes):
    for pipe in pipes: 
       if bird_rect.colliderect(pipe):
          return False
    
    if bird_rect.top <= 0 or bird_rect.bottom >= screen_height - floor_height:
        return False
    
    return True

def score_display(game_state):
    
    if game_state == 'main_game':
        # score
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (score_display_x, score_display_y))
        screen.blit(score_surface, score_rect)
        
        # high score
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(270, 30))
        screen.blit(high_score_surface, high_score_rect)

        # iteration
        interation_surface = game_font.render(f'Iteration: {int(iteration)}', True, (255, 255, 255))
        interation_rect = interation_surface.get_rect(center=(85, 30))
        screen.blit(interation_surface, interation_rect)
        
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# =============================================================================
# START OF THE GAME
# =============================================================================

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 25)

#start of the game variables
bird_movement = 0
game_active = True
score = 0
high_score = 0

#initilaizing q-table
Q = np.zeros((10, 300, 2), dtype=float)

# background
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (screen_width, screen_height))

# floor
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (floor_width, floor_height))
floor_x_pos = 0

# bird
bird_surface = pygame.image.load('assets/yellowbird-midflap.png').convert()
bird_surface = pygame.transform.scale(bird_surface, (bird_width,bird_height))
bird_rect = bird_surface.get_rect(center = (bird_pos_x, bird_pos_y))

# pipe
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale(pipe_surface, (pipe_width, pipe_height))

pipe_height = [270, 370, 350, 300, 400]
pipe_list = []
pipe_list.extend(create_pipe())

#graph
iteration = 0
x = []
y = []

# =============================================================================
# GAME RUNNING
# =============================================================================
while True:
               
    #adding background
    screen.blit(bg_surface, (0,0))
    
    # q-learning
    x_prev, y_prev = get_states(bird_rect.topleft[0], bird_rect.topleft[1], pipe_list[-2])
    jump = to_jump(x_prev, y_prev)
    
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           # plotting
           plt.scatter(x, y)
           plt.xlabel("ITERATION")
           plt.ylabel("SCORE")
           plt.title("Flappy Bird")
           plt.show()
           
           pygame.quit()
           sys.exit()

           
    if jump:
        bird_movement = -flap
        bird_rect.centery += bird_movement
    
    if game_active:
        #adding bird, and moving it
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect)
        game_active = check_collision(pipe_list)
        #reward for being alive
        reward = 15

        #moving pipes, adding them in list and screen and deleting
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        # q-learning
        x_new, y_new = get_states(bird_rect.topleft[0], bird_rect.topleft[1], pipe_list[-2])
        Q_update(x_prev, y_prev, jump, reward, x_new, y_new, Q)

        for pipe_index in range(0, len(pipe_list), 2):
            
            if pipe_list[pipe_index].centerx == bird_pos_x:
                score += 1
            if pipe_list[pipe_index].centerx == pipe_pos_x_to_add_pipes:
                pipe_list.extend(create_pipe())

        pipe_list=delete_pipes(pipe_list)
        
        
        score_display('main_game')
    else:
        # graph
        iteration += 1
        x.append(iteration)
        y.append(score)
        
        # updating high-score
        high_score = update_score(score, high_score)
        
        #reward for dying
        reward = -1000
        #updating q-table
        Q_update(x_prev, y_prev, jump, reward, x_new, y_new, Q)
        
        #variables for starting game
        score = 0
        pipe_list.clear()
        pipe_list.extend(create_pipe())
        bird_movement = 0
        bird_rect.center = (bird_pos_x, bird_pos_y)
        counter = 0
        
        #starting game
        game_active = True

    # adding floor, and moving it
    floor_x_pos -= 2
    draw_floor()
    if floor_x_pos <= -screen_width:
        floor_x_pos = 0

    
    pygame.display.update()
    clock.tick(120)
