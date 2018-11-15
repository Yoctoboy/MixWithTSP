import sys
from data_loader import get_tsp_manager


if __name__ == "__main__":
    filename = sys.argv[1]
    tsp_manager = get_tsp_manager(filename)
    tsp_manager.perform()
    print(tsp_manager.songs)