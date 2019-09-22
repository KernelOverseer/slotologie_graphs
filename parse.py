import re
import numpy as np
import requests
import pandas as pd
import matplotlib.pyplot as plt
import pickle

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

global  cookie

cookie = {"_intra_42_session_production" : "<your cookie>"}

def load_corrections(username, pagenum=1):
    global  cookie
    regex2 = re.compile(r'<span class=\'reason\'>\nDefense plannification\n<\/span>\n.*\n.*<a data-tooltip-login="(.*?)".*<\/a>')
    regex = re.compile(r'<span class=\'reason\'>\nEarning after defense\n<\/span>\n.*\n.*\n.*\n<a data-tooltip-login="(.*?)".*<\/a>')
    content = requests.get("https://profile.intra.42.fr/users/" + username + "/correction_point_historics?page=" + str(pagenum), cookies=cookie).text
    results = regex.findall(content)
    i = 0;
    last = len(results)
    if results:
        results += load_corrections(username, pagenum + 1)
    return results

def process_occurences(logins):
    occurences = {}
    for i in logins:
        if i in occurences.keys():
            occurences[i] += 1
        else:
            occurences[i] = 1
    return occurences

def import_logins(filename):
    with open(filename) as login_file:
        names = login_file.read()
        login_list = names.split('\n')
        login_list.pop(len(login_list) - 1)
        return login_list

global login_all

login_all = []

def add_relation(login_list, login_table, login1, login2):
    global login_all
    login1_index = 0
    login2_index = 0
#    if login2 not in login_list and login2 not in login_all and login2[:3] != '3b3':
#        login_all.append(login2)
#        print ("============================1= ADDED ", login2, "=========================")
#    if login1 not in login_list and login1 not in login_all and login1[:3] != '3b3':
#        login_all.append(login1)
#        print ("============================2= ADDED ", login1, "=========================")
    for i in range(len(login_list)):
        if login_list[i] == login1:
            login1_index = i + 1
        if login_list[i] == login2:
            login2_index = i + 1
    if not login1_index or not login2_index:
        return 0
    login_table[login1_index][login2_index] += 1
    login_table[login2_index][login1_index] += 1
    return 1

def match_lovers(login_list, login_table, login):
    relations = load_corrections(login, 1)
    for i in relations:
        add_relation(login_list, login_table, login, i)

import sys

#final = load_corrections(sys.argv[1])
#occurences = process_occurences(final)
login_list = import_logins('logins')
login_table = [ [] + login_list ]
for i in login_list:
    login_table.append([i] + [0] * len(login_list))

#for i in range(len(login_list)):
size = len(login_list)
i = 0
while i < size:
    size = len(login_list)
    print ('matching relations for ', login_list[i])
    match_lovers(login_list, login_table, login_list[i])
    i += 1

#data = pd.DataFrame({'corrections' : occurences}).sort_values(by=['corrections'])
#data.plot(kind="bar", title=sys.argv[1] + " correction love rates")
#plt.show()
data = pd.DataFrame({'logins' : login_list})
for i in range(len(login_list)):
    data[login_list[i]] = np.array(login_table[i+1][1::])
data.to_excel('result2.xlsx')
pd.DataFrame({'login' : login_all}).to_csv('new_logins.csv')
#output_file = open('outfile', 'w')
#output_file.write(login_table)
#output_file.close()
