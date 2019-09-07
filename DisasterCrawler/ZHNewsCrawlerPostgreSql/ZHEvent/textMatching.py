# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 13:43:47 2019

@author: 86183
"""

import jieba
from gensim import corpora,models,similarities

def textAnalysis(all_doc,doc_test):

	all_doc_list = []
	for doc in all_doc:
	    doc_list = [word for word in jieba.cut(doc)]
	    all_doc_list.append(doc_list)

	doc_test_list = [word for word in jieba.cut(doc_test)]

	dictionary = corpora.Dictionary(all_doc_list)				#获取词袋

	corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]	#向量转化

	doc_test_vec = dictionary.doc2bow(doc_test_list)			#测试文本向量转化

	tfidf = models.TfidfModel(corpus)							#TF-IDF建模分析

	index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
	sim = index[tfidf[doc_test_vec]]

	maxProbabilityList = sorted(enumerate(sim), key=lambda item: -item[1])
	return maxProbabilityList[0]


