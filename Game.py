import pygame, sys
from Player import Player
from Algo import ASearch, Draw_open, Draw_close
import concurrent.futures

Collision = ['Wall']
Checking = [(1, 0, 10), (-1, 0, 10), (0, 1, 10), (0, -1, 10)]

class Game:
    def __init__(self):
        self.Block_size = 16
        self.Block= {

        }
        self.hand = 0
        self.end = 0
        self.start = 0

        self.Player =  []
        self.END_aw = []

        self.path = []
        self.screen = pygame.Surface((screen_w, screen_h))

        self.time = 0

    def update(self):
        self.screen.fill('grey')
        self.Draw_grid('white')

        mouse_pos = pygame.mouse.get_pos()
        mouse_loco = [int(mouse_pos[0] / self.Block_size), int(mouse_pos[1] / self.Block_size)]
        mouse_locostr = str(mouse_loco[0]) + ',' + str(mouse_loco[1])

        if mouse_pos[0] <= screen_w:
            # print(self.Around(mouse_loco))
            if clicking:
                if self.hand == 2:
                    self.Block[mouse_locostr] = {'type' : 'Wall' , 'Color' : 'black', 'Pos' : (mouse_loco[0], mouse_loco[1])}
                elif self.hand == 1:
                    if self.end == 0:
                        self.Block[mouse_locostr] = {'type' : 'End' , 'Color' : 'red', 'Pos' : (mouse_loco[0], mouse_loco[1])}
                        self.END_aw.append(list(mouse_loco))
                        self.end += 1
                    else:
                        self.END_aw.clear()

                        #EXTRACTING THE END BLOCK
                        for i in self.Block.copy():
                            if self.Block[i]['type'] == 'End':
                                del self.Block[i]

                        self.Block[mouse_locostr] = {'type' : 'End' , 'Color' : 'red', 'Pos' : (mouse_loco[0], mouse_loco[1])}
                        self.END_aw.append(list(mouse_loco))
                elif self.hand == 0 and self.start == 0:
                    self.start += 1
                    self.Player.append(Player(self, mouse_loco))

            if right_click:
                if mouse_locostr in self.Block:
                    if self.Block[mouse_locostr]['type'] == 'End':
                        self.end = 0
                        self.END_aw.clear()
                    del self.Block[mouse_locostr]
                for i in self.Player.copy():
                    if not i.path:
                        if mouse_loco[0] == i.pos[0] and mouse_loco[1] == i.pos[1]:
                            self.start = 0
                            self.Player.clear()

        if ISPath:
            self.Player[0].get_path()
            self.time = -round(self.time, 2)
        Draw_open(self.screen)
        Draw_close(self.screen)
        self.Draw_path('yellow')

        self.Tile_render()

        self.Showtime(Display)

        for i in self.Player:
            i.update()
            i.render(self.screen)

        #GHOSTING
        self.ghosting(mouse_loco)
        
        self.UI()
    def Draw_path(self, color):
        surf = pygame.Surface((self.Block_size, self.Block_size))
        surf.fill(color)
        if self.path:
            for i in self.path:
                self.screen.blit(surf, (i[0]*self.Block_size, i[1]*self.Block_size ))
    
    def Draw_grid(self, color):
        surf = pygame.Surface((self.Block_size - 2, self.Block_size -2))
        surf.fill(color)
        Blockx = screen_w // self.Block_size
        Blocky = screen_h // self.Block_size
        for x in range(Blockx):
            for y in range(Blocky):
                self.screen.blit(surf, (x * self.Block_size, y * self.Block_size))
    
    def ghosting(self, mouse_loco):
        surf = pygame.Surface((self.Block_size, self.Block_size))
        if self.hand == 0:
            surf.fill('green')
        elif self.hand == 1:
            surf.fill('red')
        elif self.hand == 2:
            surf.fill('black')

        surf.set_alpha(100)
        self.screen.blit(surf, (mouse_loco[0] * self.Block_size, mouse_loco[1] * self.Block_size))
    
    def UI(self):
        surf = pygame.Surface((self.Block_size * 4, self.Block_size * 4))
        if self.hand == 0:
            surf.fill('green')
        elif self.hand == 1:
            surf.fill('red')
        elif self.hand == 2:
            surf.fill('black')

        rect = surf.get_rect( topright = (screen_w + 64, 0))
        Display.blit(surf, rect )
    
    def Tile_render(self):
        surf = pygame.Surface((self.Block_size, self.Block_size))
        for i in self.Block:
            surf.fill(self.Block[i]['Color'])
            self.screen.blit(surf, (self.Block[i]['Pos'][0] * self.Block_size, self.Block[i]['Pos'][1] * self.Block_size ))

    def Around(self, pos):
        around = []
        for i in Checking:
            loco = (pos[0] + i[0], pos[1] + i[1])
            str_loco = str(loco[0]) +',' + str(loco[1])
            if str_loco in self.Block:
                if self.Block[str_loco]['type'] in Collision:
                    around.append(i)
        return around

    def Showtime(self, surf):
        text = Font.render(str(self.time), False, 'white')
        t_rect1 = text.get_rect(bottomright = (screen_w + 64, screen_h))
        surf.blit(text, t_rect1)

        text_2 = Font.render('Timer', False, 'white')
        t_rect2 = text_2.get_rect(bottomright = (screen_w + 64, screen_h - 30))
        surf.blit(text_2, t_rect2)
        

if __name__ == '__main__':
    pygame.init()
    screen_w, screen_h = 1280, 720
    Display = pygame.display.set_mode((screen_w + 64, screen_h))
    pygame.display.set_caption('A* Algorithm Visualization')
    game = Game()

    Font = pygame.font.SysFont('Calibri', 25)

    clicking = False
    right_click = False
    ISPath = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    game.hand = (game.hand + 1) % 3
                if event.button == 5:
                    game.hand = (game.hand - 1) % 3
                if event.button == 1:
                    clicking = True
                if event.button == 3:
                    right_click = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    clicking = False
                if event.button == 3:
                    right_click = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game.Player and game.END_aw:
                        ISPath = True
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit( ASearch, game ,( int(game.Player[0].pos[0]), int(game.Player[0].pos[1]) ), game.END_aw[0] )
                            return_value = future.result()
                            game.path = return_value[0]
                            game.time = return_value[1] #type: ignore
                        # game.path, game.time = ASearch(game ,( int(game.Player[0].pos[0]), int(game.Player[0].pos[1]) ), game.END_aw[0]) #type: ignore
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    ISPath = False

        Display.fill('purple')
        game.update()
        Display.blit(game.screen, (0, 0))
        pygame.display.flip()