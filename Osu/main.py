import ctypes
import sys
import pygame as pg
import sdl2
import sdl2.ext
import os
from PIL import Image
from sys import path
from sdl2.test.sdlgfx_test import sdlgfx

path.insert(0, "/templates")

class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))
        super(SoftwareRenderer, self).render(components)


class song():
    pass

class note_sprite(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=100, posy=100):
        self.sprite = sprite
        self.sprite.position = posx, posy


class Timer(object):
    def __init__(self):
        super().__init__()
        self.status = True
        self.paused = False
        self.startTicks = sdl2.timer.SDL_GetTicks()

    def stop(self):
        self.status = False
        self.paused = False

    def get_ticks(self):
        return round((sdl2.timer.SDL_GetTicks() - self.startTicks) / 1000, 1)


class Note(sdl2.ext.Applicator):
    def __init__(self, time, ar):
        super().__init__()
        self.componenttypes = Timer, note_sprite, sdl2.ext.Sprite
        self.note = None
        self.time = time
        self.is_active = False
        self.ar = ar
        self.x, self.y = ctypes.c_int(0), ctypes.c_int(0)
        self.flag, self.flag1 = True, True
        self.circle_im = self.draw_circle()

    def check(self, x, y):
        rx = x - (self.note.sprite.x + 70)
        ry = y - (self.note.sprite.y + 70)
        if (rx ** 2 + ry ** 2) < 1400:
            self.note.sprite.surface = sdl2.ext.load_image("templates/hit300.png")
            self.ar = (self.note.timer.get_ticks() + 1) - self.time
            self.flag1 = False

    def process(self, world, componentsets):
        if self.flag:
            if self.time == self.note.timer.get_ticks() and not self.is_active:
                self.is_active = True
                self.note.sprite.surface = sdl2.ext.load_image(self.circle_im)
            if self.time + self.ar == self.note.timer.get_ticks():
                if self.flag1:
                    self.ar += 1
                    self.flag1 = False
                    self.note.sprite.surface = sdl2.ext.load_image("templates/hit0-0.png")
                    self.note.sprite.x += 60
                    self.note.sprite.y += 60
                else:
                    self.is_active = False
                    self.note.world.delete(self.note)
                    self.flag = False

    def update(self, x, y):
        if self.flag1:
            self.check(x, y)


    def draw_circle(self):
        sp = []
        image = Image.open('templates/approachcircle.png')
        size = image.size
        pix = image.load()
        image2 = Image.new("RGB", size)
        for x in range(size[0]):
            for y in range(size[1]):
                image2.putpixel([x, y], pix[x, y])
        image2.save("templates/approachcircle2.png")
        return "templates/approachcircle.png"


class Menu_app(sdl2.ext.Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = Menu_sp, sdl2.ext.Sprite

    def process(self, world, componentsets):
        pass


class Menu_sp(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx, posy):
        self.sprite = sprite
        self.sprite.position = posx, posy


class game_process():
    def __init__(self, world):
        # f = map(open("map.txt").read().split(), int)
        f = [[1, 300, 100], [2, 350, 100], [3, 600, 450], [5, 400, 200], [7, 900, 500], [6, 300, 500]]
        ar = 3
        n = []
        timer = Timer()
        te = sdlgfx
        image2 = Image.new("RGB", (1, 1), (0, 0, 0))
        image2.save("templates/pix.png")
        space = []
        for i in f:
            note = Note(i[0], ar)
            world.add_system(note)
            texture = sdl2.ext.load_image("templates/pix.png")
            factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
            note_pic = factory.from_surface(texture)
            note_sp = note_sprite(world, note_pic, posx=i[1], posy=i[2])
            note_sp.timer = timer
            note.note = note_sp
            space.append(note)
        pg.mixer.music.play()
        pg.mixer.music.set_volume(0.1)
        running = True
        while running:
            events = sdl2.ext.get_events()
            for event in events:
                motion = None
                if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                    motion = event.motion
                if event.key.keysym.sym == sdl2.SDLK_r:
                    running = False
                    break
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break
            world.process()
            if motion:
                for note_ob in space:
                    if note_ob.is_active:
                        note_ob.update(motion.x, motion.y)


def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("Osu", size=(1920, 1080))
    menu = sdl2.ext.World()
    gameplay = sdl2.ext.World()

    spriterenderer = SoftwareRenderer(window)
    menu.add_system(spriterenderer)
    gameplay.add_system(spriterenderer)
    window.show()
    running = True

    lvl_1 = Menu_app()
    menu.add_system(lvl_1)
    texture = sdl2.ext.load_image("templates/1.png")
    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    menu_pic = factory.from_surface(texture)
    Menu_sp = note_sprite(menu, menu_pic, 538, 144)
    lvl_1.sp = Menu_sp
    pg.init()
    pg.mixer.music.load('templates/audio.wav')

    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.key.keysym.sym == sdl2.SDLK_q:
                game_process(gameplay)
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        menu.process()
    return 0



if __name__ == "__main__":
    sys.exit(run())