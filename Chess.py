#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Chess Game
# Erik Sandberg, September 18, 2017


import tkinter as tk
from PIL import ImageTk, Image
import numpy as np


class Screen(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.all_images = []
        self.title("Erik's Chess")
        self.mainpath = '/Users/Erik/Desktop/python_games/Chess/'
        self.black_tile = self.mainpath + 'Black_tile.png'
        self.white_tile = self.mainpath + 'White_tile.png'
        self.yellow_tile = self.mainpath+'Yellow_tile.png'
        self.img_size = 100 # pixel dimensions of images        
        self.create_images()
        
    def create_images(self):
        self.yellow_tile = Image.open(self.yellow_tile)
        self.yellow_tile = self.yellow_tile.resize((self.img_size,self.img_size),Image.ANTIALIAS)
        self.yellow_tile = ImageTk.PhotoImage(self.yellow_tile)  
        self.white_tile = Image.open(self.white_tile)
        self.white_tile = self.white_tile.resize((self.img_size,self.img_size),Image.ANTIALIAS)
        self.white_tile = ImageTk.PhotoImage(self.white_tile)  
        self.black_tile = Image.open(self.black_tile)
        self.black_tile = self.black_tile.resize((self.img_size,self.img_size),Image.ANTIALIAS)
        self.black_tile = ImageTk.PhotoImage(self.black_tile)
        self.panel = [] # used to keep track of all images in the grid, then delete them to save memory
                
    def display(self,moving=False):
        if not moving:
            self.bind("<Button-1>", self.select)
        for unit in board.units:
            unit.update_moves()
        for i in range(board.x):
            for j in range(board.y):
                unit_on_position = False
                for unit in board.units:
                    if unit.x == i and unit.y == j:
                        img = unit.image
                        unit_on_position = True
                if unit_on_position == False:
                    if (i+j)%2 == 0: # BLACK
                        img = self.black_tile
                    else: # WHITE
                        img = self.white_tile
                if moving:
                    if [i,j] in self.moving_unit.available_moves:
                        img = self.yellow_tile                    
                self.all_images.append(img)
                self.panel.append(tk.Label(self,image=img))
                self.panel[-1].grid(row=i,column=j)

            if len(self.all_images) > board.x*board.y:
                self.all_images = self.all_images[board.x*board.y:]
                for im in self.panel[:board.x*board.y]: # destroy old images
                    im.destroy()
                self.panel = self.panel[board.x*board.y:] # Don't keep old images in memory
                
    def select(self,event):
        px = self.winfo_pointerx() - self.winfo_rootx()
        py = self.winfo_pointery() - self.winfo_rooty()
        x_grid = int((px/self.winfo_width())*board.x)
        y_grid = int((py/self.winfo_height())*board.y)
        for unit in board.units:
            if unit.x == y_grid and unit.y == x_grid: # REVERSED COORDINATES FROM TKINTER
                self.bind("<Button-1>", self.move_to)
                self.moving_unit = unit
        self.display(moving=True)
                
                
    def move_to(self,event):
        px = self.winfo_pointerx() - self.winfo_rootx()
        py = self.winfo_pointery() - self.winfo_rooty()
        x_grid = int((px/self.winfo_width())*board.x)
        y_grid = int((py/self.winfo_height())*board.y)        
        if [y_grid,x_grid] in self.moving_unit.available_moves:# or [y_grid,x_grid] == self.moving_unit.available_moves:
            self.moving_unit.x = y_grid # REVERSED COORDINATES
            self.moving_unit.y = x_grid # REVERSED COORDINATES
            for unit in board.units: # REMOVE CAPTURED UNITS
                if unit.x == self.moving_unit.x and unit.y == self.moving_unit.y and unit.unitID != self.moving_unit.unitID:
                    board.remove_unit(unit.unitID)            
        else:
            print("Can't move there!")

        try: # Breaks on game win because window is destroyed before this line
            self.display()
        except: 
            pass
        self.moving_unit = False # Clear out the moving unit
            
    def game_over(self,loser):
        toplevel = tk.Toplevel()
        size = self.img_size * board.x
        balloons = Image.open(self.mainpath + 'balloons.png')
        balloons = balloons.resize((size,size),Image.ANTIALIAS)
        balloons = ImageTk.PhotoImage(balloons)

        toplevel.minsize(width=size, height=size)
        toplevel.maxsize(width=size, height=size)
        if loser == "White":
            winner = "Black"
        else:
            winner = "White"

        button = tk.Button(toplevel,text=winner + " wins! \n Click anywhere to exit.", font=("Arial",40,"bold"), image = balloons, compound='center',command = toplevel.destroy)
        button.image = balloons
        button.pack()
        label = tk.Label(toplevel,text=winner + " wins!")
        label.pack()
        self.destroy()
        self.quit()

                          
    def run(self):
        self.display()    
        self.mainloop()
        
class Board():
    def __init__(self):
        self.x = 8
        self.y = 8
        self.units = []
    def add_unit(self,unit):
        self.units.append(unit)
        
    def remove_unit(self,unitID):
        for i, unit in enumerate(self.units):
            if unit.unitID == unitID:
                self.units.pop(i) 
                if unit.type == "king":
                    screen.game_over(unit.color)
class Piece():
    def __init__(self,x,y,unitID,color,unit_type):
        self.x = x
        self.y = y
        self.unitID = unitID
        self.type = unit_type
        self.color = color
        self.image_path = '/Users/Erik/Desktop/python_games/Chess/'+self.color+'_'+self.type+'.png'
        self.img_size = 100
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((self.img_size,self.img_size),Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)        
class Pawn():
    def __init__(self,x,y,unitID,color):
        Piece.__init__(self,x,y,unitID,color,'pawn')
        self.x_start = x
        self.y_start = y
        self.update_moves()
        
    def update_moves(self):
        self.available_moves = []
        can_double_jump = True
        if self.color == "White":
            self.available_moves.append([self.x+1,self.y]) # Jump one
            if self.x_start == self.x and self.y_start == self.y: # Jump 2 on first move
                #double_jump = [self.x+2,self.y]
                for unit in board.units:
                    if [unit.x,unit.y] == [self.x+1,self.y]:
                        can_double_jump = False
                if can_double_jump:
                    self.available_moves.append([self.x+2,self.y]) # Double jump
            mask = np.ones(len(self.available_moves)).astype(bool)
            for unit in board.units:
                if [unit.x,unit.y] in self.available_moves:
                    mask[self.available_moves.index([unit.x,unit.y])] = 0
            self.available_moves = np.array(self.available_moves)[mask].tolist()
            for unit in board.units:
                if unit.color != "White" and (self.y == unit.y+1 or self.y == unit.y-1) and (self.x == unit.x-1):
                    self.available_moves.append([unit.x,unit.y])                
        elif self.color == "Black":
            self.available_moves.append([self.x-1,self.y]) 
            if self.x_start == self.x and self.y_start == self.y: # Double jump
                for unit in board.units:
                    if [unit.x,unit.y] == [self.x-1,self.y]:
                        can_double_jump = False
                if can_double_jump:
                    self.available_moves.append([self.x-2,self.y]) # Double jump
            mask = np.ones(len(self.available_moves)).astype(bool)
            for unit in board.units:
                if [unit.x,unit.y] in self.available_moves:
                    mask[self.available_moves.index([unit.x,unit.y])] = 0
            self.available_moves = np.array(self.available_moves)[mask].tolist()
            for unit in board.units:
                if unit.color != "Black" and (self.y == unit.y+1 or self.y == unit.y-1) and (self.x == unit.x+1):
                    self.available_moves.append([unit.x,unit.y])                      
        



class Rook():
    def __init__(self,x,y,unitID,color):
        Piece.__init__(self,x,y,unitID,color,'rook')
        self.update_moves()
    def update_moves(self):
        self.available_moves = []
        for i in range(board.x):
            if i != self.y:
                self.available_moves.append([self.x,i])
            if i != self.x:
                self.available_moves.append([i,self.y])
        mask = np.ones(len(self.available_moves)).astype(bool)


        for unit in board.units:
            # STRAIGHT UP
            if ([unit.x,unit.y] in self.available_moves) and (unit.x < self.x) and (unit.y == self.y):
                for move in self.available_moves:
                    if unit.color == self.color:
                        if move[0] < (unit.x+1):
                            mask[self.available_moves.index(move)] = 0
                    if unit.color != self.color:
                        if move[0] < unit.x:
                            mask[self.available_moves.index(move)] = 0                            
                        
            # STRAIGHT DOWN
            if ([unit.x,unit.y] in self.available_moves) and (unit.x > self.x) and (unit.y == self.y):
                for move in self.available_moves:
                    if unit.color == self.color:
                        if move[0] > (unit.x-1):
                            mask[self.available_moves.index(move)] = 0
                    if unit.color != self.color:
                        if move[0] > unit.x:
                            mask[self.available_moves.index(move)] = 0    
                            
            
            # STRAIGHT RIGHT
            if ([unit.x,unit.y] in self.available_moves) and (unit.x == self.x) and (unit.y > self.y):
                for move in self.available_moves:
                    if unit.color == self.color:
                        if move[1] > (unit.y-1):
                            mask[self.available_moves.index(move)] = 0
                    if unit.color != self.color:
                        if move[1] > (unit.y):
                            mask[self.available_moves.index(move)] = 0                            
                                              
            
           # STRAIGHT LEFT
            if ([unit.x,unit.y] in self.available_moves) and (unit.x == self.x) and (unit.y < self.y):
                for move in self.available_moves:
                    if unit.color == self.color:
                        if move[1] < (unit.y+1):
                            mask[self.available_moves.index(move)] = 0
                    if unit.color != self.color:
                        if move[1] < (unit.y):
                            mask[self.available_moves.index(move)] = 0                            
                                                                                  
                        
        self.available_moves = np.array(self.available_moves)[mask].tolist()
        


        
                    
class Knight():
    def __init__(self,x,y,unitID,color):
        Piece.__init__(self,x,y,unitID,color,'knight')
        self.update_moves()
    def update_moves(self):
        self.available_moves = []

        self.available_moves.append([self.x+1,self.y+2])
        self.available_moves.append([self.x+1,self.y-2])
        self.available_moves.append([self.x-1,self.y+2])
        self.available_moves.append([self.x-1,self.y-2])
        self.available_moves.append([self.x+2,self.y+1])
        self.available_moves.append([self.x+2,self.y-1])
        self.available_moves.append([self.x-2,self.y+1])
        self.available_moves.append([self.x-2,self.y-1])        
        mask = np.ones(len(self.available_moves)).astype(bool)
        for unit in board.units:
            if [unit.x,unit.y] in self.available_moves and unit.color == self.color:
                i = self.available_moves.index([unit.x,unit.y])
                mask[i] = 0
        self.available_moves = (np.array(self.available_moves)[mask]).tolist()
                
class Bishop():
    def __init__(self,x,y,unitID,color):
        Piece.__init__(self,x,y,unitID,color,'bishop')
        self.update_moves()
    def update_moves(self):
        self.available_moves = []
        
        for i in range(board.x):
            self.available_moves.append([self.x+i,self.y+i])
            self.available_moves.append([self.x-i,self.y+i])
            self.available_moves.append([self.x+i,self.y-i])
            self.available_moves.append([self.x-i,self.y-i])
        mask = np.ones(len(self.available_moves)).astype(bool)
        for i,move in enumerate(self.available_moves):
            if [self.x,self.y] == move:
                mask[i] = 0
        for unit in board.units:
            # DOWN RIGHT (increasing x and y)
            if ([unit.x,unit.y] in self.available_moves) and (unit.x > self.x) and (unit.y > self.y):
                for move in self.available_moves:
                    if unit.color == self.color:
                        if move[0] > (unit.x-1) and move[1] > (unit.y-1):
                            mask[self.available_moves.index(move)] = 0
                    if unit.color != self.color:
                        if move[0] > unit.x and move[1] > unit.y:
                            mask[self.available_moves.index(move)] = 0
            # UP RIGHT
            if ([unit.x,unit.y] in self.available_moves) and (unit.x < self.x) and (unit.y > self.y):
                for move in self.available_moves:
                    if unit.color == self.color:
                        if move[0] < (unit.x+1) and move[1] > (unit.y-1):
                            mask[self.available_moves.index(move)] = 0
                    if unit.color != self.color:
                        if move[0] < unit.x and move[1] > unit.y:
                            mask[self.available_moves.index(move)] = 0
            # DOWN LEFT
            if ([unit.x,unit.y] in self.available_moves) and (unit.x > self.x) and (unit.y < self.y):
                for move in self.available_moves:
                    if unit.color == self.color:
                        if move[0] > (unit.x-1) and move[1] < (unit.y+1):
                            mask[self.available_moves.index(move)] = 0
                    if unit.color != self.color:
                        if move[0] > unit.x and move[1] < unit.y:
                            mask[self.available_moves.index(move)] = 0
            # UP LEFT
            if ([unit.x,unit.y] in self.available_moves) and (unit.x < self.x) and (unit.y < self.y):
                for move in self.available_moves:
                    if unit.color == self.color:
                        if move[0] < (unit.x+1) and move[1] < (unit.y+1):
                            mask[self.available_moves.index(move)] = 0
                    if unit.color != self.color:
                        if move[0] < unit.x and move[1] < unit.y:
                            mask[self.available_moves.index(move)] = 0                            
                            
        self.available_moves = np.array(self.available_moves)[mask].tolist()
                        
                    
        
           
class King():
    def __init__(self,x,y,unitID,color):
        Piece.__init__(self,x,y,unitID,color,'king')
        self.update_moves()
    def update_moves(self):
        self.available_moves = []        
        for i in range(self.x-1,self.x+2):
            for j in range(self.y-1,self.y+2):
                self.available_moves.append([i,j])
        mask = np.ones(len(self.available_moves)).astype(bool)
        for unit in board.units:
            if [unit.x,unit.y] in self.available_moves and unit.color == self.color:
                mask[self.available_moves.index([unit.x,unit.y])] = 0
                
        self.available_moves = np.array(self.available_moves)[mask].tolist()
            
        
class Queen():
    def __init__(self,x,y,unitID,color):
        Piece.__init__(self,x,y,unitID,color,'queen')
        self.update_moves()
    def update_moves(self):
        self.available_moves = [] 
              
        for i in range(board.x):
            self.available_moves.append([self.x+i,self.y+i])
            self.available_moves.append([self.x-i,self.y+i])
            self.available_moves.append([self.x+i,self.y-i])
            self.available_moves.append([self.x-i,self.y-i]) # Bishop
            self.available_moves.append([self.x,i]) # Rook
            self.available_moves.append([i,self.y]) # Rook
        mask = np.ones(len(self.available_moves)).astype(bool)
        for i,move in enumerate(self.available_moves):
            if [self.x,self.y] == move:
                mask[i] = 0
        for unit in board.units:
            # DOWN RIGHT (increasing x and y)
            if ([unit.x,unit.y] in self.available_moves) and (unit.x > self.x) and (unit.y > self.y):
                for move in self.available_moves:
                    if unit.color == self.color:
                        if move[0] > (unit.x-1) and move[1] > (unit.y-1):
                            mask[self.available_moves.index(move)] = 0
                    if unit.color != self.color:
                        if move[0] > unit.x and move[1] > unit.y:
                            mask[self.available_moves.index(move)] = 0
            # UP RIGHT
            if ([unit.x,unit.y] in self.available_moves) and (unit.x < self.x) and (unit.y > self.y):
                for move in self.available_moves:
                    if unit.color == self.color:
                        if move[0] < (unit.x+1) and move[1] > (unit.y-1):
                            mask[self.available_moves.index(move)] = 0
                    if unit.color != self.color:
                        if move[0] < unit.x and move[1] > unit.y:
                            mask[self.available_moves.index(move)] = 0
            # DOWN LEFT
            if ([unit.x,unit.y] in self.available_moves) and (unit.x > self.x) and (unit.y < self.y):
                for move in self.available_moves:
                    if unit.color == self.color:
                        if move[0] > (unit.x-1) and move[1] < (unit.y+1):
                            mask[self.available_moves.index(move)] = 0
                    if unit.color != self.color:
                        if move[0] > unit.x and move[1] < unit.y:
                            mask[self.available_moves.index(move)] = 0
            # UP LEFT
            if ([unit.x,unit.y] in self.available_moves) and (unit.x < self.x) and (unit.y < self.y):
                for move in self.available_moves:
                    if unit.color == self.color:
                        if move[0] < (unit.x+1) and move[1] < (unit.y+1):
                            mask[self.available_moves.index(move)] = 0
                    if unit.color != self.color:
                        if move[0] < unit.x and move[1] < unit.y:
                            mask[self.available_moves.index(move)] = 0                            
            # STRAIGHT UP
            if ([unit.x,unit.y] in self.available_moves) and (unit.x < self.x) and (unit.y == self.y):
                for move in self.available_moves:
                    if unit.color == self.color:
                        if move[0] < (unit.x+1) and move[1] == self.y:
                            mask[self.available_moves.index(move)] = 0
                    if unit.color != self.color:
                        if move[0] < unit.x and move[1] == self.y:
                            mask[self.available_moves.index(move)] = 0                            
                        
            # STRAIGHT DOWN
            if ([unit.x,unit.y] in self.available_moves) and (unit.x > self.x) and (unit.y == self.y):
                for move in self.available_moves:
                    if unit.color == self.color:
                        if move[0] > (unit.x-1) and move[1] == self.y:
                            mask[self.available_moves.index(move)] = 0
                    if unit.color != self.color:
                        if move[0] > unit.x and move[1] == self.y:
                            mask[self.available_moves.index(move)] = 0    
                            
            
            # STRAIGHT RIGHT
            if ([unit.x,unit.y] in self.available_moves) and (unit.x == self.x) and (unit.y > self.y):
                for move in self.available_moves:
                    if unit.color == self.color:
                        if move[1] > (unit.y-1) and move[0] == self.x:
                            mask[self.available_moves.index(move)] = 0
                    if unit.color != self.color:
                        if move[1] > (unit.y) and move[0] == self.x:
                            mask[self.available_moves.index(move)] = 0                            
                                              
            
           # STRAIGHT LEFT
            if ([unit.x,unit.y] in self.available_moves) and (unit.x == self.x) and (unit.y < self.y):
                for move in self.available_moves:
                    if unit.color == self.color:
                        if move[1] < (unit.y+1) and move[0] == self.x:
                            mask[self.available_moves.index(move)] = 0
                    if unit.color != self.color:
                        if move[1] < (unit.y) and move[0] == self.x:
                            mask[self.available_moves.index(move)] = 0                            
                                                                   
                

        self.available_moves = np.array(self.available_moves)[mask].tolist()
        
        
if __name__ == "__main__":
    board = Board()
    unitID_counter = 0
    for i in range(board.x):
        board.add_unit(Pawn(1,i,unitID_counter,'White'))
        unitID_counter += 1
        board.add_unit(Pawn(6,i,unitID_counter, 'Black'))
        unitID_counter += 1
    board.add_unit(Rook(0,7,unitID_counter,'White'))
    unitID_counter += 1       
    board.add_unit(Rook(0,0,unitID_counter,'White'))
    unitID_counter += 1
    board.add_unit(Rook(7,7,unitID_counter,'Black'))
    unitID_counter += 1    
    board.add_unit(Rook(7,0,unitID_counter,'Black'))
    unitID_counter += 1        
    board.add_unit(Knight(0,1,unitID_counter,'White'))
    unitID_counter += 1
    board.add_unit(Knight(0,6,unitID_counter,'White'))
    unitID_counter += 1
    board.add_unit(Knight(7,1,unitID_counter,'Black'))
    unitID_counter += 1                
    board.add_unit(Knight(7,6,unitID_counter,'Black'))
    
    board.add_unit(Bishop(0,2,unitID_counter,'White'))
    unitID_counter += 1
    board.add_unit(Bishop(0,5,unitID_counter,'White'))
    unitID_counter += 1
    board.add_unit(Bishop(7,2,unitID_counter,'Black'))
    unitID_counter += 1                
    board.add_unit(Bishop(7,5,unitID_counter,'Black'))
    unitID_counter += 1
    board.add_unit(King(0,4,unitID_counter,'White'))
    unitID_counter += 1
    board.add_unit(Queen(0,3,unitID_counter,'White'))
    unitID_counter += 1
    board.add_unit(King(7,4,unitID_counter,'Black'))
    unitID_counter += 1                
    board.add_unit(Queen(7,3,unitID_counter,'Black'))
    unitID_counter +=1
    
    #board.add_unit(King(5,4,unitID_counter,'White'))
    #unitID_counter += 1         
    
    screen = Screen()
    screen.run()
        


    