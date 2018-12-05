import itertools
import time
import sys

from data_loader import get_tsp_manager
from tsp_solver import TSPSolver

files_list = ["testfiles/lewitchwavemix.txt",
              "testfiles/waveULTIMATEMEGAMIX2K18BEDODOSLAKMEISTER.txt",
              "testilfes/nothing_to_see_here_II.txt"]
shifts_list = [1]
clique_param_list = [0, 1]
gomory_param_list = [0, 1, 2]
covercuts_param_list = [-1, 0, 1, 2, 3]

for filename, shift, clique, gomory, covercuts in itertools.product(files_list, 
                                                                shifts_list,
                                                                clique_param_list,
                                                                gomory_param_list,
                                                                covercuts_param_list, 
                                                                ):
    tsp_manager = get_tsp_manager(filename, shift)
    tsp_manager.compute_graph()
    solver = TSPSolver(tsp_manager.nodes, tsp_manager.graph, 2 * tsp_manager.shifts_allowed + 1)
    solver.create_model()
    solver.prepare_solver()
    solver.solver.parameters.clocktype.set(1)
    solver.solver.parameters.timelimit.set(1000)  # 1000 seconds max
    solver.solver.parameters.mip.display.set(0)  # No node log

    # params
    solver.solver.parameters.mip.cuts.cliques.set(clique)
    solver.solver.parameters.mip.cuts.gomory.set(gomory)
    solver.solver.parameters.mip.cuts.covers.set(covercuts)

    start_clock = time.clock()
    solver.solve()
    end_clock = time.clock()
    #import ipdb; ipdb.set_trace()
    print("####################################################")
    print("File: {} with {} shifts".format(filename, shift))
    print("Cliques: {} - Gomory: {} - Covers: {}".format(clique, gomory, covercuts))
    print("CPU time elapsed: {}s - Nodes explored: {}\n".format(round(end_clock - start_clock, 2), solver.solver.solution.progress.get_num_nodes_processed()))

    with open("res.txt", "a+") as f:
        f.write("####################################################\n")
        f.write("File: {} with {} shifts\n".format(filename, shift))
        f.write("Cliques: {} - Gomory: {} - Covers: {}\n".format(clique, gomory, covercuts))
        f.write("CPU time elapsed: {}s - Nodes explored: {}\n".format(round(end_clock - start_clock, 2), solver.solver.solution.progress.get_num_nodes_processed()))
        f.write("####################################################\n\n\n")