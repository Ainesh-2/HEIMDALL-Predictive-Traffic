import tkinter as tk


class Dashboard:

    def __init__(self, mode="AI CONTROL"):

        self.root = tk.Tk()
        self.root.title("Traffic Digital Twin Dashboard")
        self.root.geometry("480x460")

        tk.Label(
            self.root,
            text="TRAFFIC DIGITAL TWIN",
            font=("Arial", 16, "bold")
        ).pack(pady=6)

        self.mode_label = tk.Label(
            self.root,
            text=mode,
            font=("Arial", 11, "bold"),
            fg="blue"
        )
        self.mode_label.pack(pady=2)

        self.labels = []
        for i in range(4):  # FIXED → 4 directions
            lbl = tk.Label(
                self.root,
                text="",
                font=("Consolas", 12),
                justify="left"
            )
            lbl.pack()
            self.labels.append(lbl)

        self.group_label = tk.Label(
            self.root,
            text="",
            font=("Consolas", 12, "bold")
        )
        self.group_label.pack(pady=6)

        self.active_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 11, "bold")
        )
        self.active_label.pack(pady=6)

        self.time_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 10)
        )
        self.time_label.pack()

        self.names = ["NORTH", "SOUTH", "EAST", "WEST"]

    def bar(self, value, max_val):
        length = 26
        filled = int((value / max_val) * length) if max_val > 0 else 0
        return "█" * filled + "░" * (length - filled)

    def update(self, pressures, active, remaining, allocated, change, step):

        N, S, E, W = pressures
        NS = (N + S) / 2
        EW = (E + W) / 2

        avg_pressure = (NS + EW) / 2
        max_p = max(max(pressures), NS, EW) + 0.01

        # individual directions
        for i, p in enumerate(pressures):
            txt = (
                f"{self.names[i]}\n"
                f"{self.bar(p, max_p)} {round(p, 1)}\n"
            )
            self.labels[i].config(text=txt)

        # group comparison (NEW)
        self.group_label.config(
            text=(
                "NS vs EW\n"
                f"NS {self.bar(NS, max_p)} {round(NS, 1)}\n"
                f"EW {self.bar(EW, max_p)} {round(EW, 1)}"
            )
        )

        active_text = "NS" if active == 0 else "EW"
        sign = "+" if change > 0 else ""

        self.active_label.config(
            text=(
                f"ACTIVE: {active_text}\n"
                f"GREEN: {allocated}s | LEFT: {remaining}s\n"
                f"CHANGE: {sign}{change}s"
            )
        )

        self.time_label.config(text=f"Simulation time: {step}s")

        if self.root.winfo_exists():
            self.root.update()

    def update_fixed(self, pressures, avg_pressure, step):

        pressures = list(pressures)
        if len(pressures) < 4:
            pressures += [0] * (4 - len(pressures))

        N, S, E, W = pressures[:4]

        NS = (N + S) / 2
        EW = (E + W) / 2

        max_p = max(max(pressures), NS, EW) + 0.01

        for i, p in enumerate(pressures):
            txt = (
                f"{self.names[i]}\n"
                f"{self.bar(p, max_p)} {round(p, 1)}\n"
            )
            self.labels[i].config(text=txt)

        self.group_label.config(
            text=(
                "NS vs EW\n"
                f"NS {self.bar(NS, max_p)} {round(NS, 1)}\n"
                f"EW {self.bar(EW, max_p)} {round(EW, 1)}"
            )
        )

        self.active_label.config(
            text="FIXED TIME CONTROL"
        )

        self.time_label.config(
            text=f"Simulation time: {step}s"
        )

        if self.root.winfo_exists():
            self.root.update()
