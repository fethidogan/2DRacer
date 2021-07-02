import time
import pygame, sys, random
from pygame import mixer
pygame.init()

# Screen Settings
width, height = 600,600
screen = pygame.display.set_mode((width,height))
caption = pygame.display.set_caption("Racer")
FPS = pygame.time.Clock()

# Background
background = pygame.image.load("road.png")
background = pygame.transform.scale(background,(600,600))

class Car:
    # Car Attributes position speed crashed or not etc...
    def __init__(self):
        self.rec_x = 200
        self.rec_y = 450
        self.rec_velocity = 5
        self.new_car_size_x = 70
        self.new_car_size_y = 120
        self.crashed = False
    def draw_car(self):
        car = pygame.image.load("car_sprite.png")
        car = pygame.transform.scale(car,(self.new_car_size_x,self.new_car_size_y))
        screen.blit(car,(self.rec_x,self.rec_y))

class Speed:
    def __init__(self):
        self.kmh = 0
        self.random_car_velocity = 1

class Score:
    def __init__(self):
        self.score_val = 0
    def increase_score(self):
        font = pygame.font.Font("freesansbold.ttf", 20)
        score_text = font.render(f"Score : {self.score_val}", True, (255, 10, 0))
        screen.blit(score_text, (350, 10))

def main_loop():
    # objects
    car = Car()
    spd = Speed()
    scr = Score()

    # Random car image & Their Random generated positions
    random_car = pygame.image.load("random_car.png")
    random_car = pygame.transform.scale(random_car, (car.new_car_size_x-8, car.new_car_size_y-8))
    random_x = random.randint(140,220)
    random_2x = random.randint(220,400)
    random_car_start_pos = -250
    random_car2_start_pos = -150

    # Looped Toyota Supra Sound
    mixer.music.load("suprasound.mp3")
    mixer.music.play(loops=500)
    mixer.music.set_volume(0.3)

    # Main Loop
    while not car.crashed:
        pygame.display.update()
        FPS.tick(60)

        spd.kmh += 15
        # Slide car on screen for each while loop
        random_car_start_pos += spd.random_car_velocity
        random_car2_start_pos += spd.random_car_velocity

        # Handling Quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()

        # İf Keys pressed move the player car
        def movement():
            if keys[pygame.K_DOWN] and car.rec_y <= height-car.new_car_size_y:
                 car.rec_y += car.rec_velocity
            elif keys[pygame.K_UP] and car.rec_y > 0:
                car.rec_y -= car.rec_velocity
            elif keys[pygame.K_LEFT] and car.rec_x > width-(width*0.8):
                car.rec_x -= car.rec_velocity
            elif keys[pygame.K_RIGHT] and car.rec_x < width-(width*0.33):
                car.rec_x += car.rec_velocity

        # when score hits 500 1000 1500 ...... every true condition random generated car's speed will increase
        def increase_level():
            if scr.score_val % 500 == 0:
                spd.random_car_velocity += 2

        def check_crash():
            # Note 125 after rec_y is adding extra offset to car's Y position because of pygame image calculation
            # you can solve this reading this thread
            # https://stackoverflow.com/questions/51182185/pygame-how-to-get-an-image-in-the-center-of-the-screen
            # if car's Y position is bigger than random car start position
            if car.rec_y + 125 > random_car_start_pos:
                # calculating difference between car and random car's Y and X positions numbers are offsets
                if car.rec_y + 125 - random_car_start_pos < 238 and (car.rec_x + 60 - random_x > 1 and car.rec_x - 55 - random_x < 1) :
                    car.crashed = True
                    time.sleep(1)
                    main_loop()

            if car.rec_y + 125 > random_car2_start_pos:
                # calculating difference between car and random car's Y and X positions numbers are offsets
                if car.rec_y + 125 - random_car2_start_pos < 238 and (car.rec_x + 60 - random_2x > 1 and car.rec_x - 55 - random_2x < 1):
                    car.crashed = True
                    time.sleep(1)
                    main_loop()

        check_crash()
        # checking keys and moving the car
        movement()
        increase_level()

        # Looping Background
        screen.blit(background, (0, spd.kmh))
        screen.blit(background, (0,spd.kmh-height))
        if spd.kmh == height:
            spd.kmh = 0

        # Sliding car from top to bottom (off screen to off screen) check line 58
        screen.blit(random_car, (random_x, random_car_start_pos))
        screen.blit(random_car, (random_2x,random_car2_start_pos))

        # İf Random car goes off screen on Y axis
        if random_car_start_pos > height+350:
            random_car_start_pos = -250
            random_x = random.randint(110, 200)
        if random_car2_start_pos > height+350:
            random_car2_start_pos = -150
            random_2x = random.randint(220, 400)

        car.draw_car()
        scr.score_val += 1
        scr.increase_score()
        pygame.display.update()

main_loop()
