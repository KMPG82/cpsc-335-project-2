from datetime import datetime

def findFreeTimes(schedule, dailyAct): #function that finds intervals of free times in a schedule
    free_time=[] #initilizae free time list

    clock_in = datetime.strptime(dailyAct[0], '%H:%M') #convert to datetime object
    clock_in_total_minutes = clock_in.hour * 60 + clock_in.minute #calculate the total minutes corresponding to given time

    clock_out = datetime.strptime(dailyAct[1], '%H:%M') #convert to datetime object
    clock_out_total_minutes = clock_out.hour * 60 + clock_out.minute #calculate the total minutes corresponding to given time

    if not schedule: #checks for an empty schedule
        return [[clock_in_total_minutes,clock_out_total_minutes]]

    for i in range(len(schedule)-1): #loop through the person's schedule list
        start_time = datetime.strptime(schedule[i][1], '%H:%M') #get the end time of a meeting, which would be the start of a free time interval
        start_total_minutes = start_time.hour * 60 + start_time.minute #convert to minutes

        end_time = datetime.strptime(schedule[i+1][0], '%H:%M') #get start time of the next meeting, which would be the end of a free time interval
        end_total_minutes = end_time.hour * 60 + end_time.minute #convert to minutes

        start_clock_in_difference = start_total_minutes-clock_in_total_minutes #calculate the difference between the start of their free time and their clock in time
        end_clock_out_difference = end_total_minutes-clock_out_total_minutes

        if start_clock_in_difference >= 0: #if difference is more than or equal to 0, it is within their clock in and clock out time
            free_time.append([start_total_minutes, end_total_minutes]) #add to free time list
        else:
            free_time.append([clock_in_total_minutes, end_total_minutes]) #if not, free time interval will start when they clock in and will last until time of next meeting

        if i+1==len(schedule)-1: #when we are at the last meeting in their schedule
            end_of_last_meeting = datetime.strptime(schedule[i+1][1], '%H:%M') #get the ending time of the last meeting
            end_of_last_total_minutes = end_of_last_meeting.hour * 60 + end_of_last_meeting.minute #convert to minutes

            end_of_last_clock_out_differnece = end_of_last_total_minutes-clock_out_total_minutes #calculate the difference

            if end_of_last_clock_out_differnece <= 0: #if the difference is less than or equal to 0 
                free_time.append([end_of_last_total_minutes, clock_out_total_minutes]) #add to free time list

    #print('schedule:', free_time) #for testing
    return free_time #return list of time intervals when the person is free

def findValidTimes(person1, person2, duration): #find overlaps in both person's free times
    valid_times=[] #initilize valid times list

    #for every free time interval for person 1, compare to each free time interval in person 2's list
    for i in range(len(person1)): #iterate through every free time interval in person 1's list
        for j in range(len(person2)): #iterate through every free time interval in person 2's list
            latest_start = max(person1[i][0], person2[j][0]) #find the last start time
            earliest_end = min(person1[i][1], person2[j][1]) #find the earliest end time

            if earliest_end-latest_start>=duration: #if the difference is more than or equal to the duration of the meeting
                valid_start='{:02d}:{:02d}'.format(*divmod(latest_start, 60)) #convert to HH:MM format
                valid_end='{:02d}:{:02d}'.format(*divmod(earliest_end, 60)) #convert to HH:MM format
                valid_times.append([valid_start, valid_end]) #add time interval to valid times list
                
    return valid_times #return list of valid time intervals


# Sample Input
person1_Schedule = [['7:00', '8:30'], ['12:00', '13:00'], ['16:00', '18:00']]
person1_DailyAct = ['9:00', '19:00']

person2_Schedule = [['9:00', '10:30'], ['12:20', '13:30'], ['14:00', '15:00'], ['16:00', '17:00']]
person2_DailyAct = ['9:00', '18:30']

duration_of_meeting = 30
# Sample output
# [[’10:30’, ’12:00’], [’15:00’, ’16:00’], [’18:00’, ’18:30’]]

person1_Gaps=findFreeTimes(person1_Schedule, person1_DailyAct)
person2_Gaps=findFreeTimes(person2_Schedule, person2_DailyAct)

print('valid intervals: ', findValidTimes(person1_Gaps, person2_Gaps, duration_of_meeting))