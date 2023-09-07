# -!- coding:utf-8 -!-
'''
Created on 2021年~12月12日

@author: Johnson
'''
from user import User
import json
import random
import time
import copy
LOGIN_FILE = 'userData.json'
class Card:
    def __init__(self, isJoker = False, color = '', number = 0,  function = "None"):
        self.isJoker = isJoker
        self.color = color
        self.number = number
        self.function = function
    def showCard(self):
        if self.isJoker == True:
            print('Joker')
        else:
            print('color = %s num = %s' %self.color % self.number)
        return True
    # End of Card
class Deck:           # 手牌
    def __init__(self):
        self.deck = []
    def deal(self, card):       # 抽牌進牌組
        self.deck.append(card)
        return True
    def play(self, index):             # 出牌
        index = index-1                #出牌時輸入把index-1，照輸出
        return self.deck.pop(index)
    def clear(self):
        # while len(self.deck)>0:
        self.deck.clear()
        return True 
    def sort(self):     # 將手牌依照顏色、數字排序
        self.deck.sort(key=lambda x:(x.isJoker, x.color,x.number))
    def showDeck(self):         # 列印牌組內的所有牌
        # for i in self.deck:
        #     i.showCard()
        for i in range(len(self.deck)):
            if self.deck[i].isJoker == True:
                print('[%2d] Joker' % (i+1))
            else:
                print('[%2d]'% (i+1) ,self.deck[i].color, self.deck[i].number)
        if len(self.deck) == 0:
            print('This deck is empty!')
        
        return True
    def Judge(self):                    #回傳False代表 牌桌上有放置錯誤
        Jokernum=0
        if(len(self.deck)==0):
            pass
        elif(len(self.deck)<3):
            return False
        self.deck.sort(key=lambda x:(not x.isJoker,x.color,x.number))
        if(self.deck[0].isJoker==True):
            Jokernum+=1
            if(self.deck[1].isJoker==True):
                Jokernum+=1
        if(Jokernum==2 and len(self.deck)==3):
            return True
        for i in range(Jokernum):
            self.deck[i].color=''
            self.deck[i].number=0
        if(Jokernum==0):                                #沒有Joker
            if(self.deck[0].color==self.deck[1].color):    #同顏色
                for i in range(1,len(self.deck)):
                    if(self.deck[0].color!=self.deck[i].color):    #顏色不同回傳錯誤
                        return False
                    elif(self.deck[i].number!=self.deck[i-1].number+1): #數字不連續回傳錯誤
                        return False
            elif(self.deck[0].number==self.deck[1].number):
                for i in range(len(self.deck)):
                    if(self.deck[0].number!=self.deck[i].number):    #數字不同
                        return False
                for j in range(len(self.deck)-1):    #顏色相同
                    for k in range(j+1,len(self.deck)):
                        if(self.deck[j].color==self.deck[i].color):
                            return False
        else:                                           #有Joker
            if(self.deck[Jokernum].color==self.deck[Jokernum+1].color):    #同顏色
                 for i in range(Jokernum+1,len(self.deck)):
                    if(self.deck[Jokernum].color!=self.deck[i].color):    #顏色不同回傳錯誤
                        return False
                    elif(self.deck[i].number!=self.deck[i-1].number+1): #數字不連續回傳錯誤
                        if(Jokernum==0):
                            return False
                        self.deck[Jokernum-1].color=self.deck[Jokernum].color
                        self.deck[Jokernum-1].number=self.deck[i-1].number+1
                        Jokernum-=1
                        self.deck.sort(key=lambda x:(x.color,x.number))
            elif(self.deck[0].number==self.deck[1].number):
                if(len(self.deck)>4):
                    return False
                for i in range(Jokernum,len(self.deck)):
                    if(self.deck[0].number!=self.deck[i].number):    #數字不同
                        return False
                for j in range(Jokernum,len(self.deck)-1):    #顏色相同
                    for k in range(j+1,len(self.deck)):
                        if(self.deck[j].color==self.deck[i].color):
                            return False
        return True
    # End of Deck
class Table():
    def __init__(self):
        self.decks = []         # 牌面上的組合
    def addDeck(self, oneDeck):        
        buff = Deck()
        # print('deck:',oneDeck.deck)        
        # print('len = ',len(oneDeck.deck))
        for i in range(len(oneDeck.deck)):      # 要將deck傳進來需要迭代(iteration)
            buff.deal(oneDeck.deck[i])
        buff.deck.sort(key=lambda x: (x.color,x.number))  # 把加進的牌排序一下
        self.decks.append(buff)
        return True
    
    def addcard(self, oneCard, deckNum):
        if deckNum > len(self.decks):        
            print('Please Enter a exist deckNum!!')
            return True
        elif deckNum == len(self.decks):
            buff = Deck()
            buff.deal(oneCard)
            self.decks.append(buff)
        else:
            self.decks[deckNum].deck.append(oneCard)
        return True
    def MoveSet(self,movedeckindex,movecardindex,toindex):
        card=self.decks[movedeckindex].play(movecardindex)
        self.addcard(card,toindex)
        self.decks[toindex].sort()
        self.decks[movedeckindex].sort()
        
    def showTable(self):
        print('Table:')
        # for i in self.decks:
        #     i.showCard()
        for i in range(len(self.decks)):
            print('table[%d]: ' % i)
            self.decks[i].showDeck()
        if len(self.decks) == 0:
            print('Table is empty!')
        return True
    
class Game:
    def __init__(self):
        self.username = {}
        self.curUser = {}
        self.decks = {}
        self.KeepTable=Table()
        self.Keepdecks=Deck()
        self.table = Table()
        self.turn = 0
        self.order = []
        self.win=0
        self.loadMember()
        self.waitRoom()
        self.start()
        #self.run()
    def loadMember(self):
        try:
            with open(LOGIN_FILE, 'r') as fp:
                member = json.load(fp)
            for index in member:
                self.username[index] = User(member[index][0] ,member[index][1])
        except json.decoder.JSONDecodeError:
            pass
        return True
    def dumpMember(self):
        temp = {}
        for index in self.username:
            temp[index] = [self.username[index].username, self.username[index].password]
        with open(LOGIN_FILE, 'w') as fp:
            json.dump(temp, fp)
        return True
    
    def register(self, username, password):
        if username in self.username:
            print(username,"Dublicate ID!")
            raise IOError
        else:
            self.username[username] = User(username, password)
            while True:
                pin = random.randint(1,999)
                if pin not in self.curUser:
                    self.curUser[pin] = self.username[username]
                    print(username,'register successfully')
                    break
            self.dumpMember()
        return pin
    def login(self, username, password):
        if username not in self.username:
            raise IOError
        else:
            while True:
                pin = random.randint(1,999)
                if pin not in self.curUser:
                    if password != self.username[username].password:
                        raise IOError
                    else:
                        self.curUser[pin] = self.username[username]
                    break
            print(username,'login successfully')
            return pin
    # End of login
    def initCards(self):       # 等同於MakeCards()
        pokers=[]			#整副牌
        for i in ['Blue','Red','Orange','Black']:
            for j in range(1,14):
                poker = Card(False, i, j, "None")
                pokers.append(poker)
        poker = Card(True)	#顏色 牌型 替換的數字
        #pokers.append(poker)
        pokers.append(poker)
        pokers = pokers*2
        random.shuffle(pokers)
        return pokers  
    # End of initCards()
    # def initPlayersDecks(self, headcount):
    #     for i in range(14):     # 各自從牌堆裡抽牌
    #         for j in range(headcount):
    #             self.curUser.deal
                # card = self.pokers.pop()
                # user.deal(card1)
    def waitRoom(self):
        players_number = 2
        while len(self.curUser)<players_number:
            print('Waiting for another %d people...' % (players_number-len(self.curUser)))
            time.sleep(0.5)
            return (players_number-len(self.curUser))
        self.start()
        return 0
    def start(self):
        print('Game start')
        self.pokers = self.initCards()  # 初始化整副牌
        for user in self.curUser:
            self.decks[user] = Deck()
        for i in range(14):
            for user in self.curUser:
                self.decks[user].deal(self.pokers.pop())
        for user in self.curUser:
            self.decks[user].sort()
            print('user = %s'% self.curUser[user].username)
            self.decks[user].showDeck()
        for pin in self.curUser:
            self.order.append(pin)
        return True
        
    def Deal(self,pin,num):
        for i in range(num):
            self.decks[pin].deal(self.pokers.pop())
        return True
    def play(self, pin, cardindex, deckNum):
        print('\n{} play [{}]th into deck[{}]\n'.format(self.curUser[pin].username,cardindex,deckNum))
        self.table.addcard(self.decks[pin].play(cardindex), deckNum)
        return True
    def Move(self,movedeckindex,movecardindex,toindex):
        print('from deck[{}] move [{}]th into deck[{}]'.format(movedeckindex,movecardindex,toindex))
        self.table.MoveSet(movedeckindex,movecardindex,toindex)
        return True
    def showMyDeck(self, pin):
        # self.decks[pin].showDeck()
        msg = '\n---------------------------\n'+self.curUser[pin].username + '\n'
        for i in range(len(self.decks[pin].deck)):
            if self.decks[pin].deck[i].isJoker == True:
                msg += '[%2d] Joker\n' % (i+1)
            else:
                msg += '[%2d] %s %s\n' % (i+1,self.decks[pin].deck[i].color, self.decks[pin].deck[i].number)
        if len(self.decks[pin].deck) == 0:
            msg += 'This deck is empty!'
        msg += '\n---------------------------\n'
        return msg
    def returnMyDeck(self, pin):
        msg = ''
        for i in range(len(self.decks[pin].deck)):
            if self.decks[pin].deck[i].isJoker == True:
                msg += 'Joker\n'
            else:
                msg += '%s %s\n' % (self.decks[pin].deck[i].color, self.decks[pin].deck[i].number)
        if len(self.decks[pin].deck) == 0:
            msg += 'This deck is empty!'
        return msg
    def showTable(self):
        msg = '\n---------------------------\n'+ 'Table' + '\n'
        for i in range(len(self.table.decks)):
            for j in range(len(self.table.decks[i].deck)):
                if self.table.decks[i].deck[j].isJoker == True:
                    msg += '[%2d] Joker\n' % (i)
                else:
                    msg += '[%2d] %s %s\n' % (i,self.table.decks[i].deck[j].color, self.table.decks[i].deck[j].number)
        if len(self.table.decks) == 0:
            msg += 'This table is empty!'
        msg += '\n---------------------------\n'
        return msg
        # self.table.showTable()
        # return True
    def returnTable(self):
        msg = ''
        for i in range(len(self.table.decks)):
            # msg += '['
            for j in range(len(self.table.decks[i].deck)):
                if self.table.decks[i].deck[j].isJoker == True:
                    msg += 'Joker\n'
                else:
                    msg += '%s %s\n' % (self.table.decks[i].deck[j].color, self.table.decks[i].deck[j].number)
            msg += '---'
        if len(self.table.decks) == 0:
            msg = 'This table is empty!'
        print('\ntable = {}\n'.format(msg))
        return msg
        # self.table.showTable()
        # return True
    def getTurn(self,pin):
        if(pin==self.order[self.turn]):
            self.KeepTable=Table()
            self.KeepTable=copy.deepcopy(self.table)
            self.Keepdecks=copy.deepcopy(self.decks[pin])
            return True
        else:
            return False
    def endTurn(self,pin):
        self.turn+=1
        self.turn=self.turn%2
        pass_judge = True                       # 原為Havewrong
        for i in range(len(self.table.decks)):
            pass_judge = self.table.decks[i].Judge()
            if(pass_judge == False):
                break
        if pass_judge == False:
            self.table=copy.deepcopy(self.KeepTable)
            self.decks[pin]=copy.deepcopy(self.Keepdecks)
            self.decks[pin].deal(self.pokers.pop())
            print('False')
            return False
        else:
            if(len(self.decks[pin].deck)==len(self.Keepdecks.deck)):
                self.decks[pin].deal(self.pokers.pop())
                return False

        if(len(self.decks[pin].deck)==0):
            self.win=pin
        print('True')
        return True
    def isGameOver(self,pin):  # 原先是endGame
        if(self.win!=0):
            if(self.win==pin):
                return "Win!!!"
            else:
                return "Lose!!!"
        else:
            return False  # 原先是True
    def run(self):
        # try:
        #     pin = self.register(input('username:'), input('password:'))
        #     print(pin)
        # except:
        #     print('Register failed!!')
        pokers = self.initCards()
        # print('len = ', len(pokers))
        
        # for i in range(len(pokers)):
        #     if pokers[i].isJoker == True:
        #         print('Joker')
        #     else:
        #         print(pokers[i].color,pokers[i].number)
        # table = Table()
        # headcount = int(input('Please enter the headcount: '))
        # while len(self.curUser) < headcount:
        #     print('Wait for %d more people...' % headcount-len(self.curUser))
        user1 = Deck()
        user2 = Deck()
        # temp = Deck()
        self.table.showTable()
        for i in range(14):     # 各自從牌堆裡抽牌
            card1 = pokers.pop()
            user1.deal(card1)
            card2 = pokers.pop()
            user2.deal(card2)
        # print('\nDeck of user2(%d):' % len(user2.deck))
        # user2.showDeck()
        # print('user1')

        # print('play: ',user1.deck[0].color,user1.deck[0].number)
        for i in range(5):
            user1.sort()
            print('\nDeck of user1(%d):' % len(user1.deck))
            user1.showDeck()
            cardIndex = int(input('Please Enter the index of card: '))
            tableIndex = int(input('Please Enter the index of card and the index of table: '))
            self.play(user1.play(cardIndex),tableIndex)
            self.table.showTable()
        while True:
            user1.sort()
            print('\nDeck of user1(%d):' % len(user1.deck))
            user1.showDeck()
            setIndex = int(input('Please Enter the index of set: '))
            cardIndex = int(input('Please Enter the index of card: '))
            tableIndex = int(input('Please Enter the index of card and the index of table: '))
            self.table.MoveSet(setIndex,cardIndex,tableIndex)
            self.table.showTable()


        # self.play(user1.play(0),0)

        # temp.deal(user1.play(0))
        # print('play: ',user1.deck[1].color,user1.deck[1].number)
        # temp.deal(user1.play(1))
        # print('play: ',user1.deck[2].color,user1.deck[2].number)
        # temp.deal(user1.play(2))
        # print('temp = ')
        # temp.showDeck()
        # self.table.addDeck(temp)
        # temp.clear()
        # print('clear: temp = ')
        # temp.showDeck()

        # temp2 = Deck()
        # print('user2')
        # print('play: ',user2.deck[0].color,user2.deck[0].number)
        # temp.deal(user2.play(0))
        # print('play: ',user2.deck[1].color,user2.deck[1].number)
        # temp.deal(user2.play(1))
        # print('play: ',user2.deck[2].color,user2.deck[2].number)
        # temp.deal(user2.play(2))
        # self.table.addDeck(temp)
        # self.table.showTable()

        # print('\nDeck of user1(%d):' % len(user1.deck))
        # user1.showDeck()
        # print('\nDeck of user2(%d):' % len(user2.deck))
        # user2.showDeck()
        # print('len = ', len(pokers))
# end of Class: Game
if __name__ == '__main__':
    Game()