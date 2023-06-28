import json
import sys

if __name__ == "__main__":
    args = {"database": "osu.db", "output": "osu.json", "md5": True, "map_info": True, "ids": True}
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} database=path output=path metadata=true/false md5=true/false map_info=true/false ids=true/false")
        exit(0)
    for arg in sys.argv[1:]:
        s = arg.split("=")
        if len(s) != 2:
            print("invalid argument")
            exit(1)
        if s[0] not in args:
            print("invalid argument")
            exit(1)
        if s[0] == "database" or s[0] == "output":
            args[s[0]] = s[1]
        else:
            args[s[0]] = s[1].lower() == "true"
    print(args)