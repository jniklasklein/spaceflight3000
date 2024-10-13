import random
import math
import time

# Run this game in Processing

# SPACEFLIGHT3000
# ***************
# by Niklas Klein, 2024

move_left = False
move_right = False
shoot = False

game_over = False
spaceship = {}  # Spaceship dictionary
star_id = 0
stars = {}  # Stars dictionary
shot_id = 0
shots = {} # Shots dictionary
points = 0
level = 0
enemy_id = 0
enemies = {}  # Enemy dictionary
next_enemy_spawn_time = 0 
level_start_time = 0  # Tracks start of current level
level_duration = 10000  # Level duration in milliseconds



def setup():
    global spaceship, game_over
    
    size(800, 800)  # Window size
    noStroke()
    textSize(30)
    # Initialize spaceship
    spaceship = {'x': width/2, 'y': height-80}
    initiate_stars()
    
    game_over = False
    level_start_time = millis()

def draw():
    global star_id, move_left, move_right, shots, shoot, points, level, enemy_id, enemies, next_enemy_spawn_time, level_start_time, level_duration, game_over
    
    background(0)  # Set background to black
    
    if game_over:
        # Display Game Over message
        fill(255, 0, 0)  # Red text
        text("Game Over", width / 2 - 100, height / 2)
        text("Press R to Restart", width / 2 - 150, height / 2 + 40)
        return
    
    # STAR GENERATOR
    strokeWeight(1) 
    starbirth = random.randint(1,11)
    flickering = starbirth/10
    if starbirth > 10:  # starbirth rate
        create_star(star_id)
        star_id += 1
    for star in stars.keys():
        #fill(200, 255, 200)
        strokeWeight(flickering)
        ellipse(stars[star].pos_x, stars[star].pos_y, 2, 2)
        stars[star].move_down()
        if stars[star].pos_y > height:
            del stars[star]
    strokeWeight(10)
    
    # Spaceship control
    
    thruster = None

    if (move_left):
        if spaceship['x'] > 50:
            spaceship['x']-= 4
            thruster = "to_left"
        
    elif (move_right):
        if spaceship['x'] < 750:
            spaceship['x']+= 4
            thruster = "to_right"
            
    if (shoot):
        fire_shot()
        shoot = False
        
    # Update and draw laser shots
    for shot in list(shots.keys()):
        shots[shot].move_up()
        shots[shot].display()
        if shots[shot].pos_y < 0:  # Remove shot if it goes off-screen
            del shots[shot]
        
    draw_spaceship(spaceship['x'], spaceship['y'], thruster)
    
    # Render Enemy Worms
    render_enemy_worms()
    
    generate_enemies(5 + level)
    
    # **Time-Based Level Progression**
    current_time = millis()
    if current_time - level_start_time >= level_duration:
        level += 1
        level_start_time = millis()  # Reset level start time for next level
        next_enemy_spawn_time = current_time + 2000  # Add short delay before next wave
        points += 200
    
    # UI points and level indicators
    text("Points: " + str(points), 10, 40)
    text("Level: " + str(level), 10, 70)

#--------------------

# ENEMY GENERATION
def generate_enemies(num_enemies):
    global enemy_id, next_enemy_spawn_time, level
    
    current_time = millis()
    
    if len(enemies) < num_enemies and current_time > next_enemy_spawn_time:
        pos_x = random.randint(50, 750)
        enemies[enemy_id] = Enemy(enemy_id, pos_x, -50)
        enemy_id += 1
        
        next_enemy_spawn_time = current_time + random.randint(500, 1500)

# RENDER ENEMIES
def render_enemy_worms():
    global enemies, shots, points, hit_count, enemy_id, game_over, level
    
    # Sine wave constants
    a = 0.1 # Adjusts wave speed
    b = 20  # Adjusts wave amplitude
    
    for eny in list(enemies.keys()):
        enemies[eny].sin_count += a
        # Render enemy worm segments
        fill(100, 255, 100)
        ellipse(enemies[eny].pos_x + math.sin(enemies[eny].sin_count) * b, enemies[eny].pos_y, 10, 10)
        ellipse(enemies[eny].pos_x + math.sin(enemies[eny].sin_count - 0.1) * b, enemies[eny].pos_y - 10, 8, 8)
        ellipse(enemies[eny].pos_x + math.sin(enemies[eny].sin_count - 0.2) * b, enemies[eny].pos_y - 18, 6, 6)
        ellipse(enemies[eny].pos_x + math.sin(enemies[eny].sin_count - 0.3) * b, enemies[eny].pos_y - 24, 4, 4)
        ellipse(enemies[eny].pos_x + math.sin(enemies[eny].sin_count - 0.4) * b, enemies[eny].pos_y - 28, 2, 2)
        fill(255, 200, 0)
        
        # Move enemy down
        enemies[eny].move_down()
        
        # Check for collisions with shots
        hit = False
        for shot_id in list(shots.keys()):
            if shots[shot_id].pos_x > enemies[eny].pos_x + math.sin(enemies[eny].sin_count) * b - 20 and shots[shot_id].pos_x < enemies[eny].pos_x + math.sin(enemies[eny].sin_count) * b + 20:
                if shots[shot_id].pos_y < enemies[eny].pos_y + 20 and shots[shot_id].pos_y > enemies[eny].pos_y - 20:
                    hit = True
        
        # Game over trigger
        if enemies[eny].pos_y > height + 28:
            del enemies[eny]
            game_over = True  
            break
        
        elif hit:
            del shots[shot_id]
            del enemies[eny]
            hit = False
            points += 50 + (3 * level)  # Increase points per hit here

# ENEMY CLASS
class Enemy:
    def __init__(self, id, pos_x, pos_y):
        self.id = id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.sin_count = 0
    
    def move_down(self):
        self.pos_y += 1 + (level * 0.2)  # Adjust speed of descent here

def create_enemy():
    global enemy_id
    enemies[enemy_id] = Enemy(enemy_id, random.randint(50, 750), 0)
    enemy_id += 1


# STARS
class Star:
    def __init__(self, id, pos_x, pos_y, speedfactor):
        self.id = id
        self.pos_y = pos_y
        self.pos_x = pos_x
        self.speed = speedfactor
        
    def move_down(self):
        self.pos_y += self.speed
        pass
        
        
def create_star(star_id):
    stars[star_id] = Star(star_id, random.randint(5, width-5), 0, random.uniform(0.1, 0.9))
    pass
    
def initiate_stars():
    global star_id
    # Initiate star background
    for y in range(1, height):
        starbirth = random.randint(1,11)
        if starbirth > 10:
            stars[star_id] = Star(star_id, random.randint(5, width-5), y, random.uniform(0.1, 0.9))
            star_id += 1
        
# LASER SHOTS
class Shot:
    def __init__(self, id, pos_x, pos_y, speed=10):
        self.id = id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed

    def move_up(self):
        self.pos_y -= self.speed  # Move the shot up

    def display(self):
        stroke(255, 0, 0)  # Laser color
        strokeWeight(4)
        line(self.pos_x, self.pos_y, self.pos_x, self.pos_y - 10)  # Draw laser line

def fire_shot():
    global shot_id
    # Create a new shot at center of the spaceship
    new_shot = Shot(shot_id, spaceship['x'], spaceship['y'] - 40)
    shots[shot_id] = new_shot
    shot_id += 1

# SPACESHIP
def draw_spaceship(x, y, thruster):
    # Draw the spaceship
    pushMatrix()
    translate(x, y)
    
    noStroke() 
    
    # Destructor laser cannons
    fill(200, 50, 50)
    rect(-20, -1, 5, 15) # Left
    rect(15, -1, 5, 15) # Right
    
    # Steering thruster flames
    if thruster == "to_right":
        fill(255, 200, 0)
        triangle(random.randint(-30, -20), 5, 10, 5, -10, 9)
        
    if thruster == "to_left":
        fill(255, 200, 0)
        triangle(random.randint(20, 30), 5, 10, 5, 10, 9)
    
    # Main body
    fill(150, 150, 255)
    beginShape()
    vertex(0, -40)   # Nose
    vertex(-20, 20)  # Left base
    vertex(20, 20)   # Right base
    endShape(CLOSE)
    
    # Cockpit
    fill(0, 200, 255)
    ellipse(0, -20, 15, 20)
    
    # Wings
    fill(150, 150, 255)
    beginShape() # Left wing
    vertex(-20, 10)   # base
    vertex(-40, 30)   # tip
    vertex(-15, 20)   # inner
    endShape(CLOSE)
    
    beginShape() # Right wing
    vertex(20, 10)   # base
    vertex(40, 30)   # tip
    vertex(15, 20)   # inner
    endShape(CLOSE)

    # Thrusters
    fill(255, 100, 100)
    rect(-10, 20, 8, 10)  # Left thruster
    rect(2, 20, 8, 10)    # Right thruster
    
    # Thruster flames
    fill(255, 200, 0)
    triangle(-8, 30, -4, 30, -6, random.randint(40, 60))  # Left flame
    triangle(4, 30, 8, 30, 6, random.randint(40, 60))      # Right flame
    
    popMatrix()

# Detect key press
def keyPressed():
    global move_left
    global move_right
    global shoot
    global points, level, enemies, shots, enemy_id, level_start_time
    if key == 'a':
        move_left = True 
    if key == 'd':
        move_right = True  
    if key == ' ':
        shoot = True
        
    # Restart game if R is pressed after game over
    if game_over and key == 'r':
        points = 0
        level = 0
        enemies.clear()
        shots.clear()
        enemy_id = 0
        level_start_time = millis()
        setup()  # Restart the game

# Detect key release
def keyReleased():
    global move_left
    global move_right
    global shoot
    if key == 'a':
        move_left = False
    if key == 'd':
        move_right = False 
    if key == ' ':
        shoot = False
