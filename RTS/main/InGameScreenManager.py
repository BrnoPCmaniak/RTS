import pygame
from pygame.locals import *
from pygame.image import *

from RTS.main.isoMath import IsoMathHelper
from RTS.main.MapLoader import Map
from RTS.gui.GLTexture import Texture
'''
Created on 25. 12. 2014

@author: fdobrovolny
'''

class InGameScreenManager(object):
    '''
    This class takes care of drawing map units buldings etc.
    '''


    def __init__(self, main, tileSizeX, tileSizeY, map="base"):
        '''
        Constructor
        '''
        self.main = main
        self.screenManager = self.main.ScreenManager
        self.tileSizeX = tileSizeX #H
        self.tileSizeY = tileSizeY #W
        
        self.IsoMathHelper = None
        self._IsoMathHelperInit()
        
        self.MapPos = self.MapPosX, self.MapPosY =  0, 0
        self.MapMovConst = 10  
        self.RegisterMapMovement()
        
        self.RecalculateDisplayTiles = True # determine if we have to recalculate which tiles should be shown
        self.RDT_X_S = None
        self.RDT_X_E = None
        self.RDT_Y_S = None
        self.RDT_Y_E = None
        
        self.Map = Map(map)
        self.Map.loadMap()
        self.tiles = []
        self.loadTextures()
        
        self.MouseSelectedTexture = Texture("../res/map/select_tile.png")
        self.MouseActive = True # False when user is in GUI
        
    
    def _IsoMathHelperInit(self):
        self.IsoMathHelper = IsoMathHelper(self.tileSizeY/2, self.tileSizeX/2, self.screenManager.width/2)
    
    
    def Draw(self):
        if self.RecalculateDisplayTiles:
            self.RDT()
        for x in range(self.RDT_X_S, self.RDT_X_E):
            for y in range(self.RDT_Y_S, self.RDT_Y_E):
                tile = self.Map.matrix[y][x]
                tile_x, tile_y = self.IsoMathHelper.Map2ScreenFIN((x,y), self.MapPos)
                self.tiles[tile].draw(tile_x, tile_y)
        
        mouseCoord = self.IsoMathHelper.Screen2MapFIN(pygame.mouse.get_pos(), self.MapPos)
        
        if  -1 < mouseCoord[0] <= self.Map.sizeX and -1 < mouseCoord[1] <= self.Map.sizeY and self.MouseActive:
            select_x, select_y = self.IsoMathHelper.Map2ScreenFIN((int(mouseCoord[0]), int(mouseCoord[1])), self.MapPos)
            self.MouseSelectedTexture.draw(select_x, select_y)
    
    
    def moveMap(self, dir1, dir2):
        if dir1:
            self.MapPosY += self.MapMovConst
        elif not dir1:
            self.MapPosY -= self.MapMovConst
        if dir2:
            self.MapPosX += self.MapMovConst
        elif not dir2:
            self.MapPosX -= self.MapMovConst
    
    
    def moveMapUp(self):
        self.MapPosY += self.MapMovConst
        self.MapPos = self.MapPosX, self.MapPosY
        self.RecalculateDisplayTiles = True
    
    
    def moveMapDown(self):
        self.MapPosY -= self.MapMovConst
        self.MapPos = self.MapPosX, self.MapPosY
        self.RecalculateDisplayTiles = True
    
    
    def moveMapRight(self):
        self.MapPosX -= self.MapMovConst
        self.MapPos = self.MapPosX, self.MapPosY
        self.RecalculateDisplayTiles = True
    
    
    def moveMapLeft(self):
        self.MapPosX += self.MapMovConst
        self.MapPos = self.MapPosX, self.MapPosY
        self.RecalculateDisplayTiles = True
    
    
    def RegisterMapMovement(self):
        self.main.EventHandler.registerKEYPRESSEDevent(K_UP, self.moveMapUp)
        self.main.EventHandler.registerKEYPRESSEDevent(K_DOWN, self.moveMapDown)
        self.main.EventHandler.registerKEYPRESSEDevent(K_LEFT, self.moveMapLeft)
        self.main.EventHandler.registerKEYPRESSEDevent(K_RIGHT, self.moveMapRight)
    
    
    def loadTextures(self):
        print(self.Map.sizeX, self.Map.sizeX)
        for TextureSrc in self.Map.textures:
            self.tiles.append(Texture("../res/map/" + TextureSrc + ".png"))
    
    
    def checkEdges(self):
        if self.MapPosY < -self.IsoMathHelper.Map2Screen((self.Map.sizeX,self.Map.sizeY-(self.screenManager.width*1.5)/self.tileSizeY))[1]:
            self.MapPosY = -self.IsoMathHelper.Map2Screen((self.Map.sizeX,self.Map.sizeY-(self.screenManager.width*1.5)/self.tileSizeY))[1]
        elif self.MapPosY > self.screenManager.width/4:
            self.MapPosY = int(self.screenManager.width/4)
        
        if self.MapPosX > self.IsoMathHelper.Map2Screen((int(self.Map.sizeX+(self.screenManager.height*0.25)/self.tileSizeX),self.Map.sizeY))[1]:
            self.MapPosX = self.IsoMathHelper.Map2Screen((int(self.Map.sizeX+(self.screenManager.height*0.25)/self.tileSizeX),self.Map.sizeY))[1]
        elif self.MapPosX < -self.IsoMathHelper.Map2Screen((int(self.Map.sizeX+(self.screenManager.height*0.25)/self.tileSizeX),self.Map.sizeY))[1]:
            self.MapPosX = -self.IsoMathHelper.Map2Screen((int(self.Map.sizeX+(self.screenManager.height*0.25)/self.tileSizeX),self.Map.sizeY))[1]
        
        
    
    def RDT(self):
        self.checkEdges()
        TopLeft = self.IsoMathHelper.Screen2MapFIN((0,0), self.MapPos)
        TopRight = self.IsoMathHelper.Screen2MapFIN((self.screenManager.width,0), self.MapPos)
        BottomRight = self.IsoMathHelper.Screen2MapFIN((self.screenManager.height, self.screenManager.width), self.MapPos)
        BottomLeft = self.IsoMathHelper.Screen2MapFIN((0, self.screenManager.height), self.MapPos)
        
        self.RDT_X_S = int(TopLeft[0]) - 2
        self.RDT_X_E = int(BottomRight[0]) + 2
        
        self.RDT_Y_S = int(TopRight[1]) - 2
        self.RDT_Y_E = int(BottomLeft[1]) + 2
        
        if self.RDT_X_S < 0:
            self.RDT_X_S = 0
        elif self.RDT_X_S > self.Map.sizeX:
            self.RDT_X_S = self.Map.sizeX
        
        if self.RDT_X_E < 0:
            self.RDT_X_E = 0
        elif self.RDT_X_E > self.Map.sizeX:
            self.RDT_X_E = self.Map.sizeX
        
        if self.RDT_Y_S < 0:
            self.RDT_Y_S = 0
        elif self.RDT_Y_S > self.Map.sizeY:
            self.RDT_Y_S = self.Map.sizeY
        
        if self.RDT_Y_E < 0:
            self.RDT_Y_E = 0
        elif self.RDT_Y_E > self.Map.sizeY:
            self.RDT_Y_E = self.Map.sizeY
        
        self.RecalculateDisplayTiles = False
        
