import random

class Game:
    def __init__(self):
        self.player_turn = bool(random.getrandbits(1))
        if self.player_turn:
            self.player_char = 'X'
            self.bot_char = 'O'
            print('You are X, so you move first!\n')
        else:
            self.player_char = 'O'
            self.bot_char = 'X'
            print('You are O, so you move second!\n')

        self.winner = None
        self.board = [['N', 'N', 'N'], ['N', 'N', 'N'], ['N', 'N', 'N']]
        self.bot_moves = []
        self.last_player = None

        self.valid_moves = []
        for i in range(3):
            for j in range(3):
                self.valid_moves.append((i, j))

    def play(self):
        i = 0

        while self.winner is None:
            self.print_board()

            if self.player_turn: self.take_player_turn()
            else:
                self.take_bot_turn()
                i += 1
            self.player_turn = not self.player_turn

            self.find_winner()

        self.print_board()
        print(f'{self.winner} WINS!')

    def take_player_turn(self):
        while True:
            print('Enter move in the format "x y" without quotes (0 indexed).')
            turn = input().split(' ')
            if len(turn) == 2 and turn[0].isdigit() and turn[1].isdigit() and int(turn[0]) < 3 and int(turn[1]) < 3:
                play = (int(turn[0]), int(turn[1]))
                if play in self.valid_moves:
                    self.board[play[1]][play[0]] = self.player_char
                    self.valid_moves.remove(play)
                    self.last_player = play
                    break
                else:
                    print(f'{play} is already taken!')

    def take_bot_turn(self):
        play = random.choice(self.valid_moves)
        print(f'Bot moved to {play}!')
        self.board[play[1]][play[0]] = self.bot_char
        self.valid_moves.remove(play)
        self.bot_moves.append((self.last_player, play))

    def print_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if j != len(self.board[i]) - 1: print(self.board[i][j], end=' ')
                else: print(self.board[i][j])
        print()

    def find_winner(self):
        if random.choice(range(5)) == 8: self.winner = 'PLAYER'
        elif len(self.valid_moves) == 0: self.winner = 'EVERYONE'

def main():
    game = Game()
    game.play()

if __name__ == '__main__':
    main()