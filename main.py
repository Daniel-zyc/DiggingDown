import logging

from Constant import *
from Control import Control, Key
from Page_Menu import Page_Menu
import Global as glb


def window_quit():
	status = glb.get_Y_or_N()
	if status:
		PG.quit()
		sys.exit(0)
	else:
		return


def refresh_page_all():
	status = glb.pages[-1].refresh(glb.ctrl)
	if status == PAGE_NONE:
		return
	if len(glb.pages) == 1:
		window_quit()
		return
	glb.pages.pop()


if __name__ == "__main__":
	glb.pages.append(Page_Menu())
	while True:
		glb.clock.tick(FPS)
		glb.frame_time += 1

		for event in PG.event.get():
			if event.type == PG.QUIT:
				window_quit()
			elif event.type == PG.KEYDOWN:
				glb.key_time += 1
				glb.ctrl.add_key(Key(event.key, glb.key_time))
			elif event.type == PG.KEYUP:
				glb.key_time += 1
				glb.ctrl.del_key(Key(event.key, glb.key_time))

		refresh_page_all()
		glb.window_refresh_display()

