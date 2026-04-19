import os
import sys

if 'SUMO_HOME' in os.environ:
    sys.path.append(
        os.path.join(os.environ['SUMO_HOME'], 'tools')
    )

import traci

from Simulation_model.config import SUMO_CMD
from Simulation_model.pressure import get_pressure
from Simulation_model.dashboard import Dashboard


def run_fixed():

    dashboard = Dashboard(mode="FIXED TIME")

    traci.start(SUMO_CMD)

    step = 0

    while step < 7200:

        pressures = get_pressure()

        avg_pressure = sum(pressures) / len(pressures)

        if step % 3 == 0:

            dashboard.update_fixed(
                pressures,
                avg_pressure,
                step
            )

        traci.simulationStep()

        step += 1

    traci.close()
