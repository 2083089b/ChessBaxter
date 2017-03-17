import chess
import chess.uci
import time


def my_next_move(state_of_the_chessboard):
	# Initialise the board with its current state
	board = chess.Board(state_of_the_chessboard)

	# Check for end of the game
	if board.is_checkmate():
		game_over = "Checkmate, I lost."
	elif board.is_game_over():
		game_over = "Draw"
	else:
		game_over = ""

	fen = str(board.fen).split("\'")[1]

	if game_over != "":
		return fen, game_over

	engine = chess.uci.popen_engine("stockfish")
	engine.uci()
	engine.ucinewgame()

	best_move = engine.go(depth=10)[0]
	print "best move: ", best_move
	board.push(best_move)
	engine.position(board)

	# Check for end of the game
	if board.is_checkmate():
		game_over = "Checkmate, I won."
	elif board.is_game_over():
		game_over = "Draw"
	else:
		game_over = ""


	fen = str(board.fen).split("\'")[1]

	return fen, game_over
