import sys
from abc import ABC, abstractmethod


class ToStr(ABC):
    def __init__(self, data, indent, text_level=0):
        self._data = data
        self._indent = indent
        self._text_level = text_level

    @abstractmethod
    def execute(self) -> str:
        pass

    @property
    def indent_space(self):
        return " " * (self._indent * self._text_level)

    def indenter(self, data: list, open_icon: str, close_icon: str) -> str:
        output_str = f"{self.indent_space}{open_icon}\n"

        for item in data:
            output_str += get_styled_text(item, self._indent, self._text_level + 1)
            if item != data[-1]:
                output_str += ","
            output_str += "\n"

        output_str += f"{self.indent_space}{close_icon}"

        return output_str

class ListToStr(ToStr):
    def execute(self) -> str:
        return self.indenter(self._data, "[", "]")


class DictToStr(ToStr):
    def execute(self) -> str:
        return self.indenter(self._data, "{", "}")

    def indenter(self, data: dict, open_icon: str, close_icon: str) -> str:
        output_str = f"{self.indent_space}{open_icon}\n"

        for key, value in data.items():
            output_str += get_styled_text(key, self._indent, self._text_level + 1)
            output_str += ":\n"
            output_str += get_styled_text(value, self._indent, self._text_level + 2)
            if key != list(data.keys())[-1]:
                output_str += ","
            output_str += "\n"

        output_str += f"{self.indent_space}{close_icon}"

        return output_str

class SetToStr(ToStr):
    def execute(self) -> str:
        return self.indenter(list(self._data), "{", "}")


class AnotherToStr(ToStr):
    def execute(self) -> str:
        return f"{self.indent_space}{self._data}"


def get_styled_text(text, indent, text_level=0):
    datatypes = {
        list: ListToStr,
        dict: DictToStr,
        set: SetToStr,
    }
    return datatypes.get(type(text), AnotherToStr)(text, indent, text_level).execute()


def mprint(*text, sep=", ", end="\n", indent=4, file=sys.stdout):
    out_put = ""
    for item in text:
        out_put += get_styled_text(item, indent)
        if item != text[-1]:
            out_put += sep
    file.write(out_put + end)
