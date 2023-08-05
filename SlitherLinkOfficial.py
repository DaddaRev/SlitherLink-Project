'''
SlitherLink by Davide Reverberi. Mat: 332781
'''
import g2d
from time import time
from random import randint

#Press the H key to get help (to know if the game is unsolvable)

#1) Fare Unittest

W, H = 40, 40
LONG_PRESS = 0.5

def abstract():
    raise NotImplementedError("Abstract method")

class BoardGame:
    def play_at(self, x: int, y: int): abstract()
    def flag_at(self, x: int, y: int): abstract()
    def value_at(self, x: int, y: int) -> str: abstract()
    def cols(self) -> int: abstract()
    def rows(self) -> int: abstract()
    def finished(self) -> bool: abstract()
    def message(self) -> str: abstract()


def print_game(game: BoardGame):
    for y in range(game.rows()):
        for x in range(game.cols()):
            print(game.value_at(x, y), end="\t")
        print()

def console_play(game: BoardGame):
    print_game(game)

    while not game.finished():
        x, y = input().split()
        game.play_at(int(x), int(y))
        print_game(game)

    print(game.message())


class Slitherlink(BoardGame):
    def __init__(self, r):
        self._directions = [(1,0),(-1,0),(0,1),(0,-1)]  #Directions to take to control the values around 1 coordinate
        self._loop = False
        
        if r == 1:
            level = "game_5x5.txt"
        if r == 2:
            level = "game_10x10.txt"
        if r == 3:
            level = "game_18x10.txt"
        if r == 4:
            level = "game_36x20.txt"
            
        count = 0
        with open(level, "r") as board:
            for line in board:
                self._cols = len(list(line)) -1
                count += self._cols
                
        self._rows = count // self._cols
        self._board = [] * (self._cols * self._rows)
        
        with open(level, "r") as board:
            for line in board:
                for c in line:
                    if c != "\n":
                        self._board.append(c)
        
    def play_at(self,x,y):
        pos = y * self._cols +x
        if self._board[pos] == " " or self._board[pos] == "x":
            if (self._board[pos-1] == "+" and self._board[pos+1] == "+") or (self._board[(y-1) * self._cols + x] == "+" and self._board[(y+1) * self._cols + x]) :
                if y%2 == 0:
                    self._board[pos] = "-"
                else:
                    self._board[pos] = "|"
            
        elif self._board[pos] == "-" or self._board[pos] == "|":
            self._board[pos] = " "
            
        elif 48 <= ord(self._board[pos]) <= 52 or self._board[pos] == "+":
            self._autocomplete(x,y)

     
    def flag_at(self,x,y):
        pos = y * self._cols +x
        if self._board[pos] != "+":
            if (self._board[pos-1] == "+" and self._board[pos+1] == "+") or (self._board[(y-1) * self._cols + x] == "+" and self._board[(y+1) * self._cols + x]) :
                self._board[pos] = "x"
            
    def value_at(self,x,y):
        return self._board[y * self._cols + x]
    
    def cols(self):
        return self._cols
    
    def rows(self):
        return self._rows
    
    def _around(self, x, y):
        pos = y * self._cols +x
        around = []
        
        for i in self._directions:
            x_, y_ = i
            if 0 <= (x + x_) <= (self._cols - 1) and 0 <= (y + y_) <= (self._rows - 1):
                around.append(self._board[(y + y_) * self._cols + (x + x_)])
        
        #around = ["Right", "Left", "Down", "Up"]
        return around
    
    def _count_lines(self):
        '''
        Function that counts the lines in the board
        '''
        n = 0
        for i in self._board:
            if i == "-" or i == "|":
                n += 1
        return n
        
    def _change_values_around(self, x, y, sign):
        for i in self._directions:
            x_, y_ = i
            if 0 <= (x + x_) <= (self._cols - 1) and 0 <= (y + y_) <= (self._rows - 1):
                pos = (y + y_) * self._cols + (x + x_)
                if self._board[pos] == " ":
                    if sign == "l":
                        if (y + y_) %2 == 0:
                            self._board[pos] = "-"
                        else:
                            self._board[pos] = "|"
                    else:
                        self._board[pos] = sign
        
                    
    def _autocomplete(self, x,y):
        '''
        Game automatism function
        '''
        pos = y * self._cols +x
        
        if 48 <= ord(self._board[pos]) <= 52:  #If position is a number. 
            around = self._around(x,y)
            count_lines = 0
            count_space = 0
            for i in around:
                if i != " " and i != "x":
                    count_lines += 1
                elif i == " ":
                    count_space += 1
                    
            if count_lines == (ord(self._board[pos])-48):  #1) There are already the right lines → all ×
                sign = "x"
                self._change_values_around(x,y, sign)
                
            elif ((ord(self._board[pos])-48) - count_lines) == count_space: #2) n lines are missing and there are n free squares → all lines
                sign = "l"
                self._change_values_around(x,y, sign)
                      
        elif self._board[pos] == "+":  #If position is a "+"
            around = self._around(x,y)
            space_count = 0
            lines_count = 0
            for i in around:
                if i == " ":
                    space_count += 1
                if i == "-" or i == "|":
                    lines_count += 1
            
            if lines_count == 2: #1) There are already two lines → all ×
                for i in range(len(around)):
                    sign = "x"
                self._change_values_around(x,y, sign)
                
            elif space_count == 1: #2) Only one square → line or × is missing 
                if lines_count == 1:
                    sign = "l"
                else:
                    sign = "x"
                self._change_values_around(x,y, sign)
                
    def _follow(self, x,y , end, prv_pos, n):
        '''
        Recursive function used to follow a random line and verify the single loop
        '''
        self._loop = False
        pos = x,y
        if pos == end and n > 0:
            self._loop = True
            return n
        for d in self._directions:
            x_, y_ = d
            if 0 <= (x + x_) <= (self._cols - 1) and 0 <= (y + y_) <= (self._rows - 1):
                x_1 = x + x_
                y_1 = y + y_
                next_pos = x_1, y_1 #New position to check if it's a line.
                if next_pos != prv_pos and (self.value_at(x_1, y_1) == "-" or self.value_at(x_1, y_1) == "|"):
                    x1, y1 = x_1 + x_, y_1 + y_
                    return self._follow(x1,y1, end, next_pos, n+1)
            
    def _first_value(self):
        '''
        Function to understand if the first value to control is "-" or "|"
        '''
        count1, count2 = 0,0
        for i in self._board:
            if i == "-":
                count1 += 1
            if i == "|":
                count2 += 1
        if count1 > count2:
            return "-"
        else:
            return "|"
            
    def _single_loop_control(self):
        if self._count_lines() == 0: return False
        i = self._board.index(self._first_value()) #Random line from which to start the check
        x,y = (i % self._cols, i // self._cols)                #prv_pos in the function _follow
        pos = (x + x % 2, y + y % 2)                           #pos, next_pos in the function _follow
        x_, y_ = pos
        return self._follow(x_, y_, pos, (x,y), 0) == self._count_lines()
                         
    def finished(self):
        finished = True
        for y in range(self._rows):
            for x in range(self._cols):
                pos = y * self._cols +x
        
                if 48 <= ord(self._board[pos]) <= 52: #Lines around the numbers checking.
                    around = self._around(x,y)
                    count_lines = 0  #Count lines around a number
                    for i in around:
                        if i == "-" or i == "|":
                            count_lines += 1
                    if count_lines != (ord(self._board[pos]) -48):
                        finished = False
                
                if self._board[pos] == "+":  #Lines around "+" checking. It could be 0 or 2.
                    around = self._around(x,y)
                    count_lines_2 = 0 #Count lines around a "+"
                    for i in around:
                        if i == "-" or i == "|":
                            count_lines_2 += 1
                    if count_lines_2 != 0 and count_lines_2 != 2:
                        finished = False
                        
        if not self._single_loop_control():
            finished = False
                
        return finished 
    
    def _unsolvable(self):
        '''
        Function to check if the game is unsolvable or not
        '''
        unsolvable = False
        for y in range(self._rows):
            for x in range(self._cols):
                pos = y * self._cols +x
        
                if 48 <= ord(self._board[pos]) <= 52: #Lines around the numbers checking.
                    around = self._around(x,y)
                    count_x = 0  #Count x around a number
                    count_lines = 0 #Count lines around a number
                    count_space = 0 #Count spaces around a number
                    for i in around:
                        if i == "x":
                            count_x += 1
                        if i == "|" or i == "-":
                            count_lines += 1
                            
                    if count_x > (4-(ord(self._board[pos]) -48)): #Violation by excess of x around a number
                        unsolvable = True
                            
                    if count_lines > (ord(self._board[pos]) -48): #Violation by excess of lines around a number
                        unsolvable = True
                        
                if self._board[pos] == "+": #Intersections checking.
                    around = self._around(x,y)
                    count_lines = 0 #Count lines around a number
                    for i in around:
                        if i == "|" or i == "-":
                            count_lines += 1
                            
                    if count_lines >= 3: #Violation by excess of lines around an intersection.
                        unsolvable = True
                                 
        self._single_loop_control() 
        if self._loop: #If there are at least 2 closed loops then game is unsolvable
            if not self._single_loop_control():
                unsolvable = True
                        
        return unsolvable
    
    def message(self):
        return "Congratulations, You won"
        
class BoardGameGui:
    def __init__(self, g: BoardGame):
        self._game = g
        self._mouse_down = 0
        self._button_time = 51
        self.update_buttons()

    def tick(self):
        if "LeftButton" in g2d.current_keys() and self._mouse_down == 0:
            self._mouse_down = time()
        elif "LeftButton" not in g2d.current_keys() and self._mouse_down > 0:
            mouse = g2d.mouse_position()
            x, y = mouse[0] // W, mouse[1] // H
            if time() - self._mouse_down > LONG_PRESS:
                self._game.flag_at(x, y)
            else:
                self._game.play_at(x, y)
            self.update_buttons()
            self._mouse_down = 0
            
        elif "h" in g2d.current_keys() and self._button_time > 20:
            if self._game._unsolvable():
                print("Unsolvable")
            self._button_time = 0
            
        self._button_time += 1
        
    def update_buttons(self):
        g2d.clear_canvas()
        g2d.set_color((0, 0, 0))
        cols, rows = self._game.cols(), self._game.rows()
        
        for y in range(1, rows):
            g2d.draw_line((0, y * H), (cols * W, y * H))
        for x in range(1, cols):
            g2d.draw_line((x * W, 0), (x * W, rows * H))
    
        for y in range(rows):
            for x in range(cols):
                if self._game.value_at(x,y) == "x":
                    value = str(self._game.value_at(x, y))
                    center = x * W + W//2, y * H + H//2
                    g2d.set_color((255,0,0))
                    g2d.draw_text_centered(value, center, H//2)
                    
                elif self._game.value_at(x,y) == "-":
                    center_x, center_y = x * W + W//2, y * H + H//2
                    g2d.set_color((0,0,0))
                    g2d.fill_rect((center_x - W, center_y), (2*W, 2))
                    
                elif self._game.value_at(x,y) == "|":
                    center_x, center_y = x * W + W//2, y * H + H//2
                    g2d.set_color((0,0,0))
                    g2d.fill_rect((center_x, center_y - H), (2, 2*H))
                    
                elif 48 <= ord(self._game.value_at(x,y)) <= 52:
                    value = str(self._game.value_at(x, y))
                    center = x * W + W//2, y * H + H//2
                    g2d.set_color((100,100,100))
                    g2d.draw_text_centered(value, center, H//2 + H//4)
                    
                elif self._game.value_at(x,y) == "+":
                    value = str(self._game.value_at(x, y))
                    center = x * W + W//2, y * H + H//2
                    g2d.set_color((0,0,0))
                    g2d.draw_text_centered(value, center, H//2)
                         
        g2d.update_canvas()
        if self._game.finished():
            g2d.alert(self._game.message())
            g2d.close_canvas()

def gui_play(game: BoardGame):
    g2d.init_canvas((game.cols() * W, game.rows() * H))
    ui = BoardGameGui(game)
    g2d.main_loop(ui.tick)

def main():
    r = int(g2d.prompt("Inserisci la tipologia di gioco:\n1) Easy: Game 5x5\n2) Medium: Game 10x10\n3) Hard: Game18x10\n4) Very Hard: 36x20"))
    game = Slitherlink(r)
    gui_play(game)
    print_game(game)
    
main()

        






