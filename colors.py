#pylint: disable=line-too-long

"""
Color class for handling colors in different formats (hex, rgb, rgba, hsl, hsla)
"""

import re
class Color:
    """
    Color class for handling colors in different formats (hex, rgb, rgba, hsl, hsla)
    """
    def __init__(self, r : int, g : int, b : int, a : int = 255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    @staticmethod
    def from_hex(hexa : str):
        """Converts a hex color string to a Color object
        Args:
            hexa (str): The hex color string (e.g. #ff0000, #f00, #ff0000ff, #f00f)
            
        Returns:
            Color: The Color object
        """
        if hexa[0] == "#":
            hexa = hexa[1:]

        r, g, b, a = 0, 0, 0, 255

        if len(hexa) == 3: #RGB
            r = int(hexa[0] * 2, 16)
            g = int(hexa[1] * 2, 16)
            b = int(hexa[2] * 2, 16)
        elif len(hexa) == 4: #RGBA
            r = int(hexa[0] * 2, 16)
            g = int(hexa[1] * 2, 16)
            b = int(hexa[2] * 2, 16)
            a = int(hexa[3] * 2, 16)
        elif len(hexa) == 6: #RRGGBB
            r = int(hexa[:2], 16)
            g = int(hexa[2:4], 16)
            b = int(hexa[4:6], 16)
        elif len(hexa) == 8: #RRGGBBAA
            r = int(hexa[:2], 16)
            g = int(hexa[2:4], 16)
            b = int(hexa[4:6], 16)
            a = int(hexa[6:8], 16)
        else:
            raise ValueError(f"Invalid hex color: {hexa}")
        return Color(r, g, b, a)

    @staticmethod
    def from_rgb(rgb : str): # r,g,b,a or r,g,b
        """Converts a rgb color string to a Color object
        Args:
            rgb (str): The rgb color string (e.g. 255,0,0,255, 255,0,0)
            
        Returns:
            Color: The Color object
        """
        if rgb.count(",") == 3: #r,g,b,a
            r, g, b, a = rgb.split(",")
            a = int(a.strip())
        elif rgb.count(",") == 2: #r,g,b
            r, g, b = rgb.split(",")
            a = 255
        else:
            raise ValueError(f"Invalid rgb color: {rgb}")
        r = int(r.strip())
        g = int(g.strip())
        b = int(b.strip())
        if r < 0 or r > 255 or g < 0 or g > 255 or b < 0 or b > 255:
            raise ValueError(f"Invalid rgb color: {rgb}")
        if a < 0 or a > 255:
            raise ValueError(f"Invalid alpha value: {a}")
        return Color(r, g, b, a)


    @staticmethod
    def from_auto(color : str) -> "Color":
        """Converts a color string to a Color object, support hex, rgb and hsl formats (with or without alpha channel)

        Args:
            color (str): The color string

        Raises:
            ValueError: If the color string is invalid

        Returns:
            Color: The Color object
        """
        if re.match(r"^#[0-9a-fA-F]{3,8}$", color):
            return Color.from_hex(color)
        if color.startswith("rgba") or color.startswith("RGBA"):
            return Color.from_rgb(color[5:-1])
        if color.startswith("rgb") or color.startswith("RGB"):
            return Color.from_rgb(color[4:-1])
        if re.match(r"^\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(,\s*\d+\s*)?$", color):
            return Color.from_rgb(color)
        raise ValueError(f"Invalid color: {color}")


    def __str__(self):
        return f"rgba({self.r}, {self.g}, {self.b}, {self.a})"

    def opposite(self) -> "Color":
        """Returns the opposite color of the current color
        Returns:
            Color: The opposite color
        """
        return Color(255 - self.r, 255 - self.g, 255 - self.b, self.a)

    def grayshade(self) -> "Color":
        """Returns the grayscale version of the current color
        Returns:
            Color: The grayscale color
        """
        gray = round(0.299 * self.r + 0.587 * self.g + 0.114 * self.b)
        return Color(gray, gray, gray, self.a)

    def black_or_white(self) -> "Color":
        """Returns black or white depending on the brightness of the color
        Returns:
            Color: The black or white color
        """
        if self.r < 200 \
        or self.g < 200 \
        or self.b < 55:
            return Color(0, 0, 0, self.a)
        return Color(255, 255, 255, self.a)

    def rgb_hex(self):
        """Returns the hex color string of the current color
        Returns:
            str: The hex color string
        """
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def rgba_hex(self):
        """Returns the hex color string of the current color with alpha channel
        Returns:
            str: The hex color string with alpha channel
        """
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}{self.a:02x}"

    def rgb(self):
        """Returns the rgb color string of the current color
        Returns:
            str: The rgb color string
        """
        return f"rgb({self.r}, {self.g}, {self.b})"

    def rgba(self):
        """Returns the rgba color string of the current color
        Returns:
            str: The rgba color string
        """
        return f"rgba({self.r}, {self.g}, {self.b}, {self.a})"


    def __eq__(self, other : object) -> bool:
        if not isinstance(other, Color):
            return NotImplemented
        return self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a

    def __ne__(self, other : object) -> bool:
        if not isinstance(other, Color):
            return NotImplemented
        return not self.__eq__(other)

    def __add__(self, other : object) -> "Color":
        if not isinstance(other, Color):
            return NotImplemented
        r = max(0, min(255, self.r + other.r))
        g = max(0, min(255, self.g + other.g))
        b = max(0, min(255, self.b + other.b))
        a = max(0, min(255, self.a + other.a))
        return Color(r, g, b, a)

    def __sub__(self, other : object) -> "Color":
        if not isinstance(other, Color):
            return NotImplemented
        r = max(0, min(255, self.r - other.r))
        g = max(0, min(255, self.g - other.g))
        b = max(0, min(255, self.b - other.b))
        a = max(0, min(255, self.a - other.a))
        return Color(r, g, b, a)

    def __repr__(self):
        return f"\033[38;2;{self.r};{self.g};{self.b}mColor({self.r} {self.g} {self.b} {self.a})\033[0m"

    def __hash__(self):
        return hash((self.r, self.g, self.b, self.a))
