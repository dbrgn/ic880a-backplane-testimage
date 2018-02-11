import time
import RPi.GPIO as g
import smbus

import adc
import sht21

LED_R = 36
LED_Y = 38
LED_B = 40
BTN = 32

# SHT21 config
SHT21_DEV_REG = '/sys/bus/i2c/devices/i2c-1/new_device'
SHT21_DEV_REG_PARAM = 'sht21 0x40'
SHT21_DEV_TMP = '/sys/class/hwmon/hwmon0/temp1_input'
SHT21_DEV_HUM = '/sys/class/hwmon/hwmon0/humidity1_input'

# ADC I2C address and voltage dividers
ADC_DEVICE_ADDRESS = 0x68
ADC_DIVIDER_R1 = 6800
ADC_DIVIDER_R2 = 3600
ADC_DIVIDER_R3 = 470

# Connect to SMBus (I2C)
bus = smbus.SMBus(1)

# Set up GPIO
g.setmode(g.BOARD)
g.setup(LED_R, g.OUT)
g.setup(LED_Y, g.OUT)
g.setup(LED_B, g.OUT)
g.setup(BTN, g.IN, pull_up_down=g.PUD_UP)

print('=== iC880A Backplane Test Program ===\n')

print('Turning on LEDs...')
g.output(LED_R, g.HIGH)
time.sleep(0.5)
g.output(LED_Y, g.HIGH)
time.sleep(0.5)
g.output(LED_B, g.HIGH)

print('\nWaiting for button...')
try:
    g.wait_for_edge(BTN, g.FALLING)
except KeyboardInterrupt:
    print('Aborted.')
    pass

g.output(LED_R, g.LOW)
g.output(LED_Y, g.LOW)
g.output(LED_B, g.LOW)

if input('\nTest sensors? [y/n] ').strip() == 'y':

    print('Initializing sensor...')
    sht = sht21.SHT21(device_number=1)

    print('Reading temperature... ', end='')
    temperature = sht.read_temperature()
    print(temperature)

    print('Reading humidity... ', end='')
    humidity = sht.read_humidity()
    print(humidity)

    print('Initializing ADC...')
    config = adc.START_CONVERSION | adc.CONVERSION_MODE_ONESHOT \
        | adc.SAMPLE_RATE_15SPS | adc.PGA_GAIN_1
    bus.write_byte(ADC_DEVICE_ADDRESS, config)

    # Wait a bit for the measurement to finish
    time.sleep(0.15)

    # Read measurement
    data = bus.read_i2c_block_data(ADC_DEVICE_ADDRESS, 0x00, 3)
    value = (data[0] << 8) + data[1]

    # Calculate voltage for the specified bit of accuracy
    def get_voltage(measurement, bit):
        v2 = measurement * adc.ADC_REF / (2**bit)
        total_r = ADC_DIVIDER_R1 + ADC_DIVIDER_R2 + ADC_DIVIDER_R3
        return v2 / (ADC_DIVIDER_R2 / total_r) * 2

    print('ADC value is %d/%d' % (value, 2**16))
    print('ADC voltage is %.4f V' % (get_voltage(value, 16) / 1000))


print('\n=== DONE! ===')

g.cleanup()
