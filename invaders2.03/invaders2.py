import pgzrun
import math
import re
import time
import pickle
import random
from random import randint  
player = Actor("life", (400, 550))
boss = Actor("boss2")
item = Actor('alien')
itemdbuff =Actor('alienpng')
logo = Actor('logo',(400,100))
logo2 = Actor('logo2',(400,350))
power_up = 0
power_up2 = 0
bigboss = Actor("boss")
bigbossspawn = False #ตัวแปลต่างที่เอาไว้ใช้ในฟั่งชั่น
bigbossgo = 0
hpbigboss = 5000
num = 0
P = 0
count = 0
count1 = 0
goitem = False
goitem2 = False
gameStatus = 0
highScore = []
a = 0
R = False
F = False
Q = False
timeup = False
def draw():  # Pygame Zero draw function
    global a,goitem,goitem2,item2,count1,bigboss,bigbossspawn
    screen.blit('background', (0, 0))
    if gameStatus == 0:  # display the title page
        logo.draw()
        logo2.draw()
        screen.draw.text(player.name, center=(400, 500), owidth=0.5, ocolor=(
            255, 0, 0), color=(0, 64, 255), fontsize=60)
    if gameStatus == 1:  # playing the games
        playerchange()
        player.draw()
        count1 = randint(1,2)
        if boss.active:
            if count1 == 1:
                boss.image = 'boss2'
                boss.draw()
            elif count1 == 2:
                boss.image = 'boss3'
                boss.draw()
        if bigbossspawn == True:
            bigboss.draw()
        if goitem == True:
            item.draw()
        if goitem2 == True:
            itemdbuff.draw()
        drawLasers()
        drawAliens()
        screen.draw.text(str(score), topright=(780, 10), owidth=0.5, ocolor=(
            255, 255, 255), color=(0, 64, 255), fontsize=60)
        screen.draw.text("LEVEL " + str(level), midtop=(400, 10), owidth=0.5,
                         ocolor=(255, 255, 255), color=(0, 64, 255), fontsize=60)
        drawLives()
        if player.status >= 30:
            if player.lives > 0:
                drawCentreText("YOU WERE HIT!\nPress Enter to re-spawn")
            else:
                drawCentreText("GAME OVER!\nPress Enter to continue")
        if len(aliens) == 0:
            drawCentreText(
                "LEVEL CLEARED!\nPress Enter to go to the next level")
    if gameStatus == 2:  # game over show the leaderboard
        drawHighScore()
def playerchange():#การเปลี่ยนรูปเมื่อเก็บitem
    global power_up,power_up2,player,num
    if power_up > 0:
        if num == 1:
            player.image = 'player1'
        else:
            player.image = 'player'
    else:
        player.image = player.images[math.floor(player.status/6)]

def drawCentreText(t):#กำหนดขาดหรือสีของตัวหนังสือ
    screen.draw.text(t, center=(400, 300), owidth=0.5, ocolor=(
        255, 255, 255), color=(255, 64, 0), fontsize=60)


def update():  # Pygame Zero update function
    global moveCounter, player, gameStatus, lasers, level, boss

    if gameStatus == 0:
        if keyboard.RETURN and player.name != "":
            gameStatus = 1
    if gameStatus == 1:
        if player.status < 30 and len(aliens) > 0:
            checkKeys()
            updateLasers()
            updateBoss()
            spawn()
            spawnitem2()
            updatebigboss()
            if moveCounter == 0:
                updateAliens()
            moveCounter += 1
            if moveCounter == moveDelay:
                moveCounter = 0
            if player.status > 0:
                player.status += 1
                if player.status == 30:
                    player.lives -= 1
            if level > 10:
                readHighScore()
                gameStatus = 2
                writeHighScore()
        else:
            if keyboard.RETURN:
                if player.lives > 0:
                    player.status = 0
                    lasers = []
                    if len(aliens) == 0:
                        level += 1
                        boss.active = False
                        initAliens()
                else:
                    readHighScore()
                    gameStatus = 2
                    writeHighScore()
    if gameStatus == 2:
        if keyboard.ESCAPE:
            init()
            gameStatus = 0


def on_key_down(key):#เช็กเมื่อกดเริ่มเกมหรือกดเริ่มเกมใหม่หลังการเกมover
    global player
    if gameStatus == 0 and key.name != "RETURN":
        if len(key.name) == 1:
            player.name += key.name
        else:
            if key.name == "BACKSPACE":
                player.name = player.name[:-1]


def readHighScore():#เอาคะแนนออกจากไฟล์
    global highScore, score, player
    highScore = []
    try:
        hsFile = open("highscores.dat", "rb")
        end_of_file =False
        while not end_of_file:
            try:
                word = pickle.load(hsFile)
            
                highScore.append(word.rstrip())
            except EOFError:
                end_of_file =True
    except:
        pass
    highScore.append(str(score) + " " + player.name)
    highScore.sort(key=natural_key, reverse=True)


def natural_key(string_):#กรอกชื่อตอนเริ่มเกม
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def writeHighScore():#เขียนคะแนนลงไฟล์
    global highScore
    hsFile = open("highscores.dat", "wb")
    for line in highScore:
        pickle.dump(line,hsFile)
    hsFile.close()


def drawHighScore():#วาดคะแนนplayerที่ทำได้
    global highScore
    y = 0
    e = 0
    screen.draw.text("TOP SCORES", midtop=(400, 30), owidth=0.5, ocolor=(
        255, 255, 255), color=(0, 64, 255), fontsize=60)
    for line in highScore:
        e = e+1
        if y < 400:
            Q = str(e)
            screen.draw.text(line, midtop=(400, 100+y), owidth=0.5,
                             ocolor=(0, 0, 255), color=(255, 255, 0), fontsize=50)
            screen.draw.text(Q+" :",midtop=(100,100+y),owidth=0.5,
                             ocolor=(0, 0, 255), color=(255, 255, 0), fontsize=50)
            y += 50
    screen.draw.text("Press Escape to play again", center=(
        400, 550), owidth=0.5, ocolor=(255, 255, 255), color=(255, 64, 0), fontsize=60)


def drawLives():#วาดชีวิตplayer
    for l in range(player.lives):
        screen.blit("life", (10+(l*32), 10))


def drawAliens():#วาดAliens
    for a in range(len(aliens)):
        aliens[a].draw()




def drawLasers():#วาดlasers
    for l in range(len(lasers)):
        lasers[l].draw()


def checkKeys():#ฟั่งชั่นที่เซ็กการเคลื่อนที่ของplayerและอื่นๆ
    global player, score, item ,a,Q,R,F,timeup
    if keyboard.left:
        if a == 30:
            if player.x > 40:
                player.x -= 2
        else:
            if player.x > 40:
                player.x -= 5
    if keyboard.right:
        if a == 30:
            if player.x < 760:
                player.x += 2
        else:
            if player.x < 760:
                player.x += 5
    if keyboard.up:
        if a == 30:
            if player.y > 350:
                player.y -= 2 
        else:
            if player.y > 350:
                player.y -= 5
    if keyboard.down:
        if a == 30:
            if player.y < 570:
                player.y += 2
        else:
            if player.y < 570:
                player.y += 5
    
    if keyboard.space:
        global power_up,P,count,power_up2,num
        if player.laserActive == 1:
            count +=1
            sounds.pew.play()
            player.laserActive = 0
            if a == 1:
                power_up -= 200
                if power_up > 0:
                    R = True
                    itemA()
                else:
                    R = False
                    nomale()
            elif a == 2:
                if count == 1:
                    P = -9
                elif count == 2:
                    P = 0
                elif count == 3:
                    P = 9
                    count = 0
                power_up -= 200
                if power_up > 0:
                    F = True
                    itemb()
                else:
                    F = False
                    P = 0
                    nomale()
            elif a == 30:
                power_up -= 200
                if power_up > 0:
                    item2()
                else:
                    nomale()
            else:
                nomale()
                a = 0
            lasers.append(Actor("laser2", (player.x, player.y-32)))
            lasers[len(lasers)-1].status = 0
            lasers[len(lasers)-1].type = 1


def makeLaserActive():#เซ็กplayerกดยิงlaser
    global player
    player.laserActive = 1


def updateLasers():#การเคลื่อนที่ของlaser
    global lasers, aliens,a,P
    for l in range(len(lasers)):
        if lasers[l].type == 0:
            lasers[l].y += 2
            checkLaserHit(l)
            if lasers[l].y > 600:
                lasers[l].status = 1
        if lasers[l].type == 1:
            lasers[l].y -= 10
            if a == 2:
                lasers[l].y -= 7
                lasers[l].x += P
            checkPlayerLaserHit(l)
            if lasers[l].y < 10:
                lasers[l].status = 1
    lasers = listCleanup(lasers)
    aliens = listCleanup(aliens)


def listCleanup(l):#ฟั่งชั่นที่เอาไว้ลบสิ่งที่ระเบิดหรือหายไปแล้ว
    newList = []
    for i in range(len(l)):
        if l[i].status == 0:
            newList.append(l[i])
    return newList


def checkLaserHit(l):#ฟั่งชั่นเอาไว้เซ็คเมื่อPlayerโดนยิง
    global player,boss,power_up,power_up2
    if player.collidepoint((lasers[l].x, lasers[l].y)):
        power_up = 0
        power_up2 = 0
        sounds.explosion.play()
        player.status = 1
        lasers[l].status = 1
    if player.colliderect(boss):
        sounds.explosion.play()
        player.status = 1
        lasers[l].status = 1


def checkPlayerLaserHit(l):#การที่เอาไว้เซ็คPlayerยิงlaserโดนAliens
    global score, boss,aliens,player,bigboss,bigbossspawn,hpbigboss
    for a in range(len(aliens)):
        if aliens[a].collidepoint((lasers[l].x, lasers[l].y)):
            sounds.expl6.play()
            lasers[l].status = 1
            aliens[a].status = 1
            score += 1000
    if boss.active:
        if boss.collidepoint((lasers[l].x, lasers[l].y)):
            sounds.expl3.play()
            lasers[l].status = 1
            boss.active = 0
            score += 5000
    if bigbossspawn == True:
        if bigboss.collidepoint((lasers[l].x,lasers[l].y)):
            hpbigboss -= 250
            if hpbigboss > 0:
                lasers[l].status = 1
                sounds.explosion.play()
            else:
                score += 10000
                bigbossspawn = False



def updateAliens():#การกำหนดการเคลื่อนที่ของAliensเเละการยิง
    global moveSequence, lasers, moveDelay,level
    movex = movey = 0
    if moveSequence < 10 or moveSequence > 30:
        movex = -15
    if moveSequence == 10 or moveSequence == 30:
        movey = 40 + (5*level)
        moveDelay -= 1
    if moveSequence > 10 and moveSequence < 30:
        movex = 15
    for a in range(len(aliens)):
        animate(aliens[a], pos=(aliens[a].x + movex,
                                aliens[a].y + movey), duration=0.5, tween='linear')
        if randint(0, 1) == 0:
            aliens[a].image = "alien1"
        else:
            aliens[a].image = "alien1b"
            if randint(0, 25-(3+level)) == 0:
                lasers.append(Actor("laser1", (aliens[a].x, aliens[a].y)))
                lasers[len(lasers)-1].status = 0
                lasers[len(lasers)-1].type = 0
                sounds.laser.play()
        if aliens[a].y > 500 and player.status == 0:
            sounds.explosion.play()
            player.status = 1
            player.lives = 1
    moveSequence += 1
    if moveSequence == 40:
        moveSequence = 0


def updateBoss():#การกำหนดการเกิดของมินิบอส
    global boss, level, player, lasers ,item
    if boss.active:
        boss.y += (0.3*level)
        if boss.direction == 0:
            boss.x -= (1 * level)
        else:
            boss.x += (1 * level)
        if boss.x < 100:
            boss.direction = 1
        if boss.x > 700:
            boss.direction = 0
        if boss.y > 500:
            sounds.explosion.play()
            player.status = 1
            boss.active = False
        if randint(0, 200-(10*level)) == 0:
            lasers.append(Actor("laser1", (boss.x, boss.y)))
            sounds.gun.play()
            lasers[len(lasers)-1].status = 0
            lasers[len(lasers)-1].type = 0
    else:
        if randint(0, 800) == 0:
            boss.active = True
            boss.x = 800
            boss.y = 100
            boss.direction = 0
def updatebigboss():#การกำหนดการเกิดของบอสใหญ่
    global bigbossspawn,level,player,lasers,item,bigboss,bigbossgo,hpbigboss
    if bigbossspawn == True:
        boss.y -= (0.2)
        if bigbossgo == 0:
            bigboss.x -= 1
        else:
            bigboss.x += 1
        if (level%5) != 0:
            bigbossspawn = False
        if bigboss.x < 100:
            bigbossgo = 1
        if bigboss.x > 700:
            bigbossgo = 0
        if bigboss.y > 500:
            sounds.explosion.play()
            player.status = 1
            bigbossspawn = False
        if randint(0, 100-(5*level)) == 0:
            lasers.append(Actor("laser1", (bigboss.x, bigboss.y)))
            sounds.gun.play()
            lasers[len(lasers)-1].status = 0
            lasers[len(lasers)-1].type = 0
    else:
        if (level % 5) == 0:
            if (level % 5) == 0 and hpbigboss > 0:
                bigbossspawn = True
                bigboss.x = 800
                bigboss.y = 100
                bigbossgo = 0
        else:
            hpbigboss = 5000
            bigbossspawn = False

def init():#เป็นที่รวมของฟั่งชั่นต่างๆ
    global lasers, score, player, moveSequence, moveCounter, moveDelay, level, boss
    initAliens()
    moveCounter = moveSequence = player.status = score = player.laserCountdown = 0
    lasers = []
    moveDelay = 30
    boss.active = False
    player.images = ["life", "explosion1", "explosion2",
                     "explosion3", "explosion4", "explosion5"]
    player.laserActive = 1
    player.lives = 3
    player.name = ""
    level = 1


def initAliens():#กำหนดการเกิดของaliens
    global aliens, moveCounter, moveSequence
    aliens = []
    moveCounter = moveSequence = 0
    for a in range(18):
        aliens.append(Actor("alien1", (210+(a % 6)*80, 100+(int(a/6)*64))))
        aliens[a].status = 0


def collideLaser(self, other):#ฟั่งชั้นที่เมื่ออะไรก็ตามโดนlasers
    return (
        self.x-20 < other.x+5 and
        self.y-self.height+30 < other.y and
        self.x+32 > other.x+5 and
        self.y-self.height+30 + self.height > other.y
    )

def spawn():#กำหนดการเกิดของไอเทมสีฟ้า
    global item,goitem,score
    if goitem == True:
        item.y += 2
        item_collected = player.colliderect(item)
        if item_collected:
            place_item()
            score += 5000
            goitem = False
        if item.y == 600:
            goitem = False
    else:
        if randint(0,150)== 0:
            goitem = True
            item.x = randint(40,760)
            item.y = 40
def spawnitem2():#กำหนดการเกิดของไอเทมสีแดง
    global itemdbuff,goitem2,score,power_up2
    if goitem2 == True:
        itemdbuff.y += 6
        item_collected = player.colliderect(itemdbuff)
        if item_collected:
            place_item2()
            score -= 5000
            goitem2 = False
        if itemdbuff.y > 600:
            goitem2 = False
    else:
        if randint(0,300)== 0:
            goitem2 = True
            itemdbuff.x = randint(40,760)
            itemdbuff.y = 40

def place_item():#กำหนดการรีเกิดของไอเทมสีฟ้า
    global item,a,power_up,count
    a = randint(1,2)
    item.x = randint(40,760)
    item.y = -5000
    count = 0
    power_up = 5000
def place_item2():#กำหนดการรีเกิดของไอเทมสีแดง
    global itemdbuff,a,power_up
    power_up = 2000
    itemdbuff.x = randint(40,760)
    itemdbuff.y = -100000
    a = 30
def item2():#เมื่อถูกใช่งานจะทำให้เกิดสถานะผิดปกติกับตัวยาน
    global num
    num = 1
    clock.schedule(makeLaserActive, 1.5)
def itemA():#เมื่อถูกเรียกใช้จะทำให้เกิดการยิงไวขั้น
    global Q,R,F,num
    num = 0
    if R == True:
        clock.schedule(makeLaserActive, 0.25)
    else:
        clock.schedule(makeLaserActive, 1.0)
def nomale():#การยิงกระสุนแบบปกติ
    global Q,R,F,num
    num = 0
    clock.schedule(makeLaserActive, 1)

def itemb():#เมื่อถูกเรียกใช้จะทำให้เกิดการยิงแบบที่2
    global score,Q,R,F,num
    num = 0
    if F == True:
        clock.schedule(makeLaserActive, 0.10)
            
init()
pgzrun.go()
