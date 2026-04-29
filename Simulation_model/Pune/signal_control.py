import traci
from Simulation_model.Pune.config import TLS_IDS, MIN_GREEN, MAX_GREEN, YELLOW

BASE_GREEN = 35
K_PRESSURE = 3

current_signal = None
next_signal = None

remaining_green = 0
allocated_green = 0

yellow_timer = 0
time_served = 0

state = "INIT"


def clamp(v, lo, hi):
    return max(lo, min(v, hi))


def compute_group_pressures(pressures):
    if len(pressures) < 4:
        pressures = pressures + [0]*(4 - len(pressures))
    N, S, E, W = pressures
    NS = (N + S) / 2
    EW = (E + W) / 2
    return NS, EW


def choose_signal(pressures):
    NS, EW = compute_group_pressures(pressures)
    return 0 if NS >= EW else 1


def compute_green_time(pressures, index):
    NS, EW = compute_group_pressures(pressures)
    avg = (NS + EW) / 2
    p = NS if index == 0 else EW

    delta = p - avg
    duration = BASE_GREEN + K_PRESSURE * delta

    return int(clamp(duration, MIN_GREEN, MAX_GREEN))


def update_controller(pressures):

    global current_signal, next_signal
    global remaining_green, allocated_green
    global yellow_timer, time_served, state

    if state == "INIT":
        current_signal = choose_signal(pressures)
        allocated_green = compute_green_time(pressures, current_signal)
        remaining_green = allocated_green
        time_served = 0
        state = "GREEN"
        return current_signal, remaining_green, allocated_green, 0

    if state == "GREEN":

        remaining_green -= 1
        time_served += 1

        if remaining_green <= 0:
            next_signal = choose_signal(pressures)
            yellow_timer = YELLOW
            state = "YELLOW"

        return current_signal, remaining_green, allocated_green, 0

    if state == "YELLOW":

        yellow_timer -= 1

        if yellow_timer <= 0:
            prev = allocated_green

            current_signal = next_signal
            allocated_green = compute_green_time(pressures, current_signal)
            remaining_green = allocated_green
            time_served = 0
            state = "GREEN"

            return current_signal, remaining_green, allocated_green, allocated_green - prev

        return current_signal, remaining_green, allocated_green, 0


def apply_signals(active):

    tls = TLS_IDS[0]

    # SUMO default phases (verified assumption)
    # 0 = NS green
    # 1 = NS yellow
    # 2 = EW green
    # 3 = EW yellow

    if state == "GREEN":
        traci.trafficlight.setPhase(tls, 0 if active == 0 else 2)
    else:
        traci.trafficlight.setPhase(tls, 1 if active == 0 else 3)
