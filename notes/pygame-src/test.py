#!/usr/bin/env python3

import pygame, random
pygame.init()
#colours
BROWN = (135, 100, 0)
RED= (220,20,60)
ROOF= (135,100,0)
DOOR = (100,70,45)
STREAK=  (100,120,205)
KNOB = (135,100,255)
MOON = (200, 70, 105)
STAR = (255,255,153)
WOOD = (236,167,117)
DARKRED = (139,0,0)
green = (0,50,0)
BLOOD = (255,0,0)
YELLOW = (255,98,0)

#size
SIZE = (1000, 700)  

screen = pygame.display.set_mode(SIZE)

#GROUND
pygame.draw.rect(screen, green,(0, 400, 1200, 300))



#HOUSE
pygame.draw.rect(screen, DARKRED,(233, 233, 233, 200))
#SECOND FLOOR WINDOW
pygame.draw.rect(screen, RED,(243, 243, 46, 46))
#GARAGE
pygame.draw.rect(screen, BROWN,(313, 300, 146, 133))
pygame.draw.rect(screen, RED,(323, 310, 46, 46))
pygame.draw.rect(screen, RED,(313, 243, 146, 46))
pygame.draw.line(screen, STREAK, (323,310), (343,330)) 
pygame.draw.line(screen, STREAK, (323,315), (343,335)) 

#BEDROOM WINDOW
pygame.draw.rect(screen, RED,(300, 243, 146, 46))
pygame.draw.line(screen, STREAK, (323,310), (343,330)) 
pygame.draw.line(screen, STREAK, (323,315), (343,335)) 

#roof
pointlist_3 = [(233, 233), (466, 233), (346, 156)]
pygame.draw.polygon(screen, ROOF, pointlist_3, 0)
#door
pygame.draw.rect(screen, DOOR,(243, 313, 60, 120))
pygame.draw.rect(screen, BROWN,(250, 350, 10, 20))
#barricade
pygame.draw.line(screen, WOOD, (300,233), (466,289),10) 
pygame.draw.line(screen, WOOD, (300,289), (466,240),10) 
pygame.draw.line(screen, WOOD, (243,289), (289,243),10)
pygame.draw.line(screen, WOOD, (243,289), (289,243),10)
pygame.draw.line(screen, WOOD, (243,313), (289,430),10)
pygame.draw.line(screen, WOOD, (243,430), (300,313),10)
pygame.draw.line(screen, WOOD, (300,313), (465,420),15)
pygame.draw.line(screen, WOOD, (300,420), (465,313),15)
# tombstones fence stars higher
#barracade, add more colours 


#SKY

pygame.display.flip() 
#MOON
pygame.draw.circle(screen, MOON, (700,150), 100) 
#STARS
pygame.draw.circle(screen, STAR, (800,100), 10) 
pygame.draw.circle(screen, STAR, (900,59), 10) 
pygame.draw.circle(screen, STAR, (900,29), 10) 
pygame.draw.circle(screen, STAR, (500,369), 10) 
pygame.draw.circle(screen, STAR, (300,59), 9) 
pygame.draw.circle(screen, STAR, (800,99), 8) 
pygame.draw.circle(screen, STAR, (900,24), 6) 
pygame.draw.circle(screen, STAR, (500,40), 1) 
pygame.draw.circle(screen, STAR, (110,20), 13) 
pygame.draw.circle(screen, STAR, (120,39), 11) 
pygame.draw.circle(screen, STAR, (110,20), 5)  
pygame.draw.circle(screen, STAR, (930,50), 2) 
pygame.draw.circle(screen, STAR, (100,80), 1) 
pygame.draw.circle(screen, STAR, (200,90), 3) 
pygame.draw.circle(screen, STAR, (600,20), 2) 
pygame.draw.circle(screen, STAR, (500,90), 10) 
pygame.draw.circle(screen, STAR, (400,0), 9) 
pygame.draw.circle(screen, STAR, (1000,10),7) 
pygame.draw.circle(screen, STAR, (610,40), 5) 
pygame.draw.circle(screen, STAR, (820,20), 1) 
pygame.draw.circle(screen, STAR, (200,0), 6) 
pygame.draw.circle(screen, STAR, (910,230), 10) 
pygame.draw.circle(screen, STAR, (940,240), 3) 
pygame.draw.circle(screen, STAR, (730,310), 10) 
pygame.draw.circle(screen, STAR, (50,320), 9) 
pygame.draw.circle(screen, STAR, (580,90), 8) 
pygame.draw.circle(screen, STAR, (490,270), 4) 
pygame.draw.circle(screen, STAR, (400,100), 5) 
pygame.draw.circle(screen, STAR, (40,250), 1) 
pygame.draw.circle(screen, STAR, (670,330), 2) 
pygame.draw.circle(screen, STAR, (570,60), 6) 
pygame.draw.circle(screen, STAR, (460,85), 7) 
pygame.draw.circle(screen, STAR, (870,334), 8) 
pygame.draw.circle(screen, STAR, (170,260), 6) 
pygame.draw.circle(screen, STAR, (920,40), 10) 
pygame.draw.circle(screen, STAR, (920,130), 4) 


pygame.draw.line(screen, STREAK, (243,243), (263,263)) 

pygame.draw.line(screen, STREAK, (243,248), (263,268)) 


pygame.draw.line(screen, STREAK, (313,243), (333,262)) 
pygame.draw.line(screen, STREAK, (313,248), (333,267)) 

#a portal to hell
while True:
    x,y = random.randint(0,SIZE[0]), random.randint(0,SIZE[1])
    
    pygame.draw.circle(screen, ROOF, (70+x,350+y), 100) 
    pygame.draw.circle(screen, DARKRED, (70+x,350+y), 90) 
    pygame.draw.circle(screen, RED, (70+x,350+y), 80) 
    pygame.draw.circle(screen, YELLOW, (70+x,350+y), 70) 
    pygame.draw.circle(screen, BLOOD, (70+x,350+y), 60) 

    pygame.display.flip()
    pygame.time.wait(3000)

pygame.display.flip() 
pygame.time.wait(3000)  
pygame.quit() 
