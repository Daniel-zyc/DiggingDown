from Constant import *
from Sprite import Sprite
from SpriteGroup import SpriteGroup
import random


class Background_Sp(Sprite):
    def __init__(self, img_url = None, fill = True):
        super().__init__()
        if img_url is None:
            self.image = pg.image.load(SKY_IMG_URL.format(random.randint(0, SKY_LEN - 1)))
        else:
            self.image = pg.image.load(img_url)

        image_height = self.image.get_height()
        image_width = self.image.get_width()

        ratio_h = SCR_H / image_height
        ratio_w = SCR_W / image_width

        if fill:
            ratio = max(ratio_w, ratio_h)
        else:
            ratio = min(ratio_w, ratio_h)

        self.image = pg.transform.scale(self.image, (image_width * ratio, image_height * ratio))
        self.rect = self.image.get_rect()
        self.rect.center = (SCR_CEN_X, SCR_CEN_Y)

    def empty(self):
        pass


class Background:
    def __init__(self):
        self.spg = SpriteGroup()
        self.spg.add(Background_Sp())
        mask = Sprite()
        mask.image = pg.surface.Surface((SCR_W, SCR_H))
        mask.image.set_alpha(144)
        mask.rect = mask.image.get_rect()
        mask.rect.x, mask.rect.y = 0, 0
        self.spg.add(mask)

    def draw(self, scr):
        self.spg.draw(scr)

    def empty(self):
        self.spg.empty()


class MenuText(Sprite):
    def __init__(self, text, size, posx = 0.5, posy = 0.5, color = (255, 255, 255), font = PIXEL_FONT_URL, center = True, absolute = False):
        super().__init__()
        size = int(size * SCR_H // 600)
        position = (int(SCR_W * posx), int(SCR_H * posy))
        if absolute:
            position = (posx, posy)
        font = pg.font.Font(font, size)
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect()
        if center:
            self.rect.center = position
        else:
            self.rect.topleft = position
        self.text = text

    def empty(self):
        self.kill()


class Block(Sprite):
    def __init__(self, w: int = SCR_W, h: int = SCR_H // 5, color = DARK_RED):
        super().__init__()
        self.w = w
        self.h = h
        self.image = pg.Surface((int(w), int(h)))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.center = (SCR_W // 2, SCR_H // 2)
