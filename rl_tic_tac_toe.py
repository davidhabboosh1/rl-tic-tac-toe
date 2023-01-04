import random
import sys

SIZE = 3 # size of the board

class Reinforcer: # runs simulated games where the robot can learn, then plays against the user
    def __init__(self, sims):
        self.sims = sims
        self.move_pts = {}
        for i in range(SIZE): # set up all possible moves with points of 0
            for j in range(SIZE):
                for k in range(SIZE):
                    for l in range(SIZE):
                        self.move_pts[((i, j), (k, l))] = 0

    def reinforce(self):
        playing = True
        sims = 0

        while playing:
            game = Game(self.move_pts, sims < self.sims)
            moves, winner = game.play()

            for move in moves: # reward wins and punish losses
                if winner == 'BOT': self.move_pts[move] = self.move_pts[move] + 1 if move in self.move_pts else 1
                elif winner == 'PLAYER': self.move_pts[move] = self.move_pts[move] - 1 if move in self.move_pts else -1

            if sims >= self.sims: # see if the user wants to play again
                resp = ''
                while resp.lower() not in ['y', 'n', 'yes', 'no']:
                    print('The bot has learned. Would you like to play again? (y/n)')
                    resp = input()

                if resp.lower() in ['n', 'no']: playing = False

            if sims < self.sims: sims += 1

class Game:
    def __init__(self, move_pts, sim):
        self.move_pts = move_pts
        self.sim = sim
        self.winner = None
        self.board = [['N' for _ in range(SIZE)] for _ in range(SIZE)]
        self.bot_moves = []
        self.last_player = None

        # determine if player or bot goes first
        self.player_turn = bool(random.getrandbits(1))
        if self.player_turn:
            self.player_char = 'X'
            self.bot_char = 'O'
            self.prints('You are X, so you move first!\n')
        else:
            self.player_char = 'O'
            self.bot_char = 'X'
            self.prints('You are O, so you move second!\n')

        self.valid_moves = []
        for i in range(SIZE): # set up all possible positions
            for j in range(SIZE):
                self.valid_moves.append((i, j))

    def play(self):
        while self.winner is None:
            self.print_board()

            if self.player_turn: self.take_player_turn()
            else: self.take_bot_turn()
            self.player_turn = not self.player_turn

            self.find_winner()

        self.print_board()
        self.prints(f'{self.winner} WINS!')
        return self.bot_moves, self.winner

    def take_player_turn(self): # take the player's turn (acts as bot if simulated)
        if self.sim:
            play = self.move_as_bot(True) # (False)
        else:
            while True:
                print('Enter move in the format "x y" without quotes (0 indexed).')
                turn = input().split(' ')
                if len(turn) == 2 and turn[0].isdigit() and turn[1].isdigit() and int(turn[0]) < 3 and int(turn[1]) < 3:
                    play = (int(turn[0]), int(turn[1]))
                    if play in self.valid_moves: break
                    else: print(f'{play} is already taken!')

        self.board[play[1]][play[0]] = self.player_char
        self.valid_moves.remove(play)
        self.last_player = play

    def take_bot_turn(self): # take the robot's turn
        play = self.move_as_bot (True) # (not self.sim)

        self.prints(f'Bot moved to {play}!')
        self.board[play[1]][play[0]] = self.bot_char
        self.valid_moves.remove(play)
        self.bot_moves.append((self.last_player, play))

    def move_as_bot(self, smart): # move as the robot. if smart, use previously learned info. otherwise be random
        if smart:
            choices = [key[1] for key in self.move_pts.keys() if key[0] == self.last_player]
            values = {move: self.move_pts[(self.last_player, move)] if move in choices else 0 for move in self.valid_moves}
            max_val = max(values.values())
            values = {k: v for k, v in values.items() if v == max_val}
        else:
            values = {k: 0 for k in self.valid_moves}

        return random.choice(list(values.keys()))

    def print_board(self): # show the board
        for row in self.board:
            for j in range(SIZE):
                if j != SIZE - 1: self.prints(row[j], end=' ')
                else: self.prints(row[j])
        self.prints()

    def find_winner(self): # set the winner if there was one
        # rows and columns
        if self.winner_from_board(self.board): return
        if self.winner_from_board(list(zip(*self.board[::-1]))): return

        # diagonals
        diags = [[], []]
        i = j = 0
        while i < len(self.board):
            diags[0].append(self.board[i][j])
            i = j = j + 1
        i = 0
        j = len(self.board) - 1
        while i < len(self.board):
            diags[1].append(self.board[i][j])
            i += 1
            j -= 1
        if self.winner_from_board(diags): return

        if len(self.valid_moves) == 0: self.winner = 'EVERYONE'

    def winner_from_board(self, board): # determine if any of the rows of a 2D list are all the same
        for row in board:
            if row.count(row[0]) == len(row):
                if self.player_char == row[0]:
                    self.winner = 'PLAYER'
                    return True
                elif self.bot_char == row[0]:
                    self.winner = 'BOT'
                    return True
        return False

    def prints(self, msg='', end='\n'): # print if not in sim
        if not self.sim: print(msg, end=end)

def main():
    if len(sys.argv) > 2:
        print('Too many arguments!')
        exit()

    if len(sys.argv) > 1:
        if not sys.argv[1].isdigit():
            print('Simulation count must be a number.')
            exit()
        reinforcer = Reinforcer(int(sys.argv[1]))
    else: reinforcer = Reinforcer(0)
    reinforcer.reinforce()

if __name__ == '__main__':
    main()