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
    # return render_template("ppt.html")
    html = r"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Insert title here</title>
    <link rel="stylesheet" href="http://code.jquery.com/mobile/1.3.2/jquery.mobile-1.3.2.min.css" />
    <script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>
    <script src="http://code.jquery.com/mobile/1.3.2/jquery.mobile-1.3.2.min.js"></script>
    <style type="text/css">
    #cover{
        height: 730px;
        display: block; margin: 0px auto;
    }
    </style>
    </head>
    <body>
    """
    for i in range(1, 32):
        html += r'''
        <div data-role="page" id="page''' + str(i) + r'''">
            <div data-role="content">
                <a href="#page''' + str(i+1) + r'''">
                    <img id="cover" src="https://github.com/orbeat/NotAI_random/blob/main/NotAI_random/show_example/NotAI_random_ppt/NotAI_random_ppt%20(''' + str(i) + r''').png?raw=true">
                    <br><br><br><br><br>
                </a>
            </div>
        </div>
        '''

    html += r"""
    </body>
    </html>
    """
    # print(html)
    return html

if __name__=='__main__': 
    app.run('0.0.0.0', 2021, True)
