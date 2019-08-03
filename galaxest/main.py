import sys
import galaxest
import runner
import locale.en as locale
from optparse import OptionParser

version = galaxest.__version__


def parse_options():
    """
    Handle command-line options with optparse.OptionParser.

    Return list of arguments, largely for use in `parse_arguments`.
    """

    # Initialize
    parser = OptionParser(usage="galaxest [options]")

    parser.add_option(
        '-l','--devices',
        action='store_true',
        dest='want_list_devices',
        default=False,
        help=locale.HELP_DEVICES
    )

    parser.add_option(
        '-c','--connect',
        action='store_true',
        dest='want_connect',
        default=False,
        help=locale.HELP_CONNECT
    )

    parser.add_option(
        '-d','--disconnect',
        action='store_true',
        dest='want_disconnect',
        default=False,
        help=locale.HELP_DISCONNECT
    )

    parser.add_option(
        '--device-id',
        dest='device_id',
        default=None,
        help=locale.HELP_DEVICE_ID
    )

    parser.add_option(
        '--local-id',
        dest='local_id',
        default=None,
        help=locale.HELP_LOCAL_ID
    )

    parser.add_option(
        '--reset-config',
        action='store_true',
        dest='want_reset_config',
        default=False,
        help=locale.HELP_RESET_CONFIG
    )

    parser.add_option(
        '-p','--show-config',
        action='store_true',
        dest='want_show_config',
        default=False,
        help=locale.HELP_SHOW_CONFIG
    )

    parser.add_option(
        '-r','--run',
        dest='test_suite',
        default=None,
        help=locale.HELP_RUN
    )

    parser.add_option(
        '--any-device',
        action='store_true',
        dest='any_device',
        default=False,
        help=locale.HELP_ANY_DEVICE
    )

    parser.add_option(
        '-i','--my-devices',
        action='store_true',
        dest='want_my_devices',
        default=False,
        help=locale.HELP_MY_DEVICES
    )

    parser.add_option(
        '-o','--opts',
        dest='opts',
        default=None,
        help=locale.HELP_OPTS
    )

    parser.add_option(
        '--parallel-n',
        dest='parallel_number',
        default=None,
        help=locale.HELP_PARALLEL_N
    )

    parser.add_option(
        '--parallel-os',
        dest='parallel_os',
        default=None,
        help=locale.HELP_PARALLEL_OS
    )

    # Finalize
    # Return three-tuple of parser + the output from parse_args (opt obj, args)
    opts, args = parser.parse_args()
    return parser, opts, args

def main():
    print("galaxest, version %s" % (version))
    parser, options, arguments = parse_options()
    runner.options = options
    runner.run()
    sys.exit(0)


if __name__ == '__main__':
    main()
