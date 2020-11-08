import os
import heapq

def frequenceDict(dirpath,gram,frequence_dict):
    begin_symbol = ''
    end_symbol = '$'

    with open(dirpath,'r', encoding='utf-8' ) as file:
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
    with open(fileout,'w',encoding='utf-8' ) as file:
        file.write(str(gen_dict))

def main():
    pathin_yahoo = os.path.join(os.path.dirname(__file__),'yahoo-words.txt')
    pathout_yahoo = os.path.join(os.path.dirname(__file__),'markov_yahoo_result.txt')
    pathin_csdn = os.path.join(os.path.dirname(__file__),'csdn-words.txt')
    pathout_csdn = os.path.join(os.path.dirname(__file__),'markov_csdn_result.txt')
    ## 4阶马尔可夫模型用于yahoo数据集
    yahoo_gram = 4
    ## 6阶马尔可夫模型用于csdn数据集
    csdn_gram = 6
    ##存储频率字典
    yahoo_frequence_dict = dict()
    csdn_frequence_dict = dict()
    ## 生成密码字典大小
    dict_size = 100000
    ## 生成密码最小长度
    length = 4
    frequenceDict(pathin_yahoo,yahoo_gram,yahoo_frequence_dict)
    gen_dict_yahoo = passwordGenete(yahoo_frequence_dict,yahoo_gram,dict_size,length)
    fileOut(pathout_yahoo,gen_dict_yahoo)

    frequenceDict(pathin_csdn,csdn_gram,csdn_frequence_dict)
    gen_dict_csdn = passwordGenete(csdn_frequence_dict,csdn_gram,dict_size,length)
    fileOut(pathout_csdn,gen_dict_csdn)

if __name__=='__main__':
    main()