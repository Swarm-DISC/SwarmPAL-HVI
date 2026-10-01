import datetime

def add_common_args(parser):
    '''Add arguments to argpars.ArgumentParser objects that
    should be consistent between scripts.'''

    parser.add_argument("-c", "--collection", default="SW_OPER_MAGB_LR_1B", help="The Swarm data product to download")
    parser.add_argument(
        "-S", "--start-date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
        help="Start date of the period to aggrate [YYYY-MM-DD]",
    )
    parser.add_argument(
        "-E", "--end-date",
        type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
        help="End date of the period to aggrate [YYYY-MM-DD]",
    )
    parser.add_argument(
        "-r", "--resolution",
        type=int,
        default=2,
        help="The H3 resolution that determines spatial bin size",
    )
