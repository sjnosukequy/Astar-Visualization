import pygame, sys
from Player import Player
from Algo import ASearch, Draw_open, Draw_close, Clear_visual, Maze, extract
import concurrent.futures
import threading

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
                elif self.hand == 0 and self.start < 5:
                    self.start = len(self.Player)
                    Exist = False
                    for i in self.Player:
                        if i.pos[0] == mouse_loco[0] and i.pos[1] == mouse_loco[1]:
                            Exist = True
                    if not Exist:
                        Clear_visual()
                        self.Player.append(Player(self, mouse_loco))

            if right_click:
                if mouse_locostr in self.Block:
                    if self.Block[mouse_locostr]['type'] == 'End':
                        self.end = 0
                        self.END_aw.clear()
                    del self.Block[mouse_locostr]
                for i in self.Player.copy():
                    if not i.path:
                        Clear_visual()
                        if mouse_loco[0] == i.pos[0] and mouse_loco[1] == i.pos[1]:
                            self.Player.remove(i)
                            self.start = len(self.Player)

        if len(self.Player) == 1:  
            Draw_open(self.screen)
            Draw_close(self.screen)

        self.Tile_render()

        self.Showtime(Display)

        for i in self.Player:
            self.Draw_path('yellow', i.path)
            i.update()
            i.render(self.screen)

        #GHOSTING
        self.ghosting(mouse_loco)
        
        self.UI()
    def Draw_path(self, color, path):
        surf = pygame.Surface((self.Block_size, self.Block_size))
        surf.fill(color)
        surf.set_alpha(100)
        if path:
            for i in path:
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

        text_3 = Font.render('Count', False, 'white')
        t_rect3 = text_3.get_rect(bottomright = (screen_w + 64, screen_h - 90))
        surf.blit(text_3, t_rect3)

        text_4 = Font.render(str(self.start), False, 'white')
        t_rect4 = text_4.get_rect(bottomright = (screen_w + 64, screen_h - 60))
        surf.blit(text_4, t_rect4)
        
    def Clear(self):
        self.END_aw.clear()
        self.Player.clear()
        self.Block.clear()
        Clear_visual()
        self.start = len(self.Player)
        self.end = 0

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

    thread = []
    path = [None] * 5
    timer = []

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
                        Ready = True
                        for i in game.Player:
                            if i.path:
                                Ready = False

                        if len(thread) == 0 and Ready:
                            N = len(game.Player)
                            for i in range(0, N):
                                thread.append(threading.Thread(target= ASearch, args= (game ,( int(game.Player[i].pos[0]), int(game.Player[i].pos[1]) ), game.END_aw[0], path, timer, i )) )
                                thread[i].start()

                if event.key == pygame.K_m:
                    Ready = True
                    for i in game.Player:
                        if i.path:
                            Ready = False

                    if len(thread) == 0 and Ready:
                        game.Clear()
                        maze = (Maze(screen_w, screen_h, game.Block_size))
                        extract(game, maze)

                if event.key == pygame.K_c:
                    Ready = True
                    for i in game.Player:
                        if i.path:
                            Ready = False

                    if len(thread) == 0 and Ready:
                        game.Clear()




            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    ISPath = False

        Display.fill('purple')
        game.update()

        N = len(game.Player)
        M = len(timer)
        if N == M and N > 0:
            for i in range(0, N):
                game.Player[i].get_path(path[i])
            game.time = timer[N - 1]
            game.time = -round(game.time, 2)
            path.clear()
            path = [None] * 5
            thread.clear()
            timer.clear()
        
        # if len(thread) == 0:
        #     print("OK")

        Display.blit(game.screen, (0, 0))
        pygame.display.flip()