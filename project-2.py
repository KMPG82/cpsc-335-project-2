from datetime import datetime

def findFreeTime(schedule, dailyAct):
    free_time=[]
    clock_in = datetime.strptime(dailyAct[0], '%H:%M')
    clock_in_total_minutes = clock_in.hour * 60 + clock_in.minute

    clock_out = datetime.strptime(dailyAct[1], '%H:%M')
    clock_out_total_minutes = clock_out.hour * 60 + clock_out.minute

    print('clock in:', clock_in_total_minutes)
    print('clock out:', clock_out_total_minutes)

    for i in range(len(schedule)-1):
        start_time = datetime.strptime(schedule[i][1], '%H:%M')
        start_total_minutes = start_time.hour * 60 + start_time.minute

        end_time = datetime.strptime(schedule[i+1][0], '%H:%M')
        end_total_minutes = end_time.hour * 60 + end_time.minute

        start_clock_in_difference = start_total_minutes-clock_in_total_minutes
        end_clock_out_difference = end_total_minutes-clock_out_total_minutes

        if start_clock_in_difference >= 0:
            free_time.append([start_total_minutes, end_total_minutes])
        else:
            free_time.append([clock_in_total_minutes, end_total_minutes])

        if i+1==len(schedule)-1:
            end_of_last_meeting = datetime.strptime(schedule[i+1][1], '%H:%M')
            end_of_last_total_minutes = end_of_last_meeting.hour * 60 + end_of_last_meeting.minute

            end_of_last_clock_out_differnece = end_of_last_total_minutes-clock_out_total_minutes
            if end_of_last_clock_out_differnece <= 0:
                free_time.append([end_of_last_total_minutes, clock_out_total_minutes])

    print(free_time)

# Sample Input
person1_Schedule = [['7:00', '8:30'], ['12:00', '13:00'], ['16:00', '18:00']]
person1_DailyAct = ['9:00', '19:00']

person2_Schedule = [['9:00', '10:30'], ['12:20', '13:30'], ['14:00', '15:00'], ['16:00', '17:00']]
person2_DailyAct = ['9:00', '18:30']

duration_of_meeting = 30
# Sample output
# [[’10:30’, ’12:00’], [’15:00’, ’16:00’], [’18:00’, ’18:30’]]

findFreeTime(person1_Schedule, person1_DailyAct)
findFreeTime(person2_Schedule, person2_DailyAct)