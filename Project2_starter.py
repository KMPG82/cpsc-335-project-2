from datetime import datetime

def convertToMinutes(schedule, dailyAct):
    minute_intervals=[] #initialize intervals in minutes list

    clock_in = datetime.strptime(dailyAct[0], '%H:%M') #convert to datetime object
    clock_in_total_minutes = clock_in.hour * 60 + clock_in.minute #calculate the total minutes corresponding to given time
   
    if dailyAct[1] == '00:00': # handles midnight edge case
        clock_out_total_minutes = 24 * 60
    else:
        clock_out = datetime.strptime(dailyAct[1], '%H:%M') #convert to datetime object
        clock_out_total_minutes = clock_out.hour * 60 + clock_out.minute #calculate the total minutes corresponding to given time
    
    daily_act_minutes=[clock_in_total_minutes, clock_out_total_minutes] #add clock in and out converted to minutes to a list
    
    for i in range(len(schedule)):
        start_time = datetime.strptime(schedule[i][0], '%H:%M') #convert to datetime object 
        start_total_minutes = start_time.hour * 60 + start_time.minute #calculate the total minutes corresponding to given time

        end_time = datetime.strptime(schedule[i][1], '%H:%M') #convert to datetime object
        end_total_minutes = end_time.hour * 60 + end_time.minute #calculate the total minutes corresponding to given time

        minute_intervals.append([start_total_minutes, end_total_minutes]) #add to intervals in minutes list

    return minute_intervals, daily_act_minutes #return both lists containing intervals converted to minutes

def convertTo24Format(schedule):
    converted_schedule=[] #initialize the converted to 24 hour format list

    for i in range(len(schedule)): #iterate through the schedule
        start='{:02d}:{:02d}'.format(*divmod(schedule[i][0], 60)) #convert to HH:MM format
        end='{:02d}:{:02d}'.format(*divmod(schedule[i][1], 60)) #convert to HH:MM format
        converted_schedule.append([start, end]) #add converted interval to the converted schedule list

    return converted_schedule #return the list containing time intervals in 24 hour format

def findFreeTimes(schedule, dailyAct): #function that finds intervals of free times in a schedule
    free_time=[] #initialize free time list

    clock_in = dailyAct[0] #initialize clock in time
    clock_out = dailyAct[1] #initialize clock out time

    if not schedule: # handles empty schedule edge case
        return [[clock_in, clock_out]]

    for i in range(len(schedule)-1): #loop through the schedule
        start_time = schedule[i][1] #get the end time of a meeting, which would be the start of a free time interval

        end_time = schedule[i+1][0] #get start time of the next meeting, which would be the end of a free time interval
        
        start_clock_in_difference = start_time-clock_in #calculate the difference between the start of their free time and their clock in time

        if start_clock_in_difference >= 0: #if difference is more than or equal to 0, it is within their clock in and clock out time
            free_time.append([start_time, end_time]) #add to free time list
        else:
            free_time.append([clock_in, end_time]) #if not, free time interval will start when they clock in and will last until time of next meeting

        if i+1==len(schedule)-1: #when we are at the last meeting in their schedule
            end_of_last_meeting = schedule[i+1][1]#get the ending time of the last meeting

            end_of_last_clock_out_difference = end_of_last_meeting-clock_out #calculate the difference

            if end_of_last_clock_out_difference <= 0: #if the difference is less than or equal to 0 
                free_time.append([end_of_last_meeting, clock_out]) #add to free time list

    return free_time #return list of time intervals when the person is free

def findValidTimes(schedule1, schedule2, duration): #find overlaps in both person's free times
    valid_times=[] #initialize valid times list

    #initialize i and j for while loop
    i=0 #will iterate through first schedule
    j=0 #will iterate through second schedule

    while i<len(schedule1) and j<len(schedule2): #iterate through both person's schedules
        latest_start = max(schedule1[i][0], schedule2[j][0]) #find the latest start time
        earliest_end = min(schedule1[i][1], schedule2[j][1]) #find the earliest end time

        if earliest_end-latest_start>=duration: #if the difference is more than or equal to the duration of the meeting
            valid_times.append([latest_start, earliest_end]) #add time interval to valid times list

        if schedule1[i][1]<schedule2[j][1]: #if person1's end time is earlier than person2's end time
            i+=1 #iterate to next free time interval for person1
        else:
            j+=1 #iterate to next free time interval for person2

    return valid_times #return list of valid time intervals

#sample input #1
person1_Schedule = [['7:00', '8:30'], ['12:00', '13:00'], ['16:00', '18:00']]
person1_DailyAct = ['9:00', '19:00']

person2_Schedule = [['9:00', '10:30'], ['12:20', '13:30'], ['14:00', '15:00'], ['16:00', '17:00']]
person2_DailyAct = ['9:00', '18:30']

duration_of_meeting = 30

person1_Schedule_Minutes, person1_DailyAct_Minutes=convertToMinutes(person1_Schedule, person1_DailyAct)
person2_Schedule_Minutes, person2_DailyAct_Minutes=convertToMinutes(person2_Schedule, person2_DailyAct)

person1_Gaps=findFreeTimes(person1_Schedule_Minutes, person1_DailyAct_Minutes)
person2_Gaps=findFreeTimes(person2_Schedule_Minutes, person2_DailyAct_Minutes)

valid_times=findValidTimes(person1_Gaps, person2_Gaps, duration_of_meeting)
converted_back=convertTo24Format(valid_times)
print('valid intervals in 24 format: ', converted_back)
#sample #1 output
#[[’10:30’, ’12:00’], [’15:00’, ’16:00’], [’18:00’, ’18:30’]]

#sample input #2
person1_Schedule = [['8:00', '9:30'], ['12:00', '13:30'], ['16:00', '17:30']]
person1_DailyAct = ['9:00', '18:00']

person2_Schedule = [['9:00', '10:00'], ['11:30', '13:00'], ['15:00', '16:30']]
person2_DailyAct = ['9:00', '18:00']

person3_Schedule = [['9:30', '10:30'], ['12:30', '14:00'], ['16:00', '17:00']]
person3_DailyAct = ['9:00', '18:00']

duration_of_meeting = 30

person1_Schedule_Minutes, person1_DailyAct_Minutes=convertToMinutes(person1_Schedule, person1_DailyAct)
person2_Schedule_Minutes, person2_DailyAct_Minutes=convertToMinutes(person2_Schedule, person2_DailyAct)
person3_Schedule_Minutes, person3_DailyAct_Minutes=convertToMinutes(person3_Schedule, person3_DailyAct)

person1_Gaps=findFreeTimes(person1_Schedule_Minutes, person1_DailyAct_Minutes)
person2_Gaps=findFreeTimes(person2_Schedule_Minutes, person2_DailyAct_Minutes)
person3_Gaps=findFreeTimes(person3_Schedule_Minutes, person3_DailyAct_Minutes)

valid_times1=findValidTimes(person1_Gaps, person2_Gaps, duration_of_meeting)
valid_times2=findValidTimes(valid_times1, person3_Gaps, duration_of_meeting)

converted_back=convertTo24Format(valid_times2)
print('valid intervals in 24 format: ', converted_back)
#sample #2 output
#[['10:30', '11:30'], ['14:00', '15:00'], ['17:30', '18:00']]