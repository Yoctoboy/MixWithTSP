import sys
from data_loader import get_tsp_manager


if __name__ == "__main__":
    filename = sys.argv[1]
    shifts_allowed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    tsp_manager = get_tsp_manager(filename, shifts_allowed)
    print(tsp_manager.songs)
    tsp_manager.perform()