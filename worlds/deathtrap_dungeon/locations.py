from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items

if TYPE_CHECKING:
    from .world import DeathtrapDungeonWorld

LOCATION_NAME_TO_ID = {
    "Starting Potion" : 1,
    "Idol's Left Eye" : 2,
    "Abandoned Backpack" : 3,
    "Slay the Dwarf" : 4,
    "Iron Grille - Loose" : 5,
    "Iron Grille - Leather Pouch" : 6,
    "Pit of Worms" : 7,
    "Trapdoor in the Sand" : 8,
    "Goblet of Red Liquid" : 9,
    "Demon Chair's Secret Panel" : 10,
    "Wooden Ball 1" : 11,
    "Wooden Ball 2" : 12,
    "Wooden Casket" : 13,
    "Wooden Box in the Iron Pipe 1" : 14,
    "Wooden Box in the Iron Pipe 2" : 15,
    "Shop in the Tunnel" : 16,
    "Hanging from an Iron Hook" : 17,
    "Slay Both Guard Dogs" : 18,
    "Ivy's Cupboard" : 19,
    "Taking the Ninja's Weapons" : 20,
    "Pole Across the Chasm" : 21,
    "Gift from the Booming Voice" : 22,
    "Slay the Orcs 1" : 23,
    "Slay the Orcs 2" : 24,
    "Gift from Sukumvit 1" : 25,
    "Gift from Sukumvit 2" : 26,
    "Skull's Left Eye" : 27,
    "Skull's Right Eye" : 28,
    "Gift from the Elf 1" : 29,
    "Gift from the Elf 2" : 30,
    "Gift from the Elf 3" : 31,
    "Gift from the Elf 4" : 32,
    "Bottom of the Pit" : 33,
    "Goblins' Cupboard 1" : 34,
    "Goblins' Cupboard 2" : 35,
    "Slay the Medusa" : 36,
    "Slay the Ninja" : 37,
    "Orc's Necklace" : 38,
    "Slay the Hobgoblins" : 39,
    "Starting Shield" : 40,
    "Meeting Horath" : 51,
    "Meeting Torgrim" : 52,
    "Meeting Thomas" : 53,
    "Meeting Ivy" : 54,
    "Meeting Ian Livingstone" : 55,
    "Meeting Igbut" : 56,
    "Meeting the Servant" : 57,
    "Meeting the Elf" : 61,
    "Meeting the Ninja" : 62,
    "Meeting the Knight" : 63,
    "Meeting Throm" : 64,
    "Meeting the Barbarian" : 65,
    "Using the Copper Key" : 71,
    "Using the Brass Key" : 72,
    "Game Over - Dying in the Arena of Death" : 101,
    "Game Over - Lacking a Jewel" : 102,
    "Game Over - Fifty-Metre Freefall" : 103,
    "Game Over - Crushing Defeat" : 104,
    "Game Over - Man in the Mirror" : 105,
    "Game Over - Hail Sukumvit" : 106,
    "Game Over - Stony Gaze" : 107,
    "Game Over - Poisoned Emerald" : 108,
    "Game Over - Another Stone for the Garden" : 109,
    "Game Over - The Bell Tolls for Thee" : 110,
    "Game Over - Chamber of the Dead" : 111,
    "Game Over - Between Troglodytes and the River" : 112,
    "Game Over - Food for the Bloodbeast" : 113,
    "Game Over - Drinking Acid" : 114,
    "Game Over - Eating the Mushrooms" : 115,
    "Game Over - Slain by the Rock Grub's Mate" : 116,
    "Game Over - Mirrored Headache" : 117,
    "Game Over - Knock-Knock" : 118,
    "Game Over - All Brawn and No Brain" : 119,
    "Game Over - Falling off the Tightrope" : 120,
    "Game Over - Too Hot to Handle" : 121,
    "Game Over - Crushed by the Boulder" : 122,
}

LOCATION_NAME_GROUPS = {
    "Game Over" : {name for name in LOCATION_NAME_TO_ID.keys() if LOCATION_NAME_TO_ID[name] > 100},
    "Trialmaster" : {name for name in LOCATION_NAME_TO_ID.keys() if 60 > LOCATION_NAME_TO_ID[name] > 50},
    "Champion" : {name for name in LOCATION_NAME_TO_ID.keys() if LOCATION_NAME_TO_ID[name] > 60},
}


class DeathtrapDungeonLocation(Location):
    game = "Deathtrap Dungeon"


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: DeathtrapDungeonWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: DeathtrapDungeonWorld) -> None:

    # Start with the always included locations
    add_locations_to_region(world, "Fenmarge", ["Slay Grimslade", "Gift from Grimslade"])
    add_locations_to_region(world, "Clearing 4", ["Gift from the Master of Wolves"])
    add_locations_to_region(world, "Clearing 5", ["Fallen Fighter"])
    add_locations_to_region(world, "Clearing 6", ["Slay the Dire Beast"])
    add_locations_to_region(world, "Clearing 9", ["Slay the Thief"])
    add_locations_to_region(world, "Clearing 14", ["Slay the Parrot", "Gift from the Mistress of Birds"])
    add_locations_to_region(world, "Clearing 16", ["Eagle's Nest"])
    add_locations_to_region(world, "Clearing 18", ["Slay the Sword Trees"])
    add_locations_to_region(world, "Clearing 19", ["Slay the Ranger"])
    add_locations_to_region(world, "Clearing 25", ["Slay the Pool Beast"])
    add_locations_to_region(world, "Clearing 29", ["Slay the Unicorn"])

    # Add the locations for the extra_locations option
    if world.options.extra_locations:
        add_locations_to_region(world, "Fenmarge", [
            "Game Over - A Hundred Pieces of Gold",
            "Game Over - Failing Selator's Quest",
            "Game Over - Itsy Bitsy Spider",
            "Game Over - Failing Poomchukker's Quest",
            "Game Over - Magic Carpet Ride",
            "Game Over - Grimslade's Trap",
            "Game Over - Out the Window and Into the Dungeons",
            "Game Over - Slain by Poomchukker's Guards",
            "Game Over - Explosion of Hellfire",
            "Game Over - Returning to Grimslade Empty-Handed"
        ])
        add_locations_to_region(world, "Clearing 1", ["Game Over - A Feast for Rats"])
        add_locations_to_region(world, "Clearing 14", ["Game Over - Curse of the Birds"])
        add_locations_to_region(world, "Clearing 17", [
            "Game Over - A Feast for the Spiders",
            "Game Over - The Master of Spiders Has No Friends"
        ])
        add_locations_to_region(world, "Clearing 20", ["Game Over - Crocodile Smile"])
        add_locations_to_region(world, "Clearing 33", ["Game Over - Dragged Down Into the River"])

    # Add the locations for the spellsanity option
    if world.options.spellsanity:
        add_locations_to_region(world, "Fenmarge", [
            "Selator's Spell Gem 1",
            "Selator's Spell Gem 2",
            "Selator's Spell Gem 3",
            "Selator's Spell Gem 4",
            "Selator's Spell Gem 5",
            "Selator's Spell Gem 6",
            "Selator's Spell Gem 7",
            "Selator's Spell Gem 8",
            "Selator's Spell Gem 9",
            "Poomchukker's Spell Gem 1",
            "Poomchukker's Spell Gem 2",
            "Poomchukker's Spell Gem 3",
            "Poomchukker's Spell Gem 4",
            "Poomchukker's Spell Gem 5",
            "Poomchukker's Spell Gem 6",
            "Grimslade's Spell Gem 1",
            "Grimslade's Spell Gem 2",
            "Grimslade's Spell Gem 3",
            "Grimslade's Spell Gem 4",
            "Grimslade's Spell Gem 5",
            "Grimslade's Spell Gem 6",
            "Grimslade's Spell Gem 7",
            "Grimslade's Spell Gem 8",
            "Grimslade's Spell Gem 9"
        ])
        add_locations_to_region(world, "Willowbend", [
            "Halicar's Shop 1",
            "Halicar's Shop 2",
            "Halicar's Shop 3",
            "Halicar's Shop 4",
            "Halicar's Shop 5",
            "Halicar's Shop 6"
        ])
        add_locations_to_region(world, "Clearing 27", [
            "Gift from the Master of Gardens 1",
            "Gift from the Master of Gardens 2",
            "Gift from the Master of Gardens 3"
        ])
        add_locations_to_region(world, "Clearing 29", [
            "Unicorn Clearing Spell Gem 1",
            "Unicorn Clearing Spell Gem 2"
        ])

    # add the locations for the clearingsanity option
    if world.options.clearingsanity:
        for i in range(1, 36):
            if i not in {2, 22, 31}:
                add_locations_to_region(world, f"Clearing {i}", [f"Clearing {i} Entered"])

    # add the locations for the wizardsanity option
    if world.options.wizardsanity:
        add_locations_to_region(world, "Fenmarge", [
            "Gronar - Directions to Selator",
            "Gronar - Directions to Poomchukker",
            "Gronar - Directions to Grimslade"
        ])



def add_locations_to_region(world: DeathtrapDungeonWorld, region: str, locations: list[str]) -> None:
    world.get_region(region).add_locations(get_location_names_with_ids(locations), DeathtrapDungeonLocation)


def create_events(world: DeathtrapDungeonWorld) -> None:

    add_events_to_region(world, "Fenmarge", {
        "Give Antherica to Selator" : "Selator Victory",
        "Give Map to Poomchukker" : "Poomchukker Victory",
        "Give Amulets to Grimslade" : "Grimslade Victory"
    })
    add_events_to_region(world, "Willowbend", {"Reach Willowbend" : "Map to Willowbend"})
    add_events_to_region(world, "Clearing 4", {"Slay the Master of Wolves" : "Wolf Amulet"})
    add_events_to_region(world, "Clearing 8", {"Rob the Master of Frogs" : "Frog Amulet"})
    add_events_to_region(world, "Clearing 11", {"Antherica Bush" : "Antherica Berry"})
    add_events_to_region(world, "Clearing 14", {"Negotiate with the Mistress of Birds" : "Bird Amulet"})
    add_events_to_region(world, "Clearing 17", {"Slay the Master of Spiders" : "Spider Amulet"})
    add_events_to_region(world, "Clearing 27", {"Slay the Master of Gardens" : "Flower Amulet"})


def add_events_to_region(world: DeathtrapDungeonWorld, region: str, events: dict[str,str]) -> None:
    for event in events:
        world.get_region(region).add_event(
            event, events[event], location_type=DeathtrapDungeonLocation, item_type=items.DeathtrapDungeonItem
        )
