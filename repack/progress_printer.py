from __future__ import annotations

import math


class PrinterTick:

    def __init__(self, printer: Printer, message: str):
        self._printer = printer
        self._message = message

    def __enter__(self):
        self._printer.tick_start(self._message)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._printer.tick_end()


class Printer:

    """
    Assists in the process writing to the console/terminal a progress bar with an associated message.
    """

    _COMPLETE_TICK_CHAR = '█'
    _INCOMPLETE_TICK_CHAR = '░'
    _PROGRESS_TICKS = 30

    def __init__(self, max_progress: int, print_blank_on_exit=True):
        self._current_progress = 0
        self._max_progress = max(max_progress, 1)
        self._last_message = ''
        self._print_blank_on_exit = print_blank_on_exit

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and self._print_blank_on_exit:
            self.print_blank_line()

    def progress_tick(self, message: str) -> PrinterTick:
        return PrinterTick(self, message)

    def tick_start(self, message: str):
        self._print_progress_message(message)

    def tick_end(self):
        self._current_progress = self._current_progress + 1
        self._print_progress_message('')

    def print_blank_line(self):
        self._print_progress_message('', True)

    def print_error_message(self, message: str):
        formatted_message = self._pad_string(message)
        self._last_message = message
        print(formatted_message)

    def _print_progress_message(self, message: str, new_line=False):
        progress_bar = self._create_progress_bar()
        formatted_message = self._pad_string(f'{progress_bar} {message}')
        self._last_message = formatted_message
        if new_line:
            print(formatted_message)
        else:
            print(f'{formatted_message}\r', end='')

    def _create_progress_bar(self):
        progress = self._current_progress / self._max_progress
        complete = math.floor(Printer._PROGRESS_TICKS * progress)
        incomplete = Printer._PROGRESS_TICKS - complete
        complete_ticks = Printer._COMPLETE_TICK_CHAR * complete
        incomplete_ticks = Printer._INCOMPLETE_TICK_CHAR * incomplete
        progress = int(progress * 100)
        return f'[{complete_ticks}{incomplete_ticks}] {progress}%'

    def _pad_string(self, message: str) -> str:
        last_length = len(self._last_message)
        next_length = len(message)
        if last_length == next_length or next_length > last_length:
            return message
        padding_length = last_length - next_length
        padding = ' ' * padding_length
        return f'{message}{padding}'
