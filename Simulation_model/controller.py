import os
import sys

if 'SUMO_HOME' in os.environ:
    sys.path.append(
        os.path.join(
            os.environ['SUMO_HOME'], 'tools'))

import traci
from Simulation_model.config import SUMO_CMD
from Simulation_model.pressure import get_pressure
from Simulation_model.signal_control import (update_controller, apply_signals)
from Simulation_model.dashboard import Dashboard


def run():

    dashboard = Dashboard()

    traci.start(SUMO_CMD)

    step = 0

    while step < 7200:
        pressures = get_pressure()
        active, remaining, allocated, change = update_controller(pressures)
        apply_signals(active)
        if step % 3 == 0:
            dashboard.update(
                pressures,
                active,
                remaining,
                allocated,
                change,
                step
            )
        traci.simulationStep()
        step += 1
    traci.close()


run()
