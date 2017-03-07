import chess
import chess.uci
import time


def my_next_move(state_of_the_chessboard):
	# Initialise the board with its current state
	board = chess.Board(state_of_the_chessboard)

	engine = chess.uci.popen_engine("stockfish")
	engine.uci()
	engine.ucinewgame()

	best_move = engine.go(depth=10)[0]
	print "best move: ", best_move
	board.push(best_move)
	engine.position(board)

	# Check for checkmate
	if board.is_checkmate():
		game_over = "checkmate"
	elif board.is_game_over():
		game_over = "draw"
	else:
		game_over = ""

	print board
	# print type(board.fen)
	# print str(board.fen)
	fen = str(board.fen).split("\'")[1]
	# print fen
	return fen, game_over
