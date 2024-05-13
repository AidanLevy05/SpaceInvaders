import turtle
import random

# Consts
path_to_invader = r"path/to/invader"
path_to_ship = r"path/to/ship"
BOUNDARY_X = 462
BOUNDARY_Y = 412

text = turtle.Turtle()
textScore = turtle.Turtle()

fighters = []
lasers = []
bombs = []

MOVEMENT_SPEED = 10
play = False
paused = False
playerHealth = 100
y = 0
x = 0
score = 0

# ------------ Class declarations ------------ #

# Fighter class
class Fighter:
    def __init__(self, x, y, shape):
        self.turtle = turtle.Turtle()
        sc.addshape(shape)
        self.turtle.speed(0)
        self.turtle.hideturtle()
        self.turtle.penup()
        self.turtle.shape(shape)
        self.turtle.showturtle()
        self.turtle.color("white")
        self.turtle.goto(x, y)
        self.turtle.showturtle()

    def move_left(self):
        x = self.turtle.xcor()
        if x - MOVEMENT_SPEED > -BOUNDARY_X:
            self.turtle.setx(x - MOVEMENT_SPEED - random.randint(0, 100))

    def move_right(self):
        x = self.turtle.xcor()
        if x + MOVEMENT_SPEED < BOUNDARY_X:
            self.turtle.setx(x + MOVEMENT_SPEED + random.randint(0, 100))

    def move_up(self):
        y = self.turtle.ycor()
        if y + MOVEMENT_SPEED < BOUNDARY_Y:
            self.turtle.sety(y + MOVEMENT_SPEED + random.randint(0, 100))

    def move_down(self):
        y = self.turtle.ycor()
        if y - MOVEMENT_SPEED > -BOUNDARY_Y:
            self.turtle.sety(y - MOVEMENT_SPEED - random.randint(0, 100))

    def maybe_shoot(self):
        if random.randint(1, 20) == 1:
            new_bomb = Bomb(self.turtle.xcor(), self.turtle.ycor() - 20)
            bombs.append(new_bomb)

    def move_towards_player(self, player_x, player_y):
        step_size = MOVEMENT_SPEED / 4
        x = self.turtle.xcor()
        y = self.turtle.ycor()
        if x < player_x:
            x += step_size
        elif x > player_x:
            x -= step_size
        if y > player_y:
            y -= step_size
        self.turtle.goto(x,y)

    def clear(self):
        self.turtle.clear()
        self.turtle.hideturtle()

# Laser class
class Laser:
    def __init__(self, x, y):
        self.laser = turtle.Turtle()
        self.laser.hideturtle()
        self.laser.penup()
        self.laser.color('red')
        self.laser.shape('square')
        self.laser.shapesize(0.5, 1.5)
        self.laser.speed(0)
        self.laser.goto(x,y)
        self.laser.showturtle()
        self.laser.setheading(90)

    def move(self):
        if self.laser.ycor() < BOUNDARY_Y:
            self.laser.sety(self.laser.ycor() + 25)
        else:
            self.laser.hideturtle()
            lasers.remove(self)

    def clear(self):
        self.laser.clear()
        self.laser.hideturtle()

# Bomb
class Bomb:
    def __init__(self, x, y):
        self.bomb = turtle.Turtle()
        self.bomb.hideturtle()
        self.bomb.penup()
        self.bomb.color('yellow')
        self.bomb.shape('circle')
        self.bomb.turtlesize(stretch_wid=1.5, stretch_len=1.5, outline=1)
        self.bomb.speed(0)
        self.bomb.goto(x, y)
        self.bomb.showturtle()
        self.bomb.setheading(-90)

    def move(self):
        if self.bomb.ycor() > -BOUNDARY_Y:
            self.bomb.sety(self.bomb.ycor() - 25)
        else:
            self.bomb.hideturtle()
            bombs.remove(self)

    def clear(self):
        self.bomb.clear()
        self.bomb.hideturtle()

# Invader generation
def create_fighter():
    f = Fighter(random.randint(-450, 450), random.randint(200, 450), path_to_invader)
    fighters.append(f)
    sc.ontimer(create_fighter, random.randint(2000,5000))

# Get screen
sc = turtle.Screen()
sc.title("Space Invaders")
sc.bgcolor("black")
sc.setup(width=1000, height=900)

# Create space invader
sc.addshape(path_to_ship)
player = turtle.Turtle()
player.shape(path_to_ship)
player.penup()
player.speed(0)
player.goto(0,-300)

# ------------ Game Updating ------------ #

def update_game():
    global score, playerHealth

    if paused:
        return
    
    # Make invaders move
    # Look for collisions
    for fighter in fighters[:]:
        fighter.move_towards_player(player.xcor(), player.ycor())
        if is_collision(fighter.turtle, player):
            print("Player was hit by invader!")

            if playerHealth - 5 < 0:
                playerHealth = 0
            else:
                playerHealth -= 5

            update_score_display()

    # Lists to track bombs
    for bomb in bombs[:]:
        bomb.move()

    # Lists to track bombs
    for bomb in bombs[:]:
        bomb.move()

    # Lists to track items to remove
    lasers_to_remove = []
    fighters_to_remove = []
    bombs_to_remove = []

    for laser in lasers[:]:  # Iterate over a copy of the lasers list
        laser.move()
        
        for fighter in fighters[:]:  # Iterate over a copy of the fighters list
            fighter.maybe_shoot()

            # Check laser - figher collision
            if is_collision(laser.laser, fighter.turtle):
                print("Hit detected!")
                score += 1
                update_score_display()
                laser.clear()
                fighter.clear()

                # Mark these items for removal
                lasers_to_remove.append(laser)
                fighters_to_remove.append(fighter)
                break  # Stop checking other fighters if one is hit

        # Look if bombs hit the player
        for bomb in bombs[:]:
            if is_collision(bomb.bomb, player):
                print("Player hit!")

                if playerHealth - 20 < 0:
                    playerHealth = 0
                else:
                    playerHealth -= 20

                update_score_display()
                bomb.clear()

                # Mark these items for removal
                bombs_to_remove.append(bomb)
                break

    # Remove the marked items outside of the loop
    for laser in lasers_to_remove:
        if laser in lasers:
            lasers.remove(laser)

    for fighter in fighters_to_remove:
        if fighter in fighters:
            fighters.remove(fighter)

    for bomb in bombs_to_remove:
        if bomb in bombs:
            bombs.remove(bomb)

    # Lose validation
    if check_game_over():
        return

    sc.update()
    sc.ontimer(update_game, 10)

# ------------ Text ------------ #

def starttext():
    text.color("white")
    text.penup()
    text.goto(0,0)
    text.write("Press ENTER to start!", align="center", font=("Arial", 24, "normal"))
    text.hideturtle()

def printStats():
    textScore.color("white")
    textScore.speed(0)
    textScore.hideturtle()
    textScore.penup()
    textScore.goto(0,350)
    textScore.write(f"Score: {score}\nHealth: {playerHealth}", align="center", font=("Arial", 24, "normal"))
    textScore.hideturtle()

def start():
    global play
    text.clear()
    play = True
    printStats()
    create_fighter()
    update_game()

    # Key presses
    sc.onkeypress(left, "Left")
    sc.onkeypress(left, "a")

    sc.onkeypress(right, "Right")
    sc.onkeypress(right, "d")

    sc.onkeypress(up, "Up")
    sc.onkeypress(up, "w")

    sc.onkeypress(down, "Down")
    sc.onkeypress(down, "s")

    sc.onkeypress(shoot, "space")

    sc.onkeypress(pause, "Escape")

# ------------ Movement ------------ #

# Movement
def left():
    x = player.xcor()
    if x - MOVEMENT_SPEED > -BOUNDARY_X:
        player.setx(x - MOVEMENT_SPEED)

def right():
    x = player.xcor()
    if x + MOVEMENT_SPEED < BOUNDARY_X:
        player.setx(x + MOVEMENT_SPEED)

def up():
    y = player.ycor()
    if y + MOVEMENT_SPEED < BOUNDARY_Y:
        player.sety(y + MOVEMENT_SPEED)

def down():
    y = player.ycor()
    if y - MOVEMENT_SPEED > -BOUNDARY_Y:
        player.sety(y - MOVEMENT_SPEED)

# ------------ Functionality ------------ #

# Pause
def pause():
    global paused
    paused = not paused

    if paused:
        text.clear()
        text.color("white")
        text.penup()
        text.goto(0,0)
        text.write("Paused", align="center", font=("Arial", 36, "normal"))
        text.hideturtle()
        sc.update()
    else:
        text.clear()


# Laser firing
def shoot():
    x = player.xcor()
    y = player.ycor() + 15

    new_laser = Laser(x, y)
    lasers.append(new_laser)

# Look for collision
def is_collision(obj1, obj2):
    distance = obj1.distance(obj2)
    if distance <= 30:
        return True
    return False

# Check if player died
def check_game_over():
    global playerHealth
    if playerHealth <= 0:
        text.clear()
        text.color("red")
        text.penup()
        text.goto(0,0)
        text.write(f"Game Over!\nScore: {playerHealth}", align="center", font=("Arial", 36, "normal"))
        text.hideturtle()
        sc.update()
        return True
    return False

# Update score
def update_score_display():
    textScore.clear()
    textScore.write(f"Score: {score}\nHealth: {playerHealth}", align="center", font=("Arial", 24, "normal"))

# ------------ Key listening ------------ #

# Intro screen
starttext()
sc.listen()
sc.onkeypress(start, "Return")

sc.mainloop()
