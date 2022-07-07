import argparse
from Loader import Loader


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar='PATH',
                    help='path to the video', required=True)

parser.add_argument('-s', '--scale', metavar='NUM', type=float, default=1,
                    help='proportion of scaling (default = 1)')

args = vars(parser.parse_args())


loader = Loader(args['input'], args['scale'])
loader.run()
