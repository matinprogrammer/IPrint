from abc import ABC, abstractmethod


class Color(ABC):
    @abstractmethod
    def get_color_code(self):
        pass


class CBlack(Color):
    def get_color_code(self):
        return "\033[1;30m"


class CRed(Color):
    def get_color_code(self):
        return "\033[1;31m"


class CGreen(Color):
    def get_color_code(self):
        return "\033[1;32m"


class CBlue(Color):
    def get_color_code(self):
        return "\033[1;34m"


class CMagenta(Color):
    def get_color_code(self):
        return "\033[1;35m"


class CCyan(Color):
    def get_color_code(self):
        return "\033[1;36m"


class CWhite(Color):
    def get_color_code(self):
        return "\033[1;37m"


class COrange(Color):
    def get_color_code(self):
        return "\033[1;33m"


class CDefault(Color):
    def get_color_code(self):
        return "\033[0m"


class ColorError(Exception):
    pass


def get_colored_message(message: str, color: Color, clear_color: Color = CDefault()):
    if not isinstance(color, Color) or not isinstance(clear_color, Color):
        raise ColorError("invalid color or clear color (need to be Color class like 'CWhite')")
    return f"{color.get_color_code()}{message}{clear_color.get_color_code()}"

