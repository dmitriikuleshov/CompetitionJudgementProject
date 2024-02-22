import unittest
from unittest.mock import patch
from main import main  # Замените 'your_program' и 'your_function' на реальные имена

# Пример Е
data: list[int] = [6, 5]
data.extend([1, 2, 5, 3, 4, 6])
data.extend([1, 2, 5, 3, 4, 6])
data.extend([1, 5, 2, 4, 3, 6])
data.extend([5, 1, 2, 6, 3, 4])
data.extend([5, 4, 2, 1, 3, 6])


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
