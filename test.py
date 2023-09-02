from Constant import *
from Global import *

group1 = pg.sprite.Group()
group2 = pg.sprite.Group()

sp1 = pg.sprite.Sprite()
sp1.image = pg.image.load(BLK_IMG_URL[DIAMOND])
sp1.rect = sp1.image.get_rect()
sp1.rect.x, sp1.rect.y = 0, 0

sp2 = pg.sprite.Sprite()
sp2.image = pg.image.load(BLK_IMG_URL[COPPER])
sp2.rect = sp2.image.get_rect()
sp2.rect.x, sp2.rect.y = 12, 0

sp3 = pg.sprite.Sprite()
sp3.image = pg.image.load(BLK_IMG_URL[EMERALD])
sp3.rect = sp3.image.get_rect()
sp3.rect.x, sp3.rect.y = 12, 12

group2.add(sp2)
group1.add(sp1)

for i in range(0, FPS*4):
	clock.tick(FPS)

	group1.draw(screen)
	group2.draw(screen)

	if i == 96:
		group1.add(sp3)

	pg.display.update()
