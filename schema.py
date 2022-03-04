from sqlalchemy import null
import sqlobject
import os

#Table definitions
class ParkingLot(sqlobject.SQLObject):          
    address = sqlobject.StringCol()
    floors = sqlobject.MultipleJoin('Floor')

class Floor(sqlobject.SQLObject):
    fid = sqlobject.IntCol()
    freeSpaces = sqlobject.IntCol()
    spots = sqlobject.MultipleJoin('Spot')
    parkingLot = sqlobject.ForeignKey('ParkingLot')

class Spot(sqlobject.SQLObject):
    sid = sqlobject.IntCol()
    empty = sqlobject.BoolCol()
    sensor = sqlobject.ForeignKey('Sensor')
    floor = sqlobject.ForeignKey('Floor')

class Sensor(sqlobject.SQLObject):
    sensorId = sqlobject.StringCol()
    apiKey = sqlobject.StringCol()
    virtual = sqlobject.BoolCol()

#Function for setting a connection
def InitConnection():           
    db_filename = os.path.abspath('data.db')
    connection_string = 'sqlite:' + db_filename
    connection = sqlobject.connectionForURI(connection_string)
    sqlobject.sqlhub.processConnection = connection

#create tables ParkingLot, Floor, Spot and sensor if not already present
def InitDB():       
    ParkingLot.createTable(ifNotExists = True)
    Floor.createTable(ifNotExists = True)
    Spot.createTable(ifNotExists = True)
    Sensor.createTable(ifNotExists = True)

#Insert data for every spot on every floor in a parking lot.
def CreateLot(address, floors, spots, apiKey):      
    lot = ParkingLot(address = address)
    for fid in range(floors):
        floor = Floor(fid = fid, parkingLot = lot, freeSpaces = 0)
        for sid in range(spots):
            sensor = Sensor(sensorId = "", apiKey = apiKey, virtual = True)
            Spot(sid = sid, empty = False, sensor = sensor, floor = floor)

    return lot

#Function for setting a sensor.
def SetSensor(lot, floor, spot, sensorId): 
    floor = Floor.select(sqlobject.AND(Floor.q.parkingLotID == lot.id, Floor.q.fid == floor))[0]
    spot = Spot.select(sqlobject.AND(Spot.q.floorID == floor.id, Spot.q.sid == spot))[0]
    spot.sensor.sensorId = sensorId
    #After initialising the sensor, value of virtual is changed from true to false
    spot.sensor.virtual = False
