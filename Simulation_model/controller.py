import traci

from Simulation_model.config import *
from Simulation_model.pressure import get_pressure
from Simulation_model.dashboard import Dashboard
from Simulation_model.signal_control import (update_controller,apply_signals)


def run():
    traci.start(SUMO_CMD)
    dashboard = Dashboard()
    step = 0
    while step < 7200:
        pressures = get_pressure()
        active_signal, remaining_green, allocated_green, change = update_controller(
            pressures)
        apply_signals(active_signal)
        avg_pressure = sum(pressures) / len(pressures)
        if step % 3 == 0:
            dashboard.update(
                pressures,
                active_signal,
                remaining_green,
                allocated_green,
                change,
                step
            )
        traci.simulationStep()
        step += 1
    traci.close()
