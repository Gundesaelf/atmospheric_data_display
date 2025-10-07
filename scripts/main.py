# IMPORTS
from machine import Pin, I2C
from utime import sleep
import bme280_float
import ssd1306

# Initialize I2C and bme280_float classes
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
bme = bme280_float.BME280(i2c=i2c, address=0x76)

# Set up display settings
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# MAIN FUNC
def main():
    oled.fill(0)
    oled.text('Atmospheric Data', 0, 0)
    oled.text('=' * 16, 0, 10)
    oled.show()
    sleep(0.5)

    # Fake loading screen
    for i in range(0, 4):
        oled.fill(0)
        oled.text('Atmospheric Data', 0, 0)
        oled.text('=' * 16, 0, 10)
        oled.text('acquiring' + '.' *(i), 0, 45)
        oled.show()
        sleep(1)
    sleep(0.5)

    # The real meat & potatoes
    try:
        while True:
            temp_c, pressure, humidity = bme.values

            temp_c = round(float(temp_c.rstrip('C')), 2)
            pressure = int(float(pressure.rstrip('hPa')))
            humidity = int(float(humidity.rstrip('%')))

            temp_f = int(temp_c * 9 / 5 + 32)

            oled.fill(0)

            # Header (yellow)
            oled.text('Atmospheric Data', 0, 0)
            oled.text('=' * 16, 0, 10)

            # Body (blue)
            oled.text(f'Temp: {temp_f}F', 0, 25)
            oled.text(f'hPa: {pressure}', 0, 35)
            oled.text(f'Humidity: {humidity}%', 0, 45)

            oled.show()

            sleep(3) # update every 3s

    except KeyboardInterrupt:
        oled.poweroff()
        print('User terminated program')

# MAINLOOP
if __name__ == '__main__':
    main()
