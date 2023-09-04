from osu_db import OsuDb

import json
import sys

def read_db(args):
    print("Loading database... (This will hang for a bit)")
    osu_data = OsuDb.from_file(args["database"]).beatmaps
    if args["sort_by_id"]:
        print("sorting...")
        osu_data.sort(key=lambda x: x.beatmap_set_id)
    print("Loaded database.")
    jsondata = []
    for beatmap in osu_data:
        try:
            if beatmap.gameplay_mode != 0:
                continue
            jsonbeatmap = {}
            if args["metadata"]:
                jsonbeatmap["metadata"] = {"artist_name": beatmap.artist_name.value, "song_title": beatmap.song_title.value, "creator_name": beatmap.creator_name.value, "difficulty": beatmap.difficulty.value}
            if args["id"]:
                jsonbeatmap["id"] = {'beatmap_id': beatmap.beatmap_id, 'beatmap_set_id': beatmap.beatmap_set_id, 'md5': beatmap.md5_hash.value}
            if args["map_info"]:
                sr = {x.int: x.double for x in beatmap.star_rating_osu.pairs}
                jsonbeatmap["map_info"] = {"AR": beatmap.approach_rate, "CS": beatmap.circle_size, "HP": beatmap.hp_drain, "OD": beatmap.overall_difficulty,"num_hitcircles": beatmap.num_hitcircles, "num_sliders" : beatmap.num_sliders, "num_spinners": beatmap.num_spinners, "ranked_status": beatmap.ranked_status, "star_rating": sr, "drain_time": beatmap.drain_time, "total_time": beatmap.total_time}
            jsondata.append(jsonbeatmap)
        except:
            print(f"Couldn't process map! {repr(beatmap)}")
        with open(args["output"], "w") as f:
            if args["pretty"]:
                json.dump(jsondata, f, indent=4)
            else:
                json.dump(jsondata, f
    )
if __name__ == "__main__":
    args = {"database": "osu.db", "output": "osu.json", "metadata": True, "map_info": True, "id": True, "sort_by_id": True, "pretty": False}
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} database=path output=path metadata=true/false map_info=true/false id=true/false sort_by_id=true/false pretty=true/false")
        exit(0)
    for arg in sys.argv[1:]:
        s = arg.split("=")
        if len(s) != 2:
            print("invalid argument")
            exit(1)
        if s[0] not in args:
            print("invalid argument")
            exit(1)
        args[s[0]] = s[1] if s[0] in ["database", "output"] else s[1].lower() == "true"
    read_db(args)