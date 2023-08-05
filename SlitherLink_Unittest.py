import unittest
from time import time
from random import randint
from SlitherLinkOfficial import Slitherlink, BoardGameGui, gui_play

# "#main()" in the main program (SlitherLinkOfficial.py) to run the test and not the game.

class SlitherLinkTest(unittest.TestCase):
    
    def test_x_play(self):
        '''
        Test on the correct positioning of the "x" on the board in the indicated position (pos = (1,0)).
        Considering the board 5x5.
        '''
        r = 1 #5x5 Matrix
        game = Slitherlink(r)
        x,y = 1,0
        game.flag_at(x,y)
        self.assertTrue(game.value_at(x,y) == "x" )
    
    def test_line1_play(self):
        '''
        Test on the correct positioning of the "|" on the board in the indicated position (pos = (0,1)).
        Considering the board 5x5.
        '''
        r = 1 #5x5 Matrix
        game = Slitherlink(r)
        x,y = 0,1
        game.play_at(x,y)
        self.assertTrue(game.value_at(x,y) == "|" )
        

    def test_line2_play(self):
        '''
        Test on the correct positioning of the "-" on the board in the indicated position (pos = (1,0)).
        Considering the board 5x5.
        '''
        r = 1 #5x5 Matrix
        game = Slitherlink(r)
        x,y = 1,0
        game.play_at(x,y)
        self.assertTrue(game.value_at(x,y) == "-" )
        
    def test_auto1(self):
        '''
        Automatism test on the number 0 (pos = (3,3) in the board).
        The positioning of the "x" in the surrounding positions is expected.
        Considering the board 5x5.
        '''
        n = 0 #Number of "x" counter
        r = 1 #5x5 Matrix
        game = Slitherlink(r)
        x,y = 3,3
        game.play_at(x,y)
        for d in game._directions:
            x_, y_ = d
            if game.value_at((x+x_),(y+y_)) == "x":
                n += 1
                
        self.assertTrue(n == 4 )
        
    def test_auto2(self):
        '''
        Automatism test on a random intersection ("+" in pos = (6,2)).
        By placing two lines in pos1 = (7,2) and pos2 = (6,3),
        the automatism is expected to act by placing two "x" in the remaining positions.
        Considering the board 5x5.
        '''
        n = 0 #Number of "x" counter
        r = 1 #5x5 Matrix
        game = Slitherlink(r)
        x,y = 7,2
        x1, y1 = 6,3
        intersection_x, intersection_y = 6,2
        game.play_at(x,y)
        game.play_at(x1,y1)
        game.play_at(intersection_x, intersection_y)
        for d in game._directions:
            x_, y_ = d
            if game.value_at((intersection_x+x_),(intersection_y+y_)) == "x":
                n += 1
                
        self.assertTrue(n == 2 )
        
    def test_game_win(self):
        '''
        Test to verify the game win.
        By placing a line in position pos = (5,2) the course will be complete with no violations and the game must be won.
        Considering the board 5x5.
        '''
        pos_list = [(3,0),(2,1),(1,2),(0,3),(1,4),(2,5),(1,6),(0,7),(0,9),(1,10),
               (3,10),(4,9),(5,8),(6,9),(7,10),(9,10),(10,9),(9,8),(8,7),(7,6),
               (5,6),(4,5),(5,4),(7,4),(9,4),(10,3),(10,1),(9,0),(8,1),(7,2),(4,1)]  #Correct path

        r = 1 #5x5 Matrix
        game = Slitherlink(r)
        for pos in pos_list:
            x_, y_ = pos
            game.play_at(x_, y_)
        x,y = 5,2 #Missing line to win the game
        game.play_at(x,y)
        self.assertTrue(game.finished)
             
    def test_unsolvable1(self):
        '''
        Test to the function unsolvable. By placing a line around one of the 4 positions around the number 0 (pos = (3,3)),
        the game should become unsolvable. Considering a line in the position to the right of 0 (line position = (4,3)).
        Considering the board 5x5.
        '''
        r = 1 #5x5 Matrix
        game = Slitherlink(r)
        x,y = 4,3
        game.play_at(x,y)
        self.assertTrue(game._unsolvable())
        
    def test_unsolvable2(self):
        '''
        Test to the function unsolvable. By placing four lines around an intersection (intersection_pos = (6,4)),
        the game should become unsolvable.
        Considering the board 5x5.
        '''
        pos_list = [(6,3),(7,4),(5,4),(6,5)]
        
        r = 1 #5x5 Matrix
        game = Slitherlink(r)
        for pos in pos_list:
            x_, y_ = pos
            game.play_at(x_, y_)
        self.assertTrue(game._unsolvable())
        
    def test_unsolvable3(self):
        '''
        Double loop test. Two loops are supposed to be on the same board, the game should become unsolvable.
        Considering the board 5x5.
        '''
        pos_loop1_list = [(9,0),(8,1),(7,2),(6,3),(7,4),(9,4),(10,3),(10,1)] #First loop
        pos_loop2_list = [(9,6),(7,6),(6,7),(6,9),(7,10),(9,10),(10,9),(10,7)] #Second loop
        
        r = 1 #5x5 Matrix
        game = Slitherlink(r)
        
        for pos in pos_loop1_list:
            x_, y_ = pos
            game.play_at(x_, y_)
        for pos in pos_loop2_list:
            x_, y_ = pos
            game.play_at(x_, y_)   
        self.assertTrue(game._unsolvable()) 

    
if __name__ == '__main__':
    unittest.main()
    
