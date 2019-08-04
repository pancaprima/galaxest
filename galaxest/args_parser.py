from optparse import OptionParser
from parallel import ParallelType
import locale.en as locale
import sys

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
    opts = _check_conflicted_opts(opts)
    return parser, opts, args

def _check_conflicted_opts(opts) :
    conflict = False

    if opts.want_connect != False and opts.want_disconnect != False :
        print locale.ERROR_CD_TOGETHER
        conflict = True

    if opts.want_disconnect is None and opts.local_id is None :
        print locale.ERROR_DISCONNECT_NO_ID
        conflict = True
    
    parallel_request = 0
    opts.parallel_type = None
    opts.parallel_specs = None
    if not opts.parallel_number is None :
        parallel_request += 1
        opts.parallel_type = ParallelType.AMOUNT
        opts.parallel_specs = opts.parallel_number
    if not opts.parallel_os is None :
        parallel_request += 1
        opts.parallel_type = ParallelType.OS
        opts.parallel_specs = opts.parallel_os
    
    if parallel_request > 1 :
        print locale.ERROR_CHOOSE_PARALLEL_TYPE
        conflict = True
    
    if conflict :
        sys.exit(0)

    return opts