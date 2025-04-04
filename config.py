import flet as ft
from enum import Enum
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

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
    BG_COLOR = ft.Colors.GREY_900
    BTN_NOT_ACTIATED_BG = ft.Colors.BLUE_900
    BORDER_COLOR = ft.Colors.TRANSPARENT

    PAGE_WIDTH = 700
    PAGE_HEIGHT = 700
    PAGE_THEME = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE_400,
        visual_density=ft.VisualDensity.COMFORTABLE,
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.PRIMARY,
            secondary=ft.Colors.GREEN_100,
            background=BG_COLOR.value,
            surface=ft.Colors.GREY_800
        ),
    )