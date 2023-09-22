GAME_SIZE = (1040,1000)
PLAYER_SIZE_W = 96
PLAYER_SIZE_H = 128
SPRITE_SIZE_W = 40
SPRITE_SIZE_H = 40

PLAYER_RES = (
    '../res/player/1_res.png',
    '../res/player/2_res.png',
    '../res/player/3_res.png',
    '../res/player/4_res.png',
    '../res/player/5_res.png',
    '../res/player/6_res.png',
    '../res/player/7_res.png'
)

BALL_RES = '../res/ball.png'

BLOCK_RES_FMT = "../res/%d.png"

GAME_OVER_RES = '../res/fail.png'

class BlockType :
    NULL = 0
    SPEED_UP = 1
    NORMAL = 2
    COPY = 3
    SPEED_DOWN =4
    WALL =9 

class SoundRes:
    JNTM = '../res/ji.mp3'
    NGM = '../res/ngm.mp3'