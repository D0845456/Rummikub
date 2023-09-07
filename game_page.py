"""
2022-1-6: 完成卡片拖曳並解決同時移動之bug
2022-1-7: 完成牌組移動判定,只差連線通訊
2022-1-8: 完成輪流出牌、畫面同步, 但發現group碰撞bug
"""

from typing import Text
import xmlrpc.client
import pygame
import os, random, time
import client_mix
from bf_button import BFButton,BFButtonGroup
import startPage, game
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

PORT = 8888
serverIP = '127.0.0.1'
server = xmlrpc.client.ServerProxy('http://' + serverIP + ':' + str(PORT))
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
        self.card = pygame.transform.scale(self.card,(28,35))
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
    def __init__(self, isJoker = False, number = 0,  color = '', group = -2, index = -1):
        global MUTEX
        MUTEX = True
        pygame.sprite.Sprite.__init__(self)
        self.isJoker = isJoker
        self.number = number
        self.color = color
        self.last_index = -1
        self.index = index
        # group(-2) == init
        # group(-1) == my deck
        # group(n) == on table  , n >= 0
        self.group = group
        self.last_group = group
        if isJoker:
            self.image = pygame.image.load(os.path.join('img','joker_card.png')).convert_alpha()
        else:
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
                print('{} {}'.format(self.color,self.number),'from deck[{}]'.format(self.group),'to mouse')
                MUTEX = False
            else:
                self.clicked = False
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
                self.last_index = self.index
                self.last_group = self.group       # record last group
                if self.group>=0:
                    table_sprites_list[self.group].remove(self)
                elif self.group==-1:
                    myDeck_sprite.remove(self)
                mouse_sprite.add(self)
        
                # print('move to mouse')
                # print('self.group = ',self.group)
                self.rect.center = mouse_pos
                  
    # End of Card
def reset_click(btn):
    global all_sprites
    all_sprites.draw(screen)
def end_click():
    pass
    # server.endTurn(pin)
    # if donothing:
    #     server.Deal(pin,1)
def win_click():
    pass
def update_index(deck):
    for i in range(len(deck)):
        deck[i].index = deck.index(deck[i])+1

def printCardInfo(deck):
    print('----------------------')
    for i in range(len(deck)):
        if deck[i].isJoker:
            print('Joker, l_g:{}, g:{}'.format(deck[i].last_group, deck[i].group))
        else:
            print('{} {}, l_g:{}, g:{}'.format(deck[i].color, deck[i].number, deck[i].last_group, deck[i].group))
    print('----------------------')
def draw_game(pin, turn = False):
    global all_sprites, table_sprites, table_sprites_list, myDeck_sprite, myDeck, table_decks, mouse_sprite, server, MUTEX
    all_sprites = pygame.sprite.Group()
    table_sprites = pygame.sprite.Group()
    table_sprites_list = []
    myDeck_sprite = pygame.sprite.Group()
    mouse_sprite = pygame.sprite.GroupSingle()
    # donothing = True
    btn_group = BFButtonGroup()
    # btn_group.make_button(screen, (WINDOW_WIDTH/7*5+100, WINDOW_HEIGHT/3+200,120,40),text='Reset',click=reset_click)
    btn_group.make_button(screen, (WINDOW_WIDTH/7*5+100, WINDOW_HEIGHT/3+200,120,40),text='End',click=end_click())

    user1 = Player('Jeff',17)
    all_sprites.add(user1)
    # table_decks = 'Table:\n[1] Joker Orange 3 Orange 4'
    # your_deck = 'Your deck:\n[ 1] Black 4\n[ 2] Black 5\n[ 3] Black 5\n[ 4] Black 9\n[ 5] Black 10\n[ 6] Blue 2\n[ 7] Blue 5\n[ 8] Blue 12\n[ 9] Orange 3\n[10] Orange 10\n[11] Red 1\n[12] Red 4\n[13] Red 7\n[14] Red 8\n'   # card = Card()
    # all_sprites.add(card)
    runing = True
    myDeck_pos = (30, WINDOW_HEIGHT-75)
# 測試之初始常數
    # server.start()

    # 拿取手牌
    recv = server.returnMyDeck(pin)
    # print('recv of my Deck == ',recv)
    recv = recv.split("\n")
    myDeck = []
    index_count = 1
    if recv[0] == 'This deck is empty!':
        print(recv)
    else:
        del recv[-1]        # 去除雜質
        for i in range(len(recv)):
            data = recv[i].split(' ')
            if len(data) == 1:  # It is Joker
                card = Card(True, 0, None, -1, index_count)
            else:
                card = Card(False, data[1], data[0], -1,index_count)
            index_count += 1
            card.set_pos(myDeck_pos[0]+i*45)
            myDeck.append(card)
            myDeck_sprite.add(card)
            all_sprites.add(card)
    
    # 檢視桌面
    recv = server.returnTable()
    print('recv str', recv)
    # table_decks = []
    table_sprites_list.clear()
    POS_X_org = 200
    POS_Y_org = 60
    try:
        if recv == 'This table is empty!':
            print(recv)
            draw_text(screen, recv, WHITE, None, 32, WINDOW_WIDTH/2, 25)
        else:
            pos_x = POS_X_org
            pos_y = POS_Y_org
            table_decks = recv.split('---')
            
            del table_decks[-1]        # 去除雜質
            # print('type of table_decks',type(table_decks))
            # print('table_decks',table_decks)
            
            # print('recv list = ')
            # print(table_decks)
            # for i in range(len(table_decks)):
            #     print(table_decks[i])
            # print('recv[-1] = ',recv[-1])
            for table_decknum in range(len(table_decks)):
                new_deck_sprites = pygame.sprite.Group()
                # table_sprites.empty()                          ##
                deck = table_decks[table_decknum].split('\n')
                del deck[-1]
                # print('deck[{}] = '.format(table_decknum))
                # print(deck)
                index_count = 1
                # print('len of deck = [{}]'.format(len(deck)))
                for card_index in range(len(deck)):
                    card = deck[card_index].split(' ')
                    # print('len of card:',len(card))
                    if len(card) == 1:  
                        c = Card(True, 0, '', table_decknum, index_count)  # It is Joker
                        # print("Joker")
                    else:
                        c = Card(False, card[1], card[0], table_decknum, index_count)
                        # print(card[0],card[1])
                    index_count += 1
                    # print('({},{})'.format(pos_x,pos_y))
                    c.set_pos(pos_x, pos_y)
                    new_deck_sprites.add(c)
                    all_sprites.add(c)
                    pos_x += 35
                # print('x+',200*((table_decknum+1)/4))
                # print('offset = ',int((table_decknum+1)/4))
                pos_x = POS_X_org+ 200*int(((table_decknum+1)/4))
                if table_decknum!=0 and table_decknum%4 == 3:
                    pos_y = POS_Y_org
                else:
                    pos_y += 60
                # pos_y %= 300
                # pos_x = 200+ 200*(table_deck/6)
                table_sprites_list.append(new_deck_sprites)
                # new_deck_sprites.empty()
            # print('+++++++++++++++++++++++++++++1')
            # print('length of sprite list:',len(table_sprites_list))
            # for num in range(len(table_sprites_list)):
                # print('deck =',num)
            #     list1 = table_sprites_list[num].sprites()
            #     print('len = ',len(list1))
            #     for ca in range(len(list1)):
            #         if list1[ca].isJoker:
            #             print('Joker')
            #         else:
            #             print(list1[ca].color,list1[ca].number)
            #     print('------------\n')
            # print('+++++++++++++++++++++++++++++2')
    except Exception as e:
        print('recv = ',recv)
        print('Exception:',e)    
    # 遊戲迴圈
    # input = inputbox.InputBox(WINDOW_WIDTH/7*4, WINDOW_HEIGHT/3*2, 400, 32)
    # input_boxes = [input]
    while runing:
        clock.tick(FPS)
        donothing = True
        collide_judge = False
        hasCollide = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runing = False
            elif event.type == pygame.MOUSEBUTTONUP and turn and not btn_group.btn_list[0].in_click:
                mouse_pos = pygame.mouse.get_pos()
                # 出牌區範圍:x = 180~720, y = 50~590
                if (180<=mouse_pos[0]<=720) and (50<=mouse_pos[1]<=590) and (len(mouse_sprite.sprites())==1):
                    collide_judge = True
            # for box in input_boxes:
            #     box.handle_event(event)
            if turn:
                for sprite in all_sprites:
                    sprite.handle_event(event)
                btn_group.update(event)

        
        # collide_judge is a flag that determine whether to do collision judge 
        if collide_judge:
            # print('len of table_sprites_list', len(table_sprites_list))
            for decknum in range(len(table_sprites_list)):
                # print('------------\n')
                # print('deck =',decknum)
                # print(table_sprites_list[decknum].sprites)
                # print('------------\n')
                play = pygame.sprite.groupcollide(mouse_sprite, table_sprites_list[decknum], False, False)
                # print('play =',play)
                if len(play)>0:
                    # print('play length =',len(play))
                    hasCollide = True
                    print('Has Collide deck[{}]!!'.format(decknum))
                    print('length of sprite list:',len(table_sprites_list))
                    for num in range(len(table_sprites_list)):
                        print('deck =',num)
                        list1 = table_sprites_list[num].sprites()
                        print('len = ',len(list1))
                        for ca in range(len(list1)):
                            if list1[ca].isJoker:
                                print('Joker')
                            else:
                                print(list1[ca].color,list1[ca].number)
                    print('------------\n')
                for card in play:
                    print('{} {}'.format(card.color, card.number), 'from mouse to deck[{}]'.format(decknum))
                    mouse_sprite.remove(card)
                    
                    card.group = decknum
                    table_sprites_list[decknum].add(card)
                    table_sprites_list[decknum].draw(screen)
                    # table_decks[decknum].append(card)                    #####
                    # move
                    try:
                        if card.last_group>=0:
                            server.Move(card.last_group, card.index, decknum)
                            return startPage.GAME_PAGE
                            # table_decks[card.last_group].remove(card)    #####
                        elif card.last_group == -1:
                            server.play(pin, card.last_index, decknum)
                            return startPage.GAME_PAGE
                            # myDeck.remove(card)                          #####
                        # card.index = table_decks[deck].index(card)
                        update_index(myDeck)
                        for table_deck in range(len(table_decks)):
                            update_index(table_decks[table_deck])
                        # print('update!')
                    except Exception as e:
                        print('Exception:',e)
                        pass
            # put down the card but had no collision 
            # so give it to a new deck on the table
            if not hasCollide:
                # 出牌區範圍:x = 180~720, y = 50~590
                # try:
                    new_deck_sprites = pygame.sprite.Group()
                    # for i in mouse_sprite:
                    list2 = mouse_sprite.sprites()
                    card = list2[0]
                    if type(card) == Card:
                        if card.isJoker:
                            print('Joker')
                        else:
                            print(card.color,card.number)
                    else:
                        print('card is a',type(card))
                    # table_deck = [card]                             #####
                    card.index = 1     ### index+1                  #####
                    # table_decks.append(table_deck)                  #####
                    # update index of every deck (include my deck)
                    # update_index(myDeck)
                    # for table_deck in range(len(table_decks)):
                    #     update_index(table_decks[table_deck])
                    if card.last_group >= 0:
                        pass
                        # table_decks[card.last_group].remove(card)     #####
                        # print(111)
                    elif card.last_group == -1:  
                        pass 
                        # myDeck.remove(card)                             #####
                        # print(222)

                    mouse_sprite.remove(card)
                    new_deck_sprites.empty()
                    new_deck_sprites.add(card)
                    table_sprites_list.append(new_deck_sprites)
                    card.group = table_sprites_list.index(new_deck_sprites)
                    print('---\n{} {} from mouse to deck[{}]\n---'.format(card.color, card.number, card.group))
                    print('length of sprite list:',len(table_sprites_list))
                    for num in range(len(table_sprites_list)):
                        print('deck =',num)
                        list1 = table_sprites_list[num].sprites()
                        # length = len(table_sprites_list[num].sprites())
                        print('len = ',len(list1))
                        for ca in range(len(list1)):
                            if list1[ca].isJoker:
                                print('Joker')
                            else:
                                print(list1[ca].color,list1[ca].number)
                    print('------------\n')

                    server.play(pin, card.last_index, card.group)
                    return startPage.GAME_PAGE

                    # print('myDeck:')
                    # for card in myDeck:
                    #     if card.isJoker:
                    #         print('[{}]Joker'.format(card.index)) 
                    #     else:
                    #         print('[{}]{} {}'.format(card.index,card.color,card.number))

        if btn_group.btn_list[0].in_click: # click end
            server.endTurn(pin)
            return startPage.GAME_PAGE
        
        screen.fill(BLUE)
        screen.blit(background,(0,0))  
        # 更新遊戲
        # update_index(myDeck)
        # for table_deck in range(len(table_decks)):
        #     update_index(table_decks[table_deck])
        all_sprites.update()  # 更新all sprites的位置
        # 畫面顯示
        if turn:
            msg = 'It\'s your turn'
        else:
            msg = 'It\'s not your turn'
        draw_text(screen, msg, WHITE, None, 32, WINDOW_WIDTH/2, 25)
        pygame.draw.rect(screen, BLUE, (180, 50, WINDOW_WIDTH/5*4-50,WINDOW_HEIGHT/5*3),2)
        # 出牌區範圍:x = 180~720, y = 50~590
        all_sprites.draw(screen)
        user1.draw(screen)
        btn_group.draw()
        pygame.display.update()

        if not turn:
            time.sleep(0.5)
            return startPage.GAME_PAGE
        clock.tick(30)
    pygame.quit() 

if __name__ == '__main__':
    draw_game()


 