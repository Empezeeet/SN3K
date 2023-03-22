
import threading
import time
import keyboard
from enum import Enum
import os
import asyncio
import random
class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3




class Renderer(threading.Thread):
    def __init__(self, **kwargs):
        """
            ARGS:
                size: int, default: 32
                fps: int, default: 2
        """
        self.size = kwargs.get("size", 32)
        self.fps = kwargs.get("fps", 2)
        pass
    
    async def render_new_frame(self, snek: list, food: list) -> bool:
        """
            snek: tuple, (x, y)
            food: tuple, (x, y)
        """
        if snek[0] > self.size: 
            snek[0] = self.size
        if snek[1] > self.size-1:
            snek[1] = self.size -2
        if snek[0] < 1: 
            snek[0] = 1
        if snek[1] < 1:
            snek[1] = 0
        
        
        print("-" + "-" * self.size + "-")
        
        for i in range(self.size-2):
            #if i == snek[1]:
            #    print("|" + " " * snek[0] + "o" + " " * (self.size - snek[0] - 1) + "|")
            if i == snek[1] and i == food[1]:
                print("|" + " " * snek[0] + "o" + " " * (food[0] - snek[0] - 1) + "X" + " " * (self.size - food[0] - 1) + "|")
            elif i == snek[1]:
                print("|" + " " * snek[0] + "o" + " " * (self.size - snek[0] - 1) + "|")
            elif i == food[1]:
                print("|" + " " * food[0] + "X" + " " * (self.size - food[0] - 1) + "|")
            else: 
                print("|" + " " * self.size + "|")
            
            
        print("-" + "-" * self.size + "-")
    def render_game_over_screen(self, points: int, start_time: float):
        os.system("cls")
        print("-" + "-" * self.size + "-")
        print("|" + " G A M E     O V E R ")
        print("|" + " ")
        print("|" + "Stats: ")
        print("|" + "    Points: " + str(points))
        print("|" + "    Time: " + str(round(time.time() - start_time, 2)))
        print("-" + "-" * self.size + "-")
        with open("last_score.txt", "w") as f:
            f.truncate(0)
            f.write(f"Points: {points}\nTime: {round(time.time() - start_time, 2)}")
class Player():
    def __init__(self, size: int = 32):
        self.direction = Direction.UP
        self.position = [1, 1]
        self.renderer = Renderer(size=size, fps=2)
        self.fruit = [15, 15]
        self.points = 0
    
    def _main(self):
        
        
        while True:
            # when the player presses specific arrow key the snek will move in that direction
            if keyboard.is_pressed("up"): self.direction = Direction.UP
            elif keyboard.is_pressed("down"): self.direction = Direction.DOWN    
            elif keyboard.is_pressed("left"): self.direction = Direction.LEFT    
            elif keyboard.is_pressed("right"):self.direction = Direction.RIGHT
            
            # move snek in the direction it is moving
            if self.direction == Direction.UP: self.position[1] -= 1
            elif self.direction == Direction.DOWN: self.position[1] += 1
            elif self.direction == Direction.LEFT: self.position[0] -= 1
            elif self.direction == Direction.RIGHT: self.position[0] += 1   
            if self.position == self.fruit:
                self.fruit = [random.randint(2, self.renderer.size-2), random.randint(2, self.renderer.size-2)]
                self.points += 1
            # if out of bands end game
            if self.position[0] > self.renderer.size:  
                break
            if self.position[0] < 0:  
                break
            if self.position[1] > self.renderer.size:
                break
            if self.position[1] < -1:
                break
            os.system("cls")
            asyncio.run(self.renderer.render_new_frame(self.position, self.fruit))
            time.sleep(self.renderer.fps / 50)
        self.renderer.render_game_over_screen(self.points, self.start_time)
    def run(self):
        self.start_time = time.time()
        self._main()
            
            
            
    
        
          
def main():

    player = Player(size=48)
    os.system(f"mode {player.renderer.size+3},{player.renderer.size+5}")
    player.run()
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
           
                
if __name__ == "__main__":
    main()