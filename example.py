#!/usr/bin/env python
import distmm

data = ['1342-0.txt_split_4\\1342-0.txt_0',
        '1342-0.txt_split_4\\1342-0.txt_1',
        '1342-0.txt_split_4\\1342-0.txt_2',
        '1342-0.txt_split_4\\1342-0.txt_3']
# The data source can be any dictionary-like object
datasource = dict(enumerate(data))

print(datasource)


def mapfn(k, v):
    for w in v.split():
        yield w, 1


def reducefn(k, vs):
    result = sum(vs)
    return result


options = {
        'datasource': datasource,
        'mapfn': mapfn,
        'reducefn': reducefn
}

results = distmm.run_server(options)
