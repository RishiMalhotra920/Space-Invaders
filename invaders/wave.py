"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Rishi Malhotra (rm725)
# December 8, 2019
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    # Attribute _alienDir: the direction the alien
    # Invariant: _alienDir is either 'right', 'left', 'right-down',
    # 'left-down'. 'right-down' means ship moving right and will move down.
    # 'left-down' means ship moving left and will move down
    #
    # Attribute: _alienFireRate: The rate at which the aliens fire
    # Invariant: integer and 0<=self._alienFireRate<=BOLT_RATE
    #
    # Attribute: _walks: The number of walks the alien makes before it fires
    # Invariant: walks is an integer 0<=self._walks<=self._alienFireRate
    #
    # Attribute _gameOverStatus: The status if the game is over
    # Invariant: Is either 'win', 'lose' or None if game continues
    #
    # Attribute: _barriers: The list of barriers behind which the ship can hide
    # Invariant: Is a list whose elements are instances of class models.Barrier
    #
    # Attribute _shipCollides: Whether a ship has collided
    # Invariant: Is a boolean True or False. True indicates ship collided with
    # bolt. False indicates did not collide with bolt in that frame.

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLives(self):
        """
        Returns the lives of the ships
        """
        return self._lives

    def getGameOverStatus(self):
        """
        Returns the status if the game is over
        """
        return self._gameOverStatus

    def getShipCollides(self):
        """
        Returns the attribute _shipCollides
        """
        return self._shipCollides

    def setGameOverStatus(self,s):
        """
        Sets the game over status to 'win','lose' or none

        Parameter: s is the new game over status
        Precondition: s is in in ['win','lose',None]
        """
        assert s in ['win','lose',None]
        self._gameOverStatus = s

    def setShipCollides(self,b):
        """
        Sets the attribute _shipCollides to b

        Parameter b: The boolean to set _shipCollides to
        Precondition: b is a boolean
        """
        assert type(b) == bool
        self._shipCollides = b



    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes variables essential to the game.

        Initializes the aliens, ships and the defense line, _time,
        _alienDirection. Initializes _alienFireRate to a random integer
        between 1 and BOLT_RATE. Sets _bolts to an empty array. Sets
        _shipCollides to False
        """
        self._lives = SHIP_LIVES
        self._time = 0
        self._alienDir = 'right'
        self._setAliens()
        self._setShip()
        self._setDefenseLine()
        self._setBarrier()
        self._alienFireRate = random.randint(1,BOLT_RATE)
        self._walks = 0
        self._bolts = []
        self._shipCollides = False

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,uInput,dt,alienSpeed):
        """
        This method updates the wave.

        The method updates the ship's location, alien's location. It randomly
        fires alien bolts, fires player bolts when the up arrow key is pressed.
        It removes alien bolts, and updates the location of all alien bolts. It
        also updates the attribute _gameOverStatus if the game is over. It does
        this through calling other methods in this module.

        Paramter uInput: The user's input
        Precondition: uInput is an instance of GInput

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter alienSpeed: The speed of aliens adjusted for waves
        Precondition: alienSpeed is int or float
        """
        assert isinstance(uInput,GInput)
        assert type(dt) in [int,float]
        assert type(alienSpeed) in [int,float]
        if self._ship is not None:
            self._updateShip(uInput)
        if not self._aliensDead():
            self._moveAliens(dt,alienSpeed)
            if self._walks == self._alienFireRate:
                self._createAlienBolts()
                self._walks = 0
        if uInput.is_key_down('up'):
            self._createPlayerBolt()
        self._removeBolts()
        self._updateBolts()
        aliensDead = True
        self.setGameOverStatus(None)
        for bolt in self._bolts:
            self.collisionWithBarrier(bolt)
            self.collisionWithAliens(bolt)
            self.collisionWithShip(bolt)
        for row in self._aliens:
            for alien in row:
                if alien is not None and\
                 alien.getY() - ALIEN_HEIGHT/2 < DEFENSE_LINE:
                    self.setGameOverStatus('lose')
        if self._aliensDead():
            self.setGameOverStatus('win')

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the ship, aliens, defensive line and bolts to the screen.

        Draws the ship if the ship is not None (if not destroyed).Draws
        the alien if alien is not destroyed. Draws the barriers too.

        Parameter view: the game view, used in drawing
        Precondition: view is an instance of GView
        """
        assert isinstance(view,GView)
        for aliens_row in self._aliens:
            for alien in aliens_row:
                if alien is not None:
                    alien.draw(view)

        if self._ship is not None:
            self._ship.draw(view)

        self._dline.draw(view)

        for bolt in self._bolts:
            bolt.draw(view)

        for barrier in self._barriers:
            if not barrier.barrierDestroyed():
                barrier.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def collisionWithBarrier(self,bolt):
        """
        Carries out tasks if collision between bolt and barrier.

        If the barrier is hit by the bolt, then reduce the life of the
        barrier by BARRIER_HEALTH_DECREMENT. If the barrier is destroyed,
        then remove it from the self._barriers

        Parameter bolt: The bolt to check collision with
        Precondition: bolt is an instance of class Bolt
        """
        assert isinstance(bolt,Bolt)
        if bolt in self._bolts:
            for barrier in self._barriers:
                if barrier.collides(bolt):
                    barrier.reduceHealth(BARRIER_HEALTH_DECREMENT)
                    self._bolts.remove(bolt)
                if barrier.barrierDestroyed():
                    self._barriers.remove(barrier)

    def collisionWithShip(self,bolt):
        """
        Carries out tasks if collision between bolt and ship.

        If alien bolt hits ship, then ship lives reduced by 1, bolt removed
        and attribute _shipCollides set to True.

        Parameter bolt: The bolt to check collision with
        Precondition: bolt is an instance of class Bolt
        """
        assert isinstance(bolt,Bolt)
        if bolt in self._bolts:
            if self._ship is not None and self._ship.collides(bolt):
                self._lives -= 1
                self._bolts.remove(bolt)
                self._shipCollides = True

    def collisionWithAliens(self,bolt):
        """
        Carries out tasks if collision between bolt and aliens.

        If ship bolt hits alien, then that alien set to None and bolt
        removed.

        Parameter bolt: The bolt to check collision with
        Precondition: bolt is an instance of class Bolt
        """
        assert isinstance(bolt,Bolt)
        if bolt in self._bolts:
            for row_i in range(ALIEN_ROWS):
                for col_i in range(ALIENS_IN_ROW):
                    if self._aliens[row_i][col_i] is not None and\
                    self._aliens[row_i][col_i].collides(bolt):
                        self._aliens[row_i][col_i] = None
                        self._bolts.remove(bolt)

    #OTHER HELPER METHODS
    def _updateShip(self,uInput):
        """
        Updates the x-coordinate of the ship.

        Gets the ship's x coordinate. Checks if the ship is allowed to move
        further right or left. If allowed, then changes the ship's x coord
        by SHIP_MOVEMENT.

        Paramter uInput: The user's input
        Precondition: uInput is an instance of GInput
        """
        assert isinstance(uInput,GInput)
        currentX = self._ship.getX()
        shipLeft = currentX - 0.5 * SHIP_WIDTH
        shipRight = currentX + 0.5 * SHIP_WIDTH

        if uInput.is_key_down('left') and shipLeft - SHIP_MOVEMENT >= 0:
            self._ship.setX(currentX-SHIP_MOVEMENT)

        if uInput.is_key_down('right') and\
         shipRight + SHIP_MOVEMENT <= GAME_WIDTH:
            self._ship.setX(currentX+SHIP_MOVEMENT)

    def _moveAliens(self,dt,alienSpeed):
        """
        Updates the x and y of the aliens

        If the alien is not None, then it checks the direction in which
        alien is moving. If it is moving right, hten adds ALIEN_H_WALK from x.
        .If left then subtracts ALIEN_H_WALK from x. If 'right-down' or
        'left-down', then subtracts ALIEN_V_WALK from the Y. Does this only
        if the time since the last walk is greater than the time alienSpeed.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter alienSpeed: The speed at which aliens move
        Precondition: alienSpeed is an int or float
        """
        assert type(dt) in [int,float]
        assert type(alienSpeed) in [int,float]
        self._time += dt

        if self._time > alienSpeed: #if time to walk, then walk
            self._walks += 1
            for row in self._aliens:
                for alien in row:
                    if alien is not None:
                        alienX = alien.getX()
                        alienY = alien.getY()
                        if self._alienDir == 'right':
                            alien.setX(alienX + ALIEN_H_WALK)
                        elif self._alienDir == 'left':
                            alien.setX(alienX - ALIEN_H_WALK)
                        elif self._alienDir == 'right-down':
                            alien.setY(alienY - ALIEN_V_WALK)
                        elif self._alienDir == 'left-down':
                            alien.setY(alienY - ALIEN_V_WALK)
            self._switchAlienDir() #Switch the alien direction

    def _switchAlienDir(self):
        """
        Switches the directions in which aliens are moving

        This method first determines the rightmost and the leftmost aliens.
        If the rightmost alien is past ALIEN_H_WALK from the edge of the
        screen, it changes the direction of the alien.
        If the leftmost alien is within the ALIEN_H_WALK
        from the left edge of the screen, it changes the
        direction. Alien dir can mean right/left - the alien is moving
        right or left. If it is 'right-down', it is moving right and about
        to move down on the next walk. 'left-down' means that it is moving
        left and about to move down on the next walk.
        """
        leftcol = -1; leftrow = -1 #col and row corresponding to the left alien
        rghtcol = -1; rghtrow = -1 #col and row corresponding to the right alien
        leftAlienSet = False
        for col_i in range(ALIENS_IN_ROW):
            for row_i in range(ALIEN_ROWS):
                if self._aliens[row_i][col_i] is not None:
                    rghtrow = row_i
                    rghtcol = col_i
                    if not leftAlienSet:
                        leftrow = row_i
                        leftcol = col_i
                        leftAlienSet = True
        rghtAlienX = self._aliens[rghtrow][rghtcol].getX()
        leftAlienX = self._aliens[leftrow][leftcol].getX()
        if self._alienDir == 'right-down':
            self._alienDir = 'left'
        elif self._alienDir == 'left-down':
            self._alienDir = 'right'
        elif(rghtAlienX+ALIEN_WIDTH/2)+ALIEN_H_WALK>(GAME_WIDTH-ALIEN_H_SEP):
            self._alienDir += '-down'
        elif (leftAlienX - ALIEN_WIDTH/2) - ALIEN_H_WALK < ALIEN_H_SEP:
            self._alienDir += '-down'
        self._time = 0

    def _createPlayerBolt(self):
        """
        Creates a ship bolt and adds it to self._bolts.

        Sets the ship's bolt x to the ship's x. Sets the ship bolt's y to
        ship y + 0.5 * ship height + 0.5 * bolt height. Creates bolts only if
        there is no player bolt present on the screen.
        """
        playerBoltPresent = False
        for bolt in self._bolts:
            if bolt.isPlayerBolt():
                playerBoltPresent = True
        if not playerBoltPresent:#if no player bolt is present, then create bolt
            boltX = self._ship.getX()
            boltY = self._ship.getY() + SHIP_HEIGHT/2 + BOLT_HEIGHT/2
            bolt = Bolt(x=boltX,y=boltY,width=BOLT_WIDTH,height=BOLT_HEIGHT,\
            fillcolor='red',linecolor='red',velocity=BOLT_SPEED)
            self._bolts.append(bolt)

    def _createAlienBolts(self):
        """
        Creates alien bolts and adds it to self._bolts

        First finds the columns which have aliens so that columns without
        aliens don't fire.
        Sets the alien bolt x to the alien's x coordinate. Set's the bolt y
        coordinate to alien's y - 0.5 * alien height - 0.5 * bolt height.
        Resets the fire rate to a random number between 1 and BOLT_RATE so that
        the bolt rate is random.
        """
        #finds a random column of aliens where not aliens are not none
        availableCols = []
        for col_i in range(ALIENS_IN_ROW):
            for row_i in range(ALIEN_ROWS):
                alien = self._aliens[row_i][col_i]
                if alien is not None and col_i not in availableCols:
                    availableCols.append(col_i)

        alienCol = random.choice(availableCols)
        #finds the bottommost alien in that column
        alienRow = 0
        for row in range(ALIEN_ROWS):
            if self._aliens[row][alienCol] is not None:
                alienRow = row

        alien = self._aliens[alienRow][alienCol]
        boltX = alien.getX()
        boltY = alien.getY() - ALIEN_HEIGHT/2 - BOLT_HEIGHT/2
        bolt = Bolt(x=boltX,y=boltY,width=BOLT_WIDTH,height=BOLT_HEIGHT,\
        fillcolor='red',linecolor='red',velocity=-BOLT_SPEED)
        self._bolts.append(bolt)
        self._alienFireRate = random.randint(1,BOLT_RATE)

    def _updateBolts(self):
        """
        Updates the y locations of the bolts

        Iterates through the bolts array and changes the y coordinate of each
        bolt. If the bolt is player bolt, adds bolt_speed, else subtracts
        bolt_speed
        """
        for bolt in self._bolts:
            y = bolt.getY()
            if bolt.isPlayerBolt():
                bolt.setY(y+BOLT_SPEED)
            else:
                bolt.setY(y-BOLT_SPEED)

    def _removeBolts(self):
        """
        Removes the bolts from self._bolts if the bolt goes past the top of
        screen

        Checks for each bolt's bottom edge and checks if it is greater than
        GAME_HEIGHT. If true, then removes the bolt from the self._bolts.
        """
        for bolt in self._bolts:
            if (bolt.getY() - BOLT_HEIGHT/2) > GAME_HEIGHT:
                self._bolts.remove(bolt)
            if (bolt.getY() + BOLT_HEIGHT/2) < 0:
                self._bolts.remove(bolt)

    def _aliensDead(self):
        """
        Returns boolean whether all aliens are dead

        Loops through each row in aliens. Loops through each alien in the
        row. If all aliens are none, then returns True, otherwise returns False.
        """
        aliensDead = True
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    return False
        return True

    def _setAliens(self):
        """
        Sets the _aliens attribute to a 2d array of aliens.

        The 2d array contains arrays which contains alien objects. These alien
        objects differ in their x,y and image
        """
        self._aliens = []
        for row in range(ALIEN_ROWS):
            #Setting the image corresponding to the alien
            pos = int((ALIEN_ROWS-row-1)/2)%len(ALIEN_IMAGES)

            #setting alien y coordinate
            alien_y = (GAME_HEIGHT-ALIEN_CEILING) - (0.5*ALIEN_HEIGHT)\
            -row*(ALIEN_V_SEP+ALIEN_HEIGHT)

            aliens_row = []
            for col in range(ALIENS_IN_ROW):
                #setting alien x coordinate
                alien_x = ALIEN_H_SEP + 0.5*ALIEN_WIDTH+\
                 col * (ALIEN_WIDTH + ALIEN_H_SEP)

                alien = Alien(x=alien_x,y=alien_y,width=ALIEN_WIDTH,\
                height=ALIEN_HEIGHT,source=ALIEN_IMAGES[pos])
                aliens_row.append(alien)

            self._aliens.append(aliens_row)

    def _setShip(self):
        """
        Creates a Ship Object and sets the _ship attribute to it
        """
        ship_x = GAME_WIDTH/2
        ship_y = SHIP_BOTTOM + SHIP_HEIGHT/2

        self._ship = Ship(x=ship_x,y=ship_y,width=SHIP_WIDTH,\
        height=SHIP_HEIGHT,source='ship.png')

    def _setDefenseLine(self):
        """
        Creates a defense line and sets it to the attribute _dline
        """
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE]\
        ,linewidth=2,linecolor='black')

    def _setBarrier(self):
        """
        Creates 2 barriers and stores them in a list the attribute _barriers
        """
        b1 = Barrier(x=GAME_WIDTH/3,y=BARRIER_Y,width=BARRIER_WIDTH,\
        height=BARRIER_HEIGHT,linecolor='blue',fillcolor='blue')
        b2 = Barrier(x=2*GAME_WIDTH/3,y=BARRIER_Y,width=BARRIER_WIDTH,\
        height=BARRIER_HEIGHT,linecolor='blue',fillcolor='blue')
        self._barriers = [b1,b2]
