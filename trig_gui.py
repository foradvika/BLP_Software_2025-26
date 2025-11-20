# Authors: Advika Govindarajan, Emily Jones, Adam Abid, Alex Garcia

import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import time
import subprocess
import datetime
import json
import queue

from pycode import Telemetry, System_Health, Metrics
from pycode import V1, V2, V3, V4, C, T, CS, A
import uart_code1


# ---------- Fake Telemetry for Simulation Testing ----------
class FakeTelemetry:
    def __init__(self, sys):
        print("FakeTelemetry: Initialized (Simulation Mode).")
        self.counter = 0

    def start_test(self):
        print("FakeTelemetry: Test started.")

    def send_data(self):
        print("FakeTelemetry: Data sent.")

    def abort(self):
        print("FakeTelemetry: Test aborted.")

    def open_valve(self, valve):
        print(f"FakeTelemetry: Valve {valve} opened.")

    def close_valve(self, valve):
        print(f"FakeTelemetry: Valve {valve} closed.")

    def upload_test_sequence(self, file_path):
        print(f"FakeTelemetry: Uploaded test sequence from {file_path}")

    def get_data(self):
        self.counter += 1
        thrust = self.counter % 201
        pt1 = (self.counter * 2) % 851
        pt2 = (self.counter * 3) % 851
        pt3 = (self.counter * 4) % 851
        pt4 = (self.counter * 5) % 851
        pt5 = (self.counter * 6) % 851
        return [thrust, pt1, pt2, pt3, pt4, pt5]


# ---------- Main GUI Class ----------
class GUI:
    def __init__(self):
        # Data storage for graphs
        self.thrust_data = []
        self.pt1_data = []
        self.pt2_data = []
        self.pt3_data = []
        self.pt4_data = []
        self.pt5_data = []
        self.all_data = []
        self.times = []
        self.time_off = None

        # Placeholders for plot elements
        self.thrust_fig = self.thrust_ax = self.thrust_canvas = self.thrust_line = None
        self.pt1_fig = self.pt1_ax = self.pt1_canvas = self.pt1_line = None
        self.pt2_fig = self.pt2_ax = self.pt2_canvas = self.pt2_line = None
        self.pt3_fig = self.pt3_ax = self.pt3_canvas = self.pt3_line = None
        self.pt4_fig = self.pt4_ax = self.pt4_canvas = self.pt4_line = None
        self.pt5_fig = self.pt5_ax = self.pt5_canvas = self.pt5_line = None

        # UI element placeholders
        self.chart_canvas = None
        self.PT5_label = None
        self.PT4_label = None
        self.PT3_label = None
        self.PT2_label = None
        self.PT1_label = None
        self.thrust_label = None
        self.temp_label = None
        self.banner_label = None
        self.abort_button = None
        self.start_button = None
        self.OV03_button = None
        self.FV03_button = None
        self.FV02_button = None
        self.NV02_button = None
        self.file_input_entry = None
        self.file_input = None
        self.title = None
        self.timer_label = None
        self.warning_label = None
        self.start_time = None
        self.after_id = None

        # Window setup
        self.window = tk.Tk()
        self.window.title("BLP GUI")
        self.window.geometry('1000x1000')
        for i in range(5):
            self.window.columnconfigure(i, weight=1, uniform="col")

        # State variables
        self.valve_status = {'NV-02': 0, 'FV-02': 0, 'FV-03': 0, 'OV-03': 0}
        self.busy = False
        self.running = False
        self.POST_ABORT_TAIL_S = 10.0
        self.tail_deadline = None
        self.tail_saving_done = False
        self.abort_time = None

        self.widgets()

    def _with_lock(self, fn):
        if self.busy:
            return
        self.busy = True
        try:
            fn()
        finally:
            self.busy = False

    def _disable_valve_buttons(self, disabled=True):
        state = tk.DISABLED if disabled else tk.NORMAL
        for b in (self.FV03_button, self.OV03_button, self.FV02_button, self.NV02_button):
            b.config(state=state)

    def widgets(self):
        # Timer label
        self.timer_label = tk.Label(self.window, text="Elapsed Time: 0 s",
                                    font=("Times New Roman", 15), fg="black")
        self.timer_label.grid(row=1, column=3, sticky="w", padx=5, pady=5)

        # Warning label
        self.warning_label = tk.Label(self.window, text=" ",
                                      font=("Times New Roman", 15), fg="red")
        self.warning_label.grid(row=2, column=4, sticky="e", padx=5, pady=5)

        # Title
        self.title = tk.Label(self.window,
                              text="BLP GUI",
                              font=("Times New Roman", 25),
                              background="light pink",
                              foreground="black")
        self.title.grid(row=0, columnspan=5, sticky="nsew", pady=(40, 5))

        # File Input
        self.file_input = tk.StringVar()
        self.file_input_entry = tk.Button(self.window,
                                          text="Upload File",
                                          foreground="black",
                                          font=("Times New Roman", 20),
                                          command=self.upload_file)
        self.file_input_entry.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # NV02 Button
        self.NV02_button = tk.Button(self.window,
                                     text="NV-02",
                                     foreground="black",
                                     font=("Times New Roman", 20),
                                     command=lambda: self.toggle_valve(V4))
        self.NV02_button.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        # FV02 Button
        self.FV02_button = tk.Button(self.window,
                                     text="FV-02",
                                     foreground="black",
                                     font=("Times New Roman", 20),
                                     command=lambda: self.toggle_valve(V1))
        self.FV02_button.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # FV03 Button
        self.FV03_button = tk.Button(self.window,
                                     text="FV-03",
                                     foreground="black",
                                     font=("Times New Roman", 20),
                                     command=lambda: self.toggle_valve(V2))
        self.FV03_button.grid(row=2, column=2, sticky="ew", padx=5, pady=5)

        # OV03 Button
        self.OV03_button = tk.Button(self.window,
                                     text="OV-03",
                                     foreground="black",
                                     font=("Times New Roman", 20),
                                     command=lambda: self.toggle_valve(V3))
        self.OV03_button.grid(row=2, column=3, sticky="ew", padx=5, pady=5)

        # Macro buttons for opening/closing both valves
        self.both_open_btn = tk.Button(self.window, text="Abrir FV-03 + OV-03",
                                       font=("Times New Roman", 16),
                                       command=self.open_both_valves_safe)
        self.both_open_btn.grid(row=3, column=2, sticky="ew", padx=5, pady=5)

        self.both_close_btn = tk.Button(self.window, text="Cerrar FV-03 + OV-03",
                                        font=("Times New Roman", 16),
                                        command=self.close_both_valves_safe)
        self.both_close_btn.grid(row=3, column=3, sticky="ew", padx=5, pady=5)

        # Start Button
        self.start_button = tk.Button(self.window,
                                      text="START",
                                      background="green",
                                      foreground="black",
                                      font=("Times New Roman", 20),
                                      command=self.start)
        self.start_button.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Abort Button
        self.abort_button = tk.Button(self.window,
                                      text="ABORT",
                                      background="red",
                                      foreground="black",
                                      font=("Times New Roman", 20),
                                      command=self.abort)
        self.abort_button.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        # Ignition Button
        self.ignition_button = tk.Button(self.window,
                                         text="IGNITION",
                                         background="orange",
                                         foreground="black",
                                         font=("Times New Roman", 20),
                                         command=self.ignition_sequence)
        self.ignition_button.grid(row=2, column=4, sticky="ew", padx=5, pady=5)

        # Labels for graphs
        self.thrust_label = tk.Label(self.window,
                                     text="Thrust",
                                     background="white",
                                     foreground="black",
                                     font=("Times New Roman", 15))
        self.thrust_label.grid(row=5, column=0, sticky="nsew", padx=5, pady=5)

        self.PT1_label = tk.Label(self.window,
                                  text="OPD_01",
                                  background="white",
                                  foreground="black",
                                  font=("Times New Roman", 15))
        self.PT1_label.grid(row=5, column=2, sticky="nsew", padx=5, pady=5)

        self.PT2_label = tk.Label(self.window,
                                  text="OPD_02",
                                  background="white",
                                  foreground="black",
                                  font=("Times New Roman", 15))
        self.PT2_label.grid(row=5, column=4, sticky="nsew", padx=5, pady=5)

        self.PT3_label = tk.Label(self.window,
                                  text="EPD_01",
                                  background="white",
                                  foreground="black",
                                  font=("Times New Roman", 15))
        self.PT3_label.grid(row=7, column=0, sticky="nsew", padx=5, pady=5)

        self.PT4_label = tk.Label(self.window,
                                  text="FPD_01",
                                  background="white",
                                  foreground="black",
                                  font=("Times New Roman", 15))
        self.PT4_label.grid(row=7, column=2, sticky="nsew", padx=5, pady=5)

        self.PT5_label = tk.Label(self.window,
                                  text="FPD_02",
                                  background="white",
                                  foreground="black",
                                  font=("Times New Roman", 15))
        self.PT5_label.grid(row=7, column=4, sticky="nsew", padx=5, pady=5)

        # Create plots and store references for updates
        self.thrust_fig, self.thrust_ax, self.thrust_canvas, self.thrust_line = \
            self.create_plot(row=6, column=0, xlabel="Time (s)", ylabel="Thrust (lbf)", data=[])

        self.pt1_fig, self.pt1_ax, self.pt1_canvas, self.pt1_line = \
            self.create_plot(row=6, column=2, xlabel="Time (s)", ylabel="Pressure (PSI)", data=[])

        self.pt2_fig, self.pt2_ax, self.pt2_canvas, self.pt2_line = \
            self.create_plot(row=6, column=4, xlabel="Time (s)", ylabel="Pressure (PSI)", data=[])

        self.pt3_fig, self.pt3_ax, self.pt3_canvas, self.pt3_line = \
            self.create_plot(row=8, column=0, xlabel="Time (s)", ylabel="Pressure (PSI)", data=[])

        self.pt4_fig, self.pt4_ax, self.pt4_canvas, self.pt4_line = \
            self.create_plot(row=8, column=2, xlabel="Time (s)", ylabel="Pressure (PSI)", data=[])

        self.pt5_fig, self.pt5_ax, self.pt5_canvas, self.pt5_line = \
            self.create_plot(row=8, column=4, xlabel="Time (s)", ylabel="Pressure (PSI)", data=[])

    def create_plot(self, row, column, xlabel, ylabel, data):
        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.grid(True)
        if data:
            line, = ax.plot(range(len(data)), data)
        else:
            line, = ax.plot([], [])
        fig.tight_layout(pad=3.0)
        fig.subplots_adjust(bottom=0.3, top=0.9)
        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=row, column=column, columnspan=2, sticky="nsew", padx=5, pady=5)
        canvas.draw()
        return fig, ax, canvas, line

    def start(self):
        print("Test started")
        # Clear all data from previous tests
        self.thrust_data = []
        self.pt1_data = []
        self.pt2_data = []
        self.pt3_data = []
        self.pt4_data = []
        self.pt5_data = []
        self.all_data = []
        self.times = []
        self.display_times = []

        self.start_time = time.time()
        self.test_start_time = self.start_time
        self.running = True
        self.tail_deadline = None
        self.tail_saving_done = False
        self.abort_time = None
        self.time_off = None  # Reset time offset for new test
        self.update_graphs()
        self.start_button.config(background="green")
        
    def ignition_sequence(self):
            """Execute full ignition: open FV-03 + OV-03 + fire spark"""
            print("Ignition sequence initiated")
            tel.ignite()
            # Update GUI to reflect both valves open
            self.FV03_button.config(bg="green")
            self.valve_status['FV-03'] = 1
            self.OV03_button.config(bg="green")
            self.valve_status['OV-03'] = 1
    

    def abort(self):
        # Record abort timestamp
        self.abort_time = time.time() - self.start_time
        print(f"Manual Test aborted at t={self.abort_time:.3f}s")

        tel.abort()
        tel.send_data()
        self.OV03_button.config(bg="red")
        self.valve_status['OV-03'] = 0
        self.FV03_button.config(bg="red")
        self.valve_status['FV-03'] = 0
        self.FV02_button.config(bg="green")
        self.valve_status['FV-02'] = 1
        self.NV02_button.config(bg="red")
        self.valve_status['NV-02'] = 0
        self.test_running = False

        if self.POST_ABORT_TAIL_S and self.POST_ABORT_TAIL_S > 0:
            self.tail_deadline = time.time() + self.POST_ABORT_TAIL_S
            self.tail_saving_done = False
            self.running = True
            self.warning_label.config(
                text=f"ABORT: registering {self.POST_ABORT_TAIL_S:.1f}s post-event…"
            )
        else:
            self.running = False
            if hasattr(self, "after_id") and self.after_id:
                self.window.after_cancel(self.after_id)
                self.after_id = None
            self.save_data_to_csv()
            messagebox.showinfo("Test Data Saved", "All telemetry data has been saved to test_data.csv")

    def upload_file(self):
        def Start_Count():
            self.start()

        def BLP_Abort():
            self.abort()
            return "Test aborted and data saved"
            
        def ignition_sequence():
            """Execute full ignition: open FV-03 + OV-03 + fire spark"""
            print("Ignition sequence initiated")
            tel.ignite()
            # Update GUI to reflect both valves open
            self.FV03_button.config(bg="green")
            self.valve_status['FV-03'] = 1
            self.OV03_button.config(bg="green")
            self.valve_status['OV-03'] = 1
                

        def Read_OPD_02():
            print(self.pt2_data)
            return ("OPD_02 within safe range")

        def Read_FPD_02():
            return ("FPD_02 within safe range")

        def Read_EPD_01():
            return ("EPD_01 within safe range")

        def FV_02_Close():
            tel.close_valve(V1)
            tel.send_data()
            self.FV02_button.config(bg="red")
            self.valve_status['FV-02'] = 0
            if self.valve_status["FV-02"] == 1:
                return BLP_Abort()
            return ("FV-02 closed")

        def NV_02_Open():
            tel.open_valve(V4)
            tel.send_data()
            self.NV02_button.config(bg="green")
            self.valve_status['NV-02'] = 1
            if self.valve_status["NV-02"] == 0:
                return BLP_Abort()
            return ("NV-02 opened")

        def OV_03_Open():
            tel.open_valve(V3)
            tel.send_data()
            self.OV03_button.config(bg="green")
            self.valve_status['OV-03'] = 1
            if self.valve_status["OV-03"] == 0:
                return BLP_Abort()
            return ("OV-03 opened")

        def FV_03_Open():
            tel.open_valve(V2)
            tel.send_data()
            self.FV03_button.config(bg="green")
            self.valve_status['FV-03'] = 1
            if self.valve_status["FV-03"] == 0:
                return BLP_Abort()
            return ("FV_03 opened")

        function_map = {
            'Start_Count': Start_Count,
            'Read_OPD_02': Read_OPD_02,
            'Read_FPD_02': Read_FPD_02,
            'Read_EPD_01': Read_EPD_01,
            'FV_02': FV_02_Close,
            'NV_02': NV_02_Open,
            'OV_03': OV_03_Open,
            'FV_03': FV_03_Open,
            'Ignition': ignition_sequence,
            'BLP_Abort': BLP_Abort,
        }

        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            print(f"Selected file: {file_path}")
            try:
                df = pd.read_csv(file_path)
                test_sequence = list(zip(df['Time'], df['Function']))

                self.test_running = True
                self.test_start_time = time.time()
                self.current_step = 0

                def execute_test_step():
                    if not self.test_running:
                        return 0
                    if self.current_step >= len(test_sequence):
                        return 0

                    current_time = time.time() - self.test_start_time
                    target_time, function = test_sequence[self.current_step]

                    if current_time >= target_time and self.test_running:
                        func = function_map.get(function)

                        if func:
                            try:
                                result = func()
                                print(f"Executed {function} at {current_time:.3f}s: {result}")
                            except Exception as e:
                                print(f"Error executing {function}: {e}")
                                self.test_running = False

                        self.current_step += 1

                    if self.test_running:
                        self.window.after(10, execute_test_step)

                execute_test_step()

            except Exception as e:
                print(f"Error loading file: {e}")
                self.test_running = False

    def open_both_valves_safe(self):
        if self.busy:
            return
        self._disable_valve_buttons(True)

        def step1():
            tel.open_valve(V2)
            tel.send_data()
            self.FV03_button.config(bg="green")
            self.valve_status['FV-03'] = 1
            self.window.after(100, step2)

        def step2():
            tel.open_valve(V3)
            tel.send_data()
            self.OV03_button.config(bg="green")
            self.valve_status['OV-03'] = 1
            self._disable_valve_buttons(False)

        self._with_lock(step1)

    def close_both_valves_safe(self):
        if self.busy:
            return
        self._disable_valve_buttons(True)

        def step1():
            tel.close_valve(V3)
            tel.send_data()
            self.OV03_button.config(bg="red")
            self.valve_status['OV-03'] = 0
            self.window.after(100, step2)

        def step2():
            tel.close_valve(V2)
            tel.send_data()
            self.FV03_button.config(bg="red")
            self.valve_status['FV-03'] = 0
            self._disable_valve_buttons(False)

        self._with_lock(step1)

    def toggle_valve(self, name):
        if name == V4 and self.valve_status['NV-02'] == 0:
            tel.open_valve(V4)
            tel.send_data()
            self.NV02_button.configure(background="green")
            self.valve_status['NV-02'] = 1
            print("NV-02 opened")
        elif name == V1 and self.valve_status['FV-02'] == 0:
            tel.open_valve(V1)
            tel.send_data()
            self.FV02_button.config(bg="green")
            self.valve_status['FV-02'] = 1
            print("FV-02 opened")
        elif name == V2 and self.valve_status['FV-03'] == 0:
            tel.open_valve(V2)
            tel.send_data()
            self.FV03_button.config(bg="green")
            self.valve_status['FV-03'] = 1
            print("FV-03 opened")
        elif name == V3 and self.valve_status['OV-03'] == 0:
            tel.open_valve(V3)
            tel.send_data()
            self.OV03_button.config(bg="green")
            self.valve_status['OV-03'] = 1
            print("OV-03 opened")
        elif name == V4 and self.valve_status['NV-02'] == 1:
            tel.close_valve(V4)
            tel.send_data()
            self.NV02_button.config(bg="red")
            self.valve_status['NV-02'] = 0
            print("NV-02 closed")
        elif name == V1 and self.valve_status['FV-02'] == 1:
            tel.close_valve(V1)
            tel.send_data()
            self.FV02_button.config(bg="red")
            self.valve_status['FV-02'] = 0
            print("FV-02 closed")
        elif name == V2 and self.valve_status['FV-03'] == 1:
            tel.close_valve(V2)
            tel.send_data()
            self.FV03_button.config(bg="red")
            self.valve_status['FV-03'] = 0
            print("FV-03 closed")
        elif name == V3 and self.valve_status['OV-03'] == 1:
            tel.close_valve(V3)
            tel.send_data()
            self.OV03_button.config(bg="red")
            self.valve_status['OV-03'] = 0
            print("OV-03 closed")
        else:
            print("Error toggling valve")

    def update_graphs(self):
        if not self.running:
            return

        # Drain all available frames from the queue (100Hz data collection)
        frames_processed = 0
        while True:
            try:
                # Get frame directly from queue (non-blocking)
                frame = uart_code1.get_frame_nowait()
                if frame is None:
                    break

                # Frame format: [t_ms, OPD01, OPD02, EPD01, FPD01, FPD02, THRUST]
                t_ms, opd01, opd02, epd01, fpd01, fpd02, thrust = frame

                # Use Arduino's timestamp (more accurate than Python time.time())
                ts = t_ms / 1000.0
                
                if self.time_off is None:
                    self.time_off = ts 
                elapsed = ts - self.time_off

                # Append all data
                self.times.append(elapsed)
                self.pt1_data.append(opd01)  # OPD01
                self.pt2_data.append(opd02)  # OPD02
                self.pt3_data.append(epd01)  # EPD01
                
                self.pt4_data.append(fpd01)  # FPD01
                self.pt5_data.append(fpd02)  # FPD02
                self.thrust_data.append(thrust)
                self.all_data.append([opd01, opd02, epd01, fpd01, fpd02, thrust])

                frames_processed += 1

            except Exception as e:
                print(f"Error processing frame: {e}")
                break
            
            # Update timer with Python elapsed time (always smooth and continuous)
        elapsed = time.time() - self.start_time
        self.timer_label.config(text=f"Elapsed Time: {elapsed:.3f} s")


        # If no new data, reschedule and return
        if frames_processed == 0:
            self.after_id = self.window.after(10, self.update_graphs)
            return

        # Update all graphs (only after processing all available frames)
        self.pt1_line.set_data(self.times, self.pt1_data)
        self.pt1_ax.relim()
        self.pt1_ax.autoscale_view()
        self.pt1_canvas.draw()

        self.pt2_line.set_data(self.times, self.pt2_data)
        self.pt2_ax.relim()
        self.pt2_ax.autoscale_view()
        self.pt2_canvas.draw()

        self.pt3_line.set_data(self.times, self.pt3_data)
        self.pt3_ax.relim()
        self.pt3_ax.autoscale_view()
        self.pt3_canvas.draw()

        self.pt4_line.set_data(self.times, self.pt4_data)
        self.pt4_ax.relim()
        self.pt4_ax.autoscale_view()
        self.pt4_canvas.draw()

        self.pt5_line.set_data(self.times, self.pt5_data)
        self.pt5_ax.relim()
        self.pt5_ax.autoscale_view()
        self.pt5_canvas.draw()

        self.thrust_line.set_data(self.times, self.thrust_data)
        self.thrust_ax.relim()
        self.thrust_ax.autoscale_view()
        self.thrust_canvas.draw()

        # Update timer with Arduino timestamp
        '''if self.times:'''
        print(elapsed)
        self.timer_label.config(text=f"Elapsed Time: {elapsed:.2f} s")

        # Check alerts using latest values
        if self.pt3_data:
            epd01 = self.pt3_data[-1]
            opd01 = self.pt1_data[-1]
            fpd01 = self.pt4_data[-1]

            alerts = []
            if epd01 > 350:
                alerts.append("Almost too high EPD_01!")
            if epd01 < 150:
                alerts.append("Almost too low EPD_01!")
            if fpd01 > 530:
                alerts.append("Almost too high FPD_01!")
            if opd01 > 825:
                alerts.append("Almost too high OPD_01!")
            self.warning_label.config(text="\n".join(alerts))

        # Check for tail deadline (abort tail saving)
        if (self.tail_deadline is not None) and (time.time() >= self.tail_deadline) and (not self.tail_saving_done):
            self.tail_saving_done = True
            self.running = False
            self.tail_deadline = None
            self.warning_label.config(text=" ")
            try:
                if hasattr(self, "after_id") and self.after_id:
                    self.window.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None
            self.save_data_to_csv()
            messagebox.showinfo("Test Data Saved", "All telemetry data has been saved to test_data.csv")
            return

        # Reschedule next update (50ms for GUI refresh, but data is 100Hz)
        if self.running:
            self.after_id = self.window.after(50, self.update_graphs)
        else:
            self.after_id = None

    def save_data_to_csv(self):
        # Add metadata rows
        data = []
        data.append(["# Test Metadata", ""])
        data.append(["Test Date", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

        if self.abort_time is not None:
            data.append(["Abort Time (s)", f"{self.abort_time:.3f}"])
        else:
            data.append(["Abort Time (s)", "N/A - Test completed normally"])

        data.append(["Post-Abort Tail Duration (s)", f"{self.POST_ABORT_TAIL_S:.1f}"])
        data.append(["Total Data Points", str(len(self.all_data))])
        data.append(["", ""])
        data.append(["# Sensor Data", ""])

        # Add sensor data
        sensors = {"OPD_01": [], "OPD_02": [], "EPD_01": [], "FPD_01": [], "FPD_02": [], "THRUST": []}
        i = 0
        for row in self.all_data:
            t = self.times[i]
            sensors["OPD_01"].append(f"{t:.2f}:{row[0]}")
            sensors["OPD_02"].append(f"{t:.2f}:{row[1]}")
            sensors["EPD_01"].append(f"{t:.2f}:{row[2]}")
            sensors["FPD_01"].append(f"{t:.2f}:{row[3]}")
            sensors["FPD_02"].append(f"{t:.2f}:{row[4]}")
            sensors["THRUST"].append(f"{t:.2f}:{row[5]}")
            i += 1

        for sensor, pairs in sensors.items():
            data.append([sensor, ", ".join(pairs)])

        df = pd.DataFrame(data, columns=["Sensor", "Time"])
        csv_filename = "test_data.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Data saved to {csv_filename}.")


if __name__ == "__main__":
    sys_health = System_Health()
    SIMULATION = False
    if SIMULATION:
        tel = FakeTelemetry(sys_health)
    else:
        tel = Telemetry(sys_health)
    window = GUI()
    window.window.mainloop()
