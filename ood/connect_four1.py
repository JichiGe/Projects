from enum import Enum
#1 平局怎么办
#2 如果那一列全满了怎么办
class Piece(Enum):
    X = "X"
    O = "O"
    
class Player():
    def __init__(self, name: str, piece: Piece):
        self.name = name
        self.score = 0
        self.piece = piece
    def get_name(self):
        return self.name
    
    def set_score(self, score: int):
        self.score = score
        
    def get_score(self):
        return self.score
    
    def get_piece(self):
        return self.piece
    
class Board():
    def __init__(self, row: int, col: int, pieces_to_connect: int):
        self.row = row
        self.col = col
        self.pieces_to_connect = pieces_to_connect
        self.board = None
        self.init_board()
    def init_board(self) -> bool:
        self.board = [[None for _ in range(self.col)] for _ in range(self.row)]
        return True
    def check_win(self, row_index, col_index, piece) -> bool:
        if row_index < 0 or row_index >= self.row or col_index < 0 or col_index >= self.col:
            raise ValueError("out of bound")
        count = 0
        for r in range(self.row):
            if self.board[r][col_index] == piece:
                count += 1
            else:
                count = 0
            if count >= self.pieces_to_connect:
                return True
        count = 0    
        for c in range(self.col):
            if self.board[row_index][c] == piece:
                count += 1
            else:
                count = 0
            if count >= self.pieces_to_connect:
                return True
        count = 0
        for r in range(self.row):
            c = row_index + col_index - r
            if self.col > c >=0 and self.board[r][c] == piece:
                count += 1
            else:
                count = 0
            if count >= self.pieces_to_connect:
                return True
        count = 0    
        for r in range(self.row):
            c = col_index - row_index + r
            if self.col > c >=0 and self.board[r][c] == piece:
                count += 1
            else:
                count = 0
            if count >= self.pieces_to_connect:
                return True
        return False
    
    def check_full(self):
        for r in range(self.row):
            for c in range(self.col):
                if self.board[r][c] is None:
                    return False
        return True
    
    def move(self, col_index: int, piece: Piece) -> int:
        if col_index < 0 or col_index >= self.col:
            raise ValueError("Index out of range")
        if self.board[0][col_index] is not None:
            raise ValueError("The col is full now")
        for r in range(self.row - 1, -1, -1):
            
            if self.board[r][col_index] is None:
                self.board[r][col_index] = piece 
            
                return r

    def print_board(self):
        col_num = "   " + " ".join(str(c) for c in range(self.col))
        print(col_num)
        print("__________________")    
        for r in range(self.row):
            row_str = f"{r} |"
            for c in range(self.col):
                if self.board[r][c] is None:
                    row_str += ". "
                else:
                    row_str += f"{self.board[r][c].value} "
            print(row_str)
        print("________________________")
            
class Game():
    def __init__(self, board: Board, score_to_win: int):
        self.score_to_win = score_to_win
        self.players = [Player("player1", Piece.O), Player("player2", Piece.X)]
        self.board = board
        self.winner = None
    def play(self):
        while self.winner is None:
            self.board.init_board()
            self.round()
            
        print(f"Congratulations {self.winner} is the winner of the game")
    def round(self):
        while not self.board.check_full():
            for player in self.players:
                self.board.print_board()
                try:
                
                    col = input(f"{player.get_piece().name}, what col do you want to put")
                    col = int(col)
                    row = self.board.move(col, player.get_piece())
                    if self.board.check_win(row, col, player.get_piece()):
                        self.board.print_board()
                        print(f"{player.get_name()} win current round")
                        player.set_score(player.get_score() + 1)
                        if player.get_score() >= self.score_to_win:
                            self.winner = player
                        return #结束以后要返回
                    
                except ValueError as e:
                    print(f"error {e}")
                    continue
            
            if self.board.check_full():
                self.board.print_board()
                print("This game is a draw")
                return
                
    
        
    # 测试代码部分
def run_tests():
    print("开始测试...")

    # 测试棋盘初始化和满盘检查
    board = Board(6, 7, 4)
    assert board.check_full() == False, "空棋盘不应该满"
    board.init_board()
    # 手动填满棋盘
    for r in range(board.row):
        for c in range(board.col):
            board.board[r][c] = Piece.X
    assert board.check_full() == True, "填满棋盘后应满"
    board.init_board()  # 重置棋盘

    # 测试垂直获胜
    for i in range(4):
        board.board[5-i][3] = Piece.X
    assert board.check_win(2, 3, Piece.X) == True, "垂直获胜测试失败"
    board.init_board()

    # 测试水平获胜
    for i in range(4):
        board.board[5][i] = Piece.O
    assert board.check_win(5, 1, Piece.O) == True, "水平获胜测试失败"
    board.init_board()

    # 测试对角线获胜（左上到右下）
    # 设置对角线：从 (2,0) 到 (5,3)
    for i in range(4):
        board.board[2+i][0+i] = Piece.X
    assert board.check_win(5, 3, Piece.X) == True, "对角线获胜测试失败"
    board.init_board()

    # 测试反对角线获胜（右上到左下）
    # 设置反对角线：从 (2,6) 到 (5,3)
    for i in range(4):
        board.board[2+i][6-i] = Piece.O
    assert board.check_win(5, 3, Piece.O) == True, "反对角线获胜测试失败"
    board.init_board()

    # 测试 move 方法
    # 在空棋盘中，尝试在第3列落子
    row_index = board.move(3, Piece.X)
    assert board.board[row_index][3] == Piece.X, "落子测试失败"

    # 测试当列满时会抛出异常
    board.init_board()
    # 填满第0列
    for _ in range(board.row):
        board.move(0, Piece.O)
    try:
        board.move(0, Piece.X)
        assert False, "当列满时应抛出异常"
    except ValueError:
        pass

    print("所有测试通过！")

if __name__ == "__main__":
    run_tests()
    # 若要运行游戏，请取消下面代码的注释
    board = Board(6, 7, 4)
    game = Game(board, score_to_win=3)
    game.play()    
        