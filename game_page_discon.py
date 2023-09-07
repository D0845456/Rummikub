"""
2022-1-6: 完成卡片拖曳並解決同時移動之bug
"""

from typing import Text
import pygame
from pygame import image
from pygame.constants import MOUSEBUTTONDOWN
import os, random

from pygame.event import set_allowed
from bf_button import BFButton,BFButtonGroup
# import inputbox
FPS = 60
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 500

GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (61, 61, 61)
ORANGE = (255, 88, 10)
RED = (235, 0, 0)
BLUE = (25, 59, 122)
BEIGE = (253, 247, 231)  # 米色
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Rummikub")
clock = pygame.time.Clock()
# 畫背景
raw_background = pygame.image.load(os.path.join('img','background.png')).convert()
background = pygame.transform.scale(raw_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
font = pygame.font.SysFont("C:\Windows\Fonts\msjh.ttc",50)
font_name = pygame.font.match_font('msjh.ttc')
def draw_text(surf, text = '', color = WHITE, color_bg = None, size = 32, x = 0, y = 0):
    text_list = text.split('\n')
    buf_x = x
    buf_y = y
    for i in range(len(text_list)):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text_list[i], True, color, color_bg)
        text_rect = text_surface.get_rect()
        text_rect.centerx = buf_x
        text_rect.top = buf_y
        surf.blit(text_surface, text_rect)
        buf_y+=20
        if i>0 and i%5==0: 
            buf_x += 120
            buf_y = y+20
class Player(pygame.sprite.Sprite):
    def __init__(self, name, card_number):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('img','user','man.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image,(80,80))
        self.card = pygame.image.load(os.path.join('img','blank.png')).convert_alpha()
        self.card = pygame.transform.scale(self.card,(32,40))
        self.card_number = card_number
        # self.image.set_colorkey(WHITE)
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50
        
    def handle_event(self, event):
        pass
    def update(self):
        pass
    def draw(self, screen):
        draw_text(screen, self.name, WHITE, None, 32, 90, 25)
        info = 'x'+str(self.card_number)
        screen.blit(self.card,(50, 140))
        draw_text(screen, info, WHITE, None, 32, 105, 150)
class Card(pygame.sprite.Sprite):
    def __init__(self, number = 0, isJoker = False, color = '', group = -1):
        global MUTEX
        MUTEX = True
        pygame.sprite.Sprite.__init__(self)
        self.isJoker = isJoker
        self.number = number
        self.color = color
        # group(-1) == init
        # group(0) == my deck
        # group(n) == on table
        self.group = group
        self.last_group = -1  
        self.image = pygame.image.load(os.path.join('img','{}'.format(str(self.color)),'{}_{}.png'.format(str(self.color),str(self.number)))).convert_alpha()
        self.image = pygame.transform.scale(self.image,(40,50))
        # self.image = pygame.Surface((40,55))
        # self.image.fill(BEIGE)
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = WINDOW_HEIGHT-75
        self.move = False
        self.clicked = False
    def set_pos(self, x = 200, y = WINDOW_HEIGHT-75):
        self.rect.x = x
        self.rect.y = y
    def handle_event(self, event):
        # draw_text(screen,str(self.number), RED, BEIGE, 18, self.rect.centerx, self.rect.top+3)
        global MUTEX
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if (self.rect.centerx-20 <= mouse_pos[0] <= self.rect.centerx+20) and (self.rect.centery-25 <= mouse_pos[1] <= self.rect.centery+25) and (MUTEX == True):
                # self.move = True
                self.clicked = True
                self.last_group = self.group
                print('{} {}'.format(self.color,self.number),'from deck[{}]'.format(self.group),'to mouse')
                MUTEX = False
            else:
                self.clicked = False
                # self.move = False
                MUTEX = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False

    def update(self):
        global mouse_sprite
        mouse_clicked = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_clicked[0]:       # Left-click
            # if self.move:
            #     self.rect.center = mouse_pos
            if self.clicked:
                # print('self.group = ',self.group)
                table_sprites_list[self.group].remove(self)
                mouse_sprite.add(self)
                # print('move to mouse')
                # print('self.group = ',self.group)
                self.rect.center = mouse_pos



    # End of Card
def reset_click(btn):
    global all_sprites
    all_sprites.draw(screen)
def end_click(btn):
    pass
def draw_game():
    global all_sprites, table_sprites, table_sprites_list, myDeck_sprite, mouse_sprite
    all_sprites = pygame.sprite.Group()
    table_sprites = pygame.sprite.Group()
    table_sprites_list = [table_sprites]
    myDeck_sprite = pygame.sprite.Group()
    mouse_sprite = pygame.sprite.Group()

    btn_group = BFButtonGroup()
    btn_group.make_button(screen, (WINDOW_WIDTH/7*5+40, WINDOW_HEIGHT/3+100,120,40),text='Reset',click=reset_click)
    btn_group.make_button(screen, (WINDOW_WIDTH/7*5+40, WINDOW_HEIGHT/3+150,120,40),text='End',click=end_click)

    user1 = Player('Jeff',17)
    all_sprites.add(user1)
    table_decks = 'Table:\n[1] Joker Orange 3 Orange 4'
    your_deck = 'Your deck:\n[ 1] Black 4\n[ 2] Black 5\n[ 3] Black 5\n[ 4] Black 9\n[ 5] Black 10\n[ 6] Blue 2\n[ 7] Blue 5\n[ 8] Blue 12\n[ 9] Orange 3\n[10] Orange 10\n[11] Red 1\n[12] Red 4\n[13] Red 7\n[14] Red 8\n'   # card = Card()
    # all_sprites.add(card)
    runing = True
    for i in range(1,14):
        card = Card(i, False, 'red', 0)
        card.set_pos(30+i*45)
        myDeck_sprite.add(card)
        all_sprites.add(card)
    color = ['red','orange','blue','black']
    pos_x = 200
    pos_y = 60
    for i in range(4):
        deck_sprites = pygame.sprite.Group()
        c = random.choice(color)
        start = random.randint(1,11)

        for j in range(start,start+3):
            card = Card(j, False, c, i+1)
            card.set_pos(pos_x, pos_y)
            # table_sprites.add(card)
            deck_sprites.add(card)
            all_sprites.add(card)
            pos_x += 35
        pos_y += 60
        pos_x = 200
        table_sprites_list.append(deck_sprites)
    # 遊戲迴圈
    # input = inputbox.InputBox(WINDOW_WIDTH/7*4, WINDOW_HEIGHT/3*2, 400, 32)
    # input_boxes = [input]
    while runing:
        clock.tick(FPS)
        collide_flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runing = False
            elif event.type == pygame.MOUSEBUTTONUP:
                # play = pygame.sprite.groupcollide(myDeck_sprite, table_sprites_list[deck], False, False)
                collide_flag = True
            # for box in input_boxes:
            #     box.handle_event(event)
            for sprite in all_sprites:
                sprite.handle_event(event)
            btn_group.update(event)
            
        # for box in input_boxes:
        #     box.update()

        screen.fill(BLUE)
        screen.blit(background,(0,0))
        # screen.fill((30, 30, 30))
        # for box in input_boxes:
        #     box.draw(screen)
        # draw_text(screen, table_decks, WHITE, None, 32, WINDOW_WIDTH/2, 50)
        # draw_text(screen, your_deck, WHITE, None, 26, WINDOW_WIDTH/5, WINDOW_HEIGHT/3*2)
        
        # 更新遊戲
        all_sprites.update()  # 更新all sprites的位置

        # 出牌碰撞判斷
        # if collide_flag:
        #     for deck in range(len(table_sprites_list)):
        #         play = pygame.sprite.groupcollide(myDeck_sprite, table_sprites_list[deck], False, False)
        #         for card in play:
        #             print('change = {} {}'.format(card.color, card.number), 'from my_deck to deck[{}]'.format(deck))
        #             myDeck_sprite.remove(card)
        #             table_sprites_list[deck].add(card)
        #             table_sprites_list[deck].draw(screen)
        #     # 桌面牌組變動碰撞判斷
        #     for deck_src in range(len(table_sprites_list)):
        #         changed = False
        #         # 把牌往前面的牌組移
        #         for deck_dest in range(deck_src-1):
        #             play = pygame.sprite.groupcollide(table_sprites_list[deck_src], table_sprites_list[deck_dest], False, False)
        #             for card in play:
        #                 print('change = ', card.number, card.color, 'from', deck_src, 'to', deck_dest)
        #                 table_sprites_list[deck_src].remove(card)
        #                 table_sprites_list[deck_dest].add(card)
        #                 table_sprites_list[deck_dest].draw(screen)
        #                 changed = True
        #                 print('The card has moved')
        #         # 把牌往後面的牌組移
        #         if not changed:
        #             for deck_dest in range(deck_src+1, len(table_sprites_list)):
        #                 play = pygame.sprite.groupcollide(table_sprites_list[deck_src], table_sprites_list[deck_dest], False, False)
        #                 for card in play:
        #                     print('change = ', card.number, card.color, 'from', deck_src, 'to', deck_dest)
        #                     table_sprites_list[deck_src].remove(card)
        #                     table_sprites_list[deck_dest].add(card)
        #                     table_sprites_list[deck_dest].draw(screen)

        if collide_flag:
            for deck in range(len(table_sprites_list)):
                play = pygame.sprite.groupcollide(mouse_sprite, table_sprites_list[deck], False, False)
                if len(play)>0:
                    print('Has Collide deck[{}]!!'.format(deck))
                for card in play:
                    print('{} {}'.format(card.color, card.number), 'from mouse to deck[{}]'.format(deck))
                    mouse_sprite.remove(card)
                    card.group = deck
                    table_sprites_list[deck].add(card)
                    table_sprites_list[deck].draw(screen)
                    
        # 畫面顯示
        all_sprites.draw(screen)
        user1.draw(screen)
        btn_group.draw()
        pygame.display.update()
        clock.tick(30)
    pygame.quit() 

if __name__ == '__main__':
    draw_game()


 