# coding=UTF-8

'''
Created on 2016年8月20日

@author: Administrator
'''

# import python standard package
import math
import datetime

# import thread package

# import my project package

def add_month( cur_time, number):
    size = int(math.fabs(number))
    remainder = size % 12
    cycle = int(size / 12)
    if number >= 0 :
        year, month = cur_time.year + cycle , cur_time.month + remainder
        if month > 12:
            year += 1 
            month -= 12
    else:
        year, month = cur_time.year - cycle, cur_time.month - remainder
        if month <= 0:
            year -= 1
            month = 12 + month 
    return datetime.datetime(year, month, 1)
    
def get_sequence_month(start_time, end_time):
    time_sequence = []
    
    year, month = start_time.year, start_time.month - 1
    while True:
        month += 1
        if month > 12:
            year += 1
            month -= 12
        
        cur_time = datetime.datetime(year, month, 1)
        if cur_time <= end_time :
            time_sequence.append(cur_time)
        else:
            break
        
    return time_sequence

def get_sequence_month_bystarttime(start_time, size):
    end_time = add_month(start_time, size)
    return get_sequence_month(start_time, end_time)

def get_sequence_month_byendtime(end_time, size):
    start_time = add_month(end_time, -size)
    return get_sequence_month(start_time, end_time)

def get_sequence_date(start_time, end_time):
    start_time = start_time.replace(hour = 0 , minute = 0 , second = 0 , microsecond = 0)
    size = (end_time - start_time).days 
    for index in range(size + 1):
        yield start_time + datetime.timedelta(days = index)

if __name__ == "__main__":
    start_time = datetime.datetime(2016, 7, 1, 1, 23)
    end_time = datetime.datetime.today()
    size = 10
#     for time in get_sequence_month_byendtime(end_time, 13):
#         print(time)
        
    for time in get_sequence_date(start_time, end_time):
        print(time)
    