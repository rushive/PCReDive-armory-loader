import argparse
from Loader import Loader


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', metavar='PATH',
                        help='path to the video', required=True)

    parser.add_argument('-s', '--scale', metavar='NUM', type=float, default=1,
                        help='proportion of scaling (default = 1)')

    parser.add_argument('-q', '--quiet', action='store_true',
                        help='hide window when processing')

    args = vars(parser.parse_args())


    loader = Loader(args['input'], args['scale'], args['quiet'])
    loader.run()
