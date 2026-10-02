#!/usr/bin/env python3
"""
Simple serial port monitor. By Claude Sonnet 5.5 Medium

Install:  pip install pyserial

Examples:
  python serial_monitor.py --list
  python serial_monitor.py COM3 -b 115200
  python serial_monitor.py /dev/ttyUSB0 -b 9600 --hex --log session.log
  python serial_monitor.py /dev/ttyUSB0 --eol crlf      # type text + Enter to send
"""
import argparse
import sys
import threading
from datetime import datetime

import serial
from serial.tools import list_ports

EOL = {"none": b"", "lf": b"\n", "cr": b"\r", "crlf": b"\r\n"}
PARITY = {"N": serial.PARITY_NONE, "E": serial.PARITY_EVEN, "O": serial.PARITY_ODD,
          "M": serial.PARITY_MARK, "S": serial.PARITY_SPACE}
STOPBITS = {"1": serial.STOPBITS_ONE, "1.5": serial.STOPBITS_ONE_POINT_FIVE,
            "2": serial.STOPBITS_TWO}


def list_available_ports():
    ports = sorted(list_ports.comports())
    if not ports:
        print("No serial ports found.")
        return
    for p in ports:
        print(f"{p.device:<20} {p.description}")


def ts():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


class Monitor:
    def __init__(self, ser, hex_mode, show_ts, log_file):
        self.ser = ser
        self.hex_mode = hex_mode
        self.show_ts = show_ts
        self.log = log_file
        self.stop = threading.Event()
        self.lock = threading.Lock()
        self.line_buf = bytearray()

    def emit(self, direction, text):
        prefix = f"[{ts()}] " if self.show_ts else ""
        line = f"{prefix}{direction} {text}"
        with self.lock:
            print(line, flush=True)
            if self.log:
                self.log.write(line + "\n")
                self.log.flush()

    def handle_rx(self, data: bytes):
        if self.hex_mode:
            hexpart = " ".join(f"{b:02X}" for b in data)
            asc = "".join(chr(b) if 32 <= b < 127 else "." for b in data)
            self.emit("RX", f"{hexpart}  |{asc}|")
            return
        # Text mode: emit complete lines, keep partial data buffered
        self.line_buf.extend(data)
        while b"\n" in self.line_buf or b"\r" in self.line_buf:
            idx = min(i for i in (self.line_buf.find(b"\n"), self.line_buf.find(b"\r")) if i >= 0)
            line = bytes(self.line_buf[:idx])
            del self.line_buf[:idx + 1]
            if line:
                self.emit("RX", line.decode("utf-8", errors="replace"))

    def reader(self):
        while not self.stop.is_set():
            try:
                data = self.ser.read(self.ser.in_waiting or 1)
            except serial.SerialException as e:
                self.emit("ERR", f"Serial error: {e}")
                self.stop.set()
                break
            if data:
                self.handle_rx(data)

    def run(self, eol):
        t = threading.Thread(target=self.reader, daemon=True)
        t.start()
        print("Monitoring. Type text + Enter to send, Ctrl+C to quit.")
        try:
            for line in sys.stdin:
                if self.stop.is_set():
                    break
                payload = line.rstrip("\r\n").encode() + eol
                self.ser.write(payload)
                self.emit("TX", payload.decode("utf-8", errors="replace").rstrip("\r\n"))
        except KeyboardInterrupt:
            pass
        finally:
            self.stop.set()
            t.join(timeout=1)


def main():
    ap = argparse.ArgumentParser(description="Serial port monitor")
    ap.add_argument("port", nargs="?", help="e.g. COM3 or /dev/ttyUSB0")
    ap.add_argument("-l", "--list", action="store_true", help="list available ports and exit")
    ap.add_argument("-b", "--baud", type=int, default=9600)
    ap.add_argument("--bytesize", type=int, choices=[5, 6, 7, 8], default=8)
    ap.add_argument("--parity", choices=PARITY.keys(), default="N")
    ap.add_argument("--stopbits", choices=STOPBITS.keys(), default="1")
    ap.add_argument("--hex", action="store_true", help="show received data as hex + ASCII")
    ap.add_argument("--no-ts", action="store_true", help="hide timestamps")
    ap.add_argument("--eol", choices=EOL.keys(), default="lf", help="line ending appended to sent text")
    ap.add_argument("--log", metavar="FILE", help="also write output to FILE")
    args = ap.parse_args()

    if args.list or not args.port:
        list_available_ports()
        return

    try:
        ser = serial.Serial(
            port=args.port, baudrate=args.baud, bytesize=args.bytesize,
            parity=PARITY[args.parity], stopbits=STOPBITS[args.stopbits], timeout=0.1,
        )
    except serial.SerialException as e:
        sys.exit(f"Could not open {args.port}: {e}")

    log_file = open(args.log, "a", encoding="utf-8") if args.log else None
    print(f"Opened {args.port} @ {args.baud} {args.bytesize}{args.parity}{args.stopbits}")
    try:
        Monitor(ser, args.hex, not args.no_ts, log_file).run(EOL[args.eol])
    finally:
        ser.close()
        if log_file:
            log_file.close()


if __name__ == "__main__":
    main()
