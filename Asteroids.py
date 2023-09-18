import pygame
import sys
from pygame.locals import *
import random
import math

pygame.init()  # initialize pygame

#initialzize the background image
screenwidth, screenheight = (1000, 720)
screen = pygame.display.set_mode((screenwidth, screenheight))
picture = pygame.image.load('space_background.webp')
bg = pygame.transform.scale(picture, (screenwidth, screenheight))
pygame.display.set_caption('Asteroids by Liam McCarthy')
font = pygame.font.Font(None, 36)

#class to control the player's ship
class PlayerShip:
    def __init__(self):
        self.shape = pygame.transform.scale(pygame.image.load('spaceship.png'), (100,100))
        self.angle = 0
        self.velocity = 0
        self.x = 450
        self.y = 300
        self.lives = 3

        self.center = self.shape.get_rect(center = (self.x, self.y)).center 

    #function to display the PlayerShip on the game screen
    def show(self, surface):
        rotated_image = pygame.transform.rotate(self.shape, self.angle)
        new_rect = rotated_image.get_rect(center = self.shape.get_rect(topleft = (self.x, self.y)).center)
        surface.blit(rotated_image, new_rect)

    #function to reset the game
    def game_reset(self):
        self. x = 450
        self.y = 300
        self.lives = 3
        self.angle = 0
        self.velocity = 0  

    #function to update PlayerShip when it is hit
    def ship_hit(self):
        self. x = 450
        self.y = 300
        self.lives -= 1
        self.angle = 0
        self.velocity = 0  

    #function to update the coordinates of the PlayerShip
    def updateCoords(self):
        #increment the PlayerShip's x and y coordinates
        self.x += math.cos((-self.angle - 90) * 0.0174533) * self.velocity
        self.y += math.sin((self.angle - 90) * 0.0174533) * self.velocity
        
        #PlayerShip appears on other side of screen if it leaves x-axis
        if self.x <= -50:
            self.x = screenwidth + 20
        elif self.x >= screenwidth + 50:
            self.x = -50
        
        #Playership appears on top or bottom of screen if it leaves y-axis
        if self.y <= -50:
            self.y = screenheight + 20
        elif self.y >= screenheight + 50:
            self.y = -50

        #constantly reduce the PlayerShip's velocity
        if self.velocity > 0:
            self.velocity -= 0.08

    #function to update PlayerShip coordinates on each clock tick
    def turnLeft(self):
        if self.angle >= 360:
            self.angle = 0
        elif self.angle <= -360:
            self.angle = 0
        self.angle += 5
        
    #function to update PlayerShip coordinates on each clock tick
    def turnRight(self):
        if self.angle >= 360:
            self.angle -= 360
        elif self.angle <= -360:
            self.angle += 360
        self.angle -= 5

    #function to increase the PlayerShip's velocity
    def accelerate(self):
        if self.velocity <= 8:
            self.velocity += 0.8

#class to control the player's lasers
class Laser:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.active = False
        self.shape = pygame.transform.scale(pygame.image.load('projectile.png'), (20,50))
        self.speed = 10

    #function to show the laser on the game screen
    def show(self, surface):
        if self.active == True:
            rotated_image = pygame.transform.rotate(self.shape, self.angle)
            new_rect = rotated_image.get_rect(center = self.shape.get_rect(topleft = (self.x + 38, self.y + 21)).center)
            surface.blit(rotated_image, new_rect)

    #function to fire a Laser from the PlayerShip
    def fire(self, x, y, angle):
        self.active = True
        self.angle = angle
        self.x = x + 45 * math.cos((-angle - 90) * 0.0174533)
        self.y = y + 45 * math.sin((-angle - 90) * 0.0174533)

    #function to move the laser up on the screen
    def updateCoords(self):  
        self.x += math.cos((-self.angle - 90) * 0.0174533) * self.speed
        self.y += math.sin((self.angle - 90) * 0.0174533) * self.speed

        #deactivates Laser if it leaves the screen
        if self.x <= -50 or self.x >= screenwidth:
            self.active = False
        if self.y <= -50 or self.y >= screenheight:
            self.active = False

    #function to check if the laser collides with an enemy
    def checkCollision(self, enemy_x, enemy_y, enemy_size, enemy_alive):
        if abs(enemy_x - self.x) < (enemy_size / 2) and abs(self.y - enemy_y) < (enemy_size / 2) and enemy_alive == True and self.active == True:
            return True

#class to control the player's Cannon (group of Lasers)
class Cannon:
    def __init__(self, x, y, angle):
        self.lasers = [Laser(x, y, angle),
                       Laser(x, y, angle),
                       Laser(x, y, angle),
                       Laser(x, y, angle),
                       Laser(x, y, angle)]

    #function to show each active Laser
    def show(self, surface):
        for laser in self.lasers:
            if laser.active == True:
                rotated_image = pygame.transform.rotate(laser.shape, laser.angle)
                new_rect = rotated_image.get_rect(center = laser.shape.get_rect(topleft = (laser.x + 38, laser.y + 21)).center)
                surface.blit(rotated_image, new_rect)
                laser.updateCoords()

    #function to fire a Laser from the Cannon
    def fire(self, x, y, angle):
        for i in range(1,3):
            if self.lasers[0].active == False:
                self.lasers[0].fire(x, y, angle)
                break
            if self.lasers[i].active == False and self.lasers[i - 1].active == True:
                self.lasers[i].fire(x, y, angle)
                break

#class to control an Asteroid
class Asteroid:
    def __init__(self, size, x, y, speed = 2):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.angle = random.randrange(0, 360)
        self.active = True
        self.shape = pygame.transform.scale(pygame.image.load('asteroid.png'), (self.size, self.size))

    #function to show an Asteroid
    def show(self, surface):
        if self.active == True and self.size >= 60:
            surface.blit(self.shape, (self.x, self.y))

    #function to update the coordinates of an Asteroid
    def updateCoords(self):
        self.x += math.cos((-self.angle - 90) * 0.0174533) * self.speed
        self.y += math.sin((self.angle - 90) * 0.0174533) * self.speed

        #Asteroid appears on opposite side of screen when it leaves bounds
        if self.x <= -100:
            self.x = screenwidth + 20
        elif self.x >= screenwidth + 100:
            self.x = -50
        if self.y <= -100:
            self.y = screenheight + 20
        elif self.y >= screenheight + 100:
            self.y = -50

    #function to determine if an EnemyShip is touching a PlayerShip
    def touchingPlayer(self, player_x, player_y):
        if abs(self.x - player_x) < self.size / 2 and abs(self.y - player_y) < self.size / 2 and self.active == True and self.size >= 60:
            return True

#class to control a group of Asteroids
class Asteroid_Cluster:
    def __init__(self):
        self.asteroids = []
        self.size = 5

    #function to show each Asteroid in the Asteroid_Cluster
    def show(self, surface):
        for asteroid in self.asteroids:
            asteroid.show(surface)

    #function to create a group of Asteroids    
    def makeAsteroids(self):
        self.asteroids = []
        for i in range(self.size):
            self.asteroids.append(Asteroid(100, random.randrange(0, 1000), random.randrange(-100, 100)))
        self.size = 5

    #function to update the coordinates of each Asteroid
    def updateCoords(self):
        for asteroid in self.asteroids:
            asteroid.updateCoords()

    #function to remove an Asteroid from the Asteroid_Cluster
    def destroy(self, asteroid, size, x, y, speed):
        screen.blit(pygame.transform.scale(pygame.image.load('ship_explosion.png'), (size, size)), (x, y))
        pygame.display.update()
        if asteroid.size > 60:
            self.asteroids.remove(asteroid)
            self.asteroids.append(Asteroid(size - 20, x, y, speed + 1.5))
            self.asteroids.append(Asteroid(size - 20, x, y, speed + 1.5))
        else:
            self.asteroids.remove(asteroid)

#function to draw a starting menu that greets the player and provides game instructions
def draw_start_menu():
    screen.fill((15, 15, 15))
    font = pygame.font.SysFont('arial', 190)
    mediumFont = pygame.font.SysFont('arial', 50)
    smallFont = pygame.font.SysFont('arial', 30)
    title = font.render('ASTEROIDS', True, (255, 255, 0))
    start_button = mediumFont.render('Press [SPACE] to start', True, (255, 255, 0))
    instructions1 = smallFont.render('Press left and right arrows to rotate the ship and the', True, (255, 255, 255))
    instructions2 = smallFont.render('up arrow to accelerate. Press space to shoot the asteroids.', True, (255, 255, 255))
    instructions3 = smallFont.render('Destroy all the asteroids and avoid being hit to clear each level.', True, (255, 255, 255))
    screen.blit(title, (screenwidth/2 - title.get_width()/2, 50))
    screen.blit(start_button, (screenwidth/2 - start_button.get_width()/2, 400))
    screen.blit(instructions1, (screenwidth/2 - instructions1.get_width()/2, 250))
    screen.blit(instructions2, (screenwidth/2 - instructions2.get_width()/2, 280))
    screen.blit(instructions3, (screenwidth/2 - instructions3.get_width()/2, 310))
    comet = pygame.transform.scale(pygame.image.load('comet.png'), (200, 200))
    ship = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('spaceship.png'), (200, 200)), -50)
    screen.blit(ship, (300, 450))
    screen.blit(comet, (800, 100))
    pygame.display.update()

#function to draw a screen that appears between game levels
def draw_next_level(score, lives):
    screen.fill((15, 15, 15))
    font = pygame.font.SysFont('arial', 60)
    title = font.render('Press [SPACE] to destroy more asteroids!', True, (255, 255, 0))
    show_score = font.render(f'Score: {score}', True, (255, 255, 0))
    show_lives = font.render(f'Lives Remaining: {lives}', True, (255, 255, 0))
    comet = pygame.transform.scale(pygame.image.load('comet.png'), (300, 300))
    ship = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('spaceship.png'), (300, 300)), -50)
    laser = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('projectile.png'), (100, 150)), -50)
    screen.blit(title, (screenwidth/2 - title.get_width()/2, 200 - title.get_height()/2))
    screen.blit(show_score, (screenwidth/2 - show_score.get_width()/2, 200 + show_score.get_height()/2))
    screen.blit(show_lives, (screenwidth/2 - show_lives.get_width()/2, 200 + show_score.get_height() + show_lives.get_height()/2))
    screen.blit(comet, (800, -100))  
    screen.blit(comet, (750, 200)) 
    screen.blit(comet, (400, -100)) 
    screen.blit(ship, (100, 450)) 
    screen.blit(laser, (400, 420)) 
    pygame.display.update()

#function to draw a game over screen
def draw_game_over_screen(score):
    screen.fill((0, 0, 0))
    # image = pygame.transform.scale(pygame.image.load("game_over.png"), (1000,500))
    # screen.blit(image, (0, 50))
    bigFont = pygame.font.SysFont('arial', 200)
    font = pygame.font.SysFont('arial', 100)
    smallFont = pygame.font.SysFont('arial', 60)
    game_over = bigFont.render(f'GAME OVER', True, (255, 255, 0))
    show_score = font.render(f'Score: {score}', True, (255, 255, 0))
    try_again = smallFont.render('Press [SPACE] to try again!', True, (255, 255, 0))
    astronaut = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('astronaut.png'), (100,100)), 30)
    explosion = pygame.transform.scale(pygame.image.load('ship_explosion.png'), (200, 200))
    ship = pygame.transform.scale(pygame.image.load('spaceship.png'), (200, 200))
    screen.blit(game_over, (screenwidth/2 - game_over.get_width()/2, 50))
    screen.blit(show_score, (screenwidth/2 - show_score.get_width()/2, 300))
    screen.blit(try_again, (screenwidth/2 - try_again.get_width()/2, 400))
    screen.blit(astronaut, (350, 600))
    screen.blit(ship, (500, 530))
    screen.blit(explosion, (500, 550))
    pygame.display.update()   
    

# intialize the starting variables for the game
Player = PlayerShip()
Cannon = Cannon(Player.x, Player.y, Player.angle)
Asteroids = Asteroid_Cluster()
Asteroids.makeAsteroids()
game_state = "startMenu"
score = 0

while True:

    #allow the user to exit the game by pressing the 'X' button
    for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    Cannon.fire(Player.x, Player.y, Player.angle)
            if event.type == pygame.QUIT:
                sys.exit()

    #initialize keys
    keys = pygame.key.get_pressed()

    #show the game's start menu
    if game_state == "startMenu":
        draw_start_menu()
        if keys[pygame.K_SPACE]:
            game_state = "game"

    #show the game's end screen
    if game_state == "gameOver":
        draw_game_over_screen(score)
        if keys[pygame.K_SPACE]:
            score = 0
            Player.game_reset()     
            Asteroids.makeAsteroids()
            game_state = "game"

    #show the completed level screen
    if game_state == "nextLevel":
        draw_next_level(score, Player.lives)
        if keys[pygame.K_SPACE]:
            score = 0
            Player.game_reset()     
            Asteroids.makeAsteroids()
            game_state = "game"

    #show the game screen
    if game_state == "game":
        #show the game elements on the screen
        pygame.time.wait(25)
        screen.blit(bg, (0, 0))
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        lives_text = font.render(f'Lives: {Player.lives}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10)) 
        screen.blit(lives_text, (10, 30))   

        #control the behavior of the Asteroid_Cluster
        for asteroid in Asteroids.asteroids:
            #check if any Lasers are colliding with an Asteroid
            for laser in Cannon.lasers:
                if laser.checkCollision(asteroid.x, asteroid.y, asteroid.size, asteroid.active):
                    if asteroid.size >= 40:
                        asteroid.active = False
                        laser.active = False
                        Asteroids.destroy(asteroid, asteroid.size, asteroid.x, asteroid.y, asteroid.speed)
                    if asteroid.size == 100:
                        score += 10
                    elif asteroid.size == 80:
                        score += 20
                    elif asteroid.size == 60:
                        score += 50
            #check if any Asteroids are hitting the PlayerShip
            if asteroid.touchingPlayer(Player.x, Player.y):
                Player.ship_hit()
                Asteroids.destroy(asteroid, asteroid.size, asteroid.x, asteroid.y, asteroid.speed)

        #end the game if the player is out of lives
        if Player.lives == 0:
            game_state = "gameOver"

        #clear level if there are no more Asteroids
        if len(Asteroids.asteroids) == 0:
            game_state = "nextLevel"

        #display the player and enemies
        Player.show(screen)    
        Player.updateCoords()
        Cannon.show(screen)
        Asteroids.show(screen)
        Asteroids.updateCoords()

        

        # if left arrow key is pressed
        if keys[pygame.K_LEFT]:
            # decrement in x co-ordinate
            Player.turnLeft()
            
        # if left arrow key is pressed
        if keys[pygame.K_RIGHT]:   
            # increment in x co-ordinate
            Player.turnRight()

        if keys[pygame.K_UP] :
            Player.accelerate()


        #update the game
        pygame.display.update()
