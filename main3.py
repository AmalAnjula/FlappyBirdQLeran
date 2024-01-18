from itertools import cycle
import random
import sys

import threading

import pygame
from pygame.locals import *
from contain import *
import tracemalloc
 
import argparse
import pickle
import time
import os
import cv2

import tkinter as tk
from tkinter import ttk

sys.path.append(os.getcwd())

start_time=time.time()

MaxScoreToTrain = 10


tracemalloc.start()
def your_function(arg):
    
    def nothing(x):
        pass
    # Your function logic goes here
    result = arg * 2
    print("Result:", result)
    cv2.namedWindow('result')
    cv2.createTrackbar('damp_Intvl', 'result',1,100,nothing)
    cv2.createTrackbar('dis_fact', 'result',1,100,nothing)
    cv2.createTrackbar('self_learn', 'result',1,100,nothing)

    cv2.setTrackbarPos( 'damp_Intvl','result', myBot.dumping_interval)
    cv2.setTrackbarPos( 'dis_fact','result',int( myBot.discount_factor*100))
    cv2.setTrackbarPos('self_learn','result',int( myBot.learning_rate*100 ))

 
    while True:
        myBot.dumping_interval = cv2.getTrackbarPos('damp_Intvl','result')
        myBot.discount_factor = cv2.getTrackbarPos('damp_Intvl','result')/100.00
        myBot.learning_rate = cv2.getTrackbarPos('self_learn','result')/100.00
        #print(myBot.discount_factor) 
        time.sleep(0.1)
         
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Break the loop if 'Esc' key is pressed
            break
        
    cv2.destroyAllWindows()

def main():
    global SCREEN, FPSCLOCK, FPS, myBot

    parser = argparse.ArgumentParser("flappy.py")
    parser.add_argument("--fps", type=int, default=60, help="number of frames per second")
    parser.add_argument(
        "--dump_hitmasks", action="store_true", help="dump hitmasks to file and exit"
    )
    args = parser.parse_args()

    FPS = args.fps

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Flappy Bird")

    # numbers sprites for score display
    IMAGES["numbers"] = (
        pygame.image.load("data/assets/sprites/0.png").convert_alpha(),
        pygame.image.load("data/assets/sprites/1.png").convert_alpha(),
        pygame.image.load("data/assets/sprites/2.png").convert_alpha(),
        pygame.image.load("data/assets/sprites/3.png").convert_alpha(),
        pygame.image.load("data/assets/sprites/4.png").convert_alpha(),
        pygame.image.load("data/assets/sprites/5.png").convert_alpha(),
        pygame.image.load("data/assets/sprites/6.png").convert_alpha(),
        pygame.image.load("data/assets/sprites/7.png").convert_alpha(),
        pygame.image.load("data/assets/sprites/8.png").convert_alpha(),
        pygame.image.load("data/assets/sprites/9.png").convert_alpha(),
    )

    # game over sprite
    IMAGES["gameover"] = pygame.image.load("data/assets/sprites/gameover.png").convert_alpha()
    # message sprite for welcome screen
    IMAGES["message"] = pygame.image.load("data/assets/sprites/message.png").convert_alpha()
    # base (ground) sprite
    IMAGES["base"] = pygame.image.load("data/assets/sprites/base.png").convert_alpha()

    # sounds
    if "win" in sys.platform:
        soundExt = ".wav"
    else:
        soundExt = ".ogg"

    SOUNDS["die"] = pygame.mixer.Sound("data/assets/audio/die" + soundExt)
    SOUNDS["hit"] = pygame.mixer.Sound("data/assets/audio/hit" + soundExt)
    SOUNDS["point"] = pygame.mixer.Sound("data/assets/audio/point" + soundExt)
    SOUNDS["swoosh"] = pygame.mixer.Sound("data/assets/audio/swoosh" + soundExt)
    SOUNDS["wing"] = pygame.mixer.Sound("data/assets/audio/wing" + soundExt)

    while True:
        # select random background sprites
        randBg = random.randint(0, len(backGroundList) - 1)
        IMAGES["background"] = pygame.image.load(backGroundList[randBg]).convert()

        # select random player sprites
        randPlayer = random.randint(0, len(birdModels) - 1)
        IMAGES["player"] = (
            pygame.image.load(birdModels[randPlayer][0]).convert_alpha(),
            pygame.image.load(birdModels[randPlayer][1]).convert_alpha(),
            pygame.image.load(birdModels[randPlayer][2]).convert_alpha(),
        )

        # select random pipe sprites
        pipeindex = random.randint(0, len(pipeList) - 1)
        IMAGES["pipe"] = (
            pygame.transform.rotate(pygame.image.load(pipeList[pipeindex]).convert_alpha(), 180),
            pygame.image.load(pipeList[pipeindex]).convert_alpha(),
        )

        # hismask for pipes
        HITMASKS["pipe"] = (getHitmask(IMAGES["pipe"][0]), getHitmask(IMAGES["pipe"][1]))

        # hitmask for player
        HITMASKS["player"] = (
            getHitmask(IMAGES["player"][0]),
            getHitmask(IMAGES["player"][1]),
            getHitmask(IMAGES["player"][2]),
        )

        if args.dump_hitmasks:
            with open("data/hitmasks_data.pkl", "wb") as output:
                pickle.dump(HITMASKS, output, pickle.HIGHEST_PROTOCOL)
            sys.exit()

        movementInfo = showWelcomeAnimation()
        crashInfo = mainGame(movementInfo)
        showGameOverScreen(crashInfo)


def showWelcomeAnimation():
    """Shows welcome screen animation of flappy bird"""
    # index of player to blit on screen
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0

    playerx = int(screenWidth * 0.2)
    playery = int((screenHeight - IMAGES["player"][0].get_height()) / 2)

    messagex = int((screenWidth - IMAGES["message"].get_width()) / 2)
    messagey = int(screenHeight * 0.12)

    basex = 0
    # amount by which base can maximum shift to left
    baseShift = IMAGES["base"].get_width() - IMAGES["background"].get_width()

    # player shm for up-down motion on welcome screen
    playerShmVals = {"val": 0, "dir": 1}

    while True:
        
        SOUNDS["wing"].play()
        return {
            "playery": playery + playerShmVals["val"],
            "basex": basex,
            "playerIndexGen": playerIndexGen,
        }

        # adjust playery, playerIndex, basex
        if (loopIter + 1) % 5 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 4) % baseShift)
        playerShm(playerShmVals)

        # draw sprites
        SCREEN.blit(IMAGES["background"], (0, 0))
        SCREEN.blit(IMAGES["player"][playerIndex], (playerx, playery + playerShmVals["val"]))
        SCREEN.blit(IMAGES["message"], (messagex, messagey))
        SCREEN.blit(IMAGES["base"], (basex, baseY))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def mainGame(movementInfo):

    global start_time

    score = playerIndex = loopIter = 0
    playerIndexGen = movementInfo["playerIndexGen"]

    playerx, playery = int(screenWidth * 0.2), movementInfo["playery"]

    basex = movementInfo["basex"]
    baseShift = IMAGES["base"].get_width() - IMAGES["background"].get_width()

    # get 2 new pipes to add to upperPipes lowerPipes list
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {"x": screenWidth + 200, "y": newPipe1[0]["y"]},
        {"x": screenWidth + 200 + (screenWidth / 2), "y": newPipe2[0]["y"]},
    ]

    # list of lowerpipe
    lowerPipes = [
        {"x": screenWidth + 200, "y": newPipe1[1]["y"]},
        {"x": screenWidth + 200 + (screenWidth / 2), "y": newPipe2[1]["y"]},
    ]

    pipeVelX = -4

    # player velocity, max velocity, downward accleration, accleration on flap
    playerVelY = -9  # player's velocity along Y, default same as playerFlapped
    playerMaxVelY = 10  # max vel along Y, max descend speed
    playerMinVelY = -8  # min vel along Y, max ascend speed
    playerAccY = 1  # players downward accleration
    playerFlapAcc = -9  # players speed on flapping
    playerFlapped = False  # True when player flaps

    while True:
        #playerx=140
        #playery=180
        if -playerx + lowerPipes[0]["x"] > -30:
            myPipe = lowerPipes[0]
        else:
            myPipe = lowerPipes[1]

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > -2 * IMAGES["player"][0].get_height():
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    SOUNDS["wing"].play()
        #print(-playerx , myPipe["x"],-playerx+myPipe["x"], -playery , myPipe["y"], -playery + myPipe["y"])
        if myBot.actions(-playerx + myPipe["x"], -playery + myPipe["y"], playerVelY):
            if playery > -2 * IMAGES["player"][0].get_height():
                playerVelY = playerFlapAcc
                playerFlapped = True
                SOUNDS["wing"].play()

        # check for crash here
        crashTest = checkCrash(
            {"x": playerx, "y": playery, "index": playerIndex}, upperPipes, lowerPipes
        )
        if crashTest[0]:
            # Update the q scores
            myBot.writeQval()

            #print(myBot.game_count ,myBot.q_values[myBot.state][act],)

            #time.sleep(2)
            print("crashed")
            start_time = time.time()  # Record the start time


            f = open("data/plotData.csv", "a")
            
            f.write(str( myBot.game_count)+","+ str(score) +","+str(round(myBot.singleQVal,4))+","+str(round(tracemalloc.get_traced_memory()[0]/1000,2))+","+str(round(tracemalloc.get_traced_memory()[1]/1000,2))+"\n")
            f.close()



            return {
                "y": playery,
                "groundCrash": crashTest[1],
                "basex": basex,
                "upperPipes": upperPipes,
                "lowerPipes": lowerPipes,
                "score": score,
                "playerVelY": playerVelY,
            }

        # check for score
        playerMidPos = playerx + IMAGES["player"][0].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe["x"] + IMAGES["pipe"][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                SOUNDS["point"].play()

        # playerIndex basex change
        if (loopIter + 1) % 3 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift)

        # player's movement
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False
        playerHeight = IMAGES["player"][playerIndex].get_height()
        playery += min(playerVelY, baseY - playery - playerHeight)

        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe["x"] += pipeVelX
            lPipe["x"] += pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 0 < upperPipes[0]["x"] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if upperPipes[0]["x"] < -IMAGES["pipe"][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # draw sprites
        SCREEN.blit(IMAGES["background"], (0, 0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES["pipe"][0], (uPipe["x"], uPipe["y"]))
            SCREEN.blit(IMAGES["pipe"][1], (lPipe["x"], lPipe["y"]))

        SCREEN.blit(IMAGES["base"], (basex, baseY))
        # print score so player overlaps the score
        showScore(score)
        SCREEN.blit(IMAGES["player"][playerIndex], (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def showGameOverScreen(crashInfo):
    """crashes the player down and shows gameover image"""
    score = crashInfo["score"]
    playerx = screenWidth * 0.2
    playery = crashInfo["y"]
    playerHeight = IMAGES["player"][0].get_height()
    playerVelY = crashInfo["playerVelY"]
    playerAccY = 2

    basex = crashInfo["basex"]

    upperPipes, lowerPipes = crashInfo["upperPipes"], crashInfo["lowerPipes"]

    # play hit and die sounds
    SOUNDS["hit"].play()
    if not crashInfo["groundCrash"]:
        SOUNDS["die"].play()

    while True:
        
        return  ### Must remove to activate press-key functionality

        # player y shift
        if playery + playerHeight < baseY - 1:
            playery += min(playerVelY, baseY - playery - playerHeight)

        # player velocity change
        if playerVelY < 15:
            playerVelY += playerAccY

        # draw sprites
        SCREEN.blit(IMAGES["background"], (0, 0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES["pipe"][0], (uPipe["x"], uPipe["y"]))
            SCREEN.blit(IMAGES["pipe"][1], (lPipe["x"], lPipe["y"]))

        SCREEN.blit(IMAGES["base"], (basex, baseY))
        showScore(score)
        SCREEN.blit(IMAGES["player"][1], (playerx, playery))

        FPSCLOCK.tick(FPS)
        pygame.display.update()


def playerShm(playerShm):
    """oscillates the value of playerShm['val'] between 8 and -8"""
    if abs(playerShm["val"]) == 8:
        playerShm["dir"] *= -1

    if playerShm["dir"] == 1:
        playerShm["val"] += 1
    else:
        playerShm["val"] -= 1


def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(baseY * 0.6 - pipGapz))
    gapY += int(baseY * 0.2)
    pipeHeight = IMAGES["pipe"][0].get_height()
    pipeX = screenWidth + 10

    return [
        {"x": pipeX, "y": gapY - pipeHeight},  # upper pipe
        {"x": pipeX, "y": gapY + pipGapz},  # lower pipe
    ]


def showScore(score):
    global start_time,newTime,MaxScoreToTrain
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0  # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES["numbers"][digit].get_width()

    Xoffset = (screenWidth - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES["numbers"][digit], (Xoffset, screenHeight * 0.1))
        Xoffset += IMAGES["numbers"][digit].get_width()


    font = pygame.font.Font(None, 25)  # You can adjust the font size as needed
     #
    
    game_count = font.render("Game try: {}".format(myBot.game_count)+"", True, (0, 0, 0))
    #tracemalloc.get_traced_memory()


    if score < MaxScoreToTrain:
        newTime=time.time()
    
    time_text = font.render("Time: {}s ".format(round((newTime - start_time),2)), True, (0, 0, 0))

    text_rect = time_text.get_rect(center=(screenWidth // 2, screenHeight * 0.85))
    game_count_text_rect = game_count.get_rect(center=(screenWidth // 2, screenHeight * 0.9))
    
    memNow,MemPeak=tracemalloc.get_traced_memory()
    memNow=round(memNow/1000,2)
    MemPeak=round(MemPeak/1000,2)

    #memInfo=str(memNow)+str(MemPeak)

    memInfo=font.render("Now: {}Kb".format(memNow)+" Peak {}Kb".format(MemPeak), True, (0, 0, 0))
    #memUseRect=memInfo.get_rect(center=(screenWidth // 2, screenHeight * 0.95))
    memUseRect=memInfo.get_rect(center=(screenWidth // 2, screenHeight * 0.95))

    SCREEN.blit(time_text, text_rect)
    SCREEN.blit(game_count, game_count_text_rect)
    SCREEN.blit(memInfo, memUseRect)




def checkCrash(player, upperPipes, lowerPipes):
    """returns True if player collders with base or pipes."""
    pi = player["index"]
    player["w"] = IMAGES["player"][0].get_width()
    player["h"] = IMAGES["player"][0].get_height()

    # if player crashes into ground
    if (player["y"] + player["h"] >= baseY - 1) or (player["y"] + player["h"] <= 0):
        return [True, True]
    else:

        playerRect = pygame.Rect(player["x"], player["y"], player["w"], player["h"])
        pipeW = IMAGES["pipe"][0].get_width()
        pipeH = IMAGES["pipe"][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe["x"], uPipe["y"], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe["x"], lPipe["y"], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS["player"][pi]
            uHitmask = HITMASKS["pipe"][0]
            lHitmask = HITMASKS["pipe"][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]


def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                return True
    return False


def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask


if __name__ == "__main__":
    #thread1 = threading.Thread(target=your_function, args=(10,))
    # Start threads
    #thread1.start()
    main()
