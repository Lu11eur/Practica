import sys
from logger import Logger

def main():
    out_stream = sys.stderr
    time_formatter = "%Y-%m-%d %H:%M:%S"
    logger = Logger(out_stream, time_formatter)
    logger.log("message for logging")
    logger.log("another message")

if __name__ == "__main__":
    main()
