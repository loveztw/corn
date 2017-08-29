'''
Created on Aug 16, 2017

@author: zhout
'''
import copy

class menuDto:
    def __init__(self):
        self.__menuList = []
    
    KEY_MENUNAME = 'name'
    
    KEY_TYPE = 'type'
    
    KEY_TYPEID = 'typeid'
    
    KEY_KEY = 'key'
    
    KEY_URL = 'url'
    
    KEY_PARENT = 'parent'
    
    KEY_PARENTID = 'pid'
    
    KEY_EDITFLAG = 'editflag'

    def getMenuList(self):
        return self.__menuList

    def __getSubButton(self, dicts, parent):
    
        for subDict in dicts:
            
            item = copy.deepcopy(subDict)
                
            if parent:
                item[self.KEY_PARENT] = parent
            
            self.__menuList.append(item)
            
            if 'sub_button' in subDict:
                self.__getSubButton(subDict['sub_button'], subDict['name'])
    
    def dictLoad(self, inputDict):
        buttonDict = {}
        if 'menu' in inputDict:
            buttonDict =inputDict['menu']
         
            if 'button' in buttonDict:
                self.__getSubButton(buttonDict['button'], None)