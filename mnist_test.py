from flask import Flask, request, render_template, make_response
import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    from_year = int(request.form['from_year'])
    ref_days = int(request.form['ref_days'])
    code = request.form['code']
    code_dl = code + ".t"

    end_date = datetime.now()
    start_date = datetime(end_date.year - from_year, 1, 1)
    df = yf.download(code_dl, start=start_date, end=end_date, interval="1d")

    fig, ax = plt.subplots()
    ax.plot(df['Close'])
    ax.set_title('Close Price History')
    ax.set_xlabel('Date')
    ax.set_ylabel('Close Price')

    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return make_response(img.getvalue(), 200, {'Content-Type': 'image/png'})

if __name__ == '__main__':
    app.run(debug=True)