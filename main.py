from Constant import *
from Page_Menu import Page_Menu
import Global as glb

if __name__ == "__main__":
	glb.pages.append(Page_Menu())
	have_focus = 1
	while True:
		glb.clock.tick(FPS)
		glb.frame_time += 1

		for event in pg.event.get():
			if event.type == pg.QUIT and isinstance(glb.pages[-1], Page_Menu):
				force_quit()
			if event.type == pg.QUIT:
				glb.soft_quit()
			elif event.type == pg.WINDOWFOCUSLOST:
				have_focus = 0
				glb.ctrl.clear()
			elif event.type == pg.WINDOWFOCUSGAINED:
				have_focus = 1
				glb.ctrl.clear()
			elif event.type == pg.KEYDOWN:
				glb.key_time += 1
				glb.ctrl.add_key(event.key, glb.key_time)
			elif event.type == pg.KEYUP:
				glb.ctrl.del_key(event.key)
			elif event.type == pg.MOUSEBUTTONDOWN:
				if event.button == 1:
					glb.ctrl.mouse_down(event.pos)
			elif event.type == pg.MOUSEBUTTONUP:
				if event.button == 1:
					glb.ctrl.mouse_up()

		if have_focus:
			glb.refresh_page()
			glb.refresh_display()
