import sys
from abc import ABC
import time


class BaseTest(ABC):
    test_description = ''
    file_name = ''
    start_time: float
    end_time: float
    execution_time: float
    run_error = False

    def __init__(self):
        self.header()
        self.run()
        if not self.run_error:
            self.footer()

    def header(self):
        print(f'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'
              f'Running test file "{self.file_name}"\n'
              f'Test description: "{self.test_description}"')
        self.start_time = time.time()

    def run(self):
        pass

    def error(self, exception: Exception):
        self.end_time = time.time()
        self.run_error = True
        exc_type, exc_obj, exc_tb = sys.exc_info()
        self.execution_time = self.end_time - self.start_time
        print(f'Error of test file "{self.file_name}"'
              f' after {self.execution_time} secs of execution'
              f' at line {exc_tb.tb_lineno}.\n'
              f'[ERROR]: {exception}\n'
              f'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')

    def footer(self):
        self.end_time = time.time()
        self.execution_time = self.end_time - self.start_time
        print(f'Ended run of test file "{self.file_name}" in {self.execution_time} secs.\n'
              f'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
