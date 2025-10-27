import serial
import csv
import time
import os
from datetime import datetime
# === Serial Port Configuration ===
PORT = '/dev/cu.usbmodem112301'   # Change to your Arduino port
BAUDRATE = 250000
TIMEOUT = 1                      # Serial read timeout (seconds)
DURATION = 300                   # Total capture duration (seconds)
PAYLOAD_BITS = 56                # Payload length in bits
TIMEOUT_GAP = 2.0                # If no data for >2s, log TIMEOUT

# === Create output folder with timestamp ===
timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
output_dir = f"SEth_CAN-bus-PDF_rx_{timestamp_str}"
os.makedirs(output_dir, exist_ok=True)

CSV_FILE = os.path.join(output_dir, "data.csv")
TXT_FILE = os.path.join(output_dir, "decoded.txt")

# === Utility Functions ===
def timestamp_now():
    """Return current timestamp in HH:MM:SS.mmm format"""
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def bits_to_ascii_and_hex(bitstring):
    """
    Decode bitstring to ASCII and HEX representation.
    Matches Arduino's array_to_ascii logic (reverse bit order).
    """
    ascii_decoded = ''
    hex_decoded = []
    for i in range(0, len(bitstring), 8):
        chunk = bitstring[i:i+8]
        if len(chunk) == 8:
            val = 0
            for bit in reversed(chunk):  # Reverse bit order
                val = (val << 1) | int(bit)
            hex_decoded.append(f"{val:02X}")
            ascii_decoded += chr(val) if 32 <= val <= 126 else '.'
    return ascii_decoded, ' '.join(hex_decoded)

# === Main Program ===
def main():
    ser = serial.Serial(PORT, BAUDRATE, timeout=TIMEOUT)
    print(f"Listening on {PORT} ({BAUDRATE} baud)")
    print(f"Data will be saved in folder: {output_dir}")
    start_time = time.time()
    last_packet_time = time.time()

    with open(CSV_FILE, 'w', newline='') as csv_file, open(TXT_FILE, 'w') as txt_file:
        writer = csv.writer(csv_file)
        writer.writerow(['timestamp', 'bits', 'ascii', 'hex', 'status'])

        while time.time() - start_time < DURATION:
            line = ser.readline().decode(errors='ignore').strip()

            # Check for timeout
            if line == '':
                if time.time() - last_packet_time > TIMEOUT_GAP:
                    ts = timestamp_now()
                    print(f"{ts} -> [TIMEOUT]")
                    writer.writerow([ts, '', '', '', 'TIMEOUT'])
                    last_packet_time = time.time()
                continue

            # Process only binary strings of correct length
            if all(c in '01' for c in line) and len(line) == PAYLOAD_BITS:
                ascii_decoded, hex_decoded = bits_to_ascii_and_hex(line)
                ts = timestamp_now()

                # Print to console
                print(f"{ts} -> {line} | ASCII: {ascii_decoded} | HEX: {hex_decoded}")

                # Write to CSV
                writer.writerow([ts, line, ascii_decoded, hex_decoded, 'OK'])

                # Write ASCII to TXT
                txt_file.write(ascii_decoded + '\n')

                last_packet_time = time.time()

    ser.close()
    print(f"\n✅ Done. Files saved in folder: {output_dir}")

if __name__ == '__main__':
    main()