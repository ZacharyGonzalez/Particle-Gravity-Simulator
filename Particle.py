import math
from scipy.constants import G
SCALE = 1
class Particle:
    """Currently only contains update_particle and update_position"""
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
            distance = (math.dist((self.x,self.y),(other.x,other.y)))
            if distance > self.radius*3:
                continue
            if distance <= (self.radius + other.radius):
                total_mass = self.mass + other.mass
                self.vx = (self.vx * self.mass + other.vx * other.mass) / total_mass
                self.vy = (self.vy * self.mass + other.vy * other.mass) / total_mass
                self.mass = total_mass
                self.radius = int(math.sqrt(self.radius**2 + other.radius**2))
                to_remove.append(other)
                continue

            force = G * (self.mass * other.mass) / (distance**2)                     # TODO math.hypot can possibly return 0 since its just sqrt(x**2+y**2), should maybe add SMALL_FLOAT here for safety
            force *= SCALE                                                           # TODO need to make simulation feel better using smaller SCALE to be more realistic. SCALE < 1e7 is extremely slow

            ax = force*(dx/distance)/self.mass
            ay = force*(dy/distance)/self.mass

            self.vx += ax
            self.vy += ay
        for dead in to_remove:
            others.remove(dead)
        
        pass
    def update_position(self) -> None:
        
        self.x += self.vx
        self.y += self.vy
        
