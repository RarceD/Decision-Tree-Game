import pygame
import cv2

import threading
import time
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# To capture video from webcam. 
cap = cv2.VideoCapture(1)
   
pygame.init()
screen_x = 950
screen_y = 620
win = pygame.display.set_mode((screen_x, screen_y))  # dimensions of it
pygame.display.set_caption("Bea's Game")  # title of this shit of game
# bg = pygame.image.load('b_land.jpg')
font = pygame.font.SysFont('bitstreamverasans', 30, True, True)

down_space = 100
right_space = 300

gravity = 9

def render(win):
    # win.blit(bg, (0, 0))  # always print first the background
    text = font.render('Try to jump Bea', 2, (255, 182, 8))
    text2 = font.render('Counter: ' + str(34), 2, (255, 182, 8))
    text3 = font.render('Max Score: ' + str(5656), 2, (255, 0, 8))zº
    win.blit(text, (50, 30))
    win.blit(text2, (700, 30))
    win.blit(text3, (700, 80))
    pygame.display.update()  # update the screen frames

game_run = True

def facial_recognition():
    while(True):
        # Read the frame
        _, img = cap.read()
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            if (w>95):
                if (x<100):
                    print("RIGHT")
                    # cat.x -= cat.vel*2
                elif (x>300):
                    print("LEFT")
                    pass
                    # cat.x += cat.vel*2
        # Display
        cv2.imshow('img', img)
        # Stop if escape key is pressed
        k = cv2.waitKey(30) & 0xff
        if k==27:
            # Release the VideoCapture object
            cap.release()
            break
        

def run_game_thread():
    while(True):
        render(win)
        pygame.time.delay(10)  # 64x64 images
        for event in pygame.event.get():  # Check for events of close
            if event.type == pygame.QUIT:
                game_run = False
                pygame.quit()
    
# _thread.start_new_thread( facial_recognition(), ("Thread-1", 2 ) )
# _thread.start_new_thread( run_game_thread(), ("Thread-2", 4 ) )
threading.Thread(target=facial_recognition(), args=(0,)).start()
threading.Thread(target=run_game_thread(), args=(0,)).start()
