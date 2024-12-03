import os
import struct
import csv
import tempfile
import unittest

# Импортируем функцию assemble из assembler.py
from assembler import assemble

class TestAssembler(unittest.TestCase):
    def setUp(self):
        # Создание временных файлов
        self.input_file = tempfile.NamedTemporaryFile(delete=False)
        self.output_file = tempfile.NamedTemporaryFile(delete=False)
        self.log_file = tempfile.NamedTemporaryFile(delete=False)

    def tearDown(self):
        # Удаление временных файлов
        try:
            os.unlink(self.input_file.name)
            os.unlink(self.output_file.name)
            os.unlink(self.log_file.name)
        except OSError:
            pass

    def write_input(self, content):
        with open(self.input_file.name, 'w') as f:
            f.write(content)

    def test_assemble_load_const(self):
        self.write_input("LOAD_CONST 1 100\n")
        assemble(self.input_file.name, self.output_file.name, self.log_file.name)
        
        # Проверка бинарного файла
        with open(self.output_file.name, 'rb') as f:
            data = f.read()
            expected_binary = struct.pack('<BHI', 201, 1, 100)
            self.assertEqual(data, expected_binary)

        # Проверка файла лога
        with open(self.log_file.name, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertEqual(rows[1], ['LOAD_CONST', '1', '100', ''])

    def test_assemble_load_mem(self):
        self.write_input("LOAD_MEM 2 3\n")
        assemble(self.input_file.name, self.output_file.name, self.log_file.name)
        
        with open(self.output_file.name, 'rb') as f:
            data = f.read()
            expected_binary = struct.pack('<BHH', 57, 2, 3)
            self.assertEqual(data, expected_binary)

        with open(self.log_file.name, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertEqual(rows[1], ['LOAD_MEM', '2', '3', ''])

    def test_assemble_invalid_command(self):
        self.write_input("INVALID_CMD 1 2\n")
        assemble(self.input_file.name, self.output_file.name, self.log_file.name)
        
        with open(self.output_file.name, 'rb') as f:
            data = f.read()
            self.assertEqual(data, b'')

        with open(self.log_file.name, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 1)  # Только заголовок

if __name__ == '__main__':
    unittest.main()
