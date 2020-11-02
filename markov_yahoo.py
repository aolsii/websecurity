import os
import heapq

def frequenceDict(dirpath,gram,frequence_dict):
    begin_symbol = ''
    end_symbol = '$'

    with open(dirpath,'r') as file:
        password_list = file.read().split('\n')
    number = dict()
    for password in password_list:
        password = password.strip()
        password = begin_symbol + password + end_symbol
        prestring = ''
        for char in password:
            prestring = prestring[-gram:]
            if prestring not in frequence_dict:
                frequence_dict[prestring] = dict()
            if char in frequence_dict[prestring]:
                frequence_dict[prestring][char] += 1
            else:
                frequence_dict[prestring][char] = 1
            if prestring in number:
                number[prestring] += 1
            else:
                number[prestring] = 1   
            prestring = prestring + char
    
    for key in frequence_dict:
        for char_key in frequence_dict[key]:
            frequence_dict[key][char_key] = frequence_dict[key][char_key]/number[key]

def passwordGenete(frequence_dict,gram,dict_size,length):
    q = [(-1,'')]
    password_num = 0
    gen_dict = ''
    while len(q) > 0:
        prob,password = heapq.heappop(q)
        if password.endswith('$'):
            if len(password) > length-1:
                gen_dict = gen_dict + password[:-1] + '\n'
                password_num += 1
                if password_num == dict_size:
                    break
        else:
            endstring = password[-gram:]
            if endstring in frequence_dict:
                for char in frequence_dict[endstring]:
                    heapq.heappush(q,(frequence_dict[endstring][char]*prob,password+char))
    return gen_dict

def fileOut(fileout,gen_dict):
    print(gen_dict)
    with open(fileout,'w') as file:
        file.write(str(gen_dict))

def main():
    pathin = os.path.join(os.path.dirname(__file__),'yahoo-words.txt')
    pathout = os.path.join(os.path.dirname(__file__),'yahoo_result.txt')
    ## 4阶马尔可夫模型
    gram = 4
    ##存储频率字典
    frequence_dict = dict()
    ## 生成密码字典大小
    dict_size = 100000
    ## 生成密码最小长度
    length = 4
    frequenceDict(pathin,gram,frequence_dict)
    gen_dict = passwordGenete(frequence_dict,gram,dict_size,length)
    fileOut(pathout,gen_dict)

if __name__=='__main__':
    main()