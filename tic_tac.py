import socket


def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)

def check_winner(board, player):
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

    board = [[' ' for _ in range(3)] for _ in range(3)]
    print_board(board)

    while True:
        client_move = client_socket.recv(1024).decode()
        row, col = map(int, client_move.split(','))

        if row >= len(board) or col >= len(board[0]):
            enlarge_board(board, row, col)

        board[row][col] = 'X'

        if check_winner(board, 'X'):
            print("Client wins!")
            break
        client_socket.sendall('\n'.join([''.join(row) for row in board]).encode())
        print("Server's turn:")
        row, col = map(int, input("Enter your move (row,col): ").split(','))

        # Place 'O' on the board
        board[row][col] = 'O'

        # Send server's move to client
        client_socket.sendall('\n'.join([''.join(row) for row in board]).encode())

        # Check if server wins
        if check_winner(board, 'O'):
            print("Server wins!")
            break

        print_board(board)

    client_socket.close()
    server_socket.close()

def PlayClient():
    ip = input("Enter server IP: ")
    port = 9999

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

    # Receive who starts
    starting_player = client_socket.recv(1024).decode()
    print(f"Starting player is: {starting_player}")

    board = [[' ' for _ in range(3)] for _ in range(3)]

    while True:
        # Make client's move
        print_board(board)
        row, col = map(int, input("Enter your move (row,col): ").split(','))
        client_socket.send(f"{row},{col}".encode())

        # Receive updated board from server
        updated_board = client_socket.recv(1024).decode()
        print("Updated board:")
        print_board(updated_board)

        # Check if game over
        if "wins" in updated_board or "draw" in updated_board:
            break

        # Make server's move
        print("Waiting for opponent's move...")
        server_move = client_socket.recv(1024).decode()
        print(server_move)
        


        # Check if game over
        if "wins" in server_move or "draw" in server_move:
            print_board(board)
            break

    client_socket.close()    

mode =input("pour entre en mode server taper \"Serve\" sinon juste enter ")

if mode == "Serve":
    print("mode server")
    PlayServe()
else:
    print("mode cliant")
    PlayClient()
