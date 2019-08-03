import sys
import galaxest
import runner
import args_parser
version = galaxest.__version__

def main():
    print("galaxest, version %s" % (version))
    parser, options, arguments = args_parser.parse_options()
    runner.options = options
    runner.run()
    sys.exit(0)

if __name__ == '__main__':
    main()
