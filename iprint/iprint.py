import sys
import inspect
from abc import ABC, abstractmethod
from tools.colored_text import get_colored_message, CBlue, CMagenta, CGreen, CCyan, COrange, CBlack


list_color = CMagenta()
dict_color = CBlue()
set_color = CCyan()
str_color = CGreen()
int_color = COrange()
another_color = CBlack()


class ToStr(ABC):
    def __init__(self, data, indent, text_level=0, colorize=False):
        self._data = data
        self._indent = indent
        self._text_level = text_level
        self._colorize = colorize

    @abstractmethod
    def execute(self) -> str:
        pass

    @property
    def indent_space(self):
        return " " * (self._indent * self._text_level)

    def indenter(self, data: list, open_icon: str, close_icon: str) -> str:
        output_str = f"{self.indent_space}{open_icon}\n"

        for item in data:
            output_str += get_styled_text(item, self._indent, self._text_level + 1, self._colorize)
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
            output_str += get_styled_text(key, self._indent, self._text_level + 1, self._colorize)
            output_str += ":\n"
            output_str += get_styled_text(value, self._indent, self._text_level + 2, self._colorize)
            if key != list(data.keys())[-1]:
                output_str += ","
            output_str += "\n"

        output_str += f"{self.indent_space}{close_icon}"

        return output_str


class SetToStr(ToStr):
    def execute(self) -> str:
        return self.indenter(list(self._data), "{", "}")


class IntToStr(ToStr):
    def execute(self) -> str:
        return f"{self.indent_space}{str(self._data)}"


class StringToStr(ToStr):
    def get_output_text(self):
        new_data = self._data.replace("\n", f"\n{self.indent_space}")
        return f"{self.indent_space}{new_data}"

    def execute(self) -> str:
        return self.get_output_text()


class AnotherToStr(ToStr):
    def execute(self) -> str:
        return f"{self.indent_space}{str(self._data)}"


class ColorListToStr(ListToStr):
    def execute(self) -> str:
        open_icon = get_colored_message("[", list_color)
        close_icon = get_colored_message("]", list_color)
        return self.indenter(self._data, open_icon, close_icon)


class ColorDictToStr(DictToStr):
    def execute(self) -> str:
        open_icon = get_colored_message("{", dict_color)
        close_icon = get_colored_message("}", dict_color)
        return self.indenter(self._data, open_icon, close_icon)


class ColorSetToStr(SetToStr):
    def execute(self) -> str:
        open_icon = get_colored_message("{", set_color)
        close_icon = get_colored_message("}", set_color)
        return self.indenter(list(self._data), open_icon, close_icon)


class ColorIntToStr(IntToStr):
    def execute(self) -> str:
        return f"{self.indent_space}{get_colored_message(str(self._data), int_color)}"


class ColorStringToStr(StringToStr):
    def execute(self) -> str:
        return get_colored_message(self.get_output_text(), str_color)


class ColorAnotherToStr(AnotherToStr):
    def execute(self) -> str:
        return f"{self.indent_space}{get_colored_message(str(self._data), another_color)}"


def get_styled_text(text, indent, text_level=0, colorize=False):
    if colorize:
        datatypes = {
            list: ColorListToStr,
            dict: ColorDictToStr,
            set: ColorSetToStr,
            str: ColorStringToStr,
            int: ColorIntToStr,
        }
        default = ColorAnotherToStr
    else:
        datatypes = {
            list: ListToStr,
            dict: DictToStr,
            set: SetToStr,
            str: StringToStr,
            int: IntToStr,
        }
        default = AnotherToStr

    return datatypes.get(type(text), default)(text, indent, text_level, colorize).execute()


def iprint(*text, sep=", ", end="\n", indent=4, file=sys.stdout):
    out_put = ""
    for item in text:
        out_put += get_styled_text(item, indent)
        if item != text[-1]:
            out_put += sep
    file.write(out_put + end)


def cprint(*text, sep=" ", end="\n", indent=4):
    out_put = ""
    for item in text:
        out_put += get_styled_text(item, indent, colorize=True)
        if item != text[-1]:
            out_put += sep
    sys.stdout.write(out_put + end)


def status_print(instance, *, end="\n", indent=4, file=sys.stdout, colorize=False, show_dunder_attr=False):
    document = instance.__doc__
    size = instance.__sizeof__()
    try:
        instance_variables = dict(instance.__dict__)
    except AttributeError:
        instance_variables = {}

    class_variables = {}
    methods = {}
    class_methods = {}
    static_methods = {}
    properties = {}
    other_members = {}

    for name, attr in vars(instance.__class__).items():
        if isinstance(attr, staticmethod):
            static_methods[name] = attr
        elif isinstance(attr, classmethod):
            class_methods[name] = attr
        elif isinstance(attr, property):
            properties[name] = attr
        elif not name.startswith('__') and not name.endswith('__'):
            if inspect.ismethod(attr) or inspect.isfunction(attr) or inspect.ismethoddescriptor(attr):
                methods[name] = attr
            else:
                class_variables[name] = attr
        else:
            if name != "__doc__":
                other_members[name] = attr

    data = {
        "document": document,
        "size": size,
        "instance_variables": instance_variables,
        "class_variables": class_variables,
        "methods": methods,
        "class_methods": class_methods,
        "static_methods": static_methods,
        "properties": properties,
        "other_members": other_members if show_dunder_attr else "'off'",
    }

    if colorize:
        if file != sys.stdout:
            raise RuntimeError("can't write colorized in file")
        cprint(data, end=end, indent=indent)
    else:
        iprint(data, end=end, indent=indent, file=file)


if __name__ == "__main__":
    # Example:
    class AnotherData:
        """document of test class"""
        class_variable = "class_variable_value"

        def __init__(self, data):
            self.instance_variable = data

        def instance_method(self):
            pass

        @classmethod
        def class_method(cls):
            pass

        @staticmethod
        def static_method():
            pass

        @property
        def property_variable(self):
            return "property_variable_value"


    string_data = "my name is matin"
    int_data = 20
    another_data = AnotherData("instance_variable_value")
    dict_data = {"auther": "matin ahmadi", "github": "https://github.com/matinprogrammer"}
    set_data = {1, 2, 3}
    list_data = [string_data, int_data, another_data, dict_data, set_data, [[["test list"]]]]

    print("result of mprint: ")
    iprint(list_data)

    print("\nresult of cprint: ")
    cprint(list_data)

    print("\nresult of status_print: ")
    status_print(another_data, show_dunder_attr=True, colorize=True)
