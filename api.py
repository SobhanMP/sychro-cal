import json

import pandas as pd
from flask import Flask, Response
from flask_cors import CORS
from flask import request
import tempfile
from get_file import login, get_semester_list, get_courses
from make_ical import make_ical
from open_file import read_table

app = Flask(__name__)
CORS(app)


@app.route('/sessions', methods=['POST'])
def hello_world():
    data = request.json
    print(data['username'])

    username = data['username']
    password = data['password']

    driver = login(username, password, headless=True)
    result = get_semester_list(driver)
    driver.quit()
    return json.dumps(result)

import time
@app.route('/calendar', methods=['POST'])
def f():
    now = time.time()
    data = request.json
    print(data['username'])

    username = str(data['username'])
    password = str(data['password'])

    driver = login(username, password, headless=True)
    result = get_semester_list(driver)
    if 'selection' in data:
        selection = data['selection']
    else:
        selection = list(range(len(result)))
    course_tables = get_courses(selection, driver)
    driver.quit()
    tables = [read_table(table) for table in course_tables]

    courses = pd.concat(tables)
    calendar = make_ical(courses)
    print('took {}s'.format(time.time() - now))
    return Response(''.join(calendar),
                    mimetype='text/calendar',
                    headers={'Content-Disposition': 'attachment; filename=calendar.ics'})


if __name__ == '__main__':
    app.run(host="0.0.0.0", ssl_context='adhoc')
