from datetime import datetime

def findFreeTime(schedule, dailyAct):
    free_time=[]
    for i in range(len(schedule)-1):

        free_time.append([schedule[i][1], schedule[i+1][0]])

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