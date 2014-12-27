import pygame, sys
from RTS.main.ScreenManager import ScreenManager
from RTS.main.SoundManager import SoundManager
from RTS.main.EventHandler import EventHandler
from RTS.main.InGameScreenManager import InGameScreenManager
from RTS.gui.MainMenu import MainMenu
'''
Created on 30. 11. 2014

@author: fdobrovolny
'''
class main(object):
    def __init__(self):
        
        self.version = "0.0.1"
        self.gameDevelopmentState = "Pre-Alpha"
        
        self.EventHandler = EventHandler(self)
        self.ScreenManager = ScreenManager(self, 1024, 600, 30)
        self.SoundManager = SoundManager(self)
        self.mainMenu = MainMenu(self)
        #self.InGameScreenManager = InGameScreenManager(self, 64, 128,)
        self.start_loop()
    
    def start_loop(self):
        while True:
            self.ScreenManager.clearScreen()
            self.EventHandler.tick()
            self.mainMenu.draw()
            #self.InGameScreenManager.Draw()
            self.ScreenManager.UpdateDisplay()
    
    
    ''' this func is called when app is closing'''
    def quit(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    main()