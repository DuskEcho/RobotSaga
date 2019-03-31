# Copyright SAGA 2019
# Not to be duplicated without express consent of
# original members. Not for release. 


import random
import gui
import time
import thread





        ####################
        #                  #
        #     CONSTANTS    #
        #                  #
        #    (MIGHT BE     #
        #     MOVED TO     #
        #  STARTUP CLASS)  #
        #                  #
        #                  #
        ####################


        # used for movement animations. Lowest stable is .12
moveAnimationSleep = .12  # any lower and coords get messed up


#bits is how many pixels are in each texture
bits = 32
#how many tiles there are wide
widthTiles = 40
#how many tiles there are tall
heightTiles = 22

shopKeeperX = 5*bits
shopKeeperY = 2*bits



#beings
beingList = []
#interactable objects
objectList = []

##class CoreGame():   experimented with a class to hold game data. could be addressed later
#    def __init__(self):
        #add select game folder (to allow more portable loading of assets to path)
try: 
           path #test to see if path exists
except NameError: #if path does not exist make new path
           printNow("Please select your game install folder")
           path = pickAFolder()
else: printNow("Welcome Back") #welcome the player back to the game






# Dictionaries for items
# Numbers correspond to stats
# arrays in form [attack/def, spritePaths]

weaponStatsList = {    
    "Stick": [1, [path + "stickUp.gif",
                  path + "stickDown.gif",
                  path + "stickLeft.gif",
                  path + "stickRight.gif"]],
   "Rock": [2, "spritePath"]
   }
helmStatsList = {
    "Hair": [0, "spritePath"],
    "Leaf": [1, "spritePath"]
    }
chestStatsList = {
    "BDaySuit": [0, "spritePath"],
    "Fur Coat": [1, "spritePath"]
    }
legsStatsList = {
    "Shame": [0, "spritePath"],
    "Fur Pants": [1, "spritePath"]
    }
feetStatsList = {
    "Toes": [0, "spritePath"],
    "Fur Boots": [1, "spritePath"]
    }
handStatsList = {
    "Digits": [0, "spritePath"],
    "Fur Gloves": [1, "spritePath"]
    }
itemsList = {}  #potions, etc.


lootTable = {}







        ####################
        #                  #
        #    FUNCTIONS     #
        #                  #
        ####################




# TEMPORARY TEXT DISPLAY UNTIL MENUS ARE IN PLACE
# Converts the given rawText to a Label object to be added to the 
# display, then adds at coordsX, coordsY. 



def showText(rawText, coordsX = backWidth * (2/5), coordsY = 0):
    label = gui.Label(rawText)
    display.add(rawText, coordsX, coordsY)






    
# TEMPORARY TEXT DISPLAY UNTIL MENUS ARE IN PLACE
# Adds the given gui.Label to the display at the Label's coords (default 0, 0)

def showLabel(label):
    display.add(label, backWidth*(2/5), 0)






# All actions that depend on the turn counter go here

def turnPass():
    for person in beingList:
        if person.hostile == true:
            simpleEnemyAI(person)
    if bot1.hp <= 0:
        bot1.coords.x = 0
        bot1.coords.y = 0
        bot1.sprite.spawnSprite(bot1.coords.x, bot1.coords.y)
    clearBadSprites()
    #total action counter to affect shop/store stock
    





def slideRight(object, targetXBig, sprite):
    time.sleep(.005)
    object.coords.x += 1 
    object.forwardCoords.x += 1
    display.remove(object.sprite)
    object.sprite = sprite
    display.add(object.sprite, object.coords.x, object.coords.y)
    if object.coords.x < targetXBig:
        thread.start_new_thread(slideRight, (object, targetXBig, sprite))







# Used to remove objects (labels, sprites, etc.) from the display after a delay.
# only call delayRemoveObject.  threadDelayRemoveObject() is not meant to be called
# directly.
# Parameters:
#   object          - An object on the displays self.items list
#   delay           - the amount of time in seconds to delay the removal

def delayRemoveObject(object, delay):
    thread.start_new_thread(threadDelayRemoveObject, (object, delay))
def threadDelayRemoveObject(object, delay):
    time.sleep(delay)
    display.remove(object)






# cleanup for duplicate sprites created when input is given
# too quickly

def clearBadSprites():
    goodSprites = []
    for being in beingList:
        goodSprites.append(being.sprite)
    for sprite in display.items:
        if sprite not in goodSprites and type(sprite) == BeingSprite:
            display.remove(sprite)







# used with thread.start_new_thread(threadRemoveSprite, (timeToWait, sprite))
# in order to despawn a sprite after a delay. For use with animations.
# parameters:
#   timeToWait      - time in seconds to delay the sprite removal
#   sprite          - sprite to be removed

def threadRemoveSprite(timeToWait, sprite):
    time.sleep(timeToWait)
    display.remove(sprite)






#helper Functions
def spotToCoord(spot):
    #if low set to 0d
    if spot < 0: spot = 0
    #if high set to max (should probably just throw error
    if spot > widthTiles * heightTiles: spot = widthTiles * heightTiles - 1
    return Coords(spot % widthTiles, spot / widthTiles)






def coordToSpot(coord):
    return coord.x + coord.y * widthTiles






def coordToSpot(coord):
    return coord.x + coord.y * widthTiles






def updateBackground(tiles):
    for spot in range(0, len(tiles)):
        if   tiles[spot] == "g": placeTex(grass, spot)
        elif tiles[spot] == "s": placeTex(stone, spot)
        #not in files yet
        #elif tiles[spot] == "m": placeTex(monster, spot)
        #elif tiles[spot] == "p": placeTex(player, spot)
        #elif tiles[spot] == "w": placeTex(wall, spot)
    writePictureTo(background, path + "newBack.png")






def placeTex(tex, spot):
    startx = (spot * bits) % backWidth;
    starty = ((spot * bits) / backWidth) * bits;
    for x in range(0, bits):
        for y in range(0, bits):
            setColor(getPixel(background, startx + x, starty + y), getColor(getPixel(tex, x, y)))






def getTexture(spot):
    texture = makeEmptyPicture(bits,bits)
    #spot to coord conversion
    startx = (spot * bits) % texWidth;
    starty = ((spot * bits) / texWidth) * bits;
    for x in range(0, bits):
        for y in range(0, bits):
            setColor(getPixel(texture, x, y), getColor(getPixel(textureMap, x + startx, y + starty)))
    return texture






# intro credits, adjust to add fade, etc.

def loadIntro():
    display.drawImage(path + "LogoOmega.png", 0, 0)
    time.sleep(1.5)
    display.drawImage(path + "dummyStartScreen.png", 0, 0)
    time.sleep(1.5)




# Basic enemy AI. Enemy moves in a random direction and attacks if 
# the player is directly in front.
# parameters:
#   enemy           - enemy to perform the actions

def simpleEnemyAI(enemy):
    if enemy.forwardCoords.x == bot1.coords.x and enemy.forwardCoords.y == bot1.coords.y:
        enemy.meleeAtk()
    else:
        moveRandom(enemy)





                              
# any function passed to onKeyType() must have one and exactly one
# parameter.  This parameter is how the function knows which key is pressed
# gotta find some way to "pause" in between moves to create the illusion of animation. 
# sleep() doesn't seem to work well

def keyAction(a):
  if a == "w":
    if bot1.isMoving == false:
        bot1.isMoving = true
        bot1.moveUp()
        turnPass()
  elif a == "s":
    if bot1.isMoving == false:
        bot1.isMoving = true
        bot1.moveDown()
        turnPass()
  elif a == "a":
    if bot1.isMoving == false:
        bot1.isMoving = true
        bot1.moveLeft()
        turnPass()
  elif a == "d":
    if bot1.isMoving == false:
        bot1.isMoving = true
        bot1.moveRight()
        turnPass()
  elif a == "f":
    if bot1.isMoving == false:
        bot1.meleeAtk()
        turnPass()
  elif a == "g":
    #steal(targetLocatedAt(self.forwardX, self.forwardY)
    if bot1.isMoving == false:
      #  bot1.steal()
        turnPass()
  elif a == "q":
    print("NotImplementedAtAll")
  elif a == "t":
    #openMenu
    print("not implemented")
  elif a == "v":
    bot1.talk()






    # To pass to getKeyTyped in order to block inputs 
    # (e.g., during animations or delays)

def blockKeys(a):
    None





          
# Currently only sets up the lootTable

def initialSetup():
    for item in weaponStatsList:
        lootTable[item] = weaponStatsList[item]
    for item in helmStatsList:
        lootTable[item] = helmStatsList[item]
    for item in chestStatsList:
        lootTable[item] = chestStatsList[item]
    for item in legsStatsList:
        lootTable[item] = legsStatsList[item]
    for item in feetStatsList:
        lootTable[item] = feetStatsList[item]





        
# Moves a being in a random direction
# Parameters:
#   Being           - being to be moved


def moveRandom(Being):
    randNum = random.randint(0, 3)
    if randNum == 0:
        Being.moveUp()
    elif randNum == 1:
        Being.moveDown()
    elif randNum == 2:
        Being.moveLeft()
    else:
        Being.moveRight()

                                    



        
def keyDownEvent():
    print("NotImplemented")
    #perform action (move, attack, etc.)
    #if menu/shop window is not open, call turnPass()







        ####################
        #                  #
        #      CLASSES     #
        #                  #
        ####################







# universal coordinates object 

class Coords():
  def __init__(self, x, y):
    self.x = x
    self.y = y












# general class for sprites. Use with display.add(spritename, sprite.coords.x, sprite.coords.y)
# to display on the main screen.
# parameters: 
#   filename    - filename in string format
#   x           - x coordinate
#   y           - y coordinate

class Sprite(gui.Icon):

  def __init__(self, filename, x, y):
      gui.JPanel.__init__(self)
      gui.Widget.__init__(self)
      filename = gui.fixWorkingDirForJEM( filename )   # does nothing if not in JEM- LEGACY, NOT SURE OF NECESSITY
      self.fileName = filename
      self.offset = (0,0)                # How much to compensate - LEGACY, NOT SURE OF NECESSITY
      self.position = (0,0)              # assume placement at a Display's origin- LEGACY, NOT SURE OF NECESSITY
      self.display = None
      self.degrees = 0                   # used for icon rotation - LEGACY, NOT SURE OF NECESSITY

      self.icon = gui.ImageIO.read(File(filename))
      iconWidth = self.icon.getWidth(None)
      iconHeight = self.icon.getHeight(None)

      # keep a deep copy of the image (useful for repeated scalings - we always scale from original
      # for higher quality)- LEGACY, NOT SURE OF NECESSITY
      self.originalIcon = gui.BufferedImage(self.icon.getWidth(), self.icon.getHeight(), self.icon.getType())
      self.originalIcon.setData( self.icon.getData() )
      self.coords = Coords(x, y)






      # adds the sprite to the display. If the sprite already exists,
      # moves the sprite to the self.coords location

  def spawnSprite(self):
        display.add(self, self.coords.x, self.coords.y)
 





      # removes the sprite from the display
        
  def removeSprite(self):
        display.remove(self)











                     
  # inherits from Sprite. Separated to give   See sprite for function exacts. 
  # ownership to sub-sprites (e.g., weapon)

class BeingSprite(Sprite):
  def __init__(self, filename, x, y):
      gui.JPanel.__init__(self)
      gui.Widget.__init__(self)
      filename = gui.fixWorkingDirForJEM( filename )   # does nothing if not in JEM - LEGACY, UNUSED FOR NOW
      self.fileName = filename
      self.offset = (0,0)                # How much to compensate - LEGACY, UNUSED FOR NOW
      self.position = (0,0)              # assume placement at a Display's origin - LEGACY, UNUSED FOR NOW
      self.display = None
      self.degrees = 0                   # used for icon rotation - LEGACY, UNUSED FOR NOW
      self.icon = gui.ImageIO.read(File(filename))
      iconWidth = self.icon.getWidth(None)
      iconHeight = self.icon.getHeight(None)

      # keep a deep copy of the image (useful for repeated scalings - we always scale from original
      # for higher quality) - LEGACY, UNUSED FOR NOW
      self.originalIcon = gui.BufferedImage(self.icon.getWidth(), self.icon.getHeight(), self.icon.getType())
      self.originalIcon.setData( self.icon.getData() )






      # adds the sprite to the display. If the sprite already exists,
      # moves the sprite to the self.coords location

  def spawnSprite(self, x, y):
        display.add(self, x, y)





        
      # removes the sprite

  def removeSprite(self):
        display.remove(self)





        
      # not a huge fan of the weaponOut flag, but it works for now.
      # without the check in putAwayWeap, JES complains  

  def displayWeapon(self, sprite, coords):
    display.add(sprite, coords.x, coords.y)





       
      # hides the weapon. may be unnecessary if we get
      # animations figured out

  def hideWeapon(self):
      display.remove(self.weap)





           
      #moves sprite to location given

  def moveTo(self, x, y):
    display.add(self, x, y)











          
    # Class for weapon objects. weapName must correspond to a weapon
    # in the weaponList. Contains stats and sprites.
    #
    #
    #
    #spritePaths should be array of order [up, down, left, right]


class Weapon():
    def __init__(self, weapName):
        self.name = weapName
        if self.name != None:
          self.sprites = weaponStatsList[self.name][1]
          self.sprite = Sprite(self.sprites[3], 0, 0)
          self.power = weaponStatsList[self.name][0]
        self.displayed = false
    





        # Displays the weapon's "up/down/left/right" sprite at the coords.
        # For use with being's "self.forwardCoords.x/y" 
        
    def displayUp(self, x, y):
        if self.displayed == false:
            self.sprite = Sprite(self.sprites[0], 0, 0)
            display.add(self.sprite, x, y)
            self.displayed = true
    def displayDown(self, x, y):
        if self.displayed == false:
            self.sprite = Sprite(self.sprites[1], 0, 0)
            display.add(self.sprite, x, y)
            self.displayed = true
    def displayLeft(self, x, y):
        if self.displayed == false:
            self.sprite = Sprite(self.sprites[2], 0, 0)
            display.add(self.sprite, x, y)
            self.displayed = true
    def displayRight(self, x, y):
        if self.displayed == false:
            self.sprite = Sprite(self.sprites[3], 0, 0)
            display.add(self.sprite, x, y)
            self.displayed = true






        # removes the weapon from the display

    def hide(self):
        display.remove(self.sprite)
        self.displayed = false










        

    # Class for living entities (people, enemies, bosses, etc.)
    # handles stats, movement, experience, inventory
    # spritePaths should be an array of order [up, down, leftFace, rightFace, leftMove, rightMove]
    # All beings are added to the beingList[]
    # Parameters:
    #   name:           - Being's name as a string
    #   weapName:       - Being's starting weapon as a string - must correlate with weaponList
    #   spritePaths:    - list containing the filePaths of the Being's sprites
    #   xSpawn:         - initial x location
    #   ySpawn:         - initial y location

class Being():
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn):
        self.name = name
        self.level = 0
        self.hp = 10
        self.maxHp = 10
        self.xp = 0
        self.atk = 5
        self.df = 5
        self.lootValue = self.maxHp + self.atk + self.df
        self.xpValue = self.lootValue/2
        self.hostile = false
        self.inv = []
        self.coords = Coords(xSpawn, ySpawn)
        self.forwardCoords = Coords(self.coords.x + bits, self.coords.y)
        self.spritePaths = spritePaths
        self.sprite = BeingSprite(self.spritePaths[1], xSpawn, ySpawn)
        self.weapon = Weapon(weapName)
        self.facing = "right"
        self.isMoving = false
        self.talkingLines = ["Hello!",
                             "Yes?",
                             "Can I Help you?"]
        beingList.append(self)






        # returns the Being's level

    def getLevel(self):
        return self.level






        # level-up logic. Semi-randomly increases max HP, Atk, df
        
    def levelUp(self):
        self.xp = 0
        self.level += 1
        self.changeMaxHP(random.randint(0, 8))
        self.changeAtk(random.randint(0, 4))
        self.changeDf(random.randint(0, 4))


    



        # returns the Being's name

    def getName(self):
        return self.name
    




        
        # returns the Being's current hp

    def getCurrentHP(self):
        return int(self.hp)





        
        # returns the Being's max hp

    def getMaxHP(self):
        return int(self.maxHp)
    




        
        # returns the Being's current xp

    def getXp(self):
        return int(self.xp)
    




           
        # returns the Being's ATK

    def getAtk(self):
        return int(self.atk)
    




           
        # returns the Being's DF

    def getDf(self):
        return int(self.df)





             
        # increases xp by the amount given.
        # negative amounts will reduce xp
        # contains built in "barrier" formula
        # for levelling up

    def changeXp(self, amount):
        for i in range(1, amount):
            self.xp +=1
            if self.xp>=(self.level**1.2)*1.5:
                self.levelUp()
    

                               


                
        # changes ATK by the amount given

    def changeAtk(self, amount):
        self.atk += amount
    

               


        
        # changes DF by the amount given


    def changeDf(self, amount):
        self.df += amount


               


        
        # changes max HP by the amount given

    def changeMaxHP(self, amount):
        self.maxHp += amount


               



        # changes current HP by amount given.
        # negative values reduce.
        # if hp falls below 0, calls dead()
        
    def changeHp(self, amount):
        self.hp = int(self.hp + amount)
        if self.hp > self.maxHp:
            self.hp = self.maxHp
        elif self.hp < 0:
            self.dead()

            




        #undeveloped, for use in handling hp == 0

    def dead(self):
        print("NotImplemented")







        # For use with actions that can target more than one target (e.g., attacks)

    def getFrontTargetList(self):
        bigList = beingList + objectList
        targetList = []
        for target in bigList:
            if target.coords.x == self.forwardCoords.x and target.coords.y == self.forwardCoords.y:
                targetList.append(target)
        return targetList
        






        #for use with actions that can only target one target (e.g., talking)

    def getFrontTarget(self):
        bigList = beingList + objectList
        for target in bigList:
            if target.coords.x == self.forwardCoords.x and target.coords.y == self.forwardCoords.y:
                return target

            


            
        #needs to be reworked for better decomp
        #
        # activates the melee attack action.
        # displays the weapon at the being's forward coord
        # and activates a damage calculation if any being is there
        # Friendly fire is enabled. Attacking a friendly turns them hostile
        # if the target is killed, exp is calculated.  If the player is killed,
        # the player loses all levels/items and respawns as a new instance of the
        # User class.

    def meleeAtk(self):
        self.displayWeapon()
        x = 1
        thread.start_new_thread(threadRemoveSprite, (.2, self.weapon.sprite))
        self.weapon.displayed = false
        for target in self.getFrontTargetList():
            if target != bot1:
                target.hostile = true
            damage = self.atk
            if damage <= 0:
                damage = 1
            target.hp -= damage
            self.displayDamage(target.coords.x, target.coords.y)
            if target.hp <= 0:
                self.changeXp(target.xpValue)
                target.sprite.removeSprite()
                if target is not bot1:
                    beingList.remove(target)
                    del target
                else:                        
                    target.__init__("bot1", "Stick", userSpritePaths, 32, 32)
                    
            



                    
        # Display's the "damage splash" sprite at
        # the given location. Uses multithreading.

    def displayDamage(self, x, y):
        damage = Sprite(path + "damage.gif", x, y)
        display.add(damage, x, y)
        thread.start_new_thread(threadRemoveSprite, (.25, damage))

        




        # For use with meleeAtk and thread.start_new_thread().
        # may be removed and have functionality replaced by 
        # more general function

    def threadHideWeapon(self, x):
            time.sleep(.2)
            self.weapon.hide()






        # displays the being's weapon at the being's forward coords
        # note that the weapon sprite is not despawned

    def displayWeapon(self):
        if self.facing == "up":
            self.weapon.displayUp(self.forwardCoords.x, self.forwardCoords.y)
        elif self.facing == "down":
            self.weapon.displayDown(self.forwardCoords.x, self.forwardCoords.y)
        elif self.facing == "left":
            self.weapon.displayLeft(self.forwardCoords.x, self.forwardCoords.y)
        else:  #right
            self.weapon.displayRight(self.forwardCoords.x, self.forwardCoords.y)


    


                    # MOVEMENT CLUSTER                                                    
        # Moves the being up/down/left/right one unit in two steps.
        # the first step is instant/halfstep, the second
        # is through a delayed call to thread moveDirection
        # in order to give the illusion of animation.
        # faceDirection is called first 
        # threadMoveDirection is not meant to be called directly.
        #
        # may be streamlined by using a single moveForward function
        # that interacts with direction facing

    

 
    def moveUp(self):
        if self.coords.y >= 0:
            self.faceUp()
            self.coords.y -= bits/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[0], self.coords.x, self.coords.y)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveUp, (x,))
            if self.facing == "up": 
              self.forwardCoords.y = self.coords.y - bits - bits/2
              self.forwardCoords.x = self.coords.x
        else:
            self.isMoving = false
                           
    def threadMoveUp(self, x):
        time.sleep(.15)
        self.coords.y -= bits/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[0], self.coords.x, self.coords.y)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.isMoving = false
        

    def moveDown(self):
        if self.coords.y < backHeight:
            self.faceDown()
            self.coords.y += bits/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[1], self.coords.x, self.coords.y)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveDown, (x,))
            self.sprite.moveTo(self.coords.x, self.coords.y)
            if self.facing == "down":
              self.forwardCoords.y = self.coords.y + bits + bits/2
              self.forwardCoords.x = self.coords.x
        else:
            self.isMoving = false
                   
    def threadMoveDown(self, x):
        time.sleep(.15)
        self.coords.y += bits/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[1], self.coords.x, self.coords.y)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.isMoving = false


    def moveLeft(self):
        if self.coords.x >= 0:
            self.faceLeft()
            self.coords.x -= bits/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[4], self.coords.x, self.coords.y)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveLeft, (x,))
            if self.facing == "left":
              self.forwardCoords.y = self.coords.y
              self.forwardCoords.x = self.coords.x - bits - bits/2 
        else:
            self.isMoving = false

    def threadMoveLeft(self, x):
        time.sleep(.15)
        self.coords.x -= bits/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[2], self.coords.x, self.coords.y)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.isMoving = false

    def moveRight(self):
        if self.coords.x < backWidth:
            self.faceRight()
            self.coords.x += bits/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[5], self.coords.x, self.coords.y)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveRight, (x,))
            if self.facing == "right":
              self.forwardCoords.y = self.coords.y
              self.forwardCoords.x = self.coords.x + bits+ bits/2
        else:
            self.isMoving = false


    def threadMoveRight(self, x):
        time.sleep(.1)
        self.coords.x += bits/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[3], self.coords.x, self.coords.y)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.isMoving = false


        # changes the being's sprite to one facing the corresponding
        # direction. If a weapon is displayed, it is first hidden.
        # adjusts forwardCoords accordingly

    def faceUp(self):
        #playAnimation
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != "up":
          self.facing = "up"
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[0], self.coords.x, self.coords.y)
          self.sprite.spawnSprite(self.coords.x, self.coords.y)
          self.forwardCoords.y = self.coords.y - bits
          self.forwardCoords.x = self.coords.x
                           
    def faceDown(self):
        #playAnimation
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != "down":
          self.facing = "down"
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[1], self.coords.x, self.coords.y)
          self.sprite.spawnSprite(self.coords.x, self.coords.y)
          self.forwardCoords.y = self.coords.y + bits
          self.forwardCoords.x = self.coords.x
                   
    def faceLeft(self):
        #playAnimation
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != "left":
          self.facing = "left"
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[2], self.coords.x, self.coords.y)
          self.sprite.spawnSprite(self.coords.x, self.coords.y)
          self.forwardCoords.x = self.coords.x - bits
          self.forwardCoords.y = self.coords.y
                   
    def faceRight(self):
        #playAnimation
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != "right":
          self.facing = "right"
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[3], self.coords.x, self.coords.y)
          self.sprite.spawnSprite(self.coords.x, self.coords.y)
          self.forwardCoords.x = self.coords.x + bits
          self.forwardCoords.y = self.coords.y












    # Class for living entities (people, enemies, bosses, etc.)
    # handles stats, movement, experience, inventory
    # spritePaths should be an array of order [up, down, leftFace, rightFace, leftMove, rightMove]
    # All beings are added to the beingList[]
    # Parameters:
    #   name:           - Being's name as a string
    #   weapName:       - Being's starting weapon as a string - must correlate with weaponList
    #   spritePaths:    - list containing the filePaths of the Being's sprites
    #   xSpawn:         - initial x location
    #   ySpawn:         - initial y location
    #   species:        - Being's species as a string
    #   level:          - Being's starting level

class Enemy(Being):
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn, species, level):
        Being.__init__(self, name, weapName, spritePaths, xSpawn, ySpawn)
        self.species = species 
        for val in range(0, level):
            self.levelUp()
        self.hostile = true





        
        # in progress loot-dropping function

    def dropLoot(self):
        #animateDeath()
        loot = self.randomInvItem()
        #drop loot at gridLocation self.coords.x, self.coords.y






        # in progress hp == 0 action

    def dead(self):
        #play animation
        #delete coordinate data from grid
        dropLoot();
        




               
        # returns a random inventory item the being has

    def randomInvItem(self):
        possibilities = len(self.inv)
        if possibilities>0:
            itemIndex = random.randint(0, possibilities-1)
            return self.inv[itemIndex]
            



        






        
        # Class for armor/equipment, in development

class Armor():
    def __init__(self, name):
        self.armorType = "FIX THIS CLASS"











                     
    # Class for living entities (people, enemies, bosses, etc.)
    # handles stats, movement, experience, inventory
    # spritePaths should be an array of order [up, down, leftFace, rightFace, leftMove, rightMove]
    # All beings are added to the beingList[]
    # Parameters:
    #   name:           - Being's name as a string
    #   weapName:       - Being's starting weapon as a string - must correlate with weaponList
    #   spritePaths:    - list containing the filePaths of the Being's sprites
    #   xSpawn:         - initial x location
    #   ySpawn:         - initial y location
    #   species:        - Being's species as a string
    #   level:          - Being's starting level

class User(Being):
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn):
        Being.__init__(self, name, weapName, spritePaths, xSpawn, ySpawn)
        self.name = name
        self.helm = "Hair"
        self.chest = "BDaySuit"
        self.legs = "Shame"
        self.boots = "Toes"
        self.gloves = "Digits"
        self.wallet = 0
        self.sprite.spawnSprite(self.coords.x, self.coords.y)






        # Updates wallet by amount

    def changeWallet(amount):
        wallet += amount
        if wallet <= 0:
            wallet == 0
            




            
        # Adds item to inventory list

    def inventoryAdd(self, item):
        inv.append(item)





               # EQUIPMENT CLUSTER
        # The following 6 functions handle equipping items
        # to  specific parts of the body.  Atk and Df stats
        # are adjusted accordingly.  The equipped item must
        # correlate to one of the itemLists

    def setWeapon(self, weapon):
        if self.weapon != "Stick":
            inventoryAdd(self.weapon)
        self.atk -= weaponStatsList[self.weapon]
        self.weapon = weapon
        self.atk += weaponStatsList[self.weapon]
               

    def setHelm(self, helm):
        if self.helm != "Hair":
            inventoryAdd(self.helm)
        self.df -= helmStatsList(self.helm)
        self.helm = helm
        self.df += helmStatsList(self.helm)


    def setChest(self, chest):
        if self.chest != "BDaySuit":
            inventoryAdd(self.chest)
        self.df -= chestStatsList(self.chest)
        self.chest = chest
        self.df += chestStatsList(self.chest)
               

    def setLegs(self, legs):
        if self.legs != "Shame":
            inventoryAdd(self.legs)
        self.df -= legsStatsList(self.legs)
        self.legs = legs
        self.df += legsStatsList(self.legs)
                 
        
    def setBoots(self, boots):
        if self.boots != "Toes":
            inventoryAdd(self.boots)
        self.df -= bootsStatsList(self.boots)
        self.boots = boots
        self.df += bootsStatsList(self.boots)
        

    def setGloves(self, gloves):
        if self.gloves != "Digits":
            inventoryAdd(self.gloves)
        self.df -= glovesStatsList(self.gloves)
        self.gloves = gloves
        self.df += glovesStatsList(self.gloves)
    




                     
        # equips a given item by calling one of the 
        # equipment "set" functions
        # item should be passed as it's key as it appears
        # in the item lists

    def equip(self, item):
        if indexName == weaponStatsList:
            if item in weaponStatsList:
                self.setWeapon(item)
        elif indexName == helmStatsList:
            if item in helmStatsList:
                self.setHelm(item)
        elif indexName == legsStatsList:
            if item in legsStatsList:
                self.setLegs(item)
        elif indexName == chestStatsList:
            if item in chestStatsList:
                self.setChest(item)
        elif indexName == glovesStatsList:
            if item in glovesStatsList:
                self.setGloves(item)
        elif indexName == bootsStatsList:
            if item in bootsStatsList:
                self.setBoots(item)
         





            # action - attempts to steal an item from a target
            # Being.  If the attempt fails, the Being turns hostile

    def steal(self, target):
        possibilities = len(target.inv)
        if possibilities>0:
            if random.randint(0, 10)%10 == 0:
                item = target.randomInvItem()
                target.inv.remove(item)
                self.inv.append(item)
            else:
                target.hostile = true

    def talk(self):
        target = self.getFrontTarget()
        speech = gui.Label(target.talkingLines[random.randint(0, len(target.talkingLines)-1)])
        showLabel(speech)
        delayRemoveObject(speech, 2)





            ######################
            #                    #
            #    PSEUDO-MAIN     #
            #                    #
            ######################







textureMap = makePicture(path + "texture.png")

#get width and height
texWidth = getWidth(textureMap)
texHeight = getHeight(textureMap)
#initailize textures
stone = getTexture(1)

grass = getTexture(2)

#create emply grass field will clean up later
home  = "gsgsgsgsgsgsgsgsgsgsgsgsgggggggggggggggg"
home += "sgsgsgsgsgsgsgsgsgsgsggggggggggggggggggg"
home += "gsgsgsgsgsgsgsgsgsgsgsgggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
#initailize background image
backWidth = bits * widthTiles
backHeight = bits * heightTiles
background = makeEmptyPicture(backWidth, backHeight) #704 is chosen because its divisible by 32
updateBackground(home)


display = gui.Display("Robot Saga", backWidth, backHeight)
#loadIntro()
text = gui.TextField("", 1)
text.onKeyType(keyAction)
display.add(text)
#create background (probably prerender home background later)
userSpritePaths = [path + "botBlueBack.gif",
               path + "botBlueFront.gif",
               path + "botBlueSideLeft.gif",
               path + "botBlueSideRight.gif",
               path + "botBlueMovingLeft.gif",
               path + "botBlueMovingRight.gif",]
blueEnemySpritePaths = [path + "blueRobotBack.gif",
               path + "blueRobotFront.gif",
               path + "BlueRobotSideLeft.gif",
               path + "BlueRobotSideRight.gif",
               path + "BlueRobotMovingLeft.gif",
               path + "BlueRobotMovingRight.gif",]
shopKeeperSpritePaths = [path + "ShopkeeperbotCloseup.gif",
                         path + "ShopkeeperbotFront.gif"]

display.drawImage(path + "newBack.png", 0, 0)
bot1 = User("bot1", "Stick", userSpritePaths, 32, 32)
bot2 = Enemy("Enemy", "Stick", blueEnemySpritePaths, random.randint(0, 10)*32, random.randint(0, 10)*32, "orc", 1)
bot3 = Enemy("Enemy", "Stick", blueEnemySpritePaths, random.randint(0, 10)*32, random.randint(0, 10)*32, "orc", 1)
bot4 = Enemy("Enemy", "Stick", blueEnemySpritePaths, random.randint(0, 10)*32, random.randint(0, 10)*32, "orc", 1)
shopKeeper = Being("shopKeep", None, shopKeeperSpritePaths, shopKeeperX, shopKeeperY)
bot2.sprite.spawnSprite(bot2.coords.x, bot2.coords.y)
bot3.sprite.spawnSprite(bot3.coords.x, bot3.coords.y)
bot4.sprite.spawnSprite(bot4.coords.x, bot4.coords.y)
shopKeeper.sprite.spawnSprite(shopKeeper.coords.x, shopKeeper.coords.y)







