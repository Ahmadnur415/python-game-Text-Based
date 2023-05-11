from ..utils import clamp


def generate_value_property(name):
    @property
    def value_property(self):
        return getattr(self, "base_" + name)

    @value_property.setter
    def value_property(self, v):
        max_v = getattr(self, "max_" + name)
        v = clamp(v, 0, max_v)
        setattr(self, "base_" + name, v)

    return value_property


def generate_missing_value_property(name):
    @property
    def value_property(self):
        return getattr(self, "max_" + name) - getattr(self, name)

    @value_property.setter
    def value_property(self, v):
        pass

    return value_property


def generate_level_property():
    @property
    def value_property(self):
        if not hasattr(self, "_base_level"):
            self._base_level = 0
        return self._base_level

    @value_property.setter
    def value_property(self, n: int):
        lv = self.level
        mlv = self.max_level
        n = clamp(n, lv, mlv)
        self._base_level = n

        level_up = self._base_level - lv
        if level_up > 0:
            point = 5 * level_up
            self.point_level += point

    return value_property


def generate_point_level_property():
    @property
    def value_property(self):
        if not hasattr(self, "_base_point_level"):
            self._base_point_level = 0
        return self._base_point_level

    @value_property.setter
    def value_property(self, n: int):
        self._base_point_level = clamp(n, 0, self.level * 5)

    return value_property


def generate_exp_property():
    @property
    def value_property(self):
        if not hasattr(self, "_base_exp"):
            self._base_exp = 0
        return self._base_exp

    @value_property.setter
    def value_property(self, n: int):
        self._base_exp = n
        # if self._base_exp >= self.max_exp:
        #     pass

    return value_property
