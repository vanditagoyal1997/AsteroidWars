import math

class Vector_2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def addVectors(self,x,y):
        new_x = self.x + x
        new_y = self.y + y
        return Vector_2D(new_x,new_y)

    def value(self):
        return math.sqrt(self.x**2 + self.y**2)
