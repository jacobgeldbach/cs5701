_ROWS = 6
_COLS = 7

class Board:
    def __init__(self):
        self.grid = [[0] * _COLS for _ in range(_ROWS)]

    def is_valid_col(self, col: int) -> bool:
        return self.grid[0][col] == 0

    def get_valid_cols(self) -> list[int]:
        return [c for c in range(_COLS) if self.is_valid_col(c)]

    def drop_piece(self, col: int, player: int) -> int:
        for row in range(_ROWS - 1, -1, -1):
            if self.grid[row][col] == 0:
                self.grid[row][col] = player
                return row
        return -1

    def check_win(self, player: int) -> bool:
        g = self.grid
        for r in range(_ROWS):
            for c in range(_COLS - 3):
                if all(g[r][c + i] == player for i in range(4)):
                    return True
        for r in range(_ROWS - 3):
            for c in range(_COLS):
                if all(g[r + i][c] == player for i in range(4)):
                    return True
        for r in range(_ROWS - 3):
            for c in range(_COLS - 3):
                if all(g[r + i][c + i] == player for i in range(4)):
                    return True
        for r in range(_ROWS - 3):
            for c in range(3, _COLS):
                if all(g[r + i][c - i] == player for i in range(4)):
                    return True
        return False

    def is_draw(self) -> bool:
        return all(self.grid[0][c] != 0 for c in range(_COLS))


    def eval(self, player: int) -> float:
        opponent = 1 if player == 2 else 2

        if self.check_win(opponent):
            return float('-inf')

        if self.check_win(player):
            return float('inf')

        if self.is_draw():
            return 0

        eval_total = 0
        g = self.grid
        # Per window checks, where a window is a 4 playable sections in a row that would be a win
        for r in range(_ROWS):
            for c in range(_COLS - 3):
                count     = sum(1 for i in range(4) if g[r][c + i] == player)
                opp_count = sum(1 for i in range(4) if g[r][c + i] == opponent)
                   
                # This window is unscorable if there are both colors in it
                if (count and opp_count):
                    continue

                window_eval = (((count * 10) * count) + ((opp_count * -10) * opp_count))
                    
                # Need to prioritize not losing (blocking this window)
                if opp_count == 3:
                    window_eval = -1000

                eval_total += window_eval
                        

        for r in range(_ROWS - 3):
            for c in range(_COLS):
                count     = sum(1 for i in range(4) if g[r + i][c] == player)
                opp_count = sum(1 for i in range(4) if g[r + i][c] == opponent)
                   
                # This window is unscorable if there are both colors in it
                if (count and opp_count):
                    continue
                    
                window_eval = (((count * 10) * count) + ((opp_count * -10) * opp_count))

                # Need to prioritize not losing (blocking this window)
                if opp_count == 3:
                    window_eval = -1000

                eval_total += window_eval

        for r in range(_ROWS - 3):
            for c in range(_COLS - 3):
                count     = sum(1 for i in range(4) if g[r + i][c + i] == player)
                opp_count = sum(1 for i in range(4) if g[r + i][c + i] == opponent)
                   
                # This window is unscorable if there are both colors in it
                if (count and opp_count):
                    continue
                    
                window_eval = (((count * 10) * count) + ((opp_count * -10) * opp_count))

                # Need to prioritize not losing (blocking this window)
                if opp_count == 3:
                    window_eval = -1000

                eval_total += window_eval

        for r in range(_ROWS - 3):
            for c in range(3, _COLS):
                count     = sum(1 for i in range(4) if g[r + i][c - i] == player)
                opp_count = sum(1 for i in range(4) if g[r + i][c - i] == opponent)
                   
                # This window is unscorable if there are both colors in it
                if (count and opp_count):
                    continue
                    
                window_eval = (((count * 10) * count) + ((opp_count * -10) * opp_count))
                
                # Need to prioritize not losing (blocking this window)
                if opp_count == 3:
                    window_eval = -1000


                eval_total += window_eval

        return eval_total
