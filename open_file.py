from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
import pandas as pd
from collections import defaultdict
import json


def read_html(file):
    soup = BeautifulSoup(file, 'html.parser')
    i: Tag
    data = defaultdict(list)
    for i in soup.find('tbody').find_all('tr', recursive=False):

        i = i.find('tbody')
        if i is None:
            continue

        name_holder, rest = i.find_all('tr', recursive=False)
        if name_holder is None:
            continue
        name = name_holder.text.strip()

        rest = list(filter(lambda x: type(x) != NavigableString and x.text.strip() != "", rest.find('tbody').find_all('tr', recursive=False)))[-1]
        rest = rest.find('tbody').find('tbody').find_all('tr', recursive=False)
        print(name, end=';\n')

        column_name = [b.text.strip() for b in rest[0].find_all('th')]
        column_name.append('course name')

        rows: Tag
        # drop column names
        rows = rest[1:]

        for row in rows :
            row = list(map(lambda x: x.text.strip(), row.find_all('td')))
            row.append(name)
            print('; '.join(row))
            print(column_name)
            for k, c in zip(row, column_name):
                # print(k, end='; ')
                data[c].append(k)
            # print()
    data = dict(data)
    df = pd.DataFrame(data=data, columns=column_name)
    return df


if __name__ == '__main__':
    df = read_html(open('page.html'))
    df.to_pickle('courses.csv')
    print(df.head())
