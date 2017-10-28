'''Class created to facilitate the saving and loading of game data'''


import os, sys



class SaveGame:
    def __init__(self, name):
        self.name = name
        self.properties = {'Number of times played':0, 'Top Score':0}
        self.folder = 'game_data'
        self.fh = None

    def load(self):
        filename = self.name + '.txt'
        if os.path.exists(self.folder + '/' + filename):
            self.fh = open(self.folder + '/' + filename,'r')
            properties = self.fh.readlines()
            self.fh.close()
            for line in properties:
                prop = line.split(':')
                self.properties[prop[0]] = prop[1]
            return True
        return False 

    def get_properties(self):
        return self.properties

    def save(self, properties):
        filename = self.name + '.txt'
        self.fh = open(self.folder + '/' + filename,'w')
        for key in properties.keys():
            self.fh.write(key + ':' + str(properties[key]) + '\n')
        self.fh.close()
        
