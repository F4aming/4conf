import unittest
from unittest.mock import patch, MagicMock
import os


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.input_file = 'test_input.bin'
        self.output_file = 'test_output.csv'
        self.mem_start = 0
        self.mem_end = 10

    @patch('builtins.open', new_callable=MagicMock)
    @patch('os.path.exists', return_value=False)
    def test_execute_invalid_opcode(self, mock_exists, mock_open):
        # Исправляем байтовые данные, чтобы избежать ошибки ValueError
        invalid_binary_data = bytearray([255, 0, 0, 0, 100])  # Теперь используем допустимый байт (255)

        # Мокируем открытие файла
        mock_open.return_value.__enter__.return_value.read = MagicMock(return_value=invalid_binary_data)
        mock_open.return_value.__enter__.return_value.write = MagicMock()

        with patch('builtins.print') as mock_print:
            from interpreter import execute
            execute(invalid_binary_data, (self.mem_start, self.mem_end), self.output_file)

            # Проверяем, что ошибка обработана
            self.assertIn("Неизвестная команда 255 по адресу 0", [call[0][0] for call in mock_print.call_args_list])

            # Проверяем, что файл не был создан
            self.assertFalse(os.path.exists(self.output_file))

    @patch('builtins.open', new_callable=MagicMock)
    @patch('os.path.exists', return_value=False)
    def test_execute_not_enough_data(self, mock_exists, mock_open):
        insufficient_data = bytearray([201, 0, 0])  # Недостаточно данных для команды

        # Мокируем открытие файла
        mock_open.return_value.__enter__.return_value.read = MagicMock(return_value=insufficient_data)
        mock_open.return_value.__enter__.return_value.write = MagicMock()

        with patch('builtins.print') as mock_print:
            from interpreter import execute
            execute(insufficient_data, (self.mem_start, self.mem_end), self.output_file)

            # Проверяем, что ошибка обработана
            self.assertIn("Ошибка: недостаточно данных для команды LOAD_CONST по адресу 0", 
                          [call[0][0] for call in mock_print.call_args_list])

            # Проверяем, что файл не был создан
            self.assertFalse(os.path.exists(self.output_file))

    @patch('builtins.open', new_callable=MagicMock)
    @patch('os.path.exists', return_value=False)
    def test_execute_empty_data(self, mock_exists, mock_open):
        empty_binary_data = bytearray()

        # Мокируем открытие файла
        mock_open.return_value.__enter__.return_value.read = MagicMock(return_value=empty_binary_data)
        mock_open.return_value.__enter__.return_value.write = MagicMock()

        with patch('builtins.print') as mock_print:
            from interpreter import execute
            execute(empty_binary_data, (self.mem_start, self.mem_end), self.output_file)

            # Проверяем, что ничего не было выведено
            self.assertEqual(mock_print.call_count, 0)

            # Проверяем, что файл не был создан
            self.assertFalse(os.path.exists(self.output_file))

if __name__ == '__main__':
    unittest.main()
