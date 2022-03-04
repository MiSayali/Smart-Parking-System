import schema
import state
import time

#create connection
schema.InitConnection()
#create database
schema.InitDB()

#check if the database has a lot by the name "Swargate". Number of rows matching the address is returned.
lots = schema.ParkingLot.selectBy(address = "Swargate")

#if there is no lot by the name "Swargate", create a lot.
if lots.count() == 0:
    lot = schema.CreateLot("Swargate", 3, 50, "31787a56-af8a-4a28-ab51-0cde074cbfd0")
else:
    lot = lots[0]

#set the sensor of a parking lot.
schema.SetSensor(lot, 2, 1, "BOLT8024098")

#loop for checking and displaying number of empty spaces on each floor every 10s.
while True:
    state.CheckAll()
    for floor in lot.floors:
        print("Empty spaces on floor ", floor.fid, ":", floor.freeSpaces)
    time.sleep(10)
t