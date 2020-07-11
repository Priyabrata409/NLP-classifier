from flask import Flask,render_template,request,flash
import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import numpy as np
import nltk
nltk.download("stopwords")
lema=WordNetLemmatizer()
app=Flask(__name__)
app.secret_key="kunu_lucky_pintu"
@app.route("/")
def home():
    return render_template("home.html")
with open("model_nlp.pkl","rb") as f:
    model=pickle.load(f)
cv=model[0]
classifier=model[1]
punc=""":;""?!#@&.,"""

@app.route("/predict",methods=["POST","GET"])
def predict():
  #  data = pd.read_csv("Restaurant_Reviews.tsv", delimiter="\t", quoting=3)
   # from nltk.corpus import stopwords
  
   # from nltk.stem import WordNetLemmatizer
   # corpus = []
   # punc = """:;""?!#@&.,"""
   # lema = WordNetLemmatizer()
   # for i in range(0, 1000):
   #     mess = [w for w in data.Review[i] if w not in punc]
   #     mess = "".join(mess)
   #     mess = mess.lower()
   #     all_stop_word = stopwords.words("english")
   #     all_stop_word.remove('not')
   #     all_stop_word.remove('no')
   #     all_stop_word.remove("didn't")
   #     all_stop_word.remove("won't")
   #     all_stop_word.remove("shan't")

      #  message = [lema.lemmatize(word) for word in mess.split() if word not in set(all_stop_word)]
      #  message = " ".join(message)
      #  corpus.append(message)
    #from sklearn.feature_extraction.text import CountVectorizer
    #cv = CountVectorizer(max_features=1500)
    #X = cv.fit_transform(corpus).toarray()
    #y = data.iloc[:, -1].values
    #from sklearn.linear_model import LogisticRegression
    #classifier = LogisticRegression()
    #classifier.fit(X, y)
    #model = [cv, classifier]
    #with open("model_nlp.pkl", "wb") as f:
    #    pickle.dump(model, f)
    if request.method == "POST":
        review = request.form["review"]
        if review=="":
            return render_template("home.html")
        else:
            li = []
            feed = review
            review = [word for word in feed if word not in punc]
            review = ''.join(review)
            review = review.lower()
            all_stopwords = stopwords.words("english")
            all_stopwords.remove("not")
            all_stopwords.remove("no")
            all_stopwords.remove("didn't")
            all_stopwords.remove("won't")
            all_stopwords.remove("shan't")
            reviw = [lema.lemmatize(word) for word in review.split() if word not in set(all_stopwords)]
            review = ' '.join(reviw)
            li.append(review)
            result = classifier.predict(cv.transform(li))
            if result == 1:
                flash(f"Hurray!! Resturant got a Good Review ", "info")
            else:
                flash(f"Sorry!! Bad Review! Maybe Resturant needs to improvise its servises","info")

            return render_template("home.html")
    else:
        return render_template("home.html")
if __name__=="__main__":
    app.run(debug=True)
