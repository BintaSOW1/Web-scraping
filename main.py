from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route('/')
def index():
    data = []
    with open('amazon_product_dat.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data.append(row)
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)