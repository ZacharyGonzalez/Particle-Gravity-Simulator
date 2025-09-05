import pygame

clock = pygame.time.Clock()

class SimScreen:
    def __init__(self, width=1080, height=720):
        self.window_height = height
        self.window_width = width
        self.window_size = ((self.window_width,self.window_height))
        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)

    def bounds_check(self, particle) -> None:
        """This repositions a particle on the opposite border that it collides with, instead of bouncing the object"""
        # TODO Current implementation has incorrect jump positions, need to also swap opposite coordinate during an change (top right quadrant should alwasy go to the bottom left quadrant)
        limit = particle.radius/2
        if particle.x + limit >= self.window_width:
            particle.x = 0 + particle.radius
        elif particle.x - limit <= 0:
            particle.x = self.window_width-particle.radius
        
        if particle.y + limit >= self.window_height:
            particle.y = 0 + particle.radius
        elif particle.y - limit <= 0:
            particle.y = self.window_height - particle.radius

    def bounds_check_diff(self, particle) -> None:
        # TODO Current implementation has incorrect jump positions, need to also swap opposite coordinate during an change (top right quadrant should alwasy go to the bottom left quadrant)
        limit = particle.radius/2
        if particle.x + limit >= self.window_width or particle.x - limit <= 0:
            particle.vx= -particle.vx            
        if particle.y + limit >= self.window_height or particle.y - limit <= 0:
            particle.vy = -particle.vy
    
    def draw_particle(self, screen, particle, draw_color):
        pygame.draw.circle(screen,draw_color,(int(particle.x),int(particle.y)),particle.radius)
        self.draw_direction(screen,particle)

    def draw_direction(self, screen, particle):
        scale = 20  # just a multiplier so we can actually see the line
        end_x = particle.x + particle.vx * scale
        end_y = particle.y + particle.vy * scale
        pygame.draw.line(screen, (255, 255, 255), (particle.x, particle.y), (end_x, end_y))
        
    def update(self) -> None:
        pygame.display.flip()
    
    def fill(self, COLOR):
        self.screen.fill(COLOR)

    def get_screen(self):
        return self.screen
