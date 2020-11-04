import re
import csv

import pandas as pd
from pandas import DataFrame

class Analysis(object):
	def __init__(self,passwordlist):
		self.passwordlist = passwordlist

	# 结构统计
	def Struc(self):
		StruList = []
		for passwd in self.passwordlist:
			struc = ''
			passwd = str(passwd)
			for ch in passwd:
				if ch.isdigit():
					struc += 'D'
				elif ch.isalpha():
					struc += 'L'
				else:
					struc += 'S'
			StruList.append(struc)

		unique_data = pd.unique(StruList)
		freq = []
		for ii in unique_data:
			freq.append('{:.12f}'.format(int(StruList.count(ii)) * 1.0 / len(StruList)))
		dic = {'password': unique_data,
			   'freq': freq}
		dataFrame = DataFrame(dic)
		dataFrame = dataFrame.sort_values(by='freq')
		return dataFrame

	#字母数字统计
	def Letter(self):
		dic={'L1':{},'L2':{},'L3':{},'L4':{},'L5':{},'L6':{},'L7':{},'L8':{},'L9':{},'L10':{},'L11':{},'L12':{},'L13':{},'L14':{},'L15':{},'L16':{},'L17':{},'L18':{},'L19':{},'L20':{},'L21':{},'L22':{},'L23':{},'L24':{},'L25':{},
			'D1':{},'D2':{},'D3':{},'D4':{},'D5':{},'D6':{},'D7':{},'D8':{},'D9':{},'D10':{},'D11':{},'D12':{},'D13':{},'D14':{},'D15':{},'D16':{},'D17':{},'D18':{},'D19':{},'D20':{},'D21':{},'D22':{},'D23':{},'D24':{},'D25':{},
			'S1':{},'S2':{},'S3':{},'S4':{},'S5':{},'S6':{},'S7':{},'S8':{},'S9':{},'S10':{},'S11':{},'S12':{},'S13':{},'S14':{},'S15':{},'S16':{},'S17':{},'S18':{},'S19':{},'S20':{},'S21':{},'S22':{},'S23':{},'S24':{},'S25':{}}

		dataFrame = DataFrame(columns=('structure','nums','1','2','3','4','5','6','7','8','9','10'))
		LetterPattern = re.compile(r'[A-Za-z]+$')
		DigitPattern = re.compile(r'\d+$')
		SigPattern = re.compile(r'\W+$')
		for password in self.passwordlist:
			password = str(password)
			s = ''
			if LetterPattern.match(password):
				s = 'L' + str(len(password))
			elif DigitPattern.match(password):
				s = 'D' + str(len(password))
			elif SigPattern.match(password):
				s = 'S' + str(len(password))
			if s:
				if password in dic[s]:
					dic[s][password] += 1
				else:
					dic[s][password] = 1
		
		for dic_element in dic:
			pwst_element = dic[dic_element]
			sums = sum(pwst_element.get(x) for x in pwst_element)
			rows = [dic_element,sums]
			pwst_element = sorted(pwst_element.items(),key = lambda x:x[1],reverse = True)
			if len(pwst_element) > 10:
				for r in range(10):
					rows.append(str(pwst_element[r]))
			else:
				for r in range(len(pwst_element)):
					rows.append(str(pwst_element[r][0]) + ' : ' + str(pwst_element[r][1]))
				for r in range(10 - len(pwst_element)):
					rows.append(0)
			dataFrame.loc[dic_element] = rows
		dataFrame = dataFrame.sort_values(by = 'nums')
		return dataFrame


	#字符串统计
	def Str(self):
		LetterPattern = re.compile(r'[A-Za-z]+$')
		DigitPattern = re.compile(r'\d+$')
		SigPattern = re.compile(r'\W+$')
		outputDic = {}
		def countStrTool(all_element, LDS):
			for pw_ele in all_element:
				pattern = str(LDS) + str(len(pw_ele))
				if pattern in outputDic:
					if str(pw_ele) in outputDic[pattern]:
						outputDic[pattern][str(pw_ele)] += 1
					else:
						outputDic[pattern][str(pw_ele)] = 1
				else:
					outputDic[pattern] = {str(pw_ele):1}
		str_file = open('StringFile.txt','w')
		csv_write = csv.writer(str_file)
		for password in self.passwordlist:
			all_letter = re.findall(LetterPattern,str(password))
			all_digit = re.findall(DigitPattern,str(password))
			all_sig = re.findall(SigPattern,str(password))
			countStrTool(all_letter, 'L')
			countStrTool(all_digit, 'D')
			countStrTool(all_sig, 'S')
			
		for tmpDic in outputDic.keys():
			tmpList = sorted(outputDic[tmpDic].items(),key=lambda item:item[1],reverse=True)
			write_res = [tmpDic]
			for tu in tmpList:
				s = str(tu[0]) + '-' + str(tu[1])
				write_res.append(s)
			csv_write.writerow(write_res)


def main():
	file='yahoo-words.txt'
	df = pd.read_csv(file,encoding='gbk',sep="\t",names=["password"])
	passwordlist = pd.Series(df['password'].values)
	result = Analysis(passwordlist)

	result.Struc().to_csv('structure.txt',index = False)
	result.Letter().to_csv('letter.txt', index = False)
	result.Str()

if __name__=='__main__':
	main()




