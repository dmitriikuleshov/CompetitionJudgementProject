import unittest
from unittest.mock import patch
from main import main  # Замените 'your_program' и 'your_function' на реальные имена

# Таблица 4
data: list[int] = [6, 5]
data.extend([4, 5, 6, 1, 2, 3])
data.extend([6, 5, 1, 4, 2, 3])
data.extend([6, 1, 3, 2, 5, 4])
data.extend([6, 1, 3, 2, 5, 4])
data.extend([6, 1, 4, 5, 2, 3])


class TestYourProgram(unittest.TestCase):

    @patch('builtins.input', side_effect=data)
    def test_keyboard_input(self, mock_input):
        # Вызываем функцию, которую вы хотите протестировать
        try:
            result = main()  # Замените 'your_function' на реальное имя вашей функции
            print(result)
        except Exception as e:
            raise e
        # Проверяем результат выполнения функции
        # self.assertEqual(result, ...)  # Замените 'expected_result' на ожидаемый результат


if __name__ == '__main__':
    unittest.main()
