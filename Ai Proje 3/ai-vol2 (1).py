import time
import random
import copy
import numpy as np

player_1_SOS = []
player_1_SOS_predicted = []

player_2_SOS = []
player_2_SOS_predicted = []

def sos_game():
    board = [['S', ' ', ' ', ' ', 'S'],
             [' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             [' ', ' ', ' ', ' ', ' '],
             ['S', ' ', ' ', ' ', 'S']]
    return board

def players():
    players = [('Player 1',0), ('Player 2',0)]  # human vs ai = player 1 vs player 2
    return players

def print_board(board):
   for _ in board:
        print(_)

def get_move():
    move = input('Enter row column and letter: ')
    move = move.split(' ')
    move[0] = int(move[0])
    move[1] = int(move[1])
    move[2] = move[2].upper()
    return move

def check_move(move, board):
    if move[0] > 4 or move[0] < 0 or move[1] > 4 or move[1] < 0:
        return False
    elif board[move[0]][move[1]] != ' ':
        return False
    else:
        return True

def update_board(move, board):
    board[move[0]][move[1]] = move[2]
    return board

def add_player_SOS_move(row_col_first_s, row_col_o, row_col_second_s, player):
    if player == 'Player 1':
        player_1_SOS.append((row_col_first_s, row_col_o, row_col_second_s))
        return player_1_SOS
    else:
        player_2_SOS.append((row_col_first_s, row_col_o, row_col_second_s))
        return player_2_SOS

def add_player_SOS_predicted_move(row_col_first_s, row_col_o, row_col_second_s, player):
    if player == 'Player 1':
        player_1_SOS_predicted.append((row_col_first_s, row_col_o, row_col_second_s))
        return player_1_SOS_predicted
    else:
        player_2_SOS_predicted.append((row_col_first_s, row_col_o, row_col_second_s))
        return player_2_SOS_predicted


def check_sos_human(move, board, player):
    row, col, letter = move
    score=0
    if letter == 'O':
        # check row : 'SOS'
        if (col >= 1 and col <=3) and board[row][col - 1] == 'S' and board[row][col + 1] == 'S':
            add_player_SOS_predicted_move((row, col - 1), (row, col), (row, col + 1), player)
            score =1
        # check column: 'SOS'
        elif (row >= 1 and row <= 3) and board[row - 1][col] == 'S' and board[row + 1][col] == 'S':
            score =1
            add_player_SOS_predicted_move((row - 1, col), (row, col), (row + 1, col), player)
        # check diagonally left to right: 'SOS'
        elif (row >= 1 and col >= 1 and row <=3 and col <=3) and board[row - 1][col - 1] == 'S' and board[row + 1][col + 1] == 'S':
            score=1
            add_player_SOS_predicted_move((row - 1, col - 1), (row, col), (row + 1, col + 1), player)
        # check diagonally right to left: 'SOS'
        elif (row >= 1 and row <= 3 and col >=1 and col <= 3) and board[row - 1][col + 1] == 'S' and board[row + 1][col - 1] == 'S':
            score=1
            add_player_SOS_predicted_move((row - 1, col + 1), (row, col), (row + 1, col - 1), player)
    elif letter == 'S':
        # Check 2 left: 'SOS'
        if col >= 2 and board[row][col - 1] == 'O' and board[row][col - 2] == 'S':
            score=1
            add_player_SOS_predicted_move((row, col - 2), (row, col - 1), (row, col), player)
        # Check 2 right: 'SOS'
        elif col <= 2 and board[row][col + 1] == 'O' and board[row][col + 2] == 'S':
            score=1
            add_player_SOS_predicted_move((row, col), (row, col + 1), (row, col + 2), player)
        # Check 2 up: 'SOS'
        elif row >= 2 and board[row - 1][col] == 'O' and board[row - 2][col] == 'S':
            score=1
        # Check 2 down: 'SOS'
        elif row <= 2 and board[row + 1][col] == 'O' and board[row + 2][col] == 'S':
            score=1
            add_player_SOS_predicted_move((row, col), (row + 1, col), (row + 2, col), player)
        # Check diagonally left to right: 'SOS'
        elif row >= 2 and col >= 2 and board[row - 1][col - 1] == 'O' and board[row - 2][col - 2] == 'S':
            score=1
            add_player_SOS_predicted_move((row - 2, col - 2), (row - 1, col - 1), (row, col), player)
        # Check diagonally right to left: 'SOS'
        elif row >= 2 and col <= 2 and board[row - 1][col + 1] == 'O' and board[row - 2][col + 2] == 'S':
            score=1
            add_player_SOS_predicted_move((row - 2, col + 2), (row - 1, col + 1), (row, col), player)
        if(score):
            return True
        return False  # Return False if no matching pattern is found
def check_sos(node,move, board, player):
    row, col, letter = move
    score=0
    if letter == 'O':
        # check row : 'SOS'
        if (col >= 1 and col <=3) and board[row][col - 1] == 'S' and board[row][col + 1] == 'S':
            add_player_SOS_predicted_move((row, col - 1), (row, col), (row, col + 1), player)
            score =1
        # check column: 'SOS'
        elif (row >= 1 and row <= 3) and board[row - 1][col] == 'S' and board[row + 1][col] == 'S':
            score =1
            add_player_SOS_predicted_move((row - 1, col), (row, col), (row + 1, col), player)
        # check diagonally left to right: 'SOS'
        elif (row >= 1 and col >= 1 and row <=3 and col <=3) and board[row - 1][col - 1] == 'S' and board[row + 1][col + 1] == 'S':
            score=1
            add_player_SOS_predicted_move((row - 1, col - 1), (row, col), (row + 1, col + 1), player)
        # check diagonally right to left: 'SOS'
        elif (row >= 1 and row <= 3 and col >=1 and col <= 3) and board[row - 1][col + 1] == 'S' and board[row + 1][col - 1] == 'S':
            score=1
            add_player_SOS_predicted_move((row - 1, col + 1), (row, col), (row + 1, col - 1), player)
    elif letter == 'S':
        # Check 2 left: 'SOS'
        if col >= 2 and board[row][col - 1] == 'O' and board[row][col - 2] == 'S':
            score=1
            add_player_SOS_predicted_move((row, col - 2), (row, col - 1), (row, col), player)
        # Check 2 right: 'SOS'
        elif col <= 2 and board[row][col + 1] == 'O' and board[row][col + 2] == 'S':
            score=1
            add_player_SOS_predicted_move((row, col), (row, col + 1), (row, col + 2), player)
        # Check 2 up: 'SOS'
        elif row >= 2 and board[row - 1][col] == 'O' and board[row - 2][col] == 'S':
            score=1
        # Check 2 down: 'SOS'
        elif row <= 2 and board[row + 1][col] == 'O' and board[row + 2][col] == 'S':
            score=1
            add_player_SOS_predicted_move((row, col), (row + 1, col), (row + 2, col), player)
        # Check diagonally left to right: 'SOS'
        elif row >= 2 and col >= 2 and board[row - 1][col - 1] == 'O' and board[row - 2][col - 2] == 'S':
            score=1
            add_player_SOS_predicted_move((row - 2, col - 2), (row - 1, col - 1), (row, col), player)
        # Check diagonally right to left: 'SOS'
        elif row >= 2 and col <= 2 and board[row - 1][col + 1] == 'O' and board[row - 2][col + 2] == 'S':
            score=1
            add_player_SOS_predicted_move((row - 2, col + 2), (row - 1, col + 1), (row, col), player)
    if(score):
        if(player =='Player 2'):
            node.player_2_score +=1 
        else:
            node.player_1_score +=1
        return True
    return False  # Return False if no matching pattern is found

def sos_game_start():
    board = sos_game()
    players_list = players()
    player_1, player_1_score = players_list[0]
    player_2, player_2_score = players_list[1]
    
    print_board(board)    
    player = player_1  # Player 1 starts the game
    while any(' ' in row for row in board):
        #time.sleep(1) ai vs ai
        print(f"current situation: player-1: {player_1_score} - player-2: {player_2_score}")
        print(f"{player} playing:")
        # move = get_move()
        # while not check_move(move, board):
        #     print('invalid move')
        #     print(f"{player} playing again:")
        #     move = get_move()
        if player == player_1:
            move = get_move()
            while not check_move(move, board):
                print('Invalid move')
                print(f"{player} playing again: ")
                move = get_move()
            #move = ai_move(board)
        else:
            move = ai_move(board)    
        print(f"{player} Move: {move}")
        update_board(move, board)
        print_board(board)
        
        if check_sos_human(move, board, player):
            if player == player_1:
               player_1_score += 1
               print(f"{player} found SOS !!! Score: {player_1_score}")
            else:
                player_2_score += 1
                print(f"{player} found SOS !!! Score: {player_2_score}")
        #switch player 
        if player == player_1:
            player = player_2
        else:
            player = player_1
        #print(f"player_1_sos: {player_1_SOS}")
        #print(f"player_2_sos: {player_2_SOS}")
        #print("\n")
#sos_game_start() 3#############33###########

def count_sos(board):
    # find "S" "O" "S" pattern in board
    rows, cols = len(board), len(board[0])
    player_1_SOS_count = 0
    player_2_SOS_count = 0
    error_sos_count = 0
    
    #check rows
    for row in range(rows):
        for col in range(cols - 2):
            if board[row][col] == 'S' and board[row][col + 1] == 'O' and board[row][col + 2] == 'S':
                if ((row, col), (row, col + 1), (row, col + 2)) in player_1_SOS:
                    player_1_SOS_count += 1
                elif ((row, col), (row, col + 1), (row, col + 2)) in player_2_SOS:
                    player_2_SOS_count += 1
                else:
                    error_sos_count += 1
    
    # Check columns
    for col in range(cols):
        for row in range(rows - 2):
            if board[row][col] == 'S' and board[row + 1][col] == 'O' and board[row + 2][col] == 'S':
                if ((row, col), (row + 1, col), (row + 2, col)) in player_1_SOS:
                    player_1_SOS_count += 1
                elif ((row, col), (row + 1, col), (row + 2, col)) in player_2_SOS:
                    player_2_SOS_count += 1
                else:
                    error_sos_count += 1
    
    # Check diagonals (left to right)
    for row in range(rows - 2):
        for col in range(cols - 2):
            if board[row][col] == 'S' and board[row + 1][col + 1] == 'O' and board[row + 2][col + 2] == 'S':
                if ((row, col), (row + 1, col + 1), (row + 2, col + 2)) in player_1_SOS:
                    player_1_SOS_count += 1
                elif ((row, col), (row + 1, col + 1), (row + 2, col + 2)) in player_2_SOS:
                    player_2_SOS_count += 1
                else:
                    error_sos_count += 1
    
    # Check diagonals (right to left)
    for row in range(rows - 2):
        for col in range(2, cols):
            if board[row][col] == 'S' and board[row + 1][col - 1] == 'O' and board[row + 2][col - 2] == 'S':
                if ((row, col), (row + 1, col - 1), (row + 2, col - 2)) in player_1_SOS:
                    player_1_SOS_count += 1
                elif ((row, col), (row + 1, col - 1), (row + 2, col - 2)) in player_2_SOS:
                    player_2_SOS_count += 1
                else:
                    error_sos_count += 1
    
    return player_1_SOS_count, player_2_SOS_count, error_sos_count


def heuristic_one(node, maximizing_player):
    ## heuristic function to evaluate board  (takes difference of scores)
    ## AI ve Player ın hareketlerini tutan listeleri oluştur. AI ve Player hareket yaptığında, hareketi listeye ekle.
    ## aldığı board'da SOS leri arasın. SOS bulduğunda, row ve col değerlerini, AI ve Player oyuncularının hareketlerinin tutulduğu liste ile karşılaştırıp, hareket kiminse ona göre puan versi
    if maximizing_player:
        return node.player_2_score - node.player_1_score
    else:
        return node.player_1_score - node.player_2_score
    
def heuristic_two(board, player):
    ## heuristic 2 function to evaluate board
    pass
def copy_board(original_board):
    size = len(original_board)
    new_board = [[' ' for _ in range(size)] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            new_board[i][j] = original_board[i][j]

    return new_board


def generate_possible_moves(board):
    moves = []
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == ' ':
                moves.append((row, col, 'O'))
                moves.append((row, col, 'S'))
    #random.shuffle(moves)
    return moves

def undo_move(move, board, current_player):
    global player_1_SOS_predicted, player_2_SOS_predicted
    board[move[0]][move[1]] = ' '
    #print(player_2_SOS_predicted, move, board, current_player

    return board

def ai_move(board):
    
    root_node = Node(board,0,0)
    _, best_move = minimax(root_node,1, True, float('-inf'), float('inf'))
    return best_move
class Node:
    def __init__(self, board, player_1_score,player_2_score):
        self.board = board
        self.player_1_score = player_1_score
        self.player_2_score = player_2_score
        self.children = []

    def add_child(self, child):
        self.children.append(child)

def minimax(node,depth, maximizing_player, alpha, beta):
    # if depth == 0 or not any(' ' in row for row in node.board):
    if depth == 0:
        return heuristic_one(node, maximizing_player), None
    
    if maximizing_player:
        max_eval = float('-inf')
        best_move = None

        for move in generate_possible_moves(node.board):
            new_board = copy_board(node.board)
            update_board(move, new_board)
            child_node = Node(new_board,node.player_1_score,node.player_2_score) 
            check_sos(child_node,move, new_board, 'Player 1')
            node.add_child(child_node)
            eval, _ = minimax(child_node, depth - 1, False, alpha, beta)
        
            
            max_eval = max(max_eval, eval)
            alpha = max(alpha, max_eval)
                
            if beta <= alpha:
                break
            if eval == max_eval:
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None        
        for move in generate_possible_moves(node.board):
            new_board = copy_board(node.board)
            update_board(move,new_board)
            child_node = Node(new_board,node.player_1_score,node.player_2_score) 
            check_sos(child_node,move, new_board, 'Player 2')
            node.add_child(child_node)
            eval, _ = minimax(node.board, depth - 1, True, alpha, beta)
            
                
            min_eval = min(min_eval, eval)
            beta = min(beta, min_eval)

            if beta <= alpha:
                break
            if eval == min_eval:
                best_move = move
        return min_eval, best_move

sos_game_start()