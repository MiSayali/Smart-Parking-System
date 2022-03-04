import schema
from boltiot import Bolt
import json
from boltiot.requesting import request_from
import sqlite3


maxDistance = 200

#WRBolt is derived from Bolt
class WRBolt(Bolt):
    def __init__(self, api_key, device_id):
        #call init function of super class
        super().__init__(api_key, device_id)

    def serialWR(self, data):
        """
        Writes the data to the serial port and reads back the reply.

        :param str data: in bits per second (baud)

        :returns:  request status and data read from serial port
        :example: {"success": "1", "value": "data"}

        :rtype: JSON
        """
        return request_from('http://cloud.boltiot.com/remote/{}/serialWR?data={}&deviceName={}', self.api_key, data, self.device_id)

#check status of all the sensors in a parking lot
def CheckAll():     
    for lot in schema.ParkingLot.select():
        for floor in lot.floors:
            for spot in floor.spots:
                if spot.sensor.virtual:
                    empty = spot.sid % (3 + floor.fid) == 0
                else:
                    reading = GetSensorReading(spot.sensor.apiKey, spot.sensor.sensorId)
                    print("Distance: ", reading)
                    #distance greater than maxDistance indicates that the spot is empty
                    empty = reading > maxDistance
                if empty:
                    #Car not present
                    #Check if the spot was full in the previous iteration
                    if not spot.empty:
                        floor.freeSpaces += 1
                        if not spot.sensor.virtual:
                            MarkEmpty(spot.sensor.apiKey, spot.sensor.sensorId)
                        spot.empty = True
                else:
                    #Car present
                    #Check if car the spot was empty in the previous iteration
                    if spot.empty:
                        floor.freeSpaces -= 1
                        if not spot.sensor.virtual:
                            MarkFull(spot.sensor.apiKey, spot.sensor.sensorId)
                        spot.empty = False

def GetState():
    state = []
    i = 0
    con = sqlite3.connect('data.db')
    for lot in schema.ParkingLot.select():
        state.append({})
        state[i]["address"] = lot.address
        c = con.cursor()
        c.execute('select * from floor where parking_lot_id = ?', (lot.id, ))
        for row in c:
            state[i]["floor%d" % row[1]] = row[2]
        c.close()
        i += 1
    con.close()
    return state

#Function for getting sensor reading from the bolt cloud
def GetSensorReading(apiKey, sensorId):
    #create object of WRBolt class
    mybolt = WRBolt(apiKey, sensorId)
    read_data = mybolt.serialWR("getReading")
    reading = json.loads(read_data)
    #value is returned in the form of dictionary. Select the value part
    reading = int(reading['value'])
    return reading

def MarkEmpty(apiKey, sensorId):
    mybolt = Bolt(apiKey, sensorId)
    mybolt.digitalWrite(1, 'HIGH')

def MarkFull(apiKey, sensorId):
    mybolt = Bolt(apiKey, sensorId)
    mybolt.digitalWrite(1, 'LOW')

