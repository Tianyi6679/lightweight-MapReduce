#!/usr/bin/env python
import distmm
import re
import string

data = ['98.txt_split_4/98.txt_0',
        '98.txt_split_4/98.txt_1',
        '98.txt_split_4/98.txt_2',
        '98.txt_split_4/98.txt_3']
# The data source can be any dictionary-like object
datasource = dict(enumerate(data))

print(datasource)


def mapfn(k, v):
    for w in re.sub('['+string.punctuation+']', '', v).split():
        yield w.lower(), 1


def reducefn(k, vs):
    result = sum(vs)
    return result

def reducefn2(k, vs):
    result = sum(vs)
    return result

def reducefn3(k, vs):
    result = sum(vs)
    return result


options = {
        'datasource': datasource,
        'mapfn': mapfn,
        'reducefn': reducefn
}

results = distmm.run_server(options)

options['reducefn'] = reducefn2
results = distmm.run_server(options)

options['reducefn'] = reducefn3
results = distmm.run_server(options)