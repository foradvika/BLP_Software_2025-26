import serial
import time
import re
import queue
import threading

arduino_port = '/dev/ttyACM0'
baud_rate = 115200  # Keep at 115200

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=0.02)
    print(f"Connected to Arduino on port {arduino_port}")
except serial.SerialException as e:
    print(f"Error connecting to the Arduino: {e}")
    exit()

time.sleep(2)

# CSV line format: t_ms,OPD01,OPD02,EPD01,FPD01,FPD02,THRUST
# Matches lines with 7 comma-separated float values
_line_re = re.compile(r"^\s*(-?\d+(?:\.\d+)?)(?:\s*,\s*(-?\d+(?:\.\d+)?)){6}\s*$")

_q = None
_reader_started = False

def _ensure_reader():
    """Ensure background reader thread is started"""
    global _q, _reader_started
    if _reader_started:
        return

    _q = queue.Queue(maxsize=5000)  # Buffer up to 5000 frames (~50s at 100Hz)

    def _reader():
        """Background thread that continuously reads CSV lines from Arduino"""
        frame_count = 0
        last_report = time.time()

        while True:
            try:
                line = ser.readline().decode('latin1', 'ignore').strip()
                if not line:
                    continue

                # Only accept valid CSV format
                if not _line_re.match(line):
                    print(f"[DEBUG] Invalid CSV line: {line}")
                    continue

                # Parse CSV: t_ms,OPD01,OPD02,EPD01,FPD01,FPD02,THRUST
                vals = [float(x) for x in line.split(',')]

                # Put in queue (non-blocking, drop if full)
                try:
                    _q.put(vals, timeout=0.01)
                    frame_count += 1

                    # Report rate every second
                    if time.time() - last_report >= 1.0:
                        print(f"[DEBUG] Receiving at {frame_count} Hz")
                        frame_count = 0
                        last_report = time.time()

                except queue.Full:
                    # Drop oldest frame if queue is full
                    print("[DEBUG] Queue full! Dropping old frame")
                    try:
                        _q.get_nowait()
                        _q.put(vals, timeout=0.01)
                    except:
                        pass
            except Exception as e:
                # Ignore parsing errors, continue reading
                print(f"[DEBUG] Parse error: {e}, line: {line}")
                continue

    # Start daemon thread
    threading.Thread(target=_reader, daemon=True).start()
    _reader_started = True
    print("Background CSV reader started at 100Hz")

def start_reader():
    """Start the background reader thread and return the queue"""
    _ensure_reader()
    return _q

def get_frame_nowait():
    """Get the most recent frame without blocking. Returns None if no data available."""
    _ensure_reader()
    try:
        return _q.get_nowait()
    except queue.Empty:
        return None

def send_message(message):
    """Send valve control commands to Arduino (simplified, no delays)"""
    ser.reset_output_buffer()
    for char in message:
        if char != '0':  # Only send non-zero commands
            ser.write(char.encode())
    ser.flush()
