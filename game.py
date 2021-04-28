import ctypes
import sys
from ctypes.wintypes import RGB

import sdl2
import sdl2.ext
import os

from numpy.core import uint32
from sdl2 import surface, SDL_GetColorKey, SDL_SetColorKey
from sdl2.ext.compat import isiterable
from sdl2.sdlimage import IMG_Load
from PIL import Image


def load_image(name, colorkey=None, convert=None):
    fullname = os.path.join(name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = sdl2.ext.load_image(fullname)
    # if colorkey is not None:
    #     image = image.convert()
    #     if colorkey == -1:
    #         colorkey = image.get_at((0, 0))
    #     image.set_colorkey(colorkey)
    # else:
    #     image = image.convert_alpha()
    # if convert is not None:
    #     image = pygame.transform.scale(image, convert)
    return image


class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))
        super(SoftwareRenderer, self).render(components)


class song():
    pass

class Menu:
    def __init__(self, Window):
        self.window = Window

    def d1_point(self, x, y, surface, color):
        r, g, b = color
        WHITE = sdl2.ext.Color(r, g, b)
        pixelview = sdl2.ext.PixelView(surface)
        pixelview[y][x] = WHITE

    def draw_menu1(self, i, j, color=None):
        image = Image.open('1.png')
        size = image.size
        pix = image.load()
        for x in range(size[0]):
            for y in range(size[1]):
                if color == None:
                    Menu.d1_point(self, x + i, y + j, self.window.get_surface(), pix[x, y][:3])
                else:
                    Menu.d1_point(self, x + i, y + j, self.window.get_surface(), (0, 0, 0))



class game_process():
    def __init__(self, world):
        self.draw_you_win()
        # f = map(open("map.txt").read().split(), int)
        f = [[3], [5], [7], [8]]
        ar = 3
        n = []
        timer = Timer()

        for i in f:
            note = Note(i[0], ar)
            world.add_system(note)
            texture = sdl2.ext.load_image("approachcircle2.png")
            b = sdl2.ext.Color(0xff, 0xff, 0xff)
            SDL_SetColorKey(texture, sdl2.SDL_TRUE, b)
            factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
            note_pic = factory.from_surface(texture)
            note_sp = note_sprite(world, note_pic, posx=(100 + i[0] * 100), posy=(900 - i[0] * 100))
            note_sp.timer = timer
            note.note = note_sp

        running = True
        while running:
            events = sdl2.ext.get_events()
            for event in events:
                motion = None
                if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                    pass
                    # motion = event.motion
                    # print(motion.x, motion.y)
                    # print(sdl2.timer.SDL_GetTicks() / 1000)
                if event.key.keysym.sym == sdl2.SDLK_r:
                    running = False
                    break
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break
            world.process()


    def draw_you_win(self):
        sp = []
        image = Image.open('approachcircle.png')
        size = image.size
        print(size)
        pix = image.load()
        image2 = Image.new("RGB", size)
        for x in range(size[0]):
            for y in range(size[1]):
                if pix[x, y] == (255, 255, 255, 255):
                    image2.putpixel([x, y], (255, 255, 255, 255))
        image2.save("approachcircle2.png")


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
        return (sdl2.timer.SDL_GetTicks() - self.startTicks) // 1000


class Note(sdl2.ext.Applicator):
    def __init__(self, time, ar):
        super().__init__()
        self.componenttypes = Timer, note_sprite, sdl2.ext.Sprite
        self.note = None
        self.time = time
        self.is_active = False
        self.ar = ar
        self.x, self.y = ctypes.c_int(0), ctypes.c_int(0)
        self.flag = True

    def check(self):
        rx = self.x.value - (self.note.sprite.x + 70)
        ry = self.y.value - (self.note.sprite.y + 70)
        print(rx, ry)
        if (rx ** 2 + ry ** 2) < 1400:
            self.note.sprite.surface = sdl2.ext.load_image("hit300.png")

    def process(self, world, componentsets):
        if self.flag:
            if self.time == self.note.timer.get_ticks() and not self.is_active:
                self.is_active = True
                self.note.sprite.surface = sdl2.ext.load_image("approachcircle.png")

            if self.is_active:
                if self.time + self.ar == self.note.timer.get_ticks():
                    print("False")
                    self.is_active = False
                    self.note.world.delete(self.note)
                    self.flag = False
                    # b = sdl2.ext.Color(0xff, 0xff, 0xff)
                    # SDL_SetColorKey(self.note.sprite.surface, sdl2.SDL_TRUE, b)
                else:
                    buttonstate = sdl2.mouse.SDL_GetMouseState(ctypes.byref(self.x), ctypes.byref(self.y))
                    if buttonstate:
                        self.check()







def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("The Pong Game", size=(1600, 900))
    menu = sdl2.ext.World()
    gameplay = sdl2.ext.World()

    spriterenderer = SoftwareRenderer(window)
    menu.add_system(spriterenderer)
    gameplay.add_system(spriterenderer)
    lvl_1 = Menu(window)

    window.show()
    lvl_1.draw_menu1(500, 50)
    running = True
    state = sdl2.mouse.SDL_GetMouseState(None, None)

    # print(note.note.sprite.x)

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