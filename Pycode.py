'''
Author: Izuka Ikedionwu

Description: python side to interface with pi and front this is the middle man

features:
- streamlined wifi

Created: 6/28/24
'''

import socket
import numpy
import json
import struct
import serial
from threading import Timer
import time
import uart_code1
from test_sequ_excel import test_sequence

# Global variables
V1 = 0
V2 = 1
V3 = 2
V4 = 3
P1 = 4
P2 = 5
P3 = 6
P4 = 7

C = 4
T = 5
CS = 6
A = 7


class System_Health:
    '''Shared Data'''
    py_stats = {}
    pi_stats = {}
    sys_stats = {}

    py_stats['init wifi connection'] = 'null'
    py_stats['wifi message tx'] = 'null'
    py_stats['wifi message rx'] = 'null'
    py_stats['v1 open command'] = 'null'
    py_stats['v2 open command'] = 'null'
    py_stats['v3 open command'] = 'null'
    py_stats['v4 open command'] = 'null'
    py_stats['v5 open command'] = 'null'
    py_stats['coil on command'] = 'null'
    py_stats['cal command'] = 'null'
    py_stats['test command'] = 'null'
    py_stats['BM command'] = 'null'

    pi_stats["valve 1 fb"] = 'null'
    pi_stats["valve 2 fb"] = 'null'
    pi_stats["valve 3 fb"] = 'null'
    pi_stats["valve 4 fb"] = 'null'
    pi_stats["valve 5 fb"] = 'null'
    pi_stats["coil fb"] = 'null'
    pi_stats["pt 1 fb"] = 'null'
    pi_stats["pt 2 fb"] = 'null'
    pi_stats["pt 3 fb"] = 'null'
    pi_stats["pt 4 fb"] = 'null'
    pi_stats["pt 5 fb"] = 'null'
    pi_stats["lc fb"] = 'null'
    pi_stats["thermo 1 fb"] = 'null'
    pi_stats["thermo 2 fb"] = 'null'
    pi_stats["abort pt 1 "] = 'null'
    pi_stats["abort pt 2 "] = 'null'
    pi_stats["abort pt 3 "] = 'null'
    pi_stats["abort pt 4 "] = 'null'
    pi_stats["abort pt 5 "] = 'null'
    pi_stats["abort pt 6 "] = 'null'
    py_stats['cal command fb'] = 'null'
    py_stats['test command fb'] = 'null'
    py_stats['BM command fb'] = 'null'

    sys_stats = {}
    sys_stats.update(py_stats)
    sys_stats.update(pi_stats)

    def get_pi_status(self):
        return self.pi_stats

    def get_py_status(self):
        return self.py_stats

    @classmethod
    def get_sys_status(self):
        id = 0
        keys = list(self.sys_stats.keys())
        values = list(self.sys_stats.values())

        max_key_length = max(len(key) for key in keys)

        for i in range(len(keys)):
            print(f'{keys[i].ljust(max_key_length)} : {values[i]}')
        return self.sys_stats


class Wifi_Host:
    def __init__(self, port):
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to external IP (Google DNS)
        ip = s.getsockname()[0]
        s.close()
        print(ip)
        self.host = ip
        self.port = port
        self.server_socket = None
        self.connection = None
        self.addy = None
        '''
        pass

    def send_command(self, d):
        '''
        telemetry packet:
        [heartbeat][data layer][aborts][status data]
        '''
        sent = self.connection.sendall(d)
        System_Health.py_stats["wifi message tx"] = 'good'

        if (sent == 0):
            System_Health.py_stats["wifi message tx"] = 'bad'
            raise RuntimeError("socket connection broken at sent")
        return 0

    def recieve_data(self):
        '''
        telemetry packet:
        [heartbeat][data layer][status data]
        '''
        packet_size = 1024
        self.data = self.connection.recv(packet_size)

        if (self.data == ''):
            System_Health.py_stats["wifi message rx"] = 'bad'
            raise RuntimeError("did not recieve packet")
        else:
            System_Health.py_stats["wifi message rx"] = 'good'

        return self.data


class Telemetry:
    def __init__(self, sys):
        self.heartbeat = -49
        self.coil_speed = 80
        self.data = [[0], [0], [0], [0], [0], [0], [0], [0]]
        self.sys = sys
        self.data_packet = [0, 0, 0, 0, 0, 0, 0, 0]
        self.rx_data = []

        # Start background reader for 100Hz CSV streaming
        try:
            uart_code1.start_reader()
            print("100Hz telemetry reader started")
        except Exception as e:
            print(f"Warning: Could not start reader: {e}")

    def set_coil(self, ms):
        self.coil_speed = ms
        self.data_packet[CS] = [ms]
        return 0

    def send_data(self):
        payload = []
        for x in self.data_packet:
            if isinstance(x, list) and len(x) == 1:
                payload.append(str(x[0]))
            else:
                payload.append(str(x))
        uart_code1.send_message(''.join(payload))
        return 0

    def get_data(self):
        """
        Get telemetry data from the queue (non-blocking).
        Returns: [t_ms, OPD01, OPD02, EPD01, FPD01, FPD02, THRUST]

        For backward compatibility with GUI, we reorder to match expected format:
        [OPD02, OPD01, EPD01, FPD01, FPD02, THRUST, t_ms]
        """
        frame = uart_code1.get_frame_nowait()
        if frame is None:
            raise RuntimeError("No frame available")

        # Frame format from Arduino: [t_ms, OPD01, OPD02, EPD01, FPD01, FPD02, THRUST]
        t_ms, opd01, opd02, epd01, fpd01, fpd02, thrust = frame

        # Return in format GUI expects: [OPD02, OPD01, EPD01, FPD01, FPD02, THRUST]
        # Plus timestamp as 7th element
        return [opd02, opd01, epd01, fpd01, fpd02, thrust, t_ms]

    def open_valve(self, num):
        if(num == V1):
            self.data_packet[num] = [1]
        if(num == V2):
            self.data_packet[num] = [2]
        if(num == V3):
            self.data_packet[num] = ['3']
        if(num == V4):
            self.data_packet[num] = [4]

        System_Health.py_stats["v f'{num} open command"] = 'good'
        return 0

    def close_valve(self, num):
        if(num == V1):
            self.data_packet[num] = ["!"]
        if(num == V2):
            self.data_packet[num] = ["@"]
        if(num == V3):
            self.data_packet[num] = ["#"]
        if(num == V4):
            self.data_packet[num] = ["$"]
        System_Health.py_stats["v{num} open command"] = 'bad'
        return 0

    def ignite(self):
        """Full ignition sequence: open FV03 + OV03 + fire spark"""
        uart_code1.send_message('D')
        System_Health.py_stats["ignition command"] = 'good'
        return 0

    def start_test(self):
        print("*start test- > needs to be finished")
        return 0

    def abort(self):
        self.data_packet[V3] = ["#"]
        self.data_packet[V1] = [1]
        self.data_packet[V4] = ["$"]
        time.sleep(0.5)
        self.data_packet[V2] = ["@"]
        return 0

    def upload_test_sequence(self, file_path):
        ts = test_sequence(file_path)
        td = ['TEST']
        td = ts.parse_test()
        BT.send_data(self.sock, td)
        td = ts.parse_abort_limit()
        BT.send_data(self.sock, td)


class Metrics:
    def __init__(self):
        print("metrics")


if __name__ == "__main__":
    for i in range(2):
        sys = System_Health
        tel = Telemetry(sys)























            

