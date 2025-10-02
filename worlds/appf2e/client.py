# Most of this code is sourced from the League of Legends APWorld found at: https://github.com/gaithernOrg/LoLAP and has
# been edited to fit my needs.

from __future__ import annotations
import os
import sys
import asyncio
import shutil
import requests
import json

import ModuleUpdate
ModuleUpdate.update()

import Utils

from worlds.appf2e.world import APPF2eWorld

check_num = 0

###Set up game communication path###
game_communication_path = os.path.expandvars(APPF2eWorld.settings["connections_directory"])
if not os.path.exists(game_communication_path):
    os.makedirs(game_communication_path)


###Client###
if __name__ == "__main__":
    Utils.init_logging("APPF2eClient", exception_logger="Client")

from NetUtils import NetworkItem, ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop


def check_stdin() -> None:
    if Utils.is_windows and sys.stdin:
        print("WARNING: Console input is not routed reliably on Windows, use the GUI instead.")

class APPF2eClientCommandProcessor(ClientCommandProcessor):
    pass

class APPF2eContext(CommonContext):
    command_processor: int = APPF2eClientCommandProcessor
    game = "AP Test"
    items_handling = 0b111  # full remote

    def __init__(self, server_address, password):
        super(APPF2eContext, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        # self.game_communication_path: files go in this path to pass data between us and the actual game
        self.game_communication_path = os.path.expandvars(APPF2eWorld.settings["connections_directory"])
        if not os.path.exists(self.game_communication_path):
            os.makedirs(self.game_communication_path)
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root+"/"+file)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(APPF2eContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(APPF2eContext, self).connection_closed()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root + "/" + file)

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(APPF2eContext, self).shutdown()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root+"/"+file)

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            if not os.path.exists(self.game_communication_path):
                os.makedirs(self.game_communication_path)
            for ss in self.checked_locations:
                filename = f"send{ss}"
                with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                    f.close()
            #Handle Slot Data
            for slot_data_key in list(args['slot_data'].keys()):
                with open(os.path.join(self.game_communication_path, slot_data_key.replace(" ", "_") + ".cfg"), 'w') as f:
                    f.write(str(args['slot_data'][slot_data_key]))
                    f.close()
            #End Handle Slot Data
            
        if cmd in {"ReceivedItems"}:
            start_index = args["index"]
            if start_index != len(self.items_received):
                for item in args['items']:
                    check_num = 0
                    for filename in os.listdir(self.game_communication_path):
                        if filename.startswith("AP"):
                            if int(filename.split("_")[-1].split(".")[0]) > check_num:
                                check_num = int(filename.split("_")[-1].split(".")[0])
                    item_id = ""
                    location_id = ""
                    player = ""
                    found = False
                    for filename in os.listdir(self.game_communication_path):
                        if filename.startswith(f"AP"):
                            with open(os.path.join(self.game_communication_path, filename), 'r') as f:
                                item_id = str(f.readline()).replace("\n", "")
                                location_id = str(f.readline()).replace("\n", "")
                                player = str(f.readline()).replace("\n", "")
                                if str(item_id) == str(NetworkItem(*item).item) and str(location_id) == str(NetworkItem(*item).location) and str(player) == str(NetworkItem(*item).player) and int(location_id) > 0:
                                    found = True
                    if not found:
                        filename = f"AP_{str(check_num+1)}.item"
                        with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                            f.write(str(NetworkItem(*item).item) + "\n" + str(NetworkItem(*item).location) + "\n" + str(NetworkItem(*item).player))
                            f.close()

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                for ss in self.checked_locations:
                    filename = f"send{ss}"
                    with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                        f.close()

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class APPF2eManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago AP Pathfinder 2e Client"

        self.ui = APPF2eManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def game_watcher(ctx: APPF2eContext):
    # from worlds.appf2e.locations import lookup_id_to_name
    while not ctx.exit_event.is_set():
        if ctx.syncing == True:
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        sending = []
        victory = False
        for root, dirs, files in os.walk(ctx.game_communication_path):
            for file in files:
                if file.find("send") > -1:
                    st = file.split("send", -1)[1]
                    if st != "nil":
                        sending = sending+[(int(st))]
                if file.find("victory") > -1:
                    victory = True
        ctx.locations_checked = sending
        message = [{"cmd": 'LocationChecks', "locations": sending}]
        await ctx.send_msgs(message)
        if not ctx.finished_game and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)


def launch_ap_pf2e_client():
    async def main(args):
        ctx = APPF2eContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="APPF2eProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="AP Pathfinder 2e Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
