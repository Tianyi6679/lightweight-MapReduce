#!/usr/bin/env python
import distmm
import fileiter

data = fileiter.read('1342-0.txt', 500)
# The data source can be any dictionary-like object
datasource = dict(enumerate(data))


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
print(results)
print(len(results))
