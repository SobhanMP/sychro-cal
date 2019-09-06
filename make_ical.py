import pandas as pd
from datetime import datetime, timedelta
from ics import *
import pytz

week = timedelta(days=7)
tz = pytz.timezone('America/Toronto')


def make_ical(df):
    calendar = Calendar()
    t = df['Dates début/fin'].map(lambda x: x.split('-'))
    df['begin_date'] = pd.to_datetime([x[0] for x in t])
    df['end_date'] = pd.to_datetime([x[-1] for x in t])
    t = df['Jours et heures']
    df['begin_time'] = pd.to_datetime(t.map(lambda x: x.split(' ')[1]))
    df['end_time'] = pd.to_datetime(t.map(lambda x: x.split(' ')[-1]))
    print(df.head())

    for n, i in df.iterrows():
        date = i['begin_date']
        end_date = i['end_date']
        while date <= end_date:
            time = i['begin_time']
            begin = tz.localize(date + timedelta(hours=time.hour, minutes=time.minute))
            time = i['end_time']
            end = tz.localize(date + timedelta(hours=time.hour, minutes=time.minute))
            i.fillna('')
            e = {
                'begin': begin,
                'end': end,
                'name': (str(i['Volet']) + ' ' + i['course name']).strip(),
                'location': i['Local'],
                # 'status': 'CANCELLED'
            }
            if i['Volet'] != '':
                e['categories'] = set([str(i['Volet'])])
            e = Event(**e)
            calendar.events.add(e)
            date += week

    return calendar
