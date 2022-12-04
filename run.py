import datetime
import logging
import traceback

import data_processing


def main():
    try:
        data_processing.DataProcessing().data_transfor_dataframe()
    except Exception as e:
        traceback.print_exc()
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        log_name = 'error_log' + now + '.txt'
        logging.basicConfig(filename=log_name, level=logging.DEBUG, filemode='w',
                            format='[%(asctime)s] [%(levelname)s] >>> %(message)s', datefmt='%Y-%m-%d %I:%M:%S')
        logging.error("main program error:")
        logging.error(e)
        logging.error(traceback.format_exc())


if __name__ == '__main__':
    main()