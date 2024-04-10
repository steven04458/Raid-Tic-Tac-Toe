import socket
import random

def PlayServe2(server_socket, client_socket):
    board = [[' ' for _ in range(3)] for _ in range(3)]
    boardSting = printBoard(board)
    print(boardSting)
    client_socket.sendall(boardSting.encode())

    while True:
        print("Server's turn:")
        row, col = map(int, input("Enter your move (col,row): ").split(','))
    
        while not valider_mouvement(board, row, col):
            print("Invalid move. Try again.")
            row, col = map(int, input("Enter your move (col,row): ").split(','))

        board[row][col] = 'O'
        boardSting = printBoard(board)
        print(boardSting)
        client_socket.sendall(boardSting.encode())


        if checkWinner(board, 'O'):
            client_socket.sendall('lose'.encode())
            print("Server wins!")
            break
        
        client_move = client_socket.recv(1024).decode()

        row, col = map(int, client_move.split(','))
        
        while not valider_mouvement(board, row, col):
            client_socket.send("INVALID".encode())
            client_move = client_socket.recv(1024).decode()
            row, col = map(int, client_move.split(','))

        board[row][col] = 'X'

        if checkWinner(board, 'X'):
            client_socket.sendall('wins'.encode())
            print("Client wins!")
            break

        client_socket.sendall('null'.encode())
        boardSting = printBoard(board)
        print (boardSting)
        client_socket.sendall(boardSting.encode())
        

    client_socket.close()
    server_socket.close()

def valider_mouvement(board, row, col):
    if 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] == ' ':
        return True
    else:
        return False

def printBoard(board):
    boardSting = ""
    for row in board:
        boardSting += "|".join(row)
        boardSting += "\n"
        boardSting += "-" * 5 + "\n"
    return boardSting

def checkWinner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def launchServe():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("Server is listening...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")
    first=random.choice(['Serve', 'Client'])
    if first == "Serve": 
        print("you start with the 'O'")
        starting_player = "you play in 2nd with 'X'"
    else:
        print("you play in 2nd with 'O'")
        starting_player = "you start with the 'X'"
    client_socket.send(starting_player.encode())
    return server_socket, client_socket, first

def PlayServe(server_socket, client_socket):
    board = [[' ' for _ in range(3)] for _ in range(3)]
    boardSting = printBoard(board)
    print(boardSting)
    client_socket.sendall(boardSting.encode())

    while True:
        client_move = client_socket.recv(1024).decode()
        row, col = map(int, client_move.split(','))
        
        while not valider_mouvement(board, row, col):
            client_socket.send("INVALID".encode())
            client_move = client_socket.recv(1024).decode()
            row, col = map(int, client_move.split(','))

        board[row][col] = 'X'
        boardSting = printBoard(board)
        print (boardSting)
        client_socket.sendall(boardSting.encode())

        if checkWinner(board, 'X'):
            client_socket.sendall('wins'.encode())
            print("Client wins!")
            break

        print("Server's turn:")
        row, col = map(int, input("Enter your move (col,row): ").split(','))
    
        while not valider_mouvement(board, row, col):
            print("Invalid move. Try again.")
            row, col = map(int, input("Enter your move (col,row): ").split(','))

        board[row][col] = 'O'

        if checkWinner(board, 'O'):
            client_socket.sendall('lose'.encode())
            print("Server wins!")
            break

        client_socket.sendall('null'.encode())
        boardSting = printBoard(board)
        print (boardSting)
        client_socket.sendall(boardSting.encode())
        

    client_socket.close()
    server_socket.close()

def launchClient():
    ip = input("Enter server IP: ")
    port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    starting_player = client_socket.recv(1024).decode()
    print(f"Starting player is: {starting_player}")
    return client_socket

def PlayClient(client_socket):
    boardSting = client_socket.recv(1024).decode()
    print(boardSting)

    while True:
        row, col = map(int, input("Enter your move (col,row): ").split(','))
        client_socket.send(f"{row},{col}".encode())
        updated_board = client_socket.recv(1024).decode()
        print("Updated board:")
        print (updated_board)

        while updated_board == "INVALID":
            row, col = map(int, input("Enter your move (col,row): ").split(','))
            client_socket.send(f"{row},{col}".encode())
            updated_board = client_socket.recv(1024).decode()
            print("Updated board:")
            print (updated_board)

        print("Waiting for opponent's move...")
        statue = client_socket.recv(1024).decode()
        updated_board = client_socket.recv(1024).decode()
        print("Updated board:")
        print (updated_board)
        
        # Check if game over
        if "wins" == statue:
            print("Client wins!")
            break
        if "lose" == statue:
            print("Server wins!")
            break

    client_socket.close()

mode = input("pour entre en mode server taper \"Serve\" sinon juste enter ")
first= ""
client_socket= ""
server_socket=""

if mode == "Serve":
    print("mode server")
    server_socket, client_socket,first = launchServe()
else:
    print("mode client")
    client_socket=launchClient()


if first == "Client":
    if mode == "Serve":
        PlayServe(server_socket, client_socket)
    else:
        PlayClient(client_socket)
else: 
    if mode == "Serve":
        PlayServe2(server_socket, client_socket)
    else:
        PlayClient(client_socket)


