import csv
import datetime as dt
import time
from calendar import timegm
from typing import List
from .dtos import OUTPUT_DATA_DTO, GPS_DTO, SONAR_DTO
from .utils import get_gps_timestamp, get_sonar_timestamp

class Worker:

    def __init__(self):
        self.data: List[OUTPUT_DATA_DTO] = []
        self.output_path = './outputs/output.csv'
        self.gps_file = open('./inputs/gps.txt','r')
        self.sonar_file = open('./inputs/sonar.csv','r')
        self.config_file = open('./inputs/config.csv')


    def get_gps_csv_dict(self):
        fieldnames = ['title', 'lat', 'lon', 'height', 'v', 'a', 'b', 'c', 'd', 'x', 'y', 'z', 'date', 'time']
        reader = csv.DictReader(self.gps_file,fieldnames,delimiter='\t')
        data: List[GPS_DTO] = []
        for row in reader:
            item: GPS_DTO = GPS_DTO(row['title'], row['lat'], row['lon'], get_gps_timestamp(row['date'], row['time']), row['date']+' '+row['time'])
            data.append(item.serialize())
        return data


    def get_sonar_csv_dict(self):
        fieldnames = ['lat', 'lon', 'depth', 'e1', 'e2', 'peaksv', 'datetime', 'track_name']
        reader = csv.DictReader(self.sonar_file,fieldnames,delimiter=',')
        data: List[SONAR_DTO] = []
        *delta, altitude = self.get_config_data()
        next(reader) #skip header
        for row in reader:
            item: SONAR_DTO = SONAR_DTO(round(float(row['depth']),2), round(altitude - float(row['depth']),2), get_sonar_timestamp(row['datetime'], delta))
            data.append(item.serialize())
        return data


    def get_config_data(self):
        reader = csv.DictReader(self.config_file, fieldnames=['h','m','s','altitude'], delimiter='\t')
        next(reader) #skip header
        config_data = next(reader)
        return tuple(map(lambda i: float(i), config_data.values()))


    def map_data(self):
        gps_data = self.get_gps_csv_dict()
        sonar_data = self.get_sonar_csv_dict()
        print('Data')
        loops = 0
        s = 0
        for gps_row in gps_data:
            item: OUTPUT_DATA_DTO = OUTPUT_DATA_DTO(gps_row['title'], gps_row['lat'], gps_row['lon'], 0, 0, '', 0)
            loops+=1
            for i in range(s, len(sonar_data)):
                loops+=1
                sonar_timestamp_next = sonar_data[i+1]['timestamp'] if i+1 < len(sonar_data) else sonar_data[i]['timestamp']  

                if abs(gps_row['timestamp'] - sonar_data[i]['timestamp']) < abs(gps_row['timestamp'] - sonar_timestamp_next):
                    item.depth = sonar_data[i]['depth']
                    item.altitude = sonar_data[i]['altitude']
                    item.datetime = gps_row['datetime']
                    item.time_diff = round(gps_row['timestamp'] - sonar_data[i]['timestamp'], 2)
                    s = i
                    self.data.append(item)
                    break
        print(f'Data mapped in {loops} loops')


    def write_output(self):
        file_ = open(self.output_path,'w',newline='')
        writer = csv.DictWriter(file_,['title','lat','lon','altitude','depth','datetime','time_diff'], delimiter='\t')
        for row in self.data:
            writer.writerow(row.serialize())
        file_.close()


    def close_files(self):
        self.config_file.close()
        self.gps_file.close()
        self.sonar_file.close()
        print('Finished, open outputs directory to see the output.')
        input("Press Enter to continue...")