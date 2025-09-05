import random
from Particle import Particle
from Screen import SimScreen 
import pygame 

RADIUS = 3
MASS = 10
SMALL_FLOAT = 1e-300
BLACK = (0,0,0)
WHITE = (255,255,255)
DRAW_COLOR = WHITE



def create_particle(radius=RADIUS, mass=MASS, vx=0, vy=0,draw_color=DRAW_COLOR) -> Particle:
    point_x, point_y = pygame.mouse.get_pos()
    particle = Particle(point_x, point_y, radius, mass,vx,vy)
    return particle

def run_simulation() -> None:
    screen = SimScreen(1900,1080)
    screen.fill(COLOR=BLACK)
    window = screen.get_screen()
    repeat = True
    particles = []

    while repeat:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                repeat = False

            """
            if event.type == pygame.MOUSEBUTTONDOWN:
                particle = create_particle(vx=random.randint(-1,1),vy=random.randint(-1,1))
                particles.append(particle)
            """ 
        # not using the event.type so that i can spawn them repeatedly with a single press
        if pygame.mouse.get_pressed()[0]: 
            particle = create_particle(vx=random.randint(-1,1),vy=random.randint(-1,1), mass=random.randint(1,10000000))

            particles.append(particle)
        
        screen.fill(BLACK)

        for particle in particles:
            particle.update_particle(particles)
            screen.bounds_check_diff(particle)
            particle.update_position()
            color = (min(particle.mass, 255), 150, 150) 
            screen.draw_particle(window, particle, draw_color = color)
        screen.update()

if __name__ == "__main__":
    run_simulation()

    
