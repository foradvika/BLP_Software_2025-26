![blp-architecture-flowchart-2](https://github.com/user-attachments/assets/5da6282f-c96b-4e68-948e-d40ed44a78f4)# BLP Test Stand Control Software 2025-26!<svg viewBox="0 0 800 900" xmlns="http://www.w3.org/2000/svg">
  <!-- Define styles -->
  <defs>
    <style>
      .box { fill: white; stroke: #2c3e50; stroke-width: 2; }
      .operator-box { fill: #e8f4fd; stroke: #3498db; stroke-width: 2; }
      .safety-box { fill: #fdeaea; stroke: #e74c3c; stroke-width: 2; }
      .software-box { fill: #f0f8ff; stroke: #5b9bd5; stroke-width: 2; }
      .hardware-box { fill: #fff4e6; stroke: #ff9800; stroke-width: 2; }
      .sensor-box { fill: #e8f5e9; stroke: #4caf50; stroke-width: 2; }
      .actuator-box { fill: #f3e5f5; stroke: #9c27b0; stroke-width: 2; }
      .title-text { font-family: Arial, sans-serif; font-size: 14px; font-weight: bold; fill: #2c3e50; }
      .label-text { font-family: Arial, sans-serif; font-size: 11px; fill: #34495e; }
      .small-text { font-family: Arial, sans-serif; font-size: 9px; fill: #7f8c8d; }
      .arrow { stroke: #2c3e50; stroke-width: 2; fill: none; marker-end: url(#arrowhead); }
      .data-arrow { stroke: #3498db; stroke-width: 2; fill: none; marker-end: url(#data-arrowhead); stroke-dasharray: 5,3; }
    </style>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#2c3e50"/>
    </marker>
    <marker id="data-arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#3498db"/>
    </marker>
  </defs>

  <!-- Title -->
  <text x="400" y="30" text-anchor="middle" class="title-text" style="font-size: 18px;">BLP System Architecture</text>

  <!-- STAKEHOLDERS LAYER -->
  <text x="50" y="70" class="title-text">STAKEHOLDERS</text>
  
  <!-- Test Operator -->
  <rect x="100" y="80" width="140" height="40" rx="5" class="operator-box"/>
  <text x="170" y="100" text-anchor="middle" class="label-text">Test Operator</text>
  <text x="170" y="115" text-anchor="middle" class="small-text">(TO)</text>
  
  <!-- Safety Officer -->
  <rect x="560" y="80" width="140" height="40" rx="5" class="safety-box"/>
  <text x="630" y="100" text-anchor="middle" class="label-text">Safety Officer</text>
  <text x="630" y="115" text-anchor="middle" class="small-text">(SO)</text>

  <!-- SOFTWARE LAYER -->
  <line x1="50" y1="150" x2="750" y2="150" stroke="#e0e0e0" stroke-width="1"/>
  <text x="20" y="170" class="title-text">SOFTWARE LAYER</text>

  <!-- Operator Console -->
  <rect x="60" y="180" width="220" height="100" rx="5" class="software-box"/>
  <text x="170" y="200" text-anchor="middle" class="label-text">Test Control GUI (tkinter)</text>
  <text x="70" y="220" class="small-text">• Live data plots (6 graphs)</text>
  <text x="70" y="235" class="small-text">• CSV test sequence upload</text>
  <text x="70" y="250" class="small-text">• Manual valve toggle buttons</text>
  <text x="70" y="265" class="small-text">• START/ABORT controls</text>

  <!-- Safety Console -->
  <rect x="520" y="180" width="220" height="100" rx="5" class="software-box"/>
  <text x="630" y="200" text-anchor="middle" class="label-text">Safety Console Front-End</text>
  <text x="530" y="220" class="small-text">• Arm/Disarm, E-Stop</text>
  <text x="530" y="235" class="small-text">• Hard limits, permissives</text>
  <text x="530" y="250" class="small-text">• Status dashboard</text>
  <text x="530" y="265" class="small-text">• Alarm & event timeline</text>

  <!-- Run Controller -->
  <rect x="290" y="320" width="220" height="100" rx="5" class="software-box"/>
  <text x="400" y="340" text-anchor="middle" class="label-text">Python Control Logic</text>
  <text x="300" y="360" class="small-text">• Executes CSV test sequences</text>
  <text x="300" y="375" class="small-text">• Safety checks & abort logic</text>
  <text x="300" y="390" class="small-text">• Sends valve/igniter commands</text>
  <text x="300" y="405" class="small-text">• Stores test data to CSV</text>

  <!-- Telemetry Server -->
  <rect x="290" y="460" width="220" height="85" rx="5" class="software-box"/>
  <text x="400" y="480" text-anchor="middle" class="label-text">UART Serial Communication</text>
  <text x="300" y="500" class="small-text">• Serial port /dev/ttyACM0</text>
  <text x="300" y="515" class="small-text">• 115200 baud rate</text>
  <text x="300" y="530" class="small-text">• Character-by-character TX/RX</text>

  <!-- HARDWARE LAYER -->
  <line x1="50" y1="580" x2="750" y2="580" stroke="#e0e0e0" stroke-width="1"/>
  <text x="50" y="600" class="title-text">HARDWARE LAYER</text>

  <!-- Control Box -->
  <rect x="250" y="610" width="300" height="100" rx="5" class="hardware-box"/>
  <text x="400" y="630" text-anchor="middle" class="label-text">Control Box (MCU Board)</text>
  <text x="260" y="650" class="small-text">• MCU (Arduino/Teensy)</text>
  <text x="260" y="665" class="small-text">• Command parser + executor (FSM)</text>
  <text x="260" y="680" class="small-text">• Valve drivers (MOSFETs/relays)</text>
  <text x="260" y="695" class="small-text">• Sensor ADC/amps + Watchdog</text>

  <!-- Sensors -->
  <rect x="60" y="750" width="180" height="90" rx="5" class="sensor-box"/>
  <text x="150" y="770" text-anchor="middle" class="label-text">Sensors</text>
  <text x="70" y="790" class="small-text">• OPD_01/02 (Ox pressure)</text>
  <text x="70" y="805" class="small-text">• EPD_01 (Chamber pressure)</text>
  <text x="70" y="820" class="small-text">• FPD_01/02 (Fuel pressure)</text>
  <text x="70" y="835" class="small-text">• Load cell (thrust)</text>

  <!-- Actuators -->
  <rect x="560" y="750" width="180" height="90" rx="5" class="actuator-box"/>
  <text x="650" y="770" text-anchor="middle" class="label-text">Actuators</text>
  <text x="570" y="790" class="small-text">• NV-02 (N₂ purge)</text>
  <text x="570" y="805" class="small-text">• FV-02/03 (Fuel valve/vent)</text>
  <text x="570" y="820" class="small-text">• OV-03 (Ox vent)</text>
  <text x="570" y="835" class="small-text">• Igniter coil</text>

  <!-- Safety Chain -->
  <rect x="290" y="750" width="220" height="60" rx="5" class="box" style="fill: #ffebee; stroke: #d32f2f;"/>
  <text x="400" y="770" text-anchor="middle" class="label-text">Safety Chain (Hardwired)</text>
  <text x="300" y="790" class="small-text">• E-Stop (latches power)</text>
  <text x="300" y="805" class="small-text">• Key switch (ARM) • Reliefs</text>

  <!-- Arrows -->
  <!-- Stakeholder to Console connections -->
  <path d="M 170 120 L 170 180" class="arrow"/>
  <path d="M 630 120 L 630 180" class="arrow"/>
  
  <!-- Consoles to Run Controller -->
  <path d="M 170 280 L 170 300 L 400 300 L 400 320" class="arrow"/>
  <path d="M 630 280 L 630 300 L 400 300 L 400 320" class="arrow"/>
  
  <!-- Run Controller to Telemetry Server -->
  <path d="M 400 420 L 400 460" class="arrow"/>
  
  <!-- Telemetry Server to Control Box -->
  <path d="M 400 545 L 400 610" class="arrow"/>
  <text x="410" y="575" class="small-text">Serial 115200+</text>
  
  <!-- Control Box to Sensors/Actuators -->
  <path d="M 350 710 L 150 750" class="data-arrow"/>
  <path d="M 450 710 L 650 750" class="arrow"/>
  <path d="M 400 710 L 400 750" class="arrow" stroke="#d32f2f"/>

  <!-- Protocol Examples Box -->
  <rect x="530" y="470" width="240" height="65" rx="3" class="box" style="fill: #fffef0;"/>
  <text x="540" y="485" class="small-text" style="font-weight: bold;">Protocol Examples:</text>
  <text x="540" y="500" class="small-text" style="font-family: monospace;">CMD,seq,valve,open</text>
  <text x="540" y="515" class="small-text" style="font-family: monospace;">SENS,p1,p2,p3,thrust</text>
  <text x="540" y="530" class="small-text" style="font-family: monospace;">ACK,seq / DONE,seq,OK</text>

</svg>[Uploading blp-architecture-flowchart-2.svg…]()


Simple front-end + back-end code to run Baylor Liquid Propulsion's test stand. **Currently runs in simulation** - hardware integration coming next. Built to be safe, modular, and easy for new contributors to jump into.

## What's Built
- **GUI with live plots** - thrust + 5 pressure sensors updating in real-time
- **Valve controls** - buttons to operate valves manually
- **Automated sequences** - upload CSV files to run timed test procedures
- **Data logging** - saves all sensor data to CSV files
- **Simulation mode** - fake telemetry so anyone can run it without hardware
- **Hardware stubs** - UART interface ready for Arduino/Teensy/ESP32

## File Structure
```
guifrontend.py     ← main GUI app (defaults to SIMULATION=True)
pycode.py          ← telemetry/command interface (hardware path, WIP)
UART.py            ← serial communication helpers (WIP)
sketch_sep23a.ino  ← Arduino test sketch for sensors/valves
```

## Quick Start (Simulation Mode)

1. **Install requirements:**
   ```bash
   pip install matplotlib pandas
   ```

2. **Run the GUI:**
   ```bash
   python guifrontend.py
   ```

3. **What you'll see:**
   - 6 plots updating: thrust + OPD_01/02, EPD_01, FPD_01/02
   - Valve control buttons (actions print to console)
   - Hit **ABORT** to save data to `test_data.csv`

4. **Run automated sequences:**
   Create a CSV file like `demo_sequence.csv`:
   ```csv
   Time,Function
   0,Start_Count
   1,NV_02
   2,FV_03
   3,FV_02
   4,OV_03
   5,BLP_Abort
   ```
   Click **Upload File** in the GUI. Each function runs at the specified second.

## Available Test Functions
- `Start_Count` – start timer + plotting
- `NV_02`, `FV_02`, `FV_03`, `OV_03` – toggle named valve open
- `BLP_Abort` – safe shutdown + log data to CSV
- `Spark` – ignition placeholder (no-op in simulation)

Add new functions by extending `function_map` in `guifrontend.py`.

## Hardware Mode (Next Phase)

**To switch from simulation to real hardware:**

1. **In `guifrontend.py`, change:**
   ```python
   SIMULATION = False
   # tel = Telemetry(sys_health)  # wire this up next
   ```

2. **Configure serial settings in `UART.py`:**
   ```python
   arduino_port = '/dev/ttyACM0'  # or 'COMx' on Windows
   baud_rate = 115200             # match your microcontroller
   ```

3. **Communication protocol (draft):**
   - PC sends single bytes: `'5','6','7','8','A','&'`
   - MCU replies with **ASCII float + CRLF** per channel
   - Commands: `O<id>` open valve, `C<id>` close valve, `X` abort
   - **MCU must implement interlocks** - no valve opens without proper conditions

## Safety Requirements

**CRITICAL for hardware mode:**
- **Physical interlocks** - E-stop, permissive relays, pressure limits
- **Software guards** - pressure/time limits in code
- **Latched ABORT** - system must stay in safe vented state after abort
- **All valve operations gated by interlocks on the MCU side**

## Data Logging
After ABORT or exit, the app writes `test_data.csv` with timestamped values for all six channels.

## Team
**Contributors:** Advika Govindarajan, Emily Jones, Adam Abid, Alex Garcia, Pablo Pedrosa
