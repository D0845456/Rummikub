'''
Created on 2021年12月12日

@author: user
# 12/31 已有頁面轉換，但換頁後程式會不正常關閉
'''
from typing import Text
from xmlrpc.client import Server
import pygame
from pygame.locals import QUIT
from pygame.time import Clock
import os, time
import inputbox2
from bf_button import BFButton,BFButtonGroup
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 474
WHITE = (255, 255, 255)
BLUE = (0, 48, 96)
IMAGEWIDTH = 300
IMAGEHEIGHT = 200
FPS = 60
COLOR_INACTIVE = (100, 100, 200)
COLOR_ACTIVE = (200, 200, 255)
clock = pygame.time.Clock()
INIT_PAGE = 1
REGISTER_PAGE = 2
LOGIN_PAGE = 3
WAIT_PAGE = 4
GAME_PAGE = 5
END_PAGE = 6
# CUR_PAGE = INIT_PAGE
color_text = (200, 200, 200)
def draw_init(screen):
    raw_background = pygame.image.load(os.path.join('img','./rummikub2.png')).convert()
    background = pygame.transform.scale(raw_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(background,(0,0))
    # color_bg = (0,0,0) 
    register_clicked = False
    login_clicked = False
    # Text
    font = pygame.font.SysFont("C:\Windows\Fonts\msjh.ttc",50)
    text_reg = font.render("Register", True, color_text, (0,48,96))
    text_reg_clicked = font.render("Clicked", True, color_text)
    text_reg_rect = text_reg_clicked.get_rect(center=(WINDOW_WIDTH/5*4+50, WINDOW_HEIGHT/4))
    # Button_Regist = Button(300,200,WINDOW_WIDTH/3,WINDOW_HEIGHT/3)
    text_log = font.render("Login", True, color_text, (0,48,96))
    text_log_clicked = font.render("Clicked", True, color_text)
    text_log_rect = text_log_clicked.get_rect(center=(WINDOW_WIDTH/5*4+50, WINDOW_HEIGHT/4+65))
    while True:
        clock.tick(FPS)
        # 偵測事件
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                # exit()
                # return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                register_clicked = True if text_reg_rect.collidepoint(event.pos) else False
                login_clicked = True if text_log_rect.collidepoint(event.pos) else False
        if register_clicked:
        # screen.blit(text_clicked, text_rect)
            return REGISTER_PAGE
    #     raw_background = pygame.image.load('./background.png')
    #     background = pygame.transform.scale(raw_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    #     screen.blit(background,(0,0))    
        elif login_clicked:
            return LOGIN_PAGE
        else:
            screen.blit(text_reg, text_reg_rect)
            screen.blit(text_log, text_log_rect)
        pygame.display.update()
    return True
# register page
input_account = inputbox2.InputBox(WINDOW_WIDTH/7*2, WINDOW_HEIGHT/3, 140, 32)
input_password = inputbox2.InputBox(WINDOW_WIDTH/7*2, WINDOW_HEIGHT/3+80, 140, 32, True)
input_boxes = [input_account, input_password]
def register_click(btn):
    print(input_account.text)
    print(input_password.text)
    # input_account.text = ''
    # input_password.text = ''
    return (input_account.text, input_password.text)
def login_click(btn):
    print(input_account.text)
    print(input_password.text)
    # input_account.text = ''
    # input_password.text = ''
    return (input_account.text, input_password.text)
def back_click(btn):
#     CUR_PAGE = INIT_PAGE
#     print(btn.in_click)
    pass
def draw_regist(screen):
    back_clicked = False
    # Font
    font = pygame.font.Font('C:\Windows\Fonts\msjh.ttc', 32)
    textFont = pygame.font.Font('C:\Windows\Fonts\msjh.ttc', 24)
    # 建造按鈕
    btn_group = BFButtonGroup()
    btn_group.make_button(screen, (WINDOW_WIDTH/7*2, WINDOW_HEIGHT/3+130,120,40),text='Register',click=register_click)
    btn_group.make_button(screen, (WINDOW_WIDTH/7*3, WINDOW_HEIGHT/3+130,120,40),text='Back',click=back_click)
    
    # 畫背景
    raw_background = pygame.image.load(os.path.join('img','background.png'))
    background = pygame.transform.scale(raw_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    # screen.blit(background,(0,0))

    title_surface = font.render("註冊:", True, WHITE)

    text1_surface = textFont.render("username", True, WHITE)
    text2_surface = textFont.render("password", True, WHITE)
    # 遊戲迴圈
    while True:
        clock.tick(FPS)
        screen.blit(background,(0,0))
        screen.blit(title_surface, (WINDOW_WIDTH/7*2, WINDOW_HEIGHT/8))
        screen.blit(text1_surface, (WINDOW_WIDTH/7*2, WINDOW_HEIGHT/8*2))
        screen.blit(text2_surface, (WINDOW_WIDTH/7*2, WINDOW_HEIGHT/8*2+80))
        btn_group.draw()
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
                # back_clicked = True if text_back_rect.collidepoint(event.pos) else False
            for box in input_boxes:
                box.handle_event(event)
            btn_group.update(event)
        
        for box in input_boxes:
            box.update()

        for box in input_boxes:
            box.draw(screen)
        if btn_group.btn_list[1].in_click:
            return INIT_PAGE
        elif btn_group.btn_list[0].in_click: # click regist
            result = (input_account.text, input_password.text)
            input_account.text = ''
            input_password.text = ''
            return result
        #     screen.blit(text_back, text_back_rect)
        
        pygame.display.flip()
        screen.fill((30, 30, 30))
    return True
def draw_login(screen):
    back_clicked = False
    # Font
    font = pygame.font.Font('C:\Windows\Fonts\msjh.ttc', 32)
    textFont = pygame.font.Font('C:\Windows\Fonts\msjh.ttc', 24)
    # 建造按鈕
    btn_group = BFButtonGroup()
    btn_group.make_button(screen, (WINDOW_WIDTH/7*2, WINDOW_HEIGHT/3+130,120,40),text='Login',click=register_click)
    btn_group.make_button(screen, (WINDOW_WIDTH/7*3, WINDOW_HEIGHT/3+130,120,40),text='Back',click=back_click)
    
    # 畫背景
    raw_background = pygame.image.load(os.path.join('img','background.png'))
    background = pygame.transform.scale(raw_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    # screen.blit(background,(0,0))
    # text_back = font.render("Back", True, color_text, (0,48,96))
    # text_back_clicked = font.render("Clicked", True, color_text)
    # text_back_rect = text_back_clicked.get_rect(center=(WINDOW_WIDTH/5, WINDOW_HEIGHT/4))
    title_surface = font.render("登入:", True, WHITE)

    text1_surface = textFont.render("username", True, WHITE)
    text2_surface = textFont.render("password", True, WHITE)
    # 遊戲迴圈
    while True:
        clock.tick(FPS)
        screen.blit(background,(0,0))
        screen.blit(title_surface, (WINDOW_WIDTH/7*2, WINDOW_HEIGHT/8))
        screen.blit(text1_surface, (WINDOW_WIDTH/7*2, WINDOW_HEIGHT/8*2))
        screen.blit(text2_surface, (WINDOW_WIDTH/7*2, WINDOW_HEIGHT/8*2+80))
        btn_group.draw()
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     card_clicked = True if text_back_rect.collidepoint(event.pos) else False
            for box in input_boxes:
                box.handle_event(event)
            btn_group.update(event)
            
        
        for box in input_boxes:
            box.update()

        for box in input_boxes:
            box.draw(screen)
        if btn_group.btn_list[1].in_click:
            return INIT_PAGE
        elif btn_group.btn_list[0].in_click: # click regist
            result = (input_account.text, input_password.text)
            input_account.text = ''
            input_password.text = ''
            return result
        # elif btn_group.btn_list[0].in_click:
            # return GAME_PAGE
        pygame.display.flip()
        screen.fill((30, 30, 30))
def draw_wait(screen, rest):
    # Font
    font = pygame.font.Font('C:\Windows\Fonts\msjh.ttc', 32)
    textFont = pygame.font.Font('C:\Windows\Fonts\msjh.ttc', 24)
    
    # 畫背景
    raw_background = pygame.image.load(os.path.join('img','background.png'))
    background = pygame.transform.scale(raw_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    # screen.blit(background,(0,0))
    # text_back = font.render("Back", True, color_text, (0,48,96))
    # text_back_clicked = font.render("Clicked", True, color_text)
    # text_back_rect = text_back_clicked.get_rect(center=(WINDOW_WIDTH/5, WINDOW_HEIGHT/4))
    
    # 遊戲迴圈
    while True:
        clock.tick(FPS)
        screen.blit(background,(0,0))
        title_surface = font.render("正在等待其他玩家登入({}/2)...".format(2-rest), True, WHITE)
        screen.blit(title_surface, (WINDOW_WIDTH/7*2, WINDOW_HEIGHT/8))
        # screen.blit(text1_surface, (WINDOW_WIDTH/7*2, WINDOW_HEIGHT/8*2))
        # screen.blit(text2_surface, (WINDOW_WIDTH/7*2, WINDOW_HEIGHT/8*2+80))
       # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     card_clicked = True if text_back_rect.collidepoint(event.pos) else False
        pygame.display.flip()
        screen.fill((30, 30, 30))
        if rest == 0:
            print('the room is full')
            # title_surface = font.render("Game Start!!", True, WHITE)
            # screen.blit(title_surface, (WINDOW_WIDTH/7*2, WINDOW_HEIGHT/8))
            time.sleep(1)
            return GAME_PAGE
        else:
            return WAIT_PAGE
def draw_end(screen, msg):
    # Font
    font = pygame.font.Font('C:\Windows\Fonts\msjh.ttc', 32)
    textFont = pygame.font.Font('C:\Windows\Fonts\msjh.ttc', 24)
    
    # 畫背景
    raw_background = pygame.image.load(os.path.join('img','background.png'))
    background = pygame.transform.scale(raw_background, (WINDOW_WIDTH, WINDOW_HEIGHT))

    # 遊戲迴圈
    while True:
        clock.tick(FPS)
        screen.blit(background,(0,0))
        title_surface = font.render(msg, True, WHITE)
        text_surface = textFont.render("按下任意鍵返回主畫面", True, WHITE)
        screen.blit(title_surface, (WINDOW_WIDTH/7*2, WINDOW_HEIGHT/8))
        screen.blit(text_surface, (WINDOW_WIDTH/7*2, WINDOW_HEIGHT/8*2))
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                return INIT_PAGE
        pygame.display.flip()
        screen.fill((30, 30, 30))
        
def main():
    pygame.init()
    
    # load window surface
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Rummikub')
      
    # Font
    font = pygame.font.Font('C:\Windows\Fonts\msjh.ttc', 32)
    textFont = pygame.font.Font('C:\Windows\Fonts\msjh.ttc', 24)
    cur_page = draw_init(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        print('cur_page =',cur_page)
        if cur_page == INIT_PAGE:
            cur_page = draw_init(screen)
        elif cur_page == REGISTER_PAGE:
            cur_page = draw_regist(screen)
        elif cur_page == LOGIN_PAGE:
            cur_page = draw_login(screen)
        elif cur_page == WAIT_PAGE:
            cur_page = draw_wait(screen)
        elif cur_page == END_PAGE:
            cur_page = draw_wait(screen)
        else:
            print('Page is wrong')
    # Input box
    # input_box = pygame.Rect(100, 100, 140, 32)
                      
    # inputbox    
    # if event.type == pygame.MOUSEBUTTONDOWN:
    #     active = True if input_box.collidepoint(event.pos) else False

        # Change the current color of the input box
        # color = COLOR_ACTIVE if active else COLOR_INACTIVE
    
    # input box
    # if event.type == pygame.KEYDOWN:
    #     if active:
    #         if event.key == pygame.K_RETURN:
    #             print(text)
    #             text = ""
    #         elif event.key == pygame.K_BACKSPACE:
    #             text = text[:-1]
    #         else:
    #             text += event.unicode    
    # screen.fill(BLUE)

    # pygame.draw.rect(screen, (100, 100, 100), text_rect)
    
   

    
    # 控制遊戲迴圈迭代速率
    # main_clock.tick(FPS)
if __name__ == '__main__':
    main()