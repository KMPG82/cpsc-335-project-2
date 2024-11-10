#program by: Kevin Ponting, Alex Labitigan, Kali Ingco, John Paik
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

    if schedule[0][0]-clock_in > 0: #check if there is a free gap between clock in and the start of their first meeting
        free_time.append([clock_in, schedule[0][0]]) #add to free time list
    
    if len(schedule) == 1: # handles one busy time slot
        start_time = schedule[0][1] #get the end time of a meeting, which would be the start of a free time interval

        end_time = clock_out #get start time of the next meeting, which would be the end of a free time interval

        start_clock_in_difference = start_time-clock_in #calculate the difference between the start of their free time and their clock in time

        if start_clock_in_difference >= 0: #if difference is more than or equal to 0, it is within their clock in and clock out time
            free_time.append([start_time, end_time]) #add to free time list
        else:
            free_time.append([clock_in, end_time]) #if not, free time interval will start when they clock in and will last until time of next meeting
    else:
        for i in range(len(schedule)-1): #loop through the schedule
            start_time = schedule[i][1] #get the end time of a meeting, which would be the start of a free time interval

            end_time = schedule[i+1][0] #get start time of the next meeting, which would be the end of a free time interval

            start_clock_in_difference = start_time-clock_in #calculate the difference between the start of their free time and their clock in time

            if start_clock_in_difference >= 0: #if difference is more than or equal to 0, it is within their clock in and clock out time
                free_time.append([start_time, end_time]) #add to free time list
            else:
                if end_time-clock_in > 0: #check if end time is within their clock in/out time
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

#BELOW CODE IS NOT PART OF THE ALGORITHM, ONLY READS INPUT FROM INPUT.TXT FILE AND WRITES TO OUTPUT.TXT FILE
output=None #initialize output
with open('input.txt', 'r') as file, open('output.txt', 'w') as output_file:
    content = file.read().strip().split("\n\n")  #split by double newlines for each test case

    for case in content: #iterate through cases
        lines = case.strip().splitlines()
        schedules = [] #initialize schedules list
        clock_in_out = [] #intitalize clock in/out list
        duration_of_meeting = None #initialize duration of meeting

        for line in lines: #interpret each line
            if line.startswith("duration_of_meeting"): #indicator of meeting duration
                duration_of_meeting = int(line.split('=')[1].strip()) #get meeting duration

            elif line.startswith("person"): #indicator of a individual person
                if "Schedule" in line: #indicator of a schedule
                    schedule_str = line.split("=")[1].strip() #parse
                    schedule = eval(schedule_str) #convert string to list
                    schedules.append(schedule) #add to schedule list
                elif "DailyAct" in line: #indicator of clock in/out time
                    daily_act_str = line.split("=")[1].strip() #parse
                    daily_act = eval(daily_act_str)  #convert string to list
                    clock_in_out.append(daily_act) #add to clock in and out times
            else:
                free_time_intervals=[] #intialize free time intervals list
                for i in range(len(schedules)): #iterate through each schedule
                    schedules[i], clock_in_out[i]=convertToMinutes(schedules[i], clock_in_out[i]) #convert schedule to minutes
                    free_time_intervals.append(findFreeTimes(schedules[i], clock_in_out[i])) #find free times in schedule

                while len(free_time_intervals) > 1: #find valid times by iterating through free time intervals and finding overlaps
                    valid_times=findValidTimes(free_time_intervals[-2], free_time_intervals[-1], duration_of_meeting) #find overlaps
                    #pop the last two free time intervals off the list
                    free_time_intervals.pop() 
                    free_time_intervals.pop()
                    free_time_intervals.append(valid_times) #append the valid times interval to the back of the free times interval list to check for overlap with remaining intervals 

                output=convertTo24Format(free_time_intervals[0]) #list of valid times
                output_file.write(f"{output}\n\n") #write output to output.txt file
                print(output)
                schedules=[] #empty schedules list for next test case
                clock_in_out=[] #empty clock in/out list for next test case

