import paho.mqtt.client as mqtt
import time

# Initialize game variables
board = [' ' for _ in range(9)]  # Empty board
player_symbol = ""                 # Player's symbol (X or O)
game_over = False                  # Flag to track if the game is over
turn = "X"                         # X starts the game

# Winning combinations
win_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
    [0, 4, 8], [2, 4, 6]              # Diagonals
]

# Prints the current state of the board.
def print_board():
    for i in range(3):
        print('|'.join(board[i*3:(i+1)*3]))
        print('-' * 5)
    print()

# Checks if the given symbol has won the game
def check_winner(symbol):
    return any(all(board[i] == symbol for i in combination) for combination in win_combinations)

# Checks if the game is a draw (no empty spaces left)
def check_draw():
    return all(space != ' ' for space in board)

# Handles incoming messages from the MQTT broker
def on_message(client, userdata, message):
    global board, game_over, turn
    move_info = message.payload.decode().split(',')
    move, symbol = int(move_info[0]), move_info[1]

    if board[move] == ' ':
        board[move] = symbol  # Update the board with the opponent's move
        print_board()  # Display the updated board

        # Check for a winner or a draw
        if check_winner(symbol):
            print(f"Player {symbol} has won!")
            game_over = True
        elif check_draw():
            print("It's a draw!")
            game_over = True

        # Switch turn to the opponent
        turn = "O" if symbol == "X" else "X"

# MQTT client setup
client = mqtt.Client()

# Choose symbol and setup opponent
player_symbol = input("Are you player X or O? ").upper()
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.subscribe("tictactoe/game")
client.loop_start()

print_board()  # Show the initial board

# Main game loop
while not game_over:
    if turn == player_symbol:  # Allow move only if it's the player's turn
        try:
            move = int(input(f"Player {player_symbol}, enter your move (0-8): "))
            if 0 <= move < 9 and board[move] == ' ':
                board[move] = player_symbol  # Update the board
                client.publish("tictactoe/game", f"{move},{player_symbol}")  # Send move to the opponent
                print_board()  # Display the updated board

                # Check for a winner or a draw
                if check_winner(player_symbol):
                    print(f"Congratulations, player {player_symbol} has won!")
                    game_over = True
                elif check_draw():
                    print("It's a draw!")
                    game_over = True
                else:
                    turn = "O" if player_symbol == "X" else "X"  # Switch turn
            else:
                print("Invalid move. Try another position.")
        except ValueError:
            print("Invalid input. Enter a number between 0 and 8.")

    time.sleep(0.1)  # Small delay to prevent tight loop

client.loop_stop()  # Stop the MQTT loop
client.disconnect()  # Disconnect the client
