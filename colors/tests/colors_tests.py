import pytest
from colors.colors import Color

@pytest.mark.parametrize(
    "hexa, expected, test_id",
    [
        ("#fff", Color(255, 255, 255), "hex_3_rgb_white"),
        ("#000", Color(0, 0, 0), "hex_3_rgb_black"),
        ("#f00", Color(255, 0, 0), "hex_3_rgb_red"),
        ("#ffff", Color(255, 255, 255, 255), "hex_4_rgba_white"),
        ("#000f", Color(0, 0, 0, 255), "hex_4_rgba_black"),
        ("#f00f", Color(255, 0, 0, 255), "hex_4_rgba_red"),
        ("#ff0000", Color(255, 0, 0), "hex_6_rrggbb_red"),
        ("#00ff00", Color(0, 255, 0), "hex_6_rrggbb_green"),
        ("#0000ff", Color(0, 0, 255), "hex_6_rrggbb_blue"),
        ("#ff0000ff", Color(255, 0, 0, 255), "hex_8_rrggbbaa_red"),
        ("#00ff00ff", Color(0, 255, 0, 255), "hex_8_rrggbbaa_green"),
        ("#0000ffff", Color(0, 0, 255, 255), "hex_8_rrggbbaa_blue"),
        ("fff", Color(255, 255, 255), "hex_3_rgb_white_nohash"),
        ("ff0000", Color(255, 0, 0), "hex_6_rrggbb_red_nohash"),
    ],
    ids=lambda p: p if isinstance(p, str) else None
)
def test_from_hex_happy(hexa, expected, test_id):
    # Act

    result = Color.from_hex(hexa)

    # Assert

    assert result == expected

@pytest.mark.parametrize(
    "hexa, error, test_id",
    [
        ("#ff", ValueError, "hex_too_short"),
        ("#ff000", ValueError, "hex_5_invalid"),
        ("#ff00000", ValueError, "hex_7_invalid"),
        ("#ff0000000", ValueError, "hex_9_invalid"),
        ("#ggg", ValueError, "hex_invalid_chars"),
        ("", ValueError, "hex_empty"),
    ],
    ids=["hex_too_short", "hex_5_invalid", "hex_7_invalid", "hex_9_invalid", "hex_invalid_chars", "hex_empty"]
)
def test_from_hex_errors(hexa, error, test_id):
    # Act & Assert

    with pytest.raises(error):
        Color.from_hex(hexa)

@pytest.mark.parametrize(
    "rgb, expected, test_id",
    [
        ("255,0,0", Color(255, 0, 0), "rgb_red"),
        ("0,255,0", Color(0, 255, 0), "rgb_green"),
        ("0,0,255", Color(0, 0, 255), "rgb_blue"),
        ("255,255,255", Color(255, 255, 255), "rgb_white"),
        ("0,0,0", Color(0, 0, 0), "rgb_black"),
        ("255,0,0,128", Color(255, 0, 0, 128), "rgba_red_halfalpha"),
        (" 255 , 0 , 0 ", Color(255, 0, 0), "rgb_spaces"),
        (" 255 , 0 , 0 , 128 ", Color(255, 0, 0, 128), "rgba_spaces"),
    ],
    ids=lambda p: p if isinstance(p, str) else None
)
def test_from_rgb_happy(rgb, expected, test_id):
    # Act

    result = Color.from_rgb(rgb)

    # Assert

    assert result == expected

@pytest.mark.parametrize(
    "rgb, error, test_id",
    [
        ("255,0", ValueError, "rgb_too_few"),
        ("255,0,0,0,0", ValueError, "rgb_too_many"),
        ("256,0,0", ValueError, "rgb_r_too_high"),
        ("-1,0,0", ValueError, "rgb_r_negative"),
        ("0,256,0", ValueError, "rgb_g_too_high"),
        ("0,-1,0", ValueError, "rgb_g_negative"),
        ("0,0,256", ValueError, "rgb_b_too_high"),
        ("0,0,-1", ValueError, "rgb_b_negative"),
        ("0,0,0,256", ValueError, "rgba_a_too_high"),
        ("0,0,0,-1", ValueError, "rgba_a_negative"),
        ("a,b,c", ValueError, "rgb_nonint"),
        ("255,0,0,a", ValueError, "rgba_nonint_alpha"),
    ],
    ids=lambda p: p if isinstance(p, str) else None
)
def test_from_rgb_errors(rgb, error, test_id):
    # Act & Assert

    with pytest.raises(error):
        Color.from_rgb(rgb)

@pytest.mark.parametrize(
    "colorstr, expected, test_id",
    [
        ("#f00", Color(255, 0, 0), "auto_hex3"),
        ("#ff0000", Color(255, 0, 0), "auto_hex6"),
        ("#ff0000ff", Color(255, 0, 0, 255), "auto_hex8"),
        ("rgb(255,0,0)", Color(255, 0, 0), "auto_rgb_func"),
        ("rgba(255,0,0,128)", Color(255, 0, 0, 128), "auto_rgba_func"),
        ("255,0,0", Color(255, 0, 0), "auto_rgb_plain"),
        ("255,0,0,128", Color(255, 0, 0, 128), "auto_rgba_plain"),
        (" RGB(255,0,0) ", Color(255, 0, 0), "auto_rgb_func_caps"),
        (" RGBA(255,0,0,128) ", Color(255, 0, 0, 128), "auto_rgba_func_caps"),
        (" 255 , 0 , 0 ", Color(255, 0, 0), "auto_rgb_spaces"),
    ],
    ids=lambda p: p if isinstance(p, str) else None
)
def test_from_auto_happy(colorstr, expected, test_id):
    # Act

    result = Color.from_auto(colorstr.strip())

    # Assert

    assert result == expected

@pytest.mark.parametrize(
    "colorstr, error, test_id",
    [
        ("", ValueError, "auto_empty"),
        ("#ff", ValueError, "auto_hex_invalid"),
        ("rgb(255,0)", ValueError, "auto_rgb_invalid"),
        ("rgba(255,0,0,256)", ValueError, "auto_rgba_alpha_invalid"),
        ("hsl(0,100%,50%)", ValueError, "auto_hsl_not_supported"),
        ("notacolor", ValueError, "auto_garbage"),
    ],
    ids=lambda p: p if isinstance(p, str) else None
)
def test_from_auto_errors(colorstr, error, test_id):
    # Act & Assert

    with pytest.raises(error):
        Color.from_auto(colorstr)

def test_str_and_repr_methods():
    # Arrange

    c = Color(1, 2, 3, 4)

    # Act

    s = str(c)
    r = repr(c)

    # Assert

    assert s == "rgba(1, 2, 3, 4)"
    assert "Color(1 2 3 4)" in r
    assert "\033[38;2;1;2;3m" in r
    assert r.endswith("\033[0m")

def test_opposite():
    # Arrange

    c = Color(10, 20, 30, 40)

    # Act

    opp = c.opposite()

    # Assert

    assert opp == Color(245, 235, 225, 40)

def test_grayshade():
    # Arrange

    c = Color(100, 150, 200, 128)

    # Act

    gray = c.grayshade()

    # Assert

    expected_gray = round(0.299 * 100 + 0.587 * 150 + 0.114 * 200)
    assert gray == Color(expected_gray, expected_gray, expected_gray, 128)

@pytest.mark.parametrize(
    "color, expected, test_id",
    [
        (Color(201, 201, 56), Color(255, 255, 255, 255), "bw_white"),
        (Color(200, 200, 55), Color(255, 255, 255, 255), "bw_black_b55"),
        (Color(199, 201, 201), Color(0, 0, 0, 255), "bw_black_r199"),
        (Color(201, 199, 201), Color(0, 0, 0, 255), "bw_black_g199"),
        (Color(201, 201, 54), Color(0, 0, 0, 255), "bw_black_b54"),
    ],
    ids=["bw_white", "bw_black_b55", "bw_black_r199", "bw_black_g199", "bw_black_b54"]
)
def test_black_or_white(color, expected, test_id):
    # Act

    result = color.black_or_white()

    # Assert

    assert result == expected

def test_rgb_hex_and_rgba_hex():
    # Arrange

    c = Color(1, 2, 3, 4)

    # Act

    rgb_hex = c.rgb_hex()
    rgba_hex = c.rgba_hex()

    # Assert

    assert rgb_hex == "#010203"
    assert rgba_hex == "#01020304"

def test_rgb_and_rgba_methods():
    # Arrange

    c = Color(1, 2, 3, 4)

    # Act

    rgb = c.rgb()
    rgba = c.rgba()

    # Assert

    assert rgb == "rgb(1, 2, 3)"
    assert rgba == "rgba(1, 2, 3, 4)"

def test_eq_and_ne():
    # Arrange

    c1 = Color(1, 2, 3, 4)
    c2 = Color(1, 2, 3, 4)
    c3 = Color(4, 3, 2, 1)

    # Act & Assert

    assert c1 == c2
    assert not (c1 != c2)
    assert c1 != c3
    assert not (c1 == c3)
    assert (c1 != "notacolor") is True
    assert (c1 == "notacolor") is False

def test_add_and_sub():
    # Arrange

    c1 = Color(10, 20, 30, 40)
    c2 = Color(5, 15, 25, 35)
    c3 = Color(250, 250, 250, 250)

    # Act

    add = c1 + c2
    sub = c1 - c2
    add_clamped = c1 + c3
    sub_clamped = c1 - c3

    # Assert

    assert add == Color(15, 35, 55, 75)
    assert sub == Color(5, 5, 5, 5)
    assert add_clamped == Color(255, 255, 255, 255)
    assert sub_clamped == Color(0, 0, 0, 0)
    with pytest.raises(TypeError):
        c1 + "notacolor"
    with pytest.raises(TypeError):
        c1 - "notacolor"

def test_hash():
    # Arrange

    c1 = Color(1, 2, 3, 4)
    c2 = Color(1, 2, 3, 4)
    c3 = Color(4, 3, 2, 1)

    # Act

    h1 = hash(c1)
    h2 = hash(c2)
    h3 = hash(c3)

    # Assert

    assert h1 == h2
    assert h1 != h3
    assert len({c1, c2, c3}) == 2
