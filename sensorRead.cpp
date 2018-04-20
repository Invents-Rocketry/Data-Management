/***************************************************************************
  This is a library for the Adafruit 9DOF Breakout

  Designed specifically to work with the Adafruit 9DOF Breakout:
  http://www.adafruit.com/products/1714

  This class does not communicate directly with the hardware, but
  converts raw readings (X-Y-Z magnitudes) into more useful values in
  degrees (roll, pitch, heading).

  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing products
  from Adafruit!

  Written by Kevin Townsend for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ***************************************************************************/

#include "Lib/I2C/I2CDevice.h"
#include <stdio.h>

/*
 * Simplest implementation of a usable class extending an I2C device
 */
class LSM303DLHC : public abI2C::I2CDevice {
public:
    LSM303DLHC( ) { }
    void SetDeviceAddress( unsigned char _DeviceAddress ){ this->DeviceAddress = _DeviceAddress; }
    void SetBusId( int _BusId ) { this->BusId = _BusId; }
};

class LSM303_Accelerometer : public LSM303DLHC{
public:
    LSM303_Accelerometer( unsigned char _DeviceAddress, int _BusId ) {
        this->SetDeviceAddress( _DeviceAddress );
        this->SetBusId( _BusId );
        this->InitDevice( );
    }
};
class LSM303_Magnetometer : public LSM303DLHC{
	public:
	LSM303_Magnetometer(unsigned char _DeviceAddress, int _BusID) {
		this->SetDeviceAddress(_DeviceAddress);
		this->SetBusId(_BusID);
		this->InitDevice();
	}
};

int main(void) {
	
	accel.begin();
	mag.begin();
	FILE *dataFile = fopen('sensorData.csv', 'w+');
	fprintf(dataFile, 'Acceleration (x),Acceleration (y), Acceleration(z),Magnetometer (x),Magnetometer(y),Magnetometer(z)'
			+'Orientation,Pitch,Heading\n');
	
	
	sensors_event_t accel_event;
	sensors_event_t mag_event;
	sensors_vec_t   orientation;

	/* Read the accelerometer and magnetometer */
	accel.getEvent(&accel_event);
	mag.getEvent(&mag_event);

	  /* Use the new fusionGetOrientation function to merge accel/mag data */  
	  if (dof.fusionGetOrientation(&accel_event, &mag_event, &orientation))
	  {
		  fprintf(dataFile, '%f,%f,%f,%f,%f,%f,%f,%f,%f\n', accel_event.acceleration.x,accel_event.acceleration.y,accel_event.acceleration.z,
		  mag_event.magnetic.x,mag_event.magnetic.y,mag_event.magnetic.z, orientation.roll, orientation.pitch, orientation.heading);
	  }

}
