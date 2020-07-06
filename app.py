from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)
app.secret_key = "mysecret123"

url = "https://api.rootnet.in/covid19-in/stats/latest"

response = requests.get(url)

covidData = response.json()

indiaTotal = {
    "total" : covidData['data']['summary']['total'],
    "recovered" : covidData['data']['summary']['discharged'],
    "death" : covidData['data']['summary']['deaths'],
    "active" : covidData['data']['summary']['total'] - (covidData['data']['summary']['discharged'] + covidData['data']['summary']['deaths']),
}

stateData = []

for stateCount in range(0, 35):
    stateData.append([
        covidData['data']['regional'][stateCount]['loc'],
        covidData['data']['regional'][stateCount]['totalConfirmed'],
        covidData['data']['regional'][stateCount]['discharged'],
        covidData['data']['regional'][stateCount]['totalConfirmed'] - (covidData['data']['regional'][stateCount]['discharged'] + covidData['data']['regional'][stateCount]['deaths']),
        covidData['data']['regional'][stateCount]['deaths'],  
    ])

#print(indiaTotal)
#print(stateData)

@app.route('/')
def index():
    return render_template("index.html", indiaTotal = indiaTotal, stateData = stateData)

@app.route('/assessment')
def assessment():
    return render_template("assessment.html")

@app.route('/symptoms')
def symptoms():
    return render_template("symptoms.html")

@app.route('/helpline')
def helpline():
    return render_template("helpline.html")

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug = True)