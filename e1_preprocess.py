# -*- coding: UTF-8 -*-
__author__ = 'Dexi Liu'

import os
import sys
import codecs
import re
import string
import numpy
from simhash import Simhash,SimhashIndex

def CreatTargetDir(sf,df):
	if not os.path.exists(sf):
		print (sf,"doesn't exist!")
		sys.exit()
	if os.path.isdir(sf):
		if not os.path.exists(df):
			os.system('mkdir '+df)
	
	return

def DeletePatternInFile(line):
	# delete noisy in Weibo
	line = re.sub(u'<[^>]*>|\[\{[^\}\]]*[\}\]]',u'。',line)
	line = re.sub(u'\/\/@[^:：。 ]+[:：。]|回复@[^:：。 ]+[:：。 ]', u'。',line)
	line = re.sub(u'\/\/@[^ ]+$', u'。',line)
	line = re.sub(u'@[^ ，,;；。？?、：:]+[ ，,;；。？?、：:]|@[^ ，,;；。？?、：:]+$',u' ',line)
	line = re.sub(u'http:\/\/[0-9A-Za-z/\.]+',u' ',line)
	line = re.sub(u'[0-9A-Za-z\/\.]+html',u' ',line)
	line = re.sub(u'&quot[;]*|&gt[;]*|&gt[;]*|&amp[;]*|&lt[;]*|&amp;quot|&nbsp[;]*|&#[0-9]*|br\/',u'',line)
	line = re.sub(u'【[^】]+】', u'。', line)
	line = re.sub(u'[ ][ ]+', u' ', line)
	line = re.sub(u';|；|；|…|~|～|…|#|【|】', u'。', line)
	line = re.sub(u'[`][`]+', u'`', line)
	line = re.sub(u'[！!][！!]+', u'！', line)
	line = re.sub(u'[，,][，,]+', u'，', line)
	line = re.sub(u'[\.][\.]+', u'.', line)
	line = re.sub(u'[\-][\-]+', u'——', line)
	line = re.sub(u'[？?][？?]+', u'？', line)
	line = re.sub(u'[=][=]+', u'=', line)
	line = re.sub(u'[、][、]+', u'、', line)
	line = re.sub(u'\[',u'。[',line)
	line = re.sub(u'\]',u']。',line)
	line = re.sub(u'^[。 ]+', u'', line)
	line = re.sub(u'[。][。 ]+', u'。', line)
	sp = re.split(u'。|！|!|？|\?',line)
	line = re.sub(u'[。][。]+', u'。', line)
	if not re.search(u'。$|！$|!$|？$|\?$',line): line += u'。'
	return line

INDEX = SimhashIndex([],f=128,k=10) 
def IsDuplicate(tid,text):
	sh = Simhash(text,f=128)
	dup = INDEX.get_near_dups(sh)
	if len(dup) > 0:
		#print tid,dup[0]
		#hlog.write(tid+' '+' '.join(dup)+'\n')
		print('identify duplicate: ' + tid +' '+' '.join(dup))
		return True
	else:
		INDEX.add(tid,sh)
		return False

def PreProcess(sf,df):
	print("PreProcessing", sf)
	hsf = codecs.open(sf, 'r','utf-8')
	hdf = codecs.open(df, 'w','utf-8')
	pretid,pretext = '',''
	while True:
		line = hsf.readline()
		if len(line)==0:break
		line = line.strip()
		if line == '': continue
		temp = re.findall(u'^[0-9]+:\s*|^DOC[0-9]+:\s*',line)
		if len(temp) ==0:
			pretext += line
			continue 
		if len(temp) > 0:
			pretext = pretext.lower()
			pretext = DeletePatternInFile(pretext)
			#print pretext
			if len(pretext)>=3 and not IsDuplicate(pretid,pretext):
				hdf.write('DOC'+ pretid + ': ' + pretext+ '\n')
			tid = re.sub(u':\s*', u'', temp[0])
			pretid = tid
			pretext= re.sub(u'^[0-9]+:\s*|^DOC[0-9]+:\s*','',line)
	if len(pretext)>=3 and not IsDuplicate(pretid,pretext):
		hdf.write('DOC'+ pretid + ': ' + pretext + '\n')
	hsf.close()
	hdf.close()
	return

def PreProcess_batch(sf,df):
	CreatTargetDir(sf,df)
	if os.path.isdir(sf):
		for subfile in os.listdir(sf): 
			PreProcess(sf+'/'+subfile, df+'/'+subfile)
	else:
		PreProcess(sf,df)

import Nlpir
def Pos(tid,text):
	text = text.encode('utf-8')
	pos_clas, pos_tokenlized,pos_trectext = '','',''
	#print text
	for t in Nlpir.Seg(text):
		#if True:
		try: 
			word = t[0].decode('utf-8')
			word = re.sub(u'[^\u4e00-\u9fffa-zA-Z0-9]',u'',word)
			if word =='': continue
			pos = t[1]
			pos_clas += ' ' + word + '/' + pos
			if not re.search(u'^w|^m',pos): pos_tokenlized += ' '+word

		except:
		#else:
			print('an invalid character in doc',tid)
			continue
			#print''# pos
	if tid != '':
		pos_clas = "DOC" + tid + u": " + pos_clas + '\n'
		pos_trectext = "<DOC>\n<DOCNO>DOC" + tid + "</DOCNO>\n<TEXT>" + pos_tokenlized + '</TEXT>\n</DOC>\n'
		pos_tokenlized = "DOC" + tid + u": " + pos_tokenlized + '\n'
	else:
		print('check the format of this line', pos_tokenlized)
	return pos_clas, pos_tokenlized, pos_trectext


def TokenAndPos(sf,df_clas,df_tokenlized,df_trectext):
	print("tokenlizing and POSing", sf)
	hsf = codecs.open(sf, 'r','utf-8')
	hdf_clas = codecs.open(df_clas, 'w','utf-8')
	hdf_tokenlized = codecs.open(df_tokenlized, 'w','utf-8')
	hdf_trectext = codecs.open(df_trectext, 'w','utf-8')
	while True:
		line = hsf.readline()
		if len(line)==0:break
		line = line.strip()
		if line == '': continue
		temp = re.findall(u'^DOC[0-9]+:\s*',line)
		if len(temp)>0:
			tid = re.sub(u'^DOC|:\s*$', u'', temp[0])
		else:
			tid=''
		text= re.sub(u'^DOC[0-9]+:\s*','',line)
		text_clas,text_tokenlized, text_trectext = Pos(tid,text)
		hdf_clas.write(text_clas)
		hdf_tokenlized.write(text_tokenlized)
		hdf_trectext.write(text_trectext)
	hsf.close()
	hdf_clas.close()
	hdf_tokenlized.close()
	return

def TokenAndPos_batch(sf,df_clas,df_tokenlized,df_trectext,userdict=None):
	CreatTargetDir(sf,df_clas)
	CreatTargetDir(sf,df_tokenlized)
	if userdict:
		Nlpir.ImportUserDict(userdict)
		Nlpir.SaveTheUsrDic()	#only one userdict permitted.
	if os.path.isdir(sf):
		for subfile in os.listdir(sf): 
			TokenAndPos(sf+'/'+subfile, df_clas+'/'+subfile, df_trectext+'/'+subfile)
	else:
		TokenAndPos(sf, df_clas, df_tokenlized, df_trectext)


#from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize, sent_tokenize
#from nltk.stem.porter import PorterStemmer
#ENGLISH_STOPWORDS = stopwords.words('english')
#PORTER_STEMMER = PorterStemmer()
#def ProcessEnglish(text):	
#	tokens = [[word for word in word_tokenize(sent)] for sent in sent_tokenize(text.lower())]
#	result = ''
#	# filter the stopwords 
#	for sent in tokens:	
#		tokens_filter_stop = [word for word in sent if not word in ENGLISH_STOPWORDS]
#		# filter all punctuation
#		tokens_filter_punc = filter(lambda word: word not in ''',.-'"''', tokens_filter_stop)
#		# stemming
#		tokens_stem = [PORTER_STEMMER.stem(word) for word in tokens_filter_punc]
#		result += ' '.join(tokens_stem)
#	return result


def main():
#	text = "Mr. Write says 'the state has a maritime border with Rhode Island east of Long Island, as well as an international border with the Canadian provinces of Ontario to the north and west, and Quebec to the north.'"
#	print(ProcessEnglish(text))


	sf = './CommentData-1K.txt' #源文件(夹)
	df_preprocess = sf+'-preprocess' #预处理后的文件(夹)
	df_clas = sf+'-clas' #分词及词性标注好的文件(夹)
	df_tokenlized = sf+'-tokenlized' #分词及词性标注好的文件(夹)
	df_trectext = sf+'-trectext'
	PreProcess_batch(sf,df_preprocess)

	'''分词和词性标注：利用张华平的NLPIR对文件分词、新词发现、词性标注等'''
	userDict = './Data/MyMixedDict.txt'  # 用户提供的词典
	'''初始化NLPIR'''
	if not Nlpir.Init('',Nlpir.ENCODING.UTF8_CODE,''):
	    print("Initialization failed!")
	    sys.exit(-111111)

	'''分词及词性标，并生成 Stanford parser 需要的分词结果'''
	TokenAndPos_batch(df_preprocess,df_clas,df_tokenlized,df_trectext,userDict)
	Nlpir.Exit() # 退出NLPIR


if __name__ == "__main__":
	main()

