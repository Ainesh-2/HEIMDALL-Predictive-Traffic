import os
import sys

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

import traci

from Simulation_model.config import SUMO_CMD


traci.start(SUMO_CMD)


print("\n--- AVAILABLE LANES ---\n")

for edge in traci.edge.getIDList():

    if "1013996162" in edge:

        print("EDGE:", edge)

        lanes = traci.edge.getLaneNumber(edge)

        for i in range(lanes):

            print("   ", f"{edge}_{i}")


print("\n-----------------------\n")

traci.close()
