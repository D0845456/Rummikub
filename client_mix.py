import xmlrpc.client
import time
PORT = 8888
serverIP = '127.0.0.1'

from typing import Text
import pygame
import os
import inputbox, startPage, game_page
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
LIGHT_BLUE = (91, 155, 213)
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Rummikub")
clock = pygame.time.Clock()
# 畫背景
raw_background = pygame.image.load(os.path.join('img','background.png')).convert()
background = pygame.transform.scale(raw_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
font = pygame.font.SysFont("C:\Windows\Fonts\msjh.ttc",50)
font_name = pygame.font.match_font('msjh.ttc')
input = inputbox.InputBox(WINDOW_WIDTH/7*2, WINDOW_HEIGHT/3, 140, 32)

def draw_text(surf, text, color, color_bg, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color, color_bg)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

class Card(pygame.sprite.Sprite):
    def __init__(self, isJoker = False, color = '', number = 0,  function = "None"):
        pygame.sprite.Sprite.__init__(self)
        self.number = number
        # self.image = pygame.Surface((40,55))
        # self.image.fill(BEIGE)
        self.image = pygame.image.load(os.path.join('img','orange_{}'.format(str(self.number))))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = WINDOW_HEIGHT-75
        self.move = False
        # self.text = font.render("7", True, RED, BEIGE)
        # self.text_rect = self.text.get_rect(center=(self.rect.x, self.rect.y+20))
    def set_pos(self, x):
        self.rect.x = x
    def update(self):
        draw_text(screen,'7', RED, BEIGE, 18, self.rect.centerx, self.rect.top+3)
        mouse_clicked = pygame.mouse.get_pressed()
        if mouse_clicked[0]:       # Left-click
            self.move = True
        elif mouse_clicked[2]:     # Right-click
            self.move = False 
        if self.move == True:
            mouse_pos = pygame.mouse.get_pos()
            self.rect.center = mouse_pos
        # screen.blit(self.text, self.text_rect)
        self.move = False
        # pass
def main():
    # if len(sys.argv)<2:
    #     print("Usage: python3 Client.py serverIP username")
    #     exit(1)
    all_sprites = pygame.sprite.Group()
    # card = Card()
    # all_sprites.add(card)
    input = inputbox.InputBox(WINDOW_WIDTH/7*2, WINDOW_HEIGHT/3*2, 400, 32)
    input_boxes = [input]
    runing = True
    typing = False
    server = xmlrpc.client.ServerProxy('http://' + serverIP + ':' + str(PORT))
# begin
    pin = -1
    cur_page = 1
    while True:
        try:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
            print('cur_page =',cur_page)
            if cur_page == startPage.INIT_PAGE:
                cur_page = startPage.draw_init(screen)
                
            elif cur_page == startPage.REGISTER_PAGE:
                result = startPage.draw_regist(screen)
                if type(result) == int:
                    cur_page = result
                elif type(result) == tuple:
                    account, password = result
                    print('acc = ',account)
                    print('pass = ',password)
                    try:
                        pin = server.register(account, password)
                        print('register successful')
                        print('pin = ', pin)
                        cur_page = startPage.WAIT_PAGE
                        break
                    except xmlrpc.client.Fault:
                        draw_text(screen, 'Dublicate ID!!',WHITE, None, 32, WINDOW_WIDTH/2, 20)
                        print('Dublicate ID!!')
                        pass

            elif cur_page == startPage.LOGIN_PAGE:
                while True:
                    result = startPage.draw_login(screen)
                    # print('result is a ',type(result))
                    if type(result) == int:
                        cur_page = result
                    elif type(result) == tuple:
                        account, password= result
                        print('acc = ',account)
                        print('pass = ',password)
                        try:
                            pin = server.login(account, password)
                            print('login successful')
                            print('pin = ', pin)
                            cur_page = startPage.WAIT_PAGE
                            break
                        except xmlrpc.client.Fault:
                            print('Login Failed!!')
                            draw_text(screen, 'Login Failed!!',WHITE, None, 32, WINDOW_WIDTH/2, 20)
                            pass
            elif cur_page == startPage.WAIT_PAGE:
                # rest = server.waitRoom()
                cur_page = startPage.draw_wait(screen, server.waitRoom())
                time.sleep(0.5)
            elif cur_page == startPage.GAME_PAGE:
                game_over = server.isGameOver(pin)
                if game_over == "Win!!!":
                    cur_page = (startPage.END_PAGE, 'Win!!!')
                elif game_over == "Lose!!!":
                    cur_page = (startPage.END_PAGE, 'Lose!!')
                elif game_over == False:
                    try:
                        isYourTurn = server.getTurn(pin)
                        # print('type: ',type(isYourTurn))
                    except Exception as  e:
                        print('Exception:',e)
                    if isYourTurn == True:
                        cur_page = game_page.draw_game(pin, True)
                    else:
                        cur_page = game_page.draw_game(pin, False)

            elif cur_page == (startPage.END_PAGE,'win'):
                cur_page = startPage.draw_end(screen, "You WIN!!!")
            elif cur_page == (startPage.END_PAGE,'win'):
                cur_page = startPage.draw_end(screen, "You Lose!!")
            # else:
            #     print('Page is wrong')

            # screen.fill(BLUE)
            # screen.blit(background,(0,0))
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #         break
            #     for box in input_boxes:
            #         box.handle_event(event)
            # for box in input_boxes:
            #     box.update()
            # screen.fill(BLUE)
            # screen.blit(background,(0,0))
            # for box in input_boxes:
            #     box.draw(screen)
            # pygame.display.update()


        #     draw_text(screen,'(1) For register\n(2) For login\nEnter:', WHITE, None, 32, WINDOW_WIDTH/2, 100)
        #     typing = True
        #     while typing:
        #         for event in pygame.event.get():
        #             if event.type == pygame.QUIT:
        #                 runing = False
        #                 pygame.quit()
        #             for box in input_boxes:
        #                 result = box.handle_event(event)
        #             if result:
        #                 typing = False
        #         for box in input_boxes:
        #             box.update()
        #         screen.fill(BLUE)
        #         screen.blit(background,(0,0))
        #         for box in input_boxes:
        #             box.draw(screen)

        #     # cmd = input('(1) For register\n(2) For login\nEnter:')
        #     cmd = result
        #     print('---result = ',result)
        #     if cmd == '1':
        #         try:
        #             pin = server.register(input('username:'), input('password:'))
        #             print('pin = ', pin)
        #             break
        #         except xmlrpc.client.Fault:
        #             print('Dublicate ID!!')
        #             pass
        #     elif cmd == '2':
        #         try:
        #             pin = server.login(input('username:'), input('password:'))
        #             print('pin = ', pin)
        #             break
        #         except xmlrpc.client.Fault:
        #             print('Login failed!!')
        #             pass
        # waiting = 1
        # while waiting>0:
        #     try:
        #         for event in pygame.event.get():
        #             if event.type == pygame.QUIT:
        #                 runing = False
        #         if waiting == 0:
        #             print('Game is going to start!!')
        #             break
        #         else:
        #             print('Waiting for %d more players' % waiting)
        #         waiting = server.waitRoom()
        #     except xmlrpc.client.Fault:
        #             print('Something failed!!')
        #             pass
        # server.start()
        # # recv = server.showMyDeck(pin)
        # # print(recv)
        # while(1):
        #     winner=server.endGame(pin)
        #     if(winner==True):
        #         pass
        #     else:
        #         break
        #     while(1):
        #         winner=server.endGame(pin)
        #         if(winner==True):
        #             pass
        #         else:
        #             break
        #         reply=server.getTurn(pin)
        #         if(reply==True):
        #             break
        #         # time.sleep(10)
        #     if(winner==True):
        #         pass
        #     else:
        #         break
        #     donothing=True
        #     while(1):
        #         clock.tick(FPS)
        #         for event in pygame.event.get():
        #             if event.type == pygame.QUIT:
        #                 runing = False
        #         # 更新遊戲
        #         all_sprites.update()
        #         # 畫面顯示
        #         pygame.display.update()
        #         all_sprites.draw(screen)
        #         recv = server.showTable()
        #         print(recv)
        #         draw_text(screen,recv, 18, WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        #         recv = server.showMyDeck(pin)
        #         print(recv)
        #         draw_text(screen,recv, 18, WINDOW_WIDTH/2, WINDOW_HEIGHT-20)
        #         operate = input('Please chose move or play or end: ')
        #         if(operate=="move"):
        #             setIndex = int(input('Please Enter the index of set: '))
        #             cardIndex = int(input('Please Enter the index of card: '))
        #             tableIndex = int(input('Please Enter the index of table: '))
        #             server.Move(setIndex,cardIndex,tableIndex)
        #         elif(operate=="play"):
        #             cardIndex = int(input('Please Enter the index of card: '))
        #             tableIndex = int(input('Please Enter the index of card and the index of table: '))
        #             server.play(pin,cardIndex,tableIndex)
        #         elif(operate=="end"):
        #             server.endTurn(pin)
        #             if(donothing==True):
        #                 server.Deal(pin,1)
        #             recv = server.showTable()
        #             print(recv)
        #             recv = server.showMyDeck(pin)
        #             print(recv)
        #             break
        #         donothing=False
        # print(winner)
#end
        #     cmd = input('(1) Create a room\n(2) Join a exist room\n')
            # if cmd == '1':
                # Create room ( 2~4 People )

            # elif cmd == '2:
                # Join in a exist room
            #    
            # while True:
                # Wait for another players until room is full
                # Break
        # 
        except KeyboardInterrupt:
            print('Client exit')
            exit(1)
        

if __name__ == '__main__':
    main()
    


   


# for i in range(13):
#     card = Card()
#     card.set_pos(60+i*60)
#     all_sprites.add(card)
    
# 遊戲迴圈
# while runing:
#     clock.tick(FPS)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             runing = False
    
#     # 更新遊戲
#     screen.fill(BLUE)
#     screen.blit(background,(0,0))
#     all_sprites.update()
#     # 畫面顯示
#     pygame.display.update()
#     all_sprites.draw(screen)
#     # draw_text(screen,'777', 18, WINDOW_WIDTH/2, 10)

# pygame.quit() 


 