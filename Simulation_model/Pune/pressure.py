import traci
from Simulation_model.Pune.config import DETECTION_ZONES


def get_pressure():

    directions = ["north", "south", "east", "west"]
    pressures = []

    for d in directions:

        edges = DETECTION_ZONES.get(d, None)

        if edges is None:
            print(f"⚠️ MISSING CONFIG: {d}")
            pressures.append(0)
            continue

        count = 0

        for edge in edges:
            count += traci.edge.getLastStepVehicleNumber(edge)

        pressures.append(count)

    # 🔥 HARD GUARANTEE
    if len(pressures) != 4:
        print("❌ ERROR: pressures length =", len(pressures))

    print("PRESSURES:", pressures)

    return pressures
