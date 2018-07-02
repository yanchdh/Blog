# -*- coding: utf-8 -*-

CHESS_PIECE_NAME_LIST = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Pawn']

CHESS_BOARD_SIZE = 8

CHESS_PIECE_MOVE_RULES = {
	'R': [(1, 0, 7), (0, 1, 7), ],
	'r': [(1, 0, 7), (0, 1, 7), ],
	'N': [(1, 2, 1), (1, -2, 1), (-1, -2, 1), (-1, 2, 1), (2, 1, 1), (2, -1, 1), (-2, -1, 1), (-2, 1, 1), ],
	'n': [(1, 2, 1), (1, -2, 1), (-1, -2, 1), (-1, 2, 1), (2, 1, 1), (2, -1, 1), (-2, -1, 1), (-2, 1, 1), ],
	'B': [(1, 1, 7), (1, -1, 7), (-1, -1, 7), (-1, 1, 7), ],
	'b': [(1, 1, 7), (1, -1, 7), (-1, -1, 7), (-1, 1, 7), ],
	'Q': [(1, 1, 7), (1, -1, 7), (-1, -1, 7), (-1, 1, 7), (0, 1, 7), (0, -1, 7), (1, 0, 7), (-1, 0, 7), ],
	'q': [(1, 1, 7), (1, -1, 7), (-1, -1, 7), (-1, 1, 7), (0, 1, 7), (0, -1, 7), (1, 0, 7), (-1, 0, 7), ],
	'K': [(1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1), (0, 1, 1), (0, -1, 1), (1, 0, 1), (-1, 0, 1), ],
	'k': [(1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1), (0, 1, 1), (0, -1, 1), (1, 0, 1), (-1, 0, 1), ],
	'P': [(0, -1, 1), ],
	'p': [(0, 1, 1), ],
}

CHESS_PIECE_ATTACK_RULES = {
	'P': [(-1, -1, 1), (1, -1, 1), ],
	'p': [(-1, 1, 1), (1, 1, 1), ]
}

def singleton(cls, *args, **kw):
	instances = {}

	def _singleton():
		if cls not in instances:
			instances[cls] = cls(*args, **kw)
		return instances[cls]

	return _singleton

@singleton
class ChessHelper(object):
	def __init__(self):
		self.board_dict = [[{} for j in xrange(CHESS_BOARD_SIZE)] for i in xrange(CHESS_BOARD_SIZE)]
		for i in xrange(CHESS_BOARD_SIZE):
			for j in xrange(CHESS_BOARD_SIZE):
				for key, move_rules in CHESS_PIECE_MOVE_RULES.iteritems():
					move_points = []
					for rule in move_rules:
						points = self.get_points_by_rule(i, j, rule)
						points and move_points.append(points)
					self.board_dict[i][j].setdefault(key, {})['move_points'] = move_points

				for key, attack_rules in CHESS_PIECE_ATTACK_RULES.iteritems():
					attack_points = []
					for rule in attack_rules:
						points = self.get_points_by_rule(i, j, rule)
						points and attack_points.append(points)
					self.board_dict[i][j].setdefault(key, {})['attack_points'] = attack_points
		# print self.board_dict

	def is_valid_point(self, x, y):
		return 0 <= x < CHESS_BOARD_SIZE and 0 <= y < CHESS_BOARD_SIZE

	def get_points_by_rule(self, x, y, rule):
		points = []
		for i in xrange(rule[-1]):
			x += rule[0]
			y += rule[1]
			if self.is_valid_point(x, y):
				points.append((x, y, ))
		return points

class ChessBoard(object):
	def __init__(self):
		self.board = [
			['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'], # 8
			['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], # 7
			['*', '*', '*', '*', '*', '*', '*', '*'], # 6
			['*', '*', '*', '*', '*', '*', '*', '*'], # 5
			['*', '*', '*', '*', '*', '*', '*', '*'], # 4
			['*', '*', '*', '*', '*', '*', '*', '*'], # 3
			['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], # 2
			['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'], # 1
			# a    b    c    d    e    f    g    h
		]

	def show(self):
		for row in self.board:
			print ''.join(row)

ChessBoard().show()
ChessHelper()