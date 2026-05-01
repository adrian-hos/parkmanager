import serial

ser = serial.Serial('/dev/ttyUSB0', 115200)

def get_barrier_status():
    ser.write(b'1')
    try:
        result = ser.readline().decode('ascii').strip()
    except:
        return "fail"
    else:
        if result == '1 1':
            return True
        elif result == '1 0':
            return False

def open_barrier():
    ser.write(b'2')
    result = ser.readline().decode('ascii').strip()
    if result == "2 1":
        return True
    elif result == "2 0":
        return False

def close_barrier():
    ser.write(b'3')
    result = ser.readline().decode('ascii').strip()
    if result == "3 1":
        return True
    elif result == "3 0":
        return False

def set_time(time):
    string = f'4 {time}'
    ser.write(string.encode('ascii'))
    print(ser.readline().decode('ascii').strip())