from .base import BaseSkill
from .skills_capacity import SkillsCapacity
from typing import Optional

__all__ = ("BaseSkill", "SkillsCapacity", "Skill")


class Skill:
    def __init__(self, skill_id: str, item_inv_id: Optional[str] = None) -> None:
        self.__cooldown = 0

        self.item_inv_id = item_inv_id
        self.skill_id = skill_id

    def __getitem__(self, name: str):
        skill = self.data
        if skill is None:
            if self.item_inv_id:
                raise ValueError(
                    f"Error: Invalid attack ID: {self.skill_id} in item ID {self.item_inv_id}"
                )
            raise ValueError(f"Error: Invalid attack ID: {self.skill_id}")
        if not hasattr(skill, name):
            raise ValueError(f"Error: Tidak ada artibut dengan nama {name}")
        return getattr(skill, name)

    @property
    def data(self):
        from .db import get_skill

        return get_skill(id=self.skill_id)

    @property
    def cooldown(self):
        return self.__cooldown

    def update_cooldown(self):
        if self.__cooldown != 0:
            self.__cooldown -= 1
