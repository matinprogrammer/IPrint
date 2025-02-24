from unittest import TestCase
from mprint import mprint, get_styled_text
from functools import partial


class TestMPrint(TestCase):
    def test_write_in_file(self):
        class FileMock:
            content = ""

            def write(self, content: str):
                self.content = content

        file_mock = FileMock()
        mprint_mock = partial(mprint, file=file_mock)

        mprint_mock('hello')
        actual = file_mock.content
        expected = 'hello\n'
        self.assertEqual(actual, expected)

    def test_simple_string(self):
        actual = get_styled_text('hello', 4)
        expected = 'hello'
        self.assertEqual(actual, expected)

    def test_simple_list(self):
        indent_space = " " * 4
        actual = get_styled_text(['hello'], 4)
        expected = (
            f"[\n"
            f"{indent_space}hello\n"
            f"]"
        )
        self.assertEqual(actual, expected)

    def test_simple_list_two_index(self):
        indent_space = " " * 4

        actual = get_styled_text(['hello', 'world'], 4)
        expected = (
            f"[\n"
            f"{indent_space}hello,\n"
            f"{indent_space}world\n"
            f"]"
        )
        self.assertEqual(actual, expected)

    def test_nested_two_dimensional_list(self):
        indent_space = " " * 4

        actual = get_styled_text([["hello"]], 4)
        expected = (
            f"[\n"
            f"{indent_space}[\n"
            f"{indent_space * 2}hello\n"
            f"{indent_space}]\n"
            f"]"
        )
        self.assertEqual(actual, expected)

    def test_nested_three_dimensional_list(self):
        indent_space = " " * 4

        actual = get_styled_text([[["hello"]]], 4)
        expected = (
            f"[\n"
            f"{indent_space}[\n"
            f"{indent_space * 2}[\n"
            f"{indent_space * 3}hello\n"
            f"{indent_space * 2}]\n"
            f"{indent_space}]\n"
            f"]"
        )
        self.assertEqual(actual, expected)

    def test_nested_two_dimensional_list_two_index(self):
        indent_space = " " * 4

        actual = get_styled_text([["hello", "world"]], 4)
        expected = (
            f"[\n"
            f"{indent_space}[\n"
            f"{indent_space * 2}hello,\n"
            f"{indent_space * 2}world\n"
            f"{indent_space}]\n"
            f"]"
        )
        self.assertEqual(actual, expected)

    def test_two_list_in_a_list(self):
        indent_space = " " * 4

        actual = get_styled_text([["hello", "world"], ["test", "case"]], 4)
        expected = (
            f"[\n"
            f"{indent_space}[\n"
            f"{indent_space * 2}hello,\n"
            f"{indent_space * 2}world\n"
            f"{indent_space}],\n"
            f"{indent_space}[\n"
            f"{indent_space * 2}test,\n"
            f"{indent_space * 2}case\n"
            f"{indent_space}]\n"
            f"]"
        )
        self.assertEqual(actual, expected)

    def test_string_list_in_a_list(self):
        indent_space = " " * 4

        actual = get_styled_text([["hello", "world"], "test"], 4)
        expected = (
            f"[\n"
            f"{indent_space}[\n"
            f"{indent_space * 2}hello,\n"
            f"{indent_space * 2}world\n"
            f"{indent_space}],\n"
            f"{indent_space}test\n"
            f"]"
        )
        self.assertEqual(actual, expected)
