from level import *
from block import *
from player import *
from ball import *


class Game(object):
    def __init__(self, surface):
        self.surface = surface
        self.Load(2)

    def Load(self, lv):
        self.level = Level(lv)
        self.isGameOver = False
        
        self.balls = []
        self.loadBlockImage()
        self.loadPlayer()
        self.loadBall(self.player.Get_Rect().x,
                      self.player.Get_Rect().y-SPRITE_SIZE_H-5, 1, -1)

    def loadBlockImage(self):
        self.blocks = []
        for block in self.level.GetBlocks():
            sp = Block(block[2], block[0], block[1], (0, 0))
            self.blocks.append(sp)

    def update(self):
        if self.isGameOver:
            return 
        self.player.update()
        [ball.update() for ball in self.balls]
        self.checkBallBlockCollide()
        self.checkBallPlayerCollide()
        if self.isGameWin():
            self.Load(self.level.level+1)

        flag = True
        while flag:
            flag=False
            for ball in self.balls:
                if ball.Get_Rect().y > GAME_SIZE[1]:
                    self.balls.remove(ball)
                    flag =True
                    break

        if len(self.balls) == 0:
            self.isGameOver = True

    def draw(self):
        
        self.player.draw(self.surface)
        [block.draw(self.surface) for block in self.blocks]
        [ball.draw(self.surface) for ball in self.balls]

        if self.isGameOver:
            img = pygame.image.load(GAME_OVER_RES)
            self.surface.blit(img,img.get_rect())
            return

    def loadPlayer(self):
        self.player = Player(
            PLAYER_RES,
            (GAME_SIZE[0]-PLAYER_SIZE_W)/2, GAME_SIZE[1] -
            PLAYER_SIZE_H, SPRITE_SIZE_W, GAME_SIZE[0] -
            PLAYER_SIZE_W-SPRITE_SIZE_W
        )

    def loadBall(self, x, y, dirX, dirY):
        self.ball = Ball(BALL_RES, x, y, dirX, dirY)
        self.balls.append(self.ball)

    def checkBallBlockCollide(self):
        for ball in self.balls:
            for block in self.blocks:
                if ball.Get_Rect().colliderect(block.Get_Rect()):
                    ball.changeDir(block.Get_Rect())
                    self.processBlock(ball,block)
                    break

    def checkBallPlayerCollide(self):
        for ball in self.balls:
            if ball.Get_Rect().colliderect(self.player.Get_Rect()):
                ball.changeYDir(self.player.Get_Rect())
                break

    def processBlock(self, ball, block):
        if block.GetBlockType() == BlockType.NORMAL:
            self.blocks.remove(block)
        
        if block.GetBlockType() == BlockType.COPY:
            self.blocks.remove(block)
            self.copyBalls()

        if block.GetBlockType() == BlockType.SPEED_UP:
            self.blocks.remove(block)
            ball.SetSpeed(1)

        if block.GetBlockType() == BlockType.SPEED_DOWN:
            self.blocks.remove(block)
            ball.SetSpeed(0.2)

    def copyBalls(self):
        balls = [ball for ball in self.balls]
        for ball in balls:
            self.loadBall(ball.Get_Rect().x,ball.Get_Rect().y,1,-1)
    
    def isGameWin(self):
        for block in self.blocks:
            if block.GetBlockType()!=BlockType.WALL:
                return False
        return True
