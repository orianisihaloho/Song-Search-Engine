from flask import Flask, render_template, request
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import pandas as pd
import json
import webbrowser
import numpy as np
import math
import copy


app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def process():
	if request.method == 'GET':
		return render_template('result.html')

	elif request.method =='POST':
		kata = request.form['keyword']
		kataDepan = set(stopwords.words('english'))
		datasets = pd.read_csv("data/datasets.csv")
		dokumen = datasets.values.tolist()
		index = pd.read_csv("data/index.csv")
		index = index.values.tolist()
		
		stemmer = PorterStemmer()
		result = [[] for i in range(len(dokumen))]
		data = []

		# stemming every user's input
		kata = stemmer.stem(kata)
		kata = kata.split()

		# eliminating prepositions if there are any
		kata = [x for x in kata if x not in kataDepan]
		index = [x for x in index if x[0] in kata]

		# searching through index if there're documents containing the keywords
		for i in range(len(dokumen)):
			result[i].append(i+1)
			temp = 0
			for n in range(len(index)):
				temp += index[n][i+1]
			result[i].append(temp)

		result = [x for x in result if x[1] > 0]

		# sorting result using result variable
		result = sorted(result, key=lambda x: x[1], reverse=True)

		for i in range(len(result)):
			data.append(dokumen[result[i][0]-1])

		return render_template('result.html', keyword=" ".join(kata), data=data)
		
		
	# else:
 #        '<center>404 Not Found</center>'

# run app
if __name__ == "__main__":
    app.run(debug=True)