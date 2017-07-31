path = 'C:/Users/Lauren/smartshoe/temp.txt'
realterm_file = open(path,'r')
array_of_lines = realterm_file.readlines()
num = []
difference = []
for i in array_of_lines:
    if len(i) >= 92:
        print("i is ", i)
        number = int(i[:4])
        if i != array_of_lines[1]:
            previous_number = num[-1:][0]
            difference.append(number - previous_number)
        num.append(number)
print ("the differences are ", difference)
# print("then numbers are ", num)
print (len(difference))
a = sum(1 for i in difference if (i > 2) or (i<0 and i > -254))
print (a)
print("percent skipping is ", a/len(difference))
