import pygame
Hoz = [(1, 0, 10), (-1, 0, 10)]
Ver = [(0, 1, 10), (0, -1, 10)]

class Player:
    def __init__(self, game, pos):
        self.pos = list(pos)
        self.color = 'green'
        self.game = game
        self.Vel = pygame.math.Vector2()
        self.path = []
        self.reachx = False
        self.reachy = False
    
    def update(self):
        if self.path:
            if round(self.path[0][0], 2) > round(self.pos[0], 2):
                self.Vel[0] = 1
            elif round(self.path[0][0], 2) < round(self.pos[0], 2):
                self.Vel[0] = -1
            else:
                self.Vel[0] = 0
            
            if round(self.path[0][1], 2) > round(self.pos[1], 2):
                self.Vel[1] = 1
            elif round(self.path[0][1], 2) < round(self.pos[1], 2):
                self.Vel[1] = -1
            else:
                self.Vel[1] = 0
            
            if self.Vel[0] == 0 and self.Vel[1] == 0:
                self.path.pop(0)

            self.Vel[0] *= 0.1
            self.Vel[1] *= 0.1

            self.pos[0] += self.Vel[0]
            self.pos[1] += self.Vel[1]

            self.pos[0] = round(self.pos[0], 2)
            self.pos[1] = round(self.pos[1], 2)

            
            
    
    def get_path(self, path):
        self.path = path.copy()
        self.path.reverse()


    def render(self, screen):
        size = self.game.Block_size
        surf = pygame.Surface((16,16))
        surf.fill(self.color)
        screen.blit(surf, (self.pos[0] * size, self.pos[1] * size))