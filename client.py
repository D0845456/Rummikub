# -!- coding:utf-8 -!-
'''
Created on 2021年~12月11日
@author: Johnson
'''
import xmlrpc.client
import time
PORT = 8888
serverIP = '127.0.0.1'
def main():
    # if len(sys.argv)<2:
    #     print("Usage: python3 Client.py serverIP username")
    #     exit(1)

    server = xmlrpc.client.ServerProxy('http://' + serverIP + ':' + str(PORT))
    try:
        while True:
            cmd = input('(1) For register\n(2) For login\nEnter:')
            if cmd == '1':
                try:
                    pin = server.register(input('username:'), input('password:'))
                    print('pin = ', pin)
                    break
                except xmlrpc.client.Fault:
                    print('Dublicate ID!!')
                    pass
            elif cmd == '2':
                try:
                    pin = server.login(input('username:'), input('password:'))
                    print('pin = ', pin)
                    break
                except xmlrpc.client.Fault:
                    print('Login failed!!')
                    pass
        waiting = 1
        while waiting>0:
            try:
                if waiting == 0:
                    print('Game is going to start!!')
                    break
                else:
                    print('Waiting for %d more players' % waiting)
                waiting = server.waitRoom()
            except xmlrpc.client.Fault:
                    print('Something failed!!')
                    pass
        server.start()
        # recv = server.showMyDeck(pin)
        # print(recv)
        while(1):
            winner=server.endGame(pin)
            if(winner==True):   # Judge whether gameover
                pass
            else:
                break
            while(1):
                winner=server.isGameOver(pin)  # endGame
                if(winner==True):
                    pass
                else:
                    break
                reply=server.getTurn(pin) # getTurn
                if(reply==True):
                    break
                # time.sleep(10)
            if(winner==True):      # Judge whether gameover
                pass
            else:
                break
            donothing=True
            while(1):
                recv = server.showTable()
                print(recv)
                recv = server.showMyDeck(pin)
                print(recv)
                operate = input('Please chose move or play or end: ')
                if(operate=="move"):
                    setIndex = int(input('Please Enter the index of set: '))
                    cardIndex = int(input('Please Enter the index of card: '))
                    tableIndex = int(input('Please Enter the index of table: '))
                    server.Move(setIndex,cardIndex,tableIndex)
                elif(operate=="play"):
                    cardIndex = int(input('Please Enter the index of card: '))
                    tableIndex = int(input('Please Enter the index of card and the index of table: '))
                    server.play(pin,cardIndex,tableIndex)
                elif(operate=="end"):
                    server.endTurn(pin)
                    if(donothing==True):
                        server.Deal(pin,1)
                    recv = server.showTable()
                    print(recv)
                    recv = server.showMyDeck(pin)
                    print(recv)
                    break
                donothing=False
        print(winner)

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