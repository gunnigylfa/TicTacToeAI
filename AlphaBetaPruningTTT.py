#!/bin/python
import random
import copy
import time
start_time = time.time()


globvar = 0
class GameNode:

	def __init__(self):
		#Standard board 
		self.board = ['_']*9
		# Board in which X wins in the next move
		#self.board = ['X','O','X','X','O','_','_','_','O']
		#self.board = ['X','_','_','_','_','Y','_','_','_']
		self.value = 0
		self.children = []

'''
 A function that checks whether a winning strategy is on the board for either player
'''
def checkWin(board,player):
	if ( (board[0] == 'X' and board[1] == 'X' and board[2] == 'X') or #top row
			(board[3] == 'X' and board[4] == 'X' and board[5] == 'X') or #middle row
			(board[6] == 'X' and board[7] == 'X' and board[8] == 'X') or  #bottom row
			(board[0] == 'X' and board[3] == 'X' and board[6] == 'X') or #first column
			(board[1] == 'X' and board[4] == 'X' and board[7] == 'X') or # middle column
			(board[2] == 'X' and board[5] == 'X' and board[8] == 'X') or # last column
			(board[0] == 'X' and board[4] == 'X' and board[8] == 'X') or # left-right diagonal column
			(board[2] == 'X' and board[4] == 'X' and board[6] == 'X')):
			return 'X' #right-left diagonal column
	elif ( (board[0] == 'O' and board[1] == 'O' and board[2] == 'O') or #top row
			(board[3] == 'O' and board[4] == 'O' and board[5] == 'O') or #middle row
			(board[6] == 'O' and board[7] == 'O' and board[8] == 'O') or  #bottom row
			(board[0] == 'O' and board[3] == 'O' and board[6] == 'O') or #first column
			(board[1] == 'O' and board[4] == 'O' and board[7] == 'O') or # middle column
			(board[2] == 'O' and board[5] == 'O' and board[8] == 'O') or # last column
			(board[0] == 'O' and board[4] == 'O' and board[8] == 'O') or # left-right diagonal column
			(board[2] == 'O' and board[4] == 'O' and board[6] == 'O')): 
		return 'O'
	else:
		return None

'''
 A function that copies the board in a node and returns a new node with an identical board
'''
def copyBoard(node):
	tmp = GameNode()
	for i in range(len(node.board)):
		tmp.board[i] = node.board[i]
	return tmp


'''
 A function that creates a list of possible moves given the current status of the game board
'''
def possibleMoves(board,player):
	moves = []
	for i in range(len(board)):
		if board[i] == '_':
			newNode = GameNode()
			newNode.board = copy.copy(board)
			newNode.board[i] = player
			moves.append(newNode)
	return moves


'''
 A function that checks if a tie is on the board
'''
def checkTie(board):
	# If a square is unmarked, that is has '_' in it's field there is not a tie
	if '_' in board:
		return False
	else:
		return True


def minimax(node,player,a,b):
	global globvar  
	#if we are at a goalnode return it's value
	if checkWin(node.board, player) == 'X':
		node.value = 10
		return node.value
	elif checkWin(node.board, player) == 'O':
		node.value = -10
		return node.value

	if checkTie(node.board):
		return node.value
	#if our player is 'X' return max of minimax calls
	if player == 'X':
		#v = -99999999999
		node.children = possibleMoves(node.board,player)
		#vals = []
		for c in node.children:
			globvar += 1
			result = minimax(c,'O' if player == 'X' else 'X',a,b)
			if result > a:
				a = result
			if a >= b:
				return a
		return a
	#if our player is 'Y' return min of minimax calls
	if player == 'O':
		#v = 99999999999
		node.children = possibleMoves(node.board,player)
		#vals = []
		for c in node.children:
			globvar += 1
			result = minimax(c,'O' if player == 'X' else 'X',a,b)
			if result < b:
				b = result
			if b <= a:
				return b
		return b


'''
 A function that returns the value of win for a given player
'''
def setValue(player):
	return 10 if player == 'X' else -10

'''
 A  helper function that prints out the list in the form of a 3-by-3 grid
'''
def printBoard(board):
	print "-------------" 
	print board[0], " | ", board[1]," | ", board[2]
	print "-------------" 
	print board[3], " | ", board[4]," | ", board[5]
	print "-------------" 
	print board[6], " | ", board[7]," | ", board[8]
	print "-------------" 


'''
 A function that returns the next move given a current board and a player which turn it is to move
'''
def nextMove(player,board):
	moves = possibleMoves(board,player)
	#two huge numbers, a and b instead of using positive infinity and negative infinity
	a = -99999999999
	b = 99999999999
	values = []
	for move in moves:
		values.append(minimax(move,'O' if player == 'X' else 'X',a,b))
	if player == 'O':
		indexToFind = values.index(min(values))
	if player == 'X':
		indexToFind = values.index(max(values))
	print globvar
	return findIndexOfDifferentBoardElement(board,moves[indexToFind].board)


'''
 A function that finds the index of the field that we made our move into
'''
def findIndexOfDifferentBoardElement(oldBoard,newBoard):
	for i in range(len(oldBoard)):
		if oldBoard[i] != newBoard[i]:
			return mapMove(i)

'''
 A switch case statement to map the index of our boarod to a 3-by-3 grid system
'''
def mapMove(index):
	switcher = {
		0: (0,0),
		1: (0,1),
		2: (0,2),
		3: (1,0),
		4: (1,1),
		5: (1,2),
		6: (2,0),
		7: (2,1),
		8: (2,2),
	}
	print switcher.get(index)[0], switcher.get(index)[1]



#If player is X, I'm the first player.
#If player is O, I'm the second player.
player = raw_input()

#Read the board now. The board is a 3x3 array filled with X, O or _.
boardString =  raw_input()
boardString += raw_input()
boardString += raw_input()
board = list(boardString)

nextMove(player,board);  


print("--- %s seconds ---" % (time.time() - start_time))



