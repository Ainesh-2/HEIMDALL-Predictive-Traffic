import tkinter as tk


class Dashboard:

    def __init__(self, mode="AI CONTROL"):

        self.root = tk.Tk()

        self.root.title("Traffic Digital Twin Dashboard")

        self.root.geometry("460x420")

        title = tk.Label(

            self.root,

            text="TRAFFIC DIGITAL TWIN",

            font=("Arial", 16, "bold")

        )

        title.pack(pady=6)

        self.mode_label = tk.Label(

            self.root,

            text=mode,

            font=("Arial", 11, "bold"),

            fg="blue"

        )

        self.mode_label.pack(pady=2)

        self.labels = []

        for i in range(3):

            lbl = tk.Label(

                self.root,

                text="",

                font=("Consolas", 12),

                justify="left"

            )

            lbl.pack()

            self.labels.append(lbl)

        self.avg_label = tk.Label(

            self.root,

            text="",

            font=("Consolas", 12, "bold")

        )

        self.avg_label.pack(pady=6)

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

    def bar(self, value, max_val):

        length = 26

        filled = int((value/max_val)*length) if max_val > 0 else 0

        return "█"*filled + "░"*(length-filled)

    # AI controller dashboard

    def update(

        self,

        pressures,

        active,

        remaining,

        allocated,

        change,

        step

    ):

        avg_pressure = sum(pressures)/len(pressures)

        max_p = max(max(pressures), avg_pressure) + 0.01

        for i, p in enumerate(pressures):

            txt = (

                f"Signal {i}\n"

                f"{self.bar(p, max_p)} {round(p, 1)}\n"

            )

            self.labels[i].config(text=txt)

        self.avg_label.config(

            text=(
                "Average Pressure\n"
                f"{self.bar(avg_pressure, max_p)} "
                f"{round(avg_pressure, 1)}"
            )
        )

        sign = "+" if change > 0 else ""

        self.active_label.config(

            text=(

                f"ACTIVE SIGNAL: {active}\n"

                f"ALLOCATED GREEN: {allocated}s\n"

                f"TIME LEFT: {remaining}s\n"

                f"CHANGE: {sign}{change}s"

            )

        )

        self.time_label.config(

            text=f"Simulation time: {step}s"

        )

        self.root.update()

    # fixed-time dashboard

    def update_fixed(

        self,

        pressures,

        avg_pressure,

        step

    ):

        max_p = max(max(pressures), avg_pressure) + 0.01

        for i, p in enumerate(pressures):

            txt = (

                f"Signal {i}\n"

                f"{self.bar(p, max_p)} {round(p, 1)}\n"

            )

            self.labels[i].config(text=txt)

        self.avg_label.config(

            text=(

                "Average Pressure\n"

                f"{self.bar(avg_pressure, max_p)} "

                f"{round(avg_pressure, 1)}"

            )

        )

        self.active_label.config(

            text="Fixed-time signal operation"

        )

        self.time_label.config(

            text=f"Simulation time: {step}s"

        )

        self.root.update()
