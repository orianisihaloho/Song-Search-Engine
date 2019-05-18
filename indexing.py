
from nltk.stem import PorterStemmer
from collections import Counter
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import math
import copy




kataDepan = set(stopwords.words('english'))
datasets = pd.read_csv("data/datasets.csv")
dokumen = datasets.values.tolist()
stemmer = PorterStemmer()

stemmedDoc, index = [], []

for baris in dokumen:
	arrayTempBaris = baris[2].split()

	#  - Filtering - cek bila kata memiliki stopword yang harus dihapus
	arrayTempBaris = [x for x in arrayTempBaris if x not in kataDepan]
	tempBaris = " ".join(arrayTempBaris)

	# - Stemming - mengubah menjadi kata dasar
	tempBaris = stemmer.stem(tempBaris)
	stemmedDoc.append(tempBaris.split())

for record in stemmedDoc:
	for kata in record:
		if kata not in index:
			index.append(kata)

df_index = pd.DataFrame({
	'kata':index
	})

for i in range(len(stemmedDoc)):
	terdeteksi = []
	for kata in index:
		terdeteksi.append(stemmedDoc[i].count(kata))
	df_index[i+1] = pd.Series(terdeteksi)

print(df_index)

df_index.to_csv("data/index.csv", index=False)