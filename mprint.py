import sys
from abc import ABC, abstractmethod


class ToStr(ABC):
    def __init__(self, data, main_indent, second_indent):
        self._data = data
        self._main_indent = main_indent
        self._second_indent = second_indent

    @abstractmethod
    def execute(self) -> str:
        pass


class ListToStr(ToStr):
    def execute(self) -> str:
        indent_space = " " * (self._second_indent - self._main_indent)

        output_str = f"{indent_space}[\n"
        for item in self._data:
            output_str += get_styled_text(item, self._main_indent, self._second_indent + self._main_indent)
            if item != self._data[-1]:
                output_str += ","
            output_str += "\n"
        output_str += f"{indent_space}]"

        return output_str


class AnotherToStr(ToStr):
    def execute(self) -> str:
        indent_space = " " * (self._second_indent - self._main_indent)
        return indent_space + str(self._data)


def get_styled_text(text, indent, second_indent=None):
    if second_indent is None:
        second_indent = indent
    datatypes = {
        list: ListToStr,
    }
    return datatypes.get(type(text), AnotherToStr)(text, indent, second_indent).execute()


def mprint(text, sep=" ", end="\n", indent=4, file=sys.stdout):
    file.write(get_styled_text(text, indent) + end)

mprint([1,2,3,4,[15,12]])