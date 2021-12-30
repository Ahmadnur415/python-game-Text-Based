from .. import interface, until, setup


max_level = setup.ENTITY["attribute"]["max_level"]

def levelUp(self):
    lv = 0

    while self.max_exp < self.exp and self.level < max_level:
        self.exp -= self.max_exp
        self.level += 1
        lv += 1

    if lv > 0:

        until.add_multiple_attributes(
            self,
            point_level=lv * 3,
            health=getattr(self, "max_health"),
            mana=getattr(self, "max_mana"),
            stamina=getattr(self, "max_stamina")
        )

        interface.centerprint(interface.get_messages("player.level_up").format(level=lv))
        interface.get_enter()
    return


def gain_exp(self, amount):
    self.exp += amount
    
    if self.exp > self.max_exp and self.level < max_level:
        return self.levelUp()


