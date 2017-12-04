import random, pygame, sys, tkinter, pickle
import dumbmenu as dm
import pygame_textinput
from pygame.locals import *


class Path(object): #Holds level objects
    def __init__(self, name, levelList):
        self.name = name
        self.levelList = levelList
        
    def getName(self):
        return self.name
    
    def getLevelList(self):
        return self.levelList

class Level(object): #Holds Level, including name, background image, 
    def __init__(self, name, background, spriteList, nodesToWin, levelId):
        self.name = name
        self.background = background
        self.spriteList = spriteList
        self.nodesToWin = nodesToWin
        self.levelId = levelId
        
    def getName(self):
        return self.name
    
    def getLevelId(self):
        return self.levelId    
    
    def getBackground(self):
        return self.background
    
    def getSpriteList(self):
        return self.spriteList
    
    def getNodesToWin(self):
        return self.nodesToWin
    
class Player(object):
    def __init__(self, name, score, currentLevel, currentPath):
        self.name = name
        self.score = score
        self.currentLevel = currentLevel  
        self.currentPath = currentPath
        
    def setScore(self, score):
        self.score = score
    
    def getScore(self):
        return self.score 
    
    def setName(self, name):
        self.name = name
    
    def setCurrentLevel(self, currentLevel):
        self.currentLevel = currentLevel

    def setCurrentPath(self, currentPath):
        self.currentPath = currentPath

FPS = 10 #Number of frames per second the game plays at; This could be changed to accommodate difficulty levels within the game
WINDOWWIDTH = 1000
WINDOWHEIGHT = 680
CELLSIZE = 40 #Size of cell 
assert WINDOWWIDTH % CELLSIZE == 0, "Window width needs to be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height needs to be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#RGB colors
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
PURPLE    = ( 139,  0, 139)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # Head of player

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, SURFACE
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))    
    mudBG = pygame.image.load("mud.jpg")
    background = mudBG
    DISPLAYSURF.blit(background, [0,0])          
    SURFACE = pygame.image.load("favicon.ico")
    pygame.display.set_icon(SURFACE)
    FPSCLOCK = pygame.time.Clock()
    pygame.init()
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)        
    pygame.display.update()
    pygame.display.set_caption('Snake Evolutions')
    
    counter = 0
    
    while True:
        showStartScreen()
        counter += 1
        if counter > 0:
            mainMenu()        
        
def drawpoison(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    poison = pygame.image.load('poison.png')
    DISPLAYSURF.blit(poison, (x,y))
    
def drawfood(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    food = pygame.image.load('food.png')
    DISPLAYSURF.blit(food, (x,y))

def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def drawScore(score, Player):
    time = pygame.time.get_ticks()
    totalScore = Player.getScore()
    timeSurf = BASICFONT.render('Time: %s'% (time), True, WHITE)
    scoreSurf = BASICFONT.render('Score: %s'% (score), True, WHITE)
    totalScoreSurf = BASICFONT.render('Total Score: %s' % (totalScore), True, WHITE)
    
    timeRect = timeSurf.get_rect()
    timeRect.topleft = (WINDOWWIDTH -350, 10)
    DISPLAYSURF.blit(timeSurf, timeRect)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH-350, 40)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    totalScoreRect = totalScoreSurf.get_rect()
    totalScoreRect.topleft = (WINDOWWIDTH -350, 70)
    DISPLAYSURF.blit(totalScoreSurf, totalScoreRect)
    return (score)

def winGame(Player):
    Font = pygame.font.Font('freesansbold.ttf', 70)
    gameSurf = Font.render('You won the game!', True, WHITE)
    gameRect = gameSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 100)
    
    game1surf = Font.render('More TBA!', True, WHITE)
    game1rect = gameSurf.get_rect()
    game1rect.midtop = (WINDOWWIDTH / 3, 300)    

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(game1surf, game1rect)    
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue    

def drawplayer(playerCoords, Level):

    spriteList = Level.spriteList
    
    for coord in playerCoords:
        randomSprite = random.choice(spriteList)
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        DISPLAYSURF.blit(randomSprite, (x, y))   

def checkWinPath(Level, Player, currentPath): #Jesus is the code level for the end of a path, and different paths have different jesuses
    if Player.currentLevel == "jesus" and currentPath == "squid":
        winPathway(Level, Player, Path)
    
    if Player.currentLevel == "jesus2" and currentPath == "fish":
        winPathway(Level, Player, Path)
        
    if Player.currentLevel == "jesus3" and currentPath == "reptile":
        winGame(Player)
        
def checkWinLevel(score, Level, Player): #Checks during runGame() to see if player won level
    nodesToWin = Level.nodesToWin
    
    if(score >= nodesToWin):
        paused(Level, Player) #To pause menu
        checkForKeyPress() # clear out any key presses in the event queue

def winPathway(Player, Level, Path): #Checks to see if whole path is won and prompts user action
    
    Font = pygame.font.Font('freesansbold.ttf', 70)
    gameSurf = Font.render('You Won this path!', True, WHITE)
    gameRect = gameSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 100)
    
    game1surf = Font.render('Continue to next path?', True, WHITE)
    game1rect = gameSurf.get_rect()
    game1rect.midtop = (WINDOWWIDTH / 3, 300)    

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(game1surf, game1rect)    
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue
    levelName = Level.name
    levelList = generateFishList()
    
    for level in levelList: #testing purposes
        print(level.name)
    
    choose = dm.dumbmenu(DISPLAYSURF, [
        'Next Path',
        'Save Game',
        'Main Menu',
        'Submit to Leaderboard',
        'Quit Game'], 64,64,None,32,1.4,PURPLE,RED)
            
    if choose == 0:
        if levelName == ("jesus"):    
            Player.setCurrentPath("fish")            
            newLevel = loadStarfish()
            Player.setCurrentLevel(newLevel.name)
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
        
        if levelName == ("jesus2"):
            Player.setCurrentPath("reptile")
            newLevel = loadTadpole()
            Player.setCurrentLevel(newLevel.name)
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
        
        elif levelName == ("starfish"):     
            newLevel = loadGuppy()
            Player.setCurrentLevel(newLevel.name)
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
        
        elif levelName == ("guppy"):     
            newLevel = loadGoldfish()
            Player.setCurrentLevel(newLevel.name)
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return        
        
        elif levelName == ("goldfish"):          
            newLevel = loadCatfish()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return       
        
        elif levelName == ("catfish"):          
            newLevel = loadPiranha()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return              
        
        elif levelName == ("piranha"):          
            newLevel = loadShark()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return             
        
        elif levelName == ("shark"):          
            newLevel = loadDolphin()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return      
        
        elif levelName == ("dolphin"):          
            newLevel = loadWhale()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return          
        
        elif levelName == ("whale"):          
            newLevel = loadLochNess()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return   
        
        elif levelName == ("lochness"):          
            newLevel = loadJesus2()
            Player.setCurrentLevel(newLevel.name)    
            return            
        
        elif levelName == ("jesus2"):          
            newLevel = loadTadpole()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return
        
        elif levelName == ("tadpole"):          
            newLevel = loadFrog()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return       
        
        elif levelName == ("frog"):          
            newLevel = loadNewt()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return
        
        elif levelName == ("newt"):          
            newLevel = loadSnake()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return      
        
        elif levelName == ("snake"):          
            newLevel = loadTurtle()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return        
        
        elif levelName == ("turtle"):          
            newLevel = loadIguana()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return        
           
        elif levelName == ("iguana"):          
            newLevel = loadCrocodile()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return     
        
        elif levelName == ("crocodile"):          
            newLevel = loadDragon()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return        
           
        elif levelName == ("dragon"):          
            newLevel = loadJesus3()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return
        
        elif levelName == ("jesus3"):          
            
            winGame(Player)
            
            return              
           
           
        
        else: 
            newLevel = loadGuppy()
            Player.setCurrentLevel(newLevel.name)
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return            
            
    
    elif choose == 1: #Save game
        saveGame(Player)
        mainMenu()
        return
    
    elif choose == 2:
        submitToLeaderboard(Player)
    
    elif choose == 3:
        terminate()
        
    else:
        mainMenu()
        return    
        
    pygame.display.update()        

def paused(Level, Player):
    
    nodesToWin = Level.nodesToWin
    pause = True
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        
    name = Level.name
    currentPath = Player.currentPath
    
    if Player.currentLevel == "jesus":
        winPathway(Player, Level, currentPath)
    
    if Player.currentLevel == "jesus2":
        winPathway(Player, Level, currentPath)

    if Player.currentLevel == "jesus3":
        winPathway(Player, Level, currentPath)

    Font = pygame.font.Font('freesansbold.ttf', 100)
    gameSurf = Font.render('You Evolved!', True, WHITE)
    gameRect = gameSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 100)
    
    game1surf = Font.render(name + ' no longer!', True, WHITE)
    game1rect = gameSurf.get_rect()
    game1rect.midtop = (WINDOWWIDTH / 3, 300)    

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(game1surf, game1rect)    
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue
    levelName = Level.name
    
    choose = dm.dumbmenu(DISPLAYSURF, [
        'Next Level',
        'Save Game',
        'Submit to Leaderboard',
        'Quit Game'], 64,64,None,32,1.4,PURPLE,RED)
        
    
    if choose == 0: #Next Level         
        if levelName == ("amoeba"):          
            newLevel = loadWorm()
            print(Player.currentLevel)
            print(newLevel.name)
            Player.setCurrentLevel(newLevel.name)
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return
        
        if levelName == ("worm"):     
            print(Player.currentLevel)
            newLevel = loadBug()
            Player.setCurrentLevel(newLevel.name)
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return
        
        if levelName == ("bug"):     
            print(Player.currentLevel)
            newLevel = loadSlug()
            Player.setCurrentLevel(newLevel.name)
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return        

        if levelName == ("slug"):          
            newLevel = loadSnail()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return       
        
        if levelName == ("snail"):          
            newLevel = loadLobster()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return              
        
        if levelName == ("lobster"):          
            newLevel = loadJellyfish()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return             
        
        if levelName == ("jellyfish"):          
            newLevel = loadSquid()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return      

        if levelName == ("squid"):          
            newLevel = loadFish()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return          
        
        if levelName == ("fish"):          
            newLevel = loadCthulhu()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return    
        
        if levelName == ("cthulhu"):          
            newLevel = loadJesus()
            Player.setCurrentLevel(newLevel.name)
            paused(newLevel, Player)
            return          
        
        if levelName == ("jesus"):          
            newLevel = loadStarfish()
            Player.setCurrentLevel(newLevel.name)
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            
        elif levelName == ("starfish"):     
            newLevel = loadGuppy()
            Player.setCurrentLevel(newLevel.name)
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
        
        elif levelName == ("guppy"):     
            newLevel = loadGoldfish()
            Player.setCurrentLevel(newLevel.name)
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return        
        
        elif levelName == ("goldfish"):          
            newLevel = loadCatfish()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return       
        
        elif levelName == ("catfish"):          
            newLevel = loadPiranha()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return              
        
        elif levelName == ("piranha"):          
            newLevel = loadShark()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return             
        
        elif levelName == ("shark"):          
            newLevel = loadDolphin()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return      
        
        elif levelName == ("dolphin"):          
            newLevel = loadWhale()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return          
        
        elif levelName == ("whale"):          
            newLevel = loadLochNess()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return    
        
        if levelName == ("lochness"): 
            newLevel = loadJesus2()
            Player.setCurrentLevel(newLevel.name)
            paused(newLevel, Player)
            mainMenu()
        
        elif levelName == ("tadpole"):          
            newLevel = loadFrog()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return       
        
        elif levelName == ("frog"):          
            newLevel = loadNewt()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return
        
        elif levelName == ("newt"):          
            newLevel = loadSnake()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return      
        
        elif levelName == ("snake"):          
            newLevel = loadTurtle()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return        
        
        elif levelName == ("turtle"):          
            newLevel = loadIguana()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return        
           
        elif levelName == ("iguana"):          
            newLevel = loadCrocodile()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return     
        
        elif levelName == ("crocodile"):          
            newLevel = loadDragon()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return        
           
        elif levelName == ("dragon"):          
            newLevel = loadJesus3()
            Player.setCurrentLevel(newLevel.name)    
            runGame(newLevel, Player)
            showGameOverScreen(newLevel, Player)
            mainMenu()
            return
        
        elif levelName == ("jesus3"):          
            
            winGame(Player)
            
            return              
        
    elif choose == 1: #Save game
        saveGame(Player)
        mainMenu()
        return
    
    elif choose == 2:
        submitToLeaderboard(Player)

    elif choose == 3:
        terminate()
        
    else:
        mainMenu()
        return    
        
    pygame.display.update()

def drawGrid(Level):
    
    #galaxy = pygame.image.load("galaxy.png")
    BACKGROUND = Level.background
    
    DISPLAYSURF.blit(BACKGROUND, [0,0])
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    if pygame.event == pygame.K_p:
        pause = True

    return keyUpEvents[0].key

def loadSquidPath():
    name = "squid"
    levelList = generateSquidList()
    

def survivalMode():
    currentPlayer = Player("Player",0,"dragon2", "reptile")
    level = loadDragon2()
    runGame(level, currentPlayer)
    showGameOverScreen(level, currentPlayer)
    mainMenu()  
        
def howToPlay():
    DISPLAYSURF.fill(BLACK)
    gameOverFont2 = pygame.font.Font('freesansbold.ttf', 90)    
    gameOverFont = pygame.font.Font('freesansbold.ttf', 50)
    gameSurf = gameOverFont2.render('How To Play', True, WHITE)
    overSurf = gameOverFont.render("Don't run into yourself, ", True, WHITE)
    otherSurf = gameOverFont.render("eat poison, or hit the wall!", True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    otherRect = otherSurf.get_rect()
    
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 50 + 65)
    otherRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 80 + 95)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    DISPLAYSURF.blit(otherSurf, otherRect)
    
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(3000)
    checkForKeyPress() 
    return    

def viewLeaderboard(Player):

    with open('leaderboard_data.txt', 'r') as input:
        content = input.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    
        
    DISPLAYSURF.fill(BLACK)
    gameOverFont2 = pygame.font.Font('freesansbold.ttf', 90)    
    gameOverFont = pygame.font.Font('freesansbold.ttf', 50)
    gameSurf = gameOverFont2.render('Leaderboard', True, WHITE)
    rank3Surf = gameOverFont.render(str(content[2]), True, WHITE)
    rank2Surf = gameOverFont.render(str(content[1]), True, WHITE)    
    rank1Surf = gameOverFont.render(str(content[0]), True, WHITE)
    
    gameRect = gameSurf.get_rect()
    rank1Rect = rank1Surf.get_rect()
    rank2Rect = rank2Surf.get_rect()
    rank3Rect = rank3Surf.get_rect()

    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    rank3Rect.midtop = (WINDOWWIDTH / 2, gameRect.height + 50 + 65)
    rank2Rect.midtop = (WINDOWWIDTH / 2, gameRect.height + 30 + 45)
    rank1Rect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(rank1Surf, rank1Rect)        
    DISPLAYSURF.blit(rank2Surf, rank2Rect)
    DISPLAYSURF.blit(rank3Surf, rank3Rect)
    
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(5000)
    checkForKeyPress() 
    mainMenu()

def loadAmoeba():
    amoebaBG = pygame.image.load("amoebaBG.png")
    background = amoebaBG
    amoeba0 = pygame.image.load("amoeba.png")
    amoeba1 = pygame.image.load("amoeba2.png")
    amoeba2 = pygame.image.load("amoeba3.png")    
    nodesToWin = 1
    name = "amoeba"
    path = "squid"
    spriteList = [amoeba0, amoeba1, amoeba2]    
    amoebaLevel = Level(name,background,spriteList,nodesToWin,path) 
    return amoebaLevel

def loadWorm():
    mudBG = pygame.image.load("mud.jpg")
    background = mudBG
    worm0 = pygame.image.load("worm1.png")
    worm1 = pygame.image.load("worm2.png")
    nodesToWin = 1
    name = "worm"
    path = "squid"    
    spriteList = [worm0, worm1]    
    wormLevel = Level(name,background,spriteList,nodesToWin, path) 
    return wormLevel

def loadSlug():
    mudBG = pygame.image.load("dirt.jpg")
    background = mudBG
    slug0 = pygame.image.load("slug0.png")
    slug1 = pygame.image.load("slug1.png")
    slug2 = pygame.image.load("slug2.png")    
    nodesToWin = 1
    name = "slug"
    path = "squid"    
    spriteList = [slug0, slug1, slug2]    
    wormLevel = Level(name,background,spriteList,nodesToWin, path) 
    return wormLevel

def loadSnail():
    background = pygame.image.load("snailBG.png")
    sprite0 = pygame.image.load("snail0.png")
    sprite1 = pygame.image.load("snail1.png")
    sprite2 = pygame.image.load("snail2.png")    
    nodesToWin = 1
    name = "snail"
    path = "squid"    
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin,path) 
    return thisLevel

def loadLobster():
    background = pygame.image.load("lobsterBG.png")
    sprite0 = pygame.image.load("lobster0.png")
    sprite1 = pygame.image.load("lobster1.png")
    sprite2 = pygame.image.load("lobster2.png")    
    nodesToWin = 1
    name = "lobster"
    path = "squid"    
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadJellyfish():
    background = pygame.image.load("jellyfishBG.png")
    sprite0 = pygame.image.load("jellyfish0.png")
    sprite1 = pygame.image.load("jellyfish1.png")
    sprite2 = pygame.image.load("jellyfish2.png")    
    nodesToWin = 1
    name = "jellyfish"
    path = "squid"    
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadSquid():
    background = pygame.image.load("squidBG.png")
    sprite0 = pygame.image.load("squid0.png")
    sprite1 = pygame.image.load("squid1.png")
    sprite2 = pygame.image.load("squid2.png")    
    nodesToWin = 1
    name = "squid"
    path = "squid"    
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadCthulhu():
    background = pygame.image.load("cthulhuBG.png")
    sprite0 = pygame.image.load("cthulhu0.png")
    sprite1 = pygame.image.load("cthulhu1.png")
    sprite2 = pygame.image.load("cthulhu2.png")    
    nodesToWin = 1
    name = "cthulhu"
    path = "squid"    
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadStarfish():
    background = pygame.image.load("starfishBG.png")
    sprite0 = pygame.image.load("starfish0.png")
    sprite1 = pygame.image.load("starfish1.png")
    sprite2 = pygame.image.load("starfish2.png")    
    nodesToWin = 1
    path = "fish"    
    name = "starfish"
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadGuppy():
    background = pygame.image.load("guppyBG.png")
    sprite0 = pygame.image.load("guppy0.png")
    sprite1 = pygame.image.load("guppy1.png")
    sprite2 = pygame.image.load("guppy2.png")    
    nodesToWin = 1
    name = "guppy"
    path = "fish"    
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadGoldfish():
    background = pygame.image.load("goldfishBG.png")
    sprite0 = pygame.image.load("goldfish0.png")
    sprite1 = pygame.image.load("goldfish1.png")
    sprite2 = pygame.image.load("goldfish2.png")    
    nodesToWin = 1
    name = "goldfish"
    path = "fish"    
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin,path) 
    return thisLevel

def loadCatfish():
    background = pygame.image.load("catfishBG.png")
    sprite0 = pygame.image.load("catfish0.png")
    sprite1 = pygame.image.load("catfish1.png")
    sprite2 = pygame.image.load("catfish2.png")    
    nodesToWin = 1
    name = "catfish"
    path = "fish"        
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin,path) 
    return thisLevel

def loadPiranha():
    background = pygame.image.load("piranhaBG.png")
    sprite0 = pygame.image.load("piranha0.png")
    sprite1 = pygame.image.load("piranha1.png")
    sprite2 = pygame.image.load("piranha2.png")    
    nodesToWin = 1
    name = "piranha"
    path = "fish"        
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadShark():
    background = pygame.image.load("sharkBG.png")
    sprite0 = pygame.image.load("shark0.png")
    sprite1 = pygame.image.load("shark1.png")
    sprite2 = pygame.image.load("shark2.png")    
    nodesToWin = 1
    name = "shark"
    path = "fish"        
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadDolphin():
    background = pygame.image.load("dolphinBG.png")
    sprite0 = pygame.image.load("dolphin0.png")
    sprite1 = pygame.image.load("dolphin1.png")
    sprite2 = pygame.image.load("dolphin2.png")    
    nodesToWin = 1
    name = "dolphin"
    path = "fish"        
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadWhale():
    background = pygame.image.load("whaleBG.png")
    sprite0 = pygame.image.load("whale0.png")
    sprite1 = pygame.image.load("whale1.png")
    sprite2 = pygame.image.load("whale2.png")    
    nodesToWin = 1
    path = "fish"        
    name = "whale"
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadLochNess():
    background = pygame.image.load("lochnessBG.png")
    sprite0 = pygame.image.load("lochness0.png")
    sprite1 = pygame.image.load("lochness1.png")
    sprite2 = pygame.image.load("lochness2.png")    
    nodesToWin = 2
    name = "lochness"
    path = "fish"        
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadTadpole():
    background = pygame.image.load("tadpoleBG.png")
    sprite0 = pygame.image.load("tadpole0.png")
    sprite1 = pygame.image.load("tadpole1.png")
    sprite2 = pygame.image.load("tadpole2.png")    
    nodesToWin = 1
    name = "tadpole"
    path = "reptile"        
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadFrog():
    background = pygame.image.load("frogBG.png")
    sprite0 = pygame.image.load("frog0.png")
    sprite1 = pygame.image.load("frog1.png")
    sprite2 = pygame.image.load("frog2.png")    
    nodesToWin = 1
    name = "frog"
    path = "reptile"        
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadNewt():
    background = pygame.image.load("newtBG.png")
    sprite0 = pygame.image.load("newt0.png")
    sprite1 = pygame.image.load("newt1.png")
    sprite2 = pygame.image.load("newt2.png")    
    nodesToWin = 1
    name = "newt"
    path = "reptile"        
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadSnake():
    background = pygame.image.load("snakeBG.png")
    sprite0 = pygame.image.load("snake0.png")
    sprite1 = pygame.image.load("snake1.png")
    sprite2 = pygame.image.load("snake2.png")    
    nodesToWin = 1
    name = "snake"
    path = "reptile"        
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadTurtle():
    background = pygame.image.load("turtleBG.png")
    sprite0 = pygame.image.load("turtle0.png")
    sprite1 = pygame.image.load("turtle1.png")
    sprite2 = pygame.image.load("turtle2.png")    
    nodesToWin = 1
    name = "turtle"
    path = "reptile"        
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadIguana():
    background = pygame.image.load("iguanaBG.png")
    sprite0 = pygame.image.load("iguana0.png")
    sprite1 = pygame.image.load("iguana1.png")
    sprite2 = pygame.image.load("iguana2.png")    
    nodesToWin = 1
    name = "iguana"
    path = "reptile"        
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadCrocodile():
    background = pygame.image.load("crocodileBG.png")
    sprite0 = pygame.image.load("crocodile0.png")
    sprite1 = pygame.image.load("crocodile1.png")
    sprite2 = pygame.image.load("crocodile2.png")    
    nodesToWin = 1
    name = "crocodile"
    path = "reptile"        
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadDragon():
    background = pygame.image.load("dragonBG.png")
    sprite0 = pygame.image.load("dragon0.png")
    sprite1 = pygame.image.load("dragon1.png")
    sprite2 = pygame.image.load("dragon2.png")    
    nodesToWin = 1
    name = "dragon"
    path = "reptile"        
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel

def loadDragon2():
    background = pygame.image.load("dragonBG.png")
    sprite0 = pygame.image.load("dragon0.png")
    sprite1 = pygame.image.load("dragon1.png")
    sprite2 = pygame.image.load("dragon2.png")    
    nodesToWin = 1000
    name = "dragon2"
    path = "reptile"        
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel


def loadJesus3():
    background = pygame.image.load("heaven1.jpg")
    sprite0 = pygame.image.load("jesus0.png")
    sprite1 = pygame.image.load("jesus1.png")
    sprite2 = pygame.image.load("jesus2.png")    
    nodesToWin = 1
    name = "jesus3"
    path = "reptile"        
    spriteList = [sprite0, sprite1, sprite2]    
    thisLevel = Level(name,background,spriteList,nodesToWin, path) 
    return thisLevel


def loadBug():
    bugBG = pygame.image.load("bugBG.png")
    background = bugBG
    bug0 = pygame.image.load("bug0.png")
    bug1 = pygame.image.load("bug1.png")
    bug2 = pygame.image.load("bug2.png")    
    nodesToWin = 1
    name = "bug"
    path = "squid"
    spriteList = [bug0, bug1, bug2]    
    bugLevel = Level(name,background,spriteList,nodesToWin, path) 
    return bugLevel

def loadFish():
    oceanBG = pygame.image.load("ocean.png")
    background = oceanBG
    fish0 = pygame.image.load("fish0.png")
    fish1 = pygame.image.load("fish1.png")
    fish2 = pygame.image.load("fish2.png")    
    nodesToWin = 1
    name = "fish"
    path = "squid"        
    spriteList = [fish0, fish1, fish2]    
    fishLevel = Level(name,background,spriteList,nodesToWin, path) 
    return fishLevel

def loadJesus():
    heavenBG = pygame.image.load("heaven1.jpg")
    background = heavenBG
    jesus0 = pygame.image.load("jesus0.png")
    jesus1 = pygame.image.load("jesus1.png")
    jesus2 = pygame.image.load("jesus2.png")    
    nodesToWin = 20
    path = "squid"        
    name = "jesus"
    spriteList = [jesus0, jesus1, jesus2]    
    jesusLevel = Level(name,background,spriteList,nodesToWin, path) 
    return jesusLevel


def loadJesus2():
    heavenBG = pygame.image.load("heaven1.jpg")
    background = heavenBG
    jesus0 = pygame.image.load("jesus0.png")
    jesus1 = pygame.image.load("jesus1.png")
    jesus2 = pygame.image.load("jesus2.png")    
    nodesToWin = 20
    path = "fish"        
    name = "jesus2"
    spriteList = [jesus0, jesus1, jesus2]    
    jesusLevel = Level(name,background,spriteList,nodesToWin, path) 
    return jesusLevel

def mainMenu():

    amoebaLevel = loadAmoeba()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        
    SURFACE.fill(BLACK)
    pygame.display.update()
    choose = dm.dumbmenu(DISPLAYSURF, [
                            'New Story',
                            'Load Story',
                            'How To Play',
                            'Leaderboard',
                            'Survival',
                            'Quit Game'], 64,64,None,32,1.4,PURPLE,RED)
    
    if choose == 0: #New game
        currentPlayer = Player("Player",0,"amoeba", "squid")
        runGame(amoebaLevel, currentPlayer)
        showGameOverScreen(amoebaLevel, currentPlayer)
        mainMenu()
        
        return
    
    elif choose == 1: #Saved game
        currentPlayer = loadSavedGame()
        levelList = generateLevelList()
        
        for level in levelList:
            if level.name == currentPlayer.currentLevel:
                runGame(level, currentPlayer)
                showGameOverScreen(level, currentPlayer)                
                mainMenu()            
        
        runGame(Level, currentPlayer)
        showGameOverScreen(Level, currentPlayer)
        mainMenu()
        return
    
    elif choose == 2: #How to play
        howToPlay()   
        mainMenu()
        
    elif choose == 3: #Leaderboard
        currentPlayer = loadSavedGame()        
        viewLeaderboard(currentPlayer)   
        mainMenu()
        
    elif choose == 4: #Survival Mode
        survivalMode()
        mainMenu()    
        
    elif choose == 5: #Quit game
        terminate()
    
    else:
        mainMenu()
        return    

def saveGame(Player): 
    with open('save_data.pkl', 'wb') as output:
        savedGame = Player.score, Player.currentLevel, Player.name, Player.currentPath
        pickle.dump(savedGame, output, pickle.HIGHEST_PROTOCOL)
        #print(savedGame)
    mainMenu()

def promptPlayerName():
    textinput = pygame_textinput.TextInput()
    
    screen = pygame.display.set_mode((1000, 600))
    clock = pygame.time.Clock()
    
    playerName = None
    
    while playerName is None:
        screen.fill((225, 225, 225))
    
        gameOverFont2 = pygame.font.Font('freesansbold.ttf', 90)    
        gameSurf = gameOverFont2.render('Enter Name:', True, WHITE)
        gameRect = gameSurf.get_rect()
        gameRect.midtop = (WINDOWWIDTH / 2, 10)
    
        screen.blit(gameSurf, gameRect)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
                
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:     
                    playerName = textinput.get_text()
                    return playerName
                    
       
        # Feed it with events every frame
        textinput.update(events)
        # Blit its surface onto the screen
        screen.blit(textinput.get_surface(), (10, 10))
    
        pygame.display.update()
        clock.tick(30)
        
def submitToLeaderboard(Player):
    
    playerName = promptPlayerName()
    Player.setName(playerName)
        
    DISPLAYSURF.fill(BLACK)
    
    with open('leaderboard_data.txt', 'a') as output:
        leaderboard = (Player.name + ": " + str(Player.score) +"\n")
        output.write(leaderboard)
        
    gameOverFont2 = pygame.font.Font('freesansbold.ttf', 90)    
    gameOverFont = pygame.font.Font('freesansbold.ttf', 50)
    gameSurf = gameOverFont2.render('Leaderboard', True, WHITE)
    overSurf = gameOverFont.render("Score was submitted successfully!", True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 50 + 65)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    
    pygame.display.update()
    pygame.time.wait(1000)
    checkForKeyPress()    
    
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press any key to play.', True, BLACK)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 50)
    titleSurf1 = titleFont.render('SNAKE', True, WHITE, BLACK)
    titleSurf2 = titleFont.render('EVOLUTIONS', True, RED)
    degrees1 = 0
    degrees2 = 0
    while True:
        
        DISPLAYSURF.fill(BLACK)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 1 
        degrees2 += 51 

def terminate():
    pygame.quit()
    sys.exit()

def generateSquidList():
    
    amoebaLevel = loadAmoeba()
    wormLevel = loadWorm()
    bugLevel = loadBug()
    snailLevel = loadSnail()
    lobsterLevel = loadLobster()
    jellyfishLevel = loadJellyfish()
    squidLevel = loadSquid()
    cthulhuLevel = loadCthulhu()
    jesusLevel = loadJesus()
    
    levelList = [amoebaLevel, wormLevel, bugLevel, snailLevel, lobsterLevel, jellyfishLevel, squidLevel, cthulhuLevel, jesusLevel]  
    
    return levelList

def generateFishList():
    
    starfishLevel = loadStarfish()
    guppyLevel = loadGuppy()
    goldfishLevel = loadGoldfish()
    catfishLevel = loadCatfish()
    piranhaLevel = loadPiranha()
    sharkLevel = loadShark()
    dolphinLevel = loadDolphin()
    whaleLevel = loadWhale()
    lochnessLevel = loadLochNess()
    jesus2Level = loadJesus2()
    
    levelList = [starfishLevel, guppyLevel, goldfishLevel, catfishLevel, piranhaLevel, sharkLevel, dolphinLevel, whaleLevel, lochnessLevel, jesus2Level]  
    
    return levelList

def generateLevelList():
    
    amoebaLevel = loadAmoeba()    
    wormLevel = loadWorm()
    bugLevel = loadBug()
    slugLevel = loadSlug()
    snailLevel = loadSnail()
    lobsterLevel = loadLobster()
    jellyfishLevel = loadJellyfish()
    squidLevel = loadSquid()
    cthulhuLevel = loadCthulhu()
    fishLevel = loadFish()
    jesusLevel = loadJesus()
    jesus2Level = loadJesus2()    
    starfishLevel = loadStarfish()
    guppyLevel = loadGuppy()
    goldfishLevel = loadGoldfish()
    catfishLevel = loadCatfish()
    piranhaLevel = loadPiranha()
    sharkLevel = loadShark()
    dolphinLevel = loadDolphin()
    whaleLevel = loadWhale()
    lochnessLevel = loadLochNess()
    jesus2Level = loadJesus2()
    tadpoleLevel = loadTadpole()
    frogLevel = loadFrog()
    newtLevel = loadNewt()
    snakeLevel = loadSnake()
    turtleLevel = loadTurtle()
    iguanaLevel = loadIguana()
    crocodileLevel = loadCrocodile()
    dragonLevel = loadDragon()
    dragon2Level = loadDragon2()    
    jesus3Level = loadJesus3()
    
    levelList = [amoebaLevel, wormLevel, bugLevel, slugLevel, snailLevel, lobsterLevel, jellyfishLevel, squidLevel, fishLevel,
                 starfishLevel, guppyLevel, goldfishLevel, catfishLevel, piranhaLevel, sharkLevel, dolphinLevel, whaleLevel, lochnessLevel, 
                 cthulhuLevel, jesusLevel, jesus2Level, tadpoleLevel, frogLevel, newtLevel, snakeLevel, turtleLevel, iguanaLevel,
                 crocodileLevel, dragonLevel, jesus3Level]  
    
    return levelList
    
def showGameOverScreen(Level, Player):
        
    background = pygame.image.load("heaven.jpg")
    DISPLAYSURF.blit(background, [0,0])    
    gameOverFont = pygame.font.Font('freesansbold.ttf', 100)
    gameSurf = gameOverFont.render('RIP!', True, WHITE)
    overSurf = gameOverFont.render(':(', True, WHITE)
    
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    
    currentLevel = Level.name
    
    levelList = generateLevelList()
    
    pygame.display.update()    
    
    choose = dm.dumbmenu(DISPLAYSURF, [
        'Resume from last level',
        'Main Menu',
        'Submit To Leaderboard',
        'Quit Game'], 64,64,None,32,1.4,PURPLE,RED)
        
    if choose == 0: #Resume from last level 
        
        for level in levelList:
            if level.name == currentLevel:
                runGame(level, Player)
                mainMenu()
                #return                
    elif choose == 1: #Main Menu
        mainMenu()
        
    elif choose == 2: #Submit to leaderboard
        submitToLeaderboard(Player)
        
    elif choose == 3: #Terminate
        terminate()        
        
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue
    return

def loadSavedGame():
    
    with open('save_data.pkl', 'rb') as input:
        loadedFile = pickle.load(input)
        
    score = loadedFile[0]
    currentLevel = loadedFile[1]
    name = loadedFile[2]
    path = loadedFile[3]
        
    loadedPlayer = Player(name, score, currentLevel, path)
    return loadedPlayer

def runGame(Level, Player):

    # Set a random start point.
    background = Level.background
    DISPLAYSURF.blit(background, [0,0])      
    pygame.display.update()
    nodesToWin = Level.nodesToWin
        
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    playerCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Place food in random space
    food = getRandomLocation()
    
    # Place poison in random space
    #poison = getRandomLocation() #Disabled for testing

    while True: # main game loop        
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the player has hit itself or the edge
        if playerCoords[HEAD]['x'] == -1 or playerCoords[HEAD]['x'] == CELLWIDTH or playerCoords[HEAD]['y'] == -1 or playerCoords[HEAD]['y'] == CELLHEIGHT:
            return
        for playerBody in playerCoords[1:]:
            if playerBody['x'] == playerCoords[HEAD]['x'] and playerBody['y'] == playerCoords[HEAD]['y']:
                return # game over

        # check if player has eaten the food
        if playerCoords[HEAD]['x'] == food['x'] and playerCoords[HEAD]['y'] == food['y']:
            # don't remove player's tail segment
            food = getRandomLocation() # set a new food somewhere
        else:
            del playerCoords[-1] # remove player's tail segment
            
        ## check if player has eaten poison
        #if playerCoords[HEAD]['x'] == poison['x'] and playerCoords[HEAD]['y'] == poison['y']:
            ## don't remove player's tail segment
            #return #game over

        # move the player by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': playerCoords[HEAD]['x'], 'y': playerCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': playerCoords[HEAD]['x'], 'y': playerCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': playerCoords[HEAD]['x'] - 1, 'y': playerCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': playerCoords[HEAD]['x'] + 1, 'y': playerCoords[HEAD]['y']}
        playerCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid(Level)
        drawplayer(playerCoords, Level)
        #drawpoison(poison) #Disabled for testing purposes
        drawfood(food)
        score = drawScore(len(playerCoords) - 3, Player)                
        Player.setCurrentLevel(Level.name)        
        drawScore(len(playerCoords) - 3, Player)
        pygame.display.update()
        totalScore = (len(playerCoords)-3 + Player.getScore())
        Player.setScore(totalScore)        
        FPSCLOCK.tick(FPS)
        checkWinLevel(score, Level, Player)
        currentPath = Player.currentPath
        checkWinPath(Level, Player, currentPath)

if __name__ == '__main__':
    main()