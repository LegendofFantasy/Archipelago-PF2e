from dataclasses import dataclass

from Options import OptionGroup, PerGameCommonOptions, ItemDict, Toggle, Range


class Trialmastersanity(Toggle):
    """
    Adds all the Trialmasters to the item pool. You will need their respective items for them to appear in the game.
    A location will be added for meeting each one for the first time.
    """

    display_name = "Trialmastersanity"


class Championsanity(Toggle):
    """
    Adds all the other Champions to the item pool. You will need their respective items for them to appear in the game.
    A location will be added for meeting each one for the first time.
    """

    display_name = "Championsanity"

class ShufflePotion(Toggle):
    """
    Shuffles the potion you start the game with, creating a new location that you will get right away. The potion added
    to the pool will be selected randomly.
    """

    display_name = "Shuffle Potion"

class ShuffleShield(Toggle):
    """
    Shuffles the shield you start the game with, creating a new location that you will get right away.
    """

    display_name = "Shuffle Shield"

class GemHunt(Toggle):
    """
    Adds a requirement that you have all the gems available in the game (the always required Emerald, Sapphire, and
    Diamond as well as the usually unnecessary Pearl, Topaz, Ruby, and Garnet) in order to reach the goal.
    """

    display_name = "Gem Hunt"

class PackSize(Range):
    """
    Sets the amount of provisions that you will get when you receive a "Pack of Provisions" item. If you make this
    value negative, Packs of Provisions will be classified as traps instead of filler.
    """

    display_name = "Pack Size"
    range_start = -10
    range_end = 10
    default = 2


class ExtraLocations(Toggle):
    """
    Adds additional locations for reaching all the bad endings in the game aside from running out of Stamina.

    If Progressive Statistics is on, this will be forced on as well.
    """

    display_name = "Extra Locations"


class ProgressiveStats(Toggle):
    """
    Adds additional items to the item pool that increase the minimum values of each of your stats at the beginning
    of each run. For example, if you have three Progressive Skill items your Skill will be in the range of 10-12
    instead of 7-12.

    If this setting is on, Extra Locations will be forced on as well regardless of your settings to accommodate the
    additional items.
    """

    display_name = "Progressive Statistics"


class FillerWeights(ItemDict):
    """
    For any filler items that are added, these are the weights that each choice will be added. Any of the game's items
    can be added to this list if desired. Leave it as the default if you don't know what you're doing.

    If all weights are 0, the filler items will all be Packs of Provisions.
    """

    display_name = "Filler Weights"

    default = {
        "Pack of Provisions" : 1
    }


@dataclass
class DeathtrapDungeonOptions(PerGameCommonOptions):
    pack_size : PackSize
    gem_hunt : GemHunt
    shuffle_shield : ShuffleShield
    shuffle_potion : ShufflePotion
    trialmastersanity : Trialmastersanity
    championsanity : Championsanity
    extra_locations : ExtraLocations
    progressive_stats : ProgressiveStats
    filler_weights : FillerWeights


option_groups = [
    OptionGroup(
        "Goal Options",
        [GemHunt],
    ),
    OptionGroup(
        "Location Options",
        [Trialmastersanity, Championsanity, ShuffleShield, ShufflePotion, ExtraLocations],
    ),
    OptionGroup(
        "Item Options",
        [ProgressiveStats, PackSize, FillerWeights],
    ),
]

option_presets = {
    "Recommended": {
        "pack_size": 2,
        "gem_hunt": True,
        "shuffle_shield": True,
        "shuffle_potion": True,
        "trialmastersanity": True,
        "championsanity": True,
        "extra_locations": True,
        "progressive_stats": True,
        "filler_weights": FillerWeights.default,
    },
}
