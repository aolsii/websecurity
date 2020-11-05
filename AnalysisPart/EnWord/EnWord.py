# Output:word frequency length

#把EnFrequency125k.txt转为前25k个转为csv（因为GRE才15k），第二列为频率
#先把每行拿出来预处理把可能的字母换下来，并把数字和符号去掉然后如果大于3就分割，最后统计频率

#!!注意到可能有o替换为e的，比如passwerd

import pandas as pd
import re
from math import log

FileFlag=1# 0是yahoo，1是csdn
RESULTFILE="EnFreqRes_y.csv"
PWDFILE="yahoopw.csv"
PWDFILE_c="csdn.csv"
fre={}

def returnToWord(string):
    # 把字符串中的字符转换成可能的字母
    # 把0还原回o，1还原回l @还原为o 5还原为s
    newstr=""
    newstr = string.replace('0','o')
    newstr = newstr.replace('1','l')
    newstr = newstr.replace('@','a')
    newstr = newstr.replace('5','s')
    newstr = newstr.replace('3','e')
    newstr = newstr.replace('!', 'i')
    #换成小写
    newstr=newstr.lower()
    #只保留小写字母
    newstr = ''.join(re.findall('[a-z]', newstr))
    return newstr

# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
words = open("EnFreq25k.txt").read().split()
wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
maxword = max(len(x) for x in words)

def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    # 这个可以直接计算出二维数组，不需要每次计算
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)# 9e999表示正无穷，等同于inf

    # Build the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]# assert（断言）用于判断一个表达式，在表达式条件为 false 的时候触发异常
        out.append(s[i-k:i])
        i -= k

    return " ".join(reversed(out))


if FileFlag==0:
    df=pd.read_csv(PWDFILE,low_memory=False)
    for pwd in df['passwd']:
        temp=returnToWord(str(pwd))
        temp=infer_spaces(temp)
        temp=temp.split(' ')
        for wd in temp:
            if wd not in fre:
                fre[wd]=1
            else:
                fre[wd]+=1
    pd.DataFrame(list(fre.items())).to_csv('EnFreqRes_y.csv')

else:
    df = pd.read_csv(PWDFILE_c,encoding='gbk',low_memory=False,header=None,names=['username','passwd','mail'])
    for pwd in df['passwd']:
        temp = returnToWord(str(pwd))
        temp = infer_spaces(temp)
        temp = temp.split(' ')
        for wd in temp:
            if wd not in fre:
                fre[wd] = 1
            else:
                fre[wd] += 1
    pd.DataFrame(list(fre.items())).to_csv('EnFreqRes_c.csv')


