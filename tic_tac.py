import socket


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


def enlarge_board(board, row, col):
    current_rows = len(board)
    current_cols = len(board[0])

    # Enlarge rows if needed
    while row >= len(board):
        board.append([' ' for _ in range(current_cols)])

    # Enlarge columns if needed
    for r in board:
        while col >= len(r):
            r.append(' ')


def PlayServe():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(1)
    print("Server is listening...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")
    starting_player = 'X'
    client_socket.send(starting_player.encode())

    while True:
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
        row, col = map(int, input("Enter your move (row,col): ").split(','))
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


def PlayClient():
    ip = input("Enter server IP: ")
    port = 9999
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    starting_player = client_socket.recv(1024).decode()
    print(f"Starting player is: {starting_player}")

    while True:
        row, col = map(int, input("Enter your move (row,col): ").split(','))
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
board = [[' ' for _ in range(3)] for _ in range(3)]
boardSting = printBoard(board)
print (boardSting)
if mode == "Serve":
    print("mode server")
    PlayServe()
else:
    print("mode cliant")
    PlayClient()
