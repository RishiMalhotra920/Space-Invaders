"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

# Rishi Malhotra (rm725)
# December 8, 2019
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Returns the x coordinate of the ship
        """
        return self.x

    def getY(self):
        """
        Returns the y coordinate of the ship
        """
        return self.y

    def setX(self,x):
        """
        Set the x coordinate of the ship

        Paramter x: The x coordinate to set
        Precondition: 0<=x<=GAME_WIDTH. x is int or float
        """
        assert 0<=x<=GAME_WIDTH and type(x) in [int,float]
        self.x = x

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self,x,y,width,height,source):
        """
        Initializes the ship's x,y,width,height,source by passing them into
        the superclass's initializer

        Parameter x: The x coordinate of the ship
        Precondition: 0<=x<=GAME_WIDTH. x is int or float

        Parameter y: The y coordinate of the ship
        Precondition: 0<=y<=GAME_HEIGHT. y is int or float

        Parameter width: The width of the ship
        Precondition: 0<width<=GAME_WIDTH. width is int or float

        Parameter height: The height of the ship
        Precondition: 0<=height<=GAME_HEIGHT. height is int or float

        Parameter source: The image file source
        Precondition: source is a string
        """
        assert 0<=x<=GAME_WIDTH and type(x) in [int,float]
        assert 0<=y<=GAME_HEIGHT and type(y) in [int,float]
        assert 0<=width<=GAME_WIDTH and type(width) in [int,float]
        assert 0<=height<=GAME_HEIGHT and type(height) in [int,float]
        assert type(source) == str

        super().__init__(x=x,y=y,width=width,height=height,source=source)

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self,bolt):
        """
        Returns True if the alien bolt collides with this player

        This method first determines the 4 corners of the bolt.This method
        returns False if bolt was not fired by the alien or if
        no collision

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt,Bolt)

        if not bolt.isPlayerBolt():
            c1 = (bolt.getX() + BOLT_WIDTH/2, bolt.getY() + BOLT_HEIGHT/2)
            c2 = (bolt.getX() + BOLT_WIDTH/2, bolt.getY() - BOLT_HEIGHT/2)
            c3 = (bolt.getX() - BOLT_WIDTH/2, bolt.getY() + BOLT_HEIGHT/2)
            c4 = (bolt.getX() - BOLT_WIDTH/2, bolt.getY() - BOLT_HEIGHT/2)
            return self.contains(c1) or self.contains(c2) or self.contains(c3)\
            or self.contains(c4)
        return False
        # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Returns the x coordinate of the alien
        """
        return self.x

    def getY(self):
        """
        Returns the y coordinate of the alien
        """
        return self.y

    def setX(self,x):
        """
        Set the x coordinate of the alien

        Paramter x: The x coordinate to set
        Precondition: 0<=x<=GAME_WIDTH. x is int or float
        """
        assert 0<=x<=GAME_WIDTH and type(x) in [int,float]
        self.x = x

    def setY(self,y):
        """
        Set the y coordinate of the alien

        Paramter y: The y coordinate to set
        Precondition: 0<=y<=GAME_HEIGHT. y is int or float
        """
        assert 0<=y<=GAME_HEIGHT and type(y) in [int,float]
        self.y = y

    #INITIALIZER TO CREATE AN ALIEN
    def __init__(self,x,y,width,height,source):
        """
        Initializes the alien's x,y,width,height,source by passing them into
        the superclass's initializer

        Parameter x: The x coordinate of the alien
        Precondition: 0<=x<=GAME_WIDTH. x is int or float

        Parameter y: The y coordinate of the alien
        Precondition: 0<=y<=GAME_HEIGHT. y is int or float

        Parameter width: The width of the alien
        Precondition: 0<width<=GAME_WIDTH. width is int or float

        Parameter height: The height of the alien
        Precondition: 0<=height<=GAME_HEIGHT. height is int or float

        Parameter source: The image file source
        Precondition: source is a string
        """
        assert 0<=x<=GAME_WIDTH and type(x) in [int,float]
        assert 0<=y<=GAME_HEIGHT and type(y) in [int,float]
        assert 0<=width<=GAME_WIDTH and type(width) in [int,float]
        assert 0<=height<=GAME_HEIGHT and type(height) in [int,float]
        assert type(source) == str
        super().__init__(x=x,y=y,width=width,height=height,source=source)

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method first determines the 4 corners of the bolt.This method
        returns False if bolt was not fired by the player or if
        no collision.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt,Bolt)

        if bolt.isPlayerBolt():
            c1 = (bolt.getX() + BOLT_WIDTH/2, bolt.getY() + BOLT_HEIGHT/2)
            c2 = (bolt.getX() + BOLT_WIDTH/2, bolt.getY() - BOLT_HEIGHT/2)
            c3 = (bolt.getX() - BOLT_WIDTH/2, bolt.getY() + BOLT_HEIGHT/2)
            c4 = (bolt.getX() - BOLT_WIDTH/2, bolt.getY() - BOLT_HEIGHT/2)
            return self.contains(c1) or self.contains(c2) or self.contains(c3)\
            or self.contains(c4)
        return False

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Returns the bolt X coordinates
        """
        return self.x

    def getY(self):
        """
        Returns the bolt y coordinates
        """
        return self.y

    def setX(self,x):
        """
        Sets the bolt's x coordinate to parameter x

        Parameter x: the x coordinate to update
        Precondition: x is an int or float
        """
        assert type(x) in [int,float]
        self.x=x

    def setY(self,y):
        """
        Sets the bolt's y coordinate to parameter y

        Parameter y: the y coordinate to update
        Precondition: y is an int or float
        """
        assert type(y) in [int,float]
        self.y=y

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,width,height,fillcolor,linecolor,velocity):
        """
        Initializes the class

        Sets x,y,width,height,source from the parent. Sets velocity manually

        Parameter x: The x coordinate of the alien
        Precondition: 0<=x<=GAME_WIDTH. x is int or float

        Parameter y: The y coordinate of the alien
        Precondition: 0<=y<=GAME_HEIGHT. y is int or float

        Parameter width: The width of the alien
        Precondition: 0<width<=GAME_WIDTH. width is int or float

        Parameter height: The height of the alien
        Precondition: 0<=height<=GAME_HEIGHT. height is int or float

        Parameter fillcolor: The linecolor of the bolt
        Precondition: linecolor is a string

        Parameter linecolor: The fillcolor of the bolt
        Precondition: fillcolor is a string

        Parameter velocity: The velocity
        Precondition: velocity is int or float
        """
        assert 0<=x<=GAME_WIDTH and type(x) in [int,float]
        assert 0<=y<=GAME_HEIGHT and type(y) in [int,float]
        assert 0<=width<=GAME_WIDTH and type(width) in [int,float]
        assert 0<=height<=GAME_HEIGHT and type(height) in [int,float]
        assert type(fillcolor) == str
        assert type(linecolor) == str
        assert type(velocity) in [int,float]
        super().__init__(x=x,y=y,width=width,height=height,\
        fillcolor=fillcolor,linecolor=linecolor)
        self._velocity = velocity

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        Returns whether the bolt is a player's bolt

        True indicates player's bolt. False indicates alien's bolt.Checks
        if speed > 0 then it is a player's bolt. Otherwise it is an
        alien's bolts
        """
        return self._velocity > 0

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE


class Barrier(GRectangle):
    """
    A class representing a defense barrier.

    The defense barrier is just a rectangle protecting the user
    from bullets. The defense barrier will provide respite from bullets.
    All defense barriers will have health
    However instances of this class will have health BARRIER_HEALTH. Everytime
    a bullet hits the barrier, the health of the barrier will reduce if
    they are struck with a player or alien bolt.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _health: the the health of the barrier
    # Invariant: _health is an int or float

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,x,y,width,height,fillcolor,linecolor):
        """
        Initializes the class

        Sets x,y,width,height,source from the parent. Sets velocity manually

        Parameter x: The x coordinate of the alien
        Precondition: 0<=x<=GAME_WIDTH. x is int or float

        Parameter y: The y coordinate of the alien
        Precondition: 0<=y<=GAME_HEIGHT. y is int or float

        Parameter width: The width of the alien
        Precondition: 0<width<=GAME_WIDTH. width is int or float

        Parameter height: The height of the alien
        Precondition: 0<=height<=GAME_HEIGHT. height is int or float

        Parameter fillcolor: The linecolor of the bolt
        Precondition: linecolor is a string

        Parameter linecolor: The fillcolor of the bolt
        Precondition: fillcolor is a string

        Parameter velocity: The velocity
        Precondition: velocity is int or float
        """
        assert 0<=x<=GAME_WIDTH and type(x) in [int,float]
        assert 0<=y<=GAME_HEIGHT and type(y) in [int,float]
        assert 0<=width<=GAME_WIDTH and type(width) in [int,float]
        assert 0<=height<=GAME_HEIGHT and type(height) in [int,float]
        assert type(fillcolor) == str
        assert type(linecolor) == str

        super().__init__(x=x,y=y,width=width,height=height,\
        fillcolor=fillcolor,linecolor=linecolor)
        self._health = BARRIER_HEALTH

    def reduceHealth(self,h):
        """
        Reduces the health of the barrier by h

        Parameter h: The number by which to reduce health
        Precondition: h is an integer or float
        """
        assert type(h) in [int,float]
        self._health -= h

    def barrierDestroyed(self):
        """
        Returns a boolean: True if barrier destroyed, False if not destroyed
        """
        return self._health <= 0

    def collides(self,bolt):
        """
        Returns True if the bolt hits any barrier.

        This method first determines the 4 corners of the bolt.This method
        returns False if no collision.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt,Bolt)

        c1 = (bolt.getX() + BOLT_WIDTH/2, bolt.getY() + BOLT_HEIGHT/2)
        c2 = (bolt.getX() + BOLT_WIDTH/2, bolt.getY() - BOLT_HEIGHT/2)
        c3 = (bolt.getX() - BOLT_WIDTH/2, bolt.getY() + BOLT_HEIGHT/2)
        c4 = (bolt.getX() - BOLT_WIDTH/2, bolt.getY() - BOLT_HEIGHT/2)
        return self.contains(c1) or self.contains(c2) or self.contains(c3)\
        or self.contains(c4)
