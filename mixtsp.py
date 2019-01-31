import sys
import argparse
from data_loader import get_tsp_manager


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Compute the best possible mix")
    parser.add_argument("--file", type=str, nargs='?', help="The path to the input file")
    parser.add_argument("--shifts_allowed", type=int,nargs='?', default=0)
    parser.add_argument("--result_file", type=str, nargs='?', default=None)
    parser.add_argument("--delete_ok", type=bool, nargs='?', default=False)
    args = parser.parse_args()

    filename = args.file
    shifts_allowed = args.shifts_allowed
    delete_ok = args.delete_ok
    result_file = args.result_file

    tsp_manager = get_tsp_manager(filename, shifts_allowed, delete_ok, result_file)
    tsp_manager.perform()
