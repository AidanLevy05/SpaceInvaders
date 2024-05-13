import turtle
import random

# Consts
path_to_invader = r"C:/Users/aidan/OneDrive/Documents/Code/Python/Projects/Space Invaders/sprite.gif"
path_to_ship = r"C:/Users/aidan/OneDrive/Documents/Code/Python/Projects/Space Invaders/ship.gif"
BOUNDARY_X = 462
BOUNDARY_Y = 412

text = turtle.Turtle()
textScore = turtle.Turtle()

fighters = []
lasers = []
bombs = []

MOVEMENT_SPEED = 10
play = False
playerHealth = 100
y = 0
x = 0
score = 0

# Fighter class
class Fighter:
    def __init__(self, x, y, shape):
        self.turtle = turtle.Turtle()
        sc.addshape(shape)
        self.turtle.shape(shape)
        self.turtle.showturtle()
        self.turtle.color("white")
        self.turtle.penup()
        self.turtle.speed(0)
        self.turtle.goto(x, y)

    def move_left(self):
        x = self.turtle.xcor()
        if x - MOVEMENT_SPEED > -BOUNDARY_X:
            self.turtle.setx(x - MOVEMENT_SPEED)

    def move_right(self):
        x = self.turtle.xcor()
        if x + MOVEMENT_SPEED < BOUNDARY_X:
            self.turtle.setx(x + MOVEMENT_SPEED)

    def move_up(self):
        y = self.turtle.ycor()
        if y + MOVEMENT_SPEED < BOUNDARY_Y:
            self.turtle.sety(y + MOVEMENT_SPEED)

    def move_down(self):
        y = self.turtle.ycor()
        if y - MOVEMENT_SPEED > -BOUNDARY_Y:
            self.turtle.sety(y - MOVEMENT_SPEED)

    def maybe_shoot(self):
        if random.randint(1, 20) == 1:
            new_bomb = Bomb(self.turtle.xcor(), self.turtle.ycor() - 20)
            bombs.append(new_bomb)

# Laser class
class Laser:
    def __init__(self, x, y):
        self.laser = turtle.Turtle()
        self.laser.color('red')
        self.laser.shape('square')
        self.laser.shapesize(0.5, 1.5)
        self.laser.penup()
        self.laser.speed(0)
        self.laser.goto(x,y)
        self.laser.setheading(90)

    def move(self):
        if self.laser.ycor() < BOUNDARY_Y:
            self.laser.sety(self.laser.ycor() + 20)
        else:
            self.laser.hideturtle()
            lasers.remove(self)

# Bomb
class Bomb:
    def __init__(self, x, y):
        self.bomb = turtle.Turtle()
        self.bomb.color('yellow')
        self.bomb.shape('circle')
        self.bomb.penup()
        self.bomb.speed(0)
        self.bomb.goto(x, y)
        self.bomb.setheading(-90)

    def move(self):
        if self.bomb.ycor() > -BOUNDARY_Y:
            self.bomb.sety(self.bomb.ycor() - 20)
        else:
            self.bomb.hideturtle()
            bombs.remove(self)

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

def update_game():
    global score

    # Lists to track bombs
    for bomb in bombs[:]:
        bomb.move()

    # Lists to track items to remove
    lasers_to_remove = []
    fighters_to_remove = []

    for laser in lasers[:]:  # Iterate over a copy of the lasers list
        laser.move()
        
        for fighter in fighters[:]:  # Iterate over a copy of the fighters list
            fighter.maybe_shoot()
            if is_collision(laser.laser, fighter.turtle):
                print("Hit detected!")
                score += 1
                update_score_display()
                laser.laser.hideturtle()
                fighter.turtle.hideturtle()

                # Mark these items for removal
                lasers_to_remove.append(laser)
                fighters_to_remove.append(fighter)
                break  # Stop checking other fighters if one is hit

    # Remove the marked items outside of the loop
    for laser in lasers_to_remove:
        if laser in lasers:
            lasers.remove(laser)

    for fighter in fighters_to_remove:
        if fighter in fighters:
            fighters.remove(fighter)

    sc.update()
    sc.ontimer(update_game, 50)

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

# Laser firing
def shoot():
    x = player.xcor()
    y = player.ycor() + 10

    new_laser = Laser(x, y)
    lasers.append(new_laser)

# Look for collision
def is_collision(obj1, obj2):
    distance = obj1.distance(obj2)
    if distance < 35:
        return True
    return False

# Update score
def update_score_display():
    textScore.clear()
    textScore.write(f"Score: {score}\nHealth: {playerHealth}", align="center", font=("Arial", 24, "normal"))

# Intro screen
starttext()
sc.listen()
sc.onkeypress(start, "Return")

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

sc.mainloop()