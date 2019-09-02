import os
import time
import RPi.GPIO as g
import smbus

import adc
import shtcx

# Pins
LED_R = 36
LED_Y = 38
LED_B = 40
BTN = 32

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

# Classification function
def classify(val, minok, maxok, minwarn, maxwarn):
    if minok < val < maxok:
        return 'OK'
    if minwarn < val < maxwarn:
        return 'WARNING'
    return 'ERROR'

print('=== iC880A Backplane Test Program ===\n')

print('Turning on LEDs...')
g.output(LED_R, g.HIGH)
time.sleep(0.2)
g.output(LED_Y, g.HIGH)
time.sleep(0.2)
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

print('\nInitializing SHTC3 sensor...')
shtcx.init()

print('Reading sensor values...')
(temp, humi) = shtcx.read()
prefix = classify(temp, 21, 28, 19, 30)
print('  [%s] Temp: {} C'.format(prefix, temp))
prefix = classify(humi, 30, 70, 20, 80)
print('  [%s] Humi: {} %RH'.format(prefix, humi))

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

millivolt = get_voltage(value, 16)
prefix = classify(millivolt, 498, 512, 495, 520)
print('  [%s] Volt: %.4f V' % (prefix, millivolt / 1000))

print('\n=== DONE! ===')

g.cleanup()

if input('\nShutdown? [Y/n] ').strip() in ['y', '']:
    os.system('halt')
