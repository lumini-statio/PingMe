import flet as ft
from enum import Enum

"""
Define constants
"""
class Styles(Enum):
    """
    Enumerate different app styles options
    """
    MIN_TEXT_SIZE = 18
    MID_TEXT_SIZE = 24
    MAX_TEXT_SIZE = 28
    HEADER_TEXT_SIZE = 100
    BTN_RADIUS = 7
    BORDER = ft.border.all(1, ft.Colors.TRANSPARENT)
    ERROR_COLOR = ft.Colors.RED_700
    DROP_COLOR = ft.Colors.GREY_700
    BG_COLOR = ft.Colors.GREY_900
    BTN_NOT_ACTIATED_BG = ft.Colors.BLUE_900
    BORDER_COLOR = ft.Colors.TRANSPARENT

    PAGE_THEME = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
        visual_density=ft.VisualDensity.COMFORTABLE,
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE,
            secondary=ft.Colors.ORANGE,
            background=BG_COLOR.value,
            surface=ft.Colors.GREY_800
        ),
    )