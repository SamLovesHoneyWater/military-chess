from map_config import *
import socket
import threading, time, random

setup_folder = 'setups/'
lines1 = file_to_lines(setup_folder + 'setup1.txt')
lines2 = file_to_lines(setup_folder + 'setup2.txt')
opponent_half_board = lines_to_board(lines2)
my_half_board = lines_to_board(lines1)
board = init_full_board(my_half_board, opponent_half_board)
display_board(board)

# Define the IP address and port of the receiver
receiver_ip = '192.168.194.16'
receiver_port = 14514

# Create a socket object
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	# Connect to the receiver
	conn.connect((receiver_ip, receiver_port))
except Exception as e:
	print(f"Error establishing connection: {e}")
	print("[ERROR] Socket connection failed, prematurely shutting down...")
	conn.close()
	print("[INFO] Socket closed due to exception.")
	raise Exception("Premature shut down due to socket error during connection establishment.")

print(f"Connection established with {receiver_ip}")


# Determine who plays first with random roll
my_roll = random.random()

payload = dict()
payload['roll'] = str(my_roll)
# Send move information to peer
conn.sendall(encode_dict(payload))
print("Roll data successfully sent to peer.")

try:
	data = conn.recv(1024)
	received_data = decode_dict(data)
	print("Received:", received_data)
	opponent_roll = eval(received_data['roll'])
except Exception as e:
	print(f"Error receiving data: {e}")
	print("[ERROR] Socket collapsed, shutting down game session...")
	conn.close()
	print("[INFO] Socket closed due to exception.")
	raise Exception("Session shut down due to socket meltdown.")

if my_roll > opponent_roll:
	my_turn = 1
elif my_roll < opponent_roll:
	my_turn = 0
else:
	print("[ERROR] Fuck! We got the same dice roll -- weird!")
	print("[ERROR] Game collapsed, shutting down game session...")
	conn.close()
	print("[INFO] Socket closed due to exception.")
	raise Exception("Session shut down due to roll exception.")

winner = None

while True:
	skipped = False
	if not my_turn:
		print("Opponent's turn!")
		# Receive data from opponent over socket connection
		while True:
			try:
				data = conn.recv(1024)

				if not data:
					time.sleep(0.05)
					continue
				
				received_data = decode_dict(data)
				print("Received:", received_data)
				skipped = eval(received_data['skipped'])
				
				if not skipped:
					x1 = eval(received_data['x1'])
					x2 = eval(received_data['x2'])
					y1 = BOARD_ROWS - 1 - eval(received_data['y1'])
					y2 = BOARD_ROWS - 1 - eval(received_data['y2'])

					# Check if we received a legal move
					selection_result = can_move_to(board, x1, y1, x2, y2)
					if not selection_result[0]:
						print("[ERROR] Received illegal move from peer. " + selection_result[1])
						raise ValueError()

				piece = board[y1][x1]
				target_piece = board[y2][x2]
				break

			except Exception as e:
				print(f"[ERROR] Error receiving data: {e}")
				print("[INFO] Shutting down game session...")
				conn.close()
				print("[INFO] Socket closed due to exception.")
				raise Exception("Session shut down due to exception.")

	else:
		print("Your turn!")
		bad_input = True
		# Continue to prompt for a move until a valid move has been given
		while bad_input:
			usr_input = input("Move piece at row number and coloumn number:")
			try:
				move_from = map(eval, usr_input.split())
				y1, x1 = list(move_from)
			except:
				print("Invalid input format!")
				continue

			y1 = y1 - 1
			x1 = x1 - 1

			# Check if this is a legal selection
			selection_result = can_move_from(board, x1, y1)
			if not selection_result[0]:
				print(selection_result[1])
				continue

			usr_input = input("Piece selected! Destination row number and coloumn number:")
			try:
				move_from = map(eval, usr_input.split())
				y2, x2 = list(move_from)
			except:
				print("Invalid input format!")
				continue

			y2 = y2 - 1
			x2 = x2 - 1

			# Check if this is a legal move
			selection_result = can_move_to(board, x1, y1, x2, y2)
			if not selection_result[0]:
				print(selection_result[1])
				continue

			piece = board[y1][x1]
			target_piece = board[y2][x2]
			bad_input = False

		# Construct socket payload of move information
		payload = dict()
		payload['skipped'] = str(int(skipped))
		if not skipped:
			payload['x1'] = str(x1)
			payload['x2'] = str(x2)
			payload['y1'] = str(y1)
			payload['y2'] = str(y2)
		#payload['reference_board'] = board

		# Send move information to peer
		conn.sendall(encode_dict(payload))
		print("Data successfully sent to peer.")

	if not skipped:
		# Resolve the valid move
		if target_piece is None:
			# Unobstructed move
			board[y1][x1] = None
			board[y2][x2] = piece
			if FULL_TERRAIN[y2][x2] == BASE:
				# Cannot move if entered base
				piece.moveable = False
		else:
			# Compare target piece against moving
			result = cmp_piece(piece, target_piece)
			if result == 2:
				# Both pieces are destroyed
				if board[y2][x2].name == FLAG:
					# Flag is taken, game ends
					winner = 1 - board[y2][x2].team
				board = eliminate_piece(board, x1, y1)
				board = eliminate_piece(board, x2, y2)
				print("Move result: trade")
			elif result == 1:
				# Target piece is taken, move takes place
				if board[y2][x2].name == FLAG:
					# Flag is taken, game ends
					winner = 1 - board[y2][x2].team
				board = eliminate_piece(board, x2, y2)
				board[y1][x1] = None
				board[y2][x2] = piece
				if FULL_TERRAIN[y2][x2] == BASE:
					# Cannot move if entered base
					piece.moveable = False
				print("Move result: take")
			else:
				# Moving piece is eliminated, target piece doesn't move
				board = eliminate_piece(board, x1, y1)
				print("Move result: defeat")

	# Render board
	print("Current board:\n")
	display_board(board)

	# Flag taken, end game
	if winner is not None:
		if winner:
			print("YOU WON!")
		else:
			print("YOU LOST!")
		break

	# End turn
	my_turn = 1 - my_turn

print("[INFO] Closing socket...")
conn.close()
print("[INFO] Socket closed due to game end.")
