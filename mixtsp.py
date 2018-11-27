import sys
from data_loader import get_tsp_manager


if __name__ == "__main__":
    filename = sys.argv[1]
    shifts_allowed = int(sys.argv[2])
    result_file = sys.argv[3] if len(sys.argv) >= 4 else None #filename[:-4]+"_res_{}.txt".format(shifts_allowed)
    tsp_manager = get_tsp_manager(filename, shifts_allowed, result_file)
    tsp_manager.perform()
