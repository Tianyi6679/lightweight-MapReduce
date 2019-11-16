from itertools import islice
import optparse
import os


def read(filename, n=20):
    # if you get UnicodeDecodingError below, try specifying utf-8 as encoding method
    with open(filename, 'r') as f:
        while True:
            lines = ''.join([line for line in islice(f, n)])
            if lines == '':
                break
            yield lines


def split_file(filename, n=4):
    f = read(filename)
    dirname = "./%s_split_%d" % (filename, n)
    try:
        os.mkdir(dirname)
    except FileExistsError:
        print("file already processed, please delete the directory before resplit")
        return
    files = [open("%s/%s_%d" % (dirname, filename, i), 'w') for i in range(n)]
    for i, line in enumerate(f):
        files[i % n].write(line)
    for f in files:
        f.close()


def splitter_options_parse():
    parser = optparse.OptionParser(usage='%prog [options]', version='%%prog %s' % '0.0.1')
    parser.add_option('-f', '--filename', dest='filename', default="", help='name of input file')
    parser.add_option('-n', '--number_of_splits', dest='number_of_splits', default='4',
                      help='number of splits')
    return parser


if __name__ == '__main__':
    parser = splitter_options_parse()
    (options, args) = parser.parse_args()
    if options.filename == "":
        print("please enter file name")
    else:
        split_file(options.filename, int(options.number_of_splits))
