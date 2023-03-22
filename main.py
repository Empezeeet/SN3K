
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
    STAY = 4




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
    
    async def new_frame_renderer(self, snek: list, food: list, points: int = 0, highscore: int = 0):
        """
            snek: list, (x, y)
            food: list, (x, y)
        """
        print("-" + "-" * (self.size-2) + "-")
        try:
            for i in range(self.size - 2):
                line_content = [" " for i in range(self.size - 2)]
                if (snek[1] == i): line_content[snek[0]] = "o"
                if (food[1] == i): line_content[food[0]] = "X"
                print("|" + "".join(line_content) + "|")
        except IndexError:
            pass 
        print("-" + "-" * (self.size-2) + "-")   
        print("Points: " + str(points)) 
        print("Highscore: " + str(highscore))

    
    def render_game_over_screen(self, points: int, start_time: float):
        os.system("cls")
        print("-" + "-" * self.size + "-")
        print("|" + " G A M E     O V E R ")
        print("|" + " ")
        print("|" + "Stats: ")
        print("|" + "    Points: " + str(points))
        print("|" + "    Time: " + str(round(time.time() - start_time, 2)))
        print("-" + "-" * self.size + "-")
        # Write last score to file  
        with open("last_score.txt", "w") as f:
            f.truncate(0)
            f.write(f"Points: {points}\nTime: {round(time.time() - start_time, 2)}")
class Player():
    def __init__(self, size: int = 32):
        self.direction = Direction.STAY
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
                self.fruit = [random.randint(4, self.renderer.size-4), random.randint(4, self.renderer.size-4)]
                self.points += 1
            # if out of bands end game
            if self.position[0] > self.renderer.size - 2:  
                break
            if self.position[0] < -1:  
                break
            if self.position[1] > self.renderer.size - 2:
                break
            if self.position[1] < -1:
                break
            os.system("cls")
            asyncio.run(self.renderer.new_frame_renderer(self.position, self.fruit, points=self.points))
            time.sleep(self.renderer.fps / 30)
        self.renderer.render_game_over_screen(self.points, self.start_time)
    def run(self):
        self.start_time = time.time()
        self._main()
         
def main():
    while True:
        player = Player(size=32)
        os.system(f"mode {player.renderer.size+3},{player.renderer.size+5}")
        player.run()
        if (input("Do you want to play again? (y/n): ") == "y"):
            continue
        else: 
            break
    print("Thanks for playing!")
    input("Press enter to exit...")
           
main()