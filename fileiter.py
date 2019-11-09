from itertools import islice



def read(filename, n=20):
    with open(filename, 'r') as f:
        while True:
            lines =  ''.join([line for line in islice(f, n)])
            if lines == '':
                break
            yield lines
