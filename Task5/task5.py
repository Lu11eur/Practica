import sys
import datetime

# Абстрактний форматтер
class Formatter:
    def format(self, message):
        raise NotImplementedError("Must implement format method")

# Форматтер з міткою часу
class TimeFormatter(Formatter):
    def __init__(self, fmt="%Y-%m-%d %H:%M:%S"):
        self.fmt = fmt

    def format(self, message):
        now = datetime.datetime.now().strftime(self.fmt)
        return f"[{now}] {message}"

# Абстрактний хендлер
class Handler:
    def handle(self, formatted_message):
        raise NotImplementedError("Must implement handle method")

# Вивід у потік (stderr за замовчуванням)
class StreamHandler(Handler):
    def __init__(self, stream=sys.stderr):
        self.stream = stream

    def handle(self, formatted_message):
        print(formatted_message, file=self.stream)

# Основний логгер
class Logger:
    def __init__(self, formatter: Formatter):
        self.formatter = formatter
        self.handlers = []

    def add_handler(self, handler: Handler):
        self.handlers.append(handler)

    def log(self, message):
        formatted = self.formatter.format(message)
        for handler in self.handlers:
            handler.handle(formatted)

# Точка входу
def main():
    formatter = TimeFormatter("%Y-%m-%d %H:%M:%S")
    logger = Logger(formatter)
    stderr_handler = StreamHandler(sys.stderr)
    logger.add_handler(stderr_handler)

    logger.log("message for logging")
    logger.log("another message")

if __name__ == "__main__":
    main()
