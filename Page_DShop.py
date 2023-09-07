from Constant import *
from Menu import Background, MenuText
from Control import Control
from Page import Page
from SpriteGroup import SpriteGroup
from Drill import Drill
import Global as glb


class Page_DShop(Page):
    def __init__(self, dr: Drill, drill):
        super().__init__()
        self.dr, self.drill = dr, drill
        self.update_range = pg.Rect(0, 0, SCR_W, SCR_H)
        spg = SpriteGroup()
        self.list.append(Background())
        spg.add(MenuText('装备商店', 64, posy = 0.1))
        self.esc = MenuText('返回游戏 [ESC]', 36, color = LIGHT_RED, posy = 0.9)
        spg.add(self.esc)
        self.list.append(spg)
        self.opt = self.text = None
        self.update()

    def refresh(self, ctrl: Control):
        if ctrl.get_key(CTRL_ESC) or ctrl.get_click(self.esc.rect):
            return PAGE_EXIT
        for i in range(1, len(self.opt)):
            if self.opt[i] is None:
                continue
            if ctrl.get_key(CTRL_OPT[i]) or ctrl.get_click(self.opt[i].rect):
                self.upgrade(i)
        return PAGE_NONE

    def upgrade(self, idx):
        if idx == 1:    # rgd
            lv = self.dr.rgd_l
            cst = DRILL_COST['rgd'][lv]
            self.dr.money -= cst
            self.dr.rgd_l += 1
            self.drill.heads = self.drill.get_drill_sp(HEAD)
        elif idx == 2:
            lv = self.dr.h_l
            cst = DRILL_COST['h_max'][lv]
            self.dr.money -= cst
            self.dr.h_l += 1
            self.dr.h_max = DRILL_DATA['h_max'][lv + 1]
            self.drill.bodys = self.drill.get_drill_sp(BODY)
        elif idx == 3:
            lv = self.dr.g_l
            cst = DRILL_COST['g_max'][lv]
            self.dr.money -= cst
            self.dr.g_l += 1
            self.dr.g_max = DRILL_DATA['g_max'][lv + 1]
            self.drill.sflames = self.drill.get_drill_sp(SFLAME)
            self.drill.lflames = self.drill.get_drill_sp(LFLAME)
        elif idx == 4:
            lv = self.dr.p_l
            cst = DRILL_COST['p_max'][lv]
            self.dr.money -= cst
            self.dr.p_l += 1
            self.dr.p_max = DRILL_DATA['p_max'][lv + 1]
        elif idx == 5:
            lv = self.dr.o_l
            cst = DRILL_COST['o_max'][lv]
            self.dr.money -= cst
            self.dr.o_l += 1
            self.dr.o_max = DRILL_DATA['o_max'][lv + 1]
        elif idx == 6:
            lv = self.dr.eng_l
            cst = DRILL_COST['eng'][lv]
            self.dr.money -= cst
            self.dr.eng_l += 1
        upgrade_sound.play()
        self.update()

    def draw(self, scr):
        for obj in self.list:
            obj.draw(scr)
        self.text.draw(scr)
        for i in range(1, len(self.opt)):
            if self.opt[i] is not None:
               self.opt[i].draw(scr)

    def update(self, font_sz = 24):
        self.opt = [None]
        self.text = SpriteGroup()
        self.text.add(MenuText(f'金钱：{self.dr.money}', font_sz, posx = 0.8, posy = 0.1))

        self.opt.append(None)
        lv, pct = self.dr.rgd_l, 0.24
        cur = DRILL_DATA['rgd'][lv]
        self.text.add(MenuText(f'升级钻头', font_sz, posx = 0.1, posy = pct))
        self.text.add(MenuText(f'当前硬度 {cur}', font_sz, color = DRILL_LEVEL_COLOR[lv], posx = 0.3, posy = pct))
        if lv < DRILL_LEVEL_MAX:
            nxt, cst = DRILL_DATA['rgd'][lv + 1], DRILL_COST["rgd"][lv]
            self.text.add(MenuText(f'下一硬度 {nxt}', font_sz, color = DRILL_LEVEL_COLOR[lv + 1], posx = 0.5, posy = pct))
            self.text.add(MenuText(f'花费 {cst}', font_sz, posx = 0.7, posy = pct))
            if self.dr.money < cst:
                self.text.add(MenuText(f'金钱不足', font_sz, color = LIGHT_RED, posx = 0.9, posy = pct))
            else:
                self.opt[-1] = MenuText(f'升级', font_sz, color = LIGHT_GREEN, posx = 0.9, posy = pct)
        else:
            self.text.add(MenuText(f'已满级', font_sz, color = DRILL_LEVEL_COLOR[lv], posx = 0.9, posy = pct))

        self.opt.append(None)
        lv, pct = self.dr.h_l, 0.35
        cur = DRILL_DATA['h_max'][lv]
        self.text.add(MenuText(f'升级车身', font_sz, posx = 0.1, posy = pct))
        self.text.add(MenuText(f'当前血量 {cur}', font_sz, color = DRILL_LEVEL_COLOR[lv], posx = 0.3, posy = pct))
        if lv < DRILL_LEVEL_MAX:
            nxt, cst = DRILL_DATA['h_max'][lv + 1], DRILL_COST["h_max"][lv]
            self.text.add(MenuText(f'下一血量 {nxt}', font_sz, color = DRILL_LEVEL_COLOR[lv + 1], posx = 0.5, posy = pct))
            self.text.add(MenuText(f'花费 {cst}', font_sz, posx = 0.7, posy = pct))
            if self.dr.money < cst:
                self.text.add(MenuText(f'金钱不足', font_sz, color = LIGHT_RED, posx = 0.9, posy = pct))
            else:
                self.opt[-1] = MenuText(f'升级', font_sz, color = LIGHT_GREEN, posx = 0.9, posy = pct)
        else:
            self.text.add(MenuText(f'已满级', font_sz, color = DRILL_LEVEL_COLOR[lv], posx = 0.9, posy = pct))

        self.opt.append(None)
        lv, pct = self.dr.g_l, 0.46
        cur = DRILL_DATA['g_max'][lv]
        self.text.add(MenuText(f'升级氮气箱', font_sz, posx = 0.1, posy = pct))
        self.text.add(MenuText(f'当前容量 {cur}', font_sz, color = DRILL_LEVEL_COLOR[lv], posx = 0.3, posy = pct))
        if lv < DRILL_LEVEL_MAX:
            nxt, cst = DRILL_DATA['g_max'][lv + 1], DRILL_COST["g_max"][lv]
            self.text.add(MenuText(f'下一容量 {nxt}', font_sz, color = DRILL_LEVEL_COLOR[lv + 1], posx = 0.5, posy = pct))
            self.text.add(MenuText(f'花费 {cst}', font_sz, posx = 0.7, posy = pct))
            if self.dr.money < cst:
                self.text.add(MenuText(f'金钱不足', font_sz, color = LIGHT_RED, posx = 0.9, posy = pct))
            else:
                self.opt[-1] = MenuText(f'升级', font_sz, color = LIGHT_GREEN, posx = 0.9, posy = pct)
        else:
            self.text.add(MenuText(f'已满级', font_sz, color = DRILL_LEVEL_COLOR[lv], posx = 0.9, posy = pct))

        self.opt.append(None)
        lv, pct = self.dr.p_l, 0.57
        cur = DRILL_DATA['p_max'][lv]
        self.text.add(MenuText(f'升级燃油箱', font_sz, posx = 0.1, posy = pct))
        self.text.add(MenuText(f'当前容量 {cur}', font_sz, color = DRILL_LEVEL_COLOR[lv], posx = 0.3, posy = pct))
        if lv < DRILL_LEVEL_MAX:
            nxt, cst = DRILL_DATA['p_max'][lv + 1], DRILL_COST["p_max"][lv]
            self.text.add(MenuText(f'下一容量 {nxt}', font_sz, color = DRILL_LEVEL_COLOR[lv + 1], posx = 0.5, posy = pct))
            self.text.add(MenuText(f'花费 {cst}', font_sz, posx = 0.7, posy = pct))
            if self.dr.money < cst:
                self.text.add(MenuText(f'金钱不足', font_sz, color = LIGHT_RED, posx = 0.9, posy = pct))
            else:
                self.opt[-1] = MenuText(f'升级', font_sz, color = LIGHT_GREEN, posx = 0.9, posy = pct)
        else:
            self.text.add(MenuText(f'已满级', font_sz, color = DRILL_LEVEL_COLOR[lv], posx = 0.9, posy = pct))

        self.opt.append(None)
        lv, pct = self.dr.o_l, 0.68
        cur = DRILL_DATA['o_max'][lv]
        self.text.add(MenuText(f'升级矿石箱', font_sz, posx = 0.1, posy = pct))
        self.text.add(MenuText(f'当前容量 {cur}', font_sz, color = DRILL_LEVEL_COLOR[lv], posx = 0.3, posy = pct))
        if lv < DRILL_LEVEL_MAX:
            nxt, cst = DRILL_DATA['o_max'][lv + 1], DRILL_COST["o_max"][lv]
            self.text.add(MenuText(f'下一容量 {nxt}', font_sz, color = DRILL_LEVEL_COLOR[lv + 1], posx = 0.5, posy = pct))
            self.text.add(MenuText(f'花费 {cst}', font_sz, posx = 0.7, posy = pct))
            if self.dr.money < cst:
                self.text.add(MenuText(f'金钱不足', font_sz, color = LIGHT_RED, posx = 0.9, posy = pct))
            else:
                self.opt[-1] = MenuText(f'升级', font_sz, color = LIGHT_GREEN, posx = 0.9, posy = pct)
        else:
            self.text.add(MenuText(f'已满级', font_sz, color = DRILL_LEVEL_COLOR[lv],posx = 0.9, posy = pct))

        self.opt.append(None)
        lv, pct = self.dr.eng_l, 0.79
        cur = DRILL_DATA['eng'][lv]
        self.text.add(MenuText(f'升级引擎', font_sz, posx = 0.1, posy = pct))
        self.text.add(MenuText(f'当前等级 {cur}', font_sz, color = DRILL_LEVEL_COLOR[lv], posx = 0.3, posy = pct))
        if lv < DRILL_LEVEL_MAX:
            nxt, cst = DRILL_DATA['eng'][lv + 1], DRILL_COST["eng"][lv]
            self.text.add(MenuText(f'下一等级 {nxt}', font_sz, color = DRILL_LEVEL_COLOR[lv + 1], posx = 0.5, posy = pct))
            self.text.add(MenuText(f'花费 {cst}', font_sz, posx = 0.7, posy = pct))
            if self.dr.money < cst:
                self.text.add(MenuText(f'金钱不足', font_sz, color = LIGHT_RED, posx = 0.9, posy = pct))
            else:
                self.opt[-1] = MenuText(f'升级', font_sz, color = LIGHT_GREEN, posx = 0.9, posy = pct)
        else:
            self.text.add(MenuText(f'已满级', font_sz, color = DRILL_LEVEL_COLOR[lv], posx = 0.9, posy = pct))
