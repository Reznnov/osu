import sys
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


class Velocity(object):
    def __init__(self):
        super(Velocity, self).__init__()
        self.vx = 0
        self.vy = 0


class Note(sdl2.ext.Applicator):
    def __init__(self):
        super().__init__()
        print(self.componenttypes)
        self.componenttypes = note_sprite, sdl2.ext.Sprite
        print(self.componenttypes)

    def start_timer(self):
        self.status = True
        self.paused = False
        self.startTicks = sdl2.timer.SDL_GetTicks()

    # def stop(self):
    #     self.status = False
    #     self.paused = False

    def get_ticks(self):
        return sdl2.timer.SDL_GetTicks() - self.startTicks

    def process(self, world, componentsets):
        collitems = [comp for comp in componentsets if self._overlap(comp)]
        print(collitems)
        for sprite in componentsets:
            print(sprite)
            print("smh")
            sprite.x += 50


def run():
    sdl2.ext.init()

    window = sdl2.ext.Window("The Pong Game", size=(800, 600))
    world = sdl2.ext.World()


    note = Note()
    spriterenderer = SoftwareRenderer(window)
    world.add_system(spriterenderer)
    world.add_system(note)


    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    sp_ball = factory.from_image("screenshot023.png")
    note_sp = note_sprite(world, sp_ball)
    window.show()
    running = True
    state = sdl2.mouse.SDL_GetMouseState(None, None)


    while running:
        events = sdl2.ext.get_events()

        for event in events:
            if event.key.keysym.sym == sdl2.SDLK_z:
                note.start_timer()
                print("n")
            if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                motion = event.motion
                print(motion.x, motion.y)
                print(sdl2.timer.SDL_GetTicks() / 1000)
                print(note.get_ticks() / 1000)
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        world.process()
    return 0



if __name__ == "__main__":
    sys.exit(run())
