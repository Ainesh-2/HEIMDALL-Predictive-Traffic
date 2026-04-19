import traci
from Simulation_model.config import TLS_IDS, MIN_GREEN, MAX_GREEN, YELLOW


# tuning parameters
EARLY_SWITCH_RATIO = 1.30
MIN_SERVICE_TIME = 20


current_signal = None
next_signal = None

remaining_green = 0
allocated_green = 0
time_served = 0

yellow_timer = 0

last_allocation = 0

state = "GREEN"   # GREEN or YELLOW


def normalize_pressures(pressures):

    p_min = min(pressures)
    p_max = max(pressures)

    norm = []

    for p in pressures:

        value = (p - p_min) / (p_max - p_min + 0.0001)

        norm.append(value)

    return norm


def compute_green_duration(norm_pressure):

    duration = MIN_GREEN + (MAX_GREEN - MIN_GREEN) * norm_pressure

    return int(duration)


def select_signal(pressures):

    return pressures.index(max(pressures))


def should_early_switch(pressures):

    global current_signal

    if current_signal is None:
        return False

    current_p = pressures[current_signal]

    max_p = max(pressures)

    if time_served < MIN_SERVICE_TIME:
        return False

    return max_p > EARLY_SWITCH_RATIO * current_p


def update_controller(pressures):

    global current_signal
    global next_signal

    global remaining_green
    global allocated_green
    global time_served

    global yellow_timer
    global last_allocation
    global state

    # FIRST RUN
    if current_signal is None:

        current_signal = select_signal(pressures)

        norm = normalize_pressures(pressures)

        allocated_green = compute_green_duration(
            norm[current_signal]
        )

        remaining_green = allocated_green

        last_allocation = allocated_green

        state = "GREEN"

        return current_signal, remaining_green, allocated_green, 0

    # GREEN PHASE RUNNING
    if state == "GREEN":

        remaining_green -= 1
        time_served += 1

        # early switch condition
        if should_early_switch(pressures):

            remaining_green = 0

        # green finished → start yellow
        if remaining_green <= 0:

            next_signal = select_signal(pressures)

            yellow_timer = YELLOW

            state = "YELLOW"

        return current_signal, remaining_green, allocated_green, 0

    # YELLOW PHASE RUNNING
    if state == "YELLOW":

        yellow_timer -= 1

        # yellow finished → switch signal
        if yellow_timer <= 0:

            current_signal = next_signal

            norm = normalize_pressures(pressures)

            allocated_green = compute_green_duration(
                norm[current_signal]
            )

            change = allocated_green - last_allocation

            last_allocation = allocated_green

            remaining_green = allocated_green

            time_served = 0

            state = "GREEN"

            return current_signal, remaining_green, allocated_green, change

        return current_signal, remaining_green, allocated_green, 0


def apply_signals(active):

    global state

    for i, tls in enumerate(TLS_IDS):

        logic = traci.trafficlight.getAllProgramLogics(tls)[0]

        green_state = logic.phases[0].state
        yellow_state = logic.phases[1].state
        red_state = logic.phases[-1].state.replace("G", "r")

        # ACTIVE SIGNAL
        if i == active:

            if state == "GREEN":

                traci.trafficlight.setRedYellowGreenState(
                    tls,
                    green_state
                )

            else:

                traci.trafficlight.setRedYellowGreenState(
                    tls,
                    yellow_state
                )

        # NON ACTIVE SIGNALS
        else:

            traci.trafficlight.setRedYellowGreenState(
                tls,
                red_state
            )
