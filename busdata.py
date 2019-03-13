import requests
from datetime import datetime

class BusDatacenter:
	APIprefix = "http://kv78turbo.ovapi.nl" #https://github.com/skywave/KV78Turbo-OVAPI/wiki
	
	def __init__(self):
		print("BusDatacenter launched")

	@classmethod
	def GetBusStopData(cls, busStop):
		APIaddress = cls.APIprefix + "/stopareacode/" + busStop #https://github.com/skywave/KV78Turbo-OVAPI/wiki/StopAreaCode
		req = requests.get(APIaddress)
		return req.json()
		
	@classmethod
	def CheckBusTimeDelay(cls, bus):
		target = datetime.strptime(bus["TargetArrivalTime"], "%Y-%m-%dT%H:%M:%S")
		expected = datetime.strptime(bus["ExpectedArrivalTime"], "%Y-%m-%dT%H:%M:%S")
		return expected - target

def main():
	busStop = "ehvdhk" #hurksestraat
	data = BusDatacenter.GetBusStopData(busStop)
	for lines in data[busStop]:
		for line in data[busStop][lines]["Passes"]:
			print(data[busStop][lines]["Passes"][line]["LinePlanningNumber"][1:5]) #Remove the L
			print(data[busStop][lines]["Passes"][line]["DestinationName50"])
			print(data[busStop][lines]["Passes"][line]["TargetArrivalTime"].split("T")[1]) #Remove the date
			print(BusDatacenter.CheckBusTimeDelay(data[busStop][lines]["Passes"][line]))
			print("  ")

if __name__ == '__main__':
    main()
