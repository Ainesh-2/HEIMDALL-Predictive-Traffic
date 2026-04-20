import traci

from Simulation_model.config import (
    TLS_IDS,
    MIN_GREEN,
    MAX_GREEN,
    YELLOW
)


BASE_GREEN = 180
K_PRESSURE = 5

EARLY_SWITCH_RATIO = 1.25
MIN_SERVICE_TIME = 40


current_signal = None
next_signal = None

remaining_green = 0
allocated_green = 0

time_served = 0

yellow_timer = 0

state = "INIT"

last_allocation = BASE_GREEN


def clamp(v, lo, hi):

    return max(lo, min(v, hi))


def normalize_pressures(pressures):

    p_avg = sum(pressures)/len(pressures)

    return p_avg


def compute_green_time(pressures, index):

    p_avg = normalize_pressures(pressures)

    delta = pressures[index] - p_avg

    duration = BASE_GREEN + K_PRESSURE * delta

    return int(

        clamp(

            duration,

            MIN_GREEN,

            MAX_GREEN

        )

    )


def choose_signal(pressures):

    scores = []

    avg_p = sum(pressures)/len(pressures)

    for p in pressures:

        scores.append(

            p - avg_p

        )

    return scores.index(max(scores))


def should_early_switch(pressures):

    global current_signal
    global time_served

    if time_served < MIN_SERVICE_TIME:

        return False

    current_p = pressures[current_signal]

    max_p = max(pressures)

    return max_p > EARLY_SWITCH_RATIO * current_p


def update_controller(pressures):

    global current_signal
    global next_signal

    global remaining_green
    global allocated_green

    global yellow_timer

    global time_served
    global state

    global last_allocation

    # first cycle
    if state == "INIT":

        current_signal = choose_signal(pressures)

        allocated_green = compute_green_time(

            pressures,

            current_signal

        )

        remaining_green = allocated_green

        time_served = 0

        state = "GREEN"

        return current_signal, remaining_green, allocated_green, 0

    # GREEN PHASE
    if state == "GREEN":

        remaining_green -= 1

        time_served += 1

        # early switch if another approach heavily congested
        if should_early_switch(pressures):

            remaining_green = 0

        if remaining_green <= 0:

            next_signal = choose_signal(pressures)

            yellow_timer = YELLOW

            state = "YELLOW"

        return current_signal, remaining_green, allocated_green, 0

    # YELLOW PHASE
    if state == "YELLOW":

        yellow_timer -= 1

        if yellow_timer <= 0:

            previous = allocated_green

            current_signal = next_signal

            allocated_green = compute_green_time(

                pressures,

                current_signal

            )

            remaining_green = allocated_green

            time_served = 0

            state = "GREEN"

            change = allocated_green - previous

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

        # ALL OTHER SIGNALS REMAIN RED
        else:

            traci.trafficlight.setRedYellowGreenState(

                tls,

                red_state

            )
