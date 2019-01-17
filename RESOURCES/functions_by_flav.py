import os, sys, time
from random import randint, choice
from pygame.display import flip
from pygame.locals import *
from string import *
import sys

import pygame, pygame.font, pygame.event, pygame.draw, string

def diplay_fixation_point(screen,GAME_AREA,ctr_x,ctr_y):
    pygame.draw.rect(screen, (0, 0, 0), GAME_AREA, 0) #(0=fill)
    pygame.draw.line(screen,(255,255,255),(ctr_x-50,ctr_y),(ctr_x+50,ctr_y), 4)
    pygame.draw.line(screen,(255,255,255),(ctr_x,ctr_y-50),(ctr_x,ctr_y+50), 4)

def read_next_word(end):
    idx=find(end, ' ')
    if idx > 0:
        leftmost_word = end[:idx]
        end = end[idx+1:].strip()
    else:
        leftmost_word = end.strip()
        end =''
    return leftmost_word,end

def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def get_user_input(screen,USER_INPUT_AREA,firstkey):
        text_input = firstkey
        while True: #while typing until enter key is pressed
            pygame.font.init()
         
            my_font2 = pygame.font.SysFont('arial', 14)
            message = my_font2.render(text_input, False, Color('black'))

            for sys_event in pygame.event.get():
                if sys_event.type == pygame.QUIT:
                    exit_game()
                    
                elif sys_event.type == pygame.KEYDOWN:
                    if sys_event.key == K_BACKSPACE:
                        text_input = text_input[0:-1]
                    elif sys_event.key == K_RETURN:
                        return text_input
                        break
                    
                    else: #COLLECT ENTERRED CHARACTERS
                        text_input += chr(sys_event.key)
                        message = my_font2.render(text_input, False, Color('black'))
            
            msgHt =message.get_height()
            #creen.blit(message, USER_INPUT_AREA.move(20,  msgHt/6))
            screen.blit(message, USER_INPUT_AREA.move(10,  0))
            pygame.display.flip()

class MyButton:
    """Button class based on the
    Command pattern."""
    
    def __init__(self, x, y, w, h, text):
        lw = 4 #line_width
        bw = 2
        self.text=text
        #self.rect = Rect(x-lw,y-lw,w+2*lw,h+2*lw)
        self.rect = Rect(x-bw+1,y-bw+1,w+2*bw,h+2*bw)
        self.face = Rect(x,y,w,h)
        self.pt1 = x,y
        self.pt2 = x+w,y
        self.pt3 = x+w,y+h
        self.pt4 = x,y+h
        self.button_pos = "UP"
        
    def draw(self,surface):
        if self.button_pos == "UP":
            self.draw_up(surface)
        else:
            self.draw_down(surface)
            
    def draw_up(self, surface):
        # You could of course use pictures here.
        # This method could also be implemented
        # by subclasses.
        face_color = (150,150,150)
        ln_color=Color('black')
        lw = 4 #Line width
        #pygame.draw.rect(surface,(100,100,100),self.rect)
        pygame.draw.rect(surface, ln_color, self.rect)
        pygame.draw.rect(surface, face_color, self.face)
        #Highlight
        pygame.draw.line(surface, (255, 255, 255), (self.pt1), (self.pt2))
        pygame.draw.line(surface, (255, 255, 255), (self.pt2), (self.pt3))
        pygame.draw.line(surface, (100, 100, 100), (self.pt1), (self.pt4))
        pygame.draw.line(surface, (100, 100, 100), (self.pt4), (self.pt3))
                # WRITE LABEL
        my_font = pygame.font.SysFont('arial', 20)
        message1_sf = my_font.render(self.text, True, Color('white'))
        msgHt =message1_sf.get_height()
        msgWd = message1_sf.get_width()
        msgX = (self.rect.width - msgWd)/2
        msgY = (self.rect.height - msgHt)/2
        surface.blit(message1_sf, self.rect.move(msgX,  msgY))
        
    def draw_down(self, surface):
        face_color = (150,150,150)
        ln_color=Color('black')
        lw = 4 #Line width
        #pygame.draw.rect(surface,(100,100,100),self.rect)
        pygame.draw.rect(surface, ln_color, self.rect)
        pygame.draw.rect(surface, face_color, self.face)
        #Highlight
        pygame.draw.line(surface, (255, 255, 255), (self.pt1), (self.pt4))
        pygame.draw.line(surface, (255, 255, 255), (self.pt4), (self.pt3))
        pygame.draw.line(surface, (100, 100, 100), (self.pt1), (self.pt2))
        pygame.draw.line(surface, (100, 100, 100), (self.pt2), (self.pt3))
        # WRITE LABEL
        my_font = pygame.font.SysFont('arial', 20)
        message1_sf = my_font.render(self.text, True, Color('white'))
        msgHt =message1_sf.get_height()
        msgWd = message1_sf.get_width()
        msgX = (self.rect.width - msgWd)/2
        msgY = (self.rect.height - msgHt)/2
        surface.blit(message1_sf, self.rect.move(msgX,  msgY+1))
        
def find_corr(x,y):
 # see: https://books.google.com/books?id=EvWbCgAAQBAJ&pg=PA75&lpg=PA75&dq=python+correlation+between+two+sets+of+data&source=bl&ots=NJXTskco9f&sig=z8zHHlM39snBlMS62bvbW8-2gWc&hl=en&sa=X&ved=0ahUKEwiGnd_lp4HSAhWJ54MKHV7KDaw4ChDoAQg6MAY#v=onepage&q=python%20correlation%20between%20two%20sets%20of%20data&f=false
 # Doing math with python by Amit Saha, 2015, pp75-78.
     n = len(x)
     #find sum of products
     prod=[]
     for xi,yi in zip(x,y):
         prod.append(xi*yi)

     sum_prod_x_y = sum(prod)
     sum_x = sum(x)
     sum_y = sum(y)
     squared_sum_x = sum_x**2
     squared_sum_y = sum_y**2

     x_square = []
     for xi in x:
         x_square.append(xi**2)
     #find the sum
     x_square_sum = sum(x_square)

     y_square = []
     for yi in y:
         y_square.append(yi**2)
     #find the sum
     y_square_sum = sum(y_square)
     #use formula to calculate correlation
     numerator = n*sum_prod_x_y - sum_x * sum_y
     denominator_term1 = n*x_square_sum - squared_sum_x
     denominator_term2 = n*y_square_sum - squared_sum_y
     denominator = (denominator_term1*denominator_term2)**0.5
     #print ("numerator: ", numerator,"   denominator: ", denominator)
     if denominator != 0.0: correlation = numerator/denominator
     else: correlation = -9999999.9 # error
     return correlation
