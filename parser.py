# -*- coding: utf-8 -*-

ter_set = set()
non_ter_set = set()
pro_set = []
first_set = {}
follow_set={}
fir_num = {}
fol_num={}


non_ter_set = {'E', 'E\'', 'T', 'T\'', 'F'}
ter_set = {'id', '+', '*', '(', ')'}
pro_set.append(['E', '->', 'T', 'E\''])
pro_set.append(['E\'', '->', '+', 'T', 'E\''])
pro_set.append(['E\'', '->', 'empty'])
pro_set.append(['T', '->', 'F', 'T\''])
pro_set.append(['T\'', '->', '*', 'F', 'T\''])
pro_set.append(['T\'', '->', 'empty'])
pro_set.append(['F', '->', '(', 'E', ')'])
pro_set.append(['F', '->', 'id'])
S = 'E'
for f in non_ter_set:
    first_set[f] = set()
    follow_set[f]=set()


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
        print(first_set)
        return

def loop_fo():
    for x in non_ter_set:
        if x ==S:
            follow_set[x].add('$')
        print(follow_set)
        for p in pro_set:
            left=p[0]
            right=p[2:]
            print(p)
            print(right)
            print(x)
            a=input()
            if x in right:
                i=right.index(x)
                if x ==right[-1]:
                    follow_set[x]=follow_set[x]|(follow_set[left]-{'empty'})
                else:
                    for n in right[i+1:]:
                        if n in ter_set:
                            follow_set[x].add(n)
                            break
                        elif n in non_ter_set:
                            follow_set[x]=follow_set[x]|(follow_set[n]-{'empty'})
                            if has_empty(n):
                                if n==right[-1]:
                                    follow_set[x]=follow_set[x]|(follow_set[left]-{'empty'})
                                else:continue
                            else:break
def fol_change():
    for f in follow_set:
        if fol_num[f]!=len(follow_set[f]):
            return True
    return False
def get_follow():
    while True:
        for f in follow_set:
            fol_num[f]=len(follow_set[f])
        loop_fo()
        if fol_change:
            continue
        print(follow_set)
        return


if __name__ == "__main__":
    # get_first()
    get_follow()
