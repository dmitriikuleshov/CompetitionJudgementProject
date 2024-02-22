import unittest
from unittest.mock import patch
from main import main  # Замените 'your_program' и 'your_function' на реальные имена

# Пример CfА
data: list[int] = [6, 5]
data.extend([3, 6, 2, 4, 1, 5])
data.extend([3, 6, 2, 4, 5, 1])
data.extend([3, 6, 5, 2, 1, 4])
data.extend([2, 6, 4, 3, 1, 5])
data.extend([3, 5, 1, 4, 2, 6])


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
