import os
import re
from collections import defaultdict
from typing import Counter
import itertools

mypath = f"/Users/aikyab/Documents/CS583HW1"
os.chdir(mypath)

with open('data-1.txt') as f:
    Lines1 = f.readlines()


with open('para-1.txt') as f:
    Lines2 = f.readlines()



T = []
items = []

regex = re.compile('[\d]+')
for line in Lines1:
    list1 = []
    numbers = regex.finditer(line)
    for num in numbers:
        list1.append(int(num.group()))
        if int(num.group()) not in items:
            items.append(int(num.group()))
    T.append(list1)

MIS = {}
data = []

support_count = defaultdict(int)
n = len(T)

for line in Lines2:
    list1 = line.split("=")
    data.append(list1)

for inf in data:
    if inf[0].find("(")>=0:
        val = inf[0][inf[0].index("(")+1:inf[0].index(")")]
        if val=="rest":
            for num in items:
                if num not in MIS:
                    MIS[num]=float(inf[1].strip())
        else:
            MIS[int(val.strip())] = float(inf[1].strip())
    else:
        if inf[0].find("SDC")!=-1:
            sdc = float(inf[1].strip())

def sortfunc(items,ms):
    for i in range(0,len(items)):
        for j in range(0,len(items)-1):
            if ms[items[j]]>ms[items[j+1]]:
                items[j],items[j+1] = items[j+1],items[j]
    return items


def init_pass(items,tran):
    
    for t in tran:
        for i in t:
            support_count[i]+=1
    l = []
    flag = 0
    for item in items:
        if flag == 1:
            if support_count[item]/n >= first_mis:
                l.append(item)
        else:
            if support_count[item]/n >= MIS[item]:
                first_mis = MIS[item]
                flag = 1
                l.append(item)
    return l

def level_two_candidate_gen(l,sdc):
    two_itemsets = []
    for i in range(len(l)-1):
        if support_count[l[i]]/n>=MIS[l[i]]:
            for j in range(i+1,len(l)):
                if support_count[l[j]]/n>=MIS[l[i]] and abs((support_count[l[i]]-support_count[l[j]])/n)<=sdc:
                    two_itemsets.append([l[i],l[j]])
    return two_itemsets

def candidate_gen(fkless1,sdc):
    gen_set = []



    for i in range(len(fkless1)-1):
        for j in range(i+1,len(fkless1)):
            count = 0
            for k in range(len(fkless1[j])):
                if k==len(fkless1[j])-1:
                    if abs((support_count[fkless1[i][k]]-support_count[fkless1[j][k]])/n)<=sdc:
                        list1 = fkless1[j][:k]
                        if MIS[fkless1[i][k]]<MIS[fkless1[j][k]]:
                            list1.append(fkless1[i][k])
                            list1.append(fkless1[j][k])
                        else:
                            list1.append(fkless1[j][k])
                            list1.append(fkless1[i][k])
                        gen_set.append(list1)
                else:
                    if fkless1[i][k]!=fkless1[j][k]:
                        break
    flag = {}
    for i in range(len(gen_set)):
        kless1 = list(itertools.combinations(gen_set[i],len(gen_set[i])-1))
        for elem in kless1:
            check = list(elem)
            if check not in fkless1:
                if check[0]!=gen_set[i][0]:
                    continue
                else:
                    flag[i]=1
    new_list = []
    for i in range(len(gen_set)):
        if i not in flag:
            new_list.append(gen_set[i])
    return new_list






items = sortfunc(items,MIS)
l = init_pass(items,T)
f_one = []
for i in range(len(l)):
    if support_count[l[i]]/n >= MIS[l[i]]:
        f_one.append(l[i])
k = 2
c_sup_count = defaultdict(int)
fkless_1 = 1
frequent_item_sets = {}
frequent_item_sets[1] = f_one

while fkless_1:
    if k==2:
        ck = level_two_candidate_gen(l,sdc)
    else:
        ck = candidate_gen(fkless_1,sdc)
    for cand in ck:
        for tran in T:
            counter = 0
            for i in range(len(cand)):
                if cand[i] in tran:
                    counter+=1
            if counter==len(cand):
                c_sup_count[tuple(cand)]+=1
    fkless_1 = []
    for cand in ck:
        if c_sup_count[tuple(cand)]/n >= MIS[cand[0]]:
            fkless_1.append(cand)
    if fkless_1:
        frequent_item_sets[k] = fkless_1
    k+=1

output_string = ""
f_out = open("result.txt", "w")

output_string+="59\n"

if len(frequent_item_sets) == 0:
	output_string += "No Frequent itemsets were found \n\n"



for key,value in frequent_item_sets.items():
    output_string+= "(Length-"+str(key)+" "+str(len(value))+" \n"
    if key==1:
        for num in value:
            output_string+= "("+str(num)+")\n"
    else:
        for num in value:
            output_string+= "("+" ".join(list(map(str,num)))+")\n"
    output_string+= ")\n"



f_out.write(output_string)
f_out.close()






        

