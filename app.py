from flask import Flask, request, render_template, jsonify
import pickle




app = Flask(__name__)



def load_model():
       with open('rfc_model.pickle','rb') as f:
              model = pickle.load(f)
       return model
       

@app.route('/')
def home():
       return render_template('index.html')

@app.route('/_predict', methods=['GET','POST'])
def predict():
       if request.method == 'POST':
              age = int(request.form['age'])
              fare = float(request.form['fare'])
              pclass = int(request.form['pclass'])
              parch = int(request.form['parch'])
              sibsp = int(request.form['sibsp'])
              sex = request.form['sibsp']
              embark = request.form['embark']

       sex_male = None
       sex_female = None
       Embarked_C = None
       Embarked_Q = None
       Embarked_S = None
       model = None
       pred = None

       model = load_model()
       
       if sex == 'sex_male':
              sex_male = 1
              sex_female = 0
       else:
              sex_male = 0
              sex_female = 1

       if embark == 'Embarked_C':
              Embarked_C = 1
              Embarked_Q = 0
              Embarked_S = 0
       elif embark == 'Embarked_Q':
              Embarked_C = 0
              Embarked_Q = 1
              Embarked_S = 0
       elif embark == 'Embarked_S':
              Embarked_C = 0
              Embarked_Q = 0
              Embarked_S = 1

       
       prediction = model.predict([[pclass,age,sibsp,parch,fare,sex_female, sex_male,Embarked_C, Embarked_Q,Embarked_S]])[0]
       if prediction == 1:
              pred = 'Survived'
       else:
              pred = 'Not Survived'
       response = jsonify({
              'estimate_prediction' : pred
       })
       response.headers.add('Access-Control-Allow-Orgin', '*')
       return response








if __name__ == '__main__':
       app.run(debug=True)