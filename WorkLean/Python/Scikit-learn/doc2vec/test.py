#%matplotlib inline
import pandas as pd
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import jieba as jb
import re
from sklearn import utils
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from gensim.models.doc2vec import TaggedDocument
import multiprocessing
from gensim.models import Doc2Vec
from tqdm import tqdm


df = pd.read_csv('./data/shopping.csv')
df=df[['cat','review']]
print("数据总量: %d ." % len(df))
# print(df.sample(10))

# print("在 cat 列中总共有 %d 个空值." % df['cat'].isnull().sum())
# print("在 review 列中总共有 %d 个空值." % df['review'].isnull().sum())
df[df.isnull().values==True]
df = df[pd.notnull(df['review'])]
df = df.reset_index(drop=True)
# print(df.head())
# d = {'cat':df['cat'].value_counts().index, 'count': df['cat'].value_counts()}
# df_cat = pd.DataFrame(data=d).reset_index(drop=True)
# print(df_cat)

# df_cat.plot(x='cat', y='count', kind='bar', legend=False,  figsize=(8, 5))
# plt.rcParams['font.sans-serif']=['SimHei']		#防止中文乱码
# plt.rcParams['axes.unicode_minus']=False
# plt.title("类目数量分布")
# plt.ylabel('数量', fontsize=18)
# plt.xlabel('类目', fontsize=18)
# plt.show()

def remove_punctuation(line):
    line = str(line)
    if line.strip()=='':
        return ''
    line = ''.join(re.findall('[\u4e00-\u9fa5]',line))
    return line

def stopwordslist(filepath):  
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]  
    return stopwords  

stopwords = stopwordslist("./data/chineseStopWords.txt")

df['clean_review'] = df['review'].apply(remove_punctuation)

df['cut_review'] = df['clean_review'].apply(lambda x: [w for w in list(jb.cut(x)) if w not in stopwords])
# print(df.head())
train, test = train_test_split(df, test_size=0.3, random_state=42,stratify = df.cat.values)

train_tagged = train.apply(
    lambda r: TaggedDocument(words=r['cut_review'], tags=[r['cat']]), axis=1)
test_tagged = test.apply(
    lambda r: TaggedDocument(words=r['cut_review'], tags=[r['cat']]), axis=1)

cores = multiprocessing.cpu_count()

model_dbow = Doc2Vec(dm=0,  negative=5, hs=0, min_count=2, sample = 0, workers=cores)
model_dbow.build_vocab([x for x in tqdm(train_tagged.values)])

# %%time
for epoch in range(30):
    model_dbow.train(utils.shuffle([x for x in tqdm(train_tagged.values)]), total_examples=len(train_tagged.values), epochs=1)
    model_dbow.alpha -= 0.002
    model_dbow.min_alpha = model_dbow.alpha

def vec_for_learning(model, tagged_docs):
    sents = tagged_docs.values
    targets, regressors = zip(*[(doc.tags[0], model.infer_vector(doc.words, steps=20)) for doc in sents])
    return targets, regressors
 
y_train, X_train = vec_for_learning(model_dbow, train_tagged)
y_test, X_test = vec_for_learning(model_dbow, test_tagged)

print(y_train.head(),X_train.head())


# #使用逻辑回归来预测
# logreg = LogisticRegression(n_jobs=1, C=1e5)
# logreg.fit(X_train, y_train)
# y_pred = logreg.predict(X_test)

# from sklearn.metrics import accuracy_score, f1_score
 
# print('Testing accuracy %s' % accuracy_score(y_test, y_pred))
# print('Testing F1 score: {}'.format(f1_score(y_test, y_pred, average='weighted')))