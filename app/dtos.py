class OUTPUT_DATA_DTO:
    def __init__(self,title: str, lat:str, lon:str, depth:float, altitude:float, datetime: str, time_diff: float):
        self.title = title
        self.lat = lat
        self.lon = lon
        self.depth = depth
        self.altitude = altitude
        self.datetime = datetime
        self.time_diff = time_diff
    
    def serialize(self):
        return{
            "title": self.title,
            "lat": self.lat,
            "lon": self.lon,
            "depth": self.depth,
            "altitude": self.altitude,
            "datetime": self.datetime,
            "time_diff": self.time_diff 
        }

class GPS_DTO:
    def __init__(self, title:str, lat: str, lon: str, timestamp: float, datetime: str):
        self.title = title
        self.lat = lat
        self.lon = lon
        self.timestamp = timestamp
        self.date = datetime

    def serialize(self):
        return{
            "title": self.title,
            "lat": self.lat,
            "lon": self.lon,
            "timestamp": self.timestamp ,
            "datetime": self.date,
        } 

class SONAR_DTO:
    def __init__(self, depth:float, altitude:float, timestamp: float):
        self.depth = depth
        self.altitude = altitude
        self.timestamp = timestamp

    def serialize(self):
        return{
            "depth": self.depth,
            "altitude": self.altitude,
            "timestamp": self.timestamp
        } 