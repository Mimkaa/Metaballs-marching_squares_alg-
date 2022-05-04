import random

import pygame as pg
import sys
from settings import *
from objects import *
from os import path
vec=pg.Vector2


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)


    # Convert the 0-1 range into a value in the right range.

    return rightMin + (valueScaled * rightSpan)

def distance_vec(vec1,vec2):
    return math.sqrt((vec1.x-vec2.x)**2+(vec1.y-vec2.y)**2)

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        self.font=path.join("PixelatedRegular-aLKm.ttf")
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.blobs=[Blob((random.randint(20,WIDTH-20),random.randint(20,HEIGHT-20)),random.randint(30,100)) for i in range(8)]
        self.all_sprites = pg.sprite.Group()
        self.field=[]
        for i in range(GRIDWIDTH+1):
            rand_vals=[]
            for j in range(GRIDHEIGHT+1):
                rand_vals.append(random.randint(0,1))
            self.field.append(rand_vals)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()




        # update the field
        for i in range(GRIDWIDTH+1):
            for j in range(GRIDHEIGHT+1):
                sum=0
                x=i*TILESIZE
                y=j*TILESIZE
                for b in self.blobs:
                    d=distance_vec(b.pos,vec(x,y))
                    sum+=(b.radius*0.5)/d
                self.field[i][j]=sum

        # update blobs
        for b in self.blobs:
            b.update(self.dt)



    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def get_state(self,a,b,c,d):
        # gets number of case based on its  binary representation
        return a*8+b*4+c*2+d*1
    def linear_interp(self,val1,val2,start,end):
        return start+((1-val1)/(val2-val1))*(end-start)

    def draw(self):
        self.screen.fill(BLACK)
        #self.draw_grid()
        self.all_sprites.draw(self.screen)

        # draw blobs
        # for b in self.blobs:
        #     b.show(self.screen)

        # for i in range(GRIDWIDTH+1):
        #     for j in range(GRIDHEIGHT+1):
        #         clo=translate(self.field[i][j],0,100,0,255)
        #
        #         pg.draw.circle(self.screen,(clo,clo,clo),(i*TILESIZE,j*TILESIZE),3)

        # outlines
        for i in range(GRIDWIDTH):
            for j in range(GRIDHEIGHT):
                x=i*TILESIZE
                y=j*TILESIZE
                # midpoints of rect sizes
                a_add=self.linear_interp(self.field[i][j],self.field[i+1][j],x,x+TILESIZE)
                a=vec(a_add,y)
                b_add=self.linear_interp(self.field[i+1][j],self.field[i+1][j+1],y,y+TILESIZE)
                b=vec(x+TILESIZE,b_add)
                c_add=self.linear_interp(self.field[i][j+1],self.field[i+1][j+1],x,x+TILESIZE)
                c=vec(c_add,y+TILESIZE)
                d_add=self.linear_interp(self.field[i][j],self.field[i][j+1],y,y+TILESIZE)
                d=vec(x,d_add)
                state=self.get_state(int(self.field[i][j]),int(self.field[i+1][j]),int(self.field[i+1][j+1]),int(self.field[i][j+1]))

                # pg.draw.line(self.screen,WHITE,a,b)
                # pg.draw.line(self.screen,WHITE,a,c)
                # pg.draw.line(self.screen,WHITE,b,d)
                # pg.draw.line(self.screen,WHITE,d,c)
                if state==1:
                    pg.draw.line(self.screen,WHITE,d,c)
                elif state==2:
                    pg.draw.line(self.screen,WHITE,b,c)
                elif state==3:
                    pg.draw.line(self.screen,WHITE,d,b)
                elif state==4:
                    pg.draw.line(self.screen,WHITE,a,b)
                elif state==5:
                    pg.draw.line(self.screen,WHITE,d,a)
                    pg.draw.line(self.screen,WHITE,c,b)
                elif state==6:
                    pg.draw.line(self.screen,WHITE,a,c)
                elif state==7:
                    pg.draw.line(self.screen,WHITE,d,a)
                elif state==8:
                    pg.draw.line(self.screen,WHITE,d,a)
                elif state==9:
                    pg.draw.line(self.screen,WHITE,a,c)
                elif state==10:
                    pg.draw.line(self.screen,WHITE,d,a)
                    pg.draw.line(self.screen,WHITE,c,b)
                elif state==11:
                    pg.draw.line(self.screen,WHITE,a,b)
                elif state==12:
                    pg.draw.line(self.screen,WHITE,d,b)
                elif state==13:
                    pg.draw.line(self.screen,WHITE,c,b)
                elif state==14:
                    pg.draw.line(self.screen,WHITE,c,d)

        # fps
        self.draw_text(str(int(self.clock.get_fps())), self.font, 40, WHITE, 50, 50, align="center")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                



# create the game object
g = Game()
g.new()
g.run()
