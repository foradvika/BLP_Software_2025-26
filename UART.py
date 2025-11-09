import serial
import time

# Set the correct serial port (e.g., '/dev/ttyACM0')
arduino_port = '/dev/ttyACM0'  
baud_rate = 115200 

# Open the serial connection to the Arduino
try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=0.05)
    print(f"Connected to Arduino on port {arduino_port}")
except serial.SerialException as e:
    print(f"Error connecting to the Arduino: {e}")
    exit()

time.sleep(2)  # Wait for the connection to establish

def send_message(message):
    """
    Send a message one character at a time to the Arduino
    with delimiters as per the request (e.g., "[" "H" "," "e" ",").
    """
    ser.reset_output_buffer()
    for char in message:
        # Send '['
        ser.write('['.encode())
        #print(f"Sent: [")
        time.sleep(0.05)
        
        # Send the character
        #print(type(char))
        #print(char)
        ser.write(str(char).encode())
        #print(f"Sent: {char}")
        time.sleep(0.05)
        
        # Send ','
        ser.write(','.encode())  
        #print(f"Sent: ,")
        time.sleep(0.05)

def receive_response():
    """
    read 6 channels with filter, if first line is not number, continue reading.
    """
    import re, time
    _FLOAT_RE = re.compile(r"^-?\d+(?:\.\d+)?$")

    def read_float_line(deadline_s=0.20):
        end = time.time() + deadline_s
        last = ""
        while time.time() < end:
            line = ser.readline().decode('latin1', 'ignore').strip()
            if not line:
                continue
            last = line
            if _FLOAT_RE.match(line):
                return float(line)
            # if log not number, ignore
        raise ValueError(f"Non-numeric/timeout. Last='{last}'")

    rx = []
    ser.reset_input_buffer()  # clean only at start of cycle

    for cmd in (b'5', b'6', b'7', b'8', b'A', b'&'):
        ser.write(cmd); ser.flush()
        rx.append(read_float_line(0.20))

    return rx

    '''
    for i in range(30):  # Check if data is available
        #received_char = ser.read().decode('Latin1')  # Read one byte
        received_char = ser.read()  # Read one byte
        print('HERE')
        rx_data.append(received_char)
    return rx_data
    '''
'''
def main():
    try:
        while True:
            message = "[1,2,3,4,!,@,#,$]"  # Example message to send
            send_message(message)  # Send the message to Arduino

            # Receive the response from Arduino
            time.sleep(1)  # Wait for Arduino to echo back all characters

    except KeyboardInterrupt:
        print("Communication terminated by user.")
    finally:
        if ser.is_open:
            ser.close()  # Close the serial port when done
            print("Serial port closed.")

if __name__ == "
'''
