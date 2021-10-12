from .. import interface


def view_attack(self):
    new_line = "\n" + " " * 3 + " ~ "
    for i, attack in enumerate(self.attack):
        line = " " + str(i + 1) + " : " + attack.displayName
        if attack.cost_st > 0:
            line += new_line + interface.get_messages("attack.stamina_cost_template").format(cost=attack.cost_st)
        if attack.cost_mp > 0:
            line += new_line + interface.get_messages("attack.mana_cost_template").format(cost=attack.cost_mp)

        print(line)


@property
def attack_name(self):
    return [attack.name for attack in self.attack]


def get_attack_from_name(self, name: str):
    for attack in self.attack:
        if attack.name == name:
            return attack