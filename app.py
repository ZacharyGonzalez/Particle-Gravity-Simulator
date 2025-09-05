import pygame
from scipy.constants import G
import math
import random

window_height = 720
window_width = 1080
BLACK = (0,0,0)
WHITE = (255,255,255)
DRAW_COLOR = WHITE
RADIUS = 3
MASS = 1
SMALL_FLOAT = 1e-300
clock = pygame.time.Clock()
SCALE = 1e8

class Particle:
    x:int
    y:int
    dx:int
    dy:int
    ax:int
    ay:int
    mass:int
    radius:int
    
    def __init__(self,x,y,r,m,vx,vy):
        self.x = x
        self.vx = vx

        self.y = y
        self.vy = vy

        self.radius = r
        self.mass = m

    def update_particle(self,others) -> None:
        """Compares list entries to all others, collecting particles that have collided, and accumulate gravitational forces on current particle.
        
        input: List of Particles
        """
        to_remove = []
        for other in others:
            if other is self or other in to_remove:
                continue
            dx = other.x - self.x
            dy = other.y - self.y
            distance = math.hypot(dx,dy)
            if distance <= (self.radius + other.radius)/2:                           # using half of the radius's so that collisions look more natural
                total_mass = self.mass + other.mass
                self.vx = (self.vx * self.mass + other.vx * other.mass) / total_mass
                self.vy = (self.vy * self.mass + other.vy * other.mass) / total_mass
                self.mass = total_mass
                self.radius = int(math.sqrt(self.radius**2 + other.radius**2))
                if self.radius < 3:
                    self.radius+=1
                to_remove.append(other)
                continue

            force = G * (self.mass * other.mass) / (distance**2)                     # TODO math.hypot can possibly return 0 since its just sqrt(x**2+y**2), should maybe add SMALL_FLOAT here for safety
            force *= SCALE                                                           # TODO need to make simulation feel better using smaller SCALE to be more realistic. SCALE < 1e7 is extremely slow

            ax = force*(dx/distance)/self.mass
            ay = force*(dy/distance)/self.mass

            self.vx +=ax
            self.vy +=ay
        for dead in to_remove:
            others.remove(dead)

    def update_position(self) -> None:
        self.bounds_check()
        self.x += self.vx
        self.y += self.vy
        
    def bounds_check(self) -> None:
        """This repositions a particle on the opposite border that it collides with, instead of bouncing the object"""
        # TODO Current implementation has incorrect jump positions, need to also swap opposite coordinate during an change (top right quadrant should alwasy go to the bottom left quadrant)
        limit = self.radius/2
        if self.x + limit >= window_width:
            self.x = 0 + self.radius
        elif self.x - limit <= 0:
            self.x = window_width-self.radius
        
        if self.y + limit >= window_height:
            self.y = 0 + self.radius
        elif self.y - limit <= 0:
            self.y = window_height - self.radius

    def draw(self,screen) -> None:
        pygame.draw.circle(screen,DRAW_COLOR,(int(self.x),int(self.y)),self.radius)

def update_screen() -> None:
    pygame.display.flip()

def create_particle(radius=RADIUS, mass=MASS, vx=0, vy=0) -> Particle:
    point_x, point_y = pygame.mouse.get_pos()
    particle = Particle(point_x, point_y, radius, mass,vx,vy)
    return particle

def run_simulation() -> None:
    pygame.init()
    screen = pygame.display.set_mode((window_width,window_height))
    screen.fill(BLACK)
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
            particle = create_particle(vx=random.randint(-1,1),vy=random.randint(-1,1))
            particles.append(particle)
        
        screen.fill(BLACK)

        for particle in particles:
            particle.update_particle(particles)
            particle.update_position()
            particle.draw(screen)

        update_screen()
        clock.tick(60) # higher clock tick rate makes higher SCALE feel better

if __name__ == "__main__":
    run_simulation()
