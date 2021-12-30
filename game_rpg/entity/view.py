from ..import setup, interface


def view_stats(self):
    lines = {}
    distance = 3

    for stats in setup.ENTITY["stats"]:
        line = str(getattr(self, stats, 0))
        if stats in setup.ENTITY["entity_values"]["resource"]:
            line = str(getattr(self, stats, 0)) + " / " + str(getattr(self, "max_" + stats, 0))

        lines.update({interface.get_messages("view."+stats, stats): line})

    lines.update({
        "DAMAGE": "Magic ({}) physical ({})".format(" ~ ".join([str(i) for i in self.magic_damage]), " ~ ".join([str(i) for i in self.physical_damage])),
        interface.get_messages("view.critical_change", "C.Change"): str(self.critical_change),
        interface.get_messages("view.critical_hit", "C.Hit"): self.critical_hit,
        "Level": self.level
    })
    if self.namespace == "player":
        _exp = getattr(self, "exp", 0)
        _max_exp = getattr(self, "max_exp", 0)
        line = "0 / 0 | 0% (max)"
        if self.level < 60:
            line = str(_exp) + " / " + str(_max_exp) + " | " + str(round((100 * _exp) / _max_exp, 2)) + "%"

        lines.update({"Exp": line, "Gold": getattr(self, "gold", 0), "Silver": getattr(self, "silver", 0)})

    print(f"{self.name} Stats: ")
    interface.printData(
        lines, distance=distance
    )