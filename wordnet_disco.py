from nltk.corpus import wordnet as wn
from collections import OrderedDict
from scipy import spatial
import numpy as np
import operator
import commands
import pymysql
import math
import os

############################################connecting to db and fetch last id in db

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='semantic-similarity-tool_development', autocommit=True)
cur = conn.cursor()
cur.execute("SELECT id,textb1,textb2 FROM wordnet_disco_sems ORDER BY id DESC LIMIT 1");
tb_word = []
for row in cur:
	tb_word.append(row)

row_id = tb_word[0][0]

####################################################################################

#########################################################################print func

def _print(_text, _obj):
	print("\n############### " + _text + " ###############\n")
	print(_obj)
	print("\n####################################################\n")

###################################################################################


stopword = ["***", "<", ">", "/", "\\", "]", "[", "}", "{", "'", "\"", ":", ";", ",", ".", "==", "**", "=", "+", ")", "(", "*", "&", "^", "%", "$", "#", "@", "!", "-", "_", "...", "a", "[pic]", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"]

tb1_word = list(set((tb_word[0][1].lower()).split(' ')) - set(stopword))
tb2_word = list(set((tb_word[0][2].lower()).split(' ')) - set(stopword))
tb1_word = list(filter(None, tb1_word))
tb2_word = list(filter(None, tb2_word))
docWordList = [tb1_word, tb2_word]

allWordList_Dup  = tb1_word + tb2_word
allWordList  = list(set(tb1_word) | set(tb2_word))

_print("All words list with duplicate", allWordList_Dup)
_print("All words list no duplicate", allWordList)

#################################################count of word in both textbox  (df)

wordsCountInAllDocs = {}

def df():
	for i in allWordList_Dup:
		wordsCountInAllDocs[i] = allWordList_Dup.count(i)
	
	_print("All words Count",wordsCountInAllDocs)
	_print("textbox1 words", tb1_word)
	_print("textbox2 words", tb2_word)
	
####################################################################################

#####################################################################calculate tfidf

final_tfidf_dic = {}							    		#final tfidfs for textbox 1 and 2

# df()                                                		#calling the df to calculate df

def tfidf(wordlist):
	# for docsword in docWordList:				    		#each doc
	tfidfList = {}											#dic that has words and tfidf  (result)
	for word in wordlist:					    		    #each word in doc to claculate tfidf
		tf = wordlist.count(word)     						#term frequency
		df = allWordList_Dup.count(word)              		#doc frequency
		_tfidf = (1 + math.log10(tf)) * (math.log10(2/df))
		tfidfList[word] = round(_tfidf,5)
	
	_print("tfidf of textboxes",tfidfList)
	
	return tfidfList

####################################################################################

#####################function that get two words and return similarity using WORDNET

def wordnet(word1, word2):					
	w1 = wn.synsets(word1)
	w2 = wn.synsets(word2)
	if w1 and w2: 
		s = w1[0].wup_similarity(w2[0])
		print(word1," and ",word2,"  wordnet is " + str(s))
		return s
	else:
		print("wordnet can not find any similarity")
		return 0

####################################################################################

#######################function that get two words and return similarity using DISCO

def disco(word1, word2):
	s = str("java -jar disco-2.1.jar enwiki-20130403-word2vec-lm-mwl-lc-sim/ -s2 " + word1 + " " + word2)
	(a, b) = commands.getstatusoutput(s)
	print(word1," and ",word2,"  disco is " + b)
	return b

####################################################################################

#########################################################calculate wordnet and disco

firstmap = tfidf(tb1_word)                          		#first textboxes tfidfs
secondmap = tfidf(tb2_word)                       		  	#second textboxes tfidfs

def wordnet_disco_semantic():
	tb1_d 		= []										#list that contains similarity numbers in textbox1 for disco
	tb2_d 		= []										#list that contains similarity numbers in textbox2 for disco
	tb1_w 		= []										#list that contains similarity numbers in textbox1 for wordnet
	tb2_w    	= []										#list that contains similarity numbers in textbox2 for wordnet

	avg_disco   = 0
	avg_wordnet = 0
	count 		= 0
	
	for w in allWordList:
		if w not in tb1_word:								#word that is in textbox2 is not in textbox1
			for ww in tb1_word:
				disco_n      = disco(w, ww)			        #calling disco func
				wordnet_n    = wordnet(w, ww)				#calling wordnet func
				avg_disco   += round(float(disco_n),2)
				avg_wordnet += round(float(wordnet_n),2)
				count 		+= 1

			tb1_d.append(round(float(avg_disco/count),2))
			tb1_w.append(round(float(avg_wordnet/count),2))

			tb2_d.append(float(secondmap[w]))
			tb2_w.append(float(secondmap[w]))
			avg = 0
			count = 0

		elif w not in tb2_word:								#word that is in textbox1 is not in textbox2
			for ww in tb2_word:
				disco_n      = disco(w, ww)         		#calling disco func
				wordnet_n    = wordnet(w, ww)				#calling wordnet func
				avg_disco   += round(float(disco_n),2)
				avg_wordnet += round(float(wordnet_n),2)
				count 		+= 1

			tb2_d.append(round(float(avg_disco/count),2))
			tb2_w.append(round(float(avg_wordnet/count),2))

			tb1_d.append(float(firstmap[w]))
			tb1_w.append(float(firstmap[w]))
			avg = 0
			count = 0

		else:												#words that is in both textboxes
			tb1_d.append(float(firstmap[w]))				#adding word to all 	
			tb2_d.append(float(secondmap[w]))
			tb1_w.append(float(firstmap[w]))
			tb2_w.append(float(secondmap[w]))


	_print("tb1_disco"  , tb1_d)
	_print("tb2_disco"  , tb2_d)
	_print("tb1_wordnet", tb1_w)
	_print("tb2_wordnet", tb2_w)

	disco_cosine   = 0
	wordnet_cosine = 0

	if sum(tb2_d) != 0:
		disco_cosine = 1 - spatial.distance.cosine(tb1_d, tb2_d)
	else:
		disco_cosine = 0

	if sum(tb2_w) != 0:
		wordnet_cosine = 1 - spatial.distance.cosine(tb1_w, tb2_w)
	else:
		wordnet_cosine = 0

	_print("cosine of disco result"  , str(disco_cosine))
	_print("cosine of wordnet result", str(wordnet_cosine))

	sql_disco   = 'UPDATE wordnet_disco_sems set disco_result=\"'+str(disco_cosine)+'\" WHERE id='+str(row_id)
	sql_wordnet = 'UPDATE wordnet_disco_sems set wordnet_result=\"'+str(wordnet_cosine)+'\" WHERE id='+str(row_id)
	
	cur.execute(sql_disco);
	cur.execute(sql_wordnet);

####################################################################################


###################################################################calling functions

# tfidf()													#callnin tfidf to calculate
wordnet_disco_semantic()									#claculate disco semantic similarity

cur.close()
conn.close()