#!/usr/bin/python
#This program handles reading the output of the various sensor and writing the output
#to a f
import time, sys, pyinotify

class EventHandler(pyinotify.ProcessEvent):
    def my_init(self, file_object=sys.stdout):
        self._file_object = file_object

    def process_default(self, event):
        with open('/sys/bus/iio/devices/iio:device1/in_accel_x_raw', 'r') as rawXAccelFile, open('/sys/bus/iio/devices/iio:device1/in_accel_scale', 'r') as accelScaleFile, open('/sys/bus/iio/devices/iio:device2/in_pressure_raw', 'r') as rawPressureFile, open('/sys/bus/iio/devices/iio:device2/in_pressure_scale', 'r') as pressureScaleFile, open('/sys/bus/iio/devices/iio:device2/in_temp_offset', 'r') as tempOffsetFile, open('/sys/bus/iio/devices/iio:device2/in_temp_raw', 'r') as rawTempFile, open('/sys/bus/iio/devices/iio:device2/in_temp_scale', 'r') as tempScaleFile:
            main(dataFile,  rawXAccelFile,  accelScaleFile,  rawPressureFile,  pressureScaleFile,  tempOffsetFile,  rawTempFile,  tempScaleFile)

def main(dataFile,  rawXAccelFile,  accelScaleFile,  rawPressureFile,  pressureScaleFile,  tempOffsetFile,  rawTempFile,  tempScaleFile):
    print "Starting data collection"
    rawXAccel = rawXAccelFile.read()
    accelScale =  accelScaleFile.read()
    rawPressure = rawPressureFile.read()
    pressureScale = pressureScaleFile.read()
    tempOffset = tempOffsetFile.read()
    rawTemp = rawTempFile.read()
    tempScale = tempScaleFile.read()
    try:
        xAccel = int(rawXAccel) * float(accelScale) * 9.81
    except ValueError:
        pass
    try:
        pressure = int(rawPressure) * float(pressureScale) * 10
    except ValueError:
        pass
    try:
        temperature = float(tempOffset) + (int(rawTemp) * float(tempScale))
    except ValueError:
        pass
    try:
        altitude = (1 - ((pressure/1013.25) ** 0.190284)) * 145366.45
    except ValueError:
        pass
    dataFile.write(str(xAccel) + "," + str(pressure) + "," + str(temperature) + "," + str(altitude) + "\n")

def cleanup(dataFile):
    print "Starting cleanup"
    dataFile.close()
    sys.exit(1)

if __name__ == '__main__':
    try:
        dataFile = open("data.csv","w+")
        dataFile.write("Acceleration,Pressure,Temperature,Altitude\n")
        ##while True:
        ##    with open('/sys/bus/iio/devices/iio:device1/in_accel_x_raw', 'r') as rawXAccelFile, open('/sys/bus/iio/devices/iio:device1/in_accel_scale', 'r') as accelScaleFile, open('/sys/bus/iio/devices/iio:device2/in_pressure_raw', 'r') as rawPressureFile, open('/sys/bus/iio/devices/iio:device2/in_pressure_scale', 'r') as pressureScaleFile, open('/sys/bus/iio/devices/iio:device2/in_temp_offset', 'r') as tempOffsetFile, open('/sys/bus/iio/devices/iio:device2/in_temp_raw', 'r') as rawTempFile, open('/sys/bus/iio/devices/iio:device2/in_temp_scale', 'r') as tempScaleFile:
        ##        main(dataFile,  rawXAccelFile,  accelScaleFile,  rawPressureFile,  pressureScaleFile,  tempOffsetFile,  rawTempFile,  tempScaleFile)
        wm = pyinotify.WatchManager()
        notifier = pyinotify.Notifier(wm, EventHandler())
        wm.add_watch('/sys/bus/iio/devices/iio:device1/', pyinotify.ALL_EVENTS)
        wm.add_watch('/sys/bus/iio/devices/iio:device2/', pyinotify.ALL_EVENTS)
        p = EventHandler("data.csv")
        notifier.loop()
    except KeyboardInterrupt:
        cleanup(dataFile)
