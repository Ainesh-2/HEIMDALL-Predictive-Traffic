TLS_IDS = ["center"]
DETECTION_ZONES = {
    "north": ["n_in"],
    "south": ["s_in"],
    "east":  ["e_in"],
    "west":  ["w_in"]
}
WEIGHTS = {
    "bike": 0.35,
    "auto": 0.5,
    "car": 1.0,
    "car_fast": 1.0,
    "tempo": 1.4,
    "bus": 2.3,
    "truck": 2.8
}
BASE_GREEN = 60
MIN_GREEN = 45
MAX_GREEN = 220
YELLOW = 6
SWITCH_THRESHOLD = 0.25
SUMO_CMD = [
    r"C:\Program Files (x86)\Eclipse\Sumo\bin\sumo-gui.exe",
    "-c",
    r"simulation\pune\simulation.sumocfg"
]
