import pygame
import os

pygame.init()

# --- Tile Class ---
class Tile:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.connectivity = [] 
        self.placed = False    
        self.rotation = 0

tiles_folder = "tiles"

t1 = Tile(os.path.join(tiles_folder, "t1.jpg"))
t1.connectivity = [(0,1),(2,5),(3,7),(4,6)]  

t2 = Tile(os.path.join(tiles_folder, "t2.jpg"))
t2.connectivity = [(0,4),(1,2),(3,7),(5,6)]

t3 = Tile(os.path.join(tiles_folder, "t3.jpg"))
t3.connectivity = [(0,2),(1,7),(3,5),(4,6)]

t4 = Tile(os.path.join(tiles_folder, "t4.jpg"))
t4.connectivity = [(0,1),(2,6),(3,5),(4,7)]

t5 = Tile(os.path.join(tiles_folder, "t5.jpg"))
t5.connectivity = [(0,2),(1,5),(3,7),(4,6)]

t6 = Tile(os.path.join(tiles_folder, "t6.jpg"))
t6.connectivity = [(0,2),(1,4),(3,7),(5,6)]

t7 = Tile(os.path.join(tiles_folder, "t7.jpg"))
t7.connectivity = [(0,2),(1,7),(3,4),(5,6)]

t8 = Tile(os.path.join(tiles_folder, "t8.jpg"))
t8.connectivity = [(0,2),(1,4),(3,6),(5,7)]

t9 = Tile(os.path.join(tiles_folder, "t9.jpg"))
t9.connectivity = [(0,1),(2,6),(3,4),(5,7)]

t10 = Tile(os.path.join(tiles_folder, "t10.jpg"))
t10.connectivity = [(0,1),(2,5),(3,6),(4,7)]

t11 = Tile(os.path.join(tiles_folder, "t11.jpg"))
t11.connectivity = [(0,2),(1,6),(3,4),(5,7)]

t12 = Tile(os.path.join(tiles_folder, "t12.jpg"))
t12.connectivity = [(0,2),(1,5),(3,6),(4,7)]

t13 = Tile(os.path.join(tiles_folder, "t13.jpg"))
t13.connectivity = [(0,1),(2,4),(3,7),(5,6)]

t14 = Tile(os.path.join(tiles_folder, "t14.jpg"))
t14.connectivity = [(0,3),(1,6),(4,7),(2,5)]

t15 = Tile(os.path.join(tiles_folder, "t15.jpg"))
t15.connectivity = [(0,1),(2,7),(3,6),(4,5)]

t16 = Tile(os.path.join(tiles_folder, "t16.jpg"))
t16.connectivity = [(0,2),(1,3),(4,6),(5,7)]

t17 = Tile(os.path.join(tiles_folder, "t17.jpg"))
t17.connectivity = [(0,4),(1,2),(3,6),(5,7)]

t18 = Tile(os.path.join(tiles_folder, "t18.jpg"))
t18.connectivity = [(0,3),(1,5),(2,6),(4,7)]

t19 = Tile(os.path.join(tiles_folder, "t19.jpg"))
t19.connectivity = [(0,1),(2,3),(4,5),(6,7)]

t20 = Tile(os.path.join(tiles_folder, "t20.jpg"))
t20.connectivity = [(0,2),(1,6),(3,5),(4,7)]

t21 = Tile(os.path.join(tiles_folder, "t21.jpg"))
t21.connectivity = [(0,1),(2,3),(4,7),(5,6)]

t22 = Tile(os.path.join(tiles_folder, "t22.jpg"))
t22.connectivity = [(0,1),(2,3),(4,6),(5,7)]

t23 = Tile(os.path.join(tiles_folder, "t23.jpg"))
t23.connectivity = [(0,3),(1,4),(2,7),(5,6)]

t24 = Tile(os.path.join(tiles_folder, "t24.jpg"))
t24.connectivity = [(0,1),(2,7),(3,4),(5,6)]

t25 = Tile(os.path.join(tiles_folder, "t25.jpg"))
t25.connectivity = [(0,3),(1,2),(4,7),(5,6)]

t26 = Tile(os.path.join(tiles_folder, "t26.jpg"))
t26.connectivity = [(0,1),(2,7),(3,5),(4,6)]

t27 = Tile(os.path.join(tiles_folder, "t27.jpg"))
t27.connectivity = [(0,3),(1,4),(3,6),(5,7)]

t28 = Tile(os.path.join(tiles_folder, "t28.jpg"))
t28.connectivity = [(0,2),(1,3),(4,7),(5,6)]

t29 = Tile(os.path.join(tiles_folder, "t29.jpg"))
t29.connectivity = [(0,1),(2,4),(3,6),(5,7)]

t30 = Tile(os.path.join(tiles_folder, "t30.jpg"))
t30.connectivity = [(0,1),(2,6),(3,7),(4,5)]

# --- List of all tiles ---
tiles = [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10,
         t11, t12, t13, t14, t15, t16, t17, t18, t19, t20,
         t21, t22, t23, t24, t25, t26, t27, t28, t29, t30]