TLS_IDS = [
    "913535543",
    "913535601",
    "602468633"
]
DETECTION_ZONES = {
    "913535543": [
        "171505928#10_0",
        "171505928#10_1",
        "E22_0",
        "E22_1"
    ],
    "913535601": [
        "1446379669#0_0",
        "1446379669#0_1",
        "E19_0",
        "E19_1"
    ],
    "602468633": [
        "1013996162#1_0",
        "1013996162#1_1",
        "E0_0",
        "E0_1"
    ]
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
    r"simulation\simulation.sumocfg"
]
