from enum import Enum
import unittest
class GridPiece(Enum):
    X = "X"
    O = "O"
    
class Player():
    def __init__(self, name):
        self.name = name
        self.score = 0
        
class Board():
    def __init__(self, row_num, col_num, pieces_to_connect):
        #this class representing a single game , player can make a move and the board can check which player wins
        self.board = [[None for _ in range(col_num)] for _ in range(row_num)]
        self.row_num = row_num
        self.col_num = col_num
        self.pieces_to_win = pieces_to_connect

    def move(self, c, grid_piece: GridPiece):
        if c < 0 or c >= self.col_num:
            raise Exception("Out of bound error")
        
        for r in range(self.row_num - 1, -1, -1):
            if self.board[r][c] is None:
                self.board[r][c] = grid_piece
                
                return r
        raise ValueError("column is full")
        
            
         
        
            
        
    def check_win(self, row, col, piece: GridPiece):
        #check horizotal
        count = 0
        for c in range(self.col_num):
            
            if self.board[row][c] == piece:
                count += 1
            else:
                count = 0
            if count >= self.pieces_to_win:
                return True
            
        
        #check vertical
        count = 0
        for r in range(self.row_num):
            
            if self.board[r][col] == piece:
                count += 1
            else:
                count = 0
            if count >= self.pieces_to_win:
                return True
        
        #check diagnal
        count = 0
        for r in range(self.row_num):
            
            c = row + col - r
            if self.board[r][c] == piece:
                count += 1
            else:
                count = 0
            if count >= self.pieces_to_win:
                return True 
        
        #check conter diagnal
        count = 0
        for r in range(self.row_num):
            
            c = col - row + r
            if self.board[r][c] == piece:
                count += 1
            else:
                count = 0
            if count >= self.pieces_to_win:
                return True
        return False
    def print_the_board(self):
        for r in self.row_num:
            for c in self.col_num:
                print(f"{self.board[r][c]} |")
class Game():
    #this class representing multiple games and when one player wins a strack, we will output a text 
    #also this game controls when to reset the board etc
    def __init__(self):
        self.inputs = self.get_game_inputs()
        self.player1 = Player(self.inputs["player1_name"])
        self.player2 = Player(self.inputs["player2_name"])
        
        self.score_to_win = self.inputs["win_num"]
    def get_game_inputs(self):
        player1_name = input("Enter player1's name")
        player2_name = input("Enter player2's name")
        while True:
            try:        
                win_num = int(input("Input the score needed to win the game"))
                break
            except ValueError:
                print("Invalid input, pls enter integer")
        while True:
            try:
                row = int(input("Input The board's row number"))
                col = int(input("Input the number of cols on the board"))
                break
            except ValueError:
                print("Invalid input, pls enter an integer")
                
        while True:
            try:        
                pieces_to_connect = int(input("Input the number of consecutive pieces in order to win"))
                
                break
            except ValueError:
                print("Invalid input, pls enter an integer")
        return {"player1_name": player1_name,
                "player2_name": player2_name,
                "win_num": win_num,
                "row": row,
                "col": col,
                "pieces_to_connect": pieces_to_connect}        
    def greeting(player: Player):
        print(f"Congratulations, {player.name} win the game!")
    def play_round(self):
        board = Board(self.inputs["row"], self.inputs["col"], self.inputs["pieces_to_connect"])
        current_player = self.player1
        current_piece = GridPiece.X
        while True:
            board.print_the_board()
            try:
                col_input = int(input(f"{current_player.name}, choose a column (0 to {self.inputs['col'] - 1})"))
                row_placed = board.move(col_input, current_piece)
            
            except ValueError as e:
                print(e)
                continue
            if board.check_win(row_placed, col_input, current_piece):
                board.print_the_board()
                print("Congratulations")
                current_player.score += 1
                break
            if all(board.board[0][col] is not None for col in range(board.col_num)):
                board.print_the_board()
                print("Tie")
                break
        if current_player == self.player1:
            current_player = self.player2
            current_piece = GridPiece.O
        else:
            current_player = self.player1
            current_piece = GridPiece.X
    def play(self):
           
        while self.player1.score < self.score_to_win and self.player2.score < self.score_to_win:
            print(f"\nCurrent Scores - {self.player1.name}: {self.player1.score}, {self.player2.name}: {self.player2.score}")
            self.play_round()
        # Determine overall winner and print final message
        if self.player1.score >= self.score_to_win:
            winner = self.player1
        else:
            winner = self.player2
        print(f"\nCongratulations, {winner.name} wins the overall game!")
        
class TestBoard(unittest.TestCase):
    def setUp(self):
        # 使用标准的 Connect 4 设置，6行7列，连续4个棋子获胜
        self.board = Board(6, 7, 4)
    
    def test_move_success(self):
        # 在空列中落子，应该放到最底部（行索引5）
        row_placed = self.board.move(3, GridPiece.X)
        self.assertEqual(row_placed, 5)
        self.assertEqual(self.board.board[5][3], GridPiece.X)
    
    def test_move_out_of_bounds(self):
        # 测试列号越界的情况
        with self.assertRaises(Exception):
            self.board.move(-1, GridPiece.X)
        with self.assertRaises(Exception):
            self.board.move(7, GridPiece.X)
    
    def test_move_column_full(self):
        # 填满第0列，再尝试在该列落子应抛出异常
        for _ in range(6):
            self.board.move(0, GridPiece.X)
        with self.assertRaises(ValueError) as cm:
            self.board.move(0, GridPiece.O)
        self.assertEqual(str(cm.exception), "column is full")
    
    def test_horizontal_win(self):
        # 构造水平胜利：在底行连续填入4个相同棋子
        for col in range(4):
            self.board.move(col, GridPiece.X)
        # 最后一次落子应该在 (5, 3)
        self.assertTrue(self.board.check_win(5, 3, GridPiece.X))
    
    def test_vertical_win(self):
        # 构造垂直胜利：在同一列连续填入4个相同棋子
        last_row = None
        for _ in range(4):
            last_row = self.board.move(0, GridPiece.O)
        self.assertTrue(self.board.check_win(last_row, 0, GridPiece.O))
    
    def test_diagonal_win(self):
        # 构造对角线胜利（\ 方向）
        # 为了构造对角线，需要依次在不同列落子，制造斜向上升的局面：
        # 预期棋子位置： (5,0), (4,1), (3,2), (2,3)
        self.board.move(0, GridPiece.X)                # (5,0)
        self.board.move(1, GridPiece.O)                # 填充辅助位置
        self.board.move(1, GridPiece.X)                # (4,1)
        # 在col2，先填充两颗辅助棋子
        self.board.move(2, GridPiece.O)
        self.board.move(2, GridPiece.O)
        self.board.move(2, GridPiece.X)                # (3,2)
        # 在col3，先填充三颗辅助棋子
        self.board.move(3, GridPiece.O)
        self.board.move(3, GridPiece.O)
        self.board.move(3, GridPiece.O)
        self.board.move(3, GridPiece.X)                # (2,3)
        self.assertTrue(self.board.check_win(2, 3, GridPiece.X))
    
    def test_antidiagonal_win(self):
        # 构造反对角线胜利 (/ 方向)
        # 预期棋子位置： (5,3), (4,2), (3,1), (2,0)
        self.board.move(3, GridPiece.O)                # (5,3)
        self.board.move(2, GridPiece.X)                # 辅助棋子
        self.board.move(2, GridPiece.O)                # (4,2)
        self.board.move(1, GridPiece.X)                # 辅助棋子
        self.board.move(1, GridPiece.X)                # 辅助棋子
        self.board.move(1, GridPiece.O)                # (3,1)
        self.board.move(0, GridPiece.X)                # 辅助棋子
        self.board.move(0, GridPiece.X)                # 辅助棋子
        self.board.move(0, GridPiece.X)                # 辅助棋子
        self.board.move(0, GridPiece.O)                # (2,0)
        self.assertTrue(self.board.check_win(2, 0, GridPiece.O))


if __name__ == "__main__":
    unittest.main()