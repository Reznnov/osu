import sys
from ctypes.wintypes import RGB

import sdl2
import sdl2.ext
import os

from sdl2.ext.compat import isiterable


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


class note_sprite(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=100, posy=100):
        self.sprite = sprite
        self.sprite.position = posx, posy


class game_process():
    def __init__(self, world):
        # f = map(open("map.txt").read().split(), int)
        f = [[3], [5], [7], [8]]
        n = []
        timer = Timer()
        for i in f:
            note = Note(i[0])
            world.add_system(note)
            factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
            sp_ball = factory.from_image("approachcircle.png")
            a = load_image("approachcircle.png")
            sdl2.surface.SDL_SetColorKey(sp_ball, RGB(255,0,255), sdl2.SDL_MapRGB(format, 0, 0, 0))
            note_sp = note_sprite(world, sp_ball, posx=(100 + i[0] * 100), posy=(900 - i[0] * 100))
            note_sp.timer = timer
            note.note = note_sp


        running = True
        while running:
            events = sdl2.ext.get_events()
            for event in events:
                if event.key.keysym.sym == sdl2.SDLK_z:

                    print("n")
                if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                    motion = event.motion
                    print(motion.x, motion.y)
                    print(sdl2.timer.SDL_GetTicks() / 1000)
                if event.key.keysym.sym == sdl2.SDLK_r:
                    running = False
                    break
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break
            world.process()


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
    def __init__(self, time):
        super().__init__()
        self.componenttypes = Timer, note_sprite, sdl2.ext.Sprite
        self.note = None
        self.time = time
        self.is_active = False

    def _overlap(self, item):
        pos, sprite = item
        left, top, right, bottom = sprite.area
        return (right,  left, top, bottom)

    def process(self, world, componentsets):
        if self.time - self.note.timer.get_ticks():
            print(self.note.timer.get_ticks(), self.time, self.note.sprite.sdl2.surface.SDL_GetColorKey())
            self.is_active = True
        # print(self.note.sprite.x)


def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("The Pong Game", size=(1600, 900))
    menu = sdl2.ext.World()
    gameplay = sdl2.ext.World()

    spriterenderer = SoftwareRenderer(window)
    menu.add_system(spriterenderer)
    gameplay.add_system(spriterenderer)

    window.show()
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
