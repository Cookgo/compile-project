# -*- coding: utf-8 -*-
import fileinput

# 初始化工作
ter_set = set()
non_ter_set = set()
pro_set = []
first_set = {}
follow_set = {}
select_set = {}
fir_num = {}
fol_num = {}
non_rec=set()
flag=False


def init():
    for line in fileinput.input('grammar.txt'):
        a = line.split()
        pro_set.append(a)
    for p in pro_set:
        non_ter_set.add(p[0])
    for p in pro_set:
        for t in p[2:]:
            if t not in non_ter_set:
                ter_set.add(t)
    for f in non_ter_set:
        first_set[f] = set()
        follow_set[f] = set()
    for p in pro_set:
        i = pro_set.index(p)
        select_set[i] = set()


S = '程序'
# non_ter_set = {'E', 'E\'', 'T', 'T\'', 'F'}
# ter_set = {'id', '+', '*', '(', ')'}
# pro_set.append(['E', '->', 'T', 'E\''])
# pro_set.append(['E\'', '->', '+', 'T', 'E\''])
# pro_set.append(['E\'', '->', 'empty'])
# pro_set.append(['T', '->', 'F', 'T\''])
# pro_set.append(['T\'', '->', '*', 'F', 'T\''])
# pro_set.append(['T\'', '->', 'empty'])
# pro_set.append(['F', '->', '(', 'E', ')'])
# pro_set.append(['F', '->', 'id'])


# 实现栈


class Stack(object):
    def __init__(self):
        self.item = []

    def print(self):
        for x in reversed(self.item):
            print(x)

    def top(self):
        return self.item[-1]

    def push(self, x):
        self.item.append(x)

    def pop(self):
        self.item.pop(-1)


# 求first集
def has_empty(t):
    for p in pro_set:
        if p[0] == t and p[2] == 'empty':
            return True
    return False


def only_one(t):
    count = 0
    for p in pro_set:
        if p[0] == t:
            count += 1
    if count > 1:
        return False
    return True


def loop():
    for p in pro_set:
        left = p[0]
        right = p[2:]
        for r in right:
            if r in ter_set:
                first_set[left].add(r)
                break
            elif r in non_ter_set:
                first_set[left] = first_set[left] | first_set[r]
                if has_empty(r):
                    if r == right[-1]:
                        first_set[left].add('empty')
                    else:
                        continue
                else:
                    break
            elif r == 'empty':
                first_set[left].add('empty')

            else:
                print('first_set error')
                break


def fir_change():
    for f in first_set:
        if fir_num[f] != len(first_set[f]):
            return True
    return False


def get_first():
    while True:
        for f in first_set:
            fir_num[f] = len(first_set[f])
        loop()
        if fir_change():
            continue
        # print(first_set)
        return

# 求follow集


def loop_fo():
    for x in non_ter_set:
        if x == S:
            follow_set[x].add('$')
        for p in pro_set:
            left = p[0]
            right = p[2:]
            if x in right:
                i = right.index(x)
                if x == right[-1]:
                    follow_set[x] = follow_set[x] | (
                        follow_set[left]-{'empty'})
                else:
                    for n in right[i+1:]:
                        if n in ter_set:
                            follow_set[x].add(n)
                            break
                        elif n in non_ter_set:
                            follow_set[x] = follow_set[x] | (
                                first_set[n]-{'empty'})
                            if has_empty(n):
                                if n == right[-1]:
                                    follow_set[x] = follow_set[x] | (
                                        follow_set[left]-{'empty'})
                                else:
                                    continue
                            else:
                                break


def fol_change():
    for f in follow_set:
        if fol_num[f] != len(follow_set[f]):
            return True
    return False


def get_follow():
    while True:
        for f in follow_set:
            fol_num[f] = len(follow_set[f])
        loop_fo()
        if fol_change():
            continue
        # print(follow_set)
        return

# 求select集


def get_str_fir(str):
    temp = set()
    for x in str:
        if x in ter_set:
            temp.add(x)
            return temp
        elif x in non_ter_set:
            if 'empty' in first_set[x]:
                temp = temp | (first_set[x]-{'empty'})
                if x == str[-1]:
                    temp.add('empty')
                    return temp
            else:
                temp = temp | first_set[x]
                return temp
        else:
            print('求串first集时错误：既不是终结符也不是非终结符')


def get_select():
    for p in pro_set:
        i = pro_set.index(p)
        left = p[0]
        right = p[2:]
        if right[0] == 'empty':
            select_set[i] = follow_set[left]
        else:
            fir = get_str_fir(right)
            if 'empty' in fir:
                select_set[i] = select_set[i] | fir | follow_set[left] - \
                    {'empty'}
            else:
                select_set[i] = select_set[i] | fir
    # print(select_set)

# 检查回溯与左递归


def down(x,used_l,used_p):
    global non_rec
    global flag
    used_l.add(x)
    for p in pro_set:
        if p[0] == x: 
            if p[2] in ter_set:
                continue
            if p[2] in non_ter_set:
                if p[2] in used_l:
                    used_p.append(p)
                    print(p[2])
                    print(used_l)
                    print(used_p)
                    flag=True
                    return
                else:
                    
                    used_p.append(p)
                    down(p[2],used_l,used_p)
    if flag==False:
        non_rec.add(x)
def is_recursion():
    global flag
    
    used_l=set()
    used_p=[]
    for x in non_ter_set:
        down(x,used_l,used_p)
        # if flag==True:
        #     break
    return flag

# 去除回溯与递归
def re_back():
    


        


def is_ll_1():
    for x in non_ter_set:
        x_pro = []
        for p in pro_set:
            if p[0] == x:
                i = pro_set.index(p)
                x_pro.append(i)
        for i in x_pro:
            for j in x_pro:
                if i != j:
                    res = select_set[i] & select_set[j]
                    if len(res) != 0:
                        return False
    return True

# 预测分析法


def pre_analyze(str):
    if not is_ll_1() or str is None:
        print('预测分析初始化出错')
    stack = Stack()
    stack.push('$')
    stack.push(S)
    top = stack.top()
    s = str[0]
    is_find = False
    used_pro = []
    while(not(top == '$'and s == '$')):
        if top in non_ter_set:
            for p in pro_set:
                if p[0] == top:
                    is_find = True
                    i = pro_set.index(p)
                    if s in select_set[i]:
                        used_pro.append(p)
                        stack.pop()
                        if p[2] == 'empty':
                            top = stack.top()
                            break
                        for x in reversed(p[2:]):
                            stack.push(x)
                        top = stack.top()
                        break
            if is_find == False:
                print('找不到可用的产生式')
                return
            is_find = False
        elif top in ter_set:
            if top == s:
                stack.pop()
                str.pop(0)
                top = stack.top()
                s = str[0]

            else:
                print('终结符不相等')
                return
    for p in used_pro:
        print(p)


if __name__ == "__main__":
    init()
    #  for p in pro_set:
    #      print(p)
    #  print(non_ter_set)
    #  print(ter_set)
    get_first()
    get_follow()
    get_select()

    # res = is_ll_1()
    # print(res)
    res=is_recursion()
    print(res)
    # str=['id','+','id','*','id','$']
    # pre_analyze(str)
     
