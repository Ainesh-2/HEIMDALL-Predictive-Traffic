import traci

from Simulation_model.Pune.config import SUMO_CMD
from Simulation_model.Pune.pressure import get_pressure
from Simulation_model.Pune.dashboard import Dashboard
from Simulation_model.Pune.signal_control import (
    update_controller, apply_signals)


def run():

    traci.start(SUMO_CMD)

    dashboard = Dashboard(mode="AIDED")

    step = 0

    while step < 7200:

        traci.simulationStep()   # 🔥 MUST be first

        pressures = get_pressure()

        active_signal, remaining_green, allocated_green, change = update_controller(
            pressures)

        apply_signals(active_signal)

        dashboard.update(
            pressures,
            active_signal,
            remaining_green,
            allocated_green,
            change,
            step
        )

        step += 1

    traci.close()
