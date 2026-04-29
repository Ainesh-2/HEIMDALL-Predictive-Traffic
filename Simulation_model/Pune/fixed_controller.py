import traci

from Simulation_model.Pune.config import SUMO_CMD
from Simulation_model.Pune.pressure import get_pressure
from Simulation_model.Pune.dashboard import Dashboard


def run():

    traci.start(SUMO_CMD)

    dashboard = Dashboard(mode="FIXED TIME")

    step = 0

    while step < 7200:

        # -------------------------
        # GET PRESSURE
        # -------------------------
        pressures = get_pressure()
        avg_pressure = sum(pressures) / len(pressures)

        # -------------------------
        # DASHBOARD
        # -------------------------
        if step % 3 == 0:
            dashboard.update_fixed(
                pressures,
                avg_pressure,
                step
            )

        # -------------------------
        # STEP
        # -------------------------
        traci.simulationStep()
        step += 1

    traci.close()
