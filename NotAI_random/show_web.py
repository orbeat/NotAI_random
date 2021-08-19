import statistics as st

from flask import Flask
from flask.globals import request
from flask.helpers import make_response
from flask.json import jsonify
from flask.templating import render_template

app = Flask(__name__)

targetdir = r"C:\orbeat\NotAI\data/"
refiend_data_df = st.load_csv(targetdir)
refiend_data_df['control'] = refiend_data_df['z']*6 + refiend_data_df['x']*12 + refiend_data_df['left']*2 + refiend_data_df['right']*4 + refiend_data_df['down']

@app.route('/show.ppt')
def jsonTest():
    return render_template("ppt.html")

if __name__=='__main__': 
    app.run('0.0.0.0', 2021, True)
