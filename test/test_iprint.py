from unittest import TestCase
from iprint.iprint import iprint, get_styled_text
import functools
import textwrap


class TestMPrint(TestCase):
    def setUp(self):
        class FileMock:
            content = ""

            def write(self, content: str):
                self.content = content

        self.file_mock = FileMock()
        self.mprint_mock = functools.partial(iprint, file=self.file_mock)

    def test_write_in_file(self):
        self.mprint_mock('hello')
        actual = self.file_mock.content
        expected = 'hello\n'
        self.assertEqual(actual, expected)

    def test_end(self):
        self.mprint_mock('hello ', end="world")
        actual = self.file_mock.content
        expected = 'hello world'
        self.assertEqual(actual, expected)

    def test_multi_input(self):
        self.mprint_mock('hello', "world")
        actual = self.file_mock.content
        expected = 'hello, world\n'
        self.assertEqual(actual, expected)

    def test_sep(self):
        self.mprint_mock('hello', "world", sep=" test ")
        actual = self.file_mock.content
        expected = 'hello test world\n'
        self.assertEqual(actual, expected)


class TestGetStyledText(TestCase):
    def test_simple_string(self):
        actual = get_styled_text('hello', 4)
        expected = 'hello'
        self.assertEqual(actual, expected)

    def test_simple_list(self):
        actual = get_styled_text(['hello'], 4)
        expected = textwrap.dedent("""\
            [
                hello
            ]"""
        )
        self.assertMultiLineEqual(actual, expected)

    def test_simple_list_two_index(self):
        actual = get_styled_text(['hello', 'world'], 4)
        expected = textwrap.dedent("""\
            [
                hello,
                world
            ]"""
        )
        self.assertMultiLineEqual(actual, expected)

    def test_nested_two_dimensional_list(self):
        actual = get_styled_text([["hello"]], 4)
        expected = textwrap.dedent("""\
            [
                [
                    hello
                ]
            ]"""
        )
        self.assertMultiLineEqual(actual, expected)

    def test_nested_three_dimensional_list(self):
        actual = get_styled_text([[["hello"]]], 4)
        expected = textwrap.dedent("""\
            [
                [
                    [
                        hello
                    ]
                ]
            ]"""
        )
        self.assertMultiLineEqual(actual, expected)

    def test_nested_two_dimensional_list_two_index(self):
        actual = get_styled_text([["hello", "world"]], 4)
        expected = textwrap.dedent("""\
            [
                [
                    hello,
                    world
                ]
            ]"""
        )
        self.assertMultiLineEqual(actual, expected)

    def test_two_list_in_a_list(self):
        actual = get_styled_text([["hello", "world"], ["test", "case"]], 4)
        expected = textwrap.dedent("""\
            [
                [
                    hello,
                    world
                ],
                [
                    test,
                    case
                ]
            ]"""
        )
        self.assertMultiLineEqual(actual, expected)

    def test_string_list_in_a_list(self):
        actual = get_styled_text([["hello", "world"], "test"], 4)
        expected = textwrap.dedent("""\
            [
                [
                    hello,
                    world
                ],
                test
            ]"""
        )
        self.assertMultiLineEqual(actual, expected)

    def test_simple_dict(self):
        actual = get_styled_text({"hello": "world"}, 4)
        expected = textwrap.dedent("""\
            {
                hello:
                    world
            }"""
        )
        self.assertMultiLineEqual(actual, expected)

    def test_nested_dict(self):
        actual = get_styled_text({"test": {"hello": "world"}}, 4)
        expected = textwrap.dedent("""\
            {
                test:
                    {
                        hello:
                            world
                    }
            }"""
        )
        self.assertMultiLineEqual(actual, expected)

    def test_list_in_a_dict(self):
        actual = get_styled_text({"hello": ["world"]}, 4)
        expected = textwrap.dedent("""\
            {
                hello:
                    [
                        world
                    ]
            }"""
        )
        self.assertMultiLineEqual(actual, expected)

    def test_simple_set(self):
        actual = get_styled_text({"hello", "world"}, 4)
        expected = [
            textwrap.dedent("""\
                {
                    hello,
                    world
                }"""
            ),
            textwrap.dedent("""\
                {
                    world,
                    hello
                }"""
            )
        ]
        self.assertIn(actual, expected)
