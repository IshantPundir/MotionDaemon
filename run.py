"""
This is the main daemon that will talk to the micro-controller
running MotionDriver.

This essentially creates a serial connection with the MCU and start
a TCP server allowing local clients to talk to it and forward 
commands to MCU
"""
import time
import serial
import argparse

class SerialHub:
    """
    Serial connection with MCU
    """
    def __init__(self, port:str, baudrate:int = 9600, timeout:int = 1) -> None:
        print("Creating a connection....")
        self.ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
        time.sleep(2)
        print("Done!")
        
    def close(self) -> None:
        """Close the serial connection"""
        self.ser.close()

    def send(self, command:str) -> None:
        """Send a command to MCU"""
        if self.ser.isOpen():
            command = command + '\n'
            self.ser.write(command.encode())
            print(f"Send: {command.strip()}")
        else:
            print("Serial port is not open")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=str, default='/dev/ttyUSB0', help="port where MCU is connected")
    args = parser.parse_args()

    hub = SerialHub(port=args.port)
    while True:
        command = input("$. ")
        if command.lower() in ['q', 'quit', 'exit']: break
        hub.send(command)
    
    hub.close()