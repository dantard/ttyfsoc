#!/usr/bin/env python3

import argparse
import sys
import time

import readchar
import serial


def main():
    parser = argparse.ArgumentParser(description="Send message over serial port.")
    parser.add_argument("-t", "--type", type=str, help="rx or tx", default="emitter")
    parser.add_argument("-p", "--port", type=str, help="Serial port name (e.g., COM1, /dev/ttyUSB0)", default="/dev/ttyUSB1")
    parser.add_argument("-b", "--baudrate", type=int, default=9600, help="Baud rate (default: 9600)")
    parser.add_argument("-n", "--frames", type=int, default=-1, help="Number of frames")
    parser.add_argument("-d", "--delay", type=int, default=100, help="Delay ms")
    parser.add_argument("-i", "--interactive", help="Interactive mode", action='store_true')
    args = parser.parse_args()

    # Configure serial port
    ser = serial.Serial(
        port=args.port,  # Change 'COM1' to match your serial port
        baudrate=args.baudrate,  # Change baud rate as needed
        bytesize=serial.EIGHTBITS,  # Default is eight data bits
        parity=serial.PARITY_NONE,  # Specify parity here
        stopbits=serial.STOPBITS_ONE,  # Specify stop bits here
        timeout=5
    )
    # Open the serial port
    try:
        ser.open()
    except:
        ser.close()
        ser.open()

    if args.type == "emitter":
        if args.interactive:
            print("*** Interactive mode")
            while True:
                try:
                    key = readchar.readkey()
                except:
                    sys.exit(0)
                message_bytes = key.encode('utf-8')
                ser.write(message_bytes)
                print(key, end="")
                sys.stdout.flush()

        else:
            count = 0
            while count < args.frames or args.frames == -1:
                message = chr(65 + count % 26)
                message_bytes = message.encode('utf-8')
                ser.write(message_bytes)
                count += 1
                time.sleep(float(args.delay) / 1000.0)
                print("Sending frame #{:8d}".format(count), end="\r")
    else:

        received, sent, total_lost = 0, 0, 0
        prev_serial = -1
        while True:
            try:
                byte = ser.read()
            except:
                sys.exit(0)

            if byte:
                try:
                    character = byte.decode('utf-8')
                except:
                    continue
                if args.interactive:
                    print(character, end="")
                    sys.stdout.flush()

                else:
                    # Decode the byte to a character
                    frame_serial = ord(character)

                    if prev_serial == -1:
                        prev_serial = frame_serial - 1

                    # Print the received character
                    if prev_serial > frame_serial:
                        lost = 26 - (prev_serial - frame_serial) - 1
                    else:
                        lost = frame_serial - prev_serial - 1
                    sent += lost + 1
                    total_lost += lost
                    received = received + 1

                    prev_serial = frame_serial
                    print("Received frame # {:6d}, sent: {:6d}, received: {:6d}, lost: {:4d} ({:3.1f}%)".format(frame_serial, sent, received, total_lost,
                                                                                                                total_lost / sent * 100), end="\r")

    # Close the serial port
    ser.close()

    pass


if __name__ == "__main__":
    main()
