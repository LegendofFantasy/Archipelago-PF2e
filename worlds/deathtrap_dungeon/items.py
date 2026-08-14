from __future__ import annotations

import collections
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import DeathtrapDungeonWorld

ITEM_NAME_TO_ID = {
    "Pack of Provisions" : 1,
    "Potion of Skill" : 2,
    "Potion of Strength" : 3,
    "Potion of Fortune" : 4,
    "Progressive Skill" : 5,
    "Progressive Stamina" : 6,
    "Progressive Luck" : 7,
    "Iron Key" : 10,
    "Emerald" : 11,
    "Gold Piece" : 12,
    "Chainmail" : 13,
    "Sapphire" : 14,
    "Grappling Iron" : 15,
    "Brass Bell" : 16,
    "Hollow Wooden Tube" : 17,
    "Ring of Wishes" : 18,
    "Dagger" : 19,
    "Shield" : 20,
    "Goblet" : 21,
    "Doppelganger Potion" : 22,
    "Bone Monkey Charm" : 23,
    "Wooden Ball" : 24,
    "Pearl" : 25,
    "Bamboo Stilts" : 26,
    "Rope" : 27,
    "Leprechaun Tooth" : 28,
    "Old Bone" : 29,
    "Ninja's Weapons" : 30,
    "Winged Helmet" : 31,
    "Topaz" : 32,
    "Mirror" : 33,
    "Ruby" : 34,
    "Wooden Mallet" : 35,
    "Iron Spikes" : 36,
    "Garnet" : 37,
    "Diamond" : 38,
    "Necklace" : 39,
    "Jug of Acid" : 40,
    "Horath" : 51,
    "Torgrim" : 52,
    "Thomas" : 53,
    "Ivy" : 54,
    "Ian Livingstone" : 55,
    "Igbut" : 56,
    "Servant of the Trialmasters" : 57,
    "Elf" : 61,
    "Ninja" : 62,
    "Knight" : 63,
    "Throm" : 64,
    "Barbarian" : 65,
}

ITEM_NAME_GROUPS = {
    "Progressive Statistic" : {"Progressive Skill", "Progressive Stamina", "Progressive Luck"},
    "Progressive Stat" : {"Progressive Skill", "Progressive Stamina", "Progressive Luck"},
    "Trialmaster" : {name for name in ITEM_NAME_TO_ID.keys() if 60 > ITEM_NAME_TO_ID[name] > 50},
    "Champion" : {name for name in ITEM_NAME_TO_ID.keys() if ITEM_NAME_TO_ID[name] > 60}
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Pack of Provisions" : ItemClassification.filler,
    "Potion of Skill" : ItemClassification.filler,
    "Potion of Strength" : ItemClassification.filler,
    "Potion of Fortune" : ItemClassification.filler,
    "Progressive Skill" : ItemClassification.useful,
    "Progressive Stamina" : ItemClassification.useful,
    "Progressive Luck" : ItemClassification.useful,
    "Iron Key" : ItemClassification.progression,
    "Emerald" : ItemClassification.progression_skip_balancing,
    "Gold Piece" : ItemClassification.progression_deprioritized,
    "Chainmail" : ItemClassification.filler,
    "Sapphire" : ItemClassification.progression_skip_balancing,
    "Grappling Iron" : ItemClassification.useful,
    "Brass Bell" : ItemClassification.filler,
    "Hollow Wooden Tube" : ItemClassification.useful,
    "Ring of Wishes" : ItemClassification.useful,
    "Dagger" : ItemClassification.useful,
    "Shield" : ItemClassification.useful,
    "Goblet" : ItemClassification.filler,
    "Doppelganger Potion" : ItemClassification.useful,
    "Bone Monkey Charm" : ItemClassification.useful,
    "Wooden Ball" : ItemClassification.filler,
    "Pearl" : ItemClassification.filler,
    "Bamboo Stilts" : ItemClassification.useful,
    "Rope" : ItemClassification.useful,
    "Leprechaun Tooth" : ItemClassification.filler,
    "Old Bone" : ItemClassification.useful,
    "Ninja's Weapons" : ItemClassification.filler,
    "Winged Helmet" : ItemClassification.filler,
    "Topaz" : ItemClassification.filler,
    "Mirror" : ItemClassification.filler,
    "Ruby" : ItemClassification.filler,
    "Wooden Mallet" : ItemClassification.filler,
    "Iron Spikes" : ItemClassification.filler,
    "Garnet" : ItemClassification.filler,
    "Diamond" : ItemClassification.progression_skip_balancing,
    "Necklace" : ItemClassification.filler,
    "Jug of Acid" : ItemClassification.useful,
    "Horath" : ItemClassification.progression,
    "Torgrim" : ItemClassification.progression,
    "Thomas" : ItemClassification.progression,
    "Ivy" : ItemClassification.progression,
    "Ian Livingstone" : ItemClassification.progression,
    "Igbut" : ItemClassification.progression,
    "Servant of the Trialmasters" : ItemClassification.progression,
    "Elf" : ItemClassification.progression,
    "Ninja" : ItemClassification.progression,
    "Knight" : ItemClassification.progression,
    "Throm" : ItemClassification.progression,
    "Barbarian" : ItemClassification.progression,
}


class DeathtrapDungeonItem(Item):
    game = "Deathtrap Dungeon"


def get_random_filler_item_name(world: DeathtrapDungeonWorld) -> str:

    filler_names = sorted(collections.Counter(world.options.filler_weights.value).elements())
    if filler_names:
        return world.random.choice(filler_names)
    return "Pack of Provisions"


def create_item_with_correct_classification(world: DeathtrapDungeonWorld, name: str) -> DeathtrapDungeonItem:

    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    if name == "Pack of Provisions" and world.options.pack_size.value < 0:
        classification = ItemClassification.trap

    if name in {"Pearl", "Topaz", "Ruby", "Garnet"} and world.options.gem_hunt:
        classification = ItemClassification.progression_deprioritized_skip_balancing

    return DeathtrapDungeonItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: DeathtrapDungeonWorld) -> None:

    itempool: list[Item] = [
        world.create_item("Golden Magnet"),
        world.create_item("Violet Jewel"),
        world.create_item("Secret Word"),
        world.create_item("Gold Chain"),
        world.create_item("Magic Sword"),
        world.create_item("Horn of a Unicorn"),
        world.create_item("Magic Potion"),
        world.create_item("Ranger's Helmet"),
        world.create_item("Sword Tree Seeds"),
        world.create_item("Red Cloak"),
        world.create_item("Great Magic Sword"),
        world.create_item("Parrot Feathers"),
        world.create_item("Dire Beast Claws"),
    ]

    if world.options.progressive_stats:
        itempool.extend([
            world.create_item("Progressive Skill"),
            world.create_item("Progressive Skill"),
            world.create_item("Progressive Skill"),
            world.create_item("Progressive Skill"),
            world.create_item("Progressive Skill"),
            world.create_item("Progressive Stamina"),
            world.create_item("Progressive Stamina"),
            world.create_item("Progressive Stamina"),
            world.create_item("Progressive Stamina"),
            world.create_item("Progressive Stamina"),
            world.create_item("Progressive Luck"),
            world.create_item("Progressive Luck"),
            world.create_item("Progressive Luck"),
            world.create_item("Progressive Luck"),
            world.create_item("Progressive Luck"),
        ])

    if world.options.spellsanity:
        itempool.extend([
            world.create_item("Skill Spell Gem"),
            world.create_item("Skill Spell Gem"),
            world.create_item("Skill Spell Gem"),
            world.create_item("Stamina Spell Gem"),
            world.create_item("Stamina Spell Gem"),
            world.create_item("Stamina Spell Gem"),
            world.create_item("Luck Spell Gem"),
            world.create_item("Luck Spell Gem"),
            world.create_item("Luck Spell Gem"),
            world.create_item("Luck Spell Gem"), # extra from Unicorn clearing
            world.create_item("Fire Spell Gem"),
            world.create_item("Fire Spell Gem"),
            world.create_item("Fire Spell Gem"),
            world.create_item("Ice Spell Gem"),
            world.create_item("Ice Spell Gem"),
            world.create_item("Ice Spell Gem"),
            world.create_item("Illusion Spell Gem"),
            world.create_item("Illusion Spell Gem"),
            world.create_item("Illusion Spell Gem"),
            world.create_item("Friendship Spell Gem"),
            world.create_item("Friendship Spell Gem"),
            world.create_item("Friendship Spell Gem"),
            world.create_item("Friendship Spell Gem"), # extra from Unicorn clearing
            world.create_item("Growth Spell Gem"),
            world.create_item("Growth Spell Gem"),
            world.create_item("Growth Spell Gem"),
            world.create_item("Bless Spell Gem"),
            world.create_item("Bless Spell Gem"),
            world.create_item("Bless Spell Gem"),
            world.create_item("Fear Spell Gem"),
            world.create_item("Fear Spell Gem"),
            world.create_item("Withering Spell Gem"),
            world.create_item("Withering Spell Gem"),
            world.create_item("Curse Spell Gem"),
            world.create_item("Curse Spell Gem"),
        ])

    if world.options.clearingsanity:
        itempool.extend([
            world.create_item("Clearing 3"),
            world.create_item("Clearing 4"),
            world.create_item("Clearing 5"),
            world.create_item("Clearing 6"),
            world.create_item("Clearing 7"),
            world.create_item("Clearing 8"),
            world.create_item("Clearing 9"),
            world.create_item("Clearing 10"),
            world.create_item("Clearing 11"),
            world.create_item("Clearing 12"),
            world.create_item("Clearing 13"),
            world.create_item("Clearing 14"),
            world.create_item("Clearing 15"),
            world.create_item("Clearing 16"),
            world.create_item("Clearing 17"),
            world.create_item("Clearing 18"),
            world.create_item("Clearing 19"),
            world.create_item("Clearing 20"),
            world.create_item("Clearing 21"),
            world.create_item("Clearing 23"),
            world.create_item("Clearing 24"),
            world.create_item("Clearing 25"),
            world.create_item("Clearing 26"),
            world.create_item("Clearing 27"),
            world.create_item("Clearing 28"),
            world.create_item("Clearing 29"),
            world.create_item("Clearing 30"),
            world.create_item("Clearing 32"),
            world.create_item("Clearing 33"),
            world.create_item("Clearing 34"),
            world.create_item("Clearing 35"),
        ])

    if world.options.wizardsanity:
        itempool.extend([
            world.create_item(i) for i in ["Selator", "Poomchukker", "Grimslade"] if i != world.starting_wizard
        ])
        world.push_precollected(world.create_item(world.starting_wizard))

    filler_count = len(world.multiworld.get_unfilled_locations(world.player)) - len(itempool)

    itempool += [world.create_filler() for _ in range(filler_count)]

    world.multiworld.itempool += itempool
