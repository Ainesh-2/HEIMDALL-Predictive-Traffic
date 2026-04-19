import traci
from Simulation_model.config import DETECTION_ZONES, WEIGHTS


def get_pressure():
    pressures = []
    for tls in DETECTION_ZONES:
        p = 0
        for lane in DETECTION_ZONES[tls]:
            try:
                vehicles = traci.lane.getLastStepVehicleIDs(lane)
                for v in vehicles:
                    vtype = traci.vehicle.getTypeID(v)
                    p += WEIGHTS.get(vtype, 1)
            except:
                pass
        pressures.append(p)
    return pressures
