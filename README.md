# websecurity
HW about password analysis and crack

## 英文单词统计

[如何分割单词](https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words)

## PCFG
```html
1.结构分析
my_StructureAnalysis输入为：
口令集：yahoo-words.txt与csdn-words.txt
输出为:
分析结果:
1）structure.txt：对口令集的LDS字段分析结果
2）letter.txt：对口令集的字母数字分析结果
3）StringFile.txt 对口令集的字符串分析结果

2.PCFG
pcfg_generate输入为：
1）structure.csv口令集的LDS字段分析结果
2）StringFile.csv口令集的字符串分析结果
输出为:
分析结果:
1）pcfgresult_csdn：对CSDN口令集的PCFG字典
2）pcfgresult_yahoo：对yahoo口令集的PCFG字典
```
