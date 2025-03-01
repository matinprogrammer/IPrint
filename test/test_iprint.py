from unittest import TestCase
from iprint.iprint import iprint, get_styled_text, status_print
import functools
import textwrap
import re


class TestIPrint(TestCase):
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

    def test_multi_line_text(self):
        actual = get_styled_text(["""line_1\nline_2"""], 4)
        expected = textwrap.dedent("""\
            [
                line_1
                line_2
            ]"""
        )
        self.assertIn(actual, expected)


class TestStatusPrint(TestCase):
    def setUp(self):
        class FileMock:
            content = ""

            def write(self, content: str):
                self.content = content

        self.file_mock = FileMock()
        self.status_print_mock = functools.partial(status_print, file=self.file_mock)

    def test_document(self):
        class Data:
            """this is a document"""

        self.status_print_mock(Data())
        actual = self.file_mock.content
        expected = textwrap.indent(textwrap.dedent("""\
            document:
                this is a document,"""
        ), ' ' * 4)
        self.assertIn(expected, actual)

    def test_instance_variable(self):
        class Data:
            def __init__(self, data):
                self.instance_variable = data

        self.status_print_mock(Data("instance_variable_value"))
        actual = self.file_mock.content
        expected = textwrap.indent(textwrap.dedent("""\
            instance_variables:
                {
                    instance_variable:
                        instance_variable_value
                },"""
        ), ' ' * 4)
        self.assertIn(expected, actual)

    def test_class_variable(self):
        class Data:
            class_variable = "class_variable_value"

        self.status_print_mock(Data())
        actual = self.file_mock.content
        expected = textwrap.indent(textwrap.dedent("""\
            class_variables:
                {
                    class_variable:
                        class_variable_value
                },"""
        ), ' ' * 4)
        self.assertIn(expected, actual)

    def test_methods(self):
        class Data:
            def instance_method(self):
                pass

        self.status_print_mock(Data())
        actual = self.get_normalize_memory_address(self.file_mock.content)
        expected = textwrap.indent(textwrap.dedent("""\
            methods:
                {
                    instance_method:
                        <function TestStatusPrint.test_methods.<locals>.Data.instance_method at <MEMORY_ADDRESS>>
                },"""
        ), ' ' * 4)

        self.assertIn(expected, actual)

    def test_class_method(self):
        class Data:
            @classmethod
            def class_method(cls):
                pass

        self.status_print_mock(Data())
        actual = self.get_normalize_memory_address(self.file_mock.content)
        expected = textwrap.indent(textwrap.dedent("""\
            class_methods:
                {
                    class_method:
                        <classmethod(<function TestStatusPrint.test_class_method.<locals>.Data.class_method at <MEMORY_ADDRESS>>)>
                },"""
        ), ' ' * 4)
        self.assertIn(expected, actual)

    def test_static_method(self):
        class Data:
            @staticmethod
            def static_method():
                pass

        self.status_print_mock(Data())
        actual = self.get_normalize_memory_address(self.file_mock.content)
        expected = textwrap.indent(textwrap.dedent("""\
            static_methods:
                {
                    static_method:
                        <staticmethod(<function TestStatusPrint.test_static_method.<locals>.Data.static_method at <MEMORY_ADDRESS>>)>
                },"""
        ), ' ' * 4)
        self.assertIn(expected, actual)

    def test_property(self):
        class Data:
            @property
            def property_variable(self):
                return "property_variable_value"

        self.status_print_mock(Data())
        actual = self.get_normalize_memory_address(self.file_mock.content)
        expected = textwrap.indent(textwrap.dedent("""\
            properties:
                {
                    property_variable:
                        <property object at <MEMORY_ADDRESS>>
                },"""
        ), ' ' * 4)
        self.assertIn(expected, actual)
    @staticmethod
    def get_normalize_memory_address(actual):
        return re.sub(r'at 0x[0-9a-fA-F]+', 'at <MEMORY_ADDRESS>', actual)
