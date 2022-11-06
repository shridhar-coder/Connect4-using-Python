import numpy as np
import pygame
import sys
import math
import mysql.connector
from operator import itemgetter
from tabulate import tabulate

WOOD=(102,26,0)
WOOD2=(202,164,114)
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
C = (0,255,255)
WHITE=(255,255,255)

def leaderboard():
        pygame.init()
        screen=pygame.display.set_mode((700, 500))
        screen.fill((0,0,0))
        pygame.display.update()
        pygame.display.flip()
        mycursor.execute("SELECT wins.Wins, p_data.Name, wins.No_M FROM wins INNER JOIN p_data ON wins.Id=p_data.Id ORDER BY `wins`.`Wins` DESC;")
        myresult = mycursor.fetchall()
        l1=[['Wins', 'Player Username', 'Matches Played']]
        for x in myresult:
                l1.append(x)
        font = pygame.font.Font('freesansbold.ttf', 24)
        i=0
        j=0
        for l in l1:
                i=i+1
                j=0
                k=0
                for l in l:
                        text = font.render(str(l), True, WOOD)
                        screen.blit(text,(15+j*75,15+i*30))
                        j=j+1
                        j=j+k+1
                        k=k+1
                pygame.display.update()
        pygame.draw.line(screen, WOOD, (90,15), (90,500), 2)
        pygame.display.update()
        

                        
mydb = mysql.connector.connect(host="localhost",port="3306",user="root",password="",database="connect4")
mycursor = mydb.cursor()

def getlist(I):
    lst=[]
    for i in range(I):
        name=input("name")
        try:
            mycursor.execute("INSERT INTO `p_data` (`Id`, `Name`) VALUES"+"('',"+"'"+name+"');")
            mydb.commit()
            mycursor.execute("SELECT Id FROM p_data where name="+"'"+name+"';")
            l=[int(sum(mycursor.fetchone())),name]
            lst.append(l)
        except:
            #print("SELECT Id FROM p_data where name="+"'"+name+"'")
            mycursor.execute("SELECT Id FROM p_data where name="+"'"+name+"';")
            p_id=int(sum(mycursor.fetchone()))
            #print(p_id)
            l=[p_id,name]
            lst.append(l)
    #print(lst)
    #print(lst[1][1])
    return lst

def postdata(columns,rows,I,lst):
    mycursor.execute("SELECT MAX(GameNo) FROM history;")
    try:
        gameno=int(sum(mycursor.fetchone()))+1
    except:
        gameno=1
    for i in range(I):
        #print("INSERT INTO `history` (`M_ID`, `Cs`, `Rs`, `NP`, `GameNo`, `Id`) VALUES ('','"+str(columns)+"','"+str(rows)+"','"+str(I)+"','"+str(gameno)+"','"+str(lst[i][0])+"');")
        mycursor.execute("INSERT INTO `history` (`M_ID`, `Cs`, `Rs`, `NP`, `GameNo`, `Id`) VALUES ('','"+str(columns)+"','"+str(rows)+"','"+str(I)+"','"+str(gameno)+"','"+str(lst[i][0])+"');")
        mydb.commit()

def matchs(id):
    mycursor.execute("SELECT COUNT(Id) FROM history WHERE Id='"+id+"';")
    try:
        match=int(sum(mycursor.fetchone()))
    except:
        match=1
    return str(match)

def wins(id):
    m=matchs(id)
    try:
        mycursor.execute("INSERT INTO `wins`(`wID`, `Wins`, `Id`, `No_M`) VALUES('','1','"+id+"','"+m+"');")
        mydb.commit()
    except:
        mycursor.execute("SELECT Wins FROM wins WHERE Id='"+id+"';")
        wins=str(int(sum(mycursor.fetchone()))+1)
        #print(wins)
        #print("UPDATE `wins` SET `Wins`="+wins+",`No_M`="+m+" WHERE Id='"+id+"';")
        mycursor.execute("UPDATE `wins` SET `Wins`="+wins+",`No_M`="+m+" WHERE Id='"+id+"';")
        mydb.commit()

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r 

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, WOOD2, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen,BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 3:
				pygame.draw.circle(screen, C, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 4:
				pygame.draw.circle(screen, GREEN, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()
	
	
	
	
	



n=int(input("Enter Number of Players in range of 2 to 4 "))
if n<2 or n>4:
	print("wrong input")
	exit()

ROW_COUNT = int(input("Enter number of rows in range of 4 to 6 "))
if ROW_COUNT<4 or ROW_COUNT>6:
	print("wrong input")
	exit()
	
COLUMN_COUNT = int(input("Enter number of column in range of 4 to 8 "))
if COLUMN_COUNT<4 or COLUMN_COUNT>8:
	print("wrong input")
	exit()

lst= getlist(n)
postdata(COLUMN_COUNT,ROW_COUNT,n,lst)

SIZE=ROW_COUNT*COLUMN_COUNT
board = create_board()

game_over = False
turn = 0
d=0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75*width//700)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			label = myfont.render(lst[turn][1]+"'s turn", 1, WHITE)
			screen.blit(label, (40,10))
			
			if turn == 0:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			elif turn == 2:
				pygame.draw.circle(screen, C, (posx, int(SQUARESIZE/2)), RADIUS)
			elif turn == 3:
				pygame.draw.circle(screen, GREEN, (posx, int(SQUARESIZE/2)), RADIUS)
			else: 
				pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == 0:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 1)

					if winning_move(board, 1):
						label = myfont.render(lst[0][1]+" wins!!", 1, RED)
						wins(str(lst[0][0]))
						screen.blit(label, (40,10))
						game_over = True
						
			# # Ask for Player 2 Input
			elif turn == 1:				
				
				
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))
				
				

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 2)

					if winning_move(board, 2):
						label = myfont.render(lst[1][1]+" wins!!", 1, YELLOW)
						screen.blit(label, (40,10))
						wins(str(lst[1][0]))
						game_over = True
						
			# # Ask for Player 3 Input (if any)
			elif turn == 2:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 3)

					if winning_move(board, 3):
						label = myfont.render(lst[2][1]+" wins!!", 3, C)
						screen.blit(label, (40,10))
						wins(str(lst[2][0]))
						game_over = True
						
			# # Ask for Player 4 Input (if any)			
			elif turn == 3:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 4)

					if winning_move(board, 4):
						label = myfont.render(lst[3][1]+" wins!!", 4, GREEN)
						screen.blit(label, (40,10))
						wins(str(lst[3][0]))
						game_over = True
						
			# # DRAW Condition
			elif turn == -1:
				label = myfont.render("DRAW", -1, RED)
				screen.blit(label, (40,10))
				game_over = True


			draw_board(board)

			turn += 1
			d += 1
			turn = turn % n
			if d==SIZE-1:
				turn = -1

                        
if game_over:
        pygame.time.wait(6000)
        pygame.quit()
leaderboard()                               
mycursor.execute("SELECT wins.Wins, p_data.Name, wins.No_M FROM wins INNER JOIN p_data ON wins.Id=p_data.Id ORDER BY `wins`.`Wins` DESC LIMIT 3;")
myresult = mycursor.fetchall()
l1=[['Wins', 'Player Username', 'Matches Played']]
for x in myresult:
        l1.append(x)
print(tabulate(l1))
