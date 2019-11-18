import random
import string
import re
random.seed(2)
allchars = ''
for i in range(94):
    allchars = allchars + string.printable[i]

allchars ="0123456789..."


def random_IP():
    num1 = str(random.randint(0, 255))
    num2 = str(random.randint(0, 255))
    num3 = str(random.randint(0, 255))
    num4 = str(random.randint(0, 255))
    IP = num1 + '.' + num2 + '.' + num3 + '.' + num4
    return IP


def random_boolean(probability_of_true):
    if random.random() <= probability_of_true:
        return True
    else:
        return False


def random_char():
    return random.choice(allchars)


probability_of_IP = 0.2


def random_file_withIP(filepath, numlines, charsperline):
    file = open(filepath, 'w')
    IP_entries = []
    for i in range(numlines):
        line = ''
        IP_in_line = random_boolean(probability_of_IP)
        if IP_in_line:
            IP = random_IP()
            IPlen = len(IP)
            if charsperline-IPlen >= 0:
                IPloc_in_line = random.randint(0, charsperline-IPlen)
                entry = {}
                entry["IP"] = IP
                entry["linenum"] = i+1
                entry["charnum"] = IPloc_in_line
                #print(entry)
                IP_entries.append(entry)
                for j in range(0, IPloc_in_line):
                    line = line + random_char()
                line = line + IP
                for j in range(IPloc_in_line+IPlen, charsperline):
                    line = line + random_char()
            else:
                for j in range(charsperline):
                    line = line + random_char()
        else:
            for j in range(charsperline):
                line = line + random_char()
        line = line + "\n"
        file.write(line)
    return IP_entries


def index_without_error(string, to_find):
    try:
        index = string.index(to_find)
    except ValueError:
        index = -2
    return index


def change_to_int(string):
    try:
        result = {"doable": True, "value": int(string)}
    except ValueError:
        result = {"doable": False, "value": -999}
    return result


def dot_list(string):
    list = []
    helpstring = string
    add = index_without_error(helpstring, ".") + 1
    newitem = 0
    while add > 0:
        newitem = newitem + add
        list.append(newitem-1)
        helpstring = helpstring.split(".", 1)[-1]
        add = index_without_error(helpstring, ".") + 1
    #print(list)
    return list


def IP_triplet(triplet):
    clause1 = (triplet[2]-triplet[1]) <= 4 and (triplet[2]-triplet[1]) >= 2
    clause2 = (triplet[1]-triplet[0]) <= 4 and (triplet[1]-triplet[0]) >= 2
    return clause1 and clause2


def rdigitize(rchar):
    rdigitized = []
    for char in rchar:
        if char.isdigit():
            rdigitized.append(char)
        else:
            break
    numbers = []
    last_index = len(rdigitized) - 1
    number = ''
    for i in range(0, last_index + 1):
        for j in range(0, i+1):
            number = number + rdigitized[j]
        numbers.append(int(number))
        number = ''
    for num in numbers:
        if num > 255:
            numbers.remove(num)
    return numberofdigits(numbers[-1])


def ldigitize(lchar):
    ldigitized = []
    for char in reversed(lchar):
        if char.isdigit():
            ldigitized.append(char)
        else:
            break
    ldigitized.reverse()
    numbers = []
    last_index = len(ldigitized) - 1
    number = ''
    for i in range(0, last_index + 1):
        for j in range(i, last_index + 1):
            number = number + ldigitized[j]
        numbers.append(int(number))
        number = ''
    numbers.reverse()
    for num in numbers:
        if num > 255:
            numbers.remove(num)
    return numberofdigits(numbers[-1])

def numberofdigits(num:int):
    s = str(num)
    return len(s)

def check_edges_triplet(triplet, string):
    left = triplet[0]
    right = triplet[2]
    last_index = len(string) - 1
    lchar = []
    rchar = []
    if left == 0:
        return {"edgebool": False, "left": -1, "right": -1}
    elif left >= 3:
        lchar.append(string[left - 3])
        lchar.append(string[left - 2])
        lchar.append(string[left - 1])
    elif left == 2:
        lchar.append(string[left - 2])
        lchar.append(string[left - 1])
    elif left == 1:
        lchar.append(string[left - 1])
    if right >= last_index:
        return {"edgebool": False, "left": -1, "right": -1}
    elif right <= last_index - 3:
        rchar.append(string[right + 1])
        rchar.append(string[right + 2])
        rchar.append(string[right + 3])
    elif right == last_index - 2:
        rchar.append(string[right + 1])
        rchar.append(string[right + 2])
    elif right == last_index - 1:
        rchar.append(string[right + 1])
    if lchar[-1].isdigit():
        if rchar[0].isdigit():
            leftadd = ldigitize(lchar)
            rightadd = rdigitize(rchar)
            return {"edgebool": True, "left": left - leftadd, "right": right + rightadd}
        else:
            return {"edgebool": False, "left": -1, "right": -1}
    else:
        return {"edgebool": False, "left": -1, "right": -1}


def check_between_two(left, right, string):
    between = string[left+1: right]
    change_between = change_to_int(between)
    if change_between["doable"]:
        if 0 <= change_between["value"] <= 255:
            return True
        else:
            return False
    else:
        return False


def check_inside_triplet(triplet, string):
    left = triplet[0]
    middle = triplet[1]
    right = triplet[2]
    value = check_between_two(left, middle, string) and check_between_two(middle, right, string)
    return value


def find_IP_string(string):
    index_list = dot_list(string)
    result_list = []
    length_index_list = len(index_list)
    for i in range(length_index_list-2):
        triplet = (index_list[i], index_list[i+1], index_list[i+2])
        if IP_triplet(triplet):
            if check_inside_triplet(triplet, string):
                edges = check_edges_triplet(triplet, string)
                if edges["edgebool"]:
                    edges["triplet"] = triplet
                    result_list.append(edges)
    list_of_entries = []
    for result in result_list:
        entry = {}
        entry["IP"] = string[result["left"]:result["right"]+1]
        entry["charnum"] = result["left"]
        list_of_entries.append(entry)
    return list_of_entries

def find_IP_lines(lines):
    numlines = len(lines)
    IPs_in_lines = []
    for i in range(0, numlines):
        line_entries = find_IP_string(lines[i])
        for j in line_entries:
            j["linenum"] = i+1
        IPs_in_lines.extend(line_entries)
    return IPs_in_lines


def find_IP_file(filepath):
    file = open(filepath, 'r')
    lines = file.read().splitlines()
    IPs = find_IP_lines(lines)
    return IPs


def print_IP_entry(entry):
    print("linenum : " + str(entry["linenum"]) + " IP : " + str(entry['IP']) + " charnum : " + str(entry["charnum"]))


def IP_check(IPs_inserted, IPs_found):
    for entry in IPs_inserted:
        check = True
        entries_not_found = []
        if entry in IPs_found:
            pass
        else:
            check = False
            entries_not_found.append(entry)
    if check:
        print("all IPs inserted into the file were found")
    else:
        print("The following entries were not found")
        for entry in entries_not_found:
            print(entry)

filepath = '/home/misanek/PycharmProjects/IPtest/myfile.txt'

IPs_inserted = random_file_withIP(filepath, 100, 100)

IPs_found = find_IP_file(filepath)

IP_check(IPs_inserted, IPs_found)

#for entry in IPs_in_file:
#    print_IP_entry(entry)

#for entry in IPs:
#   print_IP_entry(entry)





