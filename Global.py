from Constant import *
from Control import Control
from Page_YN import Page_YN
from Page_WN import Page_WN
from Page_CG import Page_CG
from Achieve import Achieve
from Log import Log

ctrl = Control()
achieve = Achieve()
log = Log()
have_focus = frame_time = key_time = 1
pages = []
cur_bgm=menu_sound

def refresh_display():
	pg.draw.rect(screen, (0, 0, 0), pages[-1].update_range)
	pages[-1].draw(screen)
	pg.display.update(pages[-1].update_range)


def get_event():
	global key_time, have_focus
	for event in pg.event.get():
		if event.type == pg.KEYDOWN:
			key_time += 1
			ctrl.add_key(event.key, key_time)
		elif event.type == pg.KEYUP:
			ctrl.del_key(event.key)
		elif event.type == pg.WINDOWFOCUSLOST:
			have_focus = 0
			ctrl.clear()
		elif event.type == pg.WINDOWFOCUSGAINED:
			have_focus = 1
			ctrl.clear()
		elif event.type == pg.MOUSEBUTTONDOWN:
			if event.button == 1:
				ctrl.mouse_down(event.pos)
		elif event.type == pg.MOUSEBUTTONUP:
			if event.button == 1:
				ctrl.mouse_up()


def get_YN(info: str):
	global frame_time, have_focus
	pages.append(Page_YN(info))
	refresh_display()
	while True:
		clock.tick(FPS)
		frame_time += 1
		get_event()
		if have_focus:
			status, data = pages[-1].refresh(ctrl)
			if status == PAGE_EXIT:
				pages.pop()
				return data


def show_WN(info: str, color = DARK_RED):
	global frame_time, have_focus
	pages.append(Page_WN(info, color = color))
	refresh_display()
	while True:
		clock.tick(FPS)
		frame_time += 1
		get_event()
		if have_focus:
			status = pages[-1].refresh(ctrl)
			if status == PAGE_EXIT:
				pages.pop()
				return


def play_CG():
	global frame_time, have_focus
	pages.append(Page_CG())
	refresh_display()
	while True:
		clock.tick(FPS)
		frame_time += 1
		get_event()
		if have_focus:
			status = pages[-1].refresh(ctrl)
			if status == PAGE_EXIT:
				pages.pop()
				return
			refresh_display()


def soft_quit():
	status = get_YN(f'请确认是否退出游戏，所有未保存数据均会丢失')
	if status:
		force_quit()


def refresh_page():
	status = pages[-1].refresh(ctrl)
	if not status:
		return
	if len(pages) == 1:
		force_quit()
	pages.pop()
