from flask import Flask, render_template, request
import joblib

model = joblib.load('model.pkl')

app = Flask(__name__)

city_names = ['NewYork', 'Boston', 'Phildelphia', 'Pittsburg', 'Buffalo',
    'AtlanticCity', 'Portland', 'Cambridge', 'Hartford', 'Springfield',
    'Syracuse', 'Baltimore', 'York', 'Trenton', 'Warwick',
    'WashingtonDC', 'Providence', 'Harrisburg', 'Newport', 'Stamford',
    'Worcester', 'Atlanta', 'Brimingham', 'Charleston', 'Charlotte',
    'Louisville', 'Memphis', 'Nashville', 'NewOrleans', 'Raleigh',
    'Houston', 'Georgia', 'Oklahoma', 'Orlando', 'Macon', 'Huntsville',
    'Knoxville', 'Florence', 'Miami', 'Tampa', 'PanamaCity',
    'Kingsport', 'Marshall', 'Mandan', 'Waterloo', 'IowaCity',
    'Columbia', 'Indianapolis', 'Cincinnati', 'Bloomington', 'Salina',
    'KanasCity', 'Brookings', 'Minot', 'Chicago', 'Lincoln',
    'FallsCity', 'GrandForks', 'Fargo', 'Cleveland', 'Canton',
    'Columbus', 'Rochester', 'Minneapolis', 'JeffersonCity',
    'Escabana', 'Youngstown', 'SantaRosa', 'Eureka', 'SanFrancisco',
    'SanJose', 'LosAngeles', 'Oxnard', 'SanDeigo', 'Oceanside',
    'Carlsbad', 'Montrose', 'Prescott', 'Fresno', 'Reno', 'LasVegas',
    'Tucson', 'SanLuis', 'Denver', 'Kingman', 'Bakersfield',
    'Mexicali', 'SilverCity', 'Pheonix', 'SantaFe', 'Lovelock']
cities = dict(zip(city_names,[55,  5, 63, 64,  8,  1, 65,  9, 29, 79, 81,  3, 89, 83, 85, 86, 67,
    28, 56, 80, 88,  0,  6, 12, 13, 42, 47, 53, 54, 68, 30, 26, 58, 59,
    44, 31, 38, 24, 49, 82, 61, 37, 46, 45, 87, 33, 17, 32, 15,  4, 71,
    35,  7, 51, 14, 40, 22, 27, 23, 16, 10, 18, 70, 50, 34, 20, 90, 77,
    21, 73, 74, 41, 60, 72, 57, 11, 52, 66, 25, 69, 39, 84, 75, 19, 36,
     2, 48, 78, 62, 76, 43]))
job_names = ['Actor', 'Engineer', 'Academician', 'Chef', 'HomeMakers', 'Dancer',
    'Singer', 'DataScientist', 'Police', 'Student', 'Doctor',
    'Manager', 'Photographer', 'Beautician', 'CA', 'Blogger', 'CEO',
    'Labourer', 'Accountant', 'FilmDirector', 'Technician',
    'FashionDesigner', 'Architect', 'HouseKeeper', 'FilmMaker',
    'Buisnessman', 'Politician', 'DefencePersonnels', 'Analyst',
    'Clerks', 'ITProfessional', 'Farmer', 'Journalist', 'Lawyer',
    'GovEmployee']
job_titles = dict(zip(job_names,[ 2, 16,  0, 10, 22, 12, 32, 13, 30, 33, 15, 28, 29,  5,  8,  6,  9,
    26,  1, 19, 34, 18,  4, 23, 20,  7, 31, 14,  3, 11, 24, 17, 25, 27,
    21]))
disease_names = ['NoDisease', 'Epilepsy', 'EyeDisease', 'Alzheimer', 'Arthritis',
    'HeartDisease', 'Diabetes', 'Cancer', 'High BP', 'Obesity']
diseases = dict(zip(disease_names,[8, 4, 5, 0, 1, 6, 3, 2, 7, 9]))

@app.route("/")
def home():
    return render_template('home.html', cities=city_names, jobs=job_names, hereditary_diseases=disease_names)

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    try:
        if request.method == 'POST':
            age = int(request.form['age'])
            sex_select = request.form['sex']
            sex = 1 if sex_select == 'MALE' else 0
            weight = float(request.form['weight'])
            bmi = float(request.form['bmi'])
            dis_selected = request.form['disease']
            hereditary_disease = diseases[dis_selected]
            no_of_dependents = int(request.form['no_dependents'])
            smoke_select = request.form['smoke']
            smoker = 1 if smoke_select == 'YES' else 0
            city_select = request.form['city']
            city = cities[city_select]
            bp = float(request.form['blood_pressure'])
            diab_select = request.form['diabetes']
            diabetes = 1 if diab_select == 'YES' else 0
            reg_ex_select = request.form['regular_exercise']
            regular_exercise = 1 if reg_ex_select == 'YES' else 0
            job_title_selected = request.form['job_title']
            job_title = job_titles[job_title_selected]

            # Make prediction
            predictions = model.predict([[
                age,
                sex,
                weight,
                bmi,
                hereditary_disease,
                no_of_dependents,
                smoker,
                city,
                bp,
                diabetes,
                regular_exercise,
                job_title
            ]])

            # Process the prediction
            output = predictions[0] * 12147.834670761482
            output = "{:,.3f}".format(output)

            return render_template('home.html', cities=city_names, jobs=job_names, hereditary_diseases=disease_names, prediction_text="Your estimated health insurance claim is ${}.".format(output))
    except Exception as e:
        return render_template('home.html', cities=city_names, jobs=job_names, hereditary_diseases=disease_names, prediction_text="An error occurred: {}".format(e))

if __name__ == '__main__':
    app.run(port=8080)
