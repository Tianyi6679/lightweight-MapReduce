#!/usr/bin/env python
import distmm

data = ["Humpty Dumpty sat on a wall",
        "Humpty Dumpty had a great fall",
        "All the King's horses and all the King's men",
        "Couldn't put Humpty together again",
        ]
data *= 10
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
