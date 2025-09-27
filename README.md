# BLP_Software_2025-26

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

## Contributing
1. Create a branch: `git checkout -b feature/<short-name>`
2. Make small, readable commits with clear messages
3. Open a PR describing:
   - What changed
   - How to test it  
   - Any safety impact

## Future Documentation Structure
```
docs/
  protocol_uart.md        ← communication specs and examples
  interlocks_safety.md    ← E-stop, permissives, abort states  
  runbook_teststand.md    ← setup checklist and procedures
  data_logging.md         ← file formats and retention
  changelog.md            ← version history
```

## Team
**Contributors:** Advika Govindarajan, Emily Jones, Adam Abid, Alex Garcia, Pablo Pedrosa
