from time import struct_time
from time import time
from typing import Optional
import bz2
import pickle
import gc


class Race:
    def __init__(self, name, variant=None, setting='Forgotten Realms', ua=False, customized=False, note=None,
                 archived=False):
        self.name = name
        self.variant = variant
        self.setting = setting
        self.ua = ua
        self.customized = customized
        self.archived = archived
        self.note = note

    def __repr__(self):
        return f'{self.name}{"(CUSTOM)" if self.customized else ""}'


class Background:
    SEPARATE_ON_TAGS = True

    def __init__(self, name, setting='Forgotten Realms', ua=False, customized=False, variant=None, notes=''):
        self.name = name
        self.setting = setting
        self.ua = ua
        self.customized = customized
        self.variant = variant
        self.notes = notes

    def __eq__(self, other):
        if not self.SEPARATE_ON_TAGS:
            return self.name == other.name
        return self.name == other.name and self.ua == other.ua and self.variant == other.variant and not self.customized

    @classmethod
    def set_separate_on_tags(cls, value):
        cls.SEPARATE_ON_TAGS = value

    def __repr__(self):
        return f'{self.name}{"(custom)" if self.customized else ""}'


class Feat:
    SEPARATE_ON_TAGS = True

    def __init__(self, name, setting: str = 'Forgotten Realms', ua: bool = False, archived: bool = False,
                 customized: bool = False, race: list = None, choice: str = None, original_name=''):
        self.name = name
        self.setting = setting
        self.ua = ua
        self.archived = archived
        self.customized = customized
        self.race = race
        self.choice = choice
        self.original_name = original_name

    def __eq__(self, other):
        if not self.SEPARATE_ON_TAGS:
            return self.name == other.name
        s_race = self.race or []
        o_race = other.race or []
        return self.name == other.name and self.ua == other.ua and self.archived == other.archived and sorted(
            s_race) == sorted(o_race) and not self.customized and not other.customized

    @classmethod
    def set_separate_on_tags(cls, value):
        cls.SEPARATE_ON_TAGS = value

    def __hash__(self):
        if not self.SEPARATE_ON_TAGS:
            return hash(self.name)
        extra = ''
        if self.customized:  # choice is not included
            extra = time()
        return hash(self.name + str(self.ua) + str(self.archived) + str(self.race) + str(extra))

    def __repr__(self):
        if not self.customized:
            return f'{self.name} (UA: {self.ua}, Archived: {self.archived})'
        return f'[CUSTOM] {self.name}'


class Item:
    def __init__(self, name, bonus=None, value_gp=None, base_item=None, special=''):
        self.name = name
        self.bonus = bonus
        self.value_gp = value_gp
        self.special = special
        self.base_item = base_item

    def __repr__(self):
        return f'{self.name}{"(" + self.value_gp + "gp)" if isinstance(self.value_gp, int) else ""}'


class CharacterClass:
    SEPARATE_ON_TAGS = True

    def __init__(self, name, subclass=None, ua_class=False, ua_subclass=False, archived_class=False,
                 archived_subclass=False,
                 class_notes='', subclass_notes='', class_setting='Forgotten Realms',
                 subclass_setting='Forgotten Realms',
                 class_customized=False, subclass_customized=False, **kwargs):
        if subclass == '':
            subclass = None
        self.name = name
        self.subclass = subclass
        # specifics of tags
        self.ua_class = ua_class
        self.ua_subclass = ua_subclass
        self.archived_class = archived_class
        self.archived_subclass = archived_subclass
        # extra
        self.class_setting = class_setting
        self.subclass_setting = subclass_setting
        self.class_customized = class_customized
        self.subclass_customized = subclass_customized
        self.class_notes = class_notes
        self.subclass_notes = subclass_notes

    def __repr__(self):
        return f'{self.name}{"(" + self.subclass + ")" if self.subclass != "" and self.subclass is not None else ""}'

    def __eq__(self, other):
        if self.SEPARATE_ON_TAGS:
            return self.__dict__ == other.__dict__
        return self.name == other.name and self.subclass == other.subclass

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        if self.SEPARATE_ON_TAGS:
            return hash(''.join([str(q) for q in sorted(self.__dict__.items()) if '__' not in q[0]]))
        ss = self.name
        if self.subclass != None:
            ss += self.subclass
        return hash(ss)

    @classmethod
    def set_separate_on_tags(cls, value):
        cls.SEPARATE_ON_TAGS = value


class Character:
    def __init__(self, num: int, char_id: int, name: str, base_hp: int, strength: int, dexterity: int,
                 constitution: int, intelligence: int, wisdom: int, charisma: int, background: Optional[Background],
                 race: Race, feats: list[Feat], inventory: list[Item], date_modified: struct_time, notes_len: int,
                 # todo int
                 gold: float, base_class: CharacterClass, extra_classes: list[CharacterClass], total_level: int,
                 base_level: int):
        self.num = int(num)
        self.char_id = int(char_id)
        self.name = name
        self.base_hp = int(base_hp)
        self.strength = int(strength)
        self.dexterity = int(dexterity)
        self.constitution = int(constitution)
        self.intelligence = int(intelligence)
        self.wisdom = int(wisdom)
        self.charisma = int(charisma)
        self.background = background
        self.race = race
        self.feats = feats
        self.inventory = inventory
        self.date_modified = date_modified
        self.notes_len = notes_len
        self.gold = gold
        self.base_class = base_class
        self.extra_classes = extra_classes
        self.base_level = base_level
        self.total_level = total_level

    def __repr__(self):
        extra = ''
        if self.extra_classes.__len__() > 0:
            extra = f' / {", ".join([str(q) for q in self.extra_classes])} ({self.total_level})'
        return f'{self.name}: {self.base_class} ({self.base_level}) {extra}'


def load_dataset():
    with bz2.BZ2File('characters.pcl.bz2', 'rb') as f:
        gc.disable()
        data = pickle.load(f)
        gc.enable()
    return data


if __name__ == '__main__':
    data = load_dataset()
