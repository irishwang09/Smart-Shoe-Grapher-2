import serial
import time

buffer = ''
total_buffer = []
#configure serial connection
ser = serial.Serial()
ser.baudrate = 921600
ser.port = 'COM5'
ser.open()
TOTAL_RUN_TIME = 200
current_run_time = 1
all_buffer = []
transition_num = []
error_rate = 0

while current_run_time < TOTAL_RUN_TIME:
    time.sleep(0.1)
    ser.flush()
    buffer = ser.read(ser.inWaiting()).decode() #read all char in buffer
    while '\r\n' in buffer: #split data line by line and store it in var
        buffer = buffer.split('\r\n')
    # print("buffer is ", buffer)
    all_buffer.append(buffer)
    current_run_time += 1
    buffer = ' '
ser.close()

for b in all_buffer:
#     print("length of buffer is ", len(b))
#     if b[-1:] == '':
#         b = b[:-2]
    # print("b[-1] is ", b[-1])
#     print("length of b[-1] is ", len(b[-1]))
#     if len(b[0]) < 92:
#         d = int(b[1][:4])
#     else:
#         d = int(b[0][:4])
#     print("buffer currently is ", b)
#
#     # if total_buffer[-1:] == '':
#     #     total_buffer = total_buffer[:-2]
#
    if len(total_buffer) > 0:
        # print("total_buffer[-1:][0] is ", total_buffer[-1:][0])
        # print("b[0] is ", b[0])
        if len(total_buffer[-1:][0]) < 92:
            new_line = total_buffer[-1:][0] + b[0]
            # print ("new_line is ", new_line)
            # print("length of combined line is ", len(new_line))
            total_buffer = total_buffer[:-1]
            total_buffer.append(new_line)
            # total_buffer[-1:][0] = new_line
            b = b[1:]
        # print ("total buffer changed to", total_buffer[-1:][0])
        # print("new beginning of buffer is ", b[0])
        # print("number of total_buffer is ", total_buffer[-1:][0][:4])
        # print("number of buffer is ", b[0][:4])
        transition_num.append([total_buffer[-1:][0][:4], b[0][:4]])

    total_buffer += b

previous_number = 0
difference = []
all_num = []
for i in total_buffer:
    # print("i is ", i)
    if len(i) != 92:
        error_rate += 1

#     print("number is ", i[:4])
    number = i[:4]
    # print("number is ", number)
    if number.count(',')==0 and number !='':
        n = int(number)
        all_num.append(n)
        if previous_number > 0:
            difference.append(n - previous_number)
        previous_number = n
print(difference)
print (len(difference))
# print (transition_num)
a = sum(1 for i in difference if (i > 2) or (i<0 and i > -254))
print (a)
print("number of errors is ", error_rate)
print("percent skipping is ", a/len(difference))
print("percent error is ", error_rate/len(total_buffer))
