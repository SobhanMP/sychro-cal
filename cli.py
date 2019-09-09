#!python3
import json
import itertools as itt

import pandas as pd

from open_file import read_table
from make_ical import make_ical
from getpass import getpass
from sys import argv
from get_file import login, get_semester_list, get_courses
import argparse

if __name__ == '__main__':
    # if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='transform course selection into ical')
    parser.add_argument('--config', default=None)
    args = parser.parse_args()
    if args.config is not None:
        configs = json.load(open(args.config))
    else:
        configs = dict()
    try:
        username = configs['username']
    except KeyError as e:
        username = input('username: ')

    try:
        password = configs['password']
    except KeyError as e:
        password = getpass('password (hidden): ')

    driver = login(username, password)
    for index, semester_name in zip(itt.count(0), get_semester_list(driver)):
        print(index, ': ', '\t\t'.join(semester_name.split('\n')), end=';\n')
    def get_semester_selection():
        return list(map(int, input('enter desired semesters, seperated by space: ').split(' ')))
    try:
        semester_selection = configs['selection']
    except KeyError as e:
        semester_selection = get_semester_selection()

    course_tables = get_courses(semester_selection, driver)
    driver.close()

    tables = [read_table(table) for table in course_tables]

    courses = pd.concat(tables)
    calendar = make_ical(courses )

    try:
        outfile_name = configs['outfile']
    except KeyError as e:
        outfile_name = input('outfile name: ')

    with open(outfile_name, 'w') as fd:
        fd.writelines(calendar)
