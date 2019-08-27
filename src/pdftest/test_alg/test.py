import os
import sys
import datetime
#
# Complete the timeConversion function below.
#
def timeConversion(s):
    #
    # Write your code here.
    if 'am' in s.lower() and '12' in s.lower():
        return '00' + s[2:-2]

    elif 'pm' in s.lower():
        time = s.split(":")
        time[0] = str(int(time[0]) + 12)
        x = ":".join(time)
        x = x.replace('PM','')
        return x
       
    else:
        s = s.replace('AM','')
        return s
    #

if __name__ == '__main__':
    # f = open(os.environ['OUTPUT_PATH'], 'w')

    # s = input("input")
    s = "12:12:20AM"
    result = timeConversion(s)
    print(result)
    # f.write(result + '\n')

    # f.close()
