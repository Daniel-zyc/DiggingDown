from Constant import *
from Page_Menu import Page_Menu
import ToolFunc as tool
import Global as glb

if __name__ == "__main__":
	glb.pages.append(Page_Menu())
	while True:
		glb.clock.tick(FPS)
		glb.frame_time += 1

		for event in pg.event.get():
			if event.type == pg.QUIT and isinstance(glb.pages[-1], Page_Menu):
				tool.force_quit()
			elif event.type == pg.QUIT:
				glb.soft_quit()
			elif event.type == pg.KEYDOWN:
				glb.key_time += 1
				glb.ctrl.add_key(event.key, glb.key_time)
			elif event.type == pg.KEYUP:
				glb.ctrl.del_key(event.key)

		glb.refresh_page()
		glb.refresh_display()
