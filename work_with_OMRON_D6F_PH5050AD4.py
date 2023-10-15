# Imports
import machine
from machine import Pin
import time

def i2c_write_reg(i2c, i2c_addr, i2c_byte_array):
    # Start, followed by the i2c address, register address, and value
    temp = bytearray([(i2c_addr << 1) + 0])
    temp.extend(i2c_byte_array)
    i2c.start()
    a = i2c.write(temp)
    i2c.stop()
    
    if 1 == 0:
        # Expected number of acknowledges
        print("Expect " + str(1 + len(i2c_byte_array)) + ", got: " + str(a))

def i2c_read_reg(i2c, i2c_addr, buf):
    i2c.start()
    
    a1 = i2c.write(bytearray([(i2c_addr << 1) + 0, 0x07]))

    i2c.start()
    
    a2 = i2c.write(bytearray([(i2c_addr << 1) + 1]))

    i2c.readinto(buf)
    
    i2c.stop()
    
    if 1 == 0:
        # Expected number of acknowledges
        print("Expect 2, got: " + str(a1) + ", Expect 1, got: " + str(a2))



# Create I2C object
# Use I2C 0
# scl and sda are connected to GP17 and GP16 respectively
# Frequency is set to 100 000 Hz
i2c = machine.SoftI2C(scl=machine.Pin(27), sda=machine.Pin(26), freq=100000)

# Print out any addresses found
devices = i2c.scan()

# Expect 0x6c
if devices:
    for d in devices:
        print("Found:\t" + hex(d))
        

# Address of the OMRON D6F-PH5050AD4 mems differential pressure sensor
i2c_addr = 0x6C

# Initialize the pressure sensor
i2c_write_reg(i2c, i2c_addr, bytearray([0xb, 0]))

# A byte array for reading
read_back_array = bytearray([0, 0])

# Print update
temp_print = "-\\|/"
temp_print_ii = 0

while True:
    
    # Trigger data
    i2c_write_reg(i2c, i2c_addr, bytearray([0, 0xd0, 0x40, 0x18, 0x06]))
    
    # Wait for acquire
    time.sleep(0.1)
    
    # Ask for data
    i2c_write_reg(i2c, i2c_addr, bytearray([0, 0xd0, 0x51, 0x2c]))
    
    # Read it
    i2c_read_reg(i2c, i2c_addr, read_back_array)
    
    # print(str(read_back_array[0]) + ", " + str(read_back_array[1]))
    
    calc_val = (((read_back_array[0] << 8) + read_back_array[1]) - 1024.0) * 1000.0 / 60000.0 - 500.0
    
    print(temp_print[temp_print_ii] + " " + str(calc_val) + " Pa")
    temp_print_ii = (temp_print_ii + 1) % 4
    
    time.sleep(1)
