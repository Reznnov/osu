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
        #print(collitems)
        for sprite in componentsets:
            print(sprite)
            print("smh")
            sprite.x += 50

class PlayerData(object):
    def __init__(self):
        super(PlayerData, self).__init__()
        self.ai = False


class Player(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0, ai=False):
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.velocity = Velocity()
        self.playerdata = PlayerData()
        self.playerdata.ai = ai


class game_pr():
    def __init__(self, world):
        # for i in range(10):
        #     n.append(Note())
        note = Note()
        world.add_system(note)
        sdl2.ext.init()
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
        sp_ball = factory.from_image("approachcircle.png")
        note_sp = note_sprite(world, sp_ball)
        note.note = note_sp
        running = True
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
                if event.key.keysym.sym == sdl2.SDLK_m:
                    running = False
                    break
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break
            world.process()
        return None


def run():
    window = sdl2.ext.Window("The Pong Game", size=(1600, 900))
    menu = sdl2.ext.World()
    world = sdl2.ext.World()


    note = Note()
    spriterenderer = SoftwareRenderer(window)
    menu.add_system(spriterenderer)
    world.add_system(spriterenderer)
    menu.add_system(note)
    world.add_system(note)


    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    sp_ball = factory.from_image("approachcircle.png")
    sp_ball_1 = factory.from_image("approachcircle.png")
    note_sp = note_sprite(menu, sp_ball)
    note_sp = note_sprite(menu, sp_ball_1)
    running = True
    state = sdl2.mouse.SDL_GetMouseState(None, None)

    player1 = Player(menu, sp_ball, 100, 250)
    player2 = Player(menu, sp_ball_1, 400, 250)
    sdl2.ext.init()
    window.show()

    while running:
        events = sdl2.ext.get_events()

        for event in events:
            if event.key.keysym.sym == sdl2.SDLK_q:
                game_pr(world)
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        menu.process()
    return 0



if __name__ == "__main__":
    sys.exit(run())