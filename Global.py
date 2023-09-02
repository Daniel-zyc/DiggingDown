from Constant import *
from Control import Control
from Page_YN import Page_YN
from Achieve import Achieve
from Log import Log
import ToolFunc as tool

screen = pg.display.set_mode((SCR_W, SCR_H))
clock = pg.time.Clock()
ctrl = Control()
frame_time = key_time = 0
pages = []
achieve = Achieve()
log = Log()


def refresh_display():
	pg.draw.rect(screen, (0, 0, 0), pages[-1].update_range)
	pages[-1].draw(screen)
	pg.display.update(pages[-1].update_range)


def get_YN():
	global frame_time, key_time
	pages.append(Page_YN())
	refresh_display()
	have_focus = 1
	while True:
		clock.tick(FPS)
		frame_time += 1

		for event in pg.event.get():
			if event.type == pg.KEYDOWN:
				key_time += 1
				ctrl.add_key(event.key, key_time)
			elif event.type == pg.KEYUP:
				ctrl.del_key(event.key)
			elif event.type == pg.WINDOWFOCUSLOST:
				have_focus = 0
			elif event.type == pg.WINDOWFOCUSGAINED:
				have_focus = 1
		if have_focus:
			status, data = pages[-1].refresh(ctrl)
			if status == PAGE_NONE:
				continue
			if status == PAGE_EXIT:
				pages.pop()
				return data


def soft_quit():
	status = get_YN()
	if status:
		tool.force_quit()
	else:
		return


def refresh_page():
	status = pages[-1].refresh(ctrl)
	if status == PAGE_NONE:
		return
	if len(pages) == 1:
		tool.force_quit()
	pages.pop()
