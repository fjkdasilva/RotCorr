import tkinter as Tk
from tkinter.filedialog import askopenfilename,asksaveasfile

import math
import time
import os, sys, time,copy, string
import pygame
from pygame.display import flip
from pygame.locals import *
from RESOURCES.functions_by_flav import *

#################################################################
#   GLOBALS
#################################################################
SCREEN_WIDTH = 840
SCREEN_HEIGHT= 600
zeroX = int(SCREEN_WIDTH/2)
zeroY = int(SCREEN_HEIGHT/2)
# SCREEN SETUP
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCREEN_WIDTH,30)
GAME_AREA = Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode((SCREEN_WIDTH-10,SCREEN_HEIGHT-30),pygame.RESIZABLE,32)

########################################
# SCREEN
#######################################
pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (755,30) #Position on the screen
pygame.display.set_caption("Jake's MDS: by DaSilvaAutomation.com")
pygame.draw.rect(screen, (255, 255, 255), GAME_AREA, 0) #(0=fill)
start_time = time.clock()


#################################################################
#   FILE STUFF
#################################################################
def choose_file():
    root = Tk.Tk()
    root.withdraw() # we don't want a full GUI, so keep the root window from appearing
    chosenFileName = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    root.destroy()
    return chosenFileName

#################################################################
#   LABEL STUFF
#################################################################
def display_lbl(screen,text,loc_rect):
    pygame.font.init()
    my_font1 = pygame.font.SysFont('arial', 12)
    lbl2 = my_font1.render(text, False, Color('black'))#render(text, antialias, color, background=None)
    screen.blit(lbl2, loc_rect) #(x,y,w,h)
    #screen.blit(message, file2dRect.move(10,  0))

def draw_button(surface,rect,lbl,state):

    face_color = (200,200,200)
    x1 = rect[0]+1
    y1 = rect[1]+1
    x2 = rect[2] + x1 - 3
    y2 = rect[3] + y1 - 3
    Rec = Rect(rect)

    def draw_up():
        pygame.draw.rect(surface, (0,0,0), rect)
        pygame.draw.rect(surface, face_color, (x1,y1, rect[2] - 2, rect[3] - 2))
        #Highlight
        pygame.draw.line(surface, (255, 255, 255), (x1,y1), (x2,y1),2) # light
        pygame.draw.line(surface, (255, 255, 255), (x1,y1), (x1,y2),2) # light
        pygame.draw.line(surface, (100, 100, 100), (x1,y2), (x2,y2),2) # shadow
        pygame.draw.line(surface, (100, 100, 100), (x2,y1), (x2,y2),2) #shadow

    def draw_down():
        pygame.draw.rect(surface, (0,0,0), rect)
        pygame.draw.rect(surface, face_color, (x1,y1, rect[2] - 2, rect[3] - 2))
        #Highlight
        pygame.draw.line(surface, (100, 100, 100), (x1,y1), (x2,y1),2) # shadow
        pygame.draw.line(surface, (100, 100, 100), (x1,y1), (x1,y2),2) # shadow
        pygame.draw.line(surface, (255, 255, 255), (x1,y2), (x2,y2),2) # light
        pygame.draw.line(surface, (255, 255, 255), (x2,y1), (x2,y2),2) # light

    if state == "UP":
        draw_up()
    else:
        draw_down()
        print("draw DN")
    # WRITE LABEL
    my_font = pygame.font.SysFont('arial', 16)
    label = my_font.render(lbl, True, Color('white'))
    msgHt =label.get_height()
    msgWd = label.get_width()
    msgX = (Rec.width - msgWd)/2
    msgY = (Rec.height - msgHt)/2
    surface.blit(label, Rec.move(msgX,  msgY))
    

########################################################
#        MAIN PROG
########################################################
def Jakes_Program():  
    GETTINGFILE2DNAME = False
    GETTINGFILE1DNAME = False
    data1D = []
    data2D = []
    data2Dy = []
    minD = 1000000.0
    min1D = 1000000.0
    maxD = -1000000.0
    max1D = -1000000.0
    rotangR = 0.0
    rotangD = 0.0
    maxcorr = 0.0
    maxnegcorr = 0.0
    correlation = 0.0
    correlations =[]
    file2dRect = Rect(20,10,100,20)
    file1dRect = Rect(20,60,100,20)
    bestCorrRect=Rect(20,110,120,20)
    bestAngRect=Rect(20,160,120,20)
    buttonRect = Rect(20,210,100,20)
    BEST_FOUND = False
    BUTTON_PRESSED = False
    while True:
        if rotangD >= 360.0: BEST_FOUND = True
        #GAME_AREA = Rect(0, 0, SCREEN_WIDHH, SCREEN_HEIGHT)
        #pygame.draw.rect(screen, (255, 255, 255), GAME_AREA, 0)

        pygame.draw.rect(screen, (0,0,0), file2dRect, 1)
        pygame.draw.rect(screen, (0,0,0), file1dRect, 1)
        pygame.draw.rect(screen, (20,20,20), buttonRect, 1)
        
        display_lbl(screen,'2D filename',(20,35,200,20))
        display_lbl(screen,'1D filename',(20,85,200,20))
        if not BUTTON_PRESSED:
            draw_button(screen,buttonRect,"Save","UP")

        #############################################
        # GET EVENTS.  KEYBOARD, MOUSE, or EEG
        ##############################################
        for sys_event in pygame.event.get():
            if sys_event.type == pygame.QUIT:
               sys.exit()

            ########################################
            #  Keyboard Events
            ########################################
            
            #########################################################
            #  MOUSE EVENTS (always active independent of game mode)
            #########################################################

            elif (sys_event.type == pygame.MOUSEMOTION ):#
                cur_x,cur_y = pygame.mouse.get_pos() #Move Mouse


            elif (sys_event.type == pygame.MOUSEBUTTONDOWN ):#Mouse Clicked
                 # get current mouse position of Click event
                cur_x,cur_y = pygame.mouse.get_pos()
                if file2dRect.collidepoint(cur_x,cur_y):
                    GETTINGFILE2DNAME = True
                    pygame.draw.rect(screen, (255,0,0), file2dRect, 2)
                    file2dName = choose_file()
                    cur_dir, datafile = os.path.split(file2dName)
                    display_lbl(screen,datafile,(30,12,200,20))
                    try:
                         file2D = open(file2dName,'r')
                         print(file2D)
                         linenum = 0
                         for line in file2D:
                             #print(line)
                             linenum+=1
                             if linenum>2:
                                 x,y = line.split()
                                 #print("x: ",x,"  y: ",y)
                                 xydata = (float(x),float(y))
                                 #cur_dir, prognamfile = os.path.split(full_path)
                                 data2D.append(xydata)
                                 data2Dy.append(float(y))

                         file2D.close()
                    except:
                         print("problem parsing file or file name does not exist")

                elif file1dRect.collidepoint(cur_x,cur_y):
                    GETTINGFILE1DNAME = True
                    pygame.draw.rect(screen, (255,0,0), file1dRect, 2)
                    file1dName = choose_file()
                    cur_dir, datafile = os.path.split(file1dName)
                    display_lbl(screen,datafile,(30,62,200,20))
                    try:
                         file1D = open(file1dName,'r')
                         linenum = 0
                         for line in file1D: #Note stuff read from files are strings, not numbers
                             
                             linenum+=1
                             if linenum>2:
                                 data1D.append(float(line))#XXXXXXXXXXXXXXXXXXXXXXXX

                         file1D.close()
                    except:
                         print("problem parsing file or file name does not exist")

                elif buttonRect.collidepoint(cur_x,cur_y):
                     BUTTON_PRESSED = True
                     draw_button(screen,buttonRect,"Save","DN")
                     pygame.display.flip()
                     Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
                     chosenFileName = asksaveasfile(filetypes = (("text files","*.txt"),("all files","*.*"))) # show an "Open" dialog box and return the path to the selected file
                     print("BEST CORR WILL BE PRINTED INTO: ", chosenFileName)
                     try:
                         chosenFileName.write("Best Correlation angle: %3.7f (deg)\n" % (bestangD))
                         chosenFileName.write("Rotated (X,Y)\n")
                         chosenFileName.write("-----------------\n")                     
                         for x,y in bestCorrData2D:
                            chosenFileName.write("%5.5f, \t%5.5f\n" % (x,y))
                     except :
                         print("unable to write")

                     chosenFileName.close()
                     BUTTON_PRESSED = False
                elif (sys_event.type == pygame.MOUSEBUTTONUP ):
                    BUTTON_PRESSED = False
                    

        #############################################
        #  Draw Axes
        #############################################
        pygame.draw.rect(screen, (255,255,255), (zeroX - 290, zeroY -290, 570,570), 0)# clear points
        pygame.draw.line(screen, (255,0,0),(zeroX,zeroY+280),(zeroX,zeroY-280),1) #Y-axis, lines(Surface, color, closed, pointlist, width=1) -> Rect
        pygame.draw.line(screen, (255,0,0),(zeroX-280,zeroY),(zeroX+280,zeroY),1) #X-axis, lines(Surface, color, closed, pointlist, width=1) -> Rect

        if not BEST_FOUND:
            # Get min, max
            if len(data1D) > 0:
                for y in data1D:
                   if y > max1D: max1D = y
                   if y < min1D: min1D = y
            if len(data2D) > 0:
                for x,y in data2D:
                   if y > maxD: maxD = y
                   if y < minD: minD = y
                   if x > maxD: maxD = x
                   if x < minD: minD = x

            #print("len: ",len(data1D), len(data2D))
            if len(data1D) > 0:
               for y in data1D:
                   pygame.draw.circle(screen, (255,0,0), (int(zeroX),int(zeroY)-int(280.0*y/max1D)),3,0)#circle(Surface, color, pos, radius, width=0) -> Rect

            if len(data2D) > 0:
               for x,y in data2D:
                    pygame.draw.circle(screen, (0,0,255), (int(zeroX)+int(280.0*x/maxD),int(zeroY)-int(280.0*y/maxD)),4,0)#circle(Surface, color, pos, radius, width=0) -> Rect

            #################
            #  ROTATIONS
            #################
            data2Dy = []
            if len(data2D) > 0 and len(data1D) > 0: 
                for x,y in data2D:
                    xr = x*math.cos(rotangR) - y*math.sin(rotangR)
                    yr = x*math.sin(rotangR) + y*math.cos(rotangR)
                    data2Dy.append(yr)
                    #print(x,y, "maxD> ",maxD, int(280.0*xr/maxD), int(280.0*yr/maxD))
                    pygame.draw.circle(screen, (0,255,0), (zeroX+int(280.0*xr/maxD),zeroY-int(280.0*yr/maxD)),4,1)#circle(Surface, color, pos, radius, width=0) -> Rect
                    pygame.draw.line(screen, (0,0,255),(zeroX+int(280.0*xr/maxD),zeroY-int(280.0*yr/maxD)),(zeroX,zeroY-int(280.0*yr/maxD)),1) #X-axis, lines(Surface, color, closed, pointlist, width=1) -> Rect
                    rotx = int(280 * math.cos(rotangR))
                    roty = int(280 * math.sin(rotangR))
                    pygame.draw.line(screen, (0,0,255),(zeroX,zeroY),(zeroX+rotx,zeroY-roty),1)
                ######################
                # Get correlations
                ######################
                correlation = find_corr(data1D,data2Dy)
                #print ("angD: ",rotangD, "corr: ",correlation)
                correlations.append((rotangD,correlation))
                if correlation > maxcorr:
                    maxcorr = correlation
                    bestangD = rotangD
                if correlation < maxnegcorr:
                    maxnegcorr = correlation
                    bestnegangD = rotangD
                #print ("max neg corr: ",maxnegcorr, "max_corr: ",maxcorr)
                
                rotangD += 1.0
                rotangR = rotangD * math.pi/180.0
                
                #print (rotangD, rotangR)

            ########################
            # UPDATE SCREEN
            ########################
            pygame.draw.rect(screen, (255,255,255), bestCorrRect, 0)
            pygame.draw.rect(screen, (255,255,255), bestAngRect, 0)
            pygame.draw.rect(screen, (0,0,0), bestCorrRect, 1)
            pygame.draw.rect(screen, (0,0,0), bestAngRect, 1)
            
            ##    bestAngRect=Rect(20,160,120,20)
            display_lbl(screen,'Angle (deg)',(20,130,200,20))
            display_lbl(screen,str(rotangD),(30,112,200,20))
            ##    bestCorrRect=Rect(20,110,120,20)
            display_lbl(screen,'Correlation',(20,180,200,20))
            display_lbl(screen,str(correlation),(30,162,200,20))

        else: #  THE BEST CORRELATION HAS BEEN FOUND
            rotangD = bestangD
            pygame.draw.rect(screen, (255,255,255), (zeroX - 280, zeroY -280, 560,560), 0)# clear points
            pygame.draw.line(screen, (255,0,0),(zeroX,zeroY+280),(zeroX,zeroY-280),1) #Y-axis, lines(Surface, color, closed, pointlist, width=1) -> Rect
            pygame.draw.line(screen, (255,0,0),(zeroX-280,zeroY),(zeroX+280,zeroY),1) #X-axis, lines(Surface, color, closed, pointlist, width=1) -> Rect

            rotangR = rotangD * math.pi/180.0
            data2Dy = []
            bestCorrData2D = []
            if len(data2D) > 0 and len(data1D) > 0:
                for x,y in data2D:
                    xr = x*math.cos(rotangR) - y*math.sin(rotangR)
                    yr = x*math.sin(rotangR) + y*math.cos(rotangR)
                    bestCorrData2D.append((xr,yr))
                    pygame.draw.circle(screen, (0,255,0), (zeroX+int(280.0*xr/maxD),zeroY-int(280.0*yr/maxD)),4,0)#circle(Surface, color, pos, radius, width=0) -> Rect
                    pygame.draw.line(screen, (0,0,255),(zeroX+int(280.0*xr/maxD),zeroY-int(280.0*yr/maxD)),(zeroX,zeroY-int(280.0*yr/maxD)),1) #X-axis, lines(Surface, color, closed, pointlist, width=1) -> Rect
                    rotx = int(280 * math.cos(rotangR))
                    roty = int(280 * math.sin(rotangR))
                    pygame.draw.line(screen, (0,0,255),(zeroX,zeroY),(zeroX+rotx,zeroY-roty),1)
                ######################
                # Get correlations
                ######################
                correlation = find_corr(data1D,data2Dy)
                #print ("angD: ",rotangD, "corr: ",correlation)
                correlations.append((rotangD,correlation))
                if correlation > maxcorr:
                    maxcorr = correlation
                    bestangD = rotangD
                if correlation < maxnegcorr:
                    maxnegcorr = correlation
                    bestnegangD = rotangD
                #print ("max neg corr: ",maxnegcorr, "max_corr: ",maxcorr)
            if len(data1D) > 0:
               for y in data1D:
                   pygame.draw.circle(screen, (255,0,0), (zeroX,zeroY-int(280.0*y/max1D)),3,0)#circle(Surface, color, pos, radius, width=0) -> Rect

            if len(data2D) > 0:
               for x,y in data2D:
                    pygame.draw.circle(screen, (0,0,255), (zeroX+int(280.0*x/maxD),zeroY-int(280.0*y/maxD)),4,0)#circle(Surface, color, pos, radius, width=0) -> Rect

            pygame.draw.rect(screen, (255,255,255), bestCorrRect, 0)#Clear msg box
            pygame.draw.rect(screen, (255,255,255), bestAngRect, 0)#Clear msg box
            pygame.draw.rect(screen, (0,0,0), bestCorrRect, 1)#draw box
            pygame.draw.rect(screen, (0,0,0), bestAngRect, 1) #draw box
            pygame.draw.rect(screen, (255,255,255), (20,130,200,20), 0)#Clear lbl
            pygame.draw.rect(screen, (255,255,255), (20,180,200,20), 0)#Clear lbl

            ##    bestAngRect=Rect(20,160,120,20)
            display_lbl(screen,'Best Rotation (deg)',(20,130,200,20))
            display_lbl(screen,str(rotangD),(30,112,200,20))
            ##    bestCorrRect=Rect(20,110,120,20)
            display_lbl(screen,'Max Correlation',(20,180,200,20))
            display_lbl(screen,str(maxcorr),(30,162,200,20))

            
        pygame.display.flip()
        time.sleep(0.10)

#########################################################################################
def main():  # This is so you can call this program from another programs, as long as you
                 # pass it the necessary arguments. In this case there are none because the
                 # user will be asked for the needed file names.

    Jakes_Program()

if __name__ == "__main__":
    main()
##    if sys.argv[1:] == []:
##        main(['none'])
##    else:
##        main(sys.argv[1:]) #file names
##                           #the run command, as in: >> python Exp1.1.py filename1d filename2d
##                           # COMMAND LINE RUNNING WITH FILENAME ARGUMENTS NOT IMPLEMENTED YET.

