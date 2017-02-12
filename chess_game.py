import chess
import chess.uci
import time

# board = chess.Board(current_state_of_the_board)
board = chess.Board()

print board, "\n"

# Chess engine
engine = chess.uci.popen_engine("stockfish")
engine.uci()
engine.ucinewgame()

best_move = engine.go(depth=5)[0]
print best_move
board.push(best_move)
print board
engine.position(board)

while(not board.is_game_over()):
	best_move = engine.go(depth=5)[0]
	print best_move

	################# CHECK VALIDITY OF THE MOVE (??chessnut??)##############
	if chess.Move.from_uci(str(best_move)) in board.legal_moves:
		board.push(best_move)
		print "\n\n", board
		engine.position(board)
		# time.sleep(1)
	else:
		print "That move is not valid"


engine.quit()

board.legal_moves
