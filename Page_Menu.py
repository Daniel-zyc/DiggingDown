from Constant import *
from Menu import Background, MenuText
from Control import Control
from Page_Achieve import Page_Achieve
from Page_Read import Page_Read
from Page_Game import init_game
from Page_Key import Page_Key
from Page_Info import Page_Info
from Page import Page
from SpriteGroup import SpriteGroup
import Global as glb


class Page_Menu(Page):
    def __init__(self):
        super().__init__()
        spg = SpriteGroup()
        self.update_range = pg.Rect(0, 0, SCR_W, SCR_H)
        self.list.append(Background())
        spg.add(MenuText('游戏菜单', 64, posy = 0.15))
        self.opt = [None]
        self.opt.append(MenuText('开始游戏 [1]', 36, color = LIGHT_GREEN ,posy = 0.35))
        self.opt.append(MenuText('读取存档 [2]', 36, posy = 0.45))
        self.opt.append(MenuText('查看档案 [3]', 36, posy = 0.55))
        self.opt.append(MenuText('查看按键 [4]', 36, posy = 0.65))
        self.opt.append(MenuText('游戏信息 [5]', 36, posy = 0.75))
        self.esc = MenuText('退出游戏 [ESC]', 36, color = LIGHT_RED, posy = 0.9)
        spg.add(self.esc)
        for i in range(1, len(self.opt)):
            spg.add(self.opt[i])
        self.list.append(spg)

    def refresh(self, ctrl: Control):
        if ctrl.get_key(CTRL_ESC) or ctrl.get_click(self.esc.rect):
            return PAGE_EXIT
        if ctrl.get_key(CTRL_OPT[1]) or ctrl.get_click(self.opt[1].rect):
            init_game()
        elif ctrl.get_key(CTRL_OPT[2]) or ctrl.get_click(self.opt[2].rect):
            glb.pages.append(Page_Read())
        elif ctrl.get_key(CTRL_OPT[3]) or ctrl.get_click(self.opt[3].rect):
            glb.pages.append(Page_Achieve())
        elif ctrl.get_key(CTRL_OPT[4]) or ctrl.get_click(self.opt[4].rect):
            glb.pages.append(Page_Key())
        elif ctrl.get_key(CTRL_OPT[5]) or ctrl.get_click(self.opt[5].rect):
            glb.pages.append(Page_Info())
        return PAGE_NONE
