# -*- coding: utf-8 -*-

import pygame
import asyncio
import random
import math
import sys
import os
from collections import OrderedDict



# =========================================================
# ДЕТАЛЬНАЯ ГРАФИКА CYCLOPS / SEAMOTH ИЗ МАЛОГО КОДА
# =========================================================
# В референсном файле фигуры строятся в двойном разрешении и затем
# уменьшаются. Это сохраняет гладкие края и все мелкие панели/окна.
AA = 2

def P(x, y):
    return int(x * AA), int(y * AA)


def poly(surface, color, points, width=0):
    pts = [P(x, y) for x, y in points]
    pygame.draw.polygon(surface, color, pts, width * AA)


def ellipse(surface, color, rect, width=0):
    x, y, w, h = rect
    pygame.draw.ellipse(
        surface,
        color,
        pygame.Rect(
            int(x * AA),
            int(y * AA),
            int(w * AA),
            int(h * AA)
        ),
        width * AA
    )


def rect(surface, color, r, width=0, radius=0):
    x, y, w, h = r
    pygame.draw.rect(
        surface,
        color,
        pygame.Rect(
            int(x * AA),
            int(y * AA),
            int(w * AA),
            int(h * AA)
        ),
        width * AA,
        border_radius=radius * AA
    )


def line(surface, color, a, b, width=1):
    pygame.draw.line(
        surface,
        color,
        P(*a),
        P(*b),
        width * AA
    )


def circle(surface, color, pos, radius, width=0):
    pygame.draw.circle(
        surface,
        color,
        P(*pos),
        int(radius * AA),
        width * AA
    )


def aaline(surface, color, points, closed=False):
    pygame.draw.aalines(
        surface,
        color,
        closed,
        [P(x, y) for x, y in points]
    )

# ============================================================
# ЦИКЛОП
# ============================================================

def draw_cyclops(surface, cx, cy, scale=1.0):

    def pt(x, y):
        return cx + x * scale, cy + y * scale

    # --------------------------------------------------------
    # ТЕНЬ
    # --------------------------------------------------------

    shadow = [
        pt(-295, -45),
        pt(-260, -72),
        pt(-150, -91),
        pt(70, -88),
        pt(205, -65),
        pt(290, -33),
        pt(318, 0),
        pt(290, 33),
        pt(205, 65),
        pt(70, 88),
        pt(-150, 91),
        pt(-260, 72),
        pt(-295, 45),
    ]

    poly(surface, (0, 7, 10), shadow)

    # --------------------------------------------------------
    # ОСНОВНОЙ СИЛУЭТ
    # нос справа
    # --------------------------------------------------------

    body = [
        pt(-300, 0),
        pt(-283, -40),
        pt(-245, -67),
        pt(-180, -82),
        pt(-60, -87),
        pt(85, -81),
        pt(183, -68),
        pt(248, -46),
        pt(289, -21),
        pt(307, 0),

        pt(289, 21),
        pt(248, 46),
        pt(183, 68),
        pt(85, 81),
        pt(-60, 87),
        pt(-180, 82),
        pt(-245, 67),
        pt(-283, 40),
    ]

    poly(surface, (126, 132, 126), body)

    # Обводка корпуса
    pygame.draw.aalines(
        surface,
        (33, 38, 37),
        True,
        [P(x, y) for x, y in body]
    )

    # --------------------------------------------------------
    # СВЕТЛАЯ ЦЕНТРАЛЬНАЯ ПАНЕЛЬ
    # --------------------------------------------------------

    center_panel = [
        pt(-225, -54),
        pt(-135, -66),
        pt(65, -67),
        pt(175, -55),
        pt(248, -32),
        pt(267, 0),

        pt(248, 32),
        pt(175, 55),
        pt(65, 67),
        pt(-135, 66),
        pt(-225, 54),
        pt(-254, 0),
    ]

    poly(surface, (177, 181, 172), center_panel)

    # --------------------------------------------------------
    # ОРАНЖЕВЫЕ БОРТОВЫЕ СЕКЦИИ
    # --------------------------------------------------------

    orange = (224, 102, 28)
    orange_dark = (151, 61, 18)
    orange_light = (246, 131, 39)

    top_orange = [
        pt(-205, -61),
        pt(-110, -76),
        pt(70, -74),
        pt(161, -61),
        pt(174, -46),
        pt(58, -50),
        pt(-116, -51),
    ]

    bottom_orange = [
        pt(-205, 61),
        pt(-110, 76),
        pt(70, 74),
        pt(161, 61),
        pt(174, 46),
        pt(58, 50),
        pt(-116, 51),
    ]

    poly(surface, orange_dark, top_orange)
    poly(surface, orange_dark, bottom_orange)

    inner_top = [
        pt(-160, -58),
        pt(-80, -68),
        pt(60, -67),
        pt(137, -57),
        pt(146, -50),
        pt(54, -54),
        pt(-92, -54),
    ]

    inner_bottom = [
        pt(-160, 58),
        pt(-80, 68),
        pt(60, 67),
        pt(137, 57),
        pt(146, 50),
        pt(54, 54),
        pt(-92, 54),
    ]

    poly(surface, orange, inner_top)
    poly(surface, orange, inner_bottom)

    line(surface, orange_light, pt(-120, -61), pt(75, -61), 2)
    line(surface, orange_light, pt(-120, 61), pt(75, 61), 2)

    # --------------------------------------------------------
    # ЦЕНТРАЛЬНАЯ СПИНА
    # --------------------------------------------------------

    spine = [
        pt(-245, -20),
        pt(-130, -30),
        pt(85, -28),
        pt(210, -18),
        pt(269, 0),
        pt(210, 18),
        pt(85, 28),
        pt(-130, 30),
        pt(-245, 20),
    ]

    poly(surface, (77, 82, 79), spine)

    spine2 = [
        pt(-215, -12),
        pt(-105, -18),
        pt(91, -16),
        pt(192, -10),
        pt(237, 0),
        pt(192, 10),
        pt(91, 16),
        pt(-105, 18),
        pt(-215, 12),
    ]

    poly(surface, (112, 117, 111), spine2)

    # --------------------------------------------------------
    # КОМАНДНАЯ РУБКА
    # --------------------------------------------------------

    tower = [
        pt(-48, -32),
        pt(59, -30),
        pt(102, -20),
        pt(115, 0),
        pt(102, 20),
        pt(59, 30),
        pt(-48, 32),
        pt(-78, 19),
        pt(-84, 0),
        pt(-78, -19),
    ]

    poly(surface, (48, 53, 52), tower)

    tower_inner = [
        pt(-38, -22),
        pt(50, -21),
        pt(82, -14),
        pt(94, 0),
        pt(82, 14),
        pt(50, 21),
        pt(-38, 22),
        pt(-63, 13),
        pt(-68, 0),
        pt(-63, -13),
    ]

    poly(surface, (93, 102, 99), tower_inner)

    # --------------------------------------------------------
    # ОКНА РУБКИ
    # --------------------------------------------------------

    glass = (20, 76, 88)
    glass_light = (49, 139, 152)

    windows = [
        (-24, -15, 25, 12),
        (5, -15, 25, 12),
        (34, -14, 23, 11),
        (61, -11, 17, 9),

        (-24, 3, 25, 12),
        (5, 3, 25, 12),
        (34, 3, 23, 11),
        (61, 2, 17, 9),
    ]

    for x, y, w, h in windows:
        rect(
            surface,
            glass,
            (
                cx + x * scale,
                cy + y * scale,
                w * scale,
                h * scale
            ),
            radius=max(1, int(3 * scale))
        )

        line(
            surface,
            glass_light,
            pt(x + 3, y + 3),
            pt(x + w - 3, y + 3),
            max(1, int(1.5 * scale))
        )

    # --------------------------------------------------------
    # ЛЮК
    # --------------------------------------------------------

    ellipse(
        surface,
        (43, 47, 46),
        (
            cx - 122 * scale,
            cy - 17 * scale,
            39 * scale,
            34 * scale
        )
    )

    ellipse(
        surface,
        (122, 130, 125),
        (
            cx - 116 * scale,
            cy - 12 * scale,
            27 * scale,
            24 * scale
        ),
        width=max(1, int(3 * scale))
    )

    line(surface, (35, 38, 38),
         pt(-115, 0), pt(-91, 0),
         max(1, int(2 * scale)))

    # --------------------------------------------------------
    # ДЕТАЛИ КОРПУСА
    # --------------------------------------------------------

    for x in [-190, -145, -100, 120, 155, 190]:
        line(
            surface,
            (69, 73, 70),
            pt(x, -48),
            pt(x + 8, 48),
            max(1, int(scale))
        )

    # Панели
    for x in [-190, -142, -94, 118, 156]:
        rect(
            surface,
            (67, 71, 68),
            (
                cx + x * scale,
                cy - 15 * scale,
                32 * scale,
                30 * scale
            ),
            width=max(1, int(scale)),
            radius=max(1, int(3 * scale))
        )

    # --------------------------------------------------------
    # КОРМОВОЙ БЛОК
    # --------------------------------------------------------

    stern = [
        pt(-300, -36),
        pt(-336, -30),
        pt(-356, -17),
        pt(-365, 0),
        pt(-356, 17),
        pt(-336, 30),
        pt(-300, 36),
        pt(-282, 20),
        pt(-282, -20),
    ]

    poly(surface, (58, 61, 60), stern)

    # --------------------------------------------------------
    # ДВИГАТЕЛИ
    # --------------------------------------------------------

    engine_positions = [-46, 46]

    for ey in engine_positions:

        # крепление
        poly(
            surface,
            (62, 65, 62),
            [
                pt(-238, ey - 20),
                pt(-319, ey - 25),
                pt(-335, ey - 14),
                pt(-335, ey + 14),
                pt(-319, ey + 25),
                pt(-238, ey + 20)
            ]
        )

        # двигатель
        ellipse(
            surface,
            (39, 42, 42),
            (
                cx - 355 * scale,
                cy + (ey - 20) * scale,
                72 * scale,
                40 * scale
            )
        )

        ellipse(
            surface,
            (103, 109, 103),
            (
                cx - 344 * scale,
                cy + (ey - 14) * scale,
                46 * scale,
                28 * scale
            )
        )

        # внутреннее кольцо
        ellipse(
            surface,
            (18, 31, 31),
            (
                cx - 337 * scale,
                cy + (ey - 10) * scale,
                31 * scale,
                20 * scale
            )
        )

        # двигатель, голубое свечение
        ellipse(
            surface,
            (38, 157, 175),
            (
                cx - 334 * scale,
                cy + (ey - 7) * scale,
                20 * scale,
                14 * scale
            )
        )

        ellipse(
            surface,
            (122, 226, 231),
            (
                cx - 330 * scale,
                cy + (ey - 4) * scale,
                11 * scale,
                8 * scale
            )
        )

    # --------------------------------------------------------
    # БОКОВЫЕ КИЛИ / СТАБИЛИЗАТОРЫ
    # --------------------------------------------------------

    poly(
        surface,
        (72, 77, 74),
        [
            pt(-178, -71),
            pt(-130, -118),
            pt(-50, -113),
            pt(-72, -76)
        ]
    )

    poly(
        surface,
        (72, 77, 74),
        [
            pt(-178, 71),
            pt(-130, 118),
            pt(-50, 113),
            pt(-72, 76)
        ]
    )

    # Оранжевая маркировка плавников
    poly(
        surface,
        orange,
        [
            pt(-131, -108),
            pt(-78, -103),
            pt(-95, -79),
            pt(-153, -82)
        ]
    )

    poly(
        surface,
        orange,
        [
            pt(-131, 108),
            pt(-78, 103),
            pt(-95, 79),
            pt(-153, 82)
        ]
    )

    # --------------------------------------------------------
    # НОСОВАЯ ЧАСТЬ
    # --------------------------------------------------------

    nose = [
        pt(213, -40),
        pt(273, -28),
        pt(306, -8),
        pt(312, 0),
        pt(306, 8),
        pt(273, 28),
        pt(213, 40),
        pt(235, 18),
        pt(246, 0),
        pt(235, -18),
    ]

    poly(surface, (198, 200, 188), nose)

    # Носовые окна
    for yy in [-16, 4]:
        rect(
            surface,
            (19, 79, 89),
            (
                cx + 244 * scale,
                cy + yy * scale,
                34 * scale,
                12 * scale
            ),
            radius=max(1, int(3 * scale))
        )

    # --------------------------------------------------------
    # ФАРЫ
    # --------------------------------------------------------

    for yy in [-25, 25]:
        circle(surface, (55, 64, 61), pt(261, yy), 7 * scale)
        circle(surface, (186, 229, 217), pt(263, yy), 4 * scale)
        circle(surface, (235, 255, 236), pt(264, yy), 2 * scale)

    # --------------------------------------------------------
    # НОМЕР / ДЕКОР
    # --------------------------------------------------------

    line(
        surface,
        (215, 112, 37),
        pt(112, -35),
        pt(190, -29),
        max(1, int(4 * scale))
    )

    line(
        surface,
        (215, 112, 37),
        pt(112, 35),
        pt(190, 29),
        max(1, int(4 * scale))
    )


# ============================================================
# МОТЫЛЁК / SEAMOTH
# ============================================================

def draw_seamoth(surface, cx, cy, scale=1.0):

    def pt(x, y):
        return cx + x * scale, cy + y * scale

    white = (210, 213, 201)
    light = (234, 235, 217)
    dark = (54, 59, 57)

    orange = (225, 111, 27)
    orange2 = (247, 142, 39)

    glass = (17, 72, 84)
    glass_light = (67, 169, 179)

    # --------------------------------------------------------
    # ТЕНЬ
    # --------------------------------------------------------

    ellipse(
        surface,
        (0, 7, 10),
        (
            cx - 105 * scale,
            cy - 58 * scale,
            215 * scale,
            116 * scale
        )
    )

    # --------------------------------------------------------
    # БОКОВЫЕ КРЫЛЬЯ
    # --------------------------------------------------------

    poly(
        surface,
        dark,
        [
            pt(-20, -34),
            pt(-79, -89),
            pt(-122, -83),
            pt(-93, -43),
            pt(-61, -19)
        ]
    )

    poly(
        surface,
        dark,
        [
            pt(-20, 34),
            pt(-79, 89),
            pt(-122, 83),
            pt(-93, 43),
            pt(-61, 19)
        ]
    )

    # Светлые панели крыльев
    poly(
        surface,
        white,
        [
            pt(-42, -40),
            pt(-81, -76),
            pt(-106, -71),
            pt(-82, -44),
            pt(-55, -25)
        ]
    )

    poly(
        surface,
        white,
        [
            pt(-42, 40),
            pt(-81, 76),
            pt(-106, 71),
            pt(-82, 44),
            pt(-55, 25)
        ]
    )

    # --------------------------------------------------------
    # ДВИГАТЕЛИ НА КРЫЛЬЯХ
    # --------------------------------------------------------

    for yy in (-72, 72):

        ellipse(
            surface,
            (40, 45, 44),
            (
                cx - 113 * scale,
                cy + (yy - 16) * scale,
                45 * scale,
                32 * scale
            )
        )

        ellipse(
            surface,
            (105, 111, 106),
            (
                cx - 105 * scale,
                cy + (yy - 11) * scale,
                29 * scale,
                22 * scale
            )
        )

        ellipse(
            surface,
            (20, 110, 126),
            (
                cx - 98 * scale,
                cy + (yy - 7) * scale,
                17 * scale,
                14 * scale
            )
        )

        ellipse(
            surface,
            (90, 220, 225),
            (
                cx - 93 * scale,
                cy + (yy - 4) * scale,
                8 * scale,
                8 * scale
            )
        )

    # --------------------------------------------------------
    # ОСНОВНОЙ КОРПУС
    # --------------------------------------------------------

    body = [
        pt(-86, 0),
        pt(-71, -32),
        pt(-40, -50),
        pt(0, -58),
        pt(42, -51),
        pt(78, -33),
        pt(103, -10),
        pt(109, 0),

        pt(103, 10),
        pt(78, 33),
        pt(42, 51),
        pt(0, 58),
        pt(-40, 50),
        pt(-71, 32),
    ]

    poly(surface, white, body)

    # Нижняя тёмная окантовка
    outline = [
        pt(-79, 0),
        pt(-62, -27),
        pt(-32, -43),
        pt(5, -48),
        pt(42, -42),
        pt(72, -27),
        pt(94, -8),
        pt(98, 0),
        pt(94, 8),
        pt(72, 27),
        pt(42, 42),
        pt(5, 48),
        pt(-32, 43),
        pt(-62, 27),
    ]

    pygame.draw.aalines(
        surface,
        (57, 62, 59),
        True,
        [P(x, y) for x, y in outline]
    )

    # --------------------------------------------------------
    # ОРАНЖЕВЫЕ ПОЛОСЫ
    # --------------------------------------------------------

    poly(
        surface,
        orange,
        [
            pt(-48, -42),
            pt(-24, -52),
            pt(-9, -54),
            pt(-19, -29),
            pt(-39, -23)
        ]
    )

    poly(
        surface,
        orange,
        [
            pt(-48, 42),
            pt(-24, 52),
            pt(-9, 54),
            pt(-19, 29),
            pt(-39, 23)
        ]
    )

    # --------------------------------------------------------
    # КАБИНА
    # --------------------------------------------------------

    cockpit = [
        pt(-23, -33),
        pt(21, -37),
        pt(55, -27),
        pt(77, -11),
        pt(84, 0),
        pt(77, 11),
        pt(55, 27),
        pt(21, 37),
        pt(-23, 33),
        pt(-42, 20),
        pt(-48, 0),
        pt(-42, -20),
    ]

    poly(surface, dark, cockpit)

    glass_shape = [
        pt(-13, -27),
        pt(20, -30),
        pt(49, -22),
        pt(68, -9),
        pt(74, 0),

        pt(68, 9),
        pt(49, 22),
        pt(20, 30),
        pt(-13, 27),

        pt(-30, 16),
        pt(-35, 0),
        pt(-30, -16),
    ]

    poly(surface, glass, glass_shape)

    # Отражения
    line(
        surface,
        glass_light,
        pt(-17, -20),
        pt(42, -17),
        max(1, int(2 * scale))
    )

    line(
        surface,
        (119, 205, 208),
        pt(41, -15),
        pt(60, -7),
        max(1, int(2 * scale))
    )

    # Центральная рама кабины
    line(
        surface,
        (37, 44, 43),
        pt(18, -29),
        pt(18, 29),
        max(1, int(3 * scale))
    )

    # --------------------------------------------------------
    # НОС
    # --------------------------------------------------------

    poly(
        surface,
        light,
        [
            pt(70, -28),
            pt(101, -12),
            pt(112, 0),
            pt(101, 12),
            pt(70, 28),
            pt(83, 10),
            pt(87, 0),
            pt(83, -10)
        ]
    )

    # Фары
    for yy in [-15, 15]:

        circle(
            surface,
            (47, 56, 54),
            pt(92, yy),
            7 * scale
        )

        circle(
            surface,
            (181, 224, 214),
            pt(94, yy),
            4.5 * scale
        )

        circle(
            surface,
            (244, 255, 235),
            pt(95, yy),
            2 * scale
        )

    # --------------------------------------------------------
    # КОРМОВАЯ СЕКЦИЯ
    # --------------------------------------------------------

    poly(
        surface,
        (72, 77, 73),
        [
            pt(-86, -22),
            pt(-111, -18),
            pt(-123, -8),
            pt(-127, 0),
            pt(-123, 8),
            pt(-111, 18),
            pt(-86, 22)
        ]
    )

    # задний двигатель
    ellipse(
        surface,
        (39, 44, 43),
        (
            cx - 130 * scale,
            cy - 18 * scale,
            37 * scale,
            36 * scale
        )
    )

    ellipse(
        surface,
        (22, 124, 140),
        (
            cx - 125 * scale,
            cy - 12 * scale,
            24 * scale,
            24 * scale
        )
    )

    ellipse(
        surface,
        (94, 224, 227),
        (
            cx - 120 * scale,
            cy - 8 * scale,
            15 * scale,
            16 * scale
        )
    )

    # --------------------------------------------------------
    # ВЕРХНЯЯ ПАНЕЛЬ
    # --------------------------------------------------------

    ellipse(
        surface,
        (75, 82, 78),
        (
            cx - 72 * scale,
            cy - 18 * scale,
            35 * scale,
            36 * scale
        )
    )

    ellipse(
        surface,
        orange2,
        (
            cx - 66 * scale,
            cy - 12 * scale,
            23 * scale,
            24 * scale
        ),
        width=max(1, int(3 * scale))
    )

    # Болты
    for bx, by in [
        (-55, -33),
        (-55, 33),
        (62, -28),
        (62, 28)
    ]:
        circle(
            surface,
            (79, 82, 78),
            pt(bx, by),
            3 * scale
        )

def _make_reference_vehicle_sprite(draw_func, logical_size, center, target_width):
    logical_w, logical_h = logical_size
    source = pygame.Surface(
        (logical_w * AA, logical_h * AA), pygame.SRCALPHA
    )
    draw_func(source, center[0], center[1], 1.0)

    bounds = source.get_bounding_rect(min_alpha=1)
    if bounds.width > 0 and bounds.height > 0:
        source = source.subsurface(bounds).copy()

    target_width = max(1, int(target_width))
    target_height = max(1, int(round(
        target_width * source.get_height() / max(1, source.get_width())
    )))
    return pygame.transform.smoothscale(
        source, (target_width, target_height)
    ).convert_alpha()


def generate_detailed_cyclops_vehicle_sprite(target_width=180):
    return _make_reference_vehicle_sprite(
        draw_cyclops, (760, 270), (390, 135), target_width
    )


def generate_detailed_seamoth_vehicle_sprite(target_width=86):
    return _make_reference_vehicle_sprite(
        draw_seamoth, (300, 220), (150, 110), target_width
    )


# =========================================================
# КОНСТАНТЫ
# =========================================================

MAP_SIZE = 1000

CELL_SIZE = 30
VIEW_RADIUS = 10

# Масштаб камеры: 1.0 — обычный вид, меньше 1 — отдаление.
# Фактическое количество видимых клеток зависит от масштаба.
CAMERA_ZOOM_MIN = 0.60
CAMERA_ZOOM_MAX = 1.80
CAMERA_ZOOM_STEP = 1.15

# Детализация LOD: отрисовка новых деталей в РАЗРЕШЕНИИ ЭКРАНА.
# Маленькие игровые иконки не просто растягиваются: рыбы, растения,
# минералы и постройки заново создаются из фигур при увеличении.
ZOOM_DETAIL_ENABLED = True
ZOOM_DETAIL_START = 1.10
ZOOM_DETAIL_SOURCE_FACTOR = 2.6
ZOOM_DETAIL_ROTATION_STEP = 6
ZOOM_DETAIL_ROTATED_CACHE_MAX = 90

# Дополнительная ночная виньетка: края становятся совершенно чёрными
# около полуночи; центр остаётся прозрачным, сохраняя биосвечение.
NIGHT_EDGE_VIGNETTE = True
NIGHT_EDGE_FADE = 0.43  # ширина плавного перехода, доля экрана

# Ночное мерцание воды: отдельные декоративные частицы (не предметы).
# На максимуме ночи появляется до 520 частиц в области камеры.
NIGHT_PLANKTON_ENABLED = True
# Дальность, на которой хищник замечает игрока и начинает преследование.
# Значения измеряются в игровых клетках; у Сталкера — ровно 3 клетки.
PREDATOR_DETECTION_RANGE_BY_NAME = {
    "Stalker": 3.0,
    "Biter": 2.0,
    "Sand Shark": 4.0,
    "Boneshark": 4.0,
    "Crabsnake": 3.5,
    "Crabsquid": 5.0,
    "Ampeel": 4.5,
    "Warper": 5.0,
    "Reaper Leviathan": 7.0,
    "Ghost Leviathan": 7.0,
    "Sea Dragon Leviathan": 8.0,
    "Dragon Leviathan": 8.0,
    "Gasopod": 2.5,
}
PREDATOR_DETECTION_RANGE_DEFAULT = 4.0
NIGHT_PLANKTON_MAX = 520
NIGHT_FRY_CHANCE = 0.18       # доля мальков среди светящихся точек
NIGHT_FLEE_CHANCE = 0.36      # доля частиц, реагирующих на приближение
NIGHT_VISIBLE_BRIGHTNESS = 0.50  # строго ночь: ~18:00–06:00

SCREEN_SIZE = (VIEW_RADIUS * 2 + 1) * CELL_SIZE



def game_font(size, bold=False):
    """Use a bundled Cyrillic-capable web font when one is available.

    Browser OS fonts aren't exposed to pygame-web, so CI downloads an
    OFL-licensed Noto Sans into the game folder before building. Desktop
    continues using the original Arial/SysFont appearance as before.
    """
    font_path = os.path.join(os.path.dirname(__file__), "NotoSans.ttf")
    if os.path.isfile(font_path):
        result = pygame.font.Font(font_path, size)
        result.set_bold(bold)
        return result
    return pygame.font.SysFont("Arial", size, bold=bold)


def create_game_display():
    """Desktop stays fullscreen, browser uses a fixed logical canvas.

    Browser fullscreen and SCALED flags can break WebAssembly backends, so
    CSS / the pygbag host scales the browser canvas without changing the
    original 630x630 logical drawing coordinates or pixel art algorithms.
    """
    current = pygame.display.get_surface()
    if current is not None and current.get_size() == (SCREEN_SIZE, SCREEN_SIZE):
        return current
    if sys.platform == "emscripten":
        flags = 0
    else:
        flags = pygame.FULLSCREEN
        if hasattr(pygame, "SCALED"):
            flags |= pygame.SCALED
    return pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE), flags)

INVENTORY_SIZE = 30
INVENTORY_COLS = 6
INVENTORY_ROWS = 5

# =========================================================
# СТАРТОВЫЙ ИНВЕНТАРЬ — НАСТРАИВАЕТСЯ ЗДЕСЬ
# =========================================================
# Укажите игровое название предмета и нужное количество.
# Пример:
#
START_INVENTORY = {
    "Мотылёк": 1,
    "Циклоп": 1,
    "Ремкомплект": 3,
    "Сканер": 1,
    "Нож": 1,
    "Титан": 10,
    "Медная руда": 5,
    "Sea Dragon Leviathan": 1,
}
#
# Можно добавлять любые существующие предметы/ресурсы/рыб,


# Заполняется функцией init_assets().
# Содержит ВСЕ ObjectType/AnimalType, в том числе те, которые внутри
# init_assets() являются локальными переменными (например "Нож").
START_ITEM_REGISTRY = {}

# =========================================================
# V3: ОСВЕЩЕНИЕ И РЕАКЦИЯ ФАУНЫ НА СВЕТ
# =========================================================
# В оригинале явно подтверждено притяжение Crabsquid и избегание
# направленного света Oculus. Для Boneshark сведения противоречивы:
# небольшое притяжение здесь сделано по описанию КПК. Реакция двух
# дополнительных хищников — настраиваемая игровая адаптация.
# Удалите их из словаря, если хотите строго подтверждённое поведение.
LIGHT_ATTRACTION = {"Crabsquid": 1.0, "Boneshark": 0.55}
LIGHT_AVERSION = {"Oculus": 1.0, "Mesmer": 0.65, "Blighter": 0.70}
LIGHTING_ENABLED = True
VEHICLE_HEADLIGHTS_DEFAULT = True
# Ракета остаётся источником света, но в темноте не отвлекает и
# не отпугивает хищников. На свет остальных приборов они реагируют.
FLARES_DO_NOT_AFFECT_PREDATORS_AT_NIGHT = True


SLOT_SIZE = 50
SLOT_MARGIN = 10

WORLD_CHUNK_SIZE = 32
CAVE_CHUNK_SIZE = 32
ANIMAL_CHUNK_SIZE = 16
ROTATION_STEP = 3
MAX_BIOME_CACHE = 50000
MAX_CAVE_CACHE = 50000
FISH_COUNT_MULTIPLIER = 3

# =========================================================
# НАСТРОЙКА ФЛОРЫ И ФАУНЫ КАЖДОГО ПЕЩЕРНОГО ТОННЕЛЯ
# =========================================================
# Ключ — ТОЧНОЕ имя туннеля (tunnel.name). Неуказанные туннели используют
# стандартный профиль своего поверхностного биома и всё равно получают рыбу.
# Если для туннеля указан ключ "flora" или "fauna", его состав заменяется
# полностью: пустой словарь, например, отключит соответствующую флору/фауну.
#
# Флора: имя из flora_types (например acid_mushroom, sulfur_plant, cave_bush)
#        -> плотность (больше число — больше растений).
# Фауна: ключ из списка ниже (например peeper, bladderfish, crabsnake)
#        -> количество существ в этом туннеле.
#
# Пример — уберите символы # у строк, чтобы включить настройку:
# CAVE_TUNNEL_ECOSYSTEM_OVERRIDES = {
#     "Безопасные отмели: центральный пещерный узел": {
#         "flora": {"acid_mushroom": 3.0, "sulfur_plant": 1.5},
#         "fauna": {"peeper": 8, "bladderfish": 4},
#     },
#     "Грибной лес (запад): боковой зал 1": {
#         "flora": {"jellyshroom": 2.5, "cave_bush": 1.0},
#         "fauna": {"oculus": 5, "crabsnake": 2},
#     },
# }
CAVE_TUNNEL_ECOSYSTEM_OVERRIDES = {}

# =========================================================
# БИОЛЮМИНЕСЦЕНЦИЯ V2 И ПОЛНАЯ НОЧНАЯ ТЕМНОТА
# =========================================================
BIOLUMINESCENCE_ENABLED = True
MIDNIGHT_BLACKOUT = True
# Доля суток до/после полуночи, когда экран полностью чёрный.
# 0.05 = примерно 01:12 (то есть 22:48–01:12).
MIDNIGHT_BLACKOUT_HALF_WINDOW = 0.05
# Свет сохраняет естественную форму организма и не открывает весь мир.
BIOGLOW_DAY_ALPHA = 105
BIOGLOW_NIGHT_ALPHA = 250

START_CAPSULE_WIDTH = 8
START_CAPSULE_HEIGHT = 6
START_CAPSULE_INNER_WIDTH = 6
START_CAPSULE_INNER_HEIGHT = 4


# =========================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =========================================================

def quantize_angle(angle):
    return int(round(angle / ROTATION_STEP) * ROTATION_STEP) % 360


def load_image_with_proportions(path, target_size, colorkey=(255, 255, 255)):
    if not os.path.exists(path):
        return None

    image = pygame.image.load(path).convert()
    image.set_colorkey(colorkey)

    original_width, original_height = image.get_size()

    scale = min(
        target_size / original_width,
        target_size / original_height
    )

    new_width = max(1, int(original_width * scale))
    new_height = max(1, int(original_height * scale))

    scaled = pygame.transform.smoothscale(image, (new_width, new_height))

    result = pygame.Surface((target_size, target_size), pygame.SRCALPHA)

    x = (target_size - new_width) // 2
    y = (target_size - new_height) // 2

    result.blit(scaled, (x, y))

    return result.convert_alpha()


# =========================================================
# СПРАЙТЫ РЫБ
# =========================================================

def generate_pike_style_sprite(
        length,
        width,
        body_color,
        spine_color,
        belly_color,
        fin_color,
        spot_colors,
        tail_color=(255, 165, 0),
        eye_color=(255, 255, 255),
        pupil_color=(0, 0, 0)
):
    w = max(8, int(length))
    h = max(4, int(width))

    surf = pygame.Surface((w, h), pygame.SRCALPHA)

    pygame.draw.ellipse(surf, body_color, (0, 0, w, h))

    pygame.draw.ellipse(
        surf,
        spine_color,
        pygame.Rect(0, 0, w, h // 2 + 2)
    )

    pygame.draw.ellipse(
        surf,
        belly_color,
        pygame.Rect(0, h // 2 - 2, w, h // 2 + 2)
    )

    eye_radius = max(2, int(0.09 * h))
    pupil_radius = max(1, int(0.05 * h))
    eye_x = int(0.8 * w)
    eye_y1 = int(0.35 * h)
    eye_y2 = int(0.65 * h)

    pygame.draw.circle(surf, eye_color, (eye_x, eye_y1), eye_radius)
    pygame.draw.circle(surf, eye_color, (eye_x, eye_y2), eye_radius)

    pupil_offset = int(0.2 * eye_radius)

    pygame.draw.circle(
        surf, pupil_color,
        (eye_x + pupil_offset, eye_y1), pupil_radius
    )
    pygame.draw.circle(
        surf, pupil_color,
        (eye_x + pupil_offset, eye_y2), pupil_radius
    )

    dorsal_x = int(0.2 * w)
    dorsal_w = int(0.5 * w)
    dorsal_h = max(2, int(h * 0.30))

    pygame.draw.ellipse(
        surf, fin_color,
        (dorsal_x, 0, dorsal_w, dorsal_h)
    )

    pectoral_width = max(2, int(0.08 * w))
    pectoral_height = max(2, int(0.15 * h))

    pygame.draw.ellipse(
        surf, fin_color,
        (int(0.6 * w), int(0.05 * h),
         pectoral_width, pectoral_height)
    )
    pygame.draw.ellipse(
        surf, fin_color,
        (int(0.6 * w), int(0.80 * h),
         pectoral_width, pectoral_height)
    )

    tail_width = int(0.30 * w)
    tail_height = int(0.90 * h)

    tail_x = -tail_width // 2
    tail_y = (h - tail_height) // 2

    pygame.draw.ellipse(
        surf, tail_color,
        (tail_x, tail_y, tail_width, tail_height)
    )

    if spot_colors:
        for _ in range(random.randint(3, 6)):
            cx = random.uniform(0.2, 0.8) * w
            cy = random.uniform(0.15, 0.40) * h
            rx = random.uniform(0.03, 0.09) * w
            ry = random.uniform(0.03, 0.09) * h
            color = random.choice(spot_colors)

            pygame.draw.ellipse(
                surf, color,
                (int(cx - rx / 2), int(cy - ry / 2),
                 int(rx), int(ry))
            )
            pygame.draw.ellipse(
                surf, color,
                (int(cx - rx / 2), int(h - cy - ry / 2),
                 int(rx), int(ry))
            )

        for _ in range(random.randint(2, 4)):
            cx = random.uniform(0.3, 0.7) * w
            cy = random.uniform(0.05, 0.20) * h
            rx = random.uniform(0.02, 0.06) * w
            ry = random.uniform(0.01, 0.04) * h

            pygame.draw.ellipse(
                surf, spot_colors[0],
                (int(cx - rx / 2), int(cy - ry / 2),
                 int(rx), int(ry))
            )

    return surf.convert_alpha()




# =========================================================
# ДЕТАЛЬНЫЕ STALKER / REEFBACK ИЗ ДОПОЛНИТЕЛЬНЫХ КОДОВ
# =========================================================

def _create_detailed_stalker_source():

    """

    Рисует упрощённого Сталкера в стиле Subnautica.

    Существо смотрит вправо.

    """



    length = 235

    height = 115



    surf = pygame.Surface(

        (length, height),

        pygame.SRCALPHA

    )



    cy = height // 2



    # -----------------------------------------------------

    # ХВОСТ

    # -----------------------------------------------------



    pygame.draw.polygon(

        surf,

        (130, 180, 105),

        [

            (45, cy),

            (5, cy - 35),

            (23, cy - 8),

            (3, cy + 35),

            (55, cy + 10),

        ]

    )



    # -----------------------------------------------------

    # ТЕЛО

    # -----------------------------------------------------



    pygame.draw.ellipse(

        surf,

        (117, 173, 147),

        (35, cy - 25, 140, 50)

    )



    # брюхо

    pygame.draw.ellipse(

        surf,

        (160, 194, 102),

        (50, cy, 125, 28)

    )



    # спина

    pygame.draw.ellipse(

        surf,

        (104, 143, 210),

        (45, cy - 28, 130, 30)

    )



    # -----------------------------------------------------

    # ТЁМНЫЕ ПОЛОСЫ

    # -----------------------------------------------------



    for x in (72, 88, 105, 122, 139, 154):

        pygame.draw.line(

            surf,

            (75, 66, 145),

            (x, cy - 22),

            (x + 3, cy + 16),

            5

        )



    # -----------------------------------------------------

    # СПИННЫЕ ПЛАВНИКИ

    # -----------------------------------------------------



    fins = [

        (65, 30),

        (88, 36),

        (111, 32),

        (132, 27),

        (152, 22),

        (168, 17),

    ]



    for x, size in fins:

        pygame.draw.polygon(

            surf,

            (83, 55, 157),

            [

                (x - 6, cy - 22),

                (x - 4, cy - 22 - size),

                (x + 7, cy - 28 - size),

                (x + 9, cy - 20),

            ]

        )



        pygame.draw.line(

            surf,

            (130, 80, 195),

            (x - 3, cy - 22 - size),

            (x + 6, cy - 27 - size),

            2

        )



    # -----------------------------------------------------

    # ГРУДНОЙ ПЛАВНИК

    # -----------------------------------------------------



    pygame.draw.polygon(

        surf,

        (79, 55, 157),

        [

            (125, cy + 12),

            (105, cy + 48),

            (128, cy + 39),

            (145, cy + 12),

        ]

    )



    # -----------------------------------------------------

    # ГОЛОВА

    # -----------------------------------------------------



    pygame.draw.ellipse(

        surf,

        (100, 155, 145),

        (150, cy - 23, 45, 44)

    )



    # длинная морда

    pygame.draw.polygon(

        surf,

        (101, 158, 154),

        [

            (180, cy - 15),

            (231, cy - 8),

            (231, cy + 1),

            (177, cy + 3),

        ]

    )



    # нижняя челюсть

    pygame.draw.polygon(

        surf,

        (147, 184, 103),

        [

            (177, cy + 4),

            (229, cy + 3),

            (222, cy + 15),

            (175, cy + 14),

        ]

    )



    # пасть

    pygame.draw.line(

        surf,

        (25, 35, 36),

        (179, cy + 3),

        (228, cy + 2),

        4

    )



    # -----------------------------------------------------

    # ЗУБЫ

    # -----------------------------------------------------



    for x in range(185, 227, 8):

        pygame.draw.polygon(

            surf,

            (235, 239, 220),

            [

                (x, cy),

                (x + 3, cy + 8),

                (x + 6, cy),

            ]

        )



    # -----------------------------------------------------

    # ГЛАЗ

    # -----------------------------------------------------



    pygame.draw.circle(

        surf,

        (205, 215, 110),

        (177, cy - 12),

        6

    )



    pygame.draw.circle(

        surf,

        (10, 20, 20),

        (179, cy - 12),

        3

    )



    pygame.draw.circle(

        surf,

        (240, 250, 220),

        (180, cy - 14),

        1

    )



    return surf

def _reefback_draw_polyline_tube(surface, points, outer_color, inner_color,

                       start_thickness, end_thickness):

    """Рисует мягкое щупальце / трубку из набора отрезков."""

    count = max(1, len(points) - 1)



    for i in range(count):

        t = i / max(1, count - 1)

        thick = int(start_thickness + (end_thickness - start_thickness) * t)

        a = (int(points[i][0]), int(points[i][1]))

        b = (int(points[i + 1][0]), int(points[i + 1][1]))



        pygame.draw.line(surface, outer_color, a, b, max(1, thick + 4))

        pygame.draw.line(surface, inner_color, a, b, max(1, thick + 1))



        # Слабое колечко-сегментация.

        if i % 2 == 0:

            mx = int((a[0] + b[0]) * 0.5)

            my = int((a[1] + b[1]) * 0.5)

            pygame.draw.circle(surface, (150, 165, 160), (mx, my), max(1, thick // 3), 1)

def _reefback_draw_coral_tuft(surface, x, y, radius, base_color, tip_color, seed):

    """Небольшой кустик коралла."""

    rng = random.Random(seed)



    for _ in range(55):

        ang = rng.uniform(0, math.tau)

        length = rng.uniform(radius * 0.35, radius)

        bend = rng.uniform(-0.45, 0.45)



        x2 = x + math.cos(ang) * length

        y2 = y + math.sin(ang) * length

        x3 = x2 + math.cos(ang + bend) * length * 0.25

        y3 = y2 + math.sin(ang + bend) * length * 0.25



        pygame.draw.line(

            surface,

            base_color,

            (int(x), int(y)),

            (int(x2), int(y2)),

            rng.randint(1, 3)

        )



        pygame.draw.line(

            surface,

            tip_color,

            (int(x2), int(y2)),

            (int(x3), int(y3)),

            1

        )



        pygame.draw.circle(

            surface,

            tip_color,

            (int(x3), int(y3)),

            1

        )

def _reefback_draw_lumpy_plate(surface, rect, base_color, top_color, shadow_color, seed=0):

    """Островообразный бугор / пластина на спине Reefback."""

    x, y, w, h = rect

    rng = random.Random(seed)



    pygame.draw.ellipse(surface, shadow_color, (x - 5, y + 4, w + 10, h + 8))

    pygame.draw.ellipse(surface, base_color, rect)

    pygame.draw.ellipse(surface, top_color, (x + 8, y + 6, w - 16, h - 12))



    # Неровные доли поверхности.

    lobes = []

    cols = max(2, int(w / 55))

    rows = max(2, int(h / 38))



    for row in range(rows):

        for col in range(cols):

            px = x + 25 + col * (w - 50) / max(1, cols - 1) + rng.uniform(-8, 8)

            py = y + 18 + row * (h - 36) / max(1, rows - 1) + rng.uniform(-6, 6)

            rw = rng.uniform(18, 34)

            rh = rng.uniform(12, 24)

            lobes.append((px, py, rw, rh))



    for px, py, rw, rh in lobes:

        pygame.draw.ellipse(

            surface,

            (120, 150, 144),

            (int(px - rw / 2), int(py - rh / 2), int(rw), int(rh))

        )

        pygame.draw.ellipse(

            surface,

            (88, 112, 111),

            (int(px - rw / 2), int(py - rh / 2), int(rw), int(rh)),

            1

        )



    # Мелкие ямки / бугорки.

    for _ in range(int(w * h / 2500)):

        px = rng.randint(x + 12, x + w - 12)

        py = rng.randint(y + 12, y + h - 12)

        r = rng.randint(3, 7)

        pygame.draw.circle(surface, (90, 108, 110), (px, py), r)

        pygame.draw.circle(surface, (132, 150, 150), (px - 1, py - 1), max(1, r - 2), 1)



    # Редкие фиолетовые пятна.

    for _ in range(10):

        px = rng.randint(x + 12, x + w - 12)

        py = rng.randint(y + 12, y + h - 12)

        r = rng.randint(4, 8)

        pygame.draw.circle(surface, (92, 78, 138), (px, py), r, 1)



    return lobes

def _reefback_draw_glow_orb(surface, x, y, r, outer, inner):

    glow = pygame.Surface((r * 6, r * 6), pygame.SRCALPHA)

    gx = glow.get_width() // 2

    gy = glow.get_height() // 2



    pygame.draw.circle(glow, (*outer, 40), (gx, gy), r * 2)

    pygame.draw.circle(glow, (*outer, 80), (gx, gy), int(r * 1.4))

    pygame.draw.circle(glow, inner, (gx, gy), r)



    surface.blit(glow, (x - gx, y - gy))

def _create_detailed_reefback_source():

    """

    Статичный детальный Reefback, ориентированный головой вправо,

    щупальцами влево. Выполнен целиком из фигур pygame.

    """



    W = 1280

    H = 760

    surf = pygame.Surface((W, H), pygame.SRCALPHA)



    cx = 770

    cy = 385



    # -----------------------------------------------------

    # БИОЛЮМИНЕСЦЕНТНЫЙ НИЖНИЙ СИЛУЭТ / ОСНОВНОЕ МЯГКОЕ ТЕЛО

    # -----------------------------------------------------



    # Слабое внешнее свечение.

    for inflate, alpha in [(90, 20), (60, 28), (30, 38)]:

        glow = pygame.Surface((W, H), pygame.SRCALPHA)

        pygame.draw.ellipse(

            glow,

            (72, 110, 180, alpha),

            (

                cx - 300 - inflate // 2,

                cy - 220 - inflate // 2,

                600 + inflate,

                440 + inflate

            )

        )

        surf.blit(glow, (0, 0))



    # Базовые бугры тела.

    body_lobes = [

        (cx - 235, cy - 155, 220, 175),

        (cx - 70,  cy - 220, 255, 190),

        (cx + 100, cy - 160, 260, 190),

        (cx + 200, cy + 5,   230, 180),

        (cx + 45,  cy + 115, 270, 175),

        (cx - 170, cy + 110, 240, 180),

        (cx - 290, cy + 5,   215, 175),

        (cx - 105, cy - 20,  370, 245),

    ]



    for rect in body_lobes:

        pygame.draw.ellipse(surf, (72, 90, 172), rect)



    # Текстурные "соты".

    rng = random.Random(42)

    for _ in range(1500):

        ang = rng.uniform(0, math.tau)

        rad = rng.uniform(0, 1) ** 0.7

        rx = 300 * rad

        ry = 220 * rad

        px = int(cx + math.cos(ang) * rx + rng.uniform(-22, 22))

        py = int(cy + math.sin(ang) * ry + rng.uniform(-16, 16))

        r = rng.randint(4, 8)

        col = rng.choice([

            (90, 108, 190),

            (95, 105, 182),

            (82, 100, 170),

            (78, 104, 164),

        ])

        pygame.draw.circle(surf, col, (px, py), r)

        pygame.draw.circle(surf, (112, 129, 210), (px, py), r, 1)



    # Биолюминесцентные точки на теле.

    glow_points = [

        (cx - 250, cy - 145, 4, (60, 170, 220), (160, 255, 255, 255)),

        (cx - 95, cy - 195, 3, (60, 170, 220), (140, 255, 240, 255)),

        (cx + 35, cy - 138, 4, (60, 140, 255), (180, 235, 255, 255)),

        (cx + 245, cy - 85, 5, (255, 90, 80), (255, 165, 120, 255)),

        (cx + 205, cy + 130, 3, (120, 170, 255), (200, 240, 255, 255)),

        (cx - 95, cy + 175, 4, (255, 120, 170), (255, 200, 220, 255)),

        (cx - 180, cy + 35, 4, (60, 255, 180), (190, 255, 220, 255)),

    ]



    for x, y, r, outer, inner in glow_points:

        _reefback_draw_glow_orb(surf, x, y, r, outer, inner)



    # -----------------------------------------------------

    # ДЛИННЫЕ ЩУПАЛЬЦА

    # -----------------------------------------------------



    tentacle_roots = [

        (cx - 315, cy - 42),

        (cx - 360, cy + 15),

        (cx - 328, cy + 132),

    ]



    tentacle_lengths = [470, 690, 420]

    tentacle_offsets = [(-1.6, -10), (0.25, 8), (1.1, 7)]



    for idx, (root_x, root_y) in enumerate(tentacle_roots):

        points = []

        length = tentacle_lengths[idx]

        ang, wave_y = tentacle_offsets[idx]



        for i in range(22):

            t = i / 21

            x = root_x - t * length

            y = root_y + math.sin(t * math.pi * 1.6 + ang) * 8 + wave_y * t

            points.append((x, y))



        _reefback_draw_polyline_tube(

            surf,

            points,

            (86, 102, 100),

            (122, 136, 132),

            start_thickness=18,

            end_thickness=6

        )



    # -----------------------------------------------------

    # ПЛАСТИНЫ-ОСТРОВА НА СПИНЕ

    # -----------------------------------------------------



    plate_specs = [

        ((510, 110, 285, 180), 10),

        ((725, 70,  280, 195), 20),

        ((938, 135, 230, 172), 30),

        ((500, 300, 320, 220), 40),

        ((875, 295, 300, 215), 50),

        ((660, 495, 305, 190), 60),

        ((943, 472, 230, 170), 70),

    ]



    all_lobes = []

    for rect, seed in plate_specs:

        lobes = _reefback_draw_lumpy_plate(

            surf,

            rect,

            base_color=(78, 104, 109),

            top_color=(114, 146, 143),

            shadow_color=(55, 74, 77),

            seed=seed

        )

        all_lobes.extend(lobes)



    # -----------------------------------------------------

    # КОРАЛЛЫ НА ГРАНИЦАХ ПЛАСТИН

    # -----------------------------------------------------



    coral_clusters = [

        (605, 145, 48, (103, 65, 40), (158, 111, 73), 101),

        (860, 120, 58, (103, 65, 40), (158, 111, 73), 102),

        (1005, 200, 52, (103, 65, 40), (158, 111, 73), 103),



        (530, 380, 54, (103, 65, 40), (158, 111, 73), 104),

        (675, 440, 50, (103, 65, 40), (158, 111, 73), 105),

        (960, 390, 56, (103, 65, 40), (158, 111, 73), 106),

        (1090, 430, 52, (103, 65, 40), (158, 111, 73), 107),



        (740, 560, 52, (103, 65, 40), (158, 111, 73), 108),

        (1080, 540, 48, (103, 65, 40), (158, 111, 73), 109),



        (548, 610, 44, (120, 83, 55), (170, 120, 80), 110),

        (1160, 245, 46, (120, 83, 55), (170, 120, 80), 111),

        (1170, 115, 46, (120, 83, 55), (170, 120, 80), 112),

    ]



    for x, y, r, base_col, tip_col, seed in coral_clusters:

        _reefback_draw_coral_tuft(surf, x, y, r, base_col, tip_col, seed)



    # -----------------------------------------------------

    # МАЛЫЕ МОРСКИЕ ОРГАНИЗМЫ / АНЕМОНЫ / ЗВЁЗДЫ

    # -----------------------------------------------------



    # Красные анемоны.

    anemones = [

        (724, 168, 16),

        (788, 180, 10),

        (1032, 320, 12),

        (1097, 438, 13),

        (618, 430, 10),

    ]



    for x, y, r in anemones:

        for i in range(14):

            a = i / 14 * math.tau

            x2 = x + math.cos(a) * (r + 6)

            y2 = y + math.sin(a) * (r + 6)

            pygame.draw.line(surf, (182, 56, 65), (x, y), (x2, y2), 2)

        pygame.draw.circle(surf, (224, 122, 112), (x, y), r)

        pygame.draw.circle(surf, (110, 40, 50), (x, y), max(2, r // 3))



    # Зелёные кустики.

    for x, y, r in [(654, 387, 18), (878, 146, 14), (932, 545, 13)]:

        for i in range(18):

            a = i / 18 * math.tau

            x2 = x + math.cos(a) * (r + 5)

            y2 = y + math.sin(a) * (r + 5)

            pygame.draw.line(surf, (88, 132, 72), (x, y), (x2, y2), 2)

        pygame.draw.circle(surf, (132, 162, 86), (x, y), max(4, r - 8))



    # Маленькие звёзды/споры.

    for x, y in [(730, 408), (547, 354), (1037, 560), (900, 275), (616, 520)]:

        for i in range(5):

            a = i / 5 * math.tau

            x2 = x + math.cos(a) * 11

            y2 = y + math.sin(a) * 11

            pygame.draw.line(surf, (78, 184, 134), (x, y), (x2, y2), 2)

        pygame.draw.circle(surf, (178, 244, 190), (x, y), 2)



    # -----------------------------------------------------

    # ДОПОЛНИТЕЛЬНАЯ ДЕТАЛИЗАЦИЯ

    # -----------------------------------------------------



    # Синие овальные пятна на мягком теле по краям.

    edge_bumps = [

        (496, 212, 34, 22),

        (1095, 174, 38, 26),

        (1108, 565, 44, 28),

        (642, 620, 48, 32),

        (478, 500, 38, 28),

    ]

    for x, y, w, h in edge_bumps:

        pygame.draw.ellipse(surf, (89, 110, 184), (x, y, w, h))

        pygame.draw.ellipse(surf, (112, 137, 198), (x + 5, y + 4, w - 10, h - 8), 2)



    # Тени от пластин для объёма.

    shade = pygame.Surface((W, H), pygame.SRCALPHA)

    for rect, _ in plate_specs:

        x, y, w, h = rect

        pygame.draw.ellipse(shade, (0, 0, 0, 24), (x + 6, y + h - 8, w - 10, 26))

    surf.blit(shade, (0, 0))



    return surf

def _scale_detailed_creature_to_game_size(source, length, width):
    """Fit a detailed high-resolution creature into the original game footprint.

    The AnimalType fish_length/fish_width values stay untouched.  The output
    canvas also uses the same dimensions as the old procedural fauna renderer,
    so rotation, centering and collision/gameplay code continue to work exactly
    as before.
    """
    length = max(12, int(length))
    width = max(6, int(width))

    margin = max(6, int(max(length, width) * 0.18))
    surf_w = length + margin * 2
    surf_h = max(width * 3, width + margin * 2)

    result = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)

    # Scale the complete detailed sprite to the same nominal visual footprint
    # that was configured in the original game (fish_length x fish_width).
    scaled = pygame.transform.smoothscale(source, (length, width))
    result.blit(
        scaled,
        (margin, (surf_h - width) // 2)
    )

    return result.convert_alpha()


def generate_detailed_stalker_sprite(length, width):
    return _scale_detailed_creature_to_game_size(
        _create_detailed_stalker_source(), length, width
    )


def generate_detailed_reefback_sprite(length, width):
    return _scale_detailed_creature_to_game_size(
        _create_detailed_reefback_source(), length, width
    )


def _create_detailed_sea_treader_source():
    """Высокодетализированный морской топтун с длинными боковыми отростками."""
    W, H = 1200, 700
    surf = pygame.Surface((W, H), pygame.SRCALPHA)

    BODY_BLUE = (66, 132, 196)
    BODY_BLUE_2 = (85, 160, 220)
    BODY_DARK = (18, 40, 78)
    BODY_HIGHLIGHT = (145, 205, 255)

    ORANGE = (235, 153, 95)
    ORANGE_LIGHT = (250, 198, 145)
    CREAM = (242, 222, 190)
    DARK_BROWN = (88, 54, 36)

    LEG_BLUE = (75, 150, 220)
    LEG_LIGHT = (130, 200, 255)

    HORN_DARK = (36, 74, 112)
    HORN_LIGHT = (72, 123, 170)

    NECK_LIGHT = (222, 183, 110)
    NECK_DARK = (120, 84, 40)

    RED_GLOW = (255, 80, 50)

    def bezier(points, steps=40):
        result = []
        n = len(points) - 1
        for i in range(steps + 1):
            t = i / steps
            x = 0.0
            y = 0.0
            for k, p in enumerate(points):
                c = math.comb(n, k)
                b = c * ((1 - t) ** (n - k)) * (t ** k)
                x += b * p[0]
                y += b * p[1]
            result.append((int(x), int(y)))
        return result

    def draw_glow_line(surface, pts, color, width=2, glow=8):
        for i in range(glow, 0, -2):
            alpha = max(12, 80 - i * 8)
            pygame.draw.lines(surface, (*color, alpha), False, pts, width + i)
        pygame.draw.lines(surface, (*color, 230), False, pts, width)

    def draw_glow_circle(surface, pos, radius, color):
        x, y = pos
        for extra, alpha in ((12, 18), (7, 40), (3, 75)):
            pygame.draw.circle(surface, (*color, alpha), (int(x), int(y)), radius + extra)
        pygame.draw.circle(surface, (*color, 220), (int(x), int(y)), radius)

    def draw_rotated_ellipse(surface, color, center, size, angle, width=0, alpha=255):
        temp = pygame.Surface((size[0] + 20, size[1] + 20), pygame.SRCALPHA)
        pygame.draw.ellipse(temp, (*color, alpha), (10, 10, size[0], size[1]), width)
        rot = pygame.transform.rotate(temp, angle)
        rect = rot.get_rect(center=center)
        surface.blit(rot, rect)

    def draw_edge_growths(surface, cx, cy, left=True):
        sign = -1 if left else 1
        base_x = cx + sign * 118
        top_y = cy - 84

        pts = [
            (base_x - sign * 58, top_y + 10),
            (base_x - sign * 34, top_y - 20),
            (base_x - sign * 5, top_y - 28),
            (base_x + sign * 18, top_y - 18),
            (base_x + sign * 42, top_y + 10),
            (base_x + sign * 55, top_y + 42),
            (base_x + sign * 45, top_y + 70),
            (base_x + sign * 25, top_y + 56),
            (base_x + sign * 5, top_y + 36),
            (base_x - sign * 16, top_y + 25),
            (base_x - sign * 38, top_y + 28),
        ]
        pygame.draw.polygon(surface, (*CREAM, 210), pts)

        for shift in (0, 1):
            line_pts = [
                (base_x - sign * 50, top_y + 8 + shift),
                (base_x - sign * 28, top_y - 12 + shift),
                (base_x + sign * 2, top_y - 20 + shift),
                (base_x + sign * 28, top_y - 2 + shift),
                (base_x + sign * 46, top_y + 22 + shift),
                (base_x + sign * 40, top_y + 52 + shift),
            ]
            draw_glow_line(surface, line_pts, ORANGE, 2, glow=4)

        inner_sets = [
            [
                (base_x - sign * 35, top_y + 18),
                (base_x - sign * 18, top_y + 4),
                (base_x - sign * 8, top_y - 5),
                (base_x + sign * 8, top_y - 15),
            ],
            [
                (base_x - sign * 15, top_y + 24),
                (base_x + sign * 2, top_y + 7),
                (base_x + sign * 17, top_y - 7),
                (base_x + sign * 30, top_y + 6),
            ],
            [
                (base_x + sign * 2, top_y + 30),
                (base_x + sign * 16, top_y + 16),
                (base_x + sign * 32, top_y + 12),
                (base_x + sign * 42, top_y + 28),
            ],
        ]
        for segment in inner_sets:
            draw_glow_line(surface, segment, ORANGE_LIGHT, 1, glow=2)

    def draw_body(surface, cx, cy):
        for r_add, alpha in ((40, 20), (26, 30), (14, 44)):
            draw_rotated_ellipse(
                surface, RED_GLOW, (cx + 30, cy),
                (360 + r_add, 240 + r_add), -3, width=0, alpha=alpha
            )

        draw_rotated_ellipse(surface, BODY_BLUE, (cx + 30, cy), (340, 220), -3, 0, 245)
        draw_rotated_ellipse(surface, BODY_BLUE_2, (cx + 18, cy), (270, 170), -6, 0, 120)
        draw_rotated_ellipse(surface, BODY_DARK, (cx + 36, cy + 18), (330, 210), -3, 4, 140)
        draw_rotated_ellipse(surface, BODY_HIGHLIGHT, (cx + 45, cy + 5), (135, 92), -8, 0, 65)

        draw_edge_growths(surface, cx, cy, left=True)
        draw_edge_growths(surface, cx, cy, left=False)

        spots = [
            (cx - 55, cy - 42, 16, 7, -18),
            (cx - 25, cy - 20, 12, 5, 15),
            (cx + 12, cy + 12, 11, 5, -20),
            (cx - 5, cy + 52, 14, 5, 7),
            (cx + 76, cy - 28, 12, 4, -14),
            (cx + 105, cy + 20, 10, 4, 11),
            (cx - 96, cy + 35, 10, 4, 25),
        ]
        for sx, sy, w, h, ang in spots:
            draw_rotated_ellipse(surface, (236, 240, 247), (sx, sy), (w, h), ang, 0, 120)

        draw_rotated_ellipse(surface, (180, 230, 255), (cx + 28, cy), (342, 222), -3, 2, 70)

    def draw_horns(surface, cx, cy):
        horn_data = [
            ((cx + 182, cy - 34), (118, 34), -8),
            ((cx + 184, cy + 36), (120, 34), 7),
        ]
        for center, size, angle in horn_data:
            draw_rotated_ellipse(surface, HORN_DARK, center, size, angle, 0, 245)
            draw_rotated_ellipse(surface, HORN_LIGHT, (center[0] - 12, center[1]), (74, 18), angle, 0, 80)
            draw_rotated_ellipse(surface, (130, 190, 235), center, size, angle, 2, 80)

    def draw_side_appendages(surface, cx, cy):
        top_pts = bezier([
            (cx - 126, cy - 75),
            (cx - 270, cy - 138),
            (cx - 485, cy - 120),
            (cx - 735, cy - 183)
        ], 50)

        bottom_pts = bezier([
            (cx - 128, cy + 78),
            (cx - 275, cy + 140),
            (cx - 497, cy + 128),
            (cx - 734, cy + 183)
        ], 50)

        draw_glow_line(surface, top_pts, LEG_BLUE, 8, glow=6)
        draw_glow_line(surface, bottom_pts, LEG_BLUE, 8, glow=6)
        draw_glow_line(surface, top_pts, LEG_LIGHT, 2, glow=2)
        draw_glow_line(surface, bottom_pts, LEG_LIGHT, 2, glow=2)

        draw_rotated_ellipse(surface, LEG_BLUE, (cx - 748, cy - 186), (74, 26), -10, 0, 240)
        draw_rotated_ellipse(surface, LEG_BLUE, (cx - 748, cy + 187), (74, 26), 10, 0, 240)
        draw_rotated_ellipse(surface, LEG_LIGHT, (cx - 748, cy - 186), (44, 10), -10, 0, 90)
        draw_rotated_ellipse(surface, LEG_LIGHT, (cx - 748, cy + 187), (44, 10), 10, 0, 90)

    def draw_neck_and_head(surface, cx, cy):
        draw_rotated_ellipse(surface, NECK_DARK, (cx - 150, cy), (88, 48), 0, 0, 255)
        draw_rotated_ellipse(surface, NECK_LIGHT, (cx - 165, cy), (95, 34), 0, 0, 220)

        rings = [
            (cx - 190, cy, 44, 30),
            (cx - 212, cy, 38, 26),
            (cx - 232, cy, 35, 23),
        ]
        for x, y, w, h in rings:
            draw_rotated_ellipse(surface, NECK_LIGHT, (x, y), (w, h), 0, 0, 235)
            draw_rotated_ellipse(surface, DARK_BROWN, (x, y), (w, h), 0, 2, 90)

        spots = [
            (cx - 201, cy - 6),
            (cx - 214, cy + 8),
            (cx - 229, cy - 5),
            (cx - 240, cy + 7),
            (cx - 174, cy + 3),
            (cx - 185, cy - 8),
        ]
        for x, y in spots:
            draw_rotated_ellipse(surface, (150, 100, 45), (x, y), (8, 4), 10, 0, 180)

        draw_rotated_ellipse(surface, BODY_DARK, (cx - 110, cy), (50, 44), 0, 0, 250)
        draw_rotated_ellipse(surface, (210, 225, 245), (cx - 110, cy), (22, 26), 0, 0, 180)

    cx, cy = 760, 350
    draw_side_appendages(surf, cx, cy)
    draw_neck_and_head(surf, cx, cy)
    draw_body(surf, cx, cy)
    draw_horns(surf, cx, cy)
    draw_glow_circle(surf, (cx + 30, cy), 12, (180, 220, 255))

    return surf


def generate_detailed_sea_treader_sprite(length, width):
    return _scale_detailed_creature_to_game_size(
        _create_detailed_sea_treader_source(), length, width
    )


# =========================================================
# ПРИЗРАЧНЫЙ ЛЕВИАФАН
# =========================================================

def generate_ghost_leviathan_sprite(length=280, body_width=44):
    """Улучшенный призрачный левиафан с длинными боковыми отростками у головы."""
    margin = max(45, int(length * 0.22))

    surf_width = int(length) + margin * 2
    surf_height = max(180, int(body_width * 4.2)) + margin
    surf = pygame.Surface((surf_width, surf_height), pygame.SRCALPHA)

    start_x = margin
    center_y = surf_height // 2
    points_count = 72

    def bezier(points, steps=36):
        result = []
        n = len(points) - 1
        for i in range(steps + 1):
            t = i / steps
            x = 0.0
            y = 0.0
            for k, p in enumerate(points):
                c = math.comb(n, k)
                b = c * ((1 - t) ** (n - k)) * (t ** k)
                x += b * p[0]
                y += b * p[1]
            result.append((x, y))
        return result

    def draw_glow_polyline(points, color, width_px, glow_steps=4):
        for i in range(glow_steps, 0, -1):
            alpha = max(18, 80 - i * 14)
            pygame.draw.lines(surf, (*color, alpha), False, points, width_px + i * 2)
        pygame.draw.lines(surf, (*color, 230), False, points, width_px)

    def get_width(pos):
        head_bulge = math.exp(-((pos - 0.86) / 0.10) ** 2) * body_width * 0.40
        core = body_width * (0.12 + 0.88 * math.sin(pos * math.pi) ** 1.15)
        tail_taper = max(0.10, 1.0 - pos * 0.92)
        return max(2.2, core * tail_taper + head_bulge)

    centerline = []
    for i in range(points_count):
        pos = i / (points_count - 1)
        x = start_x + pos * length
        wave = math.sin(pos * math.pi * 1.65) * body_width * 0.12
        y = center_y + wave + math.sin(pos * math.pi * 4.4) * body_width * 0.035
        centerline.append((x, y))

    left_side = []
    right_side = []
    normals = []

    for i, (x, y) in enumerate(centerline):
        pos = i / (points_count - 1)
        width = get_width(pos)
        if i == 0:
            dx = centerline[1][0] - x
            dy = centerline[1][1] - y
        elif i == points_count - 1:
            dx = x - centerline[i - 1][0]
            dy = y - centerline[i - 1][1]
        else:
            dx = centerline[i + 1][0] - centerline[i - 1][0]
            dy = centerline[i + 1][1] - centerline[i - 1][1]

        dl = math.hypot(dx, dy) or 1.0
        dx /= dl
        dy /= dl
        px = -dy
        py = dx
        normals.append((dx, dy, px, py, width))

        left_side.append((x + px * width, y + py * width))
        right_side.append((x - px * width, y - py * width))

    polygon = left_side + right_side[::-1]
    center_x = sum(p[0] for p in polygon) / len(polygon)
    center_poly_y = sum(p[1] for p in polygon) / len(polygon)

    glow = pygame.Surface((surf_width, surf_height), pygame.SRCALPHA)
    for scale, alpha in ((2.35, 10), (1.95, 18), (1.55, 26), (1.25, 42)):
        scaled_polygon = [
            ((p[0] - center_x) * scale + center_x,
             (p[1] - center_poly_y) * scale + center_poly_y)
            for p in polygon
        ]
        pygame.draw.polygon(glow, (95, 215, 255, alpha), scaled_polygon)
    surf.blit(glow, (0, 0))

    pygame.draw.polygon(surf, (44, 112, 178, 105), polygon)
    pygame.draw.polygon(surf, (135, 225, 255, 58), polygon)
    pygame.draw.polygon(surf, (180, 245, 255, 145), polygon, 2)

    pygame.draw.lines(surf, (130, 230, 255, 140), False, centerline, max(2, int(body_width * 0.12)))
    pygame.draw.lines(surf, (235, 252, 255, 220), False, centerline, 2)

    for i in range(4, points_count - 5, 2):
        pos = i / (points_count - 1)
        x, y = centerline[i]
        dx, dy, px, py, width = normals[i]
        rib_alpha = int(90 * (1.0 - pos * 0.55))
        p1 = (x + px * width * 0.88, y + py * width * 0.88)
        p2 = (x - px * width * 0.88, y - py * width * 0.88)
        pygame.draw.line(surf, (175, 240, 255, rib_alpha), p1, p2, 1)

    for i in range(8, points_count - 12, 5):
        pos = i / (points_count - 1)
        x, y = centerline[i]
        dx, dy, px, py, width = normals[i]
        fin_length = width * (0.9 + (1.0 - pos) * 0.3)
        fin_sweep = width * 0.35
        for side in (-1, 1):
            base = (x + px * width * 0.82 * side, y + py * width * 0.82 * side)
            rear = (base[0] - dx * width * 0.28, base[1] - dy * width * 0.28)
            tip = (base[0] + px * fin_length * side + dx * fin_sweep,
                   base[1] + py * fin_length * side + dy * fin_sweep)
            pygame.draw.polygon(surf, (125, 215, 255, 72), [rear, base, tip])
            pygame.draw.polygon(surf, (210, 245, 255, 150), [rear, base, tip], 1)

    for i in range(3, points_count - 4, 3):
        x, y = centerline[i]
        _, _, px, py, width = normals[i]
        for side in (-1, 1):
            point = (x + px * width * 0.55 * side, y + py * width * 0.55 * side)
            pygame.draw.circle(surf, (155, 245, 255, 100), point, max(1, int(body_width * 0.08)))
            pygame.draw.circle(surf, (245, 255, 255, 190), point, 1)

    head_x, head_y = centerline[-1]
    _, _, head_px, head_py, head_w = normals[-1]

    head_shape = [
        (head_x + body_width * 0.92, head_y),
        (head_x + body_width * 0.58, head_y - head_w * 0.48),
        (head_x + body_width * 0.08, head_y - head_w * 0.82),
        (head_x - body_width * 0.44, head_y - head_w * 0.66),
        (head_x - body_width * 0.68, head_y - head_w * 0.18),
        (head_x - body_width * 0.68, head_y + head_w * 0.18),
        (head_x - body_width * 0.44, head_y + head_w * 0.66),
        (head_x + body_width * 0.08, head_y + head_w * 0.82),
        (head_x + body_width * 0.58, head_y + head_w * 0.48),
    ]
    pygame.draw.polygon(surf, (105, 195, 248, 175), head_shape)
    pygame.draw.polygon(surf, (215, 245, 255, 230), head_shape, 2)

    for side in (-1, 1):
        appendage = bezier([
            (head_x + body_width * 0.12, head_y + side * head_w * 0.42),
            (head_x + body_width * 0.45, head_y + side * head_w * 0.70),
            (head_x + body_width * 1.12, head_y + side * head_w * 0.88),
            (head_x + body_width * 1.72, head_y + side * head_w * 1.18),
        ], 30)
        draw_glow_polyline(appendage, (125, 225, 255), max(2, int(body_width * 0.10)), glow_steps=4)
        draw_glow_polyline(appendage, (235, 250, 255), 1, glow_steps=1)

        tip_x, tip_y = appendage[-1]
        tip_poly = [
            (tip_x - body_width * 0.14, tip_y - side * body_width * 0.08),
            (tip_x + body_width * 0.22, tip_y),
            (tip_x - body_width * 0.14, tip_y + side * body_width * 0.08),
        ]
        pygame.draw.polygon(surf, (180, 240, 255, 160), tip_poly)

    for side in (-1, 1):
        jaw = [
            (head_x - body_width * 0.10, head_y + side * head_w * 0.18),
            (head_x + body_width * 0.46, head_y + side * head_w * 0.24),
            (head_x + body_width * 0.86, head_y + side * head_w * 0.44),
            (head_x + body_width * 0.58, head_y + side * head_w * 0.18),
            (head_x + body_width * 0.08, head_y + side * head_w * 0.08),
        ]
        pygame.draw.polygon(surf, (120, 205, 255, 180), jaw)
        pygame.draw.polygon(surf, (230, 250, 255, 235), jaw, 1)

    for x_off, y_off, radius in ((0, -head_w * 0.38, max(2, int(body_width * 0.08))),
                                 (0, head_w * 0.38, max(2, int(body_width * 0.08))),
                                 (-body_width * 0.34, -head_w * 0.48, max(1, int(body_width * 0.055))),
                                 (-body_width * 0.34, head_w * 0.48, max(1, int(body_width * 0.055)))):
        ex = int(head_x + x_off)
        ey = int(head_y + y_off)
        pygame.draw.circle(surf, (70, 255, 255, 80), (ex, ey), int(radius * 2.5))
        pygame.draw.circle(surf, (135, 255, 255, 190), (ex, ey), int(radius))
        pygame.draw.circle(surf, (255, 255, 255), (ex, ey), max(1, int(radius * 0.45)))

    pygame.draw.line(
        surf, (215, 250, 255, 210),
        (int(head_x + body_width * 0.06), int(head_y)),
        (int(head_x + body_width * 0.94), int(head_y)),
        2
    )

    return surf.convert_alpha()





# =========================================================
# ДЕТАЛЬНЫЙ REAPER LEVIATHAN ИЗ ДОПОЛНИТЕЛЬНОГО КОДА
# =========================================================

def generate_detailed_reaper_sprite(length, width):
    """Новый детальный Reaper, адаптированный к прежнему игровому размеру."""
    WIDTH, HEIGHT = 1280, 480

    CYAN_DARK = (25, 115, 126)
    CYAN = (77, 188, 198)
    CYAN_LIGHT = (134, 225, 225)
    CYAN_HIGHLIGHT = (190, 245, 239)
    RED_DARK = (87, 28, 23)
    RED = (155, 55, 42)
    RED_LIGHT = (202, 76, 56)
    RED_GLOW = (226, 103, 72)
    BLACK_RED = (50, 18, 16)
    EYE = (255, 210, 120)

    def poly(surface, color, points):

        pygame.draw.polygon(surface, color, [(int(x), int(y)) for x, y in points])

    def ellipse(surface, color, rect):

        pygame.draw.ellipse(surface, color, pygame.Rect(*[int(v) for v in rect]))

    def line(surface, color, start, end, width=1):

        pygame.draw.line(surface, color, start, end, width)

    def aaline(surface, color, start, end):

        pygame.draw.aaline(surface, color, start, end)

    def thick_curve(surface, points, color, widths):

        """Ломаная с плавным визуальным переходом толщины."""

        for i in range(len(points) - 1):

            w = int((widths[i] + widths[i + 1]) / 2)

            pygame.draw.line(surface, color, points[i], points[i + 1], max(1, w))

            pygame.draw.circle(surface, color, points[i], max(1, w // 2))

        pygame.draw.circle(surface, color, points[-1], max(1, widths[-1] // 2))

    def add_body_scales(surface, x1, x2, center_y, amplitude, count=42):

        """Мелкие тёмно-красные штрихи на центральной полосе."""

        step = (x2 - x1) / count

        for i in range(count):

            x = int(x1 + i * step)

            length = 6 + (i % 4) * 2

            y = int(center_y + math.sin(i * 0.72) * amplitude)

            pygame.draw.line(surface, RED_DARK, (x, y), (x + length, y + (i % 3 - 1)), 2)

    def draw_reaper(surface):

        cy = 242



        # Тень под существом

        shadow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        ellipse(shadow, (0, 0, 0, 65), (95, cy + 56, 1010, 35))

        surface.blit(shadow, (0, 0))



        # ----------------------------- хвост ------------------------------

        # Основание хвоста

        poly(surface, CYAN_DARK, [

            (910, cy - 23), (1028, cy - 19), (1115, cy - 8),

            (1115, cy + 8), (1028, cy + 21), (910, cy + 24)

        ])

        poly(surface, CYAN, [

            (905, cy - 18), (1025, cy - 14), (1112, cy - 5),

            (1112, cy + 5), (1025, cy + 15), (905, cy + 18)

        ])



        # Развилка хвоста

        poly(surface, CYAN_DARK, [

            (1102, cy), (1188, 121), (1218, 93), (1197, 142),

            (1146, cy - 6), (1108, cy - 1)

        ])

        poly(surface, RED_DARK, [

            (1188, 121), (1218, 93), (1203, 132), (1191, 149)

        ])

        poly(surface, CYAN, [

            (1105, cy), (1183, 128), (1208, 102), (1191, 139),

            (1144, cy - 4)

        ])



        poly(surface, CYAN_DARK, [

            (1102, cy), (1185, 357), (1217, 386), (1195, 338),

            (1146, cy + 7), (1108, cy + 1)

        ])

        poly(surface, RED_DARK, [

            (1185, 357), (1217, 386), (1200, 347), (1189, 331)

        ])

        poly(surface, CYAN, [

            (1105, cy), (1181, 351), (1207, 377), (1190, 339),

            (1144, cy + 4)

        ])



        # Малые хвостовые плавники

        poly(surface, CYAN_DARK, [

            (983, cy - 12), (955, 184), (944, 155), (960, 173),

            (994, cy - 4)

        ])

        poly(surface, RED_DARK, [

            (955, 184), (944, 155), (957, 169), (968, 197)

        ])

        poly(surface, CYAN, [

            (983, cy - 8), (958, 188), (949, 165), (963, 180),

            (992, cy - 3)

        ])



        poly(surface, CYAN_DARK, [

            (983, cy + 12), (956, 299), (947, 323), (962, 308),

            (994, cy + 4)

        ])

        poly(surface, RED_DARK, [

            (956, 299), (947, 323), (960, 309), (969, 286)

        ])

        poly(surface, CYAN, [

            (983, cy + 8), (959, 296), (952, 315), (965, 303),

            (992, cy + 3)

        ])



        # ----------------------------- тело -------------------------------

        # Нижний тёмный контур

        body_outer = [

            (165, 214), (240, 190), (380, 184), (540, 189),

            (690, 198), (835, 207), (950, 218), (1035, 231),

            (1075, 238), (1035, 251), (950, 263), (835, 273),

            (690, 282), (540, 290), (380, 294), (240, 289), (165, 270)

        ]

        poly(surface, CYAN_DARK, body_outer)



        body_inner = [

            (171, 219), (245, 198), (380, 194), (540, 198),

            (690, 207), (835, 215), (950, 224), (1035, 235),

            (1065, 242), (1035, 247), (950, 257), (835, 265),

            (690, 274), (540, 281), (380, 285), (245, 280), (171, 265)

        ]

        poly(surface, CYAN, body_inner)



        # Верхний голубой блик

        poly(surface, CYAN_LIGHT, [

            (187, 218), (255, 203), (387, 201), (536, 205), (684, 213),

            (824, 221), (936, 230), (1005, 236), (1016, 240),

            (937, 238), (823, 232), (683, 225), (535, 216), (386, 211),

            (257, 212), (190, 227)

        ])



        # Светлый край брюшной части

        poly(surface, (111, 208, 210), [

            (176, 258), (250, 272), (385, 277), (541, 273), (690, 266),

            (836, 257), (949, 249), (1022, 243), (1035, 247),

            (950, 257), (835, 265), (690, 274), (540, 281),

            (380, 285), (245, 280), (171, 265)

        ])



        # Красная центральная полоса

        stripe = [

            (164, 228), (245, 216), (360, 216), (480, 220),

            (600, 225), (720, 229), (835, 231), (940, 234),

            (1025, 238), (1047, 241), (1024, 246), (940, 248),

            (835, 250), (720, 253), (600, 256), (480, 259),

            (360, 261), (245, 260), (165, 252)

        ]

        poly(surface, RED_DARK, stripe)



        stripe2 = [

            (170, 231), (247, 220), (360, 220), (480, 225),

            (600, 230), (720, 234), (835, 236), (940, 238),

            (1020, 241), (1038, 242), (1020, 244), (940, 245),

            (835, 247), (720, 249), (600, 252), (480, 255),

            (360, 257), (247, 256), (170, 249)

        ]

        poly(surface, RED, stripe2)

        add_body_scales(surface, 280, 940, 242, 4, 50)



        # Разрывы/светлые пятна в полосе

        for x, w in [(350, 17), (512, 12), (650, 22), (776, 11), (878, 16), (935, 9)]:

            poly(surface, CYAN_LIGHT, [

                (x, cy - 9), (x + w, cy - 7), (x + w - 2, cy + 8), (x - 2, cy + 7)

            ])



        # ---------------------- боковые плавники --------------------------

        # Передний верхний плавник

        poly(surface, CYAN_DARK, [

            (246, 207), (337, 103), (365, 86), (341, 121), (280, 220)

        ])

        poly(surface, CYAN, [

            (250, 210), (337, 111), (355, 99), (337, 126), (278, 218)

        ])

        poly(surface, RED_DARK, [

            (337, 111), (365, 86), (344, 118), (333, 130)

        ])



        # Передний нижний плавник

        poly(surface, CYAN_DARK, [

            (245, 274), (320, 363), (353, 376), (331, 349), (280, 263)

        ])

        poly(surface, CYAN, [

            (250, 271), (319, 355), (342, 367), (326, 344), (278, 265)

        ])

        poly(surface, RED_DARK, [

            (319, 355), (353, 376), (329, 346), (317, 339)

        ])



        # ------------------------------ голова ----------------------------

        # Морда

        poly(surface, CYAN_DARK, [

            (118, 224), (164, 210), (199, 215), (221, 229),

            (219, 254), (198, 269), (161, 272), (116, 258),

            (78, 249), (66, 241), (79, 233)

        ])

        poly(surface, CYAN, [

            (120, 229), (164, 217), (194, 221), (211, 232),

            (210, 251), (193, 263), (160, 265), (119, 255),

            (85, 248), (73, 241), (86, 236)

        ])

        poly(surface, CYAN_LIGHT, [

            (123, 229), (163, 220), (190, 224), (201, 231),

            (178, 232), (146, 235), (112, 238), (84, 241), (92, 236)

        ])



        # Красная маска на голове

        poly(surface, RED_DARK, [

            (92, 234), (143, 220), (181, 224), (204, 235),

            (199, 252), (177, 260), (140, 257), (95, 249)

        ])

        poly(surface, RED, [

            (101, 235), (144, 225), (176, 228), (195, 237),

            (191, 248), (174, 254), (141, 252), (102, 247)

        ])



        # Глаза

        ellipse(surface, BLACK_RED, (135, 229, 16, 10))

        ellipse(surface, EYE, (139, 231, 7, 5))

        ellipse(surface, BLACK_RED, (135, 246, 16, 10))

        ellipse(surface, EYE, (139, 248, 7, 5))



        # Носовой шип/ротовая часть

        poly(surface, RED_DARK, [

            (87, 236), (35, 230), (12, 238), (34, 246), (88, 247)

        ])

        poly(surface, RED, [

            (86, 238), (39, 234), (20, 239), (39, 243), (88, 245)

        ])



        # ------------------------ четыре мандибулы ------------------------

        # Каждая щупальцеобразная челюсть строится из толстых сегментов

        # и заканчивается тёмным крючком.



        # Верхняя левая

        pts = [(155, 225), (139, 178), (136, 127), (145, 78), (159, 41)]

        widths = [15, 18, 21, 24, 26]

        thick_curve(surface, pts, RED_DARK, [w + 5 for w in widths])

        thick_curve(surface, pts, RED, widths)

        pygame.draw.arc(surface, BLACK_RED, (121, 27, 46, 88), math.radians(105), math.radians(250), 8)

        aaline(surface, RED_GLOW, (148, 173), (150, 82))



        # Верхняя правая

        pts = [(174, 226), (185, 177), (190, 126), (191, 80), (181, 51)]

        widths = [15, 18, 22, 24, 25]

        thick_curve(surface, pts, RED_DARK, [w + 5 for w in widths])

        thick_curve(surface, pts, RED, widths)

        pygame.draw.arc(surface, BLACK_RED, (166, 39, 42, 77), math.radians(286), math.radians(88), 8)

        aaline(surface, RED_GLOW, (180, 175), (188, 83))



        # Нижняя левая

        pts = [(154, 256), (139, 300), (134, 344), (141, 390), (156, 422)]

        widths = [15, 18, 21, 24, 25]

        thick_curve(surface, pts, RED_DARK, [w + 5 for w in widths])

        thick_curve(surface, pts, RED, widths)

        pygame.draw.arc(surface, BLACK_RED, (119, 372, 48, 76), math.radians(105), math.radians(250), 8)

        aaline(surface, RED_GLOW, (148, 306), (149, 390))



        # Нижняя правая

        pts = [(176, 256), (190, 298), (196, 338), (196, 383), (184, 414)]

        widths = [15, 18, 22, 24, 24]

        thick_curve(surface, pts, RED_DARK, [w + 5 for w in widths])

        thick_curve(surface, pts, RED, widths)

        pygame.draw.arc(surface, BLACK_RED, (169, 369, 43, 73), math.radians(280), math.radians(82), 8)

        aaline(surface, RED_GLOW, (185, 303), (192, 380))



        # Голубые сочленения у основания мандибул

        for rect in [(145, 212, 20, 27), (168, 211, 20, 28), (145, 247, 20, 27), (169, 247, 20, 28)]:

            ellipse(surface, CYAN_LIGHT, rect)



        # Красные продольные детали возле шеи

        pygame.draw.line(surface, RED_LIGHT, (187, 229), (246, 230), 5)

        pygame.draw.line(surface, RED_LIGHT, (187, 252), (246, 253), 5)



        # Небольшие складки/сегменты на голове

        for x in range(112, 188, 12):

            pygame.draw.line(surface, RED_DARK, (x, 232), (x + 2, 248), 2)



        # Световые блики на спине

        pygame.draw.aaline(surface, CYAN_HIGHLIGHT, (246, 203), (765, 216))

        pygame.draw.aaline(surface, CYAN_HIGHLIGHT, (770, 217), (1000, 235))



        # Контур снизу для большей читаемости

        pygame.draw.aaline(surface, (18, 90, 98), (244, 281), (950, 258))

    source = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    draw_reaper(source)

    # В исходной системе спрайтов все существа смотрят вправо.
    source = pygame.transform.flip(source, True, False)

    length = max(12, int(length))
    width = max(6, int(width))
    margin = max(6, int(max(length, width) * 0.18))
    target_size = (
        length + margin * 2,
        max(width * 3, width + margin * 2)
    )
    return pygame.transform.smoothscale(source, target_size).convert_alpha()


# =========================================================
# ДЕТАЛЬНЫЙ CRABSQUID ИЗ ДОПОЛНИТЕЛЬНОГО КОДА
# =========================================================

def generate_detailed_crabsquid_sprite(length, width):
    """Новый детальный Crabsquid; визуальный масштаб увеличен примерно в 1.5 раза."""
    WIDTH, HEIGHT = 1024, 1024

    TEAL_DARK = (32, 74, 78)
    TEAL = (74, 142, 141)
    TEAL_LIGHT = (122, 200, 190)
    TEAL_GLOW = (188, 255, 235)
    OLIVE = (113, 101, 63)
    OLIVE_DARK = (72, 58, 40)
    BROWN = (106, 72, 45)
    BROWN_DARK = (63, 42, 28)
    SAND = (176, 154, 121)
    WHITE = (226, 241, 245)
    BLUE = (58, 136, 210)
    BLUE_LIGHT = (141, 208, 255)
    BLACK = (10, 18, 24)
    INK = (12, 24, 30)

    def poly(surface, color, pts, width=0):

        pygame.draw.polygon(surface, color, [(int(x), int(y)) for x, y in pts], width)

    def ellipse(surface, color, rect, width=0):

        pygame.draw.ellipse(surface, color, pygame.Rect(*[int(v) for v in rect]), width)

    def circle(surface, color, center, radius, width=0):

        pygame.draw.circle(surface, color, (int(center[0]), int(center[1])), int(radius), width)

    def draw_soft_glow(surface, center, radius, color, layers=6, alpha=26):

        glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        for i in range(layers, 0, -1):

            r = radius * (i / layers)

            a = int(alpha * (i / layers))

            pygame.draw.circle(glow, (*color, a), (int(center[0]), int(center[1])), int(r))

        surface.blit(glow, (0, 0))

    def segmented_leg(surface, points, widths, fill_color, shadow_color, highlight_color=None, claw=False):

        """Рисует сегментированную ногу/щупальце."""

        # Тень/контур

        for i in range(len(points) - 1):

            p1 = points[i]

            p2 = points[i + 1]

            w = int((widths[i] + widths[i + 1]) / 2) + 4

            pygame.draw.line(surface, shadow_color, p1, p2, max(1, w))

            circle(surface, shadow_color, p1, w // 2 + 1)



        # Основной стержень

        for i in range(len(points) - 1):

            p1 = points[i]

            p2 = points[i + 1]

            w = int((widths[i] + widths[i + 1]) / 2)

            pygame.draw.line(surface, fill_color, p1, p2, max(1, w))

            circle(surface, fill_color, p1, max(1, w // 2))

        circle(surface, fill_color, points[-1], max(1, widths[-1] // 2))



        # Сегменты/кольца

        for i, p in enumerate(points[1:-1], start=1):

            r = max(3, widths[i] // 2 + 1)

            circle(surface, BROWN_DARK, p, r + 1, 2)

            circle(surface, SAND, (p[0] - 2, p[1] - 2), max(2, r // 2))



        # Блики

        if highlight_color:

            for i in range(len(points) - 1):

                p1 = points[i]

                p2 = points[i + 1]

                pygame.draw.aaline(

                    surface,

                    highlight_color,

                    (p1[0] - 2, p1[1] - 2),

                    (p2[0] - 2, p2[1] - 2),

                )



        # Клешня на конце

        if claw:

            tip = points[-1]

            prev = points[-2]

            angle = math.atan2(tip[1] - prev[1], tip[0] - prev[0])



            spread = 0.65

            length = 34

            w = 14



            for sign in (-1, 1):

                ang = angle + sign * spread

                base = (

                    tip[0] - math.cos(angle) * 7,

                    tip[1] - math.sin(angle) * 7,

                )

                p1 = base

                p2 = (

                    base[0] + math.cos(ang) * length,

                    base[1] + math.sin(ang) * length,

                )

                side = (

                    base[0] + math.cos(ang + sign * 0.7) * w,

                    base[1] + math.sin(ang + sign * 0.7) * w,

                )

                poly(surface, WHITE, [p1, side, p2])

                poly(surface, (170, 225, 230), [p1, ((p1[0] + side[0]) / 2, (p1[1] + side[1]) / 2), p2])

    def draw_dome(surface, center):

        cx, cy = center

        dome = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)



        # Основной прозрачный купол

        ellipse(dome, (155, 185, 255, 42), (cx - 150, cy - 240, 300, 430))

        ellipse(dome, (180, 215, 255, 55), (cx - 136, cy - 224, 272, 404))

        ellipse(dome, (220, 235, 255, 36), (cx - 105, cy - 180, 210, 305))



        # Контуры

        ellipse(dome, (205, 220, 255, 70), (cx - 148, cy - 238, 296, 426), 3)

        ellipse(dome, (235, 244, 255, 40), (cx - 131, cy - 216, 262, 388), 2)



        # Вертикальные блики по бокам

        for dx in (-112, 114):

            for j in range(11):

                yy = cy - 170 + j * 26

                circle(dome, (245, 250, 255, 60), (cx + dx, yy), 2)

        # Мягкий верхний блик

        ellipse(dome, (255, 255, 255, 28), (cx - 54, cy - 210, 62, 84))



        surface.blit(dome, (0, 0))

    def draw_head(surface, center):

        cx, cy = center



        # Внутреннее тело/мантия

        poly(surface, OLIVE_DARK, [

            (cx - 72, cy - 140), (cx - 22, cy - 214), (cx + 45, cy - 188),

            (cx + 86, cy - 114), (cx + 69, cy + 14), (cx + 12, cy + 100),

            (cx - 61, cy + 24)

        ])

        poly(surface, BROWN, [

            (cx - 64, cy - 133), (cx - 18, cy - 201), (cx + 39, cy - 179),

            (cx + 76, cy - 111), (cx + 61, cy + 8), (cx + 9, cy + 89),

            (cx - 52, cy + 21)

        ])

        poly(surface, SAND, [

            (cx - 45, cy - 118), (cx - 5, cy - 180), (cx + 33, cy - 164),

            (cx + 55, cy - 101), (cx + 43, cy - 8), (cx + 6, cy + 57),

            (cx - 34, cy + 17)

        ])



        # Боковые лопасти

        poly(surface, OLIVE_DARK, [

            (cx - 66, cy - 110), (cx - 132, cy - 67), (cx - 90, cy + 55), (cx - 45, cy + 15)

        ])

        poly(surface, BROWN, [

            (cx - 60, cy - 104), (cx - 120, cy - 66), (cx - 85, cy + 42), (cx - 44, cy + 12)

        ])

        poly(surface, OLIVE_DARK, [

            (cx + 64, cy - 112), (cx + 132, cy - 68), (cx + 86, cy + 48), (cx + 41, cy + 16)

        ])

        poly(surface, BROWN, [

            (cx + 57, cy - 104), (cx + 120, cy - 67), (cx + 82, cy + 38), (cx + 40, cy + 12)

        ])



        # Светящаяся сетка на голове

        nodes = [

            (0, -180), (-18, -165), (18, -165), (-35, -147), (0, -145), (33, -145),

            (-47, -123), (-15, -121), (18, -121), (49, -120),

            (-58, -97), (-29, -95), (0, -94), (30, -94), (58, -95),

            (-54, -67), (-25, -63), (0, -62), (26, -64), (52, -67),

            (-44, -35), (-16, -30), (14, -31), (40, -35),

            (-26, -1), (0, 2), (22, -2), (-8, 30), (9, 26)

        ]

        edges = [

            (0,1),(0,2),(1,3),(1,4),(2,4),(2,5),(3,6),(3,7),(4,7),(4,8),(5,8),(5,9),

            (6,10),(6,11),(7,11),(7,12),(8,12),(8,13),(9,13),(9,14),

            (10,15),(11,16),(12,17),(13,18),(14,19),

            (15,20),(16,21),(17,22),(18,23),(19,23),

            (20,24),(21,24),(21,25),(22,25),(22,26),(23,26),(24,27),(25,27),(25,28),(26,28)

        ]

        translated = [(cx + x, cy + y) for x, y in nodes]

        glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        for a, b in edges:

            pygame.draw.line(glow, (150, 255, 215, 120), translated[a], translated[b], 3)

            pygame.draw.line(surface, TEAL_GLOW, translated[a], translated[b], 1)

        for p in translated:

            circle(glow, (170, 255, 230, 110), p, 4)

            circle(surface, (220, 255, 245), p, 1)

        surface.blit(glow, (0, 0))

    def draw_eyes(surface, center):

        cx, cy = center

        eye_positions = [(-55, 18), (40, 18), (-20, 73), (30, 82)]

        sizes = [(58, 58), (56, 56), (52, 52), (50, 50)]



        for (dx, dy), (w, h) in zip(eye_positions, sizes):

            x = cx + dx

            y = cy + dy



            # Внешнее кольцо

            ellipse(surface, BROWN_DARK, (x - w//2 - 4, y - h//2 - 4, w + 8, h + 8))

            ellipse(surface, BROWN, (x - w//2, y - h//2, w, h))

            ellipse(surface, SAND, (x - w//2 + 6, y - h//2 + 6, w - 12, h - 12))

            ellipse(surface, BLUE_LIGHT, (x - w//2 + 10, y - h//2 + 10, w - 20, h - 20))

            ellipse(surface, BLUE, (x - w//2 + 15, y - h//2 + 15, w - 30, h - 30))

            ellipse(surface, BLACK, (x - 10, y - 10, 20, 20))

            circle(surface, WHITE, (x - 7, y - 8), 3)



            # Внешний контур

            ellipse(surface, (90, 62, 40), (x - w//2, y - h//2, w, h), 2)

    def draw_mouth_and_feelers(surface, center):

        cx, cy = center



        # Ротовая часть

        poly(surface, (180, 200, 210), [

            (cx - 13, cy + 88), (cx + 10, cy + 86), (cx + 18, cy + 103),

            (cx + 6, cy + 123), (cx - 9, cy + 121), (cx - 19, cy + 102)

        ])

        poly(surface, WHITE, [

            (cx - 9, cy + 92), (cx + 6, cy + 90), (cx + 11, cy + 104),

            (cx + 2, cy + 118), (cx - 8, cy + 115), (cx - 15, cy + 101)

        ])



        # Усики/щупальца снизу

        for i, xoff in enumerate([-16, -6, 2, 12]):

            poly(surface, WHITE, [

                (cx + xoff, cy + 108),

                (cx + xoff + 3, cy + 143 + i * 4),

                (cx + xoff - 3, cy + 148 + i * 5)

            ])

    def draw_legs(surface, center):

        cx, cy = center



        # Левые длинные ноги

        segmented_leg(surface,

                      [(cx - 76, cy + 98), (cx - 145, cy + 138), (cx - 242, cy + 192), (cx - 341, cy + 276), (cx - 423, cy + 415)],

                      [18, 18, 16, 13, 10],

                      (95, 79, 58), (48, 36, 26), (210, 225, 230), claw=False)

        # Чёрный коготь

        poly(surface, INK, [(cx - 431, cy + 406), (cx - 451, cy + 445), (cx - 426, cy + 424)])



        segmented_leg(surface,

                      [(cx - 44, cy + 99), (cx - 92, cy + 164), (cx - 128, cy + 244), (cx - 161, cy + 345), (cx - 161, cy + 504)],

                      [17, 16, 14, 12, 8],

                      (95, 79, 58), (48, 36, 26), (210, 225, 230), claw=False)

        poly(surface, INK, [(cx - 168, cy + 494), (cx - 176, cy + 536), (cx - 156, cy + 505)])



        # Правая пара длинных ног

        segmented_leg(surface,

                      [(cx + 79, cy + 98), (cx + 150, cy + 138), (cx + 245, cy + 197), (cx + 326, cy + 283), (cx + 372, cy + 414)],

                      [18, 18, 16, 13, 10],

                      (95, 79, 58), (48, 36, 26), (210, 225, 230), claw=False)

        poly(surface, INK, [(cx + 367, cy + 404), (cx + 383, cy + 444), (cx + 361, cy + 420)])



        segmented_leg(surface,

                      [(cx + 34, cy + 108), (cx + 56, cy + 184), (cx + 86, cy + 281), (cx + 133, cy + 383), (cx + 163, cy + 517)],

                      [17, 15, 13, 11, 8],

                      (95, 79, 58), (48, 36, 26), (210, 225, 230), claw=False)

        poly(surface, INK, [(cx + 157, cy + 504), (cx + 172, cy + 547), (cx + 151, cy + 514)])



        # Средние опорные ноги

        segmented_leg(surface,

                      [(cx - 22, cy + 110), (cx - 46, cy + 175), (cx - 60, cy + 248), (cx - 66, cy + 322)],

                      [13, 12, 10, 8],

                      (95, 79, 58), (48, 36, 26), (210, 225, 230), claw=False)

        poly(surface, INK, [(cx - 71, cy + 313), (cx - 82, cy + 339), (cx - 61, cy + 321)])



        segmented_leg(surface,

                      [(cx + 12, cy + 112), (cx + 22, cy + 188), (cx + 30, cy + 261), (cx + 45, cy + 336)],

                      [13, 12, 10, 8],

                      (95, 79, 58), (48, 36, 26), (210, 225, 230), claw=False)

        poly(surface, INK, [(cx + 39, cy + 324), (cx + 50, cy + 350), (cx + 35, cy + 331)])



        # Передние маленькие клешни

        segmented_leg(surface,

                      [(cx - 5, cy + 119), (cx - 17, cy + 175), (cx - 9, cy + 231)],

                      [10, 9, 8],

                      (125, 118, 89), (53, 44, 32), (220, 240, 245), claw=True)



        segmented_leg(surface,

                      [(cx + 22, cy + 121), (cx + 35, cy + 178), (cx + 39, cy + 233)],

                      [10, 9, 8],

                      (125, 118, 89), (53, 44, 32), (220, 240, 245), claw=True)

    def draw_creature(surface):

        cx, cy = 520, 350



        # Подсветка от глаз и головы

        draw_soft_glow(surface, (cx, cy + 5), 120, (80, 180, 235), layers=7, alpha=18)

        draw_soft_glow(surface, (cx, cy - 120), 150, (70, 110, 180), layers=7, alpha=12)



        # Тень

        shadow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        ellipse(shadow, (0, 0, 0, 72), (cx - 290, cy + 500, 580, 74))

        surface.blit(shadow, (0, 0))



        # Дальние ноги сначала

        draw_legs(surface, (cx, cy))

        draw_head(surface, (cx, cy))

        draw_eyes(surface, (cx, cy))

        draw_mouth_and_feelers(surface, (cx, cy))

        draw_dome(surface, (cx, cy - 30))

    source = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    draw_creature(source)

    # Дополнительный рисунок ориентирован вверх; в игре базовое направление — вправо.
    source = pygame.transform.rotate(source, -90)

    length = max(12, int(length))
    width = max(6, int(width))
    margin = max(6, int(max(length, width) * 0.18))
    base_w = length + margin * 2
    base_h = max(width * 3, width + margin * 2)
    target_size = (
        max(1, int(round(base_w * 1.5))),
        max(1, int(round(base_h * 1.5)))
    )
    return pygame.transform.smoothscale(source, target_size).convert_alpha()




# =========================================================
# ДЕТАЛЬНЫЙ AMPEEL / ЭЛЕКТРИЧЕСКИЙ УГОРЬ ИЗ ДОПОЛНИТЕЛЬНОГО КОДА
# =========================================================

def _ampeel_add_glow(surface, pos, radius, color, strength=180):

    """Мягкое свечение."""

    radius = max(2, int(radius))



    glow = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)



    cx = radius * 2

    cy = radius * 2



    for r in range(radius * 2, 0, -3):

        k = r / (radius * 2)

        alpha = int((1 - k) * strength)



        pygame.draw.circle(

            glow,

            (*color, alpha),

            (cx, cy),

            r

        )



    surface.blit(

        glow,

        (

            int(pos[0] - cx),

            int(pos[1] - cy)

        )

    )





def _ampeel_thick_line(surface, color, start, end, width):

    pygame.draw.line(

        surface,

        color,

        (int(start[0]), int(start[1])),

        (int(end[0]), int(end[1])),

        max(1, int(width))

    )





def _ampeel_curve_points(start, control, end, segments=20):

    """Квадратичная кривая Безье."""

    pts = []



    for i in range(segments + 1):

        t = i / segments



        x = (

            (1 - t) ** 2 * start[0]

            + 2 * (1 - t) * t * control[0]

            + t ** 2 * end[0]

        )



        y = (

            (1 - t) ** 2 * start[1]

            + 2 * (1 - t) * t * control[1]

            + t ** 2 * end[1]

        )



        pts.append((int(x), int(y)))



    return pts





def _ampeel_draw_curve(surface, color, start, control, end, width):

    pts = _ampeel_curve_points(start, control, end, 24)



    if len(pts) > 1:

        pygame.draw.lines(

            surface,

            color,

            False,

            pts,

            max(1, int(width))

        )





def _ampeel_polygon_outline(surface, points, color, width=2):

    pygame.draw.polygon(surface, color, points, width)





# ------------------------------------------------------------

# ЭЛЕКТРИЧЕСКИЕ РАЗРЯДЫ

# ------------------------------------------------------------



def _ampeel_draw_lightning(surface, start, end, seed=1):

    random.seed(seed)



    x1, y1 = start

    x2, y2 = end



    points = [(x1, y1)]



    segments = 11



    dx = x2 - x1

    dy = y2 - y1



    length = math.hypot(dx, dy)



    if length == 0:

        return



    px = -dy / length

    py = dx / length



    for i in range(1, segments):

        t = i / segments



        x = x1 + dx * t

        y = y1 + dy * t



        offset = random.uniform(-12, 12)



        x += px * offset

        y += py * offset



        points.append((x, y))



    points.append((x2, y2))



    # наружное голубое свечение

    pygame.draw.lines(

        surface,

        (20, 80, 255),

        False,

        points,

        8

    )



    pygame.draw.lines(

        surface,

        (30, 180, 255),

        False,

        points,

        4

    )



    pygame.draw.lines(

        surface,

        (210, 255, 255),

        False,

        points,

        2

    )





# ------------------------------------------------------------

# УЗОР ПАНЦИРЯ

# ------------------------------------------------------------



def _ampeel_draw_armour_pattern(surface, rect, seed=0):

    random.seed(seed)



    clip_old = surface.get_clip()

    surface.set_clip(rect)



    x, y, w, h = rect



    for _ in range(14):

        cx = random.randint(x, x + w)

        cy = random.randint(y, y + h)



        rw = random.randint(9, 23)

        rh = random.randint(5, 14)



        pygame.draw.ellipse(

            surface,

            (63, 92, 72),

            (cx - rw, cy - rh, rw * 2, rh * 2),

            2

        )



        if random.random() < 0.5:

            pygame.draw.ellipse(

                surface,

                (91, 115, 86),

                (

                    cx - rw + 4,

                    cy - rh + 3,

                    max(3, rw * 2 - 8),

                    max(3, rh * 2 - 6)

                ),

                1

            )



    surface.set_clip(clip_old)





# ------------------------------------------------------------

# ОТРОСТОК

# ------------------------------------------------------------



def _ampeel_draw_tentacle(surface, base, tip, bend, scale=1.0):

    bx, by = base

    tx, ty = tip



    cx = (bx + tx) / 2 + bend[0]

    cy = (by + ty) / 2 + bend[1]



    # тёмная обводка

    _ampeel_draw_curve(

        surface,

        (45, 45, 38),

        base,

        (cx, cy),

        tip,

        12 * scale

    )



    # мясистая часть

    _ampeel_draw_curve(

        surface,

        (114, 76, 63),

        base,

        (cx, cy),

        tip,

        8 * scale

    )



    # светлая сторона

    _ampeel_draw_curve(

        surface,

        (155, 102, 90),

        base,

        (cx, cy),

        tip,

        3 * scale

    )



    # голубой кончик

    _ampeel_add_glow(

        surface,

        tip,

        22 * scale,

        (70, 255, 245),

        120

    )



    pygame.draw.circle(

        surface,

        (130, 255, 250),

        (int(tx), int(ty)),

        max(3, int(6 * scale))

    )



    pygame.draw.circle(

        surface,

        (225, 255, 255),

        (int(tx), int(ty)),

        max(2, int(3 * scale))

    )





# ------------------------------------------------------------

# ТЕЛО УГРЯ

# ------------------------------------------------------------



def _draw_detailed_electric_eel(surface, center=(700, 300), scale=1.0):



    cx, cy = center



    # Основная ось туловища

    body_start = cx - 500 * scale

    body_end = cx + 390 * scale



    # --------------------------------------------------------

    # ХВОСТ

    # --------------------------------------------------------



    tail = [

        (cx + 350 * scale, cy - 58 * scale),

        (cx + 425 * scale, cy - 68 * scale),

        (cx + 485 * scale, cy - 100 * scale),

        (cx + 535 * scale, cy - 75 * scale),

        (cx + 548 * scale, cy),

        (cx + 525 * scale, cy + 68 * scale),

        (cx + 465 * scale, cy + 83 * scale),

        (cx + 395 * scale, cy + 59 * scale),

    ]



    tail = [(int(x), int(y)) for x, y in tail]



    pygame.draw.polygon(

        surface,

        (61, 85, 64),

        tail

    )



    pygame.draw.polygon(

        surface,

        (31, 47, 36),

        tail,

        max(2, int(5 * scale))

    )



    # прожилки на хвосте

    for i in range(9):

        a = i / 8 * math.pi * 2



        x1 = cx + 465 * scale

        y1 = cy



        x2 = x1 + math.cos(a) * 65 * scale

        y2 = y1 + math.sin(a) * 55 * scale



        _ampeel_thick_line(

            surface,

            (91, 111, 75),

            (x1, y1),

            (x2, y2),

            2 * scale

        )



    # ячеистый узор хвоста

    random.seed(25)



    for _ in range(18):

        x = random.uniform(cx + 400 * scale, cx + 525 * scale)

        y = random.uniform(cy - 55 * scale, cy + 55 * scale)



        pygame.draw.circle(

            surface,

            (83, 108, 75),

            (int(x), int(y)),

            random.randint(

                max(3, int(5 * scale)),

                max(5, int(12 * scale))

            ),

            2

        )



    # --------------------------------------------------------

    # СЕГМЕНТЫ ТЕЛА

    # --------------------------------------------------------



    segment_count = 10

    segment_w = 92 * scale



    for i in range(segment_count):



        t = i / (segment_count - 1)



        x = body_start + i * segment_w



        # тело постепенно сужается

        half_h = (62 - 20 * t) * scale



        # небольшая волнистость тела

        local_y = cy + math.sin(i * 0.75) * 5 * scale



        rect = pygame.Rect(

            int(x),

            int(local_y - half_h),

            int(segment_w + 8 * scale),

            int(half_h * 2)

        )



        # сегмент

        pygame.draw.ellipse(

            surface,

            (72, 97, 74),

            rect

        )



        # верхний блик

        upper = pygame.Rect(

            rect.x + int(8 * scale),

            rect.y + int(10 * scale),

            rect.width - int(16 * scale),

            max(5, int(rect.height * 0.34))

        )



        pygame.draw.ellipse(

            surface,

            (96, 121, 92),

            upper

        )



        # нижняя тень

        pygame.draw.arc(

            surface,

            (36, 53, 40),

            rect,

            0,

            math.pi,

            max(2, int(5 * scale))

        )



        _ampeel_draw_armour_pattern(

            surface,

            rect,

            100 + i

        )



        # кольцо между сегментами

        if i > 0:

            ring_x = int(x + 7 * scale)



            pygame.draw.arc(

                surface,

                (31, 43, 32),

                (

                    ring_x - int(10 * scale),

                    int(local_y - half_h),

                    int(20 * scale),

                    int(half_h * 2)

                ),

                -math.pi / 2,

                math.pi / 2,

                max(2, int(6 * scale))

            )



            pygame.draw.line(

                surface,

                (112, 118, 75),

                (

                    ring_x,

                    int(local_y - half_h + 8 * scale)

                ),

                (

                    ring_x,

                    int(local_y + half_h - 8 * scale)

                ),

                max(1, int(2 * scale))

            )



    # --------------------------------------------------------

    # ГОЛОВА

    # --------------------------------------------------------



    head_x = cx - 520 * scale



    head_points = [

        (head_x - 75 * scale, cy),

        (head_x - 55 * scale, cy - 42 * scale),

        (head_x - 13 * scale, cy - 62 * scale),

        (head_x + 42 * scale, cy - 52 * scale),

        (head_x + 72 * scale, cy - 20 * scale),

        (head_x + 65 * scale, cy + 34 * scale),

        (head_x + 20 * scale, cy + 56 * scale),

        (head_x - 43 * scale, cy + 45 * scale),

    ]



    head_points = [

        (int(x), int(y))

        for x, y in head_points

    ]



    pygame.draw.polygon(

        surface,

        (67, 92, 70),

        head_points

    )



    pygame.draw.polygon(

        surface,

        (31, 47, 36),

        head_points,

        max(2, int(5 * scale))

    )



    # морда

    pygame.draw.ellipse(

        surface,

        (83, 112, 87),

        (

            int(head_x - 69 * scale),

            int(cy - 36 * scale),

            int(83 * scale),

            int(72 * scale)

        )

    )



    # голубое электрическое пятно

    _ampeel_add_glow(

        surface,

        (head_x - 48 * scale, cy),

        50 * scale,

        (40, 190, 255),

        100

    )



    for i in range(8):

        angle = i / 8 * math.pi * 2



        px = head_x - 48 * scale + math.cos(angle) * 25 * scale

        py = cy + math.sin(angle) * 23 * scale



        pygame.draw.arc(

            surface,

            (92, 210, 230),

            (

                int(px - 15 * scale),

                int(py - 9 * scale),

                int(30 * scale),

                int(18 * scale)

            ),

            0,

            math.pi * 1.6,

            max(1, int(2 * scale))

        )



    # глаз

    eye = (

        int(head_x - 23 * scale),

        int(cy - 18 * scale)

    )



    _ampeel_add_glow(

        surface,

        eye,

        12 * scale,

        (60, 255, 255),

        100

    )



    pygame.draw.circle(

        surface,

        (140, 255, 245),

        eye,

        max(3, int(5 * scale))

    )



    pygame.draw.circle(

        surface,

        (5, 20, 20),

        eye,

        max(1, int(2 * scale))

    )



    # --------------------------------------------------------

    # ОТРОСТКИ НА ТЕЛЕ

    # --------------------------------------------------------



    upper_tentacles = [

        (-470, -48, -510, -125),

        (-400, -55, -420, -145),

        (-325, -59, -355, -115),

        (-255, -62, -245, -145),

        (-170, -61, -190, -123),

        (-80,  -55, -45,  -125),

        (20,   -53, 70,   -120),

        (120,  -49, 175,  -105),

        (300,  -45, 350,  -88),

        (470,  -50, 500,  -130),

        (520,  -35, 575,  -60),

    ]



    lower_tentacles = [

        (-455, 42, -470, 125),

        (-370, 48, -370, 135),

        (-285, 53, -285, 125),

        (-175, 54, -160, 120),

        (-85,  48, -35,  105),

        (40,   45, 80,   105),

        (150,  40, 210,  94),

        (255,  35, 320,  88),

        (470,  43, 495,  125),

        (520,  35, 570,  75),

    ]



    for i, (bx, by, tx, ty) in enumerate(upper_tentacles):

        _ampeel_draw_tentacle(

            surface,

            (

                cx + bx * scale,

                cy + by * scale

            ),

            (

                cx + tx * scale,

                cy + ty * scale

            ),

            (

                (-1) ** i * 10 * scale,

                -10 * scale

            ),

            scale

        )



    for i, (bx, by, tx, ty) in enumerate(lower_tentacles):

        _ampeel_draw_tentacle(

            surface,

            (

                cx + bx * scale,

                cy + by * scale

            ),

            (

                cx + tx * scale,

                cy + ty * scale

            ),

            (

                (-1) ** i * 8 * scale,

                12 * scale

            ),

            scale

        )



    # --------------------------------------------------------

    # ОТРОСТКИ ОКОЛО ГОЛОВЫ

    # --------------------------------------------------------



    _ampeel_draw_tentacle(

        surface,

        (head_x - 15 * scale, cy - 40 * scale),

        (head_x - 65 * scale, cy - 100 * scale),

        (-15 * scale, -5 * scale),

        scale

    )



    _ampeel_draw_tentacle(

        surface,

        (head_x - 25 * scale, cy + 35 * scale),

        (head_x - 45 * scale, cy + 115 * scale),

        (-15 * scale, 10 * scale),

        scale

    )



    # --------------------------------------------------------

    # ЭЛЕКТРИЧЕСКИЕ ДУГИ

    # --------------------------------------------------------



    _ampeel_draw_lightning(

        surface,

        (

            head_x - 65 * scale,

            cy - 100 * scale

        ),

        (

            head_x - 130 * scale,

            cy - 120 * scale

        ),

        1

    )



    _ampeel_draw_lightning(

        surface,

        (

            head_x - 45 * scale,

            cy + 115 * scale

        ),

        (

            head_x - 5 * scale,

            cy + 55 * scale

        ),

        2

    )



    _ampeel_draw_lightning(

        surface,

        (

            head_x - 65 * scale,

            cy - 100 * scale

        ),

        (

            head_x - 20 * scale,

            cy - 55 * scale

        ),

        5

    )





# ------------------------------------------------------------

# ОСНОВНОЙ ЦИКЛ

# ------------------------------------------------------------

def generate_detailed_ampeel_sprite(length, width):
    """Detailed Ampeel from the standalone Pygame renderer, fitted to game size."""
    source = pygame.Surface((1400, 600), pygame.SRCALPHA)

    # The standalone renderer uses random.seed() for repeatable armour/lightning.
    # Preserve the game's global RNG state so generating a sprite cannot change
    # creature/resource spawn randomness.
    random_state = random.getstate()
    try:
        _draw_detailed_electric_eel(
            source,
            center=(700, 305),
            scale=0.92,
        )
    finally:
        random.setstate(random_state)

    bounds = source.get_bounding_rect(min_alpha=1)
    if bounds.width > 0 and bounds.height > 0:
        source = source.subsurface(bounds).copy()

    # The standalone picture looks left; game base sprites look right.
    source = pygame.transform.flip(source, True, False)

    length = max(12, int(length))
    width = max(6, int(width))
    margin = max(6, int(max(length, width) * 0.18))
    target_size = (
        length + margin * 2,
        max(width * 3, width + margin * 2),
    )
    return pygame.transform.smoothscale(source, target_size).convert_alpha()


# =========================================================
# ДЕТАЛЬНЫЙ ЛОПАТОЧНИК И ДРАКОН-ЛЕВИАФАН
# Перенесены из отдельных Pygame-зарисовок проекта и
# адаптированы к общей системе поворота/масштабирования игры.
# =========================================================

def _crop_alpha_surface(surface):
    bounds = surface.get_bounding_rect(min_alpha=1)
    if bounds.width > 0 and bounds.height > 0:
        return surface.subsurface(bounds).copy()
    return surface.copy()


def generate_detailed_spadefish_sprite(length, width):
    """Детальный лопаточник: огромное одиночное око, бирюзовые петли,
    светящиеся пятна и красно-розовый хвостовой плавник.

    Базовое направление спрайта — вправо, как у остальной фауны игры.
    """
    W, H = 780, 470
    s = pygame.Surface((W, H), pygame.SRCALPHA)

    # Палитра отдельной зарисовки лопаточника.
    TEAL_DARK = (0, 72, 86)
    TEAL = (0, 153, 164)
    TEAL_LIGHT = (16, 205, 211)
    CYAN = (74, 238, 239)
    CYAN_SOFT = (128, 250, 242)
    PURPLE_DARK = (65, 14, 78)
    MAGENTA = (192, 25, 168)
    MAGENTA_LIGHT = (235, 62, 205)
    CORAL_DARK = (188, 42, 58)
    CORAL = (255, 86, 101)
    CORAL_LIGHT = (255, 150, 154)
    EYE_RIM = (30, 28, 37)
    EYE_MID = (195, 197, 220)
    EYE_LIGHT = (248, 243, 223)

    def poly(color, pts, w=0):
        pygame.draw.polygon(s, color, [(int(x), int(y)) for x, y in pts], w)

    def ellipse(color, rect, w=0):
        pygame.draw.ellipse(s, color, pygame.Rect(*[int(v) for v in rect]), w)

    def circle(color, pos, r, w=0):
        pygame.draw.circle(s, color, (int(pos[0]), int(pos[1])), max(1, int(r)), w)

    # Хвост и длинный красно-коралловый плавник, рисуются позади корпуса.
    poly(TEAL_DARK, [(272, 204), (176, 188), (70, 199), (24, 232),
                     (74, 263), (175, 277), (286, 260)])
    poly(TEAL, [(280, 211), (170, 202), (74, 211), (40, 232),
                (78, 252), (170, 263), (282, 253)])
    poly(CORAL_DARK, [(300, 218), (230, 190), (141, 188), (49, 220),
                      (132, 224), (214, 228), (292, 236)])
    poly(CORAL, [(300, 220), (230, 197), (150, 198), (72, 219),
                 (151, 218), (225, 225), (294, 235)])
    poly(CORAL_LIGHT, [(286, 216), (220, 204), (159, 205), (107, 218),
                       (170, 216), (230, 220), (284, 229)])
    for x in range(118, 282, 30):
        pygame.draw.line(s, CORAL_DARK, (x, 205), (x + 34, 226), 3)

    # Основной силуэт. За глазом корпус образует две большие петли.
    body = [
        (272, 235), (305, 151), (372, 96), (466, 70), (565, 90),
        (650, 133), (720, 198), (755, 235), (720, 270), (653, 333),
        (565, 376), (468, 397), (374, 374), (306, 320),
    ]
    poly(TEAL_DARK, body)
    inner = [
        (285, 235), (320, 160), (383, 112), (469, 90), (555, 104),
        (636, 145), (700, 202), (730, 235), (699, 266), (638, 320),
        (556, 361), (471, 377), (388, 356), (324, 310),
    ]
    poly(TEAL, inner)

    # Большие прозрачные окна/петли в задней части тела.
    ellipse((0, 0, 0, 0), (314, 122, 153, 125))
    ellipse((0, 0, 0, 0), (314, 249, 153, 125))
    # Бирюзовая внутренняя окантовка петель.
    pygame.draw.arc(s, TEAL_LIGHT, pygame.Rect(307, 115, 167, 139),
                    math.radians(72), math.radians(290), 8)
    pygame.draw.arc(s, TEAL_LIGHT, pygame.Rect(307, 242, 167, 139),
                    math.radians(70), math.radians(292), 8)

    # Гигантский одиночный глаз.
    eye_c = (575, 236)
    ellipse(PURPLE_DARK, (438, 102, 276, 270))
    ellipse(MAGENTA, (451, 113, 254, 248))
    ellipse(MAGENTA_LIGHT, (461, 124, 234, 227), 7)
    ellipse(EYE_RIM, (474, 135, 210, 205))
    ellipse(EYE_MID, (485, 145, 188, 185))
    ellipse(EYE_LIGHT, (496, 153, 166, 168))
    ellipse((224, 227, 255), (545, 158, 89, 150))
    ellipse((255, 255, 255), (555, 165, 59, 99))
    # Горизонтальный зрачок, как на референсе.
    ellipse((8, 8, 10), (505, 222, 37, 43))
    pygame.draw.line(s, (250, 244, 220), (505, 243), (543, 243), 4)
    circle((255, 255, 255), (600, 188), 9)

    # Носовая грань и лёгкая подсветка.
    poly(TEAL_LIGHT, [(700, 202), (758, 235), (700, 266),
                      (719, 242), (719, 228)])
    pygame.draw.aaline(s, CYAN_SOFT, (717, 210), (751, 235))

    # Голубые пятна. Фиксированный набор сохраняет одинаковый внешний вид.
    spots = [
        (357, 102, 18, 9), (402, 92, 25, 12), (451, 87, 15, 8),
        (523, 103, 18, 9), (601, 126, 15, 8), (651, 160, 13, 7),
        (685, 192, 12, 7), (345, 140, 11, 6), (291, 191, 12, 7),
        (285, 273, 10, 6), (344, 335, 14, 8), (396, 363, 21, 10),
        (455, 379, 15, 8), (535, 364, 21, 10), (600, 336, 14, 8),
        (655, 302, 12, 7), (685, 273, 10, 6), (324, 286, 8, 5),
    ]
    for i, (x, y, rx, ry) in enumerate(spots):
        col = CYAN if i % 3 else CYAN_SOFT
        ellipse(col, (x - rx, y - ry, rx * 2, ry * 2))

    # Мелкая россыпь пятен вокруг головы/петель.
    for x, y, r in [(319,171,5),(334,155,4),(354,333,5),(376,347,4),
                    (398,116,4),(430,107,5),(481,100,4),(626,146,4),
                    (667,181,4),(664,294,4),(620,325,4),(483,370,4)]:
        circle(CYAN, (x, y), r)

    # Тёмные кольца-сегменты у хвостового корня.
    for off in (-22, -8, 8, 22):
        pygame.draw.arc(s, TEAL_DARK, pygame.Rect(247 + off, 175, 95, 120),
                        math.radians(78), math.radians(282), 4)

    # Светящиеся красные усики сверху/снизу.
    for sign in (-1, 1):
        y0 = 117 if sign < 0 else 355
        y1 = 58 if sign < 0 else 414
        pygame.draw.line(s, (130, 20, 46), (397, y0), (463, y1), 10)
        pygame.draw.line(s, (255, 45, 82), (398, y0), (463, y1), 5)
        circle((255, 25, 44, 90), (463, y1), 16)
        circle((255, 67, 83), (463, y1), 8)
        circle((255, 190, 190), (460, y1 - sign * 3), 3)

    # Внешняя контурная линия повышает читаемость после уменьшения.
    pygame.draw.aalines(s, (0, 64, 76), True,
                        [(int(x), int(y)) for x, y in body])

    s = _crop_alpha_surface(s)
    length = max(18, int(length))
    width = max(8, int(width))
    margin = max(7, int(max(length, width) * 0.18))
    target_w = length + margin * 2
    target_h = max(width * 3, width + margin * 2)
    return pygame.transform.smoothscale(s, (target_w, target_h)).convert_alpha()


def generate_detailed_sea_dragon_sprite(length, width):
    """Детальный дракон-левиафан сверху: бронированные зелёные пластины,
    четыре длинных боковых отростка, руки с когтями, рога и фиолетовые
    перепончатые плавники. Источник рисуется вертикально, затем разворачивается
    так, чтобы базовое направление в игре было вправо.
    """
    W, H = 560, 1000
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    cx = W // 2

    DARK = (23, 54, 44)
    GREEN_DARK = (38, 89, 62)
    GREEN = (67, 128, 76)
    GREEN_LIGHT = (105, 166, 94)
    SCALE_DARK = (34, 70, 58)
    PURPLE_DARK = (54, 30, 72)
    PURPLE = (105, 51, 107)
    PURPLE_LIGHT = (164, 84, 143)
    ORANGE = (255, 119, 32)
    ORANGE_LIGHT = (255, 197, 75)
    CLAW = (238, 226, 161)
    EYE = (255, 185, 73)

    def poly(color, pts, w=0):
        pygame.draw.polygon(s, color, [(int(x), int(y)) for x, y in pts], w)

    def ell(color, rect, w=0):
        pygame.draw.ellipse(s, color, pygame.Rect(*[int(v) for v in rect]), w)

    def circ(color, pos, r, w=0):
        pygame.draw.circle(s, color, (int(pos[0]), int(pos[1])), max(1, int(r)), w)

    def thick_path(points, widths, outer, inner):
        for i in range(len(points) - 1):
            a = points[i]; b = points[i + 1]
            ww = max(2, int((widths[i] + widths[i + 1]) / 2))
            pygame.draw.line(s, outer, a, b, ww + 7)
            pygame.draw.line(s, inner, a, b, ww)
            circ(inner, a, ww // 2)
        circ(inner, points[-1], max(2, widths[-1] // 2))

    # Дальние хвостовые отростки — рисуются первыми.
    tendrils = [
        ([(210, 515), (150, 610), (125, 720), (142, 835)], [28, 22, 15, 8], -1),
        ([(240, 520), (205, 645), (200, 765), (180, 902)], [30, 22, 15, 8], -1),
        ([(320, 520), (355, 645), (360, 765), (380, 902)], [30, 22, 15, 8], 1),
        ([(350, 515), (410, 610), (435, 720), (418, 835)], [28, 22, 15, 8], 1),
    ]
    for idx, (pts, widths, side) in enumerate(tendrils):
        thick_path(pts, widths, DARK, GREEN_DARK)
        # Оранжевые биолюминесцентные точки вдоль отростков.
        for j in range(1, 5):
            t = j / 5
            p0, p1 = pts[min(len(pts)-2, int(t*(len(pts)-1)))], pts[min(len(pts)-1, int(t*(len(pts)-1))+1)]
            local = (t * (len(pts)-1)) % 1.0
            x = p0[0] + (p1[0]-p0[0]) * local
            y = p0[1] + (p1[1]-p0[1]) * local
            circ((255, 90, 25, 75), (x, y), 8)
            circ(ORANGE, (x, y), 3)
        # Фиолетовая перепонка ближе к концу.
        tip = pts[-1]
        base = pts[-2]
        if side < 0:
            fin = [(base[0]-4, base[1]+20), (tip[0]-45, tip[1]-20),
                   (tip[0]-12, tip[1]+56), (tip[0]+12, tip[1]+8)]
        else:
            fin = [(base[0]+4, base[1]+20), (tip[0]+45, tip[1]-20),
                   (tip[0]+12, tip[1]+56), (tip[0]-12, tip[1]+8)]
        poly(PURPLE_DARK, fin)
        inner_fin = [(x + (cx-x)*0.08, y) for x, y in fin]
        poly(PURPLE, inner_fin)
        pygame.draw.aalines(s, PURPLE_LIGHT, True, fin)

    # Центральный мощный хвост.
    central = [(cx, 470), (cx+7, 590), (cx-4, 710), (cx+5, 830), (cx, 945)]
    thick_path(central, [72, 58, 42, 27, 13], DARK, GREEN_DARK)
    pygame.draw.line(s, GREEN_LIGHT, (cx-13, 535), (cx-8, 870), 4)
    poly(DARK, [(cx-25, 900), (cx, 975), (cx+28, 900), (cx+7, 920), (cx-7, 920)])
    poly(GREEN_DARK, [(cx-18, 903), (cx, 960), (cx+20, 903), (cx+5, 920), (cx-5, 920)])

    # Туловище и шея.
    body = [(cx-88, 165), (cx-112, 235), (cx-101, 340), (cx-80, 455),
            (cx-55, 535), (cx, 565), (cx+55, 535), (cx+80, 455),
            (cx+101, 340), (cx+112, 235), (cx+88, 165)]
    poly(DARK, body)
    body2 = [(cx-78, 172), (cx-99, 238), (cx-88, 334), (cx-69, 444),
             (cx-48, 516), (cx, 545), (cx+48, 516), (cx+69, 444),
             (cx+88, 334), (cx+99, 238), (cx+78, 172)]
    poly(GREEN, body2)

    # Поперечные бронированные пластины/чешуя.
    for i in range(14):
        y = 190 + i * 24
        taper = max(0, i - 6)
        half = 78 - taper * 4
        if i < 4:
            half = 82 + i * 4
        pts = [(cx-half, y), (cx-18, y-10), (cx, y-15),
               (cx+18, y-10), (cx+half, y), (cx+half-10, y+13),
               (cx, y+8), (cx-half+10, y+13)]
        poly(SCALE_DARK, pts)
        poly(GREEN_LIGHT, [(x+(cx-x)*0.08, yy+2) for x, yy in pts])
        pygame.draw.aaline(s, (128, 181, 111), (cx-half+10, y+1), (cx+half-10, y+1))

    # Фиолетовые рёбра по центру грудной части.
    for i in range(6):
        y = 238 + i * 35
        poly(PURPLE_DARK, [(cx-63, y), (cx-15, y+10), (cx, y+18),
                           (cx+15, y+10), (cx+63, y), (cx+45, y+13),
                           (cx, y+28), (cx-45, y+13)])

    # Руки с когтями.
    for sign in (-1, 1):
        shoulder = (cx + sign * 92, 245)
        elbow = (cx + sign * 150, 326)
        wrist = (cx + sign * 167, 405)
        thick_path([shoulder, elbow, wrist], [38, 30, 21], DARK, GREEN)
        pygame.draw.aaline(s, GREEN_LIGHT,
                           (shoulder[0]-sign*6, shoulder[1]),
                           (wrist[0]-sign*4, wrist[1]-5))
        # Пальцы/когти.
        for k in range(3):
            bx = wrist[0] + sign * (3 + k * 7)
            by = wrist[1] + k * 2
            poly(CLAW, [(bx, by), (bx + sign*(20+k*2), by+17+k*3),
                        (bx + sign*(7+k), by+9)])
        # Мелкие шипы на предплечье.
        for k in range(4):
            t = (k + 1) / 5
            x = elbow[0] + (wrist[0]-elbow[0]) * t
            y = elbow[1] + (wrist[1]-elbow[1]) * t
            poly(GREEN_LIGHT, [(x, y), (x + sign*18, y-5), (x + sign*4, y+8)])

    # Голова, "корона" и боковые перепончатые гребни.
    head = [(cx-92, 120), (cx-71, 71), (cx-32, 46), (cx, 39),
            (cx+32, 46), (cx+71, 71), (cx+92, 120), (cx+70, 173),
            (cx, 192), (cx-70, 173)]
    poly(DARK, head)
    poly(GREEN, [(x+(cx-x)*0.08, y+4) for x, y in head])

    # Рога — два центральных и боковые.
    for sign in (-1, 1):
        poly(DARK, [(cx+sign*28, 58), (cx+sign*52, 10),
                    (cx+sign*42, 72)])
        poly(GREEN_LIGHT, [(cx+sign*30, 58), (cx+sign*48, 17),
                           (cx+sign*40, 72)])
        poly(DARK, [(cx+sign*78, 100), (cx+sign*130, 70),
                    (cx+sign*86, 121)])
        poly(GREEN_LIGHT, [(cx+sign*80, 102), (cx+sign*124, 76),
                           (cx+sign*86, 117)])
        # Ушной/щечный фиолетовый плавник.
        fin = [(cx+sign*58, 75), (cx+sign*112, 37),
               (cx+sign*98, 112), (cx+sign*71, 137)]
        poly(PURPLE_DARK, fin)
        poly(PURPLE, [(x+(cx-x)*0.05, y+3) for x, y in fin])
        pygame.draw.aalines(s, PURPLE_LIGHT, True, fin)

    # Глаза и лицевая броня.
    for sign in (-1, 1):
        ex = cx + sign * 34
        ey = 115
        circ((14, 20, 18), (ex, ey), 8)
        circ(EYE, (ex, ey), 5)
        circ((255, 245, 180), (ex-sign*1, ey-2), 2)
    for i in range(5):
        y = 82 + i * 17
        half = 47 + i * 7
        poly(SCALE_DARK, [(cx-half, y), (cx, y-8), (cx+half, y),
                          (cx+half-8, y+10), (cx, y+7), (cx-half+8, y+10)])

    # Боковые светящиеся точки на корпусе.
    for sign in (-1, 1):
        for i in range(11):
            y = 185 + i * 30
            x = cx + sign * (76 - min(i, 7) * 3)
            circ((255, 100, 25, 65), (x, y), 7)
            circ(ORANGE if i % 2 else ORANGE_LIGHT, (x, y), 2.6)

    # Небольшие шипы по краям тела.
    for sign in (-1, 1):
        for i in range(7):
            y = 180 + i * 42
            x = cx + sign * (91 - max(0, i-3)*5)
            poly(GREEN_LIGHT, [(x, y), (x + sign*20, y+7), (x, y+15)])

    s = _crop_alpha_surface(s)
    # Вертикальная зарисовка -> направление головы вправо.
    s = pygame.transform.rotate(s, -90)
    s = _crop_alpha_surface(s)

    length = max(80, int(length))
    width = max(28, int(width))
    margin = max(10, int(max(length, width) * 0.12))
    target_w = length + margin * 2
    target_h = max(width * 3, width + margin * 2)
    return pygame.transform.smoothscale(s, (target_w, target_h)).convert_alpha()


# =========================================================
# КАНОНИЧЕСКИЕ СПРАЙТЫ ФАУНЫ SUBNAUTICA
# =========================================================

# =========================================================
# ДЕТАЛЬНЫЕ ПИСКУН, БУМЕРАНГ, КОЛЬЦЕВИК (предыдущая версия)
# Восстановлены по Pygame-зарисовкам от 10 октября 2026.
# Исходная геометрия ВСЕГДА масштабируется ОДИНАКОВО по X и Y,
# поэтому глаза, плавники и кольцо не деформируются.
# Кольцевик = Hoopfish. Holefish (Дырохвост) НЕ затрагивается.
# =========================================================

def _detail_fish_point_list(points):
    return [(int(round(x)), int(round(y))) for x, y in points]


def _detail_fish_bezier(a, b, c, d, steps=40):
    result = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        result.append((
            u**3 * a[0] + 3*u*u*t*b[0] + 3*u*t*t*c[0] + t**3*d[0],
            u**3 * a[1] + 3*u*u*t*b[1] + 3*u*t*t*c[1] + t**3*d[1],
        ))
    return _detail_fish_point_list(result)


def _detail_fish_tube(surface, points, outer, inner, thickness):
    points = _detail_fish_point_list(points)
    pygame.draw.lines(surface, outer, False, points, thickness + 7)
    pygame.draw.lines(surface, inner, False, points, thickness)
    for p in (points[0], points[-1]):
        pygame.draw.circle(surface, inner, p, max(2, thickness // 2))


def _source_detailed_peeper():
    """Пискун, нарисованный слева направо после зеркального отражения."""
    s = pygame.Surface((820, 460), pygame.SRCALPHA)
    P = lambda c, pts: pygame.draw.polygon(s, c, _detail_fish_point_list(pts))
    E = lambda c, r, w=0: pygame.draw.ellipse(s, c, pygame.Rect(*[int(q) for q in r]), w)
    C = lambda c, p, r, w=0: pygame.draw.circle(s, c, _detail_fish_point_list([p])[0], int(r), w)
    L = lambda c, a, b, w=1: pygame.draw.line(s, c, a, b, w)

    # Повернут влево как в отдельной зарисовке. В конце будет отражён.
    # Полупрозрачный веерообразный хвост (позади туловища).
    tail_outer = [(595,224),(653,145),(754,98),(727,188),(782,231),
                  (725,276),(758,356),(652,305),(596,254)]
    P((22,78,105), tail_outer)
    P((34,158,177,180), [(610,226),(674,165),(735,115),(712,193),
                        (760,229),(710,270),(740,334),(672,287),(606,250)])
    for end in [(738,112),(723,151),(742,206),(764,231),(741,269),(736,334)]:
        L((104,226,221), (615,233), end, 3)
        L((174,255,237), (635,231), (int(end[0]*0.94),int((end[1]+231)*0.5)), 1)

    # Два длинных плавника со множеством прожилок.
    upper = [(310,205),(385,103),(455,37),(490,38),(470,98),(524,185)]
    lower = [(295,260),(390,361),(468,428),(497,419),(478,345),(534,272)]
    P((13,82,113), upper)
    P((21,89,122), lower)
    P((48,163,176,205), [(325,199),(397,115),(451,53),(467,68),(439,131),(486,193)])
    P((44,154,170,205), [(314,270),(397,352),(459,412),(476,395),(443,339),(491,267)])
    for tip in [(457,44),(475,63),(457,93),(421,115)]:
        L((132,230,216),(369,181),tip,3)
    for tip in [(471,410),(483,385),(452,359),(420,338)]:
        L((127,221,218),(364,288),tip,3)

    # Мягкое обтекаемое тело из вложенных форм и полос.
    body = [(122,226),(147,183),(217,145),(307,126),(416,133),
            (529,164),(611,204),(639,232),(605,263),(529,299),
            (415,322),(307,322),(208,298),(142,266)]
    P((10,71,95),body)
    inner = [(137,225),(165,189),(236,157),(321,145),(419,153),
             (522,182),(598,211),(619,230),(589,250),(525,282),
             (423,303),(316,304),(228,280),(162,254)]
    P((16,141,173), inner)
    P((50,190,200),[(148,223),(179,186),(263,165),(357,159),
                     (468,172),(554,203),(578,220),(460,204),
                     (352,194),(266,207),(198,231)])
    P((5,99,143),[(167,260),(240,264),(331,272),(442,267),
                  (557,238),(590,244),(520,280),(420,301),
                  (301,299),(213,279)])
    # Продольные голубые отблески на спине и брюхе.
    pygame.draw.lines(s,(131,242,236),False,
        _detail_fish_bezier((220,164),(333,140),(484,159),(574,202)),3)
    pygame.draw.lines(s,(30,104,152),False,
        _detail_fish_bezier((230,277),(348,310),(489,281),(569,249)),4)

    # Жаберные щели, боковые отверстия и пятна.
    for x,y in [(372,203),(397,206),(422,210),(450,213),(478,213)]:
        E((2,76,111),(x,y,13,37))
        E((68,200,212),(x+2,y+2,7,24))
    for x,y,r in [(502,247,9),(535,232,8),(564,224,6),(363,264,7),
                  (320,256,6),(292,241,4),(483,189,4)]:
        C((9,90,119),(x,y),r)
        C((112,225,220),(x-2,y-2),max(2,r-4))

    # Короткая острая морда и рот (слева).
    P((24,111,144),[(117,223),(73,226),(93,213),(123,207)])
    P((35,168,184),[(117,230),(73,227),(94,240),(136,252)])
    L((3,54,73),(75,227),(127,229),4)
    for x in (88,100,113):
        P((236,246,208),[(x,226),(x+4,233),(x+8,226)])
    # Огромный фирменный золотой глаз: кольца, радужка и радиальные штрихи.
    ex,ey=246,218
    C((8,70,103),(ex,ey),93)
    C((183,119,22),(ex,ey),85)
    C((255,217,45),(ex,ey),78)
    C((255,242,118),(ex-4,ey-6),67)
    for i in range(44):
        a=math.tau*i/44
        r0,r1=55,73
        p0=(int(ex+math.cos(a)*r0),int(ey+math.sin(a)*r0))
        p1=(int(ex+math.cos(a)*r1),int(ey+math.sin(a)*r1))
        L((196,130,27) if i%3 else (255,251,164),p0,p1,2)
    C((18,39,54),(ex+3,ey+2),55)
    C((2,13,21),(ex+7,ey+3),44)
    E((255,255,255,235),(213,169,33,23))
    C((156,237,251),(ex+28,ey+29),10)
    E((247,252,235,170),(189,182,18,10))

    # В источнике Пискун смотрит налево; стандарт игры — вправо.
    return pygame.transform.flip(s, True, False)


def _source_detailed_boomerang():
    """Крупные симметричные плавники, бирюзовая чешуя, парные глаза и зубы."""
    s = pygame.Surface((900, 690), pygame.SRCALPHA)
    P = lambda c,pts: pygame.draw.polygon(s,c,_detail_fish_point_list(pts))
    E = lambda c,r,w=0: pygame.draw.ellipse(s,c,pygame.Rect(*[int(q) for q in r]),w)
    C = lambda c,p,r,w=0: pygame.draw.circle(s,c,_detail_fish_point_list([p])[0],int(r),w)
    L = lambda c,a,b,w=1: pygame.draw.line(s,c,a,b,w)

    # Крыловидные плавники позади узкого центрального тела.
    # Верх и низ строятся симметрично вокруг оси y=344.
    for sign in (-1,1):
        def Y(v): return 344+sign*v
        fin_outer=[(158,Y(0)),(240,Y(124)),(334,Y(235)),
                   (457,Y(321)),(559,Y(298)),(516,Y(215)),
                   (443,Y(145)),(479,Y(70)),(387,Y(28))]
        fin_inner=[(213,Y(14)),(265,Y(134)),(352,Y(224)),
                   (466,Y(301)),(536,Y(280)),(487,Y(203)),
                   (420,Y(140)),(454,Y(73)),(365,Y(37))]
        P((18,51,108),fin_outer)
        P((63,109,190),fin_inner)
        P((39,149,191,195),[(258,Y(128)),(351,Y(211)),
                            (457,Y(288)),(498,Y(272)),
                            (413,Y(175)),(326,Y(101))])
        # Сеть прожилок от корня плавника к краям.
        for j, tip in enumerate([(306,Y(174)),(346,Y(215)),(403,Y(274)),
                                 (470,Y(309)),(526,Y(280)),(478,Y(222))]):
            pygame.draw.lines(s,(166,195,234),False,
                _detail_fish_bezier((332,Y(37)),(358,Y(88)),
                                    (tip[0]-55,Y(abs(tip[1]-344)*0.78)),tip,23),
                2 if j%2 else 3)
        # Розовые яркие контурные полосы вдоль плавников.
        pygame.draw.lines(s,(227,91,181),False,
            _detail_fish_bezier((234,Y(102)),(323,Y(189)),
                                (405,Y(286)),(485,Y(311))),5)
        pygame.draw.lines(s,(255,151,224),False,
            _detail_fish_bezier((270,Y(118)),(353,Y(211)),
                                (429,Y(267)),(489,Y(293))),2)

    # Короткий задний хвостовой разворот.
    P((30,73,120),[(204,344),(112,291),(60,301),(102,344),
                   (60,388),(111,395)])
    P((47,153,185),[(200,344),(106,310),(83,311),(120,344),
                    (86,375),(113,382)])
    for tip in [(71,303),(64,388),(91,337)]:
        L((146,211,231),(183,346),tip,2)

    # Узкий зелено-бирюзовый корпус с головой вправо.
    P((13,66,82),[(200,341),(263,306),(391,297),(536,300),
                  (655,317),(735,329),(792,344),(746,362),
                  (656,375),(533,386),(398,380),(266,368)])
    P((18,138,157),[(216,343),(282,320),(407,311),(531,318),
                    (667,329),(769,341),(740,351),(649,360),
                    (533,368),(403,364),(289,356)])
    P((74,193,117),[(312,325),(435,320),(559,331),(630,342),
                     (557,350),(435,354),(310,350)])
    pygame.draw.lines(s,(155,240,196),False,
        _detail_fish_bezier((282,324),(431,300),(642,326),(745,340)),4)
    pygame.draw.lines(s,(4,91,121),False,
        _detail_fish_bezier((292,366),(456,385),(638,370),(750,352)),4)

    # Геометричная чешуя по бокам, не перекрывающая глаза.
    for row in range(3):
        for j in range(13):
            x=305+j*26+(row%2)*12
            y=326+row*13
            if x<658:
                P((22,125,146) if (j+row)%2 else (86,188,167),
                  [(x,y),(x+10,y-5),(x+20,y),(x+10,y+7)])
                L((137,220,200),(x+4,y-1),(x+12,y-4),1)

    # Жаберные полосы.
    for gx in (656,670,684):
        pygame.draw.arc(s,(9,89,109),pygame.Rect(gx-3,326,20,35),
                        math.radians(85),math.radians(260),3)

    # Парные большие глаза с жёлтыми кольцами и синей радужкой.
    for ex,ey in [(702,320),(700,363)]:
        C((10,54,76),(ex,ey),22)
        C((247,216,46),(ex,ey),19)
        C((255,250,154),(ex-2,ey-2),14)
        C((23,141,218),(ex+2,ey+1),11)
        C((10,26,61),(ex+4,ey+1),6)
        C((248,252,255),(ex-2,ey-5),4)

    # Приоткрытая зубастая пасть: нос вправо, два ряда маленьких зубов.
    P((6,28,42),[(752,338),(810,333),(829,345),(806,356),(755,354)])
    P((89,181,164),[(747,331),(817,329),(834,338),(772,342)])
    P((38,135,146),[(757,358),(822,359),(836,350),(772,350)])
    for x in range(777,827,10):
        P((244,249,239),[(x,338),(x+4,345),(x+8,337)])
        P((242,249,241),[(x,356),(x+4,350),(x+8,355)])
    C((189,232,226),(824,343),3)
    return s


def _source_detailed_hoopfish():
    """Кольцевик / Hoopfish: светящееся кольцо вокруг тела, а не отверстие."""
    s=pygame.Surface((890,450),pygame.SRCALPHA)
    P=lambda c,pts: pygame.draw.polygon(s,c,_detail_fish_point_list(pts))
    E=lambda c,r,w=0: pygame.draw.ellipse(s,c,pygame.Rect(*[int(q) for q in r]),w)
    C=lambda c,p,r,w=0: pygame.draw.circle(s,c,_detail_fish_point_list([p])[0],int(r),w)
    L=lambda c,a,b,w=1: pygame.draw.line(s,c,a,b,w)

    # Хвостовая лопасть и лучи веера.
    P((33,33,92),[(202,225),(116,161),(42,145),(100,226),
                  (40,316),(121,297)])
    P((95,49,164),[(205,226),(113,177),(65,166),(126,226),
                   (65,291),(125,273)])
    for tip in [(50,150),(53,314),(88,187),(91,268)]:
        L((146,111,212),(206,225),tip,3)

    # Длинное кольцо-отросток сначала рисуется ЗА телом.
    upper=_detail_fish_bezier((203,219),(270,76),(486,62),(639,204))
    lower=_detail_fish_bezier((203,234),(294,385),(488,395),(640,240))
    _detail_fish_tube(s,upper,(13,61,70),(40,220,163),13)
    _detail_fish_tube(s,lower,(13,60,77),(30,211,171),13)
    # Пульсирующая внутренняя линия и узелки кольца.
    pygame.draw.lines(s,(192,255,124),False,upper,3)
    pygame.draw.lines(s,(160,247,183),False,lower,3)
    for i in range(9,39,5):
        x,y=upper[i]
        C((32,104,104),(x,y),6)
        C((188,255,164),(x-1,y-1),3)
        x,y=lower[i]
        C((30,97,102),(x,y),6)
        C((171,249,177),(x-1,y-1),3)

    # Тело тёмно-фиолетовое, на спине фиолетовый, на брюшке бирюза.
    P((20,30,84),[(166,220),(229,190),(342,181),(474,184),
                  (585,202),(661,216),(696,228),(664,242),
                  (571,265),(472,277),(339,273),(226,252)])
    P((54,50,140),[(183,219),(244,195),(349,191),(468,193),
                  (588,208),(671,220),(667,228),(558,226),
                  (456,223),(338,222),(244,229)])
    P((16,135,153),[(190,226),(251,234),(363,239),(482,239),
                   (593,230),(668,233),(652,241),(568,254),
                   (461,266),(347,260),(241,247)])
    pygame.draw.lines(s,(99,104,201),False,
        _detail_fish_bezier((240,204),(378,169),(548,201),(659,220)),3)
    pygame.draw.lines(s,(62,225,215),False,
        _detail_fish_bezier((241,248),(385,280),(565,259),(662,237)),3)

    # Крупные чешуйки и светящиеся боковые пятна.
    for j in range(12):
        x=275+j*25
        y=209+int(5*math.sin(j*.75))
        E((27,34,103),(x,y,19,17))
        E((109,89,179),(x+3,y+2,10,7))
    for x,y,r in [(281,237,6),(326,247,5),(374,254,5),
                  (422,251,6),(470,250,5),(510,244,6),(557,238,5)]:
        C((21,77,109),(x,y),r+3)
        C((105,244,223),(x,y),r)
        C((221,255,235),(x-2,y-2),max(2,r//2))

    # Небольшой спинной плавник и грудной плавничок.
    P((66,44,127),[(393,189),(440,163),(485,148),(473,190)])
    P((138,81,200),[(410,187),(451,167),(472,162),(463,190)])
    P((21,100,148),[(458,243),(389,311),(503,266)])
    L((103,213,210),(454,253),(406,303),3)

    # Неоново-зелёная голова. Кольцо прикрепляется к её бокам.
    E((17,68,79),(604,198,115,68))
    E((71,200,111),(613,203,101,59))
    E((136,242,123),(650,209,60,41))
    # Верхний и нижний светящиеся уголки в месте крепления усиков.
    for xy in [(645,205),(647,253)]:
        C((10,74,77),xy,11)
        C((145,251,158),xy,7)
    # Парные зелёные глаза и маленькая линия рта.
    for ex,ey in [(681,215),(681,248)]:
        C((17,70,48),(ex,ey),15)
        C((190,252,98),(ex,ey),12)
        C((34,148,95),(ex+2,ey),7)
        C((13,31,43),(ex+3,ey),5)
        C((248,255,234),(ex-4,ey-4),3)
    L((6,54,66),(706,231),(724,233),3)
    L((160,247,142),(705,227),(723,229),2)
    return s


def _fit_small_fauna_proportionally(source, length, width, height_multiplier):
    """Не используем smoothscale(source, (length,width)): это сплющит рыбу!

    Берём один общий коэффициент для обеих осей. Максимальный размер
    остаётся в пределах стандартного игрового слота рыбы, а расширенные
    плавники занимают запас по высоте старого игрового спрайта.
    """
    length = max(12, int(length))
    width = max(6, int(width))
    source = _crop_alpha_surface(source)
    source_w, source_h = source.get_size()
    scale = min(length / max(1, source_w),
                (width * height_multiplier) / max(1, source_h))
    target_w = max(1, int(round(source_w * scale)))
    target_h = max(1, int(round(source_h * scale)))
    margin = max(6, int(max(length, width) * 0.18))
    canvas_w = length + 2 * margin
    canvas_h = max(width * 3, width + 2 * margin)
    # Дополнительная страховка для необычно маленьких пользовательских размеров.
    if target_w > canvas_w or target_h > canvas_h:
        adjust = min(canvas_w / target_w, canvas_h / target_h)
        target_w = max(1, int(round(target_w * adjust)))
        target_h = max(1, int(round(target_h * adjust)))
    result = pygame.Surface((canvas_w, canvas_h), pygame.SRCALPHA)
    image = pygame.transform.smoothscale(source, (target_w, target_h))
    result.blit(image, image.get_rect(center=(canvas_w//2, canvas_h//2)))
    return result.convert_alpha()


def generate_detailed_peeper_sprite(length, width):
    return _fit_small_fauna_proportionally(_source_detailed_peeper(), length, width, 2.2)


def generate_detailed_boomerang_sprite(length, width):
    return _fit_small_fauna_proportionally(_source_detailed_boomerang(), length, width, 2.7)


def generate_detailed_hoopfish_sprite(length, width):
    return _fit_small_fauna_proportionally(_source_detailed_hoopfish(), length, width, 2.25)


# =================================================================
# ФАУНА ИЗ ПРИКРЕПЛЁННЫХ PYGAME-ФАЙЛОВ
# Оригинальные примитивы рисуются однократно в исходном разрешении.
# При помещении в игровой спрайт применяется единый коэффициент по
# обеим осям: плавники, глаза и пузыри не растягиваются.
# =================================================================

_UPLOADED_SMALL_FAUNA_CACHE = {}

def _create_uploaded_boomerang_source():
    """Оригинальные фигуры из файла Вставленный текст (3).txt."""
    ART_W, ART_H = 900, 680
    MID_Y = 330
    _MASTER = None

    def _clamp(v):
        return max(0, min(255, int(v)))

    def _mix(a, b, t):
        return tuple(_clamp(a[i] + (b[i] - a[i]) * t) for i in range(3))

    def _cubic(p0, p1, p2, p3, steps=18):
        result = []
        for i in range(steps + 1):
            t = i / steps
            u = 1 - t
            result.append((
                u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
                u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]
            ))
        return result

    def _curve(start, *segments):
        """Собирает путь из кубических кривых; сегмент=(контроль1, контроль2, конец)."""
        pts = [start]
        current = start
        for a, b, end in segments:
            pts.extend(_cubic(current, a, b, end)[1:])
            current = end
        return pts

    def _mirror(points, side):
        if side == 1:
            return points
        return [(px, 2 * MID_Y - py) for px, py in points]

    def _xy(point, side):
        x, y = point
        return (x, y if side == 1 else 2 * MID_Y - y)

    def _poly(surface, points, color, side=1):
        pygame.draw.polygon(surface, color, [(round(x), round(y)) for x,y in _mirror(points, side)])

    def _line(surface, points, color, width=1, side=1, closed=False):
        if len(points) > 1:
            pygame.draw.lines(surface, color, closed, [(round(x), round(y)) for x,y in _mirror(points, side)], width)

    def _oval(surface, rect, color, side=1, width=0):
        x, y, w, h = rect
        if side == -1:
            y = 2 * MID_Y - y - h
        pygame.draw.ellipse(surface, color, pygame.Rect(round(x), round(y), round(w), round(h)), width)

    def _circle(surface, pos, radius, color, side=1):
        pygame.draw.circle(surface, color, tuple(round(v) for v in _xy(pos,side)), radius)

    def _fin_shape():
        # Один плавник. Второй получается зеркальным отражением по горизонтали.
        return _curve(
            (205, 300),
            ((223, 270), (248, 230), (278, 214)),
            ((367, 160), (471, 112), (553, 68)),
            ((572, 52), (638, 62), (670, 61)),
            ((655, 88), (626, 137), (612, 164)),
            ((591, 183), (570, 173), (554, 164)),
            ((513, 149), (483, 172), (448, 201)),
            ((401, 238), (394, 273), (392, 294)),
            ((365, 307), (297, 311), (253, 310)),
            ((225, 310), (218, 310), (205, 300)),
        )

    def _point_inside_polygon(point, polygon):
        x, y = point
        inside = False
        j = len(polygon) - 1
        for i in range(len(polygon)):
            xi, yi = polygon[i]
            xj, yj = polygon[j]
            if ((yi > y) != (yj > y)) and (x < (xj-xi) * (y-yi) / (yj-yi) + xi):
                inside = not inside
            j = i
        return inside

    def _draw_fins(surface):
        rng = random.Random(7841)  # всегда одинаковые пятна и чешуйки
        fin_path = _fin_shape()

        for side in (1, -1):
            # Самая тёмная внешняя кромка — объёмная, с холодным свечением.
            _poly(surface, fin_path, (0, 37, 55), side)
            _line(surface, fin_path, (0, 133, 156), 4, side, closed=True)
            _line(surface, fin_path[1:125], (23, 208, 205), 3, side)

            # Основная поверхность плавника: несколько фигур задают переход
            # от почти чёрного ультрамарина к тёмной бирюзе.
            _poly(surface, _curve(
                (211, 293),
                ((273, 231), (419, 142), (554, 75)),
                ((589, 64), (627, 67), (651, 66)),
                ((607, 114), (567, 125), (512, 153)),
                ((450, 190), (405, 232), (382, 288)),
                ((317, 300), (266, 298), (211, 293))
            ), (0, 72, 97), side)
            _poly(surface, _curve(
                (235, 284),
                ((299, 232), (420, 166), (555, 93)),
                ((591, 82), (631, 81), (649, 75)),
                ((594, 111), (547, 145), (476, 177)),
                ((433, 203), (402, 245), (388, 283)),
                ((318, 293), (260, 290), (235, 284))
            ), (1, 37, 69), side)

            # Продольные ленты отражённого подводного света.
            _poly(surface, _curve(
                (258, 263),
                ((380, 190), (485, 129), (560, 87)),
                ((606, 78), (630, 78), (652, 73)),
                ((606, 105), (565, 120), (505, 158)),
                ((403, 202), (315, 253), (258, 263))
            ), (0, 77, 100), side)
            _poly(surface, _curve(
                (265, 246),
                ((393, 177), (503, 109), (558, 73)),
                ((592, 63), (626, 66), (658, 65)),
                ((626, 83), (607, 95), (553, 106)),
                ((446, 148), (350, 207), (265, 246))
            ), (0, 117, 139), side)

            # Тёмный вытянутый островок на крыле.
            _poly(surface, _curve(
                (348, 262),
                ((352, 234), (370, 212), (399, 200)),
                ((430, 189), (453, 173), (478, 163)),
                ((469, 187), (447, 204), (432, 218)),
                ((403, 244), (387, 264), (348, 262))
            ), (0, 28, 65), side)
            _line(surface, _curve((349, 262), ((352, 234), (370, 212), (399, 200))), (2, 94, 116), 3, side)

            # Зеленовато-жёлтая кайма вдоль внутренней стороны крыла.
            stripe = _curve(
                (272, 276),
                ((311, 239), (353, 237), (386, 219)),
                ((435, 192), (478, 157), (533, 138)),
                ((561, 126), (571, 120), (592, 119))
            )
            _line(surface, stripe, (35, 91, 30), 15, side)
            _line(surface, stripe, (166, 203, 25), 10, side)
            _line(surface, stripe, (236, 242, 46), 4, side)
            _line(surface, stripe[8:29], (244, 252, 105), 2, side)

            # Сплошные крупные лаймовые жилки, связывающие крыло с телом.
            core_web = _curve(
                (348, 275),
                ((388, 264), (394, 246), (412, 222)),
                ((447, 184), (493, 165), (555, 151))
            )
            _line(surface, core_web, (27, 97, 57), 21, side)
            _line(surface, core_web, (100, 159, 36), 12, side)
            _line(surface, core_web, (166, 207, 40), 4, side)

            # Хвостовые широкие концы плавников: голубой полупрозрачный край.
            tip = _curve(
                (540, 83),
                ((572, 63), (615, 61), (670, 61)),
                ((653, 93), (625, 134), (612, 164)),
                ((580, 174), (558, 147), (560, 119)),
                ((556, 104), (547, 94), (540, 83))
            )
            _poly(surface, tip, (15, 127, 160), side)
            _poly(surface, _curve(
                (566, 76),
                ((590, 65), (623, 66), (657, 67)),
                ((643, 88), (627, 101), (618, 115)),
                ((600, 105), (583, 87), (566, 76))
            ), (34, 169, 202), side)
            _poly(surface, _curve(
                (593, 73),
                ((624, 72), (639, 72), (662, 66)),
                ((647, 95), (627, 129), (612, 164)),
                ((606, 144), (602, 104), (593, 73))
            ), (37, 159, 193), side)
            _line(surface, _curve((576, 73), ((614, 60), (642, 65), (669, 61))), (66, 222, 237), 3, side)
            _line(surface, _curve((612, 164), ((627, 127), (651, 91), (669, 61))), (9, 80, 106), 2, side)

            # Прожилки, идущие к краю крыла, и поперечные полоски на кончике.
            for i in range(12):
                t = i / 11
                x0 = 559 + 51*t
                y0 = 110 + 51*t
                x1 = 584 + 81*t
                y1 = 73 + 8*t
                _line(surface, _curve((x0, y0),
                                      ((x0+8, y0-17), (x1-7, y1+8), (x1, y1))),
                      (31+int(25*t), 152+int(35*t), 181+int(38*t)), 1, side)
            for i in range(12):
                x = 580 + i*5.7
                y = 86 + math.sin(i*.85)*4
                _line(surface, [(x,y), (x+10, y-2)], (79, 203, 224), 1, side)

            # Небольшие бирюзовые микро-чешуйки на мембране крыла.
            for i in range(520):
                x = rng.uniform(307, 526)
                y = rng.uniform(141, 276)
                if _point_inside_polygon((x,y), fin_path):
                    brightness = rng.random()
                    if brightness < .18:
                        c=(21, 134, 147)
                    elif brightness < .78:
                        c=(3, 84, 105)
                    else:
                        c=(14, 109, 131)
                    _circle(surface, (x,y), 1 if i%4 else 2, c, side)

            # Светящиеся контуры вдоль тела и тонкие жилки у основания.
            _line(surface, _curve(
                (215, 292),
                ((270, 224), (425, 131), (557, 68)),
                ((601, 57), (641, 66), (668, 61))
            ), (0, 184, 190), 2, side)
            _line(surface, _curve(
                (276, 283),
                ((301, 249), (328, 238), (348, 229))
            ), (214, 230, 43), 4, side)

    def _draw_center(surface):
        # Центральное оливковое тело с объёмными плавными наплывами.
        _poly(surface, _curve(
            (214, 299),
            ((255, 282), (309, 270), (348, 276)),
            ((397, 270), (432, 255), (456, 275)),
            ((472, 284), (491, 306), (485, 330)),
            ((489, 358), (464, 393), (443, 402)),
            ((413, 412), (398, 393), (346, 393)),
            ((302, 398), (256, 374), (214, 360)),
            ((199, 347), (199, 315), (214, 299))
        ), (0, 75, 69))

        # Изумрудные и жёлтые поверхностные ленты.
        _poly(surface, _curve(
            (268, 300),
            ((300, 287), (348, 286), (382, 300)),
            ((414, 297), (445, 279), (458, 293)),
            ((472, 307), (470, 337), (448, 348)),
            ((424, 341), (407, 317), (373, 320)),
            ((319, 320), (299, 319), (268, 300))
        ), (57, 148, 61))
        _poly(surface, _curve(
            (282, 353),
            ((333, 333), (391, 347), (429, 352)),
            ((450, 353), (459, 365), (453, 387)),
            ((407, 403), (363, 390), (332, 383)),
            ((315, 378), (293, 370), (282, 353))
        ), (40, 122, 60))

        # Круглая центральная 'пластина' — желтовато-зелёная выпуклость.
        _oval(surface, (415, 276, 90, 120), (20, 83, 55))
        _oval(surface, (423, 280, 75, 112), (73, 137, 43))
        _oval(surface, (429, 285, 65, 102), (115, 163, 33))
        _oval(surface, (437, 291, 54, 91), (143, 176, 34))
        _oval(surface, (447, 303, 41, 66), (164, 189, 42))
        _oval(surface, (442, 311, 39, 54), (152, 180, 34))

        # Тонкие обводы складок вокруг пластины.
        for points, c, w in [
            (_curve((444, 282), ((410, 282), (404, 306), (407, 330)),
                   ((412, 368), (431, 385), (451, 385))), (39, 79, 38), 4),
            (_curve((446, 288), ((418, 293), (414, 307), (414, 332)),
                   ((422, 365), (431, 372), (448, 377))), (182, 209, 60), 3),
            (_curve((450, 300), ((432, 303), (430, 317), (432, 329)),
                   ((437, 349), (444, 360), (455, 361))), (88, 125, 38), 3),
        ]:
            _line(surface, points, c, w)
        _line(surface, _curve((471, 302), ((492, 324), (489, 353), (471, 375))), (196, 210, 49), 2)

        # Гребни и прожилки, расходящиеся к глазам.
        for side in (1, -1):
            _line(surface, _curve((402, 318), ((388, 301), (378, 293), (369, 281))), (23, 92, 64), 9, side)
            _line(surface, _curve((402, 317), ((390, 300), (375, 292), (365, 270))), (128, 180, 40), 5, side)
            _line(surface, _curve((420, 315), ((408, 297), (407, 284), (422, 269))), (192, 219, 51), 2, side)

    def _draw_face(surface):
        # Заострённая треугольная морда и видимая кромка челюсти.
        snout = _curve(
            (207, 288),
            ((232, 280), (258, 298), (280, 306)),
            ((307, 321), (341, 317), (366, 320)),
            ((372, 327), (374, 340), (367, 349)),
            ((337, 356), (311, 343), (281, 358)),
            ((259, 372), (235, 380), (211, 359)),
            ((208, 351), (205, 346), (202, 340)),
            ((206, 327), (201, 299), (207, 288))
        )
        _poly(surface, snout, (1, 63, 82))
        _line(surface, snout[:56], (11, 138, 160), 3)

        # Тёмные, синие лобовые пластины.
        _poly(surface, _curve(
            (207, 289),
            ((234, 283), (267, 298), (283, 309)),
            ((274, 330), (244, 328), (213, 316)),
            ((207, 309), (207, 298), (207, 289))
        ), (0, 112, 141))
        _poly(surface, _curve(
            (210, 356),
            ((235, 368), (268, 362), (285, 348)),
            ((268, 337), (246, 343), (211, 345)),
            ((203, 346), (210, 350), (210, 356))
        ), (2, 82, 118))

        # Рельеф на морде: короткие линии + холодные блики.
        _line(surface, _curve((212, 298), ((235, 307), (251, 309), (260, 313))), (24, 203, 208), 2)
        _line(surface, _curve((219, 292), ((246, 295), (257, 304), (267, 309))), (31, 164, 180), 2)
        _line(surface, _curve((207, 351), ((234, 346), (245, 350), (267, 346))), (22, 153, 170), 3)
        _line(surface, _curve((218, 365), ((238, 376), (256, 368), (276, 357))), (0, 119, 160), 2)

        # Тёмная щель открытого рта и подсвеченные губы.
        mouth = [(206, 327),(220, 323),(241, 328),(260, 331),(268, 334),
                 (259, 340),(238, 343),(222, 349),(205, 342),(201, 335)]
        _poly(surface, mouth, (0, 10, 17))
        _line(surface, [(207,326),(223,321),(241,326),(257,329)], (4, 170, 196), 2)
        _line(surface, [(205,343),(222,351),(242,344),(261,341)], (10, 105, 138), 2)
        _poly(surface, [(219,337),(237,339),(250,337),(233,342)], (54, 65, 65))

        # Маленькие зубы верхнего и нижнего ряда (независимые многоугольники).
        for x, y, size in [(214,326,4),(222,326,5),(232,328,5), (241,329,4),
                            (218,346,4),(228,344,5),(240,343,4)]:
            if y < 337:
                _poly(surface, [(x,y),(x+size,y+1),(x+size//2,y+size+2)], (204, 239, 236))
            else:
                _poly(surface, [(x,y),(x+size,y-1),(x+size//2,y-size-2)], (196, 225, 220))

        # Крохотный нос на самом переднем крае.
        _poly(surface, [(198,309),(210,298),(210,315),(200,318)], (1, 59, 74))
        _line(surface, [(199,309),(205,301),(211,298)], (43, 195, 196), 2)
        _circle(surface, (207,310), 2, (1, 17, 27))

    def _draw_eyes(surface):
        # Два глаза: ярко-жёлтые глазницы, глубина и голубой глянцевый зрачок.
        for side in (1, -1):
            _oval(surface, (268, 240, 72, 83), (0, 37, 38), side)
            _oval(surface, (271, 243, 67, 77), (60, 112, 27), side)
            _oval(surface, (273, 244, 62, 73), (192, 206, 20), side)
            _oval(surface, (277, 248, 54, 65), (239, 245, 36), side)
            _oval(surface, (281, 251, 48, 60), (192, 215, 14), side)

            # Глаз чуть смещён к носу, не строго по центру жёлтого кольца.
            _oval(surface, (290, 254, 35, 52), (0, 32, 43), side)
            _oval(surface, (292, 257, 31, 47), (0, 16, 32), side)
            _oval(surface, (296, 260, 26, 39), (0, 109, 139), side)
            _oval(surface, (299, 264, 21, 31), (15, 159, 190), side)
            _oval(surface, (304, 267, 14, 24), (0, 50, 91), side)
            _circle(surface, (307, 276), 5, (116, 234, 244), side)
            _circle(surface, (307, 277), 2, (235, 252, 254), side)
            _circle(surface, (316, 289), 2, (68, 193, 216), side)

            # Лёгкая зеленоватая окантовка и морщины вокруг орбиты.
            _line(surface, _curve((270, 275), ((271, 249), (287, 240), (307, 238))), (118, 179, 22), 3, side)
            _line(surface, _curve((276, 314), ((293, 326), (315, 325), (331, 305))), (15, 106, 62), 3, side)
            _line(surface, _curve((336, 274), ((349, 271), (359, 268), (367, 264))), (36, 116, 77), 2, side)

    def _add_details(surface):
        rng = random.Random(6080)
        # Точки-поры вокруг носа, мелкие чешуйки на лице.
        for side in (1, -1):
            for i in range(190):
                x = rng.uniform(215, 388)
                y = rng.uniform(274, 319)
                if (x-305)**2/130**2 + (y-297)**2/42**2 < 1:
                    val = rng.randrange(5)
                    colors = [(0, 74, 96), (2, 90, 100), (12, 133, 148), (17, 111, 117), (11, 76, 77)]
                    _circle(surface, (x,y), 1, colors[val], side)
            for t in (0.1, .3, .5, .7):
                x = 380 + 31*t
                y = 289 + 10*t
                _line(surface, [(x,y-7),(x+8,y),(x+5,y+6)], (39, 124, 101), 2, side)

        # На центральной лимонной пластине — нерегулярная крапинка.
        for i in range(265):
            px = rng.uniform(440, 490)
            py = rng.uniform(292, 378)
            if (px-466)**2/25**2 + (py-336)**2/44**2 < 1:
                _circle(surface,(px,py),1,(135+rng.randrange(10),170+rng.randrange(16),38+rng.randrange(12)))

    def _render_master():
        pic = pygame.Surface((ART_W, ART_H), pygame.SRCALPHA)
        pic.fill((0, 0, 0, 0))
        _draw_fins(pic)
        _draw_center(pic)
        _draw_face(pic)
        _draw_eyes(pic)
        _add_details(pic)
        return pic
    return _render_master()


def _create_uploaded_garryfish_source():
    """Оригинальные фигуры из файла Вставленный Markdown.md."""
    ART_W, ART_H = 1540, 900

    _MASTER = None

    _CACHE = {}

    def _rgb(a, b, t):

        return tuple(max(0, min(255, round(a[i]*(1-t) + b[i]*t))) for i in range(3))

    def _bezier(p0, p1, p2, p3, steps=24):

        pts = []

        for i in range(steps+1):

            t = i/steps

            s = 1.0-t

            pts.append((

                s**3*p0[0] + 3*s*s*t*p1[0] + 3*s*t*t*p2[0] + t**3*p3[0],

                s**3*p0[1] + 3*s*s*t*p1[1] + 3*s*t*t*p2[1] + t**3*p3[1],

            ))

        return pts

    def _path(start, *segments):

        result = [start]

        for p1, p2, finish in segments:

            result.extend(_bezier(result[-1], p1, p2, finish)[1:])

        return result

    def _p(surface, vertices, color, stroke=None, sw=1):

        pts = [(round(x), round(y)) for x, y in vertices]

        if len(pts) >= 3:

            pygame.draw.polygon(surface, color, pts)

            if stroke:

                pygame.draw.lines(surface, stroke, True, pts, sw)

    def _l(surface, vertices, color, width=1, closed=False):

        pts = [(round(x), round(y)) for x, y in vertices]

        if len(pts) >= 2:

            pygame.draw.lines(surface, color, closed, pts, max(1, int(width)))

    def _e(surface, x, y, w, h, color, line_width=0):

        pygame.draw.ellipse(surface, color, (round(x), round(y), round(w), round(h)), line_width)

    def _dot(surface, x, y, r, color):

        pygame.draw.circle(surface, color, (round(x), round(y)), max(1, round(r)))

    def _draw_rear_fins(s):

        # Хвостовой треугольный плавник, слегка раздвоенный на самом конце.

        fin = _path((1241, 474),

            ((1312, 464), (1329, 445), (1378, 443)),

            ((1391, 462), (1395, 476), (1422, 477)),

            ((1462, 475), (1483, 480), (1504, 484)),

            ((1459, 488), (1421, 497), (1385, 494)),

            ((1369, 501), (1360, 509), (1327, 505)),

            ((1290, 503), (1269, 491), (1241, 474)))

        _p(s, fin, (73, 52, 62), (143, 83, 76), 2)

        _p(s, _path((1315, 476),

            ((1350, 469), (1372, 463), (1381, 453)),

            ((1392, 461), (1389, 479), (1386, 485)),

            ((1358, 488), (1342, 486), (1315, 476))), (117, 68, 66))

        _l(s, [(1381, 480), (1472, 484), (1495, 482)], (164, 105, 82), 2)

        for i in range(8):

            t = i/7

            _l(s, [(1340, 482+t*6), (1422+52*t, 480+8*t)], (147, 91, 82), 1)

        # Красный высокий второй спинной плавник за корпусом.

        red_dorsal = _path((559, 427),

            ((579, 384), (617, 336), (658, 284)),

            ((647, 330), (637, 377), (630, 440)),

            ((612, 448), (589, 445), (559, 427)))

        _p(s, red_dorsal, (112, 54, 70), (174, 90, 103), 2)

        _p(s, _path((592, 418),

            ((609, 370), (636, 324), (651, 301)),

            ((630, 360), (622, 403), (621, 433)),

            ((612, 435), (602, 430), (592, 418))), (155, 77, 85))

        _l(s, [(656, 286), (622, 361), (604, 408)], (209, 119, 120), 2)

        # Нижняя лента — длинный красно-фиолетовый ус/луч плавника.

        lower = _path((411, 641),

            ((423, 699), (467, 744), (531, 779)),

            ((634, 832), (753, 857), (822, 837)),

            ((750, 867), (619, 864), (519, 805)),

            ((454, 768), (413, 711), (395, 651)),

            ((398, 644), (404, 641), (411, 641)))

        _p(s, lower, (76, 52, 76), (138, 78, 93), 2)

        _l(s, _path((412, 660),

            ((430, 740), (542, 806), (660, 837)),

            ((718, 853), (781, 852), (819, 839))), (193, 105, 125), 2)

        _l(s, _path((408, 666),

            ((432, 735), (512, 782), (613, 810))), (118, 101, 139), 2)

    def _draw_large_dorsal_stalk(s):

        # Очень высокий вертикальный передний плавник — главная особенность вида.

        stalk = _path((237, 488),

            ((231, 390), (239, 283), (222, 179)),

            ((214, 95), (240, 41), (263, 13)),

            ((290, 83), (298, 156), (285, 236)),

            ((272, 321), (284, 382), (315, 425)),

            ((297, 479), (264, 499), (237, 488)))

        _p(s, stalk, (72, 76, 52), (155, 137, 74), 3)

        _p(s, _path((237, 423),

            ((231, 327), (244, 250), (235, 169)),

            ((230, 101), (246, 53), (264, 22)),

            ((277, 91), (280, 162), (266, 220)),

            ((249, 304), (261, 366), (278, 412)),

            ((259, 434), (245, 431), (237, 423))), (42, 75, 87))

        _p(s, _path((254, 43),

            ((229, 118), (232, 187), (255, 249)),

            ((269, 213), (280, 134), (265, 40)),

            ((262, 42), (258, 43), (254, 43))), (61, 105, 143))

        _p(s, _path((254, 43),

            ((239, 130), (251, 177), (256, 219)),

            ((266, 161), (267, 98), (259, 39)),

            ((258, 40), (256, 42), (254, 43))), (82, 128, 182))

        for i in range(8):

            z = i/7

            x = 239 + 8*math.sin(z*6)

            y = 60 + 170*z

            _l(s, [(x, y), (258+10*z, y+27), (248+17*z, y+54)],

               _rgb((99, 137, 177), (163, 154, 92), z), 2)

        _l(s, _path((268, 21),

            ((291, 82), (296, 181), (272, 262)),

            ((268, 333), (267, 390), (307, 435))), (190, 167, 83), 3)

        _l(s, _path((238, 330),

            ((250, 372), (258, 410), (268, 449))), (183, 159, 86), 5)

    def _draw_body(s):

        # Весь силуэт тела + хвостовой стебель. Маленькая треугольная морда слева.

        shape = _path((96, 663),

            ((130, 633), (160, 592), (162, 546)),

            ((159, 462), (195, 377), (271, 354)),

            ((347, 329), (444, 342), (522, 379)),

            ((605, 411), (652, 484), (753, 491)),

            ((862, 485), (1026, 469), (1145, 466)),

            ((1233, 464), (1308, 465), (1376, 481)),

            ((1352, 493), (1288, 499), (1201, 503)),

            ((1053, 509), (943, 521), (813, 554)),

            ((660, 589), (518, 671), (342, 703)),

            ((246, 730), (160, 727), (112, 695)),

            ((101, 690), (93, 677), (96, 663)))

        _p(s, shape, (99, 95, 37), (138, 112, 48), 4)

        # Тёмная нижняя кромка и жёлтая фаска, определяющая объём.

        _p(s, _path((103, 672),

            ((173, 694), (294, 705), (381, 680)),

            ((569, 640), (668, 566), (827, 542)),

            ((1023, 501), (1196, 483), (1352, 485)),

            ((1187, 500), (1033, 506), (809, 555)),

            ((624, 610), (523, 675), (341, 706)),

            ((224, 734), (137, 722), (103, 686)),

            ((101, 681), (102, 675), (103, 672))), (150, 121, 43))

        _p(s, _path((113, 671),

            ((162, 687), (277, 695), (356, 679)),

            ((555, 641), (707, 550), (852, 532)),

            ((1066, 495), (1257, 478), (1331, 483)),

            ((1138, 493), (1019, 505), (827, 542)),

            ((633, 582), (526, 671), (348, 695)),

            ((249, 718), (154, 718), (113, 684)),

            ((112, 681), (112, 676), (113, 671))), (176, 149, 54))

        # Желтоватый узкий светящийся край спинной линии.

        _l(s, _path((167, 546),

            ((163, 467), (207, 382), (272, 356)),

            ((363, 329), (462, 356), (535, 393)),

            ((609, 423), (660, 484), (755, 492)),

            ((895, 485), (1117, 459), (1369, 482))), (174, 145, 58), 10)

        _l(s, _path((174, 532),

            ((174, 450), (221, 383), (275, 358)),

            ((363, 334), (460, 360), (532, 393))), (213, 184, 75), 4)

        # Большой плавник-парус — тёмная оливковая мембрана на боку.

        sail = _path((185, 636),

            ((192, 557), (200, 430), (288, 384)),

            ((374, 355), (464, 378), (523, 421)),

            ((576, 454), (632, 493), (716, 516)),

            ((627, 570), (527, 632), (388, 669)),

            ((296, 696), (228, 689), (185, 636)))

        _p(s, sail, (81, 90, 44), (116, 103, 42), 3)

        # Полутень по нижнему контуру.

        _p(s, _path((205, 603),

            ((260, 617), (384, 650), (542, 600)),

            ((607, 576), (651, 539), (706, 518)),

            ((619, 574), (526, 634), (380, 673)),

            ((263, 695), (219, 678), (205, 603))), (92, 91, 37))

        # Пластины/крупная чешуя с неровными краями — характерный узор рыбы.

        panels = [

            ([(200,439),(236,405),(282,395),(308,424),(310,529),(282,612),(228,617),(201,577)], (105,110,48)),

            ([(273,390),(322,370),(356,370),(378,414),(374,536),(343,628),(299,643),(282,611),(311,521),(305,425)], (113,118,57)),

            ([(348,367),(398,361),(430,379),(444,454),(441,566),(402,631),(361,634),(376,537),(379,424)], (98,105,49)),

            ([(416,373),(468,388),(498,413),(513,492),(488,588),(448,609),(412,569),(443,455),(430,393)], (113,120,60)),

            ([(488,405),(527,425),(555,445),(581,496),(552,567),(496,591),(488,578),(517,492)], (99,106,51)),

            ([(553,456),(607,481),(643,509),(644,538),(592,567),(552,566),(581,502)], (114,115,59)),

            ([(630,492),(678,502),(713,518),(664,549),(629,540)], (81,91,45)),

        ]

        for i, (verts, fill) in enumerate(panels):

            _p(s, verts, fill)

            _l(s, [verts[0], verts[1], verts[2]], (161, 141, 59), 3)

            _l(s, verts[2:-1], _rgb(fill, (63, 68, 33), .37), 2)

            if i < 6:

                x, y = verts[0]

                _l(s, [(x+18, y+20), (x+27, y+82), (x+20, y+127)], (130, 127, 64), 2)

        # Узкие ребра плавника-паруса.

        for i in range(9):

            u = i / 8

            x_top = 232 + i*48

            y_top = 392 + 46*math.sin(u*2)

            x_bottom = 251 + i*42

            y_bottom = 648 - 84*u

            _l(s, _path((x_top,y_top),

                ((x_top+23, y_top+55), (x_bottom+31, y_bottom-68), (x_bottom,y_bottom))),

                (68+i*3, 80+i*2, 39), 2)

        # Тёплая позолота на переднем нижнем крае головы.

        _p(s, _path((100, 659),

            ((113, 634), (139, 616), (160, 608)),

            ((146, 639), (152, 658), (190, 668)),

            ((245, 682), (286, 677), (328, 671)),

            ((259, 701), (155, 706), (109, 688)),

            ((104, 683), (99, 671), (100, 659))), (136, 116, 44))

        _l(s, _path((103, 669),

            ((151, 689), (254, 701), (365, 683))), (215, 172, 56), 3)

        # Тёмная жаберная полоса, глаз не столь заметен как у пискуна.

        _l(s, _path((202, 605),

            ((217, 626), (235, 647), (239, 667))), (103, 87, 41), 5)

        _e(s, 151, 647, 17, 11, (63, 62, 36))

        _e(s, 154, 648, 8, 6, (162, 148, 75))

        _l(s, [(101, 668), (130, 675), (170, 681)], (73, 80, 44), 3)

        _l(s, [(99, 662), (125, 653), (144, 644)], (174, 152, 56), 2)

        _l(s, _path((180, 682),

            ((248, 679), (307, 668), (358, 641))), (190, 161, 62), 2)

        # Продольная боковая линия по хвостовому стеблю.

        _l(s, _path((729, 515),

            ((917, 496), (1115, 471), (1367, 482))), (88, 91, 47), 9)

        _l(s, _path((744, 518),

            ((923, 498), (1128, 474), (1370, 481))), (157, 144, 63), 4)

        _l(s, _path((756, 542),

            ((941, 503), (1135, 494), (1371, 491))), (189, 166, 67), 3)

    def _draw_big_red_fin(s):

        # Очень длинный вытянутый треугольный боковой плавник.

        # Рисуется ПОСЛЕ тела: поверх пластин, как на референсе.

        fin = _path((422, 642),

            ((613, 566), (830, 446), (1044, 388)),

            ((1004, 418), (961, 453), (907, 477)),

            ((737, 560), (574, 644), (424, 656)),

            ((418, 653), (418, 647), (422, 642)))

        _p(s, fin, (118, 55, 61), (77, 48, 56), 2)

        _p(s, _path((443, 640),

            ((614, 568), (831, 445), (1035, 393)),

            ((920, 461), (672, 591), (445, 653)),

            ((444, 650), (443, 645), (443, 640))), (163, 75, 79))

        _p(s, _path((454, 640),

            ((661, 542), (862, 447), (1026, 397)),

            ((848, 462), (660, 558), (456, 644)),

            ((455, 642), (455, 641), (454, 640))), (201, 88, 90))

        _l(s, _path((446, 639),

            ((624, 558), (852, 447), (1041, 390))), (225, 112, 104), 2)

        _l(s, _path((435, 658),

            ((650, 613), (809, 527), (920, 470))), (70, 48, 62), 3)

        # Тонкие продольные жилки.

        for i in range(11):

            t = i/10

            sx = 460 + 170*t

            sy = 643 - 58*t

            ex = 844 + 175*t

            ey = 479 - 82*t

            _l(s, _path((sx, sy),

                ((sx+112, sy-52), (ex-80, ey+28), (ex, ey))),

                _rgb((91, 55, 66), (210, 109, 103), t), 1)

    def _draw_details(s):

        rng = random.Random(94053)

        # Пятна/жилы на парусе (в пределах грубого эллипса паруса).

        for i in range(340):

            x = rng.uniform(225, 605)

            y = rng.uniform(411, 605)

            normal = ((x-407)/218)**2 + ((y-514)/139)**2

            if normal < .78:

                rr = rng.choice((1,1,1,2,2,3))

                _dot(s, x, y, rr, rng.choice((

                    (115, 119, 56), (102, 107, 50), (137, 130, 63),

                    (77, 90, 47), (150, 133, 62))))

        # По хвосту — небольшие тёмно-золотые мазки.

        for i in range(85):

            x = rng.uniform(800, 1280)

            ymid = 508-20*(x-800)/480

            y = ymid + rng.uniform(-9, 14)

            length = rng.uniform(3, 17)

            _l(s, [(x,y),(x+length,y-rng.uniform(-3,3))],

               rng.choice(((93,102,54),(151,137,63),(184,155,72))), 1)

        # Блики на верхней кромке паруса.

        _l(s, _path((266, 359),

            ((375, 320), (457, 351), (530, 388)),

            ((602, 415), (653, 473), (742, 490))), (214, 181, 77), 2)

        _l(s, _path((131, 638),

            ((152, 613), (156, 579), (166, 550))), (197, 161, 55), 3)

    def build_garryfish():

        """Создаёт исходный рисунок Garryfish на прозрачной поверхности."""

        art = pygame.Surface((ART_W, ART_H), pygame.SRCALPHA)

        art.fill((0, 0, 0, 0))

        _draw_rear_fins(art)

        _draw_large_dorsal_stalk(art)

        _draw_body(art)

        _draw_big_red_fin(art)

        _draw_details(art)

        return art
    return build_garryfish()


def _create_uploaded_bladderfish_source():
    """Оригинальные фигуры из файла Вставленный Markdown (2).md."""
    ART_W, ART_H = 920, 620

    _MASTER = None

    def _clamp(v):

        return max(0, min(255, int(v)))

    def _mix(a, b, t):

        return tuple(_clamp(a[i] + (b[i] - a[i]) * t) for i in range(3))

    def _cubic(p0, p1, p2, p3, steps=18):

        pts = []

        for i in range(steps + 1):

            t = i / steps

            u = 1 - t

            pts.append((

                u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],

                u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1],

            ))

        return pts

    def _curve(start, *segments):

        pts = [start]

        cur = start

        for a, b, end in segments:

            pts.extend(_cubic(cur, a, b, end)[1:])

            cur = end

        return pts

    def _poly(surface, pts, color):

        pygame.draw.polygon(surface, color, [(round(x), round(y)) for x, y in pts])

    def _line(surface, pts, color, width=1, closed=False):

        if len(pts) > 1:

            pygame.draw.lines(surface, color, closed, [(round(x), round(y)) for x, y in pts], width)

    def _oval(surface, rect, color, width=0):

        x, y, w, h = rect

        pygame.draw.ellipse(surface, color, pygame.Rect(round(x), round(y), round(w), round(h)), width)

    def _circle(surface, pos, radius, color, width=0):

        pygame.draw.circle(surface, color, (round(pos[0]), round(pos[1])), radius, width)

    def _glow_oval(surface, rect, colors_and_widths):

        """Мягкое свечение за счёт вложенных эллипсов."""

        x, y, w, h = rect

        for color, pad in colors_and_widths:

            _oval(surface, (x - pad, y - pad, w + 2 * pad, h + 2 * pad), color)

    def _draw_bladder(surface):

        # Верхний пузырь.

        _glow_oval(surface, (252, 120, 446, 186), [

            ((104, 98, 171, 0), 0),

        ])

        _oval(surface, (252, 120, 446, 186), (150, 143, 214))

        _oval(surface, (265, 128, 424, 170), (170, 164, 227))

        _oval(surface, (282, 136, 386, 153), (186, 180, 236))

        _oval(surface, (306, 147, 341, 131), (194, 190, 241))

        # Нижний пузырь.

        _oval(surface, (248, 310, 450, 188), (148, 141, 213))

        _oval(surface, (262, 318, 426, 171), (169, 163, 227))

        _oval(surface, (280, 326, 388, 155), (186, 179, 236))

        _oval(surface, (304, 338, 342, 132), (195, 190, 242))

        # Мягкие тени возле центрального тела.

        _oval(surface, (242, 185, 480, 78), (135, 126, 196))

        _oval(surface, (240, 357, 486, 78), (133, 124, 196))

        # Верхние и нижние холодные блики.

        for i in range(9):

            t = i / 8

            c = _mix((183, 195, 255), (243, 240, 255), t)

            _line(surface, _curve((330 + 10*i, 152 - 2*i), ((428 + 12*i, 132 - 3*i), (552 + 6*i, 132 - 2*i), (628 + 2*i, 152 + i))), c, 2)

            _line(surface, _curve((327 + 10*i, 449 + i), ((428 + 12*i, 470 + i), (548 + 8*i, 471 - 1*i), (628 + 2*i, 448 - 1*i))), c, 2)

        # Тонкие внутренние складки пузырей.

        fold_colors = [(177, 168, 232), (161, 153, 220), (193, 188, 243)]

        fold_paths_top = [

            _curve((350, 178), ((425, 157), (518, 156), (600, 175))),

            _curve((334, 203), ((428, 184), (525, 181), (610, 198))),

            _curve((355, 228), ((437, 216), (517, 214), (585, 226))),

        ]

        fold_paths_bottom = [

            _curve((350, 430), ((429, 443), (514, 443), (595, 429))),

            _curve((334, 403), ((425, 417), (521, 419), (609, 407))),

            _curve((358, 377), ((437, 390), (516, 392), (586, 383))),

        ]

        for idx, p in enumerate(fold_paths_top):

            _line(surface, p, fold_colors[idx % len(fold_colors)], 2)

        for idx, p in enumerate(fold_paths_bottom):

            _line(surface, p, fold_colors[idx % len(fold_colors)], 2)

    def _draw_core_body(surface):

        # Основное тело в центре между пузырями.

        body = _curve(

            (153, 311),

            ((214, 264), (326, 252), (473, 267)),

            ((579, 279), (679, 290), (766, 301)),

            ((780, 310), (781, 319), (768, 327)),

            ((676, 338), (573, 349), (469, 362)),

            ((329, 378), (216, 369), (154, 326)),

            ((146, 321), (146, 315), (153, 311))

        )

        _poly(surface, body, (174, 97, 133))

        _poly(surface, _curve(

            (157, 311),

            ((226, 276), (340, 273), (477, 287)),

            ((574, 296), (657, 304), (729, 310)),

            ((655, 318), (573, 326), (478, 336)),

            ((342, 350), (231, 347), (160, 323)),

            ((156, 319), (156, 315), (157, 311))

        ), (198, 124, 153))

        # Нос и рот.

        snout = _curve(

            (114, 310),

            ((120, 274), (153, 256), (187, 266)),

            ((178, 295), (176, 323), (185, 351)),

            ((149, 362), (120, 344), (114, 310))

        )

        _poly(surface, snout, (180, 107, 137))

        _poly(surface, _curve(

            (111, 309),

            ((118, 291), (134, 278), (154, 274)),

            ((167, 283), (171, 295), (172, 305)),

            ((150, 307), (129, 308), (111, 309))

        ), (218, 147, 158))

        mouth = [(110, 309), (132, 305), (160, 305), (172, 310), (161, 317), (132, 318), (114, 314)]

        _poly(surface, mouth, (31, 14, 32))

        _line(surface, [(111, 308), (134, 304), (159, 304), (171, 309)], (244, 196, 192), 2)

        # Хвостовой кончик.

        tail_tip = _curve(

            (763, 301),

            ((805, 305), (826, 311), (851, 309)),

            ((859, 315), (855, 325), (844, 329)),

            ((821, 328), (798, 325), (766, 326)),

            ((763, 319), (762, 311), (763, 301))

        )

        _poly(surface, tail_tip, (206, 141, 167))

        # Спинной и брюшной шов/плавник вдоль тела.

        _line(surface, _curve((193, 304), ((330, 286), (520, 290), (747, 306))), (211, 170, 188), 2)

        _line(surface, _curve((194, 331), ((336, 345), (527, 338), (749, 321))), (152, 73, 108), 2)

    def _draw_eye(surface):

        # Большой глаз с оранжево-золотой радужкой.

        _oval(surface, (102, 255, 105, 96), (63, 44, 66))

        _oval(surface, (109, 261, 92, 83), (228, 177, 120))

        _oval(surface, (117, 268, 75, 69), (214, 125, 72))

        _oval(surface, (126, 276, 58, 54), (243, 225, 170))

        _oval(surface, (135, 284, 40, 38), (70, 40, 60))

        _circle(surface, (155, 303), 12, (15, 10, 20))

        _circle(surface, (149, 295), 4, (255, 255, 255))

        _circle(surface, (163, 311), 2, (255, 233, 206))

        # Окантовка глаза и щёчные линии.

        _line(surface, _curve((102, 302), ((109, 264), (136, 251), (174, 259)), ((198, 271), (204, 301), (198, 327))), (104, 57, 88), 3)

        for shift in (0, 12, 24):

            _line(surface, _curve((116 + shift, 339 - shift * 0.3), ((130 + shift, 332 - shift * 0.2), (147 + shift, 330 - shift * 0.05), (165 + shift, 332))), (235, 195, 216), 2)

    def _draw_spots(surface):

        rng = random.Random(8017)

        # Крупные овальные пятна на центральном теле.

        start_x = 212

        rows = [291, 307, 323, 339]

        for row_i, y in enumerate(rows):

            for i in range(23 - row_i * 2):

                x = start_x + i * 24 + row_i * 8

                r = 10 - row_i

                outer = (237, 210, 227)

                inner = (191, 103, 142)

                _oval(surface, (x - r, y - r * 0.72, r * 2.1, r * 1.45), outer)

                _oval(surface, (x - r + 3, y - r * 0.72 + 2, r * 1.35, r * 0.8), inner)

        # Мелкая текстура на теле.

        for _ in range(240):

            x = rng.uniform(190, 760)

            y = rng.uniform(286, 346)

            if ((x - 470) / 330) ** 2 + ((y - 316) / 58) ** 2 < 1.0:

                col = rng.choice([

                    (197, 111, 148), (219, 172, 190), (235, 204, 218), (163, 87, 123)

                ])

                _circle(surface, (x, y), rng.choice([1, 1, 2]), col)

    def _draw_fins(surface):

        fin_fill = (233, 184, 232)

        fin_inner = (140, 72, 150)

        fin_edge = (255, 188, 250)

        # Верхние маленькие кольцевые плавники.

        top_positions = [355, 483, 610, 708]

        for i, x in enumerate(top_positions):

            y = 98 + (i % 2) * 6

            outer = _curve(

                (x, y),

                ((x + 12, y - 18), (x + 32, y - 18), (x + 43, y - 2)),

                ((x + 38, y + 18), (x + 16, y + 20), (x + 2, y + 7)),

                ((x - 4, y + 3), (x - 2, y + 1), (x, y))

            )

            inner = _curve(

                (x + 8, y + 2),

                ((x + 17, y - 8), (x + 28, y - 9), (x + 33, y)),

                ((x + 29, y + 9), (x + 17, y + 10), (x + 9, y + 4)),

                ((x + 7, y + 3), (x + 7, y + 3), (x + 8, y + 2))

            )

            _poly(surface, outer, fin_edge)

            _poly(surface, inner, (40, 18, 58))

            _line(surface, outer, fin_inner, 2, closed=True)

        # Нижние плавники.

        bottom_positions = [326, 444, 588, 709]

        for i, x in enumerate(bottom_positions):

            y = 519 + (i % 2) * 7

            outer = _curve(

                (x, y),

                ((x + 8, y + 18), (x + 25, y + 24), (x + 40, y + 14)),

                ((x + 35, y - 4), (x + 18, y - 8), (x + 4, y - 5)),

                ((x, y - 2), (x - 1, y - 1), (x, y))

            )

            inner = _curve(

                (x + 10, y + 2),

                ((x + 17, y + 12), (x + 24, y + 14), (x + 30, y + 9)),

                ((x + 27, y + 1), (x + 18, y), (x + 11, y + 1)),

                ((x + 10, y + 2), (x + 10, y + 2), (x + 10, y + 2))

            )

            _poly(surface, outer, fin_edge)

            _poly(surface, inner, (41, 18, 61))

            _line(surface, outer, fin_inner, 2, closed=True)

    def _draw_extra_highlights(surface):

        # Контуры соединения тела с пузырями.

        _line(surface, _curve((196, 282), ((274, 269), (400, 272), (565, 288))), (213, 180, 217), 3)

        _line(surface, _curve((196, 347), ((280, 359), (406, 355), (565, 339))), (134, 88, 138), 3)

        # Небольшой блеск на верхнем пузыре и на нижнем.

        _line(surface, _curve((308, 143), ((378, 129), (473, 129), (574, 143))), (243, 244, 255), 2)

        _line(surface, _curve((309, 457), ((386, 471), (472, 471), (572, 456))), (239, 241, 255), 2)

        # Тонкий блик вдоль носа.

        _line(surface, _curve((118, 287), ((132, 278), (151, 278), (166, 286))), (255, 216, 205), 2)

    def _render_master():

        pic = pygame.Surface((ART_W, ART_H), pygame.SRCALPHA)

        pic.fill((0, 0, 0, 0))

        _draw_bladder(pic)

        _draw_core_body(pic)

        _draw_spots(pic)

        _draw_eye(pic)

        _draw_fins(pic)

        _draw_extra_highlights(pic)

        return pic
    return _render_master()


def _uploaded_fish_sprite(kind, length, width, height_multiplier):
    master = _UPLOADED_SMALL_FAUNA_CACHE.get(kind)
    if master is None:
        draw_func = {
            'boomerang': _create_uploaded_boomerang_source,
            'garryfish': _create_uploaded_garryfish_source,
            'bladderfish': _create_uploaded_bladderfish_source,
        }[kind]
        master = draw_func()
        # Во всех трёх дополнительных файлах голова смотрит влево.
        # В исходной системе игры все рыбки смотрят вправо.
        master = pygame.transform.flip(master, True, False)
        master = _crop_alpha_surface(master)
        _UPLOADED_SMALL_FAUNA_CACHE[kind] = master
    return _fit_small_fauna_proportionally(
        master, length, width, height_multiplier
    )


def generate_uploaded_boomerang_sprite(length, width):
    return _uploaded_fish_sprite('boomerang', length, width, 2.9)


def generate_uploaded_garryfish_sprite(length, width):
    return _uploaded_fish_sprite('garryfish', length, width, 2.7)


def generate_uploaded_bladderfish_sprite(length, width):
    return _uploaded_fish_sprite('bladderfish', length, width, 2.6)



# ============================================================================
# ИСХОДНЫЕ ФИГУРЫ ИЗ ПРИСЛАННЫХ ПОЛЬЗОВАТЕЛЕМ АЛГОРИТМОВ — 10.10.2026
# Изолированные функции: одинаковые имена _curve, _draw_head и _MASTER
# внутри разных рисунков никогда не конфликтуют с основной игрой.
# ============================================================================

def _build_new_crabsnake_source():
    """Сгенерировать мастер-рисунок crabsnake из фигур Pygame."""
    import math

    import random

    import pygame

    CANVAS_W, CANVAS_H = 1480, 780

    def _clamp(v):
        return max(0, min(255, round(v)))

    def _lerp(a, b, t):
        return a + (b - a) * t

    def _bezier(a, b, c, d, steps=25):
        points = []
        for k in range(steps + 1):
            t = k / steps
            u = 1 - t
            points.append((
                u*u*u*a[0] + 3*u*u*t*b[0] + 3*u*t*t*c[0] + t*t*t*d[0],
                u*u*u*a[1] + 3*u*u*t*b[1] + 3*u*t*t*c[1] + t*t*t*d[1],
            ))
        return points

    def _path(start, *segments, steps=25):
        p = [start]
        for b, c, d in segments:
            p.extend(_bezier(p[-1], b, c, d, steps)[1:])
        return p

    def _ints(points):
        return [(round(x), round(y)) for x, y in points]

    def _poly(surf, points, col):
        if len(points) >= 3:
            pygame.draw.polygon(surf, col, _ints(points))

    def _line(surf, points, col, width=1, closed=False):
        if len(points) > 1:
            pygame.draw.lines(surf, col, closed, _ints(points), width)

    def _dot(surf, x, y, radius, col):
        pygame.draw.circle(surf, col, (round(x), round(y)), max(1, round(radius)))

    def _oval(surf, x, y, w, h, col, width=0):
        if w > 0 and h > 0:
            pygame.draw.ellipse(surf, col,
                                (round(x), round(y), max(1, round(w)), max(1, round(h))), width)

    _AXIS = _path(
        (403, 390),
        ((493, 355), (459, 249), (553, 185)),
        ((643, 115), (758, 146), (835, 232)),
        ((924, 333), (928, 410), (1051, 444)),
        ((1163, 471), (1226, 431), (1378, 365)),
        steps=85,
    )

    def _axis(t):
        t = max(0.0, min(1.0, t))
        v = t * (len(_AXIS) - 1)
        j = min(len(_AXIS) - 2, int(v))
        f = v - j
        x = _lerp(_AXIS[j][0], _AXIS[j + 1][0], f)
        y = _lerp(_AXIS[j][1], _AXIS[j + 1][1], f)
        a = _AXIS[max(0, j - 1)]
        b = _AXIS[min(len(_AXIS) - 1, j + 2)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        m = max(0.01, math.hypot(dx, dy))
        return x, y, -dy / m, dx / m

    def _width(t):
        keys = [(0.00,55),(.12,62),(.25,64),(.40,61),(.57,52),(.71,40),(.84,25),(.94,14),(1.,3)]
        for i in range(len(keys) - 1):
            ta, ra = keys[i]
            tb, rb = keys[i + 1]
            if t <= tb:
                v = max(0.0, min(1.0, (t - ta) / (tb - ta)))
                v = v*v*(3 - 2*v)
                return _lerp(ra, rb, v)
        return 3

    def _point(t, normal_multiplier=0.0, extra=0.0):
        x, y, nx, ny = _axis(t)
        n = _width(t) * normal_multiplier + extra
        return x + nx*n, y + ny*n

    def _band(t0, t1, start_offset, end_offset, steps=16):
        a, b = [], []
        for i in range(steps + 1):
            t = _lerp(t0, t1, i / steps)
            aa = start_offset(t) if callable(start_offset) else start_offset
            bb = end_offset(t) if callable(end_offset) else end_offset
            a.append(_point(t, aa))
            b.append(_point(t, bb))
        return a + b[::-1]

    def _stripes_body(surf):
        rng = random.Random(7093)
        t, count = .072, 0
        while t < .958:
            breadth = max(.015, .031 - .009*t)*rng.uniform(.72,1.27)
            begin, stop = t, min(.983, t+breadth)
            col = rng.choice([(92,30,61),(103,32,65),(117,39,67),(73,31,57)])
            polygon = _band(begin,stop,
                            lambda s:-.88+math.sin(70*s+count)*.06,
                            lambda s:.06+math.sin(98*s+count)*.21,steps=9)
            _poly(surf, polygon, col)
            _line(surf,polygon[:10],(155,52,93),2)
            if count % 3 != 0 and stop < .94:
                mid = (begin + stop)/2
                x,y = _point(mid,-.55)
                _oval(surf,x-8,y-4,16,8,(201,76,132))
            t += .041 + .011*math.sin(count*.9)
            count += 1

    def _draw_membrane(surf, side, rng):
        t0,t1 = .075,.99
        steps=230
        root,edge=[],[]
        for k in range(steps+1):
            t = _lerp(t0,t1,k/steps)
            w=(1-t)**.4
            wave=math.sin(t*31+(.7 if side>0 else 2.1))*(10+8*w)
            out=(19+27*w+wave)*min(1.,max(0.,(t1-t)/.10))
            root.append(_point(t,side*.82))
            edge.append(_point(t,side*1.06,side*out))
        _poly(surf,root+edge[::-1],(102,118,169,168))
        _poly(surf,[_point(_lerp(t0,t1,k/steps),side*.93) for k in range(steps+1)] +
              [_point(_lerp(t0,t1,k/steps),side*1.07,side*(13+13*math.sin(k/steps*31)))
               for k in range(steps,-1,-1)],(175,169,221,103))
        _line(surf,edge,(199,193,241,200),3)
        _line(surf,root,(194,191,235,140),2)
        for i in range(65):
            t=t0+(t1-t0)*i/65
            if t>=.972:continue
            wave=math.sin(t*31+(.7 if side>0 else 2.1))*(10+8*(1-t)**.4)
            out=(19+27*(1-t)**.4+wave)*min(1.,max(0.,(t1-t)/.1))
            _line(surf,[_point(t,side*.84),_point(t,side*1.06,side*out)],(191,207,241,100),1)

    def _draw_body(surf):
        fins=pygame.Surface((CANVAS_W,CANVAS_H),pygame.SRCALPHA)
        for side in (-1,1):
            _draw_membrane(fins,side,random.Random(940))
        surf.blit(fins,(0,0))
        _poly(surf,_band(0,1,-1.,1.,steps=360),(51,40,80))
        _poly(surf,_band(0,1,-.88,.91,steps=360),(112,76,112))
        _poly(surf,_band(0,1,.31,.95,steps=360),(174,168,196))
        _poly(surf,_band(0,1,.50,.91,steps=360),(211,205,220))
        _poly(surf,_band(0,1,.73,.89,steps=360),(235,229,237))
        _line(surf,[_point(i/355,.37) for i in range(356)],(105,84,124),5)
        _line(surf,[_point(i/355,.55) for i in range(356)],(221,206,225),2)
        _poly(surf,_band(0,1,-.97,.20,steps=360),(150,45,93))
        _poly(surf,_band(0,1,-.86,-.12,steps=360),(204,69,127))
        _poly(surf,_band(0,1,-.72,-.42,steps=360),(232,95,156))
        _stripes_body(surf)
        _line(surf,[_point(i/350,-.92) for i in range(351)],(241,139,181),3)
        _line(surf,[_point(i/350,.29) for i in range(351)],(109,77,124),3)
        for k in range(67):
            t=.07+k*.0133
            if t>.96:break
            _line(surf,[_point(t,.47),_point(t+.003,.88)],(191,179,210),1)
        rng=random.Random(28093)
        for k in range(1480):
            t=rng.uniform(.04,.95)
            offset=rng.uniform(-.87,.19)
            x,y=_point(t,offset)
            c=rng.choice([(165,60,113),(230,126,173),(114,42,79),(241,158,196),(187,66,124)])
            _dot(surf,x,y,rng.choice((1,1,2,2,3)),c)
        for t in (.105,.13,.204,.247,.274,.335,.36,.405,.48,.503,.566,.62,.656,.71,.77,.83):
            x,y=_point(t,-.73)
            s=.7+.3*math.sin(t*100)
            _oval(surf,x-9*s,y-6*s,19*s,14*s,(100,54,133))
            _oval(surf,x-6*s,y-5*s,13*s,8*s,(181,95,199))
            _dot(surf,x-3*s,y-3*s,2.5*s,(244,174,243))
        for t in (.12,.22,.38,.53,.68):
            x,y=_point(t,-.53)
            for j in range(5):
                a=j*math.tau/5
                r=5 if j%2==0 else 3
                xx=x+math.cos(a)*12
                yy=y+math.sin(a)*9
                _dot(surf,xx,yy,r+1,(96,51,135))
                _dot(surf,xx-1,yy-2,r,(196,127,225))
        for k in range(170):
            t=rng.uniform(.12,.90)
            of=rng.uniform(.52,.84)
            x,y=_point(t,of)
            if rng.random()<.3:
                _dot(surf,x,y,rng.choice([1,2,2,3]),(184,221,245))

    def _draw_head_back(surf):
        neck=_path((445,316),((477,321),(505,350),(501,382)),
                   ((496,416),(470,451),(429,466)),((399,458),(381,432),(379,393)),
                   ((395,350),(411,325),(445,316)))
        _poly(surf,neck,(81,48,86))
        _line(surf,neck,(197,115,168),3,closed=True)
        for k in range(7):
            x=404+k*10
            _line(surf,_path((x,336),((x+18,362),(x+12,408),(x+5,446))),
                  (133+k*6,75+k*4,127+k*4),2)
        chin=_path((213,371),((231,426),(267,474),(332,488)),
                   ((377,497),(421,476),(444,432)),((433,391),(408,379),(363,376)),
                   ((290,359),(244,356),(213,371)))
        _poly(surf,chin,(180,170,191))
        _poly(surf,_path((226,405),((261,455),(297,477),(345,477)),
                         ((382,477),(417,454),(434,423)),
                         ((364,430),(300,415),(226,405))),(223,208,218))
        _line(surf,_path((243,455),((297,491),(384,491),(429,447))),(240,218,224),2)
        shell=_path((214,360),((202,332),(213,301),(247,279)),
                    ((292,245),(385,253),(446,307)),((460,323),(467,345),(466,367)),
                    ((445,378),(414,389),(367,395)),((304,401),(256,393),(214,360)))
        _poly(surf,shell,(100,38,76))
        _poly(surf,_path((221,341),((224,317),(247,289),(273,278)),
                         ((327,255),(391,272),(437,321)),((440,335),(438,347),(431,356)),
                         ((372,366),(302,359),(221,341))),(211,68,123))
        _poly(surf,_path((238,316),((280,273),(354,272),(402,296)),
                         ((379,301),(314,300),(278,326)),((265,327),(251,323),(238,316))),(237,100,154))
        dark_marks=[
            _path((271,297),((296,283),(308,285),(321,289)),((317,301),(301,307),(278,317))),
            _path((330,278),((347,278),(355,284),(364,292)),((363,306),(354,316),(347,326)),
                  ((333,314),(324,297),(330,278))),
            _path((391,299),((408,307),(420,319),(427,331)),((417,335),(404,332),(390,322)))
        ]
        for mark in dark_marks:_poly(surf,mark,(90,35,68))
        for p in (_path((235,335),((290,307),(346,321),(411,345))),
                  _path((248,344),((299,323),(371,337),(437,358))),
                  _path((242,358),((296,350),(378,370),(440,368)))):
            _line(surf,p,(241,126,176),2)
        _line(surf,shell,(81,37,74),5,closed=True)
        _line(surf,_path((226,309),((279,255),(376,256),(442,319))),(251,152,198),3)
        rng=random.Random(572)
        for k in range(170):
            xx=rng.uniform(255,427)
            yy=rng.uniform(288,352)
            c=rng.choice([(153,48,94),(234,126,174),(109,37,75)])
            _dot(surf,xx,yy,rng.choice([1,1,2,3]),c)
        for xx,yy in [(299,308),(320,308),(354,326),(393,321),(374,304)]:
            _oval(surf,xx-6,yy-4,12,9,(96,41,101))
            _dot(surf,xx-1,yy-1,2,(213,137,206))

    def _draw_mouth_and_claws(surf):
        mouth=_path((202,353),((245,344),(296,354),(333,373)),
                    ((340,395),(326,426),(295,434)),((253,432),(215,409),(192,380)),
                    ((187,369),(192,359),(202,353)))
        _poly(surf,mouth,(40,20,47))
        _poly(surf,_path((213,366),((243,359),(294,370),(317,386)),
                         ((309,410),(290,415),(266,408)),
                         ((242,395),(222,389),(213,366))),(87,37,72))
        _line(surf,_path((198,357),((248,341),(307,354),(336,383))),(141,62,108),6)
        _line(surf,_path((200,385),((242,423),(285,446),(322,416))),(216,147,174),4)
        for x,y,ang in [(245,372,-1),(269,382,1),(299,383,-1),(314,393,1)]:
            tipx=x-19+4*ang
            tipy=y+34+ang*4
            _poly(surf,[(x-7,y),(x+9,y+2),(x+7,y+18),(tipx,tipy)],(247,218,136))
            _poly(surf,[(x-4,y+2),(x+4,y+4),(tipx,tipy)],(252,244,190))
            _line(surf,[(x-7,y),(tipx,tipy)],(171,120,75),2)
        claw_defs=[
            ((272,363),(213,382),(157,440),(141,503),-1),
            ((333,402),(276,440),(243,495),(231,558),1),
        ]
        for idx,(root,neck,fold,tip,order) in enumerate(claw_defs):
            x0,y0=root
            x1,y1=neck
            x2,y2=fold
            x3,y3=tip
            claw=_path((x0-20,y0-14),
                       ((x0-30,y0+17),(x1-20,y1+11),(x1-13,y1+20)),
                       ((x2-21,y2-9),(x2-13,y2+3),(x2-5,y2+8)),
                       ((x2+10,y2+7),(x2+27,y2-1),(x2+33,y2-17)),
                       ((x1+23,y1-36),(x0+12,y0-27),(x0-20,y0-14)))
            _poly(surf,claw,(82,95,144))
            _poly(surf,_path((x0-19,y0-7),
                             ((x0-16,y0+11),(x1-13,y1+5),(x1-8,y1+17)),
                             ((x2-8,y2+3),(x2+5,y2+4),(x2+13,y2-7)),
                             ((x1+21,y1-24),(x0+7,y0-18),(x0-19,y0-7))),(152,180,210))
            _line(surf,claw,(46,51,84),4,closed=True)
            for q in range(3):
                tt=q/3
                xx=_lerp(x0,x2,tt)
                yy=_lerp(y0,y2,tt)
                _line(surf,[(xx-11,yy-10),(xx+14,yy-7)],(206,212,237),2)
            _line(surf,_path((x0-11,y0),((x1-12,y1-4),(x2-5,y2-3),(x2+12,y2-7))),
                  (213,225,244),3)
            point=_path((x2-7,y2+4),
                        ((x2-3,y2+23),(x3-5,y3-15),(x3,y3)),
                        ((x3+10,y3-19),(x2+19,y2+12),(x2+16,y2-7)),
                        ((x2+6,y2-8),(x2-3,y2-2),(x2-7,y2+4)))
            _poly(surf,point,(29,31,49))
            _poly(surf,[(x2+1,y2+7),(x3,y3),(x2+9,y2+4)],(15,15,28))
            _line(surf,_path((x2+11,y2-6),((x2+7,y2+19),(x3,y3-18),(x3,y3))),
                  (94,111,146),2)
        _line(surf,_path((220,415),((257,441),(296,448),(323,418))),(211,173,207),3)
        _line(surf,_path((217,390),((250,391),(276,398),(298,417))),(114,78,125),2)

    def _render_master():
        result=pygame.Surface((CANVAS_W,CANVAS_H),pygame.SRCALPHA)
        result.fill((0,0,0,0))
        _draw_body(result)
        _draw_head_back(result)
        _draw_mouth_and_claws(result)
        return result

    return _render_master()



def _build_new_boneshark_source():
    """Сгенерировать мастер-рисунок boneshark из фигур Pygame."""
    import math

    import random

    import pygame

    ART_W, ART_H = 1500, 700

    MID_Y = ART_H / 2

    _MASTER = None

    def _clamp(v):

        return max(0, min(255, int(v)))

    def _mix(a, b, t):

        return tuple(_clamp(a[i] + (b[i] - a[i]) * t) for i in range(3))

    def _cubic(p0, p1, p2, p3, steps=24):

        pts = []

        for i in range(steps + 1):

            t = i / steps

            u = 1 - t

            pts.append((

                u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],

                u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1],

            ))

        return pts

    def _curve(start, *segments):

        pts = [start]

        cur = start

        for a, b, end in segments:

            pts.extend(_cubic(cur, a, b, end)[1:])

            cur = end

        return pts

    def _mirror(points, side=1):

        if side == 1:

            return points

        return [(x, 2 * MID_Y - y) for x, y in points]

    def _poly(surface, points, color, side=1):

        pygame.draw.polygon(surface, color, [(round(x), round(y)) for x, y in _mirror(points, side)])

    def _line(surface, points, color, width=1, side=1, closed=False):

        pts = _mirror(points, side)

        if len(pts) > 1:

            pygame.draw.lines(surface, color, closed, [(round(x), round(y)) for x, y in pts], width)

    def _oval(surface, rect, color, side=1, width=0):

        x, y, w, h = rect

        if side == -1:

            y = 2 * MID_Y - y - h

        pygame.draw.ellipse(surface, color, pygame.Rect(round(x), round(y), round(w), round(h)), width)

    def _circle(surface, pos, r, color, side=1, width=0):

        x, y = pos

        if side == -1:

            y = 2 * MID_Y - y

        pygame.draw.circle(surface, color, (round(x), round(y)), max(1, round(r)), width)

    def _glow_line(surface, points, palette, side=1):

        for color, width in palette:

            _line(surface, points, color, width, side)

    def _draw_tail(surface):

        # Стебель хвоста — сужающийся и более живой по форме.

        stem = _curve(

            (382, 302),

            ((331, 308), (273, 319), (219, 333)),

            ((197, 340), (180, 346), (162, 350)),

            ((180, 354), (197, 360), (219, 367)),

            ((273, 381), (331, 392), (382, 398)),

            ((392, 381), (393, 319), (382, 302))

        )

        _poly(surface, stem, (114, 109, 150))

        _poly(surface, _curve(

            (382, 312),

            ((336, 317), (280, 327), (229, 340)),

            ((210, 344), (196, 347), (183, 350)),

            ((196, 353), (210, 356), (229, 360)),

            ((280, 373), (336, 383), (382, 388)),

            ((388, 376), (389, 324), (382, 312))

        ), (144, 137, 176))



        # Большие хвостовые лопасти.

        for side in (1, -1):

            fin = _curve(

                (166, 350),

                ((135, 312), (95, 235), (60, 155)),

                ((78, 145), (104, 149), (130, 165)),

                ((164, 210), (187, 262), (202, 320)),

                ((189, 332), (178, 341), (166, 350))

            )

            _poly(surface, fin, (193, 186, 206), side)

            _poly(surface, _curve(

                (168, 350),

                ((141, 316), (106, 252), (76, 183)),

                ((89, 178), (108, 181), (127, 194)),

                ((152, 230), (171, 273), (184, 322)),

                ((178, 332), (173, 341), (168, 350))

            ), (221, 212, 226), side)

            _line(surface, fin, (136, 124, 154), 2, side, closed=True)



            # Прожилки и мягкие лиловые полосы.

            for i in range(7):

                t = i / 6

                p = _curve((166, 350),

                           ((152 - 4 * i, 327 - 10 * i), (119 - 6 * i, 262 - 8 * i), (82 - 3 * i, 190 - 6 * i)))

                _line(surface, p, _mix((221, 209, 223), (166, 149, 187), t), 1, side)

            for i in range(4):

                p = _curve((92 + i * 7, 186 + i * 10), ((118 + i * 4, 195 + i * 8), (142 + i * 4, 220 + i * 8), (166, 252 + i * 10)))

                _line(surface, p, (233, 217, 221), 1, side)



        _line(surface, [(383, 322), (355, 329), (301, 339), (248, 346), (197, 350)], (181, 168, 200), 1)

        _line(surface, [(383, 378), (355, 371), (301, 361), (248, 354), (197, 350)], (181, 168, 200), 1)

    def _draw_spine(surface):

        # Центральная ось между сегментами — глубже и темнее.

        core = _curve(

            (370, 316),

            ((505, 292), (694, 285), (954, 292)),

            ((1002, 309), (1004, 391), (952, 408)),

            ((691, 415), (503, 408), (370, 384)),

            ((360, 372), (360, 328), (370, 316))

        )

        _poly(surface, core, (98, 91, 132))

        _poly(surface, _curve(

            (389, 322),

            ((519, 303), (699, 298), (937, 303)),

            ((972, 315), (973, 385), (936, 397)),

            ((697, 402), (518, 397), (389, 378)),

            ((384, 369), (384, 331), (389, 322))

        ), (128, 120, 163))

    def _draw_segment(surface, cx, cy, w, h, seed, front_emphasis=0.0):

        outer = (129, 123, 162)

        mid = (176, 164, 191)

        inner = (155, 144, 179)

        edge = (95, 88, 123)

        gold = (226, 191, 116)



        x, y = cx - w / 2, cy - h / 2

        _oval(surface, (x, y, w, h), outer)

        _oval(surface, (x + 8, y + 7, w - 16, h - 14), mid)

        _oval(surface, (x + 22, y + 18, w - 44, h - 36), inner)



        # Передняя часть сегмента сильнее подсвечена у головных сегментов.

        glow_col = _mix((191, 170, 114), (245, 209, 126), front_emphasis)

        ridge = _curve((cx + w * 0.1, cy - h * 0.44),

                       ((cx + w * 0.34, cy - h * 0.2), (cx + w * 0.34, cy + h * 0.2), (cx + w * 0.1, cy + h * 0.44)))

        _line(surface, ridge, glow_col, 2)



        # Сетчатый жёлто-розовый рисунок.

        rng = random.Random(seed)

        for _ in range(28):

            ang = rng.uniform(0, math.tau)

            rr = rng.uniform(0.05, 0.85)

            px = cx + math.cos(ang) * (w * 0.30 * rr)

            py = cy + math.sin(ang) * (h * 0.24 * rr)

            rx = rng.uniform(8, 17)

            ry = rx * rng.uniform(0.55, 0.8)

            _oval(surface, (px - rx, py - ry, 2 * rx, 2 * ry), (214, 177, 103))

            _oval(surface, (px - rx * 0.68, py - ry * 0.62, 1.36 * rx, 1.24 * ry), (189, 141, 109))



        # Короткие текстурные прожилки.

        for j in range(5):

            dy = -h * 0.22 + j * h * 0.11

            p = _curve((cx - w * 0.23, cy + dy),

                       ((cx - w * 0.06, cy + dy - 3), (cx + w * 0.08, cy + dy + 3), (cx + w * 0.23, cy + dy)))

            _line(surface, p, (202, 191, 215), 1)



        _oval(surface, (x, y, w, h), edge, width=2)

    def _draw_segments(surface):

        # Сегменты с более точными пропорциями: от мелких у хвоста к широким в центре, затем чуть уже к голове.

        segments = [

            (420, 350, 78, 52, 1001, 0.0),

            (473, 350, 93, 62, 1002, 0.02),

            (532, 350, 106, 74, 1003, 0.04),

            (599, 350, 122, 86, 1004, 0.08),

            (676, 350, 142, 104, 1005, 0.12),

            (767, 350, 163, 124, 1006, 0.22),

            (874, 350, 182, 145, 1007, 0.35),

            (994, 350, 194, 163, 1008, 0.46),

            (1113, 350, 171, 155, 1009, 0.55),

        ]



        _draw_spine(surface)

        for cx, cy, w, h, seed, emph in segments:

            _draw_segment(surface, cx, cy, w, h, seed, emph)

    def _draw_side_spines(surface):

        # Ближе к голове — длинные шипы и брюшные плавники.

        for side in (1, -1):

            large_fin = _curve(

                (1018, 378),

                ((1003, 406), (976, 456), (939, 526)),

                ((955, 532), (972, 522), (989, 507)),

                ((1018, 464), (1042, 429), (1063, 400)),

                ((1051, 387), (1035, 380), (1018, 378))

            )

            _poly(surface, large_fin, (144, 144, 177), side)

            _poly(surface, _curve(

                (1020, 380),

                ((1008, 406), (985, 447), (956, 501)),

                ((969, 503), (983, 494), (998, 481)),

                ((1020, 448), (1040, 420), (1056, 398)),

                ((1045, 389), (1033, 383), (1020, 380))

            ), (177, 176, 196), side)

            _line(surface, large_fin, (101, 95, 130), 2, side, closed=True)



            rear_fin = _curve(

                (1128, 371),

                ((1124, 339), (1121, 281), (1123, 209)),

                ((1142, 200), (1156, 209), (1165, 227)),

                ((1162, 275), (1156, 320), (1149, 363)),

                ((1143, 370), (1136, 372), (1128, 371))

            )

            _poly(surface, rear_fin, (133, 131, 168), side)

            _poly(surface, _curve(

                (1131, 370),

                ((1128, 340), (1127, 292), (1128, 234)),

                ((1140, 228), (1148, 234), (1154, 247)),

                ((1151, 282), (1147, 322), (1142, 365)),

                ((1139, 368), (1135, 370), (1131, 370))

            ), (168, 165, 190), side)

            _line(surface, rear_fin, (95, 90, 126), 2, side, closed=True)



            # Малые боковые шипы у шеи.

            neck_spike = _curve(

                (1184, 335),

                ((1198, 319), (1211, 302), (1223, 285)),

                ((1227, 291), (1226, 299), (1223, 308)),

                ((1212, 323), (1199, 335), (1188, 343)),

                ((1183, 341), (1182, 338), (1184, 335))

            )

            _poly(surface, neck_spike, (135, 130, 170), side)

            _poly(surface, _curve(

                (1186, 336),

                ((1198, 323), (1208, 309), (1217, 296)),

                ((1219, 300), (1218, 306), (1216, 313)),

                ((1206, 325), (1196, 334), (1189, 338)),

                ((1186, 338), (1185, 337), (1186, 336))

            ), (171, 164, 194), side)

    def _draw_head(surface):

        # Более точная ромбовидная голова с массивным "капюшоном".

        head = _curve(

            (1148, 220),

            ((1227, 184), (1316, 184), (1402, 229)),

            ((1445, 281), (1469, 318), (1485, 350)),

            ((1469, 382), (1445, 419), (1402, 471)),

            ((1315, 516), (1226, 516), (1148, 480)),

            ((1118, 440), (1103, 396), (1096, 350)),

            ((1103, 304), (1119, 260), (1148, 220))

        )

        _poly(surface, head, (128, 122, 160))

        _poly(surface, _curve(

            (1160, 232),

            ((1231, 202), (1308, 204), (1378, 241)),

            ((1416, 287), (1438, 318), (1453, 350)),

            ((1438, 382), (1416, 413), (1378, 459)),

            ((1308, 496), (1231, 498), (1160, 468)),

            ((1137, 433), (1126, 393), (1120, 350)),

            ((1126, 307), (1138, 267), (1160, 232))

        ), (156, 146, 183))



        # Золотистая морда-нос.

        nose = _curve(

            (1302, 242),

            ((1347, 254), (1390, 289), (1420, 350)),

            ((1390, 411), (1347, 446), (1302, 458)),

            ((1244, 444), (1205, 407), (1189, 350)),

            ((1206, 293), (1245, 256), (1302, 242))

        )

        _poly(surface, nose, (214, 179, 116))

        _poly(surface, _curve(

            (1298, 259),

            ((1338, 270), (1374, 300), (1398, 350)),

            ((1374, 400), (1338, 430), (1298, 441)),

            ((1254, 431), (1225, 399), (1213, 350)),

            ((1226, 301), (1255, 269), (1298, 259))

        ), (231, 200, 147))



        # Центральная впадина/рот и шейные складки.

        mouth = _curve(

            (1178, 298),

            ((1203, 309), (1219, 327), (1227, 350)),

            ((1219, 373), (1203, 391), (1178, 402)),

            ((1156, 392), (1143, 373), (1136, 350)),

            ((1144, 327), (1157, 308), (1178, 298))

        )

        _poly(surface, mouth, (84, 61, 111))

        _poly(surface, _curve(

            (1182, 308),

            ((1199, 318), (1210, 332), (1216, 350)),

            ((1210, 368), (1199, 382), (1182, 392)),

            ((1168, 383), (1159, 368), (1153, 350)),

            ((1159, 332), (1168, 317), (1182, 308))

        ), (104, 78, 131))



        # Складки у основания головы.

        for side in (1, -1):

            for i in range(6):

                p = _curve((1142 + i * 10, 350), ((1157 + i * 5, 336 - i * 5), (1170 + i * 5, 314 - i * 9), (1180 + i * 5, 291 - i * 12)))

                _line(surface, p, _mix((96, 76, 121), (140, 113, 159), i / 5), 2, side)



        # Передние рога головы.

        for side in (1, -1):

            horn = _curve(

                (1217, 260),

                ((1244, 243), (1277, 222), (1312, 198)),

                ((1319, 206), (1318, 218), (1311, 229)),

                ((1280, 249), (1248, 264), (1222, 278)),

                ((1216, 272), (1214, 266), (1217, 260))

            )

            _poly(surface, horn, (138, 132, 169), side)

            _poly(surface, _curve(

                (1221, 262),

                ((1246, 248), (1273, 230), (1299, 212)),

                ((1304, 218), (1303, 226), (1298, 234)),

                ((1271, 251), (1247, 263), (1224, 273)),

                ((1220, 270), (1219, 266), (1221, 262))

            ), (171, 164, 193), side)



        # Рёбра на морде для костяного узора.

        for i in range(6):

            x0 = 1251 + i * 18

            _line(surface, _curve((x0, 281), ((x0 + 12, 301), (x0 + 18, 326), (x0 + 22, 350))), (244, 216, 168), 1)

            _line(surface, _curve((x0, 419), ((x0 + 12, 399), (x0 + 18, 374), (x0 + 22, 350))), (244, 216, 168), 1)

    def _draw_texture(surface):

        rng = random.Random(7777)



        # Мелкая "чешуя" / крапинка по телу и голове.

        for _ in range(1500):

            x = rng.uniform(360, 1450)

            y = rng.uniform(170, 530)

            if ((x - 950) / 640) ** 2 + ((y - 350) / 190) ** 2 < 1.0:

                r = rng.choice([1, 1, 1, 2])

                col = rng.choice([

                    (165, 155, 187), (134, 127, 163), (218, 187, 119),

                    (96, 89, 124), (192, 178, 210), (225, 205, 161)

                ])

                _circle(surface, (x, y), r, col)



        # Продольные лилово-золотистые блики.

        for i in range(9):

            t = i / 8

            upper = _curve((430 + i * 12, 309), ((635 + i * 8, 292 + i * 2), (887 + i * 5, 289 + i * 6), (1145, 309 + i * 2)))

            lower = _curve((430 + i * 12, 391), ((635 + i * 8, 408 - i * 2), (887 + i * 5, 411 - i * 6), (1145, 391 - i * 2)))

            _line(surface, upper, _mix((183, 172, 204), (241, 209, 143), t), 1)

            _line(surface, lower, _mix((141, 133, 177), (204, 174, 118), t), 1)



        # Жёсткий контур головы и тела.

        body_outline = _curve(

            (1148, 220),

            ((1227, 184), (1316, 184), (1402, 229)),

            ((1445, 281), (1469, 318), (1485, 350)),

            ((1469, 382), (1445, 419), (1402, 471)),

            ((1315, 516), (1226, 516), (1148, 480)),

            ((1118, 440), (1103, 396), (1096, 350)),

            ((1103, 304), (1119, 260), (1148, 220))

        )

        _line(surface, body_outline, (104, 97, 129), 2, closed=True)



        # Дополнительный мягкий контур хвоста и сегментов.

        _line(surface, _curve((382, 302), ((331, 308), (273, 319), (219, 333)), ((197, 340), (180, 346), (162, 350))), (107, 97, 132), 2)

        _line(surface, _curve((382, 398), ((331, 392), (273, 381), (219, 367)), ((197, 360), (180, 354), (162, 350))), (107, 97, 132), 2)

    def _render_master():

        pic = pygame.Surface((ART_W, ART_H), pygame.SRCALPHA)

        pic.fill((0, 0, 0, 0))

        _draw_tail(pic)

        _draw_segments(pic)

        _draw_side_spines(pic)

        _draw_head(pic)

        _draw_texture(pic)

        return pic

    return _render_master()



def _build_new_gasopod_source():
    """Сгенерировать мастер-рисунок gasopod из фигур Pygame."""
    import math

    import random

    import pygame

    ART_W, ART_H = 1280, 760

    _MASTER = None

    def _clamp(v):

        return max(0, min(255, int(v)))

    def _mix(a, b, t):

        return tuple(_clamp(a[i] + (b[i] - a[i]) * t) for i in range(3))

    def _cubic(p0, p1, p2, p3, steps=18):

        pts = []

        for i in range(steps + 1):

            t = i / steps

            u = 1 - t

            pts.append((

                u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],

                u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1],

            ))

        return pts

    def _curve(start, *segments):

        pts = [start]

        cur = start

        for a, b, end in segments:

            pts.extend(_cubic(cur, a, b, end)[1:])

            cur = end

        return pts

    def _poly(surface, pts, color):

        pygame.draw.polygon(surface, color, [(round(x), round(y)) for x, y in pts])

    def _line(surface, pts, color, width=1, closed=False):

        if len(pts) > 1:

            pygame.draw.lines(surface, color, closed, [(round(x), round(y)) for x, y in pts], width)

    def _oval(surface, rect, color, width=0):

        x, y, w, h = rect

        pygame.draw.ellipse(surface, color, pygame.Rect(round(x), round(y), round(w), round(h)), width)

    def _circle(surface, pos, radius, color, width=0):

        pygame.draw.circle(surface, color, (round(pos[0]), round(pos[1])), radius, width)

    def _bead_line(surface, pts, colors_and_widths):

        for color, width in colors_and_widths:

            _line(surface, pts, color, width)

    def _draw_spot_cluster(surface, center, radius, seed=0):

        rng = random.Random(seed)

        cx, cy = center

        for _ in range(55):

            ang = rng.uniform(0, math.tau)

            rr = radius * math.sqrt(rng.random())

            x = cx + math.cos(ang) * rr

            y = cy + math.sin(ang) * rr * 0.82

            r = rng.uniform(2.5, 9.5)

            color = rng.choice([

                (35, 45, 48), (47, 58, 61), (56, 67, 69), (26, 33, 36)

            ])

            _oval(surface, (x - r * 0.9, y - r * 0.6, r * 1.8, r * 1.2), color)

    def _draw_glow_spot(surface, x, y, r):

        # Внешняя зелёно-жёлтая аура.

        for mul, color in [

            (1.9, (40, 52, 18)),

            (1.6, (72, 82, 22)),

            (1.3, (107, 112, 26)),

            (1.05, (155, 165, 35)),

        ]:

            _circle(surface, (x, y), max(1, round(r * mul)), color)

        _circle(surface, (x, y), max(1, round(r * 0.82)), (220, 235, 50))

        _circle(surface, (x - r * 0.18, y - r * 0.22), max(1, round(r * 0.24)), (252, 250, 147))

    def _draw_main_body(surface):

        # Основной силуэт корпуса.

        body = _curve(

            (154, 392),

            ((194, 298), (335, 222), (523, 212)),

            ((651, 202), (796, 223), (915, 269)),

            ((996, 295), (1061, 336), (1094, 385)),

            ((1090, 445), (1056, 500), (994, 532)),

            ((914, 574), (809, 591), (682, 590)),

            ((533, 593), (373, 571), (248, 536)),

            ((173, 506), (141, 454), (154, 392))

        )

        _poly(surface, body, (68, 79, 78))



        # Брюхо светлее.

        belly = _curve(

            (396, 479),

            ((505, 458), (633, 455), (785, 461)),

            ((843, 467), (894, 490), (921, 523)),

            ((824, 565), (662, 573), (510, 568)),

            ((440, 564), (380, 536), (396, 479))

        )

        _poly(surface, belly, (174, 184, 177))

        _poly(surface, _curve(

            (430, 487),

            ((534, 476), (643, 476), (764, 483)),

            ((808, 492), (843, 505), (866, 523)),

            ((786, 551), (664, 558), (545, 555)),

            ((473, 553), (425, 529), (430, 487))

        ), (196, 203, 196))



        # Верхние тёмные пластины и общий оттенок спины.

        top_mass = _curve(

            (234, 318),

            ((328, 256), (467, 228), (641, 235)),

            ((767, 243), (866, 271), (953, 322)),

            ((964, 362), (942, 389), (905, 397)),

            ((830, 342), (694, 305), (541, 307)),

            ((409, 309), (322, 328), (262, 372)),

            ((245, 362), (236, 343), (234, 318))

        )

        _poly(surface, top_mass, (58, 69, 69))



        # Слабые голубовато-серые блики по телу.

        for i in range(8):

            t = i / 7

            c = _mix((73, 84, 84), (114, 129, 128), t)

            path = _curve(

                (245 + i * 7, 442 - i * 6),

                ((382 + i * 8, 369 - i * 5), (593 + i * 8, 319 - i * 4), (850 + i * 6, 319 + i * 2))

            )

            _line(surface, path, c, 2)



        # Панельные швы/сегменты корпуса.

        segment_lines = [

            _curve((235, 333), ((239, 300), (260, 280), (295, 268)), ((319, 280), (325, 317), (316, 358))),

            _curve((395, 244), ((383, 281), (389, 346), (413, 395))),

            _curve((543, 225), ((512, 258), (509, 331), (544, 383))),

            _curve((683, 232), ((655, 267), (665, 352), (725, 427))),

            _curve((862, 287), ((839, 331), (854, 415), (914, 500))),

        ]

        for p in segment_lines:

            _bead_line(surface, p, [((46, 52, 53), 7), ((90, 101, 100), 2)])



        # Контуры крупных пластин.

        plates = [

            _curve((325, 243), ((350, 229), (383, 227), (412, 241)), ((402, 298), (387, 345), (413, 395)), ((375, 396), (340, 380), (317, 357)), ((332, 313), (337, 275), (325, 243))),

            _curve((491, 224), ((526, 212), (574, 213), (623, 232)), ((625, 293), (615, 340), (542, 384)), ((500, 392), (470, 381), (448, 353)), ((455, 310), (474, 253), (491, 224))),

            _curve((668, 235), ((706, 224), (761, 235), (810, 265)), ((794, 321), (763, 369), (723, 426)), ((676, 427), (643, 407), (616, 365)), ((623, 307), (642, 256), (668, 235))),

        ]

        fill_cols = [(75, 87, 84), (72, 85, 78), (77, 88, 87)]

        for pts, col in zip(plates, fill_cols):

            _poly(surface, pts, col)

            _line(surface, pts, (53, 60, 61), 2, closed=True)

    def _draw_head(surface):

        # Морда и губы.

        head = _curve(

            (82, 405),

            ((104, 335), (154, 286), (225, 276)),

            ((251, 311), (247, 361), (223, 397)),

            ((193, 424), (154, 445), (110, 462)),

            ((90, 448), (80, 427), (82, 405))

        )

        _poly(surface, head, (84, 95, 94))

        _poly(surface, _curve(

            (101, 410),

            ((119, 371), (153, 343), (196, 336)),

            ((204, 359), (203, 384), (189, 405)),

            ((165, 425), (139, 436), (110, 448)),

            ((100, 438), (95, 424), (101, 410))

        ), (107, 115, 114))



        # Выступающий хоботок/трубка рта.

        tube = _curve(

            (66, 410),

            ((71, 397), (85, 386), (102, 387)),

            ((118, 393), (120, 410), (113, 425)),

            ((96, 430), (80, 432), (67, 425)),

            ((63, 420), (63, 415), (66, 410))

        )

        _poly(surface, tube, (117, 121, 119))

        _poly(surface, _curve(

            (57, 411),

            ((60, 403), (70, 397), (80, 397)),

            ((91, 402), (93, 413), (88, 423)),

            ((77, 425), (68, 426), (59, 422)),

            ((57, 418), (56, 414), (57, 411))

        ), (156, 158, 152))

        _line(surface, _curve((58, 412), ((67, 405), (77, 404), (87, 406))), (72, 78, 79), 2)



        # Шов на лице.

        _bead_line(surface, _curve((184, 278), ((165, 328), (166, 391), (203, 431))), [((49, 57, 58), 5), ((95, 108, 107), 2)])



        # Глаз.

        _oval(surface, (117, 301, 57, 57), (36, 45, 42))

        _oval(surface, (122, 306, 47, 47), (185, 213, 52))

        _oval(surface, (128, 311, 35, 35), (231, 247, 94))

        _oval(surface, (136, 319, 19, 19), (31, 37, 40))

        _circle(surface, (142, 325), 3, (243, 253, 181))

        _circle(surface, (138, 317), 2, (255, 255, 220))



        # Маленький грудной плавник.

        fin = _curve(

            (331, 398),

            ((346, 369), (379, 352), (418, 356)),

            ((427, 383), (425, 414), (416, 450)),

            ((382, 454), (353, 436), (331, 398))

        )

        _poly(surface, fin, (112, 131, 126))

        _poly(surface, _curve(

            (339, 396),

            ((353, 375), (378, 365), (404, 368)),

            ((410, 388), (410, 411), (402, 437)),

            ((378, 439), (355, 426), (339, 396))

        ), (131, 149, 144))

        for i in range(6):

            t = i / 5

            x0, y0 = 341, 396

            x1 = 390 + t * 15

            y1 = 371 + t * 58

            _line(surface, [(x0, y0), (x1, y1)], (165, 183, 176), 1)

    def _draw_dorsal_and_belly_fins(surface):

        # Спинной треугольный плавник.

        dorsal = _curve(

            (876, 208),

            ((926, 150), (983, 112), (1044, 102)),

            ((1057, 145), (1044, 191), (1014, 245)),

            ((963, 247), (921, 235), (876, 208))

        )

        _poly(surface, dorsal, (132, 150, 152))

        _poly(surface, _curve(

            (892, 206),

            ((934, 162), (977, 137), (1024, 129)),

            ((1031, 162), (1021, 191), (997, 227)),

            ((962, 228), (927, 221), (892, 206))

        ), (160, 175, 177))

        _line(surface, _curve((891, 205), ((939, 161), (978, 138), (1026, 129))), (208, 220, 221), 2)



        # Небольшой брюшной плавник снизу по центру.

        ventral = _curve(

            (670, 558),

            ((701, 545), (735, 544), (763, 553)),

            ((756, 582), (735, 604), (713, 616)),

            ((690, 609), (676, 589), (670, 558))

        )

        _poly(surface, ventral, (82, 91, 89))

        _poly(surface, _curve(

            (680, 560),

            ((705, 552), (730, 552), (749, 558)),

            ((743, 576), (727, 592), (710, 601)),

            ((692, 595), (684, 582), (680, 560))

        ), (108, 117, 115))

    def _draw_legs(surface):

        # Передняя крупная нога/ласт.

        leg1 = _curve(

            (834, 387),

            ((860, 376), (890, 384), (915, 405)),

            ((943, 447), (953, 509), (960, 586)),

            ((965, 655), (983, 704), (1018, 726)),

            ((1062, 724), (1093, 707), (1111, 680)),

            ((1080, 636), (1052, 593), (1028, 542)),

            ((1006, 493), (998, 448), (1002, 414)),

            ((961, 385), (902, 374), (834, 387))

        )

        _poly(surface, leg1, (91, 104, 101))

        _poly(surface, _curve(

            (852, 393),

            ((879, 389), (902, 393), (921, 410)),

            ((942, 449), (951, 500), (958, 566)),

            ((965, 625), (983, 671), (1015, 699)),

            ((1046, 696), (1072, 683), (1090, 663)),

            ((1062, 625), (1037, 586), (1015, 538)),

            ((993, 489), (985, 445), (987, 418)),

            ((949, 395), (902, 389), (852, 393))

        ), (106, 118, 114))



        # Ступня/лопасть ноги.

        foot = _curve(

            (984, 676),

            ((1015, 660), (1060, 654), (1104, 661)),

            ((1138, 684), (1142, 712), (1132, 734)),

            ((1070, 742), (1018, 738), (976, 719)),

            ((969, 700), (972, 687), (984, 676))

        )

        _poly(surface, foot, (79, 92, 88))

        _poly(surface, _curve(

            (994, 678),

            ((1028, 670), (1062, 669), (1097, 675)),

            ((1120, 691), (1123, 708), (1118, 720)),

            ((1068, 723), (1022, 720), (988, 706)),

            ((984, 696), (986, 685), (994, 678))

        ), (99, 113, 107))



        # Текстура пятнами на ласте.

        _draw_spot_cluster(surface, (1045, 697), 74, seed=107)

        _draw_spot_cluster(surface, (982, 561), 36, seed=48)



        # Складки на ноге.

        for i in range(3):

            _line(surface, _curve((874 + i * 10, 458 + i * 11), ((901 + i * 7, 466 + i * 12), (916 + i * 6, 480 + i * 16), (924 + i * 4, 497 + i * 20))), (70, 79, 77), 2)



        # Задняя маленькая конечность за газовым мешком.

        rear_leg = _curve(

            (1010, 372),

            ((1035, 361), (1064, 372), (1083, 396)),

            ((1093, 421), (1093, 449), (1088, 480)),

            ((1066, 483), (1047, 473), (1033, 452)),

            ((1022, 425), (1012, 399), (1010, 372))

        )

        _poly(surface, rear_leg, (73, 85, 81))

        _poly(surface, _curve(

            (1021, 376),

            ((1041, 371), (1058, 379), (1071, 397)),

            ((1078, 421), (1077, 443), (1072, 468)),

            ((1055, 468), (1041, 461), (1030, 443)),

            ((1024, 421), (1020, 399), (1021, 376))

        ), (92, 103, 99))

    def _draw_gas_sac(surface):

        # Газовый мешок позади тела.

        sac = _curve(

            (960, 330),

            ((1039, 292), (1149, 300), (1219, 355)),

            ((1248, 420), (1243, 503), (1202, 561)),

            ((1140, 603), (1058, 602), (997, 566)),

            ((955, 520), (936, 458), (941, 396)),

            ((944, 372), (950, 348), (960, 330))

        )

        _poly(surface, sac, (48, 57, 57))

        _poly(surface, _curve(

            (970, 338),

            ((1040, 311), (1130, 317), (1190, 362)),

            ((1213, 418), (1208, 487), (1179, 538)),

            ((1128, 572), (1067, 572), (1018, 542)),

            ((984, 504), (969, 454), (972, 403)),

            ((973, 382), (977, 355), (970, 338))

        ), (58, 70, 69))



        # Небольшие бугры/выпуклости.

        bulges = [

            (1040, 365, 44, 35), (1094, 343, 52, 38), (1154, 362, 47, 37),

            (1188, 420, 44, 37), (1170, 483, 45, 40), (1119, 530, 58, 43),

            (1045, 526, 58, 43), (1010, 470, 45, 37), (998, 406, 38, 31)

        ]

        for x, y, w, h in bulges:

            _oval(surface, (x - w / 2, y - h / 2, w, h), (42, 50, 51))

            _oval(surface, (x - w / 2 + 4, y - h / 2 + 4, w - 8, h - 8), (55, 64, 64))



        # Светящиеся газовые пузыри.

        glow_spots = [

            (1027, 369, 13), (1086, 349, 17), (1143, 371, 13), (1188, 410, 9),

            (1206, 462, 22), (1161, 516, 13), (1102, 546, 27), (1034, 533, 16),

            (994, 474, 11), (982, 418, 9), (1068, 390, 9), (1120, 395, 8),

            (1170, 379, 8), (1148, 444, 8), (1087, 481, 11), (1008, 520, 8)

        ]

        for x, y, r in glow_spots:

            _draw_glow_spot(surface, x, y, r)



        # Мелкие углубления по мешку.

        _draw_spot_cluster(surface, (1086, 406), 64, seed=200)

        _draw_spot_cluster(surface, (1140, 481), 70, seed=210)

        _draw_spot_cluster(surface, (1018, 475), 48, seed=220)

    def _draw_texture(surface):

        rng = random.Random(9025)



        # Пористая текстура корпуса.

        for _ in range(620):

            x = rng.uniform(175, 1000)

            y = rng.uniform(224, 586)

            if ((x - 624) / 485) ** 2 + ((y - 405) / 190) ** 2 < 1.0:

                col = rng.choice([

                    (66, 75, 74), (78, 89, 87), (56, 65, 63), (98, 110, 107), (40, 47, 46)

                ])

                r = rng.choice([1, 1, 1, 2, 2, 3])

                _circle(surface, (x, y), r, col)



        # Группа пор над передней ногой, как на референсе.

        _draw_spot_cluster(surface, (734, 307), 44, seed=57)



        # Зелёные мелкие точки у соединения мешка и хвоста.

        for p in [(933, 358), (952, 386), (965, 404), (951, 433), (941, 455), (926, 486)]:

            _circle(surface, p, 3, (174, 202, 51))

            _circle(surface, (p[0]-1, p[1]-1), 1, (238, 246, 138))



        # Мягкий общий контур тела.

        outline = _curve(

            (154, 392),

            ((194, 298), (335, 222), (523, 212)),

            ((651, 202), (796, 223), (915, 269)),

            ((996, 295), (1061, 336), (1094, 385)),

            ((1090, 445), (1056, 500), (994, 532)),

            ((914, 574), (809, 591), (682, 590)),

            ((533, 593), (373, 571), (248, 536)),

            ((173, 506), (141, 454), (154, 392))

        )

        _line(surface, outline, (49, 56, 56), 3, closed=True)



        # Подсветка брюха и головы.

        _line(surface, _curve((415, 506), ((567, 489), (710, 494), (856, 520))), (223, 230, 222), 2)

        _line(surface, _curve((112, 447), ((158, 437), (186, 423), (212, 398))), (156, 170, 166), 2)

        _line(surface, _curve((231, 279), ((276, 251), (315, 248), (359, 256))), (130, 142, 141), 2)

    def _render_master():

        pic = pygame.Surface((ART_W, ART_H), pygame.SRCALPHA)

        pic.fill((0, 0, 0, 0))

        _draw_main_body(pic)

        _draw_head(pic)

        _draw_dorsal_and_belly_fins(pic)

        _draw_gas_sac(pic)

        _draw_legs(pic)

        _draw_texture(pic)

        return pic

    return _render_master()


_NEW_FAUNA_MASTER_CACHE = {}

def _new_fauna_sprite(kind, length, width, height_factor):
    """Масштабировать без изменения пропорций; ориентация игры — вправо.

    Длина и ширина AnimalType остаются прежними.  Избыточный запас по высоте
    позволяет отобразить крылья, рога, мембраны и клешни без сплющивания.
    """
    master = _NEW_FAUNA_MASTER_CACHE.get(kind)
    if master is None:
        constructor = {
            'crabsnake': _build_new_crabsnake_source,
            'boneshark': _build_new_boneshark_source,
            'gasopod': _build_new_gasopod_source,
        }[kind]
        master = constructor()
        # У крабозмея и газобрюха голова нарисована слева;
        # генератор игры всегда ожидает голову справа.
        if kind in ('crabsnake', 'gasopod'):
            master = pygame.transform.flip(master, True, False)
        master = _crop_alpha_surface(master)
        _NEW_FAUNA_MASTER_CACHE[kind] = master
    return _fit_small_fauna_proportionally(master, length, width, height_factor)


def generate_uploaded_crabsnake_sprite(length, width):
    return _new_fauna_sprite('crabsnake', length, width, 3.0)


def generate_uploaded_boneshark_sprite(length, width):
    return _new_fauna_sprite('boneshark', length, width, 2.4)


def generate_uploaded_gasopod_sprite(length, width):
    return _new_fauna_sprite('gasopod', length, width, 2.4)


def _tint_creature_surface(surface, mul_rgb=(255, 255, 255), add_rgb=(0, 0, 0)):
    """Мягко перекрашивает уже нарисованный спрайт, сохраняя альфа-канал."""
    result = surface.copy().convert_alpha()
    if mul_rgb != (255, 255, 255):
        tint = pygame.Surface(result.get_size(), pygame.SRCALPHA)
        tint.fill((int(mul_rgb[0]), int(mul_rgb[1]), int(mul_rgb[2]), 255))
        result.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    if add_rgb != (0, 0, 0):
        add = pygame.Surface(result.get_size(), pygame.SRCALPHA)
        add.fill((int(add_rgb[0]), int(add_rgb[1]), int(add_rgb[2]), 0))
        result.blit(add, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    return result


def generate_variant_eyeye_sprite(length, width):
    """Eyeye как вариация детализированного пискуна: иная палитра и более крупный глаз."""
    surf = _tint_creature_surface(
        generate_detailed_peeper_sprite(max(12, int(length * 0.94)), max(6, int(width * 1.06))),
        mul_rgb=(150, 210, 135), add_rgb=(6, 18, 6)
    )
    cx, cy = surf.get_width() // 2, surf.get_height() // 2
    eye_r = max(3, int(width * 0.28))
    pygame.draw.circle(surf, (235, 245, 235, 235), (cx + int(length * 0.17), cy), eye_r)
    pygame.draw.circle(surf, (244, 206, 88, 235), (cx + int(length * 0.19), cy), max(2, int(eye_r * 0.58)))
    pygame.draw.circle(surf, (24, 26, 24, 255), (cx + int(length * 0.21), cy), max(1, int(eye_r * 0.28)))
    pygame.draw.circle(surf, (255, 255, 255, 230), (cx + int(length * 0.27), cy - max(1, eye_r // 4)), max(1, int(eye_r * 0.12)))
    return surf


def generate_variant_holefish_sprite(length, width):
    """Holefish как вариация детализированного кольцевика: синяя палитра, более округлое тело и характерное отверстие."""
    surf = _tint_creature_surface(
        generate_detailed_hoopfish_sprite(max(12, int(length * 0.98)), max(6, int(width * 1.12))),
        mul_rgb=(150, 175, 255), add_rgb=(0, 10, 28)
    )
    cx, cy = surf.get_width() // 2, surf.get_height() // 2
    hole_r = max(3, int(width * 0.22))
    hole_pos = (cx - int(length * 0.02), cy)
    pygame.draw.circle(surf, (18, 25, 44, 235), hole_pos, hole_r)
    pygame.draw.circle(surf, (108, 160, 235, 210), hole_pos, max(1, int(hole_r * 0.58)), 1)
    for frac in (0.22, 0.40, 0.58):
        x = int(cx - length * 0.23 + length * frac)
        pygame.draw.line(surf, (110, 150, 230, 180), (x, cy - int(width * 0.35)), (x, cy + int(width * 0.35)), max(1, int(width * 0.06)))
    return surf


def generate_variant_hoverfish_sprite(length, width):
    """Hoverfish как вариация детализированной Garryfish: шире тело, зелёная палитра и парящие брюшные плавники."""
    surf = _tint_creature_surface(
        generate_uploaded_garryfish_sprite(max(12, int(length * 0.95)), max(6, int(width * 1.08))),
        mul_rgb=(162, 235, 155), add_rgb=(6, 22, 6)
    )
    cx, cy = surf.get_width() // 2, surf.get_height() // 2
    fin_color = (142, 230, 112, 210)
    for sign in (-1, 1):
        for frac in (0.16, 0.02, -0.12):
            bx = cx + int(length * frac)
            pts = [
                (bx, cy + sign * int(width * 0.16)),
                (bx - int(length * 0.12), cy + sign * int(width * 0.82)),
                (bx + int(length * 0.04), cy + sign * int(width * 0.22)),
            ]
            pygame.draw.polygon(surf, fin_color, pts)
            pygame.draw.aalines(surf, (210, 255, 210, 210), True, pts)
    return surf


def generate_variant_reginald_sprite(length, width):
    """Reginald как вариация детализированной Garryfish: более длинный корпус, оливковая палитра и контрастный хвост."""
    surf = _tint_creature_surface(
        generate_uploaded_garryfish_sprite(max(12, int(length * 1.06)), max(6, int(width * 0.98))),
        mul_rgb=(168, 178, 122), add_rgb=(8, 12, 4)
    )
    cx, cy = surf.get_width() // 2, surf.get_height() // 2
    tail = [
        (cx - int(length * 0.34), cy),
        (cx - int(length * 0.56), cy - int(width * 0.34)),
        (cx - int(length * 0.46), cy - int(width * 0.05)),
        (cx - int(length * 0.56), cy + int(width * 0.34)),
    ]
    pygame.draw.polygon(surf, (110, 230, 225, 210), tail)
    pygame.draw.aalines(surf, (225, 255, 250, 210), True, tail)
    for sign in (-1, 1):
        eye = (cx + int(length * 0.22), cy + sign * int(width * 0.12))
        pygame.draw.circle(surf, (230, 240, 220, 230), eye, max(2, int(width * 0.11)))
        pygame.draw.circle(surf, (24, 28, 24, 255), eye, max(1, int(width * 0.05)))
    return surf


def generate_variant_spinefish_sprite(length, width):
    """Spinefish как вариация детализированного Bladderfish: тёмная биолюминесцентная версия с яркими рёбрами."""
    surf = _tint_creature_surface(
        generate_uploaded_bladderfish_sprite(max(12, int(length * 0.96)), max(6, int(width * 0.96))),
        mul_rgb=(92, 84, 160), add_rgb=(0, 0, 18)
    )
    cx, cy = surf.get_width() // 2, surf.get_height() // 2
    spine_col = (128, 235, 255, 220)
    pygame.draw.line(surf, spine_col, (cx - int(length * 0.28), cy), (cx + int(length * 0.28), cy), max(1, int(width * 0.10)))
    for frac in (-0.18, -0.08, 0.02, 0.12, 0.22):
        x = cx + int(length * frac)
        pygame.draw.line(surf, spine_col, (x, cy), (x - int(length * 0.06), cy - int(width * 0.44)), max(1, int(width * 0.06)))
        pygame.draw.line(surf, spine_col, (x, cy), (x - int(length * 0.06), cy + int(width * 0.44)), max(1, int(width * 0.06)))
    return surf


def generate_variant_blighter_sprite(length, width):
    """Blighter как хищная фиолетово-красная вариация Spinefish."""
    surf = _tint_creature_surface(
        generate_variant_spinefish_sprite(max(12, int(length * 1.02)), max(6, int(width * 1.02))),
        mul_rgb=(210, 120, 195), add_rgb=(16, 0, 12)
    )
    cx, cy = surf.get_width() // 2, surf.get_height() // 2
    jaw_pts = [
        (cx + int(length * 0.16), cy),
        (cx + int(length * 0.36), cy - int(width * 0.20)),
        (cx + int(length * 0.34), cy + int(width * 0.20)),
    ]
    pygame.draw.polygon(surf, (255, 110, 165, 210), jaw_pts)
    return surf



def generate_subnautica_creature_sprite(kind, length, width):
    """Procedurally draw a recognizable top-down Subnautica creature.

    The sprites are intentionally stylized for the 2D view, but preserve the
    main silhouette and color cues of each creature: Peeper's huge eye,
    Bladderfish's translucent lobes, Stalker's long jaws, Reaper mandibles,
    Jellyray glow, Reefback shell, etc. Every sprite faces right so the normal
    animal rotation cache can rotate it cheaply during gameplay.
    """
    # Обновлённая графика 10.10.2026 — без изменения AnimalType и ИИ.
    if kind == 'peeper':
        return generate_detailed_peeper_sprite(length, width)
    if kind == 'boomerang':
        return generate_uploaded_boomerang_sprite(length, width)
    if kind == 'garryfish':
        return generate_uploaded_garryfish_sprite(length, width)
    if kind == 'bladderfish':
        return generate_uploaded_bladderfish_sprite(length, width)
    if kind == 'hoopfish':    # Кольцевик; Holefish — отдельный вид!
        return generate_detailed_hoopfish_sprite(length, width)
    if kind == 'holefish':
        return generate_variant_holefish_sprite(length, width)
    if kind == 'eyeye':
        return generate_variant_eyeye_sprite(length, width)
    if kind == 'hoverfish':
        return generate_variant_hoverfish_sprite(length, width)
    if kind == 'reginald':
        return generate_variant_reginald_sprite(length, width)
    if kind == 'spinefish':
        return generate_variant_spinefish_sprite(length, width)
    if kind == 'blighter':
        return generate_variant_blighter_sprite(length, width)
    if kind == 'crabsnake':
        return generate_uploaded_crabsnake_sprite(length, width)
    if kind == 'boneshark':
        return generate_uploaded_boneshark_sprite(length, width)
    if kind == 'gasopod':
        return generate_uploaded_gasopod_sprite(length, width)

    length = max(12, int(length))
    width = max(6, int(width))
    margin = max(6, int(max(length, width) * 0.18))
    surf_w = length + margin * 2
    surf_h = max(width * 3, width + margin * 2)
    surf = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
    cy = surf_h // 2
    left = margin
    right = margin + length

    def P(points):
        return [(int(x), int(y)) for x, y in points]

    def ellipse(color, rect, border=0):
        pygame.draw.ellipse(
            surf, color,
            pygame.Rect(*(int(v) for v in rect)),
            border
        )

    def circle(color, pos, radius, border=0):
        pygame.draw.circle(
            surf, color,
            (int(pos[0]), int(pos[1])),
            max(1, int(radius)), border
        )

    def line(color, a, b, thickness=1):
        pygame.draw.line(
            surf, color,
            (int(a[0]), int(a[1])),
            (int(b[0]), int(b[1])),
            max(1, int(thickness))
        )

    # --- Small edible fish -------------------------------------------------
    if kind == 'peeper':
        body = (left + length * 0.18, cy - width * 0.46,
                length * 0.66, width * 0.92)
        ellipse((45, 150, 190), body)
        ellipse((75, 205, 220),
                (left + length * 0.24, cy - width * 0.32,
                 length * 0.48, width * 0.58))
        pygame.draw.polygon(
            surf, (250, 165, 25),
            P([(left + length * 0.20, cy),
               (left, cy - width * 0.50),
               (left, cy + width * 0.50)])
        )
        pygame.draw.polygon(
            surf, (255, 215, 45),
            P([(left + length * 0.48, cy - width * 0.35),
               (left + length * 0.60, cy - width * 0.80),
               (left + length * 0.68, cy - width * 0.30)])
        )
        eye_r = width * 0.34
        circle((255, 225, 55), (left + length * 0.76, cy), eye_r)
        circle((25, 25, 30), (left + length * 0.78, cy), eye_r * 0.56)
        circle((220, 250, 255),
               (left + length * 0.84, cy - eye_r * 0.24), eye_r * 0.18)
        line((10, 65, 85),
             (left + length * 0.35, cy - width * 0.28),
             (left + length * 0.55, cy + width * 0.28), 1)

    elif kind == 'bladderfish':
        ellipse((235, 95, 185, 185),
                (left + length * 0.20, cy - width * 0.75,
                 length * 0.58, width * 1.50))
        ellipse((255, 150, 215, 155),
                (left + length * 0.10, cy - width * 0.46,
                 length * 0.28, width * 0.92))
        ellipse((255, 150, 215, 155),
                (left + length * 0.66, cy - width * 0.46,
                 length * 0.24, width * 0.92))
        ellipse((185, 220, 75),
                (left + length * 0.35, cy - width * 0.35,
                 length * 0.28, width * 0.70))
        circle((245, 250, 250),
               (left + length * 0.70, cy - width * 0.13), width * 0.13)
        circle((35, 35, 45),
               (left + length * 0.72, cy - width * 0.13), width * 0.07)

    elif kind == 'boomerang':
        pygame.draw.polygon(
            surf, (80, 95, 210),
            P([(left, cy),
               (left + length * 0.36, cy - width * 0.82),
               (right, cy - width * 0.18),
               (left + length * 0.54, cy),
               (right, cy + width * 0.18),
               (left + length * 0.36, cy + width * 0.82)])
        )
        pygame.draw.lines(
            surf, (230, 85, 190), False,
            P([(left + length * 0.16, cy),
               (left + length * 0.39, cy - width * 0.54),
               (right - 2, cy - width * 0.10)]), 2
        )
        circle((255, 225, 65),
               (left + length * 0.78, cy - width * 0.05), width * 0.10)
        circle((25, 25, 30),
               (left + length * 0.80, cy - width * 0.05), width * 0.05)

    elif kind == 'garryfish':
        ellipse((68, 135, 92),
                (left + length * 0.18, cy - width * 0.44,
                 length * 0.64, width * 0.88))
        pygame.draw.polygon(
            surf, (245, 190, 50),
            P([(left + length * 0.25, cy),
               (left, cy - width * 0.55),
               (left + length * 0.05, cy),
               (left, cy + width * 0.55)])
        )
        pygame.draw.polygon(
            surf, (225, 175, 40),
            P([(left + length * 0.35, cy - width * 0.30),
               (left + length * 0.50, cy - width * 0.88),
               (left + length * 0.62, cy - width * 0.28)])
        )
        ellipse((125, 180, 125),
                (left + length * 0.55, cy - width * 0.35,
                 length * 0.30, width * 0.70))
        circle((235, 245, 210),
               (left + length * 0.76, cy - width * 0.08), width * 0.13)
        circle((20, 25, 20),
               (left + length * 0.78, cy - width * 0.08), width * 0.06)

    elif kind == 'holefish':
        ellipse((65, 115, 180),
                (left + length * 0.14, cy - width * 0.52,
                 length * 0.72, width * 1.04))
        pygame.draw.polygon(
            surf, (45, 75, 145),
            P([(left + length * 0.22, cy),
               (left, cy - width * 0.48),
               (left, cy + width * 0.48)])
        )
        circle((0, 0, 0, 0),
               (left + length * 0.45, cy), width * 0.24)
        circle((235, 245, 255),
               (left + length * 0.74, cy - width * 0.10), width * 0.12)
        circle((15, 20, 30),
               (left + length * 0.76, cy - width * 0.10), width * 0.06)

    elif kind == 'hoverfish':
        ellipse((70, 175, 100),
                (left + length * 0.20, cy - width * 0.34,
                 length * 0.58, width * 0.68))
        for sign in (-1, 1):
            for frac in (0.34, 0.55, 0.72):
                base_x = left + length * frac
                pygame.draw.polygon(
                    surf, (135, 220, 110),
                    P([(base_x, cy + sign * width * 0.20),
                       (base_x - length * 0.10,
                        cy + sign * width * 0.80),
                       (base_x + length * 0.05,
                        cy + sign * width * 0.28)])
                )
        circle((250, 245, 180),
               (left + length * 0.73, cy - width * 0.06), width * 0.10)
        circle((15, 30, 20),
               (left + length * 0.75, cy - width * 0.06), width * 0.05)

    elif kind == 'hoopfish':
        ellipse((190, 205, 210),
                (left + length * 0.16, cy - width * 0.42,
                 length * 0.68, width * 0.84))
        for frac in (0.32, 0.47, 0.62):
            x = left + length * frac
            line((55, 75, 95),
                 (x, cy - width * 0.38),
                 (x, cy + width * 0.38), 2)
        circle((80, 180, 230),
               (left + length * 0.10, cy), width * 0.34, 2)
        circle((0, 0, 0, 0),
               (left + length * 0.10, cy), width * 0.20)
        circle((245, 250, 255),
               (left + length * 0.77, cy - width * 0.08), width * 0.10)
        circle((20, 25, 30),
               (left + length * 0.79, cy - width * 0.08), width * 0.05)

    elif kind == 'reginald':
        ellipse((74, 105, 75),
                (left + length * 0.15, cy - width * 0.42,
                 length * 0.68, width * 0.84))
        pygame.draw.polygon(
            surf, (65, 230, 230),
            P([(left + length * 0.18, cy),
               (left, cy - width * 0.58),
               (left + length * 0.03, cy - width * 0.08),
               (left, cy + width * 0.58)])
        )
        pygame.draw.polygon(
            surf, (210, 80, 225),
            P([(left + length * 0.20, cy),
               (left + length * 0.03, cy - width * 0.32),
               (left + length * 0.04, cy + width * 0.32)])
        )
        for ysign in (-1, 1):
            circle((215, 235, 225),
                   (left + length * 0.72, cy + ysign * width * 0.15),
                   width * 0.10)
            circle((25, 30, 25),
                   (left + length * 0.74, cy + ysign * width * 0.15),
                   width * 0.05)

    elif kind == 'spadefish':
        return generate_detailed_spadefish_sprite(length, width)

    elif kind in ('eyeye', 'oculus'):
        if kind == 'eyeye':
            body_c = (70, 145, 90)
            iris_c = (245, 215, 70)
            fin_c = (80, 190, 120)
        else:
            body_c = (120, 70, 185)
            iris_c = (120, 245, 245)
            fin_c = (225, 75, 220)
        ellipse(body_c,
                (left + length * 0.20, cy - width * 0.48,
                 length * 0.56, width * 0.96))
        pygame.draw.polygon(
            surf, fin_c,
            P([(left + length * 0.24, cy),
               (left, cy - width * 0.52),
               (left, cy + width * 0.52)])
        )
        eye_r = width * 0.36
        circle((235, 245, 250),
               (left + length * 0.70, cy), eye_r)
        circle(iris_c,
               (left + length * 0.72, cy), eye_r * 0.62)
        circle((20, 20, 30),
               (left + length * 0.74, cy), eye_r * 0.30)
        circle((255, 255, 255),
               (left + length * 0.82, cy - eye_r * 0.23), eye_r * 0.12)

    elif kind == 'spinefish':
        # Dark translucent body with bright skeletal ribs.
        ellipse((35, 45, 65, 180),
                (left + length * 0.14, cy - width * 0.36,
                 length * 0.70, width * 0.72))
        line((120, 225, 245),
             (left + length * 0.18, cy),
             (left + length * 0.78, cy), 2)
        for frac in (0.28, 0.38, 0.48, 0.58, 0.68):
            x = left + length * frac
            line((100, 190, 220),
                 (x, cy), (x - length * 0.05, cy - width * 0.40), 1)
            line((100, 190, 220),
                 (x, cy), (x - length * 0.05, cy + width * 0.40), 1)
        pygame.draw.polygon(
            surf, (70, 120, 175, 180),
            P([(left + length * 0.18, cy),
               (left, cy - width * 0.38),
               (left, cy + width * 0.38)])
        )
        circle((180, 245, 255),
               (left + length * 0.77, cy - width * 0.06), width * 0.08)

    # --- Rays and unusual passive fauna -----------------------------------
    elif kind == 'rabbit_ray':
        pygame.draw.polygon(
            surf, (65, 105, 185),
            P([(left + length * 0.18, cy),
               (left + length * 0.52, cy - width * 0.70),
               (left + length * 0.83, cy),
               (left + length * 0.52, cy + width * 0.70)])
        )
        line((80, 130, 215),
             (left + length * 0.22, cy), (left, cy), 2)
        # Two forward rabbit-like lobes.
        pygame.draw.polygon(
            surf, (110, 145, 220),
            P([(left + length * 0.72, cy - width * 0.18),
               (right, cy - width * 0.52),
               (left + length * 0.84, cy - width * 0.02)])
        )
        pygame.draw.polygon(
            surf, (110, 145, 220),
            P([(left + length * 0.72, cy + width * 0.18),
               (right, cy + width * 0.52),
               (left + length * 0.84, cy + width * 0.02)])
        )
        circle((240, 245, 255),
               (left + length * 0.76, cy - width * 0.12), width * 0.08)
        circle((20, 25, 40),
               (left + length * 0.78, cy - width * 0.12), width * 0.04)

    elif kind == 'jellyray':
        pygame.draw.polygon(
            surf, (115, 175, 245, 150),
            P([(left + length * 0.18, cy),
               (left + length * 0.53, cy - width * 0.72),
               (left + length * 0.82, cy),
               (left + length * 0.53, cy + width * 0.72)])
        )
        pygame.draw.polygon(
            surf, (230, 95, 235, 135),
            P([(left + length * 0.36, cy),
               (left + length * 0.53, cy - width * 0.44),
               (left + length * 0.70, cy),
               (left + length * 0.53, cy + width * 0.44)])
        )
        line((150, 220, 255, 175),
             (left + length * 0.20, cy),
             (left - length * 0.18, cy + width * 0.18), 2)
        for sign in (-1, 1):
            for frac in (0.34, 0.48, 0.62, 0.74):
                x = left + length * frac
                line((145, 205, 255, 140),
                     (x, cy + sign * width * 0.35),
                     (x - length * 0.17,
                      cy + sign * width * (0.78 + (frac - 0.5) * 0.2)), 1)

    # --- Predators ---------------------------------------------------------
    elif kind == 'biter' or kind == 'blighter':
        body_c = (185, 55, 45) if kind == 'biter' else (95, 35, 90)
        fin_c = (245, 95, 55) if kind == 'biter' else (190, 65, 145)
        ellipse(body_c,
                (left + length * 0.18, cy - width * 0.45,
                 length * 0.62, width * 0.90))
        pygame.draw.polygon(
            surf, fin_c,
            P([(left + length * 0.23, cy),
               (left, cy - width * 0.52),
               (left, cy + width * 0.52)])
        )
        # Oversized jaw/teeth.
        pygame.draw.polygon(
            surf, (45, 20, 25),
            P([(left + length * 0.67, cy - width * 0.28),
               (right, cy),
               (left + length * 0.67, cy + width * 0.28)])
        )
        for sign in (-1, 1):
            for frac in (0.72, 0.80, 0.88):
                pygame.draw.polygon(
                    surf, (245, 235, 210),
                    P([(left + length * frac, cy + sign * width * 0.10),
                       (left + length * (frac + 0.05), cy),
                       (left + length * (frac + 0.08),
                        cy + sign * width * 0.04)])
                )
        circle((250, 220, 85),
               (left + length * 0.68, cy - width * 0.23), width * 0.08)

    elif kind == 'stalker':
        return generate_detailed_stalker_sprite(length, width)

    elif kind == 'sand_shark':
        ellipse((135, 102, 72),
                (left + length * 0.12, cy - width * 0.46,
                 length * 0.72, width * 0.92))
        pygame.draw.polygon(
            surf, (110, 82, 62),
            P([(left + length * 0.22, cy),
               (left, cy - width * 0.56),
               (left + length * 0.04, cy),
               (left, cy + width * 0.56)])
        )
        for frac in (0.30, 0.42, 0.54, 0.66):
            pygame.draw.polygon(
                surf, (165, 132, 92),
                P([(left + length * frac, cy - width * 0.36),
                   (left + length * (frac + 0.05), cy - width * 0.72),
                   (left + length * (frac + 0.10), cy - width * 0.34)])
            )
        # Broad toothed mouth.
        pygame.draw.polygon(
            surf, (45, 28, 22),
            P([(left + length * 0.70, cy - width * 0.24),
               (right, cy),
               (left + length * 0.70, cy + width * 0.24)])
        )
        for sign in (-1, 1):
            for frac in (0.76, 0.83, 0.90):
                pygame.draw.polygon(
                    surf, (240, 235, 210),
                    P([(left + length * frac, cy + sign * width * 0.10),
                       (left + length * (frac + 0.04), cy),
                       (left + length * (frac + 0.07),
                        cy + sign * width * 0.04)])
                )

    elif kind == 'boneshark':
        ellipse((92, 90, 88),
                (left + length * 0.12, cy - width * 0.42,
                 length * 0.72, width * 0.84))
        pygame.draw.polygon(
            surf, (62, 68, 72),
            P([(left + length * 0.20, cy),
               (left, cy - width * 0.52),
               (left + length * 0.03, cy),
               (left, cy + width * 0.52)])
        )
        # Bone plates and spikes.
        for frac in (0.27, 0.39, 0.51, 0.63):
            x = left + length * frac
            pygame.draw.polygon(
                surf, (190, 182, 162),
                P([(x, cy - width * 0.34),
                   (x + length * 0.04, cy - width * 0.72),
                   (x + length * 0.08, cy - width * 0.33)])
            )
            line((185, 178, 160),
                 (x, cy - width * 0.30),
                 (x, cy + width * 0.30), 2)
        pygame.draw.polygon(
            surf, (105, 100, 96),
            P([(left + length * 0.68, cy - width * 0.28),
               (right, cy - width * 0.12),
               (right, cy + width * 0.12),
               (left + length * 0.68, cy + width * 0.28)])
        )
        circle((235, 190, 65),
               (left + length * 0.74, cy - width * 0.18), width * 0.07)

    elif kind == 'ampeel':
        return generate_detailed_ampeel_sprite(length, width)

    elif kind == 'mesmer':
        cx = left + length * 0.55
        for i in range(10):
            a = i / 10 * math.tau
            r1 = width * 0.33
            r2 = width * 0.82
            p1 = (cx + math.cos(a - 0.18) * r1,
                  cy + math.sin(a - 0.18) * r1)
            p2 = (cx + math.cos(a) * r2,
                  cy + math.sin(a) * r2)
            p3 = (cx + math.cos(a + 0.18) * r1,
                  cy + math.sin(a + 0.18) * r1)
            pygame.draw.polygon(
                surf,
                (45, 175, 185) if i % 2 == 0 else (220, 70, 190),
                P([p1, p2, p3])
            )
        circle((52, 80, 130), (cx, cy), width * 0.38)
        circle((220, 245, 255), (cx + width * 0.08, cy), width * 0.20)
        circle((70, 20, 110), (cx + width * 0.12, cy), width * 0.09)

    elif kind == 'crabsquid':
        return generate_detailed_crabsquid_sprite(length, width)

    elif kind == 'crabsnake':
        # Long violet serpent, inspired by Jellyshroom Cave Crabsnakes.
        pts = []
        for i in range(15):
            t = i / 14
            pts.append((left + t * length,
                        cy + math.sin(t * math.pi * 2.0) * width * 0.18))
        for i in range(len(pts) - 1):
            line((125, 55, 145), pts[i], pts[i + 1], max(3, width // 2))
            line((205, 95, 185), pts[i], pts[i + 1], max(1, width // 5))
        hx, hy = pts[-1]
        pygame.draw.polygon(
            surf, (150, 65, 160),
            P([(hx - width * 0.2, hy - width * 0.35),
               (hx + width * 0.55, hy - width * 0.18),
               (hx + width * 0.70, hy),
               (hx + width * 0.55, hy + width * 0.18),
               (hx - width * 0.2, hy + width * 0.35)])
        )
        for sign in (-1, 1):
            circle((240, 235, 120),
                   (hx + width * 0.28, hy + sign * width * 0.14),
                   width * 0.07)

    elif kind == 'crashfish':
        cx = left + length * 0.55
        circle((225, 75, 45), (cx, cy), width * 0.42)
        for i in range(8):
            a = i / 8 * math.tau
            p1 = (cx + math.cos(a - 0.16) * width * 0.34,
                  cy + math.sin(a - 0.16) * width * 0.34)
            p2 = (cx + math.cos(a) * width * 0.88,
                  cy + math.sin(a) * width * 0.88)
            p3 = (cx + math.cos(a + 0.16) * width * 0.34,
                  cy + math.sin(a + 0.16) * width * 0.34)
            pygame.draw.polygon(surf, (245, 185, 55), P([p1, p2, p3]))
        circle((245, 245, 230),
               (cx + width * 0.16, cy - width * 0.12), width * 0.09)
        circle((30, 25, 25),
               (cx + width * 0.18, cy - width * 0.12), width * 0.05)

    # --- Large fauna / leviathans -----------------------------------------
    elif kind == 'gasopod':
        ellipse((92, 110, 95),
                (left + length * 0.25, cy - width * 0.48,
                 length * 0.54, width * 0.96))
        ellipse((145, 160, 135),
                (left + length * 0.58, cy - width * 0.33,
                 length * 0.23, width * 0.66))
        for sign in (-1, 1):
            pygame.draw.polygon(
                surf, (75, 92, 78),
                P([(left + length * 0.35, cy + sign * width * 0.24),
                   (left + length * 0.15, cy + sign * width * 0.72),
                   (left + length * 0.48, cy + sign * width * 0.36)])
            )
        for i in range(5):
            a = (i / 5) * math.tau
            px = left + length * 0.20 + math.cos(a) * width * 0.22
            py = cy + math.sin(a) * width * 0.30
            circle((205, 225, 45), (px, py), width * 0.10)
            circle((110, 145, 25), (px, py), width * 0.10, 1)
        circle((235, 245, 230),
               (left + length * 0.72, cy - width * 0.12), width * 0.08)

    elif kind == 'reefback':
        return generate_detailed_reefback_sprite(length, width)

    elif kind == 'reaper':
        return generate_detailed_reaper_sprite(length, width)

    elif kind == 'sea_dragon':
        return generate_detailed_sea_dragon_sprite(length, width)

    elif kind == 'sea_treader':
        return generate_detailed_sea_treader_sprite(length, width)

    elif kind == 'warper':
        cx = left + length * 0.55
        # Cyan energy core and purple biomechanical shell.
        circle((40, 210, 235, 150), (cx, cy), width * 0.32)
        circle((130, 240, 255, 220), (cx, cy), width * 0.17)
        pygame.draw.polygon(
            surf, (80, 45, 125),
            P([(cx - width * 0.18, cy - width * 0.18),
               (cx + width * 0.18, cy - width * 0.18),
               (cx + width * 0.28, cy + width * 0.28),
               (cx - width * 0.28, cy + width * 0.28)])
        )
        for sign in (-1, 1):
            line((105, 65, 155),
                 (cx - width * 0.10, cy + sign * width * 0.08),
                 (left + length * 0.10, cy + sign * width * 0.72),
                 max(2, width // 12))
            line((105, 65, 155),
                 (cx + width * 0.12, cy + sign * width * 0.08),
                 (right, cy + sign * width * 0.52),
                 max(2, width // 12))
        pygame.draw.polygon(
            surf, (120, 75, 170),
            P([(cx - width * 0.18, cy - width * 0.20),
               (cx, cy - width * 0.62),
               (cx + width * 0.18, cy - width * 0.20)])
        )

    else:
        # Safe fallback for future canonical species.
        generic = generate_pike_style_sprite(
            length, width,
            (90, 150, 180), (40, 80, 120), (180, 210, 220),
            (55, 105, 145), [(210, 180, 70)], (110, 180, 200)
        )
        surf.blit(generic, generic.get_rect(center=(surf_w // 2, surf_h // 2)))

    return surf.convert_alpha()

# =========================================================
# СПРАЙТ ОРУЖИЯ
# =========================================================

def generate_weapon_sprite(barrel_length, color, accent_color=None):
    if accent_color is None:
        accent_color = tuple(
            max(0, c - 90) for c in color
        )

    grip_width = 8
    grip_height = 14

    body_width = 24
    body_height = 11

    width = body_width + barrel_length + 8
    height = body_height + grip_height + 8

    surf = pygame.Surface((width, height), pygame.SRCALPHA)

    grip_x = 6
    grip_y = 4 + body_height - 1

    grip_points = [
        (grip_x + 3, grip_y),
        (grip_x + 3 + grip_width, grip_y),
        (grip_x + 3 + grip_width - 3, grip_y + grip_height),
        (grip_x, grip_y + grip_height)
    ]

    pygame.draw.polygon(surf, (35, 35, 40), grip_points)
    pygame.draw.polygon(surf, (10, 10, 15), grip_points, 1)

    pygame.draw.arc(
        surf, (25, 25, 30),
        (grip_x + 6, grip_y + 1, 12, 10),
        0, math.pi, 2
    )

    body_x = 6
    body_y = 4

    pygame.draw.rect(
        surf, color,
        (body_x, body_y, body_width, body_height),
        border_radius=3
    )

    darker = tuple(max(0, c - 50) for c in color)

    pygame.draw.rect(
        surf, darker,
        (body_x + 2, body_y + 1, body_width - 4, 2)
    )

    pygame.draw.rect(
        surf, accent_color,
        (body_x, body_y, body_width, body_height),
        2, border_radius=3
    )

    barrel_x = body_x + body_width - 2
    barrel_height = 5
    barrel_y = body_y + (body_height - barrel_height) // 2

    pygame.draw.rect(
        surf, (55, 55, 62),
        (barrel_x, barrel_y, barrel_length, barrel_height)
    )
    pygame.draw.rect(
        surf, accent_color,
        (barrel_x, barrel_y, barrel_length, barrel_height), 1
    )

    muzzle_x = barrel_x + barrel_length - 2

    pygame.draw.rect(
        surf, color,
        (muzzle_x, barrel_y - 1, 3, barrel_height + 2)
    )
    pygame.draw.rect(
        surf, (255, 255, 255),
        (muzzle_x, barrel_y - 1, 3, barrel_height + 2), 1
    )

    pygame.draw.rect(
        surf, accent_color,
        (body_x + 6, body_y - 2, 2, 3)
    )
    pygame.draw.rect(
        surf, accent_color,
        (body_x + body_width - 10, body_y - 2, 2, 3)
    )

    return surf.convert_alpha()


def _fit_size(size, minimum=18):
    return max(minimum, int(size))


def generate_tech_item_sprite(name, size, color, is_weapon=False, weapon_type=""):
    size = _fit_size(size, 18)
    surf = pygame.Surface((size + 12, size + 12), pygame.SRCALPHA)
    cx = surf.get_width() // 2
    cy = surf.get_height() // 2
    dark = _shade(color, -65)
    light = _shade(color, 45)

    lower_name = name.lower()

    def rounded_panel(rect, fill, border):
        pygame.draw.rect(surf, fill, rect, border_radius=5)
        pygame.draw.rect(surf, border, rect, 2, border_radius=5)
        inner = rect.inflate(-6, -6)
        if inner.width > 0 and inner.height > 0:
            pygame.draw.rect(surf, _shade(fill, 18), inner, border_radius=4)

    if (is_weapon or "нож" in lower_name or "клинок" in lower_name
            or "резак" in lower_name or "пушка" in lower_name
            or "винтовка" in lower_name):
        length = max(14, size + 4)
        return generate_weapon_sprite(length, color, dark)

    if "аптеч" in lower_name:
        rect = pygame.Rect(5, 6, size, size - 2)
        rounded_panel(rect, (235, 238, 238), (170, 175, 175))
        pygame.draw.rect(surf, (215, 45, 55), (cx - 3, cy - 9, 6, 18), border_radius=2)
        pygame.draw.rect(surf, (215, 45, 55), (cx - 9, cy - 3, 18, 6), border_radius=2)
    elif "батар" in lower_name or "энергояч" in lower_name:
        rect = pygame.Rect(5, 7, size - 2, max(14, size - 4))
        rounded_panel(rect, _shade(color, -10), dark)
        tip = pygame.Rect(rect.right - 3, rect.y + rect.h // 3, 4, rect.h // 3)
        pygame.draw.rect(surf, light, tip, border_radius=2)
        inner = rect.inflate(-8, -8)
        pygame.draw.rect(surf, color, inner, border_radius=3)
        pygame.draw.line(surf, (255, 255, 255), (inner.x + 4, inner.y + inner.h - 4), (inner.right - 4, inner.y + 4), 2)
    elif ("баллон" in lower_name or "костюм" in lower_name or "ребриз" in lower_name
          or "ласты" in lower_name or "компас" in lower_name):
        body = pygame.Rect(cx - size // 4, 6, size // 2, size - 4)
        pygame.draw.rect(surf, color, body, border_radius=6)
        pygame.draw.rect(surf, dark, body, 2, border_radius=6)
        pygame.draw.rect(surf, light, (body.x + 3, body.y + 3, body.w - 6, max(3, body.h // 4)), border_radius=4)
        if "компас" in lower_name:
            pygame.draw.circle(surf, (250, 250, 245), (cx, cy + 2), max(7, size // 4))
            pygame.draw.circle(surf, dark, (cx, cy + 2), max(7, size // 4), 2)
            pygame.draw.line(surf, (210, 40, 45), (cx, cy + 2), (cx, cy - 7), 2)
            pygame.draw.line(surf, (60, 90, 160), (cx, cy + 2), (cx - 5, cy + 8), 2)
        elif "ласты" in lower_name:
            pygame.draw.polygon(surf, color, [(cx - 10, cy + 2), (cx - 3, cy - 2), (cx - 2, cy + 10), (cx - 10, cy + 12)])
            pygame.draw.polygon(surf, _shade(color, 25), [(cx + 3, cy - 2), (cx + 10, cy + 2), (cx + 10, cy + 12), (cx + 2, cy + 10)])
            pygame.draw.polygon(surf, dark, [(cx - 10, cy + 2), (cx - 3, cy - 2), (cx - 2, cy + 10), (cx - 10, cy + 12)], 1)
            pygame.draw.polygon(surf, dark, [(cx + 3, cy - 2), (cx + 10, cy + 2), (cx + 10, cy + 12), (cx + 2, cy + 10)], 1)
    elif ("ракета" in lower_name or "пузыр" in lower_name or "антисеп" in lower_name
          or "кислот" in lower_name or "смаз" in lower_name or "аэрог" in lower_name):
        if "ракета" in lower_name:
            body = pygame.Rect(cx - 4, 6, 8, size)
            pygame.draw.rect(surf, color, body, border_radius=4)
            pygame.draw.polygon(surf, light, [(cx, 2), (cx - 6, 10), (cx + 6, 10)])
            pygame.draw.polygon(surf, dark, [(cx - 4, size + 2), (cx - 10, size + 8), (cx - 4, size + 8)])
            pygame.draw.polygon(surf, dark, [(cx + 4, size + 2), (cx + 10, size + 8), (cx + 4, size + 8)])
            pygame.draw.circle(surf, (255, 200, 100), (cx, size + 7), 4)
        else:
            pygame.draw.circle(surf, color, (cx, cy), max(7, size // 3))
            pygame.draw.circle(surf, dark, (cx, cy), max(7, size // 3), 2)
            pygame.draw.circle(surf, light, (cx - 3, cy - 3), max(2, size // 8))
    elif ("провод" in lower_name or "микросх" in lower_name or "комплект" in lower_name
          or "модуль" in lower_name or "скриж" in lower_name or "чип" in lower_name
          or "гидролок" in lower_name or "дрон" in lower_name):
        rect = pygame.Rect(5, 7, size, size - 2)
        rounded_panel(rect, _shade(color, -10), dark)
        for i in range(4):
            px = rect.x + 5 + i * max(3, rect.w // 5)
            pygame.draw.line(surf, light, (px, rect.y - 1), (px, rect.y + 3), 2)
            pygame.draw.line(surf, light, (px, rect.bottom - 3), (px, rect.bottom + 1), 2)
        inner = rect.inflate(-8, -8)
        pygame.draw.rect(surf, color, inner, border_radius=4)
        pygame.draw.rect(surf, (240, 245, 255), inner, 1, border_radius=4)
        pygame.draw.circle(surf, light, inner.center, max(2, inner.w // 6))
    else:
        rect = pygame.Rect(5, 7, size, size - 2)
        rounded_panel(rect, color, dark)
        pygame.draw.line(surf, light, (rect.x + 5, rect.y + rect.h - 6), (rect.right - 5, rect.y + 6), 2)
        pygame.draw.line(surf, light, (rect.x + 5, rect.y + rect.h - 3), (rect.right - 8, rect.y + 8), 2)

    return surf.convert_alpha()


def generate_building_sprite(name, size, color, wall=False):
    size = _fit_size(size, 20)
    width = size + 12
    height = size + 10
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    dark = _shade(color, -60)
    light = _shade(color, 35)
    lower_name = name.lower()

    def draw_window(rect, tint=(180, 235, 245)):
        pygame.draw.rect(surf, tint, rect, border_radius=3)
        pygame.draw.rect(surf, (95, 145, 165), rect, 1, border_radius=3)

    if wall or "окно" in lower_name or "люк" in lower_name or "переборк" in lower_name:
        panel = pygame.Rect(4, 4, width - 8, height - 8)
        pygame.draw.rect(surf, _shade(color, -8), panel, border_radius=4)
        pygame.draw.rect(surf, dark, panel, 2, border_radius=4)
        inset = panel.inflate(-10, -10)
        if "окно" in lower_name:
            draw_window(inset)
        elif "люк" in lower_name:
            pygame.draw.circle(surf, light, panel.center, max(8, min(panel.w, panel.h) // 3), 3)
            pygame.draw.circle(surf, dark, panel.center, max(8, min(panel.w, panel.h) // 3 + 3), 1)
        else:
            pygame.draw.line(surf, light, (panel.x + 4, panel.y + 4), (panel.right - 4, panel.bottom - 4), 2)
            pygame.draw.line(surf, light, (panel.right - 4, panel.y + 4), (panel.x + 4, panel.bottom - 4), 2)
    elif any(key in lower_name for key in ("панель", "прожектор", "мачта", "энергопередатчик")):
        if "панель" in lower_name:
            board = pygame.Rect(8, 4, width - 16, height - 14)
            pygame.draw.rect(surf, color, board, border_radius=3)
            pygame.draw.rect(surf, dark, board, 2, border_radius=3)
            for i in range(1, 4):
                x = board.x + i * board.w // 4
                pygame.draw.line(surf, light, (x, board.y + 2), (x, board.bottom - 2), 1)
            for i in range(1, 3):
                y = board.y + i * board.h // 3
                pygame.draw.line(surf, light, (board.x + 2, y), (board.right - 2, y), 1)
            pygame.draw.line(surf, (180, 180, 180), board.midbottom, (width // 2, height - 2), 3)
        elif "прожектор" in lower_name or "мачта" in lower_name:
            pygame.draw.line(surf, (175, 180, 185), (width // 2, height - 2), (width // 2, 9), 3)
            pygame.draw.circle(surf, (240, 235, 170), (width // 2, 8), 6)
            pygame.draw.circle(surf, dark, (width // 2, 8), 6, 2)
            pygame.draw.polygon(surf, (245, 245, 180, 70), [(width // 2, 10), (width // 2 - 14, height - 4), (width // 2 + 14, height - 4)])
        else:
            pygame.draw.line(surf, light, (width // 2, height - 3), (width // 2, 10), 3)
            pygame.draw.circle(surf, color, (width // 2, 9), 6)
            pygame.draw.circle(surf, dark, (width // 2, 9), 6, 2)
    elif any(key in lower_name for key in ("реактор", "станция", "изготов", "консоль", "сканир")):
        body = pygame.Rect(5, 5, width - 10, height - 10)
        pygame.draw.rect(surf, _shade(color, -10), body, border_radius=5)
        pygame.draw.rect(surf, dark, body, 2, border_radius=5)
        screen = pygame.Rect(body.x + 5, body.y + 5, body.w - 10, max(8, body.h // 2 - 1))
        draw_window(screen, tint=(140, 225, 245))
        pygame.draw.rect(surf, light, (body.x + 8, body.bottom - 8, body.w - 16, 3), border_radius=2)
        if "реактор" in lower_name:
            pygame.draw.circle(surf, (235, 220, 95), (body.centerx, body.bottom - 10), 4)
            pygame.draw.circle(surf, (120, 95, 30), (body.centerx, body.bottom - 10), 4, 1)
    elif any(key in lower_name for key in ("комната", "отсек", "купол", "обсерват", "шахта", "циклоп", "мотыл", "краб", "нептун")):
        hull = pygame.Rect(4, 6, width - 8, height - 12)
        pygame.draw.rect(surf, color, hull, border_radius=max(6, hull.h // 3))
        pygame.draw.rect(surf, dark, hull, 2, border_radius=max(6, hull.h // 3))
        stripe = pygame.Rect(hull.x + 4, hull.centery - 2, hull.w - 8, 4)
        pygame.draw.rect(surf, light, stripe, border_radius=2)
        if any(key in lower_name for key in ("комната", "купол", "обсерват")):
            for i in range(3):
                wx = hull.x + 6 + i * max(6, hull.w // 4)
                draw_window(pygame.Rect(wx, hull.y + 5, 6, 6))
        elif "краб" in lower_name:
            pygame.draw.line(surf, dark, (hull.x + 8, hull.bottom - 2), (hull.x + 3, height - 1), 2)
            pygame.draw.line(surf, dark, (hull.right - 8, hull.bottom - 2), (hull.right - 3, height - 1), 2)
        elif "мотыл" in lower_name:
            pygame.draw.polygon(surf, light, [(hull.right - 2, hull.centery), (hull.right + 4, hull.centery - 5), (hull.right + 4, hull.centery + 5)])
        elif "циклоп" in lower_name:
            hull.inflate_ip(4, 0)
    elif any(key in lower_name for key in ("шкаф", "контейнер", "урна", "полка", "горшок", "грядка", "аквариум", "лестниц", "кровать", "стул", "скамья", "стол", "автомат")):
        body = pygame.Rect(6, 6, width - 12, height - 10)
        pygame.draw.rect(surf, color, body, border_radius=4)
        pygame.draw.rect(surf, dark, body, 2, border_radius=4)
        if "аквариум" in lower_name:
            draw_window(body.inflate(-8, -8))
            pygame.draw.circle(surf, (245, 210, 80), (body.x + 10, body.centery), 2)
        elif "лестниц" in lower_name:
            x1 = width // 2 - 5
            x2 = width // 2 + 5
            pygame.draw.line(surf, dark, (x1, 4), (x1, height - 4), 2)
            pygame.draw.line(surf, dark, (x2, 4), (x2, height - 4), 2)
            for y in range(8, height - 4, 5):
                pygame.draw.line(surf, light, (x1, y), (x2, y), 2)
        elif any(key in lower_name for key in ("кровать", "стул", "скамья", "стол")):
            pygame.draw.rect(surf, _shade(color, 25), (body.x + 4, body.y + 4, body.w - 8, body.h // 3), border_radius=3)
    else:
        body = pygame.Rect(6, 6, width - 12, height - 10)
        pygame.draw.rect(surf, color, body, border_radius=4)
        pygame.draw.rect(surf, dark, body, 2, border_radius=4)
        draw_window(body.inflate(-10, -10))

    return surf.convert_alpha()


# =========================================================
# СПРАЙТЫ РЕСУРСОВ
# =========================================================

def _shade(color, amount):
    if amount >= 0:
        return tuple(min(255, c + amount) for c in color)
    return tuple(max(0, c + amount) for c in color)


def _rock_outline(size, rnd, squash=0.9):
    cx = size / 2.0
    cy = size / 2.0
    radius = size * 0.46

    num_points = rnd.randint(7, 10)
    points = []
    for i in range(num_points):
        angle = (i / num_points) * math.tau
        r = radius * rnd.uniform(0.72, 1.05)
        px = cx + math.cos(angle) * r
        py = cy + math.sin(angle) * r * squash
        points.append((px, py))

    return cx, cy, points


def generate_rock_sprite(size, base_color=(110, 110, 110), seed=None):
    rnd = random.Random(seed) if seed is not None else random
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy, points = _rock_outline(size, rnd)

    dark = _shade(base_color, -55)
    light = _shade(base_color, 40)
    very_light = _shade(base_color, 75)

    pygame.draw.polygon(surf, dark, points)

    body = [
        (cx + (p[0] - cx) * 0.94,
         cy + (p[1] - cy) * 0.94 - size * 0.05)
        for p in points
    ]
    pygame.draw.polygon(surf, base_color, body)

    highlight = [
        (cx + (p[0] - cx) * 0.6,
         cy + (p[1] - cy) * 0.5 - size * 0.10)
        for p in points
    ]
    pygame.draw.polygon(surf, light, highlight)

    sparkle = [
        (cx + (p[0] - cx) * 0.35,
         cy + (p[1] - cy) * 0.30 - size * 0.14)
        for p in points
    ]
    pygame.draw.polygon(surf, very_light, sparkle)

    for _ in range(rnd.randint(1, 3)):
        a = rnd.uniform(0, math.tau)
        r1 = size * 0.46 * rnd.uniform(0.10, 0.35)
        r2 = size * 0.46 * rnd.uniform(0.45, 0.75)
        x1 = cx + math.cos(a) * r1
        y1 = cy + math.sin(a) * r1
        x2 = cx + math.cos(a) * r2
        y2 = cy + math.sin(a) * r2
        pygame.draw.line(surf, dark, (x1, y1), (x2, y2), 1)

    pygame.draw.polygon(surf, _shade(base_color, -85), points, 1)
    return surf.convert_alpha()


def generate_ore_sprite(size, base_color, vein_colors,
                       vein_count=5, seed=None):
    rnd = random.Random(seed) if seed is not None else random
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy, points = _rock_outline(size, rnd)

    dark = _shade(base_color, -55)
    light = _shade(base_color, 35)

    pygame.draw.polygon(surf, dark, points)
    pygame.draw.polygon(
        surf, base_color,
        [(cx + (p[0] - cx) * 0.94,
          cy + (p[1] - cy) * 0.94 - size * 0.04)
         for p in points]
    )
    pygame.draw.polygon(
        surf, light,
        [(cx + (p[0] - cx) * 0.6,
          cy + (p[1] - cy) * 0.5 - size * 0.09)
         for p in points]
    )

    used_positions = []
    for _ in range(vein_count):
        placed = False
        for _try in range(12):
            a = rnd.uniform(0, math.tau)
            d = rnd.uniform(0, size * 0.30)
            vx = cx + math.cos(a) * d
            vy = cy + math.sin(a) * d

            too_close = False
            for (ux, uy) in used_positions:
                if (vx - ux) ** 2 + (vy - uy) ** 2 < (size * 0.18) ** 2:
                    too_close = True
                    break
            if not too_close:
                used_positions.append((vx, vy))
                placed = True
                break
        if not placed:
            continue

        vein_size = rnd.uniform(size * 0.10, size * 0.20)
        color = rnd.choice(vein_colors)
        color_light = _shade(color, 60)
        color_dark = _shade(color, -60)

        shard = [
            (vx, vy - vein_size),
            (vx + vein_size * 0.7, vy - vein_size * 0.2),
            (vx + vein_size * 0.5, vy + vein_size * 0.8),
            (vx - vein_size * 0.5, vy + vein_size * 0.8),
            (vx - vein_size * 0.7, vy - vein_size * 0.2),
        ]

        pygame.draw.polygon(surf, color_dark, shard)
        inner = [
            (vx + (x - vx) * 0.72,
             vy + (y - vy) * 0.72 - vein_size * 0.10)
            for (x, y) in shard
        ]
        pygame.draw.polygon(surf, color, inner)

        pygame.draw.circle(
            surf, color_light,
            (int(vx - vein_size * 0.20),
             int(vy - vein_size * 0.35)),
            max(1, int(vein_size * 0.25))
        )

    pygame.draw.polygon(surf, _shade(base_color, -85), points, 1)
    return surf.convert_alpha()


def generate_crystal_sprite(size, color=(0, 255, 255),
                            sparkle=True, seed=None):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = size / 2.0
    cy = size / 2.0
    r = size * 0.46

    top = (cx, cy - r)
    upper_left = (cx - r * 0.75, cy - r * 0.15)
    upper_right = (cx + r * 0.75, cy - r * 0.15)
    left = (cx - r * 0.85, cy + r * 0.15)
    right = (cx + r * 0.85, cy + r * 0.15)
    bottom = (cx, cy + r)

    dark = _shade(color, -70)
    mid = color
    light = _shade(color, 60)
    bright = _shade(color, 130)

    pygame.draw.polygon(
        surf, dark,
        [left, bottom, right, upper_right, upper_left]
    )
    pygame.draw.polygon(
        surf, mid, [top, upper_left, left, bottom]
    )
    pygame.draw.polygon(
        surf, dark, [top, upper_right, right, bottom]
    )
    pygame.draw.polygon(
        surf, light,
        [top, upper_left, (cx, cy - r * 0.05), upper_right]
    )
    pygame.draw.polygon(
        surf, bright,
        [top,
         (cx - r * 0.30, cy - r * 0.15),
         (cx - r * 0.10, cy + r * 0.05),
         (cx, cy - r * 0.05)]
    )

    pygame.draw.polygon(
        surf, _shade(color, -110),
        [top, upper_right, right, bottom, left, upper_left],
        1
    )

    if sparkle:
        sx = int(cx - r * 0.35)
        sy = int(cy - r * 0.45)
        pygame.draw.line(
            surf, (255, 255, 255), (sx - 3, sy), (sx + 3, sy), 1
        )
        pygame.draw.line(
            surf, (255, 255, 255), (sx, sy - 3), (sx, sy + 3), 1
        )

    return surf.convert_alpha()


def generate_seaweed_sprite(size, seed=None):
    rnd = random.Random(seed) if seed is not None else random
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = size / 2.0

    dark = (5, 90, 20)
    mid = (30, 160, 50)
    light = (100, 220, 90)
    bright = (180, 245, 140)

    strands = rnd.randint(3, 4)
    for i in range(strands):
        offset_x = (i - (strands - 1) / 2) * size * 0.18
        phase = rnd.uniform(0, math.tau)
        amplitude = size * rnd.uniform(0.08, 0.14)
        height = size * rnd.uniform(0.65, 0.85)

        points = []
        steps = 8
        for t in range(steps + 1):
            prog = t / steps
            x = cx + offset_x \
                + math.sin(prog * math.pi * 2.2 + phase) \
                * amplitude * (1 - prog * 0.3)
            y = size * 0.92 - prog * height
            points.append((x, y))

        width = max(2, int(size * 0.12))

        for j in range(len(points) - 1):
            pygame.draw.line(
                surf, dark, points[j], points[j + 1], width + 2
            )
        for j in range(len(points) - 1):
            pygame.draw.line(
                surf, mid, points[j], points[j + 1], width
            )
        for j in range(len(points) - 1):
            pygame.draw.line(
                surf, light, points[j], points[j + 1],
                max(1, width // 3)
            )

        tip_x, tip_y = points[-1]
        pygame.draw.circle(
            surf, light, (int(tip_x), int(tip_y)),
            max(1, width // 3)
        )
        pygame.draw.circle(
            surf, bright, (int(tip_x), int(tip_y)),
            max(1, width // 5)
        )

    return surf.convert_alpha()


def generate_lumpy_sprite(size, color, seed=None, shine=False):
    rnd = random.Random(seed) if seed is not None else random
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = size / 2.0
    cy = size / 2.0
    r = size * 0.42

    dark = _shade(color, -50)
    light = _shade(color, 35)
    bright = _shade(color, 70)

    blobs = rnd.randint(4, 6)

    for i in range(blobs):
        a = (i / blobs) * math.tau + rnd.uniform(-0.4, 0.4)
        d = r * rnd.uniform(0.15, 0.45)
        bx = cx + math.cos(a) * d
        by = cy + math.sin(a) * d
        br = r * rnd.uniform(0.55, 0.85)
        pygame.draw.circle(surf, dark, (int(bx), int(by)), int(br))

    for i in range(blobs):
        a = (i / blobs) * math.tau + rnd.uniform(-0.4, 0.4)
        d = r * rnd.uniform(0.15, 0.45)
        bx = cx + math.cos(a) * d
        by = cy + math.sin(a) * d - size * 0.05
        br = r * rnd.uniform(0.50, 0.75)
        pygame.draw.circle(surf, color, (int(bx), int(by)), int(br))

    pygame.draw.circle(
        surf, light,
        (int(cx - r * 0.30), int(cy - r * 0.40)),
        max(1, int(r * 0.35))
    )

    if shine:
        pygame.draw.circle(
            surf, bright,
            (int(cx - r * 0.35), int(cy - r * 0.45)),
            max(1, int(r * 0.15))
        )

    return surf.convert_alpha()





_HIGH_RES_RESOURCE_NAMES = {
    "Камень", "Титан", "Медная руда", "Водоросль", "Железная руда",
    "Золотая руда", "Алмаз", "Кварц", "Уголь", "Сера", "Глина",
    "Песок", "Известняк", "Нефть", "Соль", "Серебряная руда",
    "Свинец", "Литий", "Магнетит", "Уранинит", "Рубин",
    "Гелевый мешок", "Сталь", "Медный провод", "Стекло", "Порох",
    "Топливо", "Бетон", "Металлолом", "Кислотный гриб",
    "Образец водоросли", "Гроздь семян водоросли", "Пещерная сера",
    "Образец пластинчатого коралла", "Образец коралловой трубы",
    "Зуб сталкера", "Масляный сок", "Глубинный гриб", "Никелевая руда",
    "Кианит", "Ионный куб", "Газовый пузырь",
}


def _stable_preview_seed(name):
    return 10000 + sum((index + 1) * ord(ch) for index, ch in enumerate(name)) % 50000


def generate_highres_resource_preview(entity, size=280):
    """Redraw a collectible resource at scanner resolution instead of enlarging its tiny icon."""
    name = getattr(entity, "name", "")
    if name not in _HIGH_RES_RESOURCE_NAMES:
        return None

    size = max(96, int(size))
    color = tuple(getattr(entity, "color", (150, 150, 150)))[:3]
    seed = _stable_preview_seed(name)

    if name in {"Водоросль", "Образец водоросли"}:
        return generate_seaweed_sprite(size, seed=seed)

    if name in {
        "Алмаз", "Кварц", "Соль", "Литий", "Магнетит", "Уранинит",
        "Рубин", "Пещерная сера", "Кианит", "Ионный куб", "Зуб сталкера",
        "Стекло",
    }:
        return generate_crystal_sprite(size, color, sparkle=True, seed=seed)

    if "руда" in name or name in {"Сера", "Свинец"}:
        rock_base = _shade(color, -85)
        if max(rock_base) < 45:
            rock_base = (82, 84, 88)
        veins = [
            color,
            _shade(color, 50),
            _shade(color, -35),
        ]
        return generate_ore_sprite(
            size, rock_base, veins,
            vein_count=8, seed=seed,
        )

    if name in {"Камень", "Титан", "Уголь", "Известняк", "Бетон", "Металлолом"}:
        return generate_rock_sprite(size, color, seed=seed)

    if name in {"Сталь", "Медный провод", "Топливо"}:
        return generate_tech_item_sprite(name, size - 12, color)

    # Organic, granular and soft resources get a newly generated detailed mass.
    return generate_lumpy_sprite(
        size, color, seed=seed,
        shine=name in {
            "Нефть", "Гелевый мешок", "Кислотный гриб",
            "Гроздь семян водоросли", "Масляный сок", "Глубинный гриб",
            "Газовый пузырь",
        },
    )


# =========================================================
# ПРОЦЕДУРНАЯ ФЛОРА SUBNAUTICA
# =========================================================

def generate_subnautica_flora_sprite(kind, size, seed=0):
    """Создаёт стилизованный top-down спрайт канонической флоры Subnautica.

    Флора является отдельным декоративным слоем мира и не подменяет
    собираемые ресурсы. Благодаря этому растения не попадают в инвентарь
    сами по себе и не вмешиваются в существующую систему респавна ресурсов.
    """
    rnd = random.Random(seed)
    size = max(12, int(size))
    canvas = max(size + 10, int(size * 1.35))
    surf = pygame.Surface((canvas, canvas), pygame.SRCALPHA)
    cx = canvas // 2
    cy = canvas // 2
    r = max(4, size // 2)

    def pt(x, y):
        return (int(x), int(y))

    def line(color, a, b, width=1):
        pygame.draw.line(surf, color, pt(*a), pt(*b), max(1, int(width)))

    def circle(color, pos, radius, width=0):
        pygame.draw.circle(surf, color, pt(*pos), max(1, int(radius)), width)

    def ellipse(color, rect, width=0):
        pygame.draw.ellipse(
            surf, color,
            pygame.Rect(*(int(v) for v in rect)),
            width
        )

    def polygon(color, points, width=0):
        pygame.draw.polygon(surf, color, [pt(x, y) for x, y in points], width)

    def glow(pos, radius, color, alpha=55):
        g = pygame.Surface((canvas, canvas), pygame.SRCALPHA)
        for mul, a in ((2.1, alpha // 3), (1.55, alpha // 2), (1.15, alpha)):
            pygame.draw.circle(
                g, (*color, max(1, int(a))), pt(*pos),
                max(1, int(radius * mul))
            )
        surf.blit(g, (0, 0))

    # Грибы: Acid Mushroom и Deep Shroom.
    if kind in ('acid_mushroom', 'deep_shroom'):
        deep = kind == 'deep_shroom'
        cap = (110, 72, 190) if not deep else (56, 54, 92)
        rim = (190, 120, 245) if not deep else (110, 102, 165)
        spots = (235, 185, 255) if not deep else (160, 155, 220)
        glow((cx, cy), r * 0.55, rim, 42)
        ellipse((45, 38, 60), (cx-r*.76, cy-r*.42, r*1.52, r*.88))
        ellipse(cap, (cx-r*.70, cy-r*.50, r*1.40, r*.86))
        ellipse(rim, (cx-r*.62, cy-r*.42, r*1.24, r*.65), 2)
        for _ in range(7):
            a = rnd.uniform(0, math.tau)
            d = rnd.uniform(0.10, 0.48) * r
            circle(spots, (cx + math.cos(a)*d, cy + math.sin(a)*d*.62), max(1, r*.07))
        circle((65, 45, 80), (cx, cy+r*.03), r*.16)

    elif kind == 'creepvine':
        # Несколько длинных зелёных лент с жёлтыми семенными гроздьями.
        for strand in range(5):
            phase = rnd.uniform(0, math.tau)
            pts = []
            for i in range(9):
                t = i / 8
                ang = phase + t * 1.25 + strand * 0.16
                rad = r * (0.12 + t * 0.82)
                pts.append((cx + math.cos(ang) * rad, cy + math.sin(ang) * rad))
            for a, b in zip(pts, pts[1:]):
                line((20, 75, 30), a, b, max(3, r*.16))
                line((78, 158, 52), a, b, max(1, r*.09))
            tip = pts[-1]
            for j in range(3):
                a = phase + 2.0 + j * 2.0
                p = (tip[0] + math.cos(a)*r*.12, tip[1] + math.sin(a)*r*.12)
                glow(p, r*.08, (255, 185, 35), 32)
                circle((255, 188, 35), p, r*.07)
                circle((255, 235, 110), (p[0]-1, p[1]-1), r*.025)

    elif kind == 'blood_grass':
        for i in range(18):
            a = rnd.uniform(0, math.tau)
            length = rnd.uniform(r*.48, r*.95)
            bend = rnd.uniform(-0.22, 0.22)
            base = (cx + math.cos(a)*r*.10, cy + math.sin(a)*r*.10)
            tip = (cx + math.cos(a+bend)*length, cy + math.sin(a+bend)*length)
            line((85, 25, 28), base, tip, max(2, r*.10))
            line((170, 48, 55), base, tip, max(1, r*.045))

    elif kind == 'blue_palm':
        circle((60, 95, 115), (cx, cy), r*.22)
        for i in range(8):
            a = i / 8 * math.tau + rnd.uniform(-.08, .08)
            mid = (cx + math.cos(a)*r*.48, cy + math.sin(a)*r*.48)
            tip = (cx + math.cos(a)*r*.88, cy + math.sin(a)*r*.88)
            line((75, 190, 120), (cx, cy), mid, max(2, r*.11))
            line((30, 92, 155), mid, tip, max(3, r*.16))
            circle((55, 145, 190), tip, r*.10)
        circle((160, 225, 95), (cx, cy), r*.11)

    elif kind in ('writhing_weed', 'ghost_weed'):
        ghost = kind == 'ghost_weed'
        base = (65, 110, 115) if ghost else (60, 70, 145)
        stem = (90, 190, 110) if ghost else (145, 75, 185)
        tipc = (235, 80, 90) if ghost else (155, 245, 120)
        circle(base, (cx, cy), r*.25)
        for i in range(9 if not ghost else 6):
            a = i / (9 if not ghost else 6) * math.tau + rnd.uniform(-.2, .2)
            length = rnd.uniform(r*.45, r*.95)
            tip = (cx + math.cos(a)*length, cy + math.sin(a)*length)
            line((45, 45, 70), (cx, cy), tip, max(3, r*.13))
            line(stem, (cx, cy), tip, max(1, r*.07))
            glow(tip, r*.055, tipc, 28)
            circle(tipc, tip, r*.05)

    elif kind in ('spotted_reeds', 'spotted_dockleaf'):
        dock = kind == 'spotted_dockleaf'
        leaf_c = (84, 145, 72) if not dock else (84, 112, 125)
        spot_c = (230, 235, 190) if not dock else (220, 205, 95)
        count = 7 if not dock else 5
        for i in range(count):
            a = i / count * math.tau + rnd.uniform(-.18, .18)
            length = rnd.uniform(r*.52, r*.92)
            half = r * (.13 if not dock else .18)
            tip = (cx + math.cos(a)*length, cy + math.sin(a)*length)
            nx, ny = -math.sin(a)*half, math.cos(a)*half
            polygon((45, 72, 50), [(cx,cy),(tip[0]+nx,tip[1]+ny),tip,(tip[0]-nx,tip[1]-ny)])
            polygon(leaf_c, [(cx,cy),(tip[0]+nx*.72,tip[1]+ny*.72),tip,(tip[0]-nx*.72,tip[1]-ny*.72)])
            for frac in (.45, .70):
                p=(cx+(tip[0]-cx)*frac, cy+(tip[1]-cy)*frac)
                circle(spot_c,p,max(1,r*.035))

    elif kind in ('redwort', 'violet_beau'):
        violet = kind == 'violet_beau'
        stem_c = (110, 58, 62) if not violet else (85, 70, 120)
        tip_c = (220, 68, 62) if not violet else (185, 105, 235)
        for i in range(10):
            a = i / 10 * math.tau + rnd.uniform(-.12,.12)
            length = rnd.uniform(r*.38, r*.86)
            tip=(cx+math.cos(a)*length,cy+math.sin(a)*length)
            line(stem_c,(cx,cy),tip,max(2,r*.09))
            circle(tip_c,tip,r*.09)
        circle((70, 55, 75),(cx,cy),r*.16)

    elif kind in ('tiger_plant', 'spiked_horn_grass'):
        tiger = kind == 'tiger_plant'
        base_c = (95, 40, 25) if tiger else (135, 112, 72)
        stem_c = (195, 60, 40) if tiger else (190, 125, 65)
        spike_c = (245, 210, 85) if tiger else (180, 225, 85)
        circle(base_c,(cx,cy),r*.22)
        for i in range(8):
            a=i/8*math.tau+rnd.uniform(-.13,.13)
            length=rnd.uniform(r*.48,r*.92)
            tip=(cx+math.cos(a)*length,cy+math.sin(a)*length)
            line((70,40,28),(cx,cy),tip,max(4,r*.15))
            line(stem_c,(cx,cy),tip,max(2,r*.09))
            for frac in (.45,.72):
                p=(cx+(tip[0]-cx)*frac,cy+(tip[1]-cy)*frac)
                pa=a+math.pi/2
                q=(p[0]+math.cos(pa)*r*.12,p[1]+math.sin(pa)*r*.12)
                line(spike_c,p,q,max(1,r*.035))

    elif kind in ('mushroom_tree', 'jellyshroom'):
        jelly = kind == 'jellyshroom'
        outer = (70, 105, 150) if not jelly else (96, 55, 145)
        inner = (95, 165, 175) if not jelly else (205, 95, 210)
        bright = (135, 205, 190) if not jelly else (245, 155, 250)
        if jelly:
            glow((cx,cy),r*.70,(180,80,235),46)
        for i in range(6):
            a=i/6*math.tau+rnd.uniform(-.12,.12)
            rr=r*rnd.uniform(.48,.75)
            p=(cx+math.cos(a)*rr*.35,cy+math.sin(a)*rr*.35)
            circle((45,55,72),p,rr*.55)
            circle(outer,p,rr*.50)
            circle(inner,(p[0]-rr*.06,p[1]-rr*.06),rr*.38)
            circle(bright,(p[0]-rr*.14,p[1]-rr*.14),rr*.12)
        circle((35,34,50),(cx,cy),r*.22)
        if jelly:
            circle((235,175,250),(cx,cy),r*.13,2)

    elif kind == 'pygmy_fan':
        for i in range(7):
            a=i/7*math.tau
            p1=(cx+math.cos(a-.28)*r*.18,cy+math.sin(a-.28)*r*.18)
            p2=(cx+math.cos(a)*r*.88,cy+math.sin(a)*r*.88)
            p3=(cx+math.cos(a+.28)*r*.18,cy+math.sin(a+.28)*r*.18)
            polygon((95,55,145),[p1,p2,p3])
            line((210,120,245),(cx,cy),p2,max(1,r*.035))
        glow((cx,cy),r*.22,(175,95,235),28)
        circle((185,110,240),(cx,cy),r*.15)

    elif kind == 'bulb_bush':
        for i in range(9):
            a=i/9*math.tau+rnd.uniform(-.15,.15)
            d=r*rnd.uniform(.25,.72)
            p=(cx+math.cos(a)*d,cy+math.sin(a)*d)
            br=r*rnd.uniform(.18,.30)
            glow(p,br*.7,(90,120,240),25)
            circle((58,63,125),p,br+2)
            circle((96,110,205),p,br)
            circle((155,185,245),(p[0]-br*.25,p[1]-br*.25),br*.24)

    elif kind in ('bloodvine', 'bloodroot'):
        root = kind == 'bloodroot'
        strands = 7 if root else 5
        for i in range(strands):
            a=i/strands*math.tau+rnd.uniform(-.18,.18)
            length=rnd.uniform(r*.55,r*.98)
            mid=(cx+math.cos(a+.22)*length*.5,cy+math.sin(a+.22)*length*.5)
            tip=(cx+math.cos(a)*length,cy+math.sin(a)*length)
            line((50,45,58),(cx,cy),mid,max(5,r*.18 if root else r*.13))
            line((206,215,205),(cx,cy),mid,max(3,r*.11 if root else r*.08))
            line((196,205,200),mid,tip,max(2,r*.08))
            if not root or i % 2 == 0:
                p=(cx+(tip[0]-cx)*.72,cy+(tip[1]-cy)*.72)
                glow(p,r*.09,(220,55,55),34)
                circle((180,35,45),p,r*.08)
                circle((245,90,75),(p[0]-1,p[1]-1),r*.03)

    elif kind == 'gabe_feather':
        for i in range(6):
            a=i/6*math.tau+rnd.uniform(-.12,.12)
            tip=(cx+math.cos(a)*r*.92,cy+math.sin(a)*r*.92)
            line((80,65,105),(cx,cy),tip,max(3,r*.12))
            for frac in (.38,.55,.72,.86):
                p=(cx+(tip[0]-cx)*frac,cy+(tip[1]-cy)*frac)
                side=a+math.pi/2
                length=r*(.18*(1-frac*.35))
                q1=(p[0]+math.cos(side)*length,p[1]+math.sin(side)*length)
                q2=(p[0]-math.cos(side)*length,p[1]-math.sin(side)*length)
                line((170,100,185),p,q1,max(1,r*.035))
                line((170,100,185),p,q2,max(1,r*.035))

    elif kind == 'membraintree':
        glow((cx,cy),r*.62,(70,155,245),35)
        circle((40,70,95),(cx,cy),r*.72)
        circle((110,175,215,145),(cx,cy),r*.65)
        for _ in range(8):
            a=rnd.uniform(0,math.tau); d=rnd.uniform(0,r*.42)
            p=(cx+math.cos(a)*d,cy+math.sin(a)*d)
            circle((215,80,185),p,r*.10)
            circle((245,165,225),(p[0]-1,p[1]-1),r*.035)
        circle((205,235,250),(cx-r*.18,cy-r*.20),r*.18,2)

    elif kind == 'anchor_pod':
        glow((cx,cy-r*.05),r*.56,(60,210,220),45)
        circle((40,80,85),(cx,cy-r*.05),r*.60)
        circle((72,170,175),(cx,cy-r*.05),r*.53)
        circle((115,220,205),(cx-r*.15,cy-r*.20),r*.20)
        for i in range(7):
            a=i/7*math.tau
            start=(cx+math.cos(a)*r*.43,cy-r*.05+math.sin(a)*r*.43)
            end=(cx+math.cos(a)*r*.90,cy+math.sin(a)*r*.90)
            line((100,38,70),start,end,max(2,r*.065))

    elif kind == 'cave_bush':
        for i in range(13):
            a=i/13*math.tau+rnd.uniform(-.12,.12)
            length=rnd.uniform(r*.40,r*.90)
            tip=(cx+math.cos(a)*length,cy+math.sin(a)*length)
            line((65,45,85),(cx,cy),tip,max(3,r*.11))
            line((155,85,190),(cx,cy),tip,max(1,r*.055))
            circle((205,120,225),tip,r*.055)

    elif kind == 'rouge_cradle':
        glow((cx,cy),r*.38,(255,190,55),38)
        circle((55,80,125),(cx,cy),r*.62)
        for i in range(10):
            a=i/10*math.tau
            outer=(cx+math.cos(a)*r*.82,cy+math.sin(a)*r*.82)
            line((135,45,45),(cx,cy),outer,max(2,r*.09))
        circle((120,50,50),(cx,cy),r*.42,2)
        circle((245,190,60),(cx,cy),r*.24)
        circle((255,235,135),(cx-r*.06,cy-r*.06),r*.08)

    elif kind == 'drooping_stinger':
        glow((cx,cy),r*.42,(110,220,145),24)
        for i in range(7):
            a=i/7*math.tau+rnd.uniform(-.15,.15)
            d=rnd.uniform(r*.25,r*.68)
            p=(cx+math.cos(a)*d,cy+math.sin(a)*d)
            circle((40,85,58,190),p,r*.22)
            circle((105,190,105,180),(p[0]-2,p[1]-2),r*.15)
            line((80,180,105),p,(cx,cy),max(1,r*.04))

    elif kind == 'sulfur_plant':
        circle((115,72,40),(cx,cy),r*.56)
        circle((185,105,42),(cx,cy),r*.46)
        polygon((245,220,105),[
            (cx-r*.15,cy-r*.06),(cx,cy-r*.44),(cx+r*.16,cy-r*.05),
            (cx+r*.42,cy+r*.12),(cx,cy+r*.28),(cx-r*.42,cy+r*.12)
        ])
        circle((50,35,28),(cx,cy),r*.17)

    elif kind == 'sea_crown':
        glow((cx,cy),r*.42,(70,190,255),42)
        for i in range(8):
            a=i/8*math.tau
            tip=(cx+math.cos(a)*r*.90,cy+math.sin(a)*r*.90)
            line((115,210,80),(cx,cy),tip,max(3,r*.11))
            circle((225,215,70),tip,r*.06)
        circle((60,115,155),(cx,cy),r*.42)
        circle((95,185,225),(cx,cy),r*.34)
        circle((185,235,245),(cx-r*.09,cy-r*.11),r*.09)

    elif kind == 'regress_shell':
        for i, frac in enumerate((.78,.60,.43,.27)):
            circle((130+20*i,45+12*i,42+10*i),(cx,cy),r*frac, max(2,int(r*.09)))
        for i in range(8):
            a=i/8*math.tau
            tip=(cx+math.cos(a)*r*.88,cy+math.sin(a)*r*.88)
            line((220,145,70),(cx,cy),tip,max(1,r*.035))
            circle((245,235,205),tip,r*.04)

    elif kind == 'eye_stalk':
        for i in range(5):
            a=i/5*math.tau+rnd.uniform(-.2,.2)
            length=rnd.uniform(r*.55,r*.95)
            tip=(cx+math.cos(a)*length,cy+math.sin(a)*length)
            mid=(cx+math.cos(a+.28)*length*.52,cy+math.sin(a+.28)*length*.52)
            line((58,32,82),(cx,cy),mid,max(4,r*.14))
            line((125,60,155),(cx,cy),mid,max(2,r*.08))
            line((120,58,155),mid,tip,max(2,r*.07))
            glow(tip,r*.08,(245,205,70),34)
            circle((245,210,75),tip,r*.07)
            circle((70,55,45),tip,r*.025)

    elif kind == 'furled_papyrus':
        for i in range(7):
            a=i/7*math.tau+rnd.uniform(-.14,.14)
            tip=(cx+math.cos(a)*r*.78,cy+math.sin(a)*r*.78)
            line((75,105,72),(cx,cy),tip,max(3,r*.10))
            # Завиток на конце листа.
            q=(tip[0]+math.cos(a+1.8)*r*.18,tip[1]+math.sin(a+1.8)*r*.18)
            line((165,165,95),tip,q,max(2,r*.07))
            circle((205,190,110),q,r*.045)

    else:
        # Универсальный морской куст — безопасный fallback для будущих видов.
        circle((55,92,72),(cx,cy),r*.18)
        for i in range(8):
            a=i/8*math.tau+rnd.uniform(-.15,.15)
            tip=(cx+math.cos(a)*r*.86,cy+math.sin(a)*r*.86)
            line((85,155,95),(cx,cy),tip,max(2,r*.08))
            circle((145,205,125),tip,r*.06)

    return surf.convert_alpha()

# =========================================================
# СПРАЙТ ДАЙВЕРА
# =========================================================

def generate_diver_sprite(
        size=30,
        suit_color=(30, 100, 180),
        accent_color=(255, 200, 50),
        tank_color=(200, 205, 215)
):
    width = int(size * 2.4)
    height = int(size * 1.7)

    surf = pygame.Surface((width, height), pygame.SRCALPHA)

    center_x = width // 2
    center_y = height // 2

    body_length = int(size * 1.05)
    body_width = int(size * 0.62)

    flipper_length = int(size * 0.7)
    flipper_width = int(size * 0.24)

    flipper_x = center_x - body_length // 2 - flipper_length + 6

    for sign in (-1, 1):
        flipper_y = (
            center_y
            + sign * (body_width // 2 + flipper_width // 2 - 1)
            - flipper_width // 2
        )

        pygame.draw.ellipse(
            surf, (18, 18, 28),
            (flipper_x, flipper_y, flipper_length, flipper_width)
        )
        pygame.draw.ellipse(
            surf, (70, 70, 90),
            (flipper_x, flipper_y, flipper_length, flipper_width),
            1
        )

    tank_length = int(size * 0.6)
    tank_width = int(size * 0.20)
    tank_x = center_x - tank_length // 2 - 2

    for sign in (-1, 1):
        tank_y = (
            center_y
            + sign * (body_width // 2 + tank_width // 2 + 1)
            - tank_width // 2
        )

        pygame.draw.rect(
            surf, tank_color,
            (tank_x, tank_y, tank_length, tank_width),
            border_radius=3
        )
        pygame.draw.rect(
            surf, (90, 95, 110),
            (tank_x, tank_y, tank_length, tank_width),
            1, border_radius=3
        )
        pygame.draw.line(
            surf, (255, 255, 255),
            (tank_x + 3, tank_y + 1),
            (tank_x + tank_length - 3, tank_y + 1),
            1
        )

    pygame.draw.ellipse(
        surf, suit_color,
        (center_x - body_length // 2,
         center_y - body_width // 2,
         body_length, body_width)
    )

    pygame.draw.line(
        surf, accent_color,
        (center_x - body_length // 3, center_y),
        (center_x + body_length // 3, center_y),
        2
    )

    pygame.draw.ellipse(
        surf, accent_color,
        (center_x - body_length // 2,
         center_y - body_width // 2,
         body_length, body_width),
        2
    )

    arm_length = int(size * 0.5)
    arm_width = int(size * 0.16)

    for sign in (-1, 1):
        arm_y = (
            center_y
            + sign * (body_width // 2 + arm_width // 2 - 2)
            - arm_width // 2
        )
        arm_x = center_x + body_length // 4

        pygame.draw.ellipse(
            surf, suit_color,
            (arm_x, arm_y, arm_length, arm_width)
        )
        pygame.draw.ellipse(
            surf, accent_color,
            (arm_x, arm_y, arm_length, arm_width), 1
        )

    head_radius = int(size * 0.30)
    head_x = center_x + body_length // 2 - 1
    head_y = center_y

    pygame.draw.circle(
        surf, (235, 195, 160), (head_x, head_y), head_radius
    )
    pygame.draw.circle(
        surf, (140, 100, 70), (head_x, head_y), head_radius, 1
    )

    mask_width = int(head_radius * 1.6)
    mask_height = int(head_radius * 1.3)
    mask_x = head_x - mask_width // 2 + 2
    mask_y = head_y - mask_height // 2

    pygame.draw.ellipse(
        surf, (70, 180, 220),
        (mask_x, mask_y, mask_width, mask_height)
    )
    pygame.draw.ellipse(
        surf, (20, 60, 90),
        (mask_x, mask_y, mask_width, mask_height), 2
    )
    pygame.draw.ellipse(
        surf, (200, 240, 255),
        (mask_x + 2, mask_y + 2,
         max(2, mask_width // 3), max(2, mask_height // 4))
    )

    pygame.draw.line(
        surf, (255, 200, 0),
        (head_x - 2, head_y - head_radius + 2),
        (center_x - 2, center_y - body_width // 2 - 3),
        2
    )

    return surf.convert_alpha()


# =========================================================
# ТИПЫ
# =========================================================

def point_in_polygon(x, y, points):
    """Return True when a point is inside an arbitrary polygon."""
    inside = False
    j = len(points) - 1

    for i in range(len(points)):
        xi, yi = points[i]
        xj, yj = points[j]

        intersects = (
            (yi > y) != (yj > y)
            and x < (
                (xj - xi) * (y - yi)
                / ((yj - yi) + 1e-9)
                + xi
            )
        )

        if intersects:
            inside = not inside

        j = i

    return inside


def make_blob_points(
        cx, cy,
        radius_x, radius_y,
        seed,
        point_count=22,
        jitter=0.14
):
    """Create a stable irregular outline for a biome."""
    rnd = random.Random(seed)
    points = []

    for i in range(point_count):
        angle = (i / point_count) * math.tau
        radius_mul = rnd.uniform(1.0 - jitter, 1.0 + jitter)
        wave = (
            1.0
            + math.sin(angle * 3 + seed * 0.17) * 0.05
            + math.sin(angle * 5 + seed * 0.31) * 0.035
        )

        px = cx + math.cos(angle) * radius_x * radius_mul * wave
        py = cy + math.sin(angle) * radius_y * radius_mul * wave
        px = max(0, min(MAP_SIZE - 1, px))
        py = max(0, min(MAP_SIZE - 1, py))
        points.append((px, py))

    return points


def make_corridor_polygon(x1, y1, x2, y2, width):
    """Create a thick polygon corridor between two points."""
    dx = x2 - x1
    dy = y2 - y1
    distance = math.hypot(dx, dy)

    if distance <= 0.001:
        return make_blob_points(
            x1, y1,
            width, width,
            seed=int(x1 + y1),
            point_count=12,
            jitter=0.08
        )

    ux = dx / distance
    uy = dy / distance
    nx = -uy
    ny = ux
    half = width / 2.0

    sx = x1 - ux * half
    sy = y1 - uy * half
    ex = x2 + ux * half
    ey = y2 + uy * half

    return [
        (sx + nx * half, sy + ny * half),
        (sx - nx * half, sy - ny * half),
        (ex - nx * half, ey - ny * half),
        (ex + nx * half, ey + ny * half),
    ]


class Biome:

    def __init__(
            self,
            name,
            color,
            x1, y1, x2, y2,
            objects,
            animals,
            passable=True,
            polygon=None,
            map_label=None,
            cave_enabled=False,
            priority=10,
            clip_biome=None
    ):
        self.name = name
        self.color = color
        self.objects = objects
        self.animals = animals
        self.flora = []
        self.passable = passable
        self.map_label = map_label
        self.cave_enabled = cave_enabled
        self.priority = priority
        self.clip_biome = clip_biome

        if polygon:
            self.polygon = [
                (float(px), float(py))
                for px, py in polygon
            ]
            xs = [p[0] for p in self.polygon]
            ys = [p[1] for p in self.polygon]
            self.rect = (
                int(min(xs)),
                int(min(ys)),
                int(max(xs)),
                int(max(ys))
            )
        else:
            self.polygon = None
            self.rect = (x1, y1, x2, y2)

    def contains(self, x, y):
        x1, y1, x2, y2 = self.rect

        if not (x1 <= x <= x2 and y1 <= y <= y2):
            return False

        if self.polygon is not None:
            if not point_in_polygon(x, y, self.polygon):
                return False

        if self.clip_biome is not None:
            if not self.clip_biome.contains(x, y):
                return False

        return True

    def center(self):
        if self.polygon:
            x = sum(p[0] for p in self.polygon) / len(self.polygon)
            y = sum(p[1] for p in self.polygon) / len(self.polygon)
            return x, y

        x1, y1, x2, y2 = self.rect
        return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)

    def area(self):
        if self.polygon:
            result = 0.0
            count = len(self.polygon)

            for i in range(count):
                x1, y1 = self.polygon[i]
                x2, y2 = self.polygon[(i + 1) % count]
                result += x1 * y2 - x2 * y1

            return abs(result) / 2.0

        x1, y1, x2, y2 = self.rect
        return (x2 - x1 + 1) * (y2 - y1 + 1)

    def random_point(self, rng=None):
        if rng is None:
            rng = random

        x1, y1, x2, y2 = self.rect

        for _ in range(400):
            x = rng.uniform(x1, x2)
            y = rng.uniform(y1, y2)
            if self.contains(x, y):
                return x, y

        return self.center()

    def map_points(self):
        if self.polygon:
            return self.polygon

        x1, y1, x2, y2 = self.rect
        return [
            (x1, y1),
            (x2 + 1, y1),
            (x2 + 1, y2 + 1),
            (x1, y2 + 1)
        ]

    def shift(self, dx, dy):
        x1, y1, x2, y2 = self.rect
        self.rect = (x1 + dx, y1 + dy, x2 + dx, y2 + dy)

        if self.polygon:
            self.polygon = [
                (x + dx, y + dy)
                for x, y in self.polygon
            ]



# =========================================================
# БИОЛЮМИНЕСЦЕНЦИЯ V2 — ОРГАНЫ И ЦВЕТА SUBNAUTICA
# =========================================================
# Никакой случайной светящейся крапинки на всех подряд организмах.
# Каждый вид имеет собственные световые органы. Для существ, у которых
# в оригинале нет выраженного свечения, подсветка отсутствует.
# Форма глаза Пискуна и семенные гроздья Creepvine определяются по
# цветам исходных Pygame-спрайтов, а не по приблизительному овалу.

def _bio_normalize_kind(value):
    return str(value).lower().replace(' ', '_').replace('-', '_')


def _bio_stable_seed(value):
    return sum((i + 1) * ord(c) for i, c in enumerate(str(value)))


def _bio_make_electric_nodes(bounds, pad):
    """Узлы электрических ампул на верхней/нижней стороне угря.

    Рыба в исходном коде ориентирована вправо. Координаты нормированы
    по непрозрачной области исходной картинки, а не по полям спрайта.
    """
    nodes = []
    # Смещаем ряды: «шахматное» положение соответствует ампулам на сегментах.
    for row, vv in enumerate((0.12, 0.88)):
        positions = (0.11, 0.20, 0.29, 0.38, 0.47, 0.56, 0.65, 0.74, 0.82, 0.90)
        for i, uu in enumerate(positions):
            yv = vv + (0.06 if row == 0 else -0.06) * (i % 3 == 0)
            nodes.append((pad + bounds.left + bounds.width * uu,
                          pad + bounds.top + bounds.height * yv, row, i))
    return nodes


def _bio_light_art(original, species, is_plant=False, seed=0):
    """Рендерит ТОЛЬКО светящиеся участки, строго отдельно от тела.

    На выходе картинка с полями для ореола, которая может независимо
    поворачиваться вместе с исходной рыбой.
    """
    if original is None:
        return None
    bounds = original.get_bounding_rect(min_alpha=125)
    if bounds.width == 0 or bounds.height == 0:
        return None
    kind = _bio_normalize_kind(species)
    # Левиафаны вызываются и по sprite_kind, и по полному игровому имени.
    kind = {'reefback_leviathan':'reefback',
            'sea_treader_leviathan':'sea_treader',
            'sea_dragon_leviathan':'sea_dragon',
            'reaper_leviathan':'reaper'}.get(kind, kind)
    w, h = original.get_size()
    pad = max(12, min(33, int(max(bounds.width, bounds.height) * 0.14)))
    dims = (w + pad * 2, h + pad * 2)
    aura = pygame.Surface(dims, pygame.SRCALPHA)
    core = pygame.Surface(dims, pygame.SRCALPHA)
    cx, cy = pad + bounds.centerx, pad + bounds.centery
    # Все относительные координаты относятся к реальному рисунку, а не к canvas.
    def pos(u, v):
        return (round(pad + bounds.left + bounds.width * u),
                round(pad + bounds.top + bounds.height * v))

    def dot(x, y, radius, color, white=None, intensity=1.0):
        x, y = int(x), int(y)
        r = max(1, int(radius))
        for m, a in ((5, 9), (3.2, 19), (2.05, 42), (1.35, 65)):
            pygame.draw.circle(aura, (*color, min(255, round(a*intensity))),
                               (x, y), max(1, round(r*m)))
        pygame.draw.circle(core, (*color, min(255, round(205*intensity))),
                           (x, y), r+1)
        if white is None:
            white = tuple(min(255, round(c * .40 + 255 * .60)) for c in color)
        pygame.draw.circle(core, (*white, min(255, round(249*intensity))),
                           (x, y), r)

    def orb(u, v, relative_radius, color, intensity=1.0):
        x, y = pos(u, v)
        dot(x, y, max(1, round(min(bounds.width, bounds.height) * relative_radius)),
            color, intensity=intensity)

    def path(vertices, color, thickness=1, intensity=1.0):
        if len(vertices) < 2:
            return
        points = [pos(x, y) for x, y in vertices]
        thickness = max(1, round(thickness))
        for broad, alpha in ((6, 14), (3, 32)):
            pygame.draw.lines(aura, (*color, round(alpha * intensity)),
                              False, points, thickness + broad)
        pygame.draw.lines(core, (*color, round(205 * intensity)),
                          False, points, thickness + 1)
        pale = tuple(min(255, round(c * .55 + 255 * .45)) for c in color)
        pygame.draw.lines(core, (*pale, round(225 * intensity)), False, points,
                          max(1, thickness // 2))

    def luminous_oval(u, v, rw, rh, color, fill=False, intensity=1.0):
        x, y = pos(u, v)
        rx = max(2, round(bounds.width * rw))
        ry = max(2, round(bounds.height * rh))
        rectangle = pygame.Rect(x-rx, y-ry, rx*2, ry*2)
        broad = rectangle.inflate(max(4, rx//2), max(4, ry//2))
        pygame.draw.ellipse(aura, (*color, round(26*intensity)), broad)
        pygame.draw.ellipse(aura, (*color, round(56*intensity)), rectangle)
        pygame.draw.ellipse(core, (*color, round((105 if fill else 220)*intensity)),
                            rectangle, 0 if fill else max(1, min(rx, ry)//3))
        if not fill:
            inner = rectangle.inflate(-max(2, rx//3), -max(2, ry//3))
            if inner.width>1 and inner.height>1:
                pygame.draw.ellipse(core, (245, 250, 255, round(75*intensity)), inner, 1)

    def color_pixels(predicate, glow_color, region=None, stride=1, max_points=300):
        """Выделить точно окрашенный орган из уже нарисованного спрайта.

        Сохраняет форму глазных склер, семенных гроздьев, капюшонов и узоров.
        """
        x0, y0, x1, y1 = bounds.left, bounds.top, bounds.right, bounds.bottom
        if region is not None:
            ux0, vy0, ux1, vy1 = region
            x0 = max(x0, int(bounds.left+bounds.width*ux0))
            x1 = min(x1, int(bounds.left+bounds.width*ux1))
            y0 = max(y0, int(bounds.top+bounds.height*vy0))
            y1 = min(y1, int(bounds.top+bounds.height*vy1))
        chosen = []
        for yy in range(y0, y1, stride):
            for xx in range(x0, x1, stride):
                r, g, b, a = original.get_at((xx, yy))
                if a >= 170 and predicate(r, g, b):
                    px, py = xx+pad, yy+pad
                    chosen.append((px, py))
                    pygame.draw.rect(core, (*glow_color, 245), (px, py, stride, stride))
        if chosen:
            step = max(1, len(chosen)//max_points)
            for i in range(0, len(chosen), step):
                px, py = chosen[i]
                pygame.draw.circle(aura, (*glow_color, 25), (px,py),
                                   max(3, min(7, round(min(bounds.size)/10))))
        return len(chosen)

    if is_plant:
        # Несветящиеся виды оставляем тёмными, как в оригинальной игре.
        if kind in ('blood_grass', 'redwort', 'tiger_plant',
                    'spiked_horn_grass', 'mushroom_tree', 'gabe_feather',
                    'regress_shell', 'furled_papyrus'):
            return None

        if kind in ('гроздь_семян_водоросли', 'creepvine_seed_cluster'):
            luminous_oval(.50,.50,.36,.34,(255,208,32),fill=True,intensity=1.15)
            for u,v in ((.30,.37),(.65,.36),(.55,.67)):
                orb(u,v,.10,(255,220,72),1.10)
        elif kind in ('кислотный_гриб', 'acid_mushroom_item'):
            luminous_oval(.50,.50,.36,.29,(190,104,242),fill=True,intensity=.6)
        elif kind in ('глубинный_гриб', 'deep_shroom_item'):
            luminous_oval(.50,.50,.34,.27,(127,109,220),fill=True,intensity=.65)
        elif kind in ('масляный_сок', 'blood_oil'):
            for u,v in ((.38,.45),(.59,.38),(.52,.64)):
                orb(u,v,.12,(229,53,68),.9)
        elif kind in ('гелевый_мешок', 'gel_sack'):
            for u,v in ((.30,.40),(.58,.31),(.63,.63),(.39,.69)):
                orb(u,v,.085,(200,120,255),.76)
        elif kind == 'creepvine':
            # В оригинале светятся только ГРОЗДЬЯ семян, НЕ стебель и листья.
            # Геометрия восстанавливается точно: те же random() и те же
            # формулы, что у generate_subnautica_flora_sprite('creepvine').
            # Цвет семян выделяется прямо из оригинального Pygame-спрайта;
            # поэтому позиции совпадают с рисунком при любом размере.
            found = color_pixels(lambda r,g,b: r>202 and g>125 and
                                 14<b<175 and r>g*0.94 and g>b+40,
                                 (255, 218, 66), stride=1, max_points=170)
            if not found:
                for u,v in ((.33,.32),(.38,.35),(.66,.60),(.68,.55)):
                    orb(u,v,.045,(255,195,24),1.15)
            # Пульсирующее золотистое зарево без зелёных прожилок.
        elif kind in ('acid_mushroom', 'deep_shroom'):
            col=(176, 100, 235) if kind=='acid_mushroom' else (133, 102, 207)
            luminous_oval(.50,.45,.31,.29,col)
            for u,v in ((.32,.37),(.52,.32),(.68,.45),(.45,.60)):
                orb(u,v,.040,col,.55)
        elif kind == 'jellyshroom':
            # Шляпки пещерных медузных грибов.
            for u,v in ((.30,.39),(.51,.29),(.71,.40),(.38,.65),(.65,.70)):
                luminous_oval(u,v,.12,.09,(195,96,242),fill=True)
        elif kind == 'bulb_bush':
            # Голубые луковицы, а не весь куст.
            for u,v in ((.28,.34),(.53,.25),(.72,.38),(.35,.62),(.64,.70),(.5,.50)):
                luminous_oval(u,v,.105,.090,(65,145,255),fill=True)
                orb(u-.03,v-.025,.035,(120,225,255))
        elif kind in ('bloodvine','bloodroot'):
            # Кровавые масляные мешочки на белых ветвях.
            for u,v in ((.21,.37),(.42,.23),(.77,.35),(.69,.74),(.35,.78)):
                orb(u,v,.070,(230,42,62))
        elif kind == 'eye_stalk':
            # Желтые рецепторы на кончиках стеблей.
            for u,v in ((.22,.35),(.53,.18),(.81,.43),(.65,.83),(.23,.72)):
                orb(u,v,.060,(255,209,45))
        elif kind == 'sea_crown':
            luminous_oval(.5,.5,.25,.25,(62,175,255),fill=True)
            for i in range(8):
                a=i*math.tau/8
                orb(.5+.39*math.cos(a), .5+.39*math.sin(a),.026,(235,220,105))
        elif kind == 'drooping_stinger':
            for u,v in ((.30,.35),(.52,.29),(.69,.46),(.38,.68),(.60,.70)):
                luminous_oval(u,v,.10,.09,(93,232,128),fill=True,intensity=.8)
        elif kind in ('ghost_weed','writhing_weed'):
            color=(123,220,251) if kind=='ghost_weed' else (146,236,123)
            for i in range(7):
                a=math.tau*i/7
                orb(.5+.38*math.cos(a),.5+.38*math.sin(a),.028,color,.7)
        elif kind in ('membraintree','anchor_pod'):
            color=(255,107,217) if kind=='membraintree' else (85,231,232)
            luminous_oval(.50,.48,.30,.30,color,fill=True,intensity=.64)
            for u,v in ((.42,.35),(.61,.43),(.50,.59)):
                orb(u,v,.05,color)
        elif kind == 'rouge_cradle':
            luminous_oval(.50,.50,.20,.20,(255,207,76),fill=True)
        elif kind == 'pygmy_fan':
            for i in range(7):
                a=math.tau*i/7
                path(((.5,.5),(.5+.40*math.cos(a),.5+.40*math.sin(a))),
                     (183,105,238),1,.65)
        elif kind in ('spotted_reeds','spotted_dockleaf'):
            col=(210,228,155) if kind=='spotted_reeds' else (223,207,99)
            for i in range(8):
                a=math.tau*i/8
                for rad in (.21,.32):
                    orb(.5+rad*math.cos(a),.5+rad*math.sin(a),.025,col,.6)
        elif kind in ('blue_palm','cave_bush','violet_beau','sulfur_plant'):
            col={'blue_palm':(73,158,240),'cave_bush':(191,130,221),
                 'violet_beau':(189,105,235),'sulfur_plant':(235,210,83)}[kind]
            if kind=='sulfur_plant':
                luminous_oval(.50,.50,.20,.12,col,fill=True,intensity=.44)
            else:
                for i in range(8):
                    a=i*math.tau/8
                    orb(.5+.36*math.cos(a),.5+.36*math.sin(a),.028,col,.57)
        else:
            # Не дополняем неизвестные растения придуманными световыми пятнами.
            return None
    else:
        # Крупные виды: только собственные светящиеся органы, НЕ яркое тело.
        if kind in ('peeper',):
            # Золотистая склера большого глаза, без черного зрачка.
            n = color_pixels(lambda r,g,b: r>173 and g>142 and
                             16<b<187 and r>b+45 and g>b+39,
                             (255,232,65), region=(.48,.13,.91,.89),
                             max_points=160)
            if not n:
                luminous_oval(.71,.5,.092,.31,(255,222,47))
        elif kind == 'ampeel':
            # Настоящие бело-бирюзовые кончики электрических ампул.
            for x,y,row,i in _bio_make_electric_nodes(bounds,pad):
                dot(x,y,max(1,round(min(bounds.size)*.040)),(71,219,255),
                    white=(225,255,255),intensity=1.1)
            orb(.88,.48,.038,(69,243,215))  # Бирюзовый глаз.
        elif kind == 'ghost_leviathan':
            # Полупрозрачная светящаяся кожа, синие щёчные отростки и рёбра.
            for j in range(2):
                v = .30 if j == 0 else .70
                path([( .09,v),(.29,v-.04 if j==0 else v+.04),
                      (.62,v-.08 if j==0 else v+.08),(.86,v)],
                     (85,185,246),2,.67)
            for u in (.20,.35,.50,.65,.8):
                path([(u,.35),(u+.02,.65)],(138,230,255),1,.34)
            path([(.82,.35),(.92,.20),(1.0,.14)],(154,231,255),2)
            path([(.82,.65),(.92,.80),(1.0,.86)],(154,231,255),2)
            orb(.90,.45,.06,(162,240,255))
        elif kind == 'jellyray':
            # Голубоватые края перепончатых крыльев.
            for side in (-1,1):
                vv=.50+side*.42
                path([(.25,.50),(.47,.50+side*.21),(.66,vv),(.84,.50+side*.19)],
                     (98,198,255),2,.73)
            luminous_oval(.55,.5,.14,.13,(128,221,255),fill=True,intensity=.7)
        elif kind == 'crabsquid':
            # Четыре крупные голубые глазницы и светящаяся сеточка купола.
            for u,v in ((.72,.31),(.72,.69),(.52,.35),(.52,.65)):
                luminous_oval(u,v,.04,.10,(91,184,255),fill=True)
            for i in range(5):
                x=.48+i*.048
                path([(x,.30),(x+.055,.51),(x,.70)],(97,230,195),1,.75)
        elif kind == 'mesmer':
            # Фиолетово-синие каймы гипнотизирующих плавников и глаз.
            for sign in (-1,1):
                path([(.32,.5),(.45,.5+sign*.40),(.68,.5+sign*.25),(.81,.5)],
                     (125,147,255),2,.88)
            orb(.75,.50,.095,(240,180,255))
        elif kind == 'warper':
            for u,v in ((.61,.36),(.74,.48),(.60,.65)):
                orb(u,v,.045,(94,214,255))
            path([(.35,.24),(.55,.31),(.70,.47),(.53,.75)],(128,90,255),2,.8)
        elif kind == 'reefback':
            # Синие световые органы на нижней мягкой части, не на панцире.
            for u,v in ((.27,.28),(.38,.75),(.56,.80),(.67,.33),(.76,.65)):
                orb(u,v,.025,(119,188,255),.6)
        elif kind == 'sea_treader':
            for u,v in ((.24,.23),(.24,.78),(.54,.45)):
                orb(u,v,.033,(127,207,255),.8)
        elif kind == 'sea_dragon':
            # Оранжевые рецепторы на голове, боках, хвостовых отростках.
            for u,v in ((.92,.35),(.92,.65)):
                orb(u,v,.045,(255,172,50))
            for i in range(7):
                u=.15+i*.092
                for vv in (.30,.70):
                    orb(u,vv,.020,(255,104,38),.72)
        elif kind in ('reaper', 'stalker', 'sand_shark', 'boneshark'):
            # У хищников тёмный силуэт, светятся в основном глаза.
            col=(255,180,72) if kind=='reaper' else (177,224,123)
            for vv in (.36,.64):
                orb(.82,vv,.04,col,.94)
        elif kind in ('crabsnake','biter','blighter','crashfish'):
            col={'crabsnake':(213,113,238),'biter':(255,130,83),
                 'blighter':(251,97,139),'crashfish':(255,205,72)}[kind]
            for vv in (.35,.65):
                orb(.84,vv,.033,col,.85)
            if kind=='crabsnake':
                for u in (.27,.40,.53,.66):
                    orb(u,.27,.018,(158,107,224),.68)
        elif kind == 'spadefish':
            # Бирюзовые пятна на контуре тела и красные световые усики.
            for uu in (.29,.41,.55,.67,.79):
                for vv in (.26,.74):
                    orb(uu,vv,.027,(94,240,244),.88)
            for sign in (-1,1):
                path([(.56,.5+sign*.16),(.63,.5+sign*.43)],
                     (255,75,91),2,.86)
        elif kind == 'eyeye':
            # Огромная светящаяся желто-зеленая радужка.
            luminous_oval(.74,.49,.090,.28,(236,238,99),fill=False)
        elif kind == 'oculus':
            # Синий биолюминесцентный глаз и отметины на теле.
            luminous_oval(.76,.49,.070,.21,(93,194,255))
            for u in (.29,.43,.58):
                orb(u,.32,.030,(138,176,252),.6)
        elif kind == 'spinefish':
            # Освещённые глаза и кончики костяных игл.
            orb(.83,.44,.048,(140,223,255))
            for u in (.25,.39,.54,.69):
                orb(u,.19,.015,(130,180,235),.55)
        elif kind == 'rabbit_ray':
            # Светящиеся голубые линии по краям широких крыльев.
            for side in (-1,1):
                path([(.16,.5),(.41,.5+side*.31),(.61,.5+side*.43),
                      (.81,.5+side*.22)],(104,187,252),2,.83)
            orb(.70,.50,.057,(128,219,255),.8)
        elif kind == 'reginald':
            # Светящееся светло-зелёное око.
            orb(.79,.46,.053,(194,234,113),.82)
        elif kind == 'bladderfish':
            # Розово-лиловые полупрозрачные боковые пузыри.
            for vv in (.23,.77):
                luminous_oval(.50,vv,.17,.13,(241,99,199),fill=True,intensity=.44)
        elif kind in ('boomerang','garryfish','holefish','hoverfish','hoopfish'):
            col={'boomerang':(255,213,87),'garryfish':(235,229,145),
                 'holefish':(166,209,245),'hoverfish':(248,230,137),
                 'hoopfish':(155,214,240)}[kind]
            # Незначительная подсветка глаз, без сплошной сияющей чешуи.
            orb(.75,.46,.055,col,.75)
        elif kind == 'gasopod':
            # Небольшие биолюминесцентные глаза, а не токсичное облако.
            for vv in (.39,.63):
                orb(.84,vv,.032,(184,212,110),.75)
        else:
            return None

    result = pygame.Surface(dims, pygame.SRCALPHA)
    result.blit(aura, (0,0))
    result.blit(core, (0,0))
    return result.convert_alpha()


def generate_bioluminescence_sprite(original, species, is_plant=False, seed=0):
    return _bio_light_art(original, species, is_plant, seed)


def _bio_electric_frame(base, phase, original=None):
    """Сменные видимые электрические разряды. В кадре 0 дуг нет."""
    if base is None:
        return None
    out = base.copy()
    if phase == 0:
        return out
    rng = random.Random(71003 + phase * 811)
    # Те же координаты ампул, которые использованы при создании
    # статичного свечения, поэтому разряды точно попадают в кончики.
    if original is not None:
        original_bounds = original.get_bounding_rect(min_alpha=125)
        padding = (base.get_width() - original.get_width()) // 2
        nodes = _bio_make_electric_nodes(original_bounds, padding)
    else:
        nodes = _bio_make_electric_nodes(
            pygame.Rect(0, 0, base.get_width(), base.get_height()), 0)
    # Дуги перескакивают между соседними кончиками и вдоль корпуса.
    cases = {
        1: ((0,2),(3,5),(9,12),(14,16)),
        2: ((1,3),(4,6),(10,13),(16,18),(7,17)),
        3: ((2,5),(5,8),(11,14),(14,17),(6,16)),
        4: ((0,1),(3,4),(6,8),(10,11),(15,18)),
        5: ((2,4),(6,9),(11,13),(15,17),(5,15)),
    }
    links = cases.get(phase, ())
    outline=pygame.Surface(base.get_size(),pygame.SRCALPHA)
    for a,b in links:
        ax,ay=nodes[a][:2]; bx,by=nodes[b][:2]
        points=[(round(ax),round(ay))]
        dx,dy=bx-ax,by-ay
        dist=math.hypot(dx,dy) or 1.0
        for i in range(1,9):
            t=i/9
            zig=rng.uniform(-1,1)*max(2.0,min(6.0,dist*.15))
            points.append((round(ax+dx*t-dy/dist*zig),
                           round(ay+dy*t+dx/dist*zig)))
        points.append((round(bx),round(by)))
        pygame.draw.lines(outline,(20,100,255,45),False,points,9)
        pygame.draw.lines(outline,(30,165,255,115),False,points,5)
        pygame.draw.lines(outline,(114,221,255,235),False,points,2)
        pygame.draw.lines(outline,(241,255,255,255),False,points,1)
        for endpoint in (points[0],points[-1]):
            pygame.draw.circle(outline,(120,245,255,90),endpoint,6)
            pygame.draw.circle(outline,(235,255,255,245),endpoint,2)
    out.blit(outline,(0,0))
    return out


class FloraType:

    def __init__(self, name, kind, size, seed=0):
        self.name = name
        self.kind = kind
        self.size = int(size)
        self.seed = int(seed)
        self.image = generate_subnautica_flora_sprite(
            kind, self.size, seed=self.seed
        )
        self.glow_image = generate_bioluminescence_sprite(
            self.image, kind, is_plant=True, seed=self.seed
        )


class ObjectType:

    def __init__(
            self,
            name,
            color,
            size,
            shape="circle",
            image_path=None,
            volume=1,
            is_buildable=False,
            is_wall=False,
            edible=False,
            hunger_value=0,
            thirst_value=0,
            is_weapon=False,
            damage=0,
            weapon_range=0,
            weapon_type=""
    ):
        self.name = name
        self.color = color
        self.size = size
        self.shape = shape

        self.volume = volume
        self.is_buildable = is_buildable
        self.is_wall = is_wall
        self.edible = edible
        self.hunger_value = hunger_value
        self.thirst_value = thirst_value
        self.is_weapon = is_weapon
        self.damage = damage
        self.weapon_range = weapon_range
        self.weapon_type = weapon_type

        self.image = None
        if image_path and os.path.exists(image_path):
            self.image = load_image_with_proportions(image_path, size)


class AnimalType:

    def __init__(
            self,
            name,
            color,
            size,
            shape="circle",
            speed=0.05,
            behavior="neutral",
            image_path=None,
            volume=1,
            hp=10,
            damage=0,
            edible=False,
            hunger_value=0,
            thirst_value=0,
            fish_style=False,
            fish_length=None,
            fish_width=None,
            body_color=None,
            spine_color=None,
            belly_color=None,
            fin_color=None,
            spot_colors=None,
            tail_color=(255, 165, 0),
            leviathan_style=False,
            leviathan_length=280,
            leviathan_width=44,
            sprite_kind=None,
            schooling=False,
            fear_distance=None,
            zigzag_strength=0.0,
            speed_variation=0.12,
            flee_speed_boost=1.65
    ):
        self.name = name
        self.color = color
        self.size = size
        self.shape = shape
        self.speed = speed
        self.behavior = behavior
        self.volume = volume
        self.hp = hp
        self.damage = damage
        self.edible = edible
        self.hunger_value = hunger_value
        self.thirst_value = thirst_value

        self.fish_style = (
            fish_style or leviathan_style or sprite_kind is not None
        )
        self.schooling = schooling
        self.sprite_kind = sprite_kind

        # Параметры плавания измеряются в КЛЕТКАХ (не пикселях).
        # Преследование игрока начинается лишь внутри радиуса испуга.
        self.fear_distance = (
            float(fear_distance) if fear_distance is not None
            else (2.7 if behavior == "prey" else 0.0)
        )
        self.zigzag_strength = float(zigzag_strength)  # радианы
        self.speed_variation = float(speed_variation)
        self.flee_speed_boost = float(flee_speed_boost)

        # Effective visual length is also used by the companion AI: small
        # creatures stay close to the diver, while leviathans keep farther away.
        if leviathan_style:
            self.fish_length = float(leviathan_length)
            self.fish_width = float(leviathan_width)
        else:
            self.fish_length = float(
                fish_length if fish_length is not None else max(20, size * 3)
            )
            self.fish_width = float(
                fish_width if fish_width is not None
                else max(6, self.fish_length / 6)
            )

        self.is_weapon = False
        self.is_buildable = False
        self.weapon_range = 0
        self.weapon_type = ""

        self.image = None

        if image_path and os.path.exists(image_path):
            self.image = load_image_with_proportions(image_path, size)
        elif leviathan_style:
            self.image = generate_ghost_leviathan_sprite(
                leviathan_length, leviathan_width
            )
        elif sprite_kind is not None:
            length = (
                fish_length if fish_length is not None
                else max(20, size * 3)
            )
            width = (
                fish_width if fish_width is not None
                else max(6, length // 6)
            )
            self.image = generate_subnautica_creature_sprite(
                sprite_kind, length, width
            )
        elif fish_style:
            length = (
                fish_length if fish_length is not None
                else max(20, size * 3)
            )
            width = (
                fish_width if fish_width is not None
                else max(6, length // 6)
            )
            body = body_color if body_color is not None else color
            spine = (
                spine_color if spine_color is not None
                else tuple(max(0, c - 60) for c in body)
            )
            belly = (
                belly_color if belly_color is not None
                else tuple(min(255, c + 40) for c in body)
            )
            fins = fin_color if fin_color is not None else spine
            spots = spot_colors if spot_colors is not None else [spine]

            # Палитра сохранена для повторной векторной прорисовки при зуме.
            self._hd_fish_palette = (body, spine, belly, fins, spots, tail_color)
            self.image = generate_pike_style_sprite(
                length, width, body, spine, belly, fins, spots, tail_color
            )

        # Общий для вида слой свечения и кеш его поворотов.
        self.glow_image = generate_bioluminescence_sprite(
            self.image, self.sprite_kind or self.name
        )
        self.glow_rotated_cache = {}
        self.rotated_cache = {}
        # Дуги Ampeel: пять форм разрядов + один спокойный кадр.
        # Остальные 30 видов не требуют покадровой перегенерации света.
        self.electric_glow_frames = (
            [_bio_electric_frame(self.glow_image, i, self.image) for i in range(6)]
            if self.sprite_kind == 'ampeel' and self.glow_image is not None
            else None
        )

    def get_rotated_glow(self, angle, electric_phase=0):
        if self.glow_image is None:
            return None
        angle = quantize_angle(angle)
        phase = (electric_phase % 6) if self.electric_glow_frames else 0
        key = (angle, phase)
        result = self.glow_rotated_cache.get(key)
        if result is None:
            src = (self.electric_glow_frames[phase]
                   if self.electric_glow_frames else self.glow_image)
            result = pygame.transform.rotate(src, angle)
            self.glow_rotated_cache[key] = result
        return result

    def get_rotated(self, angle):
        if self.image is None:
            return None

        angle = quantize_angle(angle)
        image = self.rotated_cache.get(angle)

        if image is None:
            image = pygame.transform.rotate(self.image, angle)
            self.rotated_cache[angle] = image

        return image


class Recipe:

    def __init__(self, name, ingredients, result, result_count=1,
                 station="Изготовитель", category="Разное"):
        self.name = name
        self.ingredients = ingredients
        self.result = result
        self.result_count = max(1, int(result_count))
        self.station = station
        self.category = category

    def can_craft(self, inventory_counts):
        for (item, needed) in self.ingredients.items():
            if inventory_counts.get(item, 0) < needed:
                return False
        return True

    def craft(self, inventory, inventory_counts):
        if not self.can_craft(inventory_counts):
            return None

        for (needed_item, needed_count) in self.ingredients.items():
            removed = 0
            for index, item in enumerate(inventory):
                if removed >= needed_count:
                    break
                if item == needed_item:
                    inventory[index] = None
                    removed += 1

            inventory_counts[needed_item] -= needed_count
            if inventory_counts[needed_item] <= 0:
                del inventory_counts[needed_item]

        return self.result


# =========================================================
# РЕСУРСЫ, ЖИВОТНЫЕ, КРАФТ, БИОМЫ
# =========================================================

def init_assets():
    global rock_type
    global titan_type
    global copper_type
    global seaweed_type

    global iron_type
    global gold_type
    global diamond_type
    global quartz_type
    global coal_type
    global sulfur_type
    global clay_type
    global sand_type
    global limestone_type
    global oil_type
    global salt_type
    global silver_type
    global lead_type
    global lithium_type
    global magnetite_type
    global uraninite_type
    global ruby_type
    global gel_sack_type
    global kyanite_type

    global steel_type
    global provod_type
    global glass_type
    global gunpowder_type
    global fuel_type
    global concrete_type

    global peeper_type
    global bladderfish_type
    global boomerang_type
    global garryfish_type
    global holefish_type
    global hoverfish_type
    global hoopfish_type
    global reginald_type
    global spadefish_type
    global eyeye_type
    global oculus_type
    global rabbit_ray_type
    global jellyray_type
    global spinefish_type

    global biter_type
    global blighter_type
    global crashfish_type
    global stalker_type
    global sand_shark_type
    global boneshark_type
    global ampeel_type
    global mesmer_type
    global crabsquid_type
    global crabsnake_type
    global gasopod_type
    global warper_type

    global reefback_type
    global reaper_type
    global ghost_leviathan_type
    global sea_treader_type
    global sea_dragon_type

    global wall_type
    global floor_type
    global habitat_builder_type

    # Предметы и постройки, к которым обращаются методы Game во время игры.
    global fins_type, reinforced_suit, water_filtration_suit, rebreather_type
    global first_aid_kit, flashlight_type, seaglide_type, flare_type
    global fire_extinguisher, air_bladder, scanner_type, pathfinder_tool
    global repair_tool, repair_kit, propulsion_cannon, repulsion_cannon, stasis_rifle
    global laser_cutter, creature_decoy, scanner_range, beacon_type
    global spotlight_type, floodlight_type, solar_panel_type, grav_trap
    global exterior_growbed, plant_pot, indoor_growbed, plant_shelf
    global composite_pot, chic_pot
    global bed_type, bench_type, chair_type, vending_machine, coffee_machine
    global water_filtration_machine, medical_fabricator, scanner_room_type
    global radio_type

    # Транспорт используется не только при создании рецептов, но и
    # непосредственно методами Game (HP, управление, ремонт, отрисовка).
    global seamoth_type, cyclops_type

    # Полный реестр типов для настраиваемого стартового инвентаря.
    global START_ITEM_REGISTRY

    global laser_pistol
    global underwater_rifle
    global plasma_cannon
    global lang_cannon
    global schweer_cannon
    global diamond_cutter
    global flamethrower
    global golden_pistol

    global recipes
    global biomes
    global flora_types
    global surface_flora_profiles
    global cave_flora_profiles

    rock_type = ObjectType("Камень", (100, 100, 100), 20, "rect")
    titan_type = ObjectType("Титан", (205, 224, 216), 35, "rect")
    copper_type = ObjectType("Медная руда", (211, 127, 34), 19, "rect")

    seaweed_type = ObjectType(
        "Водоросль", (0, 200, 0), 18, "circle",
        edible=True, hunger_value=5, thirst_value=5
    )

    iron_type = ObjectType("Железная руда", (169, 169, 169), 25, "rect")
    gold_type = ObjectType("Золотая руда", (255, 215, 0), 30, "rect")
    diamond_type = ObjectType("Алмаз", (0, 255, 255), 40, "rect")
    quartz_type = ObjectType("Кварц", (255, 255, 255), 15, "rect")
    coal_type = ObjectType("Уголь", (50, 50, 50), 22, "rect")
    sulfur_type = ObjectType("Сера", (255, 255, 0), 18, "rect")
    clay_type = ObjectType("Глина", (139, 69, 19), 12, "rect")
    sand_type = ObjectType("Песок", (194, 178, 128), 10, "rect")
    limestone_type = ObjectType("Известняк", (200, 200, 200), 16, "rect")
    oil_type = ObjectType("Нефть", (30, 30, 30), 20, "rect")

    salt_type = ObjectType("Соль", (225, 235, 245), 14, "rect")
    silver_type = ObjectType(
        "Серебряная руда", (195, 205, 215), 18, "rect"
    )
    lead_type = ObjectType("Свинец", (80, 90, 105), 20, "rect")
    lithium_type = ObjectType("Литий", (220, 210, 235), 17, "rect")
    magnetite_type = ObjectType("Магнетит", (65, 65, 78), 20, "rect")
    uraninite_type = ObjectType("Уранинит", (110, 190, 45), 22, "rect")
    ruby_type = ObjectType("Рубин", (230, 40, 65), 21, "rect")
    gel_sack_type = ObjectType(
        "Гелевый мешок", (155, 70, 190), 18, "circle"
    )

    steel_type = ObjectType("Сталь", (180, 180, 200), 18, "rect")
    provod_type = ObjectType("Медный провод", (211, 127, 34), 12, "circle")
    glass_type = ObjectType("Стекло", (200, 230, 255), 14, "rect")
    gunpowder_type = ObjectType("Порох", (60, 60, 60), 12, "circle")
    fuel_type = ObjectType("Топливо", (90, 60, 20), 16, "rect")
    concrete_type = ObjectType("Бетон", (170, 170, 160), 20, "rect")

    # Процедурная графика для переработанных ресурсов: они больше не
    # отображаются простыми квадратами ни в мире, ни в инвентаре.
    steel_type.image = generate_tech_item_sprite(
        "Сталь", steel_type.size, steel_type.color
    )
    provod_type.image = generate_tech_item_sprite(
        "Медный провод", provod_type.size, provod_type.color
    )
    glass_type.image = generate_crystal_sprite(
        glass_type.size, (190, 225, 245), sparkle=True, seed=214
    )
    gunpowder_type.image = generate_lumpy_sprite(
        gunpowder_type.size, (65, 65, 68), seed=215
    )
    fuel_type.image = generate_tech_item_sprite(
        "Топливо", fuel_type.size, fuel_type.color
    )
    concrete_type.image = generate_rock_sprite(
        concrete_type.size, (170, 170, 160), seed=216
    )

    # Канонические собираемые материалы Subnautica, которых раньше не было.
    metal_salvage_type = ObjectType("Металлолом", (125, 135, 145), 24, "rect")
    acid_mushroom_item = ObjectType("Кислотный гриб", (145, 80, 205), 15, "circle")
    creepvine_sample_type = ObjectType("Образец водоросли", (55, 165, 70), 18, "circle")
    creepvine_seed_type = ObjectType("Гроздь семян водоросли", (235, 185, 40), 17, "circle")
    cave_sulfur_type = ObjectType("Пещерная сера", (245, 220, 65), 16, "circle")
    table_coral_type = ObjectType("Образец пластинчатого коралла", (220, 85, 105), 17, "rect")
    coral_tube_type = ObjectType("Образец коралловой трубы", (185, 115, 85), 17, "rect")
    stalker_tooth_type = ObjectType("Зуб сталкера", (235, 235, 220), 14, "rect")
    blood_oil_type = ObjectType("Масляный сок", (165, 35, 45), 19, "circle")
    deep_shroom_item = ObjectType("Глубинный гриб", (70, 62, 105), 16, "circle")
    nickel_type = ObjectType("Никелевая руда", (125, 160, 150), 20, "rect")
    kyanite_type = ObjectType("Кианит", (70, 125, 245), 22, "rect")
    ion_cube_type = ObjectType("Ионный куб", (65, 245, 150), 22, "rect")
    gas_pod_type = ObjectType("Газовый пузырь", (190, 210, 65), 18, "circle")

    rock_type.image = generate_rock_sprite(
        20, (115, 115, 120), seed=101
    )
    titan_type.image = generate_rock_sprite(
        35, (205, 222, 218), seed=102
    )
    copper_type.image = generate_ore_sprite(
        19,
        (95, 95, 100),
        [(211, 127, 34), (240, 160, 60), (170, 95, 20)],
        vein_count=4, seed=103
    )
    seaweed_type.image = generate_seaweed_sprite(18, seed=104)
    iron_type.image = generate_ore_sprite(
        25,
        (115, 115, 120),
        [(190, 190, 195), (140, 140, 145), (235, 235, 240)],
        vein_count=5, seed=105
    )
    gold_type.image = generate_ore_sprite(
        30,
        (95, 85, 70),
        [(255, 215, 0), (255, 235, 120), (220, 180, 0)],
        vein_count=6, seed=106
    )
    diamond_type.image = generate_crystal_sprite(
        40, (0, 240, 255), sparkle=True, seed=107
    )
    quartz_type.image = generate_crystal_sprite(
        15, (225, 240, 255), sparkle=False, seed=108
    )
    coal_type.image = generate_rock_sprite(
        22, (45, 45, 50), seed=109
    )
    sulfur_type.image = generate_ore_sprite(
        18,
        (105, 95, 70),
        [(255, 255, 0), (255, 240, 80), (220, 220, 40)],
        vein_count=4, seed=110
    )
    clay_type.image = generate_lumpy_sprite(
        12, (139, 69, 19), seed=111
    )
    sand_type.image = generate_lumpy_sprite(
        10, (194, 178, 128), seed=112
    )
    limestone_type.image = generate_rock_sprite(
        16, (215, 215, 205), seed=113
    )
    oil_type.image = generate_lumpy_sprite(
        20, (28, 28, 32), seed=114, shine=True
    )

    salt_type.image = generate_crystal_sprite(
        14, (225, 240, 255), sparkle=False, seed=201
    )
    silver_type.image = generate_ore_sprite(
        18, (95, 100, 110),
        [(205, 215, 225), (170, 180, 195)],
        vein_count=4, seed=202
    )
    lead_type.image = generate_ore_sprite(
        20, (70, 75, 82),
        [(105, 115, 130), (65, 70, 85)],
        vein_count=4, seed=203
    )
    lithium_type.image = generate_crystal_sprite(
        17, (225, 215, 240), sparkle=True, seed=204
    )
    magnetite_type.image = generate_crystal_sprite(
        20, (65, 65, 80), sparkle=True, seed=205
    )
    uraninite_type.image = generate_crystal_sprite(
        22, (105, 190, 45), sparkle=True, seed=206
    )
    ruby_type.image = generate_crystal_sprite(
        21, (235, 40, 65), sparkle=True, seed=207
    )
    gel_sack_type.image = generate_lumpy_sprite(
        18, (145, 65, 180), seed=208, shine=True
    )
    metal_salvage_type.image = generate_rock_sprite(24, (125, 135, 145), seed=220)
    acid_mushroom_item.image = generate_lumpy_sprite(15, (145, 80, 205), seed=221, shine=True)
    creepvine_sample_type.image = generate_seaweed_sprite(18, seed=222)
    creepvine_seed_type.image = generate_lumpy_sprite(17, (235, 185, 40), seed=223, shine=True)
    cave_sulfur_type.image = generate_crystal_sprite(16, (245, 220, 65), seed=224)
    table_coral_type.image = generate_lumpy_sprite(17, (220, 85, 105), seed=225)
    coral_tube_type.image = generate_lumpy_sprite(17, (185, 115, 85), seed=226)
    stalker_tooth_type.image = generate_crystal_sprite(14, (235, 235, 220), seed=227)
    blood_oil_type.image = generate_lumpy_sprite(19, (165, 35, 45), seed=228, shine=True)
    deep_shroom_item.image = generate_lumpy_sprite(16, (70, 62, 105), seed=229, shine=True)
    nickel_type.image = generate_ore_sprite(20, (90, 105, 102), [(125, 175, 160)], seed=230)
    kyanite_type.image = generate_crystal_sprite(22, (70, 125, 245), seed=231)
    ion_cube_type.image = generate_crystal_sprite(22, (65, 245, 150), seed=232)
    gas_pod_type.image = generate_lumpy_sprite(18, (190, 210, 65), seed=233, shine=True)

    # Собираемые растения также светятся в мире (не только декоративная флора).
    for glowing_item in (
            seaweed_type, gel_sack_type, acid_mushroom_item,
            creepvine_sample_type, creepvine_seed_type, blood_oil_type,
            deep_shroom_item, table_coral_type, coral_tube_type):
        glowing_item.glow_image = generate_bioluminescence_sprite(
            glowing_item.image, glowing_item.name, is_plant=True
        )


    # -----------------------------------------------------
    # ФЛОРА — КАНОНИЧЕСКИЕ ВИДЫ ДЛЯ БИОМОВ ЭТОЙ КАРТЫ
    # -----------------------------------------------------
    # Отдельный декоративный слой: не занимает инвентарь и не участвует
    # в четырёхдневном респавне ресурсов. Уже существующие собираемые
    # seaweed_type и gel_sack_type остаются ресурсами как и раньше.
    flora_types = {
        'acid_mushroom': FloraType('Acid Mushroom', 'acid_mushroom', 22, 3001),
        'deep_shroom': FloraType('Deep Shroom', 'deep_shroom', 20, 3002),
        'creepvine': FloraType('Creepvine', 'creepvine', 68, 3003),
        'blood_grass': FloraType('Blood Grass', 'blood_grass', 24, 3004),
        'blue_palm': FloraType('Blue Palm', 'blue_palm', 38, 3005),
        'writhing_weed': FloraType('Writhing Weed', 'writhing_weed', 28, 3006),
        'spotted_reeds': FloraType('Spotted Reeds', 'spotted_reeds', 28, 3007),
        'redwort': FloraType('Redwort', 'redwort', 22, 3008),
        'violet_beau': FloraType('Violet Beau', 'violet_beau', 24, 3009),
        'tiger_plant': FloraType('Tiger Plant', 'tiger_plant', 28, 3010),
        'spiked_horn_grass': FloraType('Spiked Horn Grass', 'spiked_horn_grass', 26, 3011),
        'mushroom_tree': FloraType('Mushroom Tree', 'mushroom_tree', 76, 3012),
        'jellyshroom': FloraType('Jellyshroom', 'jellyshroom', 66, 3013),
        'pygmy_fan': FloraType('Pygmy Fan', 'pygmy_fan', 28, 3014),
        'bulb_bush': FloraType('Bulb Bush', 'bulb_bush', 48, 3015),
        'spotted_dockleaf': FloraType('Spotted Dockleaf', 'spotted_dockleaf', 28, 3016),
        'bloodvine': FloraType('Bloodvine', 'bloodvine', 62, 3017),
        'bloodroot': FloraType('Bloodroot', 'bloodroot', 68, 3018),
        'ghost_weed': FloraType('Ghost Weed', 'ghost_weed', 36, 3019),
        'gabe_feather': FloraType("Gabe's Feather", 'gabe_feather', 30, 3020),
        'membraintree': FloraType('Membrain Tree', 'membraintree', 42, 3021),
        'anchor_pod': FloraType('Anchor Pod', 'anchor_pod', 58, 3022),
        'cave_bush': FloraType('Cave Bush', 'cave_bush', 30, 3023),
        'rouge_cradle': FloraType('Rouge Cradle', 'rouge_cradle', 30, 3024),
        'drooping_stinger': FloraType('Drooping Stinger', 'drooping_stinger', 40, 3025),
        'sulfur_plant': FloraType('Sulfur Plant', 'sulfur_plant', 26, 3026),
        'sea_crown': FloraType('Sea Crown', 'sea_crown', 30, 3027),
        'regress_shell': FloraType('Regress Shell', 'regress_shell', 26, 3028),
        'eye_stalk': FloraType('Eye Stalk', 'eye_stalk', 32, 3029),
        'furled_papyrus': FloraType('Furled Papyrus', 'furled_papyrus', 28, 3030),
    }

    # -----------------------------------------------------
    # ЖИВОТНЫЕ — ТОЛЬКО КАНОНИЧЕСКАЯ ФАУНА SUBNAUTICA
    # -----------------------------------------------------

    # Небольшие съедобные рыбы. schooling=True означает, что при генерации
    # они образуют более плотные естественные популяции, но движение и
    # отрисовка по-прежнему используют пространственный индекс.
    peeper_type = AnimalType(
        "Peeper", (55, 170, 205), 12,
        speed=0.09, behavior="prey", hp=5,
        edible=True, hunger_value=30, thirst_value=5,
        fish_length=38, fish_width=12,
        sprite_kind='peeper', schooling=True,
        fear_distance=3.0, zigzag_strength=0.28,
        speed_variation=0.25, flee_speed_boost=2.15
    )

    bladderfish_type = AnimalType(
        "Bladderfish", (235, 100, 190), 11,
        speed=0.065, behavior="prey", hp=4,
        edible=True, hunger_value=12, thirst_value=20,
        fish_length=34, fish_width=13,
        sprite_kind='bladderfish', schooling=True,
        fear_distance=2.3, zigzag_strength=0.11,
        speed_variation=0.1, flee_speed_boost=1.55
    )

    boomerang_type = AnimalType(
        "Boomerang", (85, 95, 215), 11,
        speed=0.085, behavior="prey", hp=5,
        edible=True, hunger_value=21, thirst_value=3,
        fish_length=37, fish_width=12,
        sprite_kind='boomerang', schooling=True,
        fear_distance=3.4, zigzag_strength=0.43,
        speed_variation=0.24, flee_speed_boost=1.9
    )

    garryfish_type = AnimalType(
        "Garryfish", (75, 145, 95), 11,
        speed=0.07, behavior="prey", hp=5,
        edible=True, hunger_value=18, thirst_value=4,
        fish_length=38, fish_width=11,
        sprite_kind='garryfish', schooling=True,
        fear_distance=2.7, zigzag_strength=0.3,
        speed_variation=0.29, flee_speed_boost=1.7
    )

    holefish_type = AnimalType(
        "Holefish", (70, 115, 180), 11,
        speed=0.075, behavior="prey", hp=5,
        edible=True, hunger_value=16, thirst_value=4,
        fish_length=36, fish_width=12,
        sprite_kind='holefish', schooling=True,
        fear_distance=2.6, zigzag_strength=0.19,
        speed_variation=0.15, flee_speed_boost=1.8
    )

    hoverfish_type = AnimalType(
        "Hoverfish", (80, 180, 105), 10,
        speed=0.075, behavior="prey", hp=4,
        edible=True, hunger_value=16, thirst_value=4,
        fish_length=35, fish_width=10,
        sprite_kind='hoverfish', schooling=True,
        fear_distance=2.0, zigzag_strength=0.1,
        speed_variation=0.12, flee_speed_boost=1.65
    )

    hoopfish_type = AnimalType(
        "Hoopfish", (190, 205, 215), 10,
        speed=0.08, behavior="prey", hp=5,
        edible=True, hunger_value=17, thirst_value=4,
        fish_length=37, fish_width=10,
        sprite_kind='hoopfish', schooling=True,
        fear_distance=3.2, zigzag_strength=0.38,
        speed_variation=0.2, flee_speed_boost=1.9
    )

    reginald_type = AnimalType(
        "Reginald", (75, 105, 78), 13,
        speed=0.07, behavior="prey", hp=8,
        edible=True, hunger_value=44, thirst_value=4,
        fish_length=45, fish_width=13,
        sprite_kind='reginald', schooling=True,
        fear_distance=2.8, zigzag_strength=0.17,
        speed_variation=0.17, flee_speed_boost=1.8
    )

    spadefish_type = AnimalType(
        "Spadefish", (90, 130, 75), 10,
        speed=0.055, behavior="prey", hp=10,
        edible=True, hunger_value=23, thirst_value=3,
        fish_length=29, fish_width=11,
        sprite_kind='spadefish', schooling=True,
        fear_distance=2.2, zigzag_strength=0.12,
        speed_variation=0.1, flee_speed_boost=1.55
    )

    eyeye_type = AnimalType(
        "Eyeye", (70, 145, 90), 11,
        speed=0.07, behavior="prey", hp=5,
        edible=True, hunger_value=18, thirst_value=4,
        fish_length=34, fish_width=13,
        sprite_kind='eyeye', schooling=True,
        fear_distance=2.8, zigzag_strength=0.26,
        speed_variation=0.2, flee_speed_boost=1.85
    )

    oculus_type = AnimalType(
        "Oculus", (125, 70, 190), 12,
        speed=0.075, behavior="prey", hp=6,
        edible=True, hunger_value=30, thirst_value=2,
        fish_length=35, fish_width=14,
        sprite_kind='oculus', schooling=True,
        fear_distance=2.9, zigzag_strength=0.29,
        speed_variation=0.17, flee_speed_boost=1.9
    )

    spinefish_type = AnimalType(
        "Spinefish", (65, 100, 135), 11,
        speed=0.075, behavior="prey", hp=5,
        edible=True, hunger_value=20, thirst_value=3,
        fish_length=38, fish_width=10,
        sprite_kind='spinefish', schooling=True,
        fear_distance=3.1, zigzag_strength=0.35,
        speed_variation=0.2, flee_speed_boost=2.0
    )

    # Мирные крупные существа.
    rabbit_ray_type = AnimalType(
        "Rabbit Ray", (75, 115, 195), 24,
        speed=0.045, behavior="neutral", hp=18,
        edible=False,
        fish_length=62, fish_width=28,
        sprite_kind='rabbit_ray'
    )

    jellyray_type = AnimalType(
        "Jellyray", (120, 175, 245), 32,
        speed=0.035, behavior="neutral", hp=35,
        edible=False,
        fish_length=78, fish_width=32,
        sprite_kind='jellyray'
    )

    gasopod_type = AnimalType(
        "Gasopod", (100, 120, 100), 46,
        speed=0.025, behavior="neutral", hp=55,
        edible=False,
        fish_length=92, fish_width=40,
        sprite_kind='gasopod'
    )

    reefback_type = AnimalType(
        "Reefback Leviathan", (45, 75, 85), 240,
        speed=0.012, behavior="neutral", hp=500,
        edible=False,
        fish_length=380, fish_width=136,
        sprite_kind='reefback'
    )

    sea_treader_type = AnimalType(
        "Sea Treader Leviathan", (78, 80, 72), 95,
        speed=0.018, behavior="neutral", hp=350,
        edible=False,
        fish_length=135, fish_width=76,
        sprite_kind='sea_treader'
    )

    # Хищники и опасная фауна.
    biter_type = AnimalType(
        "Biter", (190, 55, 45), 12,
        speed=0.11, behavior="predator", hp=8,
        damage=2, edible=False,
        fish_length=34, fish_width=13,
        sprite_kind='biter'
    )

    blighter_type = AnimalType(
        "Blighter", (105, 40, 95), 13,
        speed=0.12, behavior="predator", hp=10,
        damage=3, edible=False,
        fish_length=36, fish_width=14,
        sprite_kind='blighter'
    )

    crashfish_type = AnimalType(
        "Crashfish", (225, 80, 45), 15,
        speed=0.14, behavior="predator", hp=6,
        damage=6, edible=False,
        fish_length=38, fish_width=20,
        sprite_kind='crashfish'
    )

    stalker_type = AnimalType(
        "Stalker", (55, 120, 78), 55,
        speed=0.095, behavior="predator", hp=45,
        damage=5, edible=False,
        fish_length=118, fish_width=24,
        sprite_kind='stalker'
    )

    sand_shark_type = AnimalType(
        "Sand Shark", (135, 105, 75), 58,
        speed=0.10, behavior="predator", hp=55,
        damage=7, edible=False,
        fish_length=112, fish_width=30,
        sprite_kind='sand_shark'
    )

    boneshark_type = AnimalType(
        "Boneshark", (95, 92, 88), 62,
        speed=0.105, behavior="predator", hp=70,
        damage=8, edible=False,
        fish_length=120, fish_width=31,
        sprite_kind='boneshark'
    )

    ampeel_type = AnimalType(
        "Ampeel", (55, 175, 165), 58,
        speed=0.085, behavior="predator", hp=85,
        damage=9, edible=False,
        fish_length=135, fish_width=22,
        sprite_kind='ampeel'
    )

    mesmer_type = AnimalType(
        "Mesmer", (55, 160, 180), 26,
        speed=0.065, behavior="predator", hp=28,
        damage=4, edible=False,
        fish_length=62, fish_width=30,
        sprite_kind='mesmer'
    )

    crabsquid_type = AnimalType(
        "Crabsquid", (100, 60, 135), 72,
        speed=0.055, behavior="predator", hp=105,
        damage=10, edible=False,
        fish_length=118, fish_width=52,
        sprite_kind='crabsquid'
    )

    crabsnake_type = AnimalType(
        "Crabsnake", (145, 65, 160), 52,
        speed=0.09, behavior="predator", hp=70,
        damage=8, edible=False,
        fish_length=130, fish_width=20,
        sprite_kind='crabsnake'
    )

    warper_type = AnimalType(
        "Warper", (95, 60, 150), 58,
        speed=0.075, behavior="predator", hp=110,
        damage=12, edible=False,
        fish_length=82, fish_width=56,
        sprite_kind='warper'
    )

    reaper_type = AnimalType(
        "Reaper Leviathan", (225, 220, 205), 180,
        speed=0.075, behavior="predator", hp=420,
        damage=20, edible=False,
        fish_length=230, fish_width=52,
        sprite_kind='reaper'
    )

    sea_dragon_type = AnimalType(
        "Sea Dragon Leviathan", (60, 120, 75), 240,
        speed=0.065, behavior="predator", hp=800,
        damage=30, edible=False,
        fish_length=300, fish_width=35,
        sprite_kind='sea_dragon'
    )

    ghost_leviathan_type = AnimalType(
        "Ghost Leviathan", (90, 190, 255), 250,
        speed=0.065, behavior="predator", hp=450,
        damage=18, edible=False,
        leviathan_style=True,
        leviathan_length=280, leviathan_width=44
    )

    # -----------------------------------------------------
    # КАНОНИЧЕСКИЕ ПРЕДМЕТЫ / ПОСТРОЙКИ SUBNAUTICA
    # -----------------------------------------------------
    # Старые экспериментальные пушки ниже сохранены как лут обломков,
    # но из основной ветки крафта убраны.

    def tech(name, color=(90, 155, 185), size=20, weapon=False,
             damage=0, weapon_range=0, weapon_type=""):
        obj = ObjectType(name, color, size, "rect", is_weapon=weapon,
                         damage=damage, weapon_range=weapon_range,
                         weapon_type=weapon_type)
        obj.image = generate_tech_item_sprite(
            name, size, color, is_weapon=weapon, weapon_type=weapon_type
        )
        return obj

    def buildable(name, color=(105, 145, 155), wall=False, size=30):
        obj = ObjectType(name, color, size, "rect",
                         is_buildable=True, is_wall=wall)
        obj.image = generate_building_sprite(name, size, color, wall=wall)
        obj.requires_habitat_builder = True
        return obj

    # Материалы Fabricator.
    titanium_ingot = tech("Титановый слиток", (185, 205, 205))
    fiber_mesh = tech("Сетчатое волокно", (120, 170, 110))
    silicone_rubber = tech("Силиконовая резина", (170, 185, 175))
    bleach_type = tech("Антисептик", (225, 235, 220))
    lubricant_type = tech("Смазка", (205, 180, 55))
    enameled_glass = tech("Эмалевое стекло", (180, 230, 245))
    plasteel_ingot = tech("Пласталевый слиток", (150, 175, 190))
    hydrochloric_acid = tech("Соляная кислота", (125, 220, 145))
    polyaniline_type = tech("Полианилин", (95, 120, 200))
    synthetic_fibers = tech("Синтетические волокна", (165, 150, 190))
    aerogel_type = tech("Аэрогель", (130, 220, 235))
    benzene_type = tech("Бензол", (185, 80, 115))
    copper_wire = tech("Медный провод", (205, 120, 40))
    wiring_kit = tech("Комплект проводов", (180, 190, 205))
    advanced_wiring_kit = tech("Расширенный комплект проводов", (205, 170, 80))
    battery_type = tech("Батарея", (235, 210, 70))
    power_cell_type = tech("Энергоячейка", (80, 190, 225), 22)
    computer_chip = tech("Микросхема", (80, 185, 125))
    reactor_rod = tech("Топливный стержень реактора", (135, 215, 75), 22)
    ion_battery = tech("Ионная батарея", (80, 245, 150))
    ion_power_cell = tech("Ионная энергоячейка", (80, 245, 180), 22)

    # Личные инструменты и экипировка.
    fins_type = tech("Ласты", (90, 170, 190))
    standard_tank = tech("Обычный кислородный баллон", (175, 185, 195), 24)
    high_capacity_tank = tech("Кислородный баллон высокой ёмкости", (120, 170, 205), 24)
    lightweight_tank = tech("Лёгкий баллон высокой ёмкости", (115, 195, 205), 24)
    ultra_tank = tech("Баллон сверхвысокой ёмкости", (100, 150, 220), 24)
    rebreather_type = tech("Ребризер", (65, 115, 145))
    radiation_suit = tech("Противорадиационный костюм", (220, 170, 65), 24)
    reinforced_suit = tech("Укреплённый костюм ныряльщика", (70, 85, 100), 24)
    water_filtration_suit = tech("Фильтрационный костюм", (80, 140, 165), 24)
    compass_type = tech("Компас", (110, 185, 205))
    first_aid_kit = tech("Аптечка", (225, 230, 230))
    fire_extinguisher = tech("Огнетушитель", (220, 70, 50), 22)
    floating_air_pump = tech("Плавучий воздушный насос", (120, 180, 205))
    pipe_type = tech("Труба", (185, 195, 205))

    survival_knife = tech("Нож", (165, 175, 185), weapon=True,
                          damage=10, weapon_range=1.7, weapon_type="нож")
    thermoblade = tech("Термоклинок", (245, 120, 50), weapon=True,
                       damage=20, weapon_range=1.7, weapon_type="нож")
    scanner_type = tech("Сканер", (80, 175, 215))
    repair_tool = tech("Ремонтный инструмент", (85, 165, 205))
    repair_kit = tech("Ремкомплект", (235, 155, 70), 22)
    flashlight_type = tech("Фонарик", (220, 220, 180))
    habitat_builder_type = tech("Строитель", (95, 190, 205))
    air_bladder = tech("Воздушный пузырь", (230, 175, 70))
    pathfinder_tool = tech("Инструмент исследователя", (100, 205, 175))
    propulsion_cannon = tech("Пропульсионная пушка", (110, 145, 205), 24,
                             True, 4, 7, "импульс")
    repulsion_cannon = tech("Репульсионная пушка", (150, 110, 210), 24,
                            True, 8, 8, "импульс")
    stasis_rifle = tech("Стазис-винтовка", (75, 145, 220), 28,
                        True, 1, 9, "стазис")
    laser_cutter = tech("Лазерный резак", (225, 110, 70), 24,
                        True, 8, 2.5, "лазер")
    flare_type = tech("Сигнальная ракета", (245, 90, 70))

    # Размещаемые устройства и транспорт.
    beacon_type = buildable("Радиомаяк", (235, 185, 65), size=24)
    creature_decoy = tech("Приманка для существ", (190, 110, 85))
    seaglide_type = tech("Морской глайдер", (70, 150, 190), 28)
    mobile_vehicle_bay = buildable("Переносной сборщик транспорта", (95, 150, 175), size=34)
    grav_trap = buildable("Грави-ловушка", (115, 120, 205), size=26)
    waterproof_locker = buildable("Водостойкий контейнер", (150, 165, 170), size=26)

    seamoth_type = buildable("Мотылёк", (220, 180, 70), size=42)
    prawn_suit_type = buildable("Костюм КРАБ", (205, 115, 65), size=44)
    cyclops_type = buildable("Циклоп", (85, 130, 155), size=58)

    # Детальная графика из малого файла: сохраняем вытянутые пропорции,
    # а не втискиваем подлодки в квадратный строительный спрайт.
    seamoth_type.image = generate_detailed_seamoth_vehicle_sprite(86)
    cyclops_type.image = generate_detailed_cyclops_vehicle_sprite(180)
    neptune_platform = buildable("Пусковая платформа «Нептуна»", (120, 135, 145), size=48)
    neptune_gantry = buildable("Башня подъёмника «Нептуна»", (135, 140, 150), size=48)
    neptune_boosters = buildable("Ускорители «Нептуна»", (180, 115, 65), size=48)
    neptune_fuel = buildable("Топливные баки «Нептуна»", (165, 95, 70), size=48)
    neptune_cockpit = buildable("Кабина «Нептуна»", (95, 155, 180), size=48)

    for _deployable in (beacon_type, mobile_vehicle_bay, grav_trap,
                        waterproof_locker, seamoth_type, prawn_suit_type,
                        cyclops_type, neptune_platform, neptune_gantry,
                        neptune_boosters, neptune_fuel, neptune_cockpit):
        _deployable.requires_habitat_builder = False

    # Артефакты Предтеч.
    purple_tablet = tech("Фиолетовая скрижаль", (165, 90, 220))
    orange_tablet = tech("Оранжевая скрижаль", (235, 145, 55))
    blue_tablet = tech("Синяя скрижаль", (70, 145, 235))

    # 18 основных частей базы.
    multipurpose_room = buildable("Многоцелевая комната", (95, 145, 160), size=38)
    hatch_type = buildable("Люк", (130, 165, 175))
    window_type = buildable("Окно", (125, 195, 215))
    foundation_type = buildable("Фундамент", (115, 125, 130), size=36)
    i_compartment = buildable("Прямой отсек", (100, 145, 155), size=34)
    l_compartment = buildable("Угловой отсек", (100, 145, 155), size=34)
    t_compartment = buildable("T-образный отсек", (100, 145, 155), size=34)
    x_compartment = buildable("Крестообразный отсек", (100, 145, 155), size=34)
    reinforcement_type = buildable("Усиление корпуса", (95, 105, 115), wall=True)
    glass_i_compartment = buildable("Прямой стеклянный отсек", (130, 205, 225), size=34)
    glass_l_compartment = buildable("Угловой стеклянный отсек", (130, 205, 225), size=34)
    observatory_type = buildable("Обсерватория", (120, 205, 225), size=38)
    vertical_connector = buildable("Вертикальный соединитель", (105, 150, 160), size=32)
    moonpool_type = buildable("Стыковочная шахта", (75, 135, 160), size=42)
    scanner_room_type = buildable("Комната сканирования", (85, 155, 170), size=40)
    large_room_type = buildable("Большая комната", (90, 135, 150), size=46)
    multipurpose_dome = buildable("Стеклянный купол многоцелевой комнаты", (145, 215, 230), size=38)
    large_room_dome = buildable("Стеклянный купол большой комнаты", (145, 215, 230), size=44)

    # Внешние модули.
    spotlight_type = buildable("Прожектор", (235, 230, 160), size=25)
    solar_panel_type = buildable("Солнечная панель", (65, 110, 180), size=30)
    power_transmitter = buildable("Энергопередатчик", (110, 175, 195), size=24)
    thermal_plant = buildable("Теплоэлектростанция", (180, 105, 70), size=30)
    exterior_growbed = buildable("Наружная грядка", (105, 125, 80), size=32)
    floodlight_type = buildable("Осветительная мачта", (230, 225, 170), size=26)
    base_air_pump = buildable("Стационарный воздушный насос", (120, 175, 195), size=26)

    # Внутренние элементы и модули.
    ladder_type = buildable("Лестница", (150, 155, 160), size=25)
    bulkhead_type = buildable("Переборка", (125, 135, 140), wall=True)
    vehicle_upgrade_console = buildable("Консоль улучшения транспорта", (75, 145, 185), size=28)
    water_filtration_machine = buildable("Водоочистная станция", (110, 165, 185), size=30)
    alien_containment = buildable("Большой аквариум", (100, 175, 195), size=34)
    bioreactor = buildable("Биореактор", (100, 165, 95), size=32)
    nuclear_reactor = buildable("Ядерный реактор", (145, 165, 80), size=34)
    large_partition_door = buildable("Дверь переборки большой комнаты", (125, 135, 145), wall=True)
    large_partition = buildable("Переборка большой комнаты", (115, 125, 135), wall=True)
    modification_station = buildable("Модификационная станция", (100, 150, 195), size=30)
    fabricator_type = buildable("Изготовитель", (95, 165, 190), size=28)
    aquarium_type = buildable("Аквариум", (95, 175, 200), size=28)
    locker_type = buildable("Шкаф", (125, 145, 155), size=28)
    wall_locker = buildable("Настенный шкаф", (135, 150, 160), wall=True, size=26)
    plant_pot = buildable("Горшок для растений", (130, 100, 75), size=24)
    indoor_growbed = buildable("Внутренняя грядка", (120, 105, 75), size=30)
    plant_shelf = buildable("Стеллаж для растений", (130, 115, 85), size=26)
    radio_type = buildable("Радио", (95, 135, 170), size=24)
    composite_pot = buildable("Композитный горшок", (115, 95, 80), size=24)
    chic_pot = buildable("Роскошный горшок", (145, 115, 95), size=24)
    medical_fabricator = buildable("Изготовитель аптечек", (210, 220, 220), size=26)
    battery_charger = buildable("Зарядное устройство батарей", (100, 160, 185), size=28)
    power_cell_charger = buildable("Зарядное устройство энергоячеек", (90, 150, 180), size=30)
    centrifuge = buildable("Центрифуга", (120, 150, 165), size=28)

    # Мебель, которая строится Habitat Builder в оригинале.
    bench_type = buildable("Скамья", (130, 115, 100), size=28)
    picture_frame = buildable("Фоторамка", (100, 110, 120), wall=True, size=22)
    wall_shelf = buildable("Настенная полка", (120, 120, 125), wall=True, size=24)
    bed_type = buildable("Кровать", (145, 125, 115), size=30)
    desk_type = buildable("Рабочий стол", (115, 120, 125), size=30)
    chair_type = buildable("Офисный стул", (95, 100, 105), size=24)
    vending_machine = buildable("Торговый автомат", (130, 145, 155), size=28)
    coffee_machine = buildable("Кофейный торговый автомат", (120, 105, 95), size=26)
    trash_can = buildable("Урна", (100, 110, 115), size=24)
    nuclear_waste = buildable("Утилизатор ядерных отходов", (145, 155, 75), size=26)

    # Апгрейды транспорта / комнаты сканирования / Циклопа.
    seamoth_depth1 = tech("Модуль глубины «Мотылька» – Мод. 1")
    seamoth_depth2 = tech("Модуль глубины «Мотылька» – Мод. 2")
    seamoth_depth3 = tech("Модуль глубины «Мотылька» – Мод. 3")
    seamoth_solar = tech("Солнечная зарядка «Мотылька»")
    vehicle_storage = tech("Модуль хранилища")
    seamoth_perimeter = tech("Система периметральной защиты «Мотылька»")
    hull_reinforcement = tech("Усиление корпуса транспорта")
    seamoth_torpedo = tech("Торпедная установка «Мотылька»")
    seamoth_sonar = tech("Гидролокатор «Мотылька»")
    vortex_torpedo = tech("Вихревая торпеда")
    gas_torpedo = tech("Газовая торпеда")
    vehicle_engine_eff = tech("Модуль эффективности двигателя")
    prawn_depth1 = tech("Модуль глубины костюма КРАБ – Мод. 1")
    prawn_depth2 = tech("Модуль глубины костюма КРАБ – Мод. 2")
    prawn_jet = tech("Улучшение реактивного ранца костюма КРАБ")
    prawn_drill = tech("Бур костюма КРАБ")
    prawn_thermal = tech("Тепловой реактор костюма КРАБ")
    prawn_propulsion = tech("Пропульсионная пушка костюма КРАБ")
    prawn_grapple = tech("Рука-захват костюма КРАБ")
    prawn_torpedo = tech("Торпедная установка костюма КРАБ")
    scanner_hud = tech("Чип интерфейса комнаты сканирования")
    scanner_range = tech("Улучшение дальности сканирования")
    scanner_speed = tech("Улучшение скорости сканирования")
    camera_drone = tech("Дрон-камера")
    cyclops_engine_eff = tech("Модуль эффективности двигателя «Циклопа»")
    cyclops_depth1 = tech("Модуль глубины «Циклопа» – Мод. 1")
    cyclops_depth2 = tech("Модуль глубины «Циклопа» – Мод. 2")
    cyclops_depth3 = tech("Модуль глубины «Циклопа» – Мод. 3")
    cyclops_shield = tech("Генератор щита «Циклопа»")
    cyclops_sonar = tech("Гидролокатор «Циклопа»")
    cyclops_repair = tech("Ремонтный модуль стыковочного отсека «Циклопа»")
    cyclops_decoy = tech("Улучшение камеры приманок «Циклопа»")
    cyclops_fire = tech("Система пожаротушения «Циклопа»")
    cyclops_thermal = tech("Модуль теплового реактора «Циклопа»")

    # Старые две простые постройки остаются совместимыми со старыми сохранениями.
    wall_type = ObjectType("Стена", (150, 75, 0), 30, "rect",
                           is_buildable=True, is_wall=True)
    wall_type.image = generate_building_sprite("Стена", 30, (150, 75, 0), wall=True)
    floor_type = ObjectType("Пол", (100, 150, 100), 30, "rect",
                            is_buildable=True, is_wall=False)
    floor_type.image = generate_building_sprite("Пол", 30, (100, 150, 100), wall=False)

    # НЕКАНОНИЧНОЕ оружие из предыдущей версии сохраняется только как лут обломков.
    laser_pistol = ObjectType("Лазерный пистолет", (255, 50, 50), 22, "rect",
                              is_weapon=True, damage=8, weapon_range=5, weapon_type="лазер")
    laser_pistol.image = generate_weapon_sprite(14, (255, 50, 50), (120, 0, 0))
    underwater_rifle = ObjectType("Подводное ружьё", (50, 150, 255), 28, "rect",
                                  is_weapon=True, damage=12, weapon_range=8, weapon_type="ружьё")
    underwater_rifle.image = generate_weapon_sprite(24, (50, 150, 255), (0, 50, 130))
    plasma_cannon = ObjectType("Плазменная пушка", (200, 50, 200), 26, "rect",
                               is_weapon=True, damage=20, weapon_range=4, weapon_type="плазма")
    plasma_cannon.image = generate_weapon_sprite(18, (200, 50, 200), (90, 0, 110))
    lang_cannon = ObjectType("Дальняя пушка", (10, 50, 200), 30, "rect",
                             is_weapon=True, damage=1, weapon_range=15, weapon_type="ружьё")
    lang_cannon.image = generate_weapon_sprite(34, (10, 50, 200), (0, 15, 90))
    schweer_cannon = ObjectType("Тяжёлая пушка", (238, 51, 32), 34, "rect",
                                is_weapon=True, damage=50, weapon_range=10, weapon_type="ружьё")
    schweer_cannon.image = generate_weapon_sprite(38, (238, 51, 32), (110, 15, 10))
    diamond_cutter = ObjectType("Алмазный резак", (150, 255, 255), 30, "rect",
                                is_weapon=True, damage=35, weapon_range=6, weapon_type="лазер")
    diamond_cutter.image = generate_weapon_sprite(22, (150, 255, 255), (0, 130, 150))
    flamethrower = ObjectType("Огнемёт", (255, 120, 20), 32, "rect",
                              is_weapon=True, damage=15, weapon_range=3, weapon_type="огонь")
    flamethrower.image = generate_weapon_sprite(30, (255, 120, 20), (120, 40, 5))
    golden_pistol = ObjectType("Золотой пистолет", (255, 215, 0), 24, "rect",
                               is_weapon=True, damage=14, weapon_range=7, weapon_type="лазер")
    golden_pistol.image = generate_weapon_sprite(16, (255, 215, 0), (140, 100, 0))

    # Объекты-станции: при установке они открывают собственную ветку крафта.
    fabricator_type.crafting_station_name = "Изготовитель"
    modification_station.crafting_station_name = "Модификационная станция"
    mobile_vehicle_bay.crafting_station_name = "Переносной сборщик транспорта"
    vehicle_upgrade_console.crafting_station_name = "Консоль улучшения транспорта"
    scanner_room_type.crafting_station_name = "Комната сканирования"
    cyclops_type.crafting_station_name = "Циклоп"

    # -----------------------------------------------------
    # КРАФТ — категории и станции соответствуют оригинальной Subnautica.
    # -----------------------------------------------------
    F = "Изготовитель"
    H = "Строитель"
    M = "Модификационная станция"
    V = "Переносной сборщик транспорта"
    U = "Консоль улучшения транспорта"
    S = "Комната сканирования"
    C = "Циклоп"

    recipes = [
        # Resources / Basic materials
        Recipe("Титан x4", {metal_salvage_type: 1}, titan_type, 4, F, "Ресурсы"),
        Recipe("Титановый слиток", {titan_type: 10}, titanium_ingot, 1, F, "Основные материалы"),
        Recipe("Сетчатое волокно", {creepvine_sample_type: 2}, fiber_mesh, 1, F, "Основные материалы"),
        Recipe("Силиконовая резина x2", {creepvine_seed_type: 1}, silicone_rubber, 2, F, "Основные материалы"),
        Recipe("Стекло", {quartz_type: 2}, glass_type, 1, F, "Основные материалы"),
        Recipe("Антисептик", {salt_type: 1, coral_tube_type: 1}, bleach_type, 1, F, "Основные материалы"),
        Recipe("Смазка", {creepvine_seed_type: 1}, lubricant_type, 1, F, "Основные материалы"),
        Recipe("Зуб сталкера", {stalker_type: 1}, stalker_tooth_type, 10, F, "Основные материалы"),
        Recipe("Эмалевое стекло", {glass_type: 1, stalker_tooth_type: 1}, enameled_glass, 1, F, "Основные материалы"),
        Recipe("Пласталевый слиток", {titanium_ingot: 1, lithium_type: 2}, plasteel_ingot, 1, F, "Основные материалы"),
        Recipe("Соляная кислота", {deep_shroom_item: 3, salt_type: 1}, hydrochloric_acid, 1, F, "Доп. материалы"),
        Recipe("Бензол", {blood_oil_type: 3}, benzene_type, 1, F, "Доп. материалы"),
        Recipe("Синтетические волокна", {benzene_type: 1, fiber_mesh: 1}, synthetic_fibers, 1, F, "Доп. материалы"),
        Recipe("Аэрогель", {ruby_type: 1, gel_sack_type: 1}, aerogel_type, 1, F, "Доп. материалы"),
        Recipe("Полианилин", {gold_type: 1, hydrochloric_acid: 1}, polyaniline_type, 1, F, "Доп. материалы"),
        Recipe("Медный провод", {copper_type: 2}, copper_wire, 1, F, "Электроника"),
        Recipe("Батарея", {acid_mushroom_item: 2, copper_type: 1}, battery_type, 1, F, "Электроника"),
        Recipe("Энергоячейка", {battery_type: 2, silicone_rubber: 1}, power_cell_type, 1, F, "Электроника"),
        Recipe("Микросхема", {table_coral_type: 2, gold_type: 1, copper_wire: 1}, computer_chip, 1, F, "Электроника"),
        Recipe("Комплект проводов", {silver_type: 2}, wiring_kit, 1, F, "Электроника"),
        Recipe("Расширенный комплект проводов", {wiring_kit: 1, gold_type: 2, computer_chip: 1}, advanced_wiring_kit, 1, F, "Электроника"),
        Recipe("Топливный стержень реактора", {uraninite_type: 3, lead_type: 1, titan_type: 1, glass_type: 1}, reactor_rod, 1, F, "Электроника"),
        Recipe("Ионная батарея", {ion_cube_type: 1, gold_type: 1, silver_type: 1}, ion_battery, 1, F, "Электроника"),
        Recipe("Ионная энергоячейка", {ion_battery: 2, silicone_rubber: 1}, ion_power_cell, 1, F, "Электроника"),

        # Personal / Equipment / Tools
        Recipe("Ласты", {silicone_rubber: 2}, fins_type, 1, F, "Снаряжение"),
        Recipe("Обычный кислородный баллон", {titan_type: 3}, standard_tank, 1, F, "Снаряжение"),
        Recipe("Баллон высокой ёмкости", {standard_tank: 1, glass_type: 2, titan_type: 4, silver_type: 1}, high_capacity_tank, 1, F, "Снаряжение"),
        Recipe("Ребризер", {wiring_kit: 1, fiber_mesh: 1}, rebreather_type, 1, F, "Снаряжение"),
        Recipe("Противорадиационный костюм", {fiber_mesh: 2, lead_type: 2}, radiation_suit, 1, F, "Снаряжение"),
        Recipe("Укреплённый костюм ныряльщика", {synthetic_fibers: 1, diamond_type: 2, titan_type: 2}, reinforced_suit, 1, F, "Снаряжение"),
        Recipe("Фильтрационный костюм", {synthetic_fibers: 1, aerogel_type: 1}, water_filtration_suit, 1, F, "Снаряжение"),
        Recipe("Компас", {copper_wire: 1, wiring_kit: 1}, compass_type, 1, F, "Снаряжение"),
        Recipe("Аптечка", {fiber_mesh: 1}, first_aid_kit, 1, F, "Снаряжение"),
        Recipe("Огнетушитель", {titan_type: 3}, fire_extinguisher, 1, F, "Снаряжение"),
        Recipe("Плавучий воздушный насос", {titan_type: 2}, floating_air_pump, 1, F, "Снаряжение"),
        Recipe("Труба", {titan_type: 2}, pipe_type, 5, F, "Снаряжение"),
        Recipe("Нож", {silicone_rubber: 1, titan_type: 1}, survival_knife, 1, F, "Инструменты"),
        Recipe("Сканер", {battery_type: 1, titan_type: 1}, scanner_type, 1, F, "Инструменты"),
        Recipe("Ремонтный инструмент", {silicone_rubber: 1, cave_sulfur_type: 1, titan_type: 1}, repair_tool, 1, F, "Инструменты"),
        Recipe("Ремкомплект", {titan_type: 2, silicone_rubber: 1, cave_sulfur_type: 1}, repair_kit, 1, F, "Инструменты"),
        Recipe("Фонарик", {battery_type: 1, glass_type: 1}, flashlight_type, 1, F, "Инструменты"),
        Recipe("Строитель", {computer_chip: 1, wiring_kit: 1, battery_type: 1}, habitat_builder_type, 1, F, "Инструменты"),
        Recipe("Воздушный пузырь", {silicone_rubber: 1, bladderfish_type: 1, titan_type: 1}, air_bladder, 1, F, "Инструменты"),
        Recipe("Инструмент исследователя", {creepvine_sample_type: 1, copper_wire: 1, titan_type: 1}, pathfinder_tool, 1, F, "Инструменты"),
        Recipe("Пропульсионная пушка", {wiring_kit: 1, battery_type: 1, titan_type: 1}, propulsion_cannon, 1, F, "Инструменты"),
        Recipe("Стазис-винтовка", {computer_chip: 1, battery_type: 1, magnetite_type: 2}, stasis_rifle, 1, F, "Инструменты"),
        Recipe("Лазерный резак", {diamond_type: 2, battery_type: 1, titan_type: 1, cave_sulfur_type: 1}, laser_cutter, 1, F, "Инструменты"),
        Recipe("Сигнальная ракета", {cave_sulfur_type: 1}, flare_type, 5, F, "Инструменты"),

        # Deployables
        Recipe("Радиомаяк", {copper_wire: 1, titan_type: 1}, beacon_type, 1, F, "Размещаемое"),
        Recipe("Приманка для существ", {titan_type: 3, wiring_kit: 1}, creature_decoy, 1, F, "Размещаемое"),
        Recipe("Морской глайдер", {battery_type: 1, lubricant_type: 1, copper_wire: 1, titan_type: 1}, seaglide_type, 1, F, "Размещаемое"),
        Recipe("Переносной сборщик транспорта", {titanium_ingot: 1, lubricant_type: 1, power_cell_type: 1}, mobile_vehicle_bay, 1, F, "Размещаемое"),
        Recipe("Грави-ловушка", {battery_type: 1, copper_wire: 1, titan_type: 1}, grav_trap, 1, F, "Размещаемое"),
        Recipe("Водостойкий контейнер", {titan_type: 4}, waterproof_locker, 1, F, "Размещаемое"),

        # Alien tablets
        Recipe("Фиолетовая скрижаль", {ion_cube_type: 1, diamond_type: 2}, purple_tablet, 1, F, "Предтечи"),
        Recipe("Оранжевая скрижаль", {ion_cube_type: 1, nickel_type: 2}, orange_tablet, 1, F, "Предтечи"),
        Recipe("Синяя скрижаль", {ion_cube_type: 1, kyanite_type: 2}, blue_tablet, 1, F, "Предтечи"),

        # Modification Station
        Recipe("Термоклинок", {survival_knife: 1, battery_type: 1}, thermoblade, 1, M, "Модификации"),
        Recipe("Лёгкий баллон высокой ёмкости", {high_capacity_tank: 1, plasteel_ingot: 1}, lightweight_tank, 1, M, "Модификации"),
        Recipe("Баллон сверхвысокой ёмкости", {high_capacity_tank: 1, lithium_type: 4}, ultra_tank, 1, M, "Модификации"),
        Recipe("Репульсионная пушка", {propulsion_cannon: 1, computer_chip: 1, magnetite_type: 2}, repulsion_cannon, 1, M, "Модификации"),
        Recipe("Модуль глубины «Мотылька» – Мод. 2", {seamoth_depth1: 1, plasteel_ingot: 1, magnetite_type: 2, enameled_glass: 1}, seamoth_depth2, 1, M, "Модификации"),
        Recipe("Модуль глубины «Мотылька» – Мод. 3", {seamoth_depth2: 1, plasteel_ingot: 1, ruby_type: 3}, seamoth_depth3, 1, M, "Модификации"),
        Recipe("Модуль глубины костюма КРАБ – Мод. 2", {prawn_depth1: 1, titan_type: 5, lithium_type: 2, kyanite_type: 3}, prawn_depth2, 1, M, "Модификации"),
        Recipe("Модуль глубины «Циклопа» – Мод. 2", {cyclops_depth1: 1, plasteel_ingot: 1, nickel_type: 3}, cyclops_depth2, 1, M, "Модификации"),
        Recipe("Модуль глубины «Циклопа» – Мод. 3", {cyclops_depth2: 1, plasteel_ingot: 1, kyanite_type: 3}, cyclops_depth3, 1, M, "Модификации"),

        # Vehicles / Neptune
        Recipe("Мотылёк", {titanium_ingot: 1, power_cell_type: 1, glass_type: 2, lubricant_type: 1, lead_type: 1}, seamoth_type, 1, V, "Транспорт"),
        Recipe("Костюм КРАБ", {plasteel_ingot: 2, aerogel_type: 2, enameled_glass: 1, diamond_type: 2, lead_type: 2}, prawn_suit_type, 1, V, "Транспорт"),
        Recipe("Циклоп", {plasteel_ingot: 3, enameled_glass: 3, lubricant_type: 1, advanced_wiring_kit: 1, lead_type: 3}, cyclops_type, 1, V, "Транспорт"),
        Recipe("Пусковая платформа «Нептуна»", {titanium_ingot: 2, computer_chip: 1, lead_type: 4}, neptune_platform, 1, V, "Нептун"),
        Recipe("Башня подъёмника «Нептуна»", {plasteel_ingot: 1, copper_wire: 1, lubricant_type: 1}, neptune_gantry, 1, V, "Нептун"),
        Recipe("Ускорители «Нептуна»", {plasteel_ingot: 1, nickel_type: 3, wiring_kit: 1, aerogel_type: 1}, neptune_boosters, 1, V, "Нептун"),
        Recipe("Топливные баки «Нептуна»", {plasteel_ingot: 1, ion_power_cell: 4, kyanite_type: 4, cave_sulfur_type: 2}, neptune_fuel, 1, V, "Нептун"),
        Recipe("Кабина «Нептуна»", {cyclops_shield: 1, plasteel_ingot: 1, enameled_glass: 1, computer_chip: 1}, neptune_cockpit, 1, V, "Нептун"),

        # Vehicle Upgrade Console
        Recipe("Модуль эффективности двигателя", {computer_chip: 1, polyaniline_type: 1}, vehicle_engine_eff, 1, U, "Улучшения транспорта"),
        Recipe("Солнечная зарядка «Мотылька»", {advanced_wiring_kit: 1, enameled_glass: 1}, seamoth_solar, 1, U, "Улучшения транспорта"),
        Recipe("Модуль хранилища", {titan_type: 3, lithium_type: 1}, vehicle_storage, 1, U, "Улучшения транспорта"),
        Recipe("Система периметральной защиты «Мотылька»", {polyaniline_type: 1, wiring_kit: 1}, seamoth_perimeter, 1, U, "Улучшения транспорта"),
        Recipe("Усиление корпуса транспорта", {titan_type: 3, lithium_type: 1, diamond_type: 1}, hull_reinforcement, 1, U, "Улучшения транспорта"),
        Recipe("Торпедная установка «Мотылька»", {titan_type: 3, lithium_type: 1, aerogel_type: 1}, seamoth_torpedo, 1, U, "Улучшения транспорта"),
        Recipe("Гидролокатор «Мотылька»", {copper_wire: 1, magnetite_type: 2}, seamoth_sonar, 1, U, "Улучшения транспорта"),
        Recipe("Вихревая торпеда", {titan_type: 1, magnetite_type: 1}, vortex_torpedo, 2, U, "Боеприпасы"),
        Recipe("Газовая торпеда", {titan_type: 1, gas_pod_type: 1}, gas_torpedo, 2, U, "Боеприпасы"),
        Recipe("Модуль глубины «Мотылька» – Мод. 1", {titanium_ingot: 1, glass_type: 2}, seamoth_depth1, 1, U, "Улучшения транспорта"),
        Recipe("Улучшение реактивного ранца костюма КРАБ", {nickel_type: 2, cave_sulfur_type: 1, titan_type: 1, lithium_type: 1}, prawn_jet, 1, U, "КРАБ"),
        Recipe("Бур костюма КРАБ", {titan_type: 5, lithium_type: 1, diamond_type: 4}, prawn_drill, 1, U, "КРАБ"),
        Recipe("Тепловой реактор костюма КРАБ", {kyanite_type: 2, polyaniline_type: 2, wiring_kit: 1}, prawn_thermal, 1, U, "КРАБ"),
        Recipe("Пропульсионная пушка костюма КРАБ", {computer_chip: 1, titan_type: 5, lithium_type: 1, magnetite_type: 2}, prawn_propulsion, 1, U, "КРАБ"),
        Recipe("Рука-захват костюма КРАБ", {advanced_wiring_kit: 1, titan_type: 5, lithium_type: 1, benzene_type: 1}, prawn_grapple, 1, U, "КРАБ"),
        Recipe("Торпедная установка костюма КРАБ", {titan_type: 5, lithium_type: 1, aerogel_type: 1}, prawn_torpedo, 1, U, "КРАБ"),
        Recipe("Модуль глубины костюма КРАБ – Мод. 1", {plasteel_ingot: 1, nickel_type: 3, ruby_type: 2}, prawn_depth1, 1, U, "КРАБ"),

        # Scanner room
        Recipe("Чип интерфейса комнаты сканирования", {computer_chip: 1, magnetite_type: 1}, scanner_hud, 1, S, "Комната сканирования"),
        Recipe("Улучшение дальности сканирования", {copper_type: 1, magnetite_type: 1}, scanner_range, 1, S, "Комната сканирования"),
        Recipe("Улучшение скорости сканирования", {silver_type: 1, gold_type: 1}, scanner_speed, 1, S, "Комната сканирования"),
        Recipe("Дрон-камера", {computer_chip: 1, battery_type: 1, glass_type: 1, titan_type: 1}, camera_drone, 1, S, "Комната сканирования"),

        # Cyclops upgrades
        Recipe("Модуль эффективности двигателя «Циклопа»", {computer_chip: 1, benzene_type: 1, polyaniline_type: 1}, cyclops_engine_eff, 1, C, "Циклоп"),
        Recipe("Модуль глубины «Циклопа» – Мод. 1", {plasteel_ingot: 1, ruby_type: 3}, cyclops_depth1, 1, C, "Циклоп"),
        Recipe("Генератор щита «Циклопа»", {advanced_wiring_kit: 1, polyaniline_type: 1, power_cell_type: 1}, cyclops_shield, 1, C, "Циклоп"),
        Recipe("Гидролокатор «Циклопа»", {computer_chip: 1, magnetite_type: 3}, cyclops_sonar, 1, C, "Циклоп"),
        Recipe("Ремонтный модуль стыковочного отсека «Циклопа»", {repair_tool: 1, copper_wire: 1}, cyclops_repair, 1, C, "Циклоп"),
        Recipe("Улучшение камеры приманок «Циклопа»", {titan_type: 3, lithium_type: 1}, cyclops_decoy, 1, C, "Циклоп"),
        Recipe("Система пожаротушения «Циклопа»", {aerogel_type: 2, cave_sulfur_type: 2}, cyclops_fire, 1, C, "Циклоп"),
        Recipe("Модуль теплового реактора «Циклопа»", {kyanite_type: 4, polyaniline_type: 2, wiring_kit: 1}, cyclops_thermal, 1, C, "Циклоп"),

        # Habitat Builder — Base Pieces
        Recipe("Многоцелевая комната", {titan_type: 6}, multipurpose_room, 1, H, "Детали базы"),
        Recipe("Люк", {quartz_type: 1, titan_type: 2}, hatch_type, 1, H, "Детали базы"),
        Recipe("Окно", {glass_type: 1}, window_type, 1, H, "Детали базы"),
        Recipe("Фундамент", {titan_type: 2, lead_type: 2}, foundation_type, 1, H, "Детали базы"),
        Recipe("Прямой отсек", {titan_type: 2}, i_compartment, 1, H, "Детали базы"),
        Recipe("Угловой отсек", {titan_type: 2}, l_compartment, 1, H, "Детали базы"),
        Recipe("T-образный отсек", {titan_type: 3}, t_compartment, 1, H, "Детали базы"),
        Recipe("Крестообразный отсек", {titan_type: 3}, x_compartment, 1, H, "Детали базы"),
        Recipe("Усиление корпуса", {lithium_type: 1, titan_type: 3}, reinforcement_type, 1, H, "Детали базы"),
        Recipe("Прямой стеклянный отсек", {glass_type: 2}, glass_i_compartment, 1, H, "Детали базы"),
        Recipe("Угловой стеклянный отсек", {glass_type: 2}, glass_l_compartment, 1, H, "Детали базы"),
        Recipe("Обсерватория", {enameled_glass: 2, titan_type: 1}, observatory_type, 1, H, "Детали базы"),
        Recipe("Вертикальный соединитель", {titan_type: 2}, vertical_connector, 1, H, "Детали базы"),
        Recipe("Стыковочная шахта", {titanium_ingot: 2, lubricant_type: 1, lead_type: 2}, moonpool_type, 1, H, "Детали базы"),
        Recipe("Комната сканирования", {titan_type: 5, copper_type: 2, gold_type: 1, table_coral_type: 1}, scanner_room_type, 1, H, "Детали базы"),
        Recipe("Большая комната", {plasteel_ingot: 2}, large_room_type, 1, H, "Детали базы"),
        Recipe("Стеклянный купол многоцелевой комнаты", {enameled_glass: 2, titan_type: 2, lithium_type: 1}, multipurpose_dome, 1, H, "Детали базы"),
        Recipe("Стеклянный купол большой комнаты", {enameled_glass: 4, titan_type: 4, lithium_type: 2}, large_room_dome, 1, H, "Детали базы"),

        # Exterior modules
        Recipe("Прожектор", {glass_type: 1, titan_type: 2}, spotlight_type, 1, H, "Внешние модули"),
        Recipe("Солнечная панель", {quartz_type: 2, titan_type: 2, copper_type: 1}, solar_panel_type, 1, H, "Внешние модули"),
        Recipe("Энергопередатчик", {gold_type: 1, titan_type: 1}, power_transmitter, 1, H, "Внешние модули"),
        Recipe("Теплоэлектростанция", {titan_type: 5, magnetite_type: 2, aerogel_type: 1}, thermal_plant, 1, H, "Внешние модули"),
        Recipe("Наружная грядка", {titan_type: 2}, exterior_growbed, 1, H, "Внешние модули"),
        Recipe("Осветительная мачта", {glass_type: 1, titan_type: 1}, floodlight_type, 1, H, "Внешние модули"),
        Recipe("Стационарный воздушный насос", {titan_type: 2}, base_air_pump, 1, H, "Внешние модули"),

        # Interior pieces
        Recipe("Лестница", {titan_type: 2}, ladder_type, 1, H, "Внутренние элементы"),
        Recipe("Переборка", {titan_type: 3, silicone_rubber: 1}, bulkhead_type, 1, H, "Внутренние элементы"),
        Recipe("Консоль улучшения транспорта", {titan_type: 3, computer_chip: 1, copper_wire: 1}, vehicle_upgrade_console, 1, H, "Внутренние элементы"),
        Recipe("Водоочистная станция", {titan_type: 3, copper_wire: 1, aerogel_type: 1}, water_filtration_machine, 1, H, "Внутренние элементы"),
        Recipe("Большой аквариум", {glass_type: 5, titan_type: 2}, alien_containment, 1, H, "Внутренние элементы"),
        Recipe("Биореактор", {titan_type: 3, wiring_kit: 1, lubricant_type: 1}, bioreactor, 1, H, "Внутренние элементы"),
        Recipe("Ядерный реактор", {plasteel_ingot: 3, advanced_wiring_kit: 1, lead_type: 3}, nuclear_reactor, 1, H, "Внутренние элементы"),
        Recipe("Дверь переборки большой комнаты", {titan_type: 1}, large_partition_door, 1, H, "Внутренние элементы"),
        Recipe("Переборка большой комнаты", {titan_type: 1}, large_partition, 1, H, "Внутренние элементы"),

        # Interior modules
        Recipe("Модификационная станция", {computer_chip: 1, titan_type: 1, diamond_type: 1, lead_type: 1}, modification_station, 1, H, "Внутренние модули"),
        Recipe("Изготовитель", {titan_type: 1, gold_type: 1, table_coral_type: 1}, fabricator_type, 1, H, "Внутренние модули"),
        Recipe("Аквариум", {glass_type: 2, titan_type: 1}, aquarium_type, 1, H, "Внутренние модули"),
        Recipe("Шкаф", {quartz_type: 1, titan_type: 2}, locker_type, 1, H, "Внутренние модули"),
        Recipe("Настенный шкаф", {titan_type: 2}, wall_locker, 1, H, "Внутренние модули"),
        Recipe("Горшок для растений", {titan_type: 2}, plant_pot, 1, H, "Внутренние модули"),
        Recipe("Внутренняя грядка", {titan_type: 2}, indoor_growbed, 1, H, "Внутренние модули"),
        Recipe("Стеллаж для растений", {titan_type: 1}, plant_shelf, 1, H, "Внутренние модули"),
        Recipe("Радио", {titan_type: 1, copper_type: 1}, radio_type, 1, H, "Внутренние модули"),
        Recipe("Композитный горшок", {titan_type: 2}, composite_pot, 1, H, "Внутренние модули"),
        Recipe("Роскошный горшок", {titan_type: 2}, chic_pot, 1, H, "Внутренние модули"),
        Recipe("Изготовитель аптечек", {computer_chip: 1, fiber_mesh: 1, silver_type: 1, titan_type: 1}, medical_fabricator, 1, H, "Внутренние модули"),
        Recipe("Зарядное устройство батарей", {wiring_kit: 1, copper_wire: 1, titan_type: 1}, battery_charger, 1, H, "Внутренние модули"),
        Recipe("Зарядное устройство энергоячеек", {advanced_wiring_kit: 1, ruby_type: 2, titan_type: 2}, power_cell_charger, 1, H, "Внутренние модули"),
        Recipe("Центрифуга", {titan_type: 2, wiring_kit: 1}, centrifuge, 1, H, "Внутренние модули"),

        # Furniture / decoration subset from the original builder menu.
        Recipe("Скамья", {titan_type: 2}, bench_type, 1, H, "Мебель"),
        Recipe("Фоторамка", {copper_wire: 1}, picture_frame, 1, H, "Мебель"),
        Recipe("Настенная полка", {titan_type: 1}, wall_shelf, 1, H, "Мебель"),
        Recipe("Кровать", {titan_type: 2, fiber_mesh: 1}, bed_type, 1, H, "Мебель"),
        Recipe("Рабочий стол", {titan_type: 1}, desk_type, 1, H, "Мебель"),
        Recipe("Офисный стул", {titan_type: 1}, chair_type, 1, H, "Мебель"),
        Recipe("Торговый автомат", {glass_type: 1, titan_type: 2}, vending_machine, 1, H, "Мебель"),
        Recipe("Кофейный торговый автомат", {titan_type: 2}, coffee_machine, 1, H, "Мебель"),
        Recipe("Урна", {titan_type: 2}, trash_can, 1, H, "Мебель"),
        Recipe("Утилизатор ядерных отходов", {titan_type: 2}, nuclear_waste, 1, H, "Мебель"),

        # Совместимость с прежней 2D-механикой: эти два элемента нужны
        # существующим сохранениям и правилу «крафт на построенном полу».
        Recipe("2D-стена", {rock_type: 2, limestone_type: 2}, wall_type, 1, F, "2D-совместимость"),
        Recipe("2D-пол", {limestone_type: 1, sand_type: 2, clay_type: 1}, floor_type, 1, F, "2D-совместимость"),
    ]

    # -----------------------------------------------------
    # БИОМЫ
    # -----------------------------------------------------

    biomes = []

    # =====================================================
    # АВРОРА: ПОДРОБНАЯ СХЕМА ОСНОВНЫХ ОТСЕКОВ
    # =====================================================
    # Планировка адаптирована под 2D-игру. В неё включены основные
    # исследуемые области оригинальной «Авроры»: входной коридор,
    # администрация, грузовой отсек и его подъёмник, нижний грузовой
    # отсек, четырёхсторонний коридор, отсек «Мотылька», двигательный
    # отсек, раздевалка, PRAWN Bay, жилые помещения с каютами,
    # комнаты чёрного ящика, большая катушка данных, лаборатория и
    # аварийный выход.

    AURORA_HULL = (78, 72, 62)
    AURORA_WALL = (102, 94, 82)
    AURORA_NOSE = (60, 55, 46)
    AURORA_ENGINE = (58, 48, 42)
    AURORA_REACTOR = (72, 48, 54)
    AURORA_FLOOR = (86, 80, 70)
    AURORA_ADMIN = (70, 82, 92)
    AURORA_CARGO = (93, 78, 58)
    AURORA_DOCK = (60, 78, 92)
    AURORA_LIVING = (92, 72, 67)
    AURORA_LAB = (66, 78, 82)
    AURORA_BLACKBOX = (50, 58, 68)

    # Базовая модель корабля была нарисована около X=200; сразу переносим
    # её на восток, в нашу Зону крушения.
    AURORA_SHIFT_X = 550

    def aurora_rect(rect):
        x1, y1, x2, y2 = rect
        return (x1 + AURORA_SHIFT_X, y1,
                x2 + AURORA_SHIFT_X, y2)

    def add_aurora_floor(name, rect, color=AURORA_FLOOR,
                         objects=None, priority=120):
        if objects is None:
            objects = []
        biome = Biome(
            name, color, *aurora_rect(rect),
            list(objects), [], passable=True,
            cave_enabled=False, priority=priority
        )
        biome.aurora_style = True
        biome.location_kind = 'aurora_room'
        biomes.append(biome)
        return biome

    def add_aurora_wall(name, rect, color=AURORA_WALL,
                        priority=170):
        biome = Biome(
            name, color, *aurora_rect(rect),
            [], [], passable=False,
            cave_enabled=False, priority=priority
        )
        biome.aurora_style = True
        biome.location_kind = 'aurora_wall'
        biomes.append(biome)
        return biome

    def add_aurora_passage(name, rect, color=AURORA_FLOOR,
                           priority=185):
        # Проход с более высоким приоритетом прорезает стену корпуса.
        return add_aurora_floor(
            name, rect, color=color,
            objects=[], priority=priority
        )

    # Основной настил корпуса. Поверх него идут именованные помещения.
    add_aurora_floor(
        'Внутренние отсеки Авроры',
        (196, 381, 299, 649),
        AURORA_FLOOR,
        priority=100
    )

    # Передняя разорванная часть корпуса.
    for rect in [
        (247, 351, 253, 356),
        (241, 357, 259, 362),
        (234, 363, 266, 368),
        (227, 369, 273, 374),
        (221, 375, 279, 380),
    ]:
        add_aurora_floor(
            'Разорванная носовая часть Авроры',
            rect, AURORA_FLOOR, priority=105
        )

    # Основные исследуемые секции.
    AURORA_ROOMS = [
        ('Входной коридор Авроры / Airlock',
         (238, 370, 260, 392), AURORA_ADMIN),
        ('Коридор администрации Авроры',
         (214, 390, 260, 404), AURORA_ADMIN),
        ('Кабинет администрации Авроры',
         (200, 402, 234, 426), AURORA_ADMIN),
        ('Обрушенный коридор Авроры к грузовому отсеку',
         (238, 402, 263, 434), AURORA_HULL),
        ('Коридор грузового отсека Авроры',
         (235, 426, 265, 448), AURORA_CARGO),
        ('Главный грузовой отсек Авроры',
         (202, 444, 292, 500), AURORA_CARGO),
        ('Грузовой подъёмник Авроры',
         (260, 486, 287, 511), AURORA_CARGO),
        ('Нижний грузовой отсек Авроры',
         (218, 498, 288, 522), AURORA_CARGO),
        ('Четырёхсторонний коридор Авроры',
         (234, 516, 266, 541), AURORA_FLOOR),
        ('Отсек «Мотылёк» Авроры',
         (197, 518, 232, 561), AURORA_DOCK),
        ('Коридор двигательного отсека Авроры',
         (263, 518, 282, 551), AURORA_ENGINE),
        ('Двигательный отсек / реактор Авроры',
         (273, 538, 298, 586), AURORA_REACTOR),
        ('Раздевалка Авроры',
         (232, 538, 263, 563), AURORA_LIVING),
        ('Отсек костюмов КРАБ / PRAWN Bay Авроры',
         (197, 562, 272, 611), AURORA_DOCK),
        ('Пролом корпуса PRAWN Bay Авроры',
         (270, 582, 293, 610), AURORA_HULL),
        ('Жилой коридор Авроры',
         (198, 607, 270, 646), AURORA_LIVING),
        ('Столовая Авроры',
         (199, 611, 220, 632), AURORA_LIVING),
        ('Каюта №1 Авроры',
         (222, 611, 235, 625), AURORA_LIVING),
        ('Каюта капитана Авроры',
         (237, 611, 254, 625), AURORA_LIVING),
        ('Каюта №3 Авроры',
         (256, 611, 269, 625), AURORA_LIVING),
        ('Каюта №4 Авроры',
         (222, 628, 235, 643), AURORA_LIVING),
        ('Каюта №6 Авроры',
         (237, 628, 249, 643), AURORA_LIVING),
        ('Каюта №7 Авроры',
         (251, 628, 265, 643), AURORA_LIVING),
        ('Подводный технический проход Авроры',
         (266, 604, 282, 636), AURORA_DOCK),
        ('Верхняя комната чёрного ящика Авроры',
         (270, 618, 292, 634), AURORA_BLACKBOX),
        ('Нижняя комната чёрного ящика Авроры',
         (270, 634, 292, 648), AURORA_BLACKBOX),
        ('Большая катушка данных Авроры',
         (258, 634, 274, 648), AURORA_BLACKBOX),
        ('Лаборатория Авроры',
         (280, 603, 299, 635), AURORA_LAB),
        ('Обрушенный коридор лаборатории Авроры',
         (286, 584, 299, 605), AURORA_HULL),
        ('Выходной коридор Авроры',
         (291, 570, 299, 594), AURORA_FLOOR),
    ]

    for room_name, room_rect, room_color in AURORA_ROOMS:
        room_objects = []
        if 'Двигательный отсек' in room_name:
            room_objects = [(schweer_cannon, 1)]
        elif 'Отсек костюмов КРАБ' in room_name:
            room_objects = [(lang_cannon, 1)]
        add_aurora_floor(
            room_name, room_rect, room_color,
            objects=room_objects, priority=125
        )

    # Наружный корпус: боковые борта и кормовая переборка.
    for rect in [
        (195, 380, 195, 650),
        (300, 380, 300, 569),
        (300, 606, 300, 650),
        (195, 650, 300, 650),
        (195, 380, 220, 380),
        (280, 380, 300, 380),
    ]:
        add_aurora_wall('Корпус Авроры', rect, AURORA_HULL)

    # Нос корабля, оставляя центральный верхний вход.
    for rect in [
        (220, 375, 226, 375),
        (226, 369, 233, 369),
        (233, 363, 240, 363),
        (240, 357, 246, 357),
        (254, 357, 260, 357),
        (260, 363, 267, 363),
        (267, 369, 274, 369),
        (274, 375, 280, 375),
    ]:
        add_aurora_wall('Нос Авроры', rect, AURORA_NOSE)

    # Несколько крупных переборок. Проходы добавляются ниже отдельными
    # passable-областями с большим приоритетом.
    for rect in [
        (196, 438, 299, 439),
        (196, 513, 299, 514),
        (196, 560, 299, 561),
        (196, 605, 299, 606),
    ]:
        add_aurora_wall('Внутренняя переборка Авроры', rect)

    # Дверные проёмы и два маршрута внутрь корабля.
    for name, rect, color in [
        ('Верхний вход Авроры', (244, 350, 256, 382), AURORA_FLOOR),
        ('Дверь грузового отсека Авроры', (245, 437, 256, 441), AURORA_CARGO),
        ('Проход к нижнему грузовому отсеку Авроры', (245, 512, 258, 516), AURORA_CARGO),
        ('Проход к PRAWN Bay Авроры', (238, 559, 258, 563), AURORA_DOCK),
        ('Проход в жилые отсеки Авроры', (204, 604, 218, 608), AURORA_LIVING),
        ('Проход к чёрному ящику Авроры', (264, 604, 278, 608), AURORA_BLACKBOX),
        ('Нижний аварийный вход Авроры', (296, 588, 305, 602), AURORA_LAB),
    ]:
        add_aurora_passage(name, rect, color=color)

    # =====================================================
    # НОВАЯ КАРТА БИОМОВ
    # =====================================================

    def add_surface_blob(
            name,
            label,
            color,
            cx, cy,
            rx, ry,
            seed,
            objects,
            priority=10,
            jitter=0.14
    ):
        polygon = make_blob_points(
            cx, cy,
            rx, ry,
            seed=seed,
            point_count=24,
            jitter=jitter
        )

        biome = Biome(
            name,
            color,
            0, 0, 0, 0,
            objects,
            [],
            polygon=polygon,
            map_label=label,
            cave_enabled=True,
            priority=priority
        )

        biomes.append(biome)
        return biome

    # Левая часть карты.
    add_surface_blob(
        "Дюны", "ДЮНЫ", (205, 187, 120),
        110, 420, 130, 300, 11,
        [
            (sand_type, 6),
            (quartz_type, 3),
            (silver_type, 2),
            (lead_type, 2),
            (iron_type, 1),
            (lithium_type, 1),
            (diamond_type, 1),
        ],
        priority=10
    )

    add_surface_blob(
        "Бурые водоросли (север)", "БУРЫЕ\nВОДОРОСЛИ",
        (170, 50, 190),
        345, 115, 155, 105, 12,
        [
            (seaweed_type, 8),
            (titan_type, 3),
            (copper_type, 3),
            (salt_type, 4),
            (quartz_type, 2),
            (coal_type, 2),
        ],
        priority=12
    )

    add_surface_blob(
        "Грибной лес (запад)", "ГРИБНОЙ\nЛЕС",
        (40, 75, 180),
        300, 325, 130, 115, 13,
        [
            (quartz_type, 4),
            (lithium_type, 3),
            (gold_type, 2),
            (diamond_type, 1),
            (coal_type, 2),
        ],
        priority=13
    )

    # Север.
    add_surface_blob(
        "Подводные острова", "ПОДВОДНЫЕ\nОСТРОВА",
        (125, 77, 55),
        500, 230, 115, 85, 14,
        [
            (quartz_type, 4),
            (lithium_type, 3),
            (gold_type, 2),
            (iron_type, 2),
            (diamond_type, 1),
        ],
        priority=14
    )

    add_surface_blob(
        "Горы", "ГОРЫ", (36, 45, 50),
        735, 130, 225, 125, 15,
        [
            (quartz_type, 4),
            (iron_type, 2),
            (lithium_type, 4),
            (magnetite_type, 3),
            (diamond_type, 2),
            (uraninite_type, 1),
        ],
        priority=11
    )

    # Правая верхняя часть.
    add_surface_blob(
        "Зона Куша", "ЗОНА КУША", (140, 125, 205),
        875, 315, 125, 175, 16,
        [
            (quartz_type, 4),
            (salt_type, 3),
            (lithium_type, 2),
            (magnetite_type, 2),
        ],
        priority=12
    )

    add_surface_blob(
        "Грибной лес (восток)", "ГРИБНОЙ\nЛЕС",
        (45, 70, 175),
        690, 365, 105, 105, 17,
        [
            (quartz_type, 4),
            (lithium_type, 3),
            (gold_type, 2),
            (diamond_type, 1),
            (coal_type, 1),
        ],
        priority=15
    )

    # Центр.
    add_surface_blob(
        "Водоросли", "ВОДОРОСЛИ", (100, 170, 65),
        535, 390, 120, 105, 18,
        [
            (seaweed_type, 10),
            (titan_type, 3),
            (copper_type, 3),
            (salt_type, 4),
            (quartz_type, 2),
            (coal_type, 2),
        ],
        priority=17
    )

    add_surface_blob(
        "Травянистое плато", "ТРАВЯНИСТОЕ\nПЛАТО",
        (185, 55, 100),
        355, 535, 145, 125, 19,
        [
            (quartz_type, 5),
            (copper_type, 3),
            (silver_type, 3),
            (lead_type, 2),
            (gold_type, 1),
            (coal_type, 4),
        ],
        priority=16
    )

    add_surface_blob(
        "Безопасные отмели", "БЕЗОПАСНЫЕ\nОТМЕЛИ",
        (130, 165, 145),
        520, 560, 115, 110, 20,
        [
            (titan_type, 5),
            (copper_type, 2),
            (quartz_type, 4),
            (limestone_type, 3),
            (salt_type, 2),
            (sand_type, 4),
            (clay_type, 3),
            (iron_type, 1),
        ],
        priority=25,
        jitter=0.11
    )

    # Юго-запад.
    add_surface_blob(
        "Бурые водоросли (юго-запад)", "БУРЫЕ\nВОДОРОСЛИ",
        (100, 45, 120),
        180, 675, 100, 80, 21,
        [
            (seaweed_type, 8),
            (titan_type, 3),
            (copper_type, 3),
            (salt_type, 4),
            (coal_type, 2),
        ],
        priority=14
    )

    add_surface_blob(
        "Редкий риф", "РЕДКИЙ РИФ", (30, 110, 80),
        375, 710, 140, 105, 22,
        [
            (quartz_type, 4),
            (ruby_type, 3),
            (lithium_type, 2),
            (uraninite_type, 2),
        ],
        priority=15
    )

    add_surface_blob(
        "Морской путь", "МОРСКОЙ\nПУТЬ", (75, 145, 185),
        110, 800, 100, 120, 23,
        [
            (quartz_type, 3),
            (lithium_type, 3),
            (silver_type, 2),
            (diamond_type, 2),
        ],
        priority=12
    )

    add_surface_blob(
        "Большой риф", "БОЛЬШОЙ\nРИФ", (20, 115, 175),
        300, 865, 195, 125, 24,
        [
            (quartz_type, 4),
            (ruby_type, 4),
            (uraninite_type, 3),
            (gel_sack_type, 3),
            (diamond_type, 1),
        ],
        priority=13
    )

    # Восток.
    add_surface_blob(
        "Зона крушения", "ЗОНА КРУШЕНИЯ", (115, 78, 75),
        825, 625, 225, 270, 25,
        [
            (titan_type, 8),
            (quartz_type, 3),
            (lead_type, 3),
            (copper_type, 2),
            (silver_type, 1),
        ],
        priority=11
    )

    add_surface_blob(
        "Скалистое поле", "СКАЛИСТОЕ\nПОЛЕ", (125, 45, 25),
        635, 845, 145, 145, 26,
        [
            (quartz_type, 4),
            (silver_type, 3),
            (gold_type, 2),
            (lithium_type, 2),
            (lead_type, 2),
        ],
        priority=15
    )


    # -----------------------------------------------------
    # КАНОНИЧЕСКИЕ КРАФТОВЫЕ РЕСУРСЫ ПО БИОМАМ
    # -----------------------------------------------------
    extra_resource_profiles = {
        "Безопасные отмели": [(metal_salvage_type, 4), (acid_mushroom_item, 5),
                              (table_coral_type, 3), (coral_tube_type, 2),
                              (cave_sulfur_type, 2), (gas_pod_type, 2)],
        "Водоросли": [(metal_salvage_type, 4), (creepvine_sample_type, 6),
                      (creepvine_seed_type, 4), (stalker_tooth_type, 2)],
        "Травянистое плато": [(metal_salvage_type, 3), (table_coral_type, 2),
                              (cave_sulfur_type, 1)],
        "Грибной лес (запад)": [(stalker_tooth_type, 1), (nickel_type, 1)],
        "Грибной лес (восток)": [(stalker_tooth_type, 1), (nickel_type, 1)],
        "Бурые водоросли (север)": [(blood_oil_type, 5), (deep_shroom_item, 4),
                                    (nickel_type, 2)],
        "Бурые водоросли (юго-запад)": [(blood_oil_type, 5), (deep_shroom_item, 4),
                                         (nickel_type, 2)],
        "Большой риф": [(nickel_type, 3), (ion_cube_type, 1), (deep_shroom_item, 2)],
        "Редкий риф": [(nickel_type, 2), (ion_cube_type, 1)],
        "Горы": [(nickel_type, 2), (ion_cube_type, 1)],
        "Зона Куша": [(nickel_type, 2)],
        "Зона крушения": [(metal_salvage_type, 7), (cave_sulfur_type, 1)],
        "Дюны": [(nickel_type, 2)],
        "Скалистое поле": [(nickel_type, 2)],
    }
    for _biome in biomes:
        if _biome.cave_enabled:
            _biome.objects.extend(extra_resource_profiles.get(_biome.name, ()))

    # -----------------------------------------------------
    # ФАУНА ПОВЕРХНОСТНЫХ БИОМОВ
    # -----------------------------------------------------
    # Состав основан на биомах оригинальной Subnautica. Количества
    # адаптированы под размер этой 2D-карты; небольшие рыбы дополнительно
    # размножаются через schooling/FISH_COUNT_MULTIPLIER.
    SURFACE_FAUNA = {
        "Безопасные отмели": [
            (peeper_type, 110), (bladderfish_type, 38),
            (boomerang_type, 112), (garryfish_type, 56),
            (holefish_type, 17), (spadefish_type, 5),
            (rabbit_ray_type, 4), (gasopod_type, 13),
        ],
        "Водоросли": [
            (peeper_type, 15), (boomerang_type, 4),
            (eyeye_type, 12), (hoopfish_type, 3),
            (hoverfish_type, 5), (rabbit_ray_type, 3),
            (stalker_type, 16), (mesmer_type, 1),
        ],
        "Травянистое плато": [
            (peeper_type, 5), (boomerang_type, 4),
            (hoopfish_type, 4), (reginald_type, 3),
            (spadefish_type, 3), (biter_type, 7),
            (sand_shark_type, 5), (reefback_type, 2),
        ],
        "Грибной лес (запад)": [
            (peeper_type, 4), (spadefish_type, 5),
            (jellyray_type, 4), (boneshark_type, 2),
            (mesmer_type, 1), (reefback_type, 1),
        ],
        "Грибной лес (восток)": [
            (peeper_type, 4), (spadefish_type, 5),
            (jellyray_type, 4), (boneshark_type, 2),
            (ampeel_type, 2), (mesmer_type, 1),
            (reefback_type, 1),
        ],
        "Подводные острова": [
            (peeper_type, 3), (boomerang_type, 4),
            (garryfish_type, 3), (hoopfish_type, 3),
            (spadefish_type, 4), (boneshark_type, 5),
            (reefback_type, 1),
        ],
        "Горы": [
            (peeper_type, 3), (boomerang_type, 3),
            (hoopfish_type, 3), (reginald_type, 3),
            (biter_type, 4), (warper_type, 2),
            (reaper_type, 2), (sea_dragon_type, 41),
        ],
        "Зона Куша": [
            (peeper_type, 3), (boomerang_type, 4),
            (eyeye_type, 4), (hoopfish_type, 4),
            (ampeel_type, 4), (boneshark_type, 5),
            (mesmer_type, 1), (reefback_type, 1),
            (warper_type, 2), (reaper_type, 1),
        ],
        "Бурые водоросли (север)": [
            (spinefish_type, 6), (blighter_type, 4),
            (ampeel_type, 3), (crabsquid_type, 2),
            (warper_type, 2), (ghost_leviathan_type, 1),
        ],
        "Бурые водоросли (юго-запад)": [
            (spinefish_type, 6), (blighter_type, 5),
            (ampeel_type, 4), (crabsquid_type, 1),
            (warper_type, 2),
        ],
        "Редкий риф": [
            (peeper_type, 4), (reginald_type, 5),
            (spadefish_type, 5), (reefback_type, 1),
        ],
        "Морской путь": [
            (peeper_type, 3), (boomerang_type, 3),
            (eyeye_type, 3), (hoopfish_type, 3),
            (reginald_type, 4), (spadefish_type, 4),
            (sea_treader_type, 3), (warper_type, 1),
        ],
        "Большой риф": [
            (peeper_type, 3), (eyeye_type, 3),
            (hoopfish_type, 3), (spadefish_type, 4),
            (jellyray_type, 3), (crabsquid_type, 3),
            (boneshark_type, 2), (mesmer_type, 1),
            (reefback_type, 21), (sea_treader_type, 2),
            (warper_type, 2), (ghost_leviathan_type, 1),
        ],
        "Зона крушения": [
            (peeper_type, 2), (bladderfish_type, 2),
            (boomerang_type, 2), (eyeye_type, 2),
            (holefish_type, 2), (hoverfish_type, 2),
            (rabbit_ray_type, 1), (reginald_type, 2),
            (sand_shark_type, 4), (stalker_type, 3),
            (boneshark_type, 2), (reaper_type, 3),
        ],
        "Дюны": [
            (peeper_type, 3), (spadefish_type, 3),
            (reginald_type, 2), (biter_type, 4),
            (sand_shark_type, 6), (gasopod_type, 2),
            (warper_type, 1), (reaper_type, 2),
        ],
        "Скалистое поле": [
            (boomerang_type, 4), (hoopfish_type, 4),
            (reginald_type, 4), (boneshark_type, 6),
            (mesmer_type, 2), (reefback_type, 2),
        ],
    }

    # Дополнительное уплотнение биомов: больше мелкой рыбы и лёгких хищников.
    dense_fish_additions = {
        "Безопасные отмели": [(hoverfish_type, 18), (eyeye_type, 12), (biter_type, 2)],
        "Водоросли": [(bladderfish_type, 16), (garryfish_type, 15), (holefish_type, 8), (biter_type, 5), (sand_shark_type, 2)],
        "Травянистое плато": [(bladderfish_type, 10), (garryfish_type, 14), (eyeye_type, 12), (hoverfish_type, 10), (stalker_type, 3), (biter_type, 6)],
        "Грибной лес (запад)": [(boomerang_type, 12), (garryfish_type, 12), (hoverfish_type, 9), (hoopfish_type, 8), (biter_type, 4)],
        "Грибной лес (восток)": [(boomerang_type, 12), (garryfish_type, 11), (hoverfish_type, 9), (hoopfish_type, 8), (biter_type, 4)],
        "Подводные острова": [(bladderfish_type, 9), (eyeye_type, 9), (hoverfish_type, 10), (reginald_type, 6), (biter_type, 4), (stalker_type, 2)],
        "Горы": [(bladderfish_type, 8), (garryfish_type, 8), (eyeye_type, 10), (hoverfish_type, 8), (biter_type, 4), (boneshark_type, 2)],
        "Зона Куша": [(bladderfish_type, 10), (garryfish_type, 12), (hoverfish_type, 9), (reginald_type, 6), (biter_type, 5), (sand_shark_type, 2)],
        "Бурые водоросли (север)": [(spinefish_type, 12), (blighter_type, 7), (biter_type, 2)],
        "Бурые водоросли (юго-запад)": [(spinefish_type, 12), (blighter_type, 8), (biter_type, 2)],
        "Редкий риф": [(peeper_type, 10), (boomerang_type, 10), (eyeye_type, 8), (hoverfish_type, 8), (biter_type, 4)],
        "Морской путь": [(bladderfish_type, 8), (garryfish_type, 10), (hoverfish_type, 10), (reginald_type, 8), (biter_type, 4)],
        "Большой риф": [(boomerang_type, 10), (garryfish_type, 10), (eyeye_type, 10), (hoverfish_type, 8), (biter_type, 4), (sand_shark_type, 1)],
        "Зона крушения": [(garryfish_type, 7), (eyeye_type, 6), (hoverfish_type, 6), (biter_type, 5), (stalker_type, 2)],
        "Дюны": [(boomerang_type, 8), (garryfish_type, 8), (hoverfish_type, 6), (eyeye_type, 6), (biter_type, 5), (stalker_type, 1)],
        "Скалистое поле": [(peeper_type, 8), (garryfish_type, 9), (eyeye_type, 7), (hoverfish_type, 7), (biter_type, 4)],
    }

    small_fish_types = {
        peeper_type, bladderfish_type, boomerang_type, garryfish_type,
        holefish_type, hoverfish_type, hoopfish_type, reginald_type,
        spadefish_type, eyeye_type, spinefish_type, blighter_type,
    }
    weak_predator_types = {biter_type, stalker_type, sand_shark_type, boneshark_type}

    for biome_name, fauna in list(SURFACE_FAUNA.items()):
        merged = OrderedDict()
        for animal_type, count in fauna:
            new_count = count
            if animal_type in small_fish_types:
                new_count = max(new_count + 2, int(round(new_count * 1.35)))
            elif animal_type in weak_predator_types:
                new_count = max(new_count + 1, int(round(new_count * 1.20)))
            merged[animal_type] = merged.get(animal_type, 0) + new_count

        for animal_type, add_count in dense_fish_additions.get(biome_name, []):
            merged[animal_type] = merged.get(animal_type, 0) + add_count

        SURFACE_FAUNA[biome_name] = list(merged.items())

    for surface_biome in biomes:
        fauna = SURFACE_FAUNA.get(surface_biome.name)
        if fauna is not None and surface_biome.cave_enabled:
            surface_biome.animals = list(fauna)


    # -----------------------------------------------------
    # ФЛОРА ПОВЕРХНОСТНЫХ БИОМОВ И ПЕЩЕР
    # -----------------------------------------------------
    # Плотности адаптированы под 2D-карту. Названия биомов соответствуют
    # текущей игре. Две зоны «Бурые водоросли» по составу фауны и ресурсов
    # выполняют роль Blood Kelp Zone, поэтому получают Bloodvine/Deep Shroom.
    F = flora_types
    surface_flora_profiles = {
        'Безопасные отмели': [
            (F['acid_mushroom'], 6.0), (F['blue_palm'], 1.4),
            (F['writhing_weed'], 3.0), (F['spotted_reeds'], 1.3),
        ],
        'Водоросли': [
            (F['creepvine'], 5.2), (F['membraintree'], 0.35),
            (F['writhing_weed'], 1.1),
        ],
        'Травянистое плато': [
            (F['blood_grass'], 15.0), (F['acid_mushroom'], 2.2),
            (F['redwort'], 1.2), (F['violet_beau'], 1.0),
            (F['tiger_plant'], 0.55), (F['furled_papyrus'], 0.7),
        ],
        'Грибной лес (запад)': [
            (F['mushroom_tree'], 2.0), (F['acid_mushroom'], 1.6),
            (F['blue_palm'], 0.8), (F['pygmy_fan'], 1.2),
            (F['writhing_weed'], 0.9),
        ],
        'Грибной лес (восток)': [
            (F['mushroom_tree'], 2.0), (F['acid_mushroom'], 1.6),
            (F['pygmy_fan'], 1.2), (F['writhing_weed'], 0.9),
            (F['spotted_reeds'], 0.7),
        ],
        'Подводные острова': [
            (F['redwort'], 1.0), (F['violet_beau'], 0.9),
            (F['spotted_dockleaf'], 0.7), (F['spotted_reeds'], 0.6),
        ],
        'Горы': [
            (F['spotted_reeds'], 1.0), (F['ghost_weed'], 0.22),
            (F['violet_beau'], 0.55),
        ],
        'Зона Куша': [
            (F['bulb_bush'], 5.0), (F['violet_beau'], 1.2),
            (F['pygmy_fan'], 0.8), (F['spotted_dockleaf'], 1.0),
            (F['writhing_weed'], 0.7), (F['spotted_reeds'], 0.7),
            (F['ghost_weed'], 0.10), (F['sea_crown'], 0.05),
        ],
        'Бурые водоросли (север)': [
            (F['bloodvine'], 3.5), (F['bloodroot'], 1.0),
            (F['deep_shroom'], 2.0), (F['ghost_weed'], 1.0),
            (F['gabe_feather'], 0.8), (F['rouge_cradle'], 0.45),
            (F['regress_shell'], 0.45),
        ],
        'Бурые водоросли (юго-запад)': [
            (F['bloodvine'], 3.2), (F['bloodroot'], 1.0),
            (F['deep_shroom'], 2.0), (F['ghost_weed'], 0.9),
            (F['gabe_feather'], 0.7), (F['rouge_cradle'], 0.4),
            (F['regress_shell'], 0.4),
        ],
        'Редкий риф': [
            (F['eye_stalk'], 1.8), (F['tiger_plant'], 0.45),
            (F['spiked_horn_grass'], 0.7), (F['redwort'], 0.7),
            (F['violet_beau'], 0.55), (F['rouge_cradle'], 0.22),
        ],
        'Морской путь': [
            (F['spiked_horn_grass'], 2.2), (F['membraintree'], 0.8),
            (F['violet_beau'], 0.6), (F['gabe_feather'], 0.45),
        ],
        'Большой риф': [
            (F['anchor_pod'], 1.6), (F['membraintree'], 1.6),
            (F['gabe_feather'], 0.4),
        ],
        'Зона крушения': [
            (F['acid_mushroom'], 1.1), (F['spotted_reeds'], 1.1),
            (F['spiked_horn_grass'], 0.25),
        ],
        'Дюны': [
            (F['acid_mushroom'], 1.0), (F['writhing_weed'], 0.8),
            (F['rouge_cradle'], 0.35), (F['regress_shell'], 0.35),
            (F['furled_papyrus'], 0.5), (F['sea_crown'], 0.03),
        ],
        'Скалистое поле': [
            (F['eye_stalk'], 1.0), (F['tiger_plant'], 0.55),
            (F['spotted_reeds'], 0.6),
        ],
    }

    cave_flora_profiles = {
        'Безопасные отмели': [
            (F['acid_mushroom'], 4.0), (F['writhing_weed'], 2.0),
            (F['sulfur_plant'], 1.8), (F['blue_palm'], 0.35),
        ],
        'Водоросли': [
            (F['drooping_stinger'], 1.2), (F['eye_stalk'], 0.8),
            (F['sulfur_plant'], 0.8), (F['membraintree'], 0.25),
        ],
        'Травянистое плато': [
            (F['jellyshroom'], 2.0), (F['rouge_cradle'], 1.8),
            (F['drooping_stinger'], 1.0), (F['tiger_plant'], 0.7),
            (F['acid_mushroom'], 1.2), (F['sea_crown'], 0.12),
            (F['furled_papyrus'], 0.8), (F['regress_shell'], 0.45),
        ],
        'Грибной лес (запад)': [
            (F['writhing_weed'], 1.3), (F['acid_mushroom'], 1.0),
            (F['cave_bush'], 0.35),
        ],
        'Грибной лес (восток)': [
            (F['writhing_weed'], 1.3), (F['acid_mushroom'], 1.0),
            (F['cave_bush'], 0.35),
        ],
        'Подводные острова': [
            (F['drooping_stinger'], 1.0), (F['spotted_dockleaf'], 0.8),
            (F['redwort'], 0.7),
        ],
        'Горы': [
            (F['cave_bush'], 1.4), (F['drooping_stinger'], 0.8),
            (F['eye_stalk'], 1.0), (F['blue_palm'], 0.45),
            (F['spotted_dockleaf'], 0.75), (F['spiked_horn_grass'], 0.65),
            (F['regress_shell'], 0.35),
        ],
        'Зона Куша': [
            (F['spotted_dockleaf'], 1.3), (F['eye_stalk'], 0.18),
            (F['spiked_horn_grass'], 0.65), (F['cave_bush'], 0.45),
        ],
        'Бурые водоросли (север)': [
            (F['bloodroot'], 1.8), (F['bloodvine'], 1.8),
            (F['deep_shroom'], 2.5), (F['ghost_weed'], 1.1),
            (F['rouge_cradle'], 0.8), (F['regress_shell'], 0.7),
        ],
        'Бурые водоросли (юго-запад)': [
            (F['bloodroot'], 1.8), (F['bloodvine'], 1.6),
            (F['deep_shroom'], 2.5), (F['ghost_weed'], 1.0),
            (F['rouge_cradle'], 0.7), (F['regress_shell'], 0.7),
        ],
        'Редкий риф': [
            (F['eye_stalk'], 2.0), (F['regress_shell'], 0.9),
            (F['spiked_horn_grass'], 0.8), (F['tiger_plant'], 0.5),
        ],
        'Морской путь': [
            (F['cave_bush'], 1.5), (F['regress_shell'], 0.8),
            (F['gabe_feather'], 0.7), (F['spiked_horn_grass'], 0.8),
        ],
        'Большой риф': [
            (F['membraintree'], 1.1), (F['anchor_pod'], 0.6),
            (F['cave_bush'], 0.6),
        ],
        'Зона крушения': [
            (F['acid_mushroom'], 1.2), (F['spotted_reeds'], 0.8),
        ],
        'Дюны': [
            (F['drooping_stinger'], 0.8), (F['rouge_cradle'], 0.8),
            (F['regress_shell'], 0.8), (F['furled_papyrus'], 0.8),
            (F['sea_crown'], 0.08),
        ],
        'Скалистое поле': [
            (F['eye_stalk'], 1.1), (F['tiger_plant'], 0.55),
        ],
    }

    for surface_biome in biomes:
        if surface_biome.cave_enabled:
            surface_biome.flora = list(
                surface_flora_profiles.get(surface_biome.name, ())
            )


    # =====================================================
    # ОБЛОМКИ АВРОРЫ
    # =====================================================
    # В оригинале крупные wrecks распределены по конкретным биомам.
    # Наша карта имеет другую геометрию, поэтому исходные X/Z координаты
    # используются для детерминированного относительного размещения внутри
    # соответствующего биома. Так сохраняется правильное распределение:
    # Дюны -> Дюны, Mountains -> Горы, Grassy Plateaus -> Травянистое
    # плато и т. д.

    def find_surface_biome(name):
        for candidate in reversed(biomes):
            if candidate.name == name and candidate.cave_enabled:
                return candidate
        return None

    def wreck_point_in_biome(parent, original_x, original_z, seed):
        cx, cy = parent.center()
        x1, y1, x2, y2 = parent.rect
        rx = max(8.0, (x2 - x1) * 0.40)
        ry = max(8.0, (y2 - y1) * 0.40)

        # Направление берём из исходных координат кратера, а расстояние
        # слегка варьируем по seed. Это не 1:1 проекция, потому что наша
        # карта стилизована под референс, но взаимное расположение внутри
        # нужного биома остаётся стабильным.
        angle = math.atan2(-original_z, original_x)
        rnd = random.Random(seed)
        distance = rnd.uniform(0.28, 0.78)

        px = cx + math.cos(angle) * rx * distance
        py = cy + math.sin(angle) * ry * distance

        for _ in range(40):
            if parent.contains(px, py):
                return int(px), int(py)
            px = (px + cx) / 2.0
            py = (py + cy) / 2.0

        return int(cx), int(cy)

    def add_wreck_piece(name, rect, passable, priority):
        wreck_biome = Biome(
            name,
            AURORA_FLOOR if passable else AURORA_HULL,
            *rect,
            [(titan_type, 2), (quartz_type, 1)] if passable else [],
            [],
            passable=passable,
            cave_enabled=False,
            priority=priority
        )
        wreck_biome.aurora_style = True
        wreck_biome.location_kind = 'aurora_wreck'
        biomes.append(wreck_biome)
        return wreck_biome

    def add_wreck_structure(wreck_id, parent_name,
                            original_x, original_z,
                            large=True):
        parent = find_surface_biome(parent_name)
        if parent is None:
            return

        seed = (
            910000
            + sum(ord(ch) for ch in str(wreck_id)) * 37
            + abs(int(original_x)) * 3
            + abs(int(original_z)) * 5
        )
        cx, cy = wreck_point_in_biome(
            parent, original_x, original_z, seed
        )

        if large:
            width = 14
            height = 10
        else:
            width = 7
            height = 5

        x1 = max(1, cx - width // 2)
        y1 = max(1, cy - height // 2)
        x2 = min(MAP_SIZE - 2, x1 + width - 1)
        y2 = min(MAP_SIZE - 2, y1 + height - 1)

        label = f'Обломок Авроры №{wreck_id}'
        floor = add_wreck_piece(
            label,
            (x1 + 1, y1 + 1, x2 - 1, y2 - 1),
            True, 82 if large else 78
        )
        floor.original_subnautica_xz = (original_x, original_z)
        floor.wreck_id = str(wreck_id)
        floor.parent_surface_biome = parent_name
        # Флаг нужен генератору мира, чтобы отличать именно крупные
        # обломки Авроры от мелких и от основной Авроры.
        floor.is_large_wreck = bool(large)

        # Стены с двумя входами у крупных обломков и одним у мелких.
        door_a = (x1 + x2) // 2
        if door_a - 1 >= x1:
            add_wreck_piece(
                label + ' — северная стенка L',
                (x1, y1, door_a - 1, y1), False, 90
            )
        if door_a + 1 <= x2:
            add_wreck_piece(
                label + ' — северная стенка R',
                (door_a + 1, y1, x2, y1), False, 90
            )

        if large:
            door_b = max(x1 + 1, min(x2 - 1, door_a + 2))
            if door_b - 1 >= x1:
                add_wreck_piece(
                    label + ' — южная стенка L',
                    (x1, y2, door_b - 1, y2), False, 90
                )
            if door_b + 1 <= x2:
                add_wreck_piece(
                    label + ' — южная стенка R',
                    (door_b + 1, y2, x2, y2), False, 90
                )
        else:
            add_wreck_piece(
                label + ' — южная стенка',
                (x1, y2, x2, y2), False, 90
            )

        add_wreck_piece(
            label + ' — левая стенка',
            (x1, y1 + 1, x1, y2 - 1), False, 90
        )
        add_wreck_piece(
            label + ' — правая стенка',
            (x2, y1 + 1, x2, y2 - 1), False, 90
        )

        # Несколько расколотых плит рядом с крупным обломком.
        if large:
            rnd = random.Random(seed + 17)
            for debris_index in range(3):
                dx = rnd.choice((-1, 1)) * rnd.randint(width // 2 + 2, width + 5)
                dy = rnd.randint(-height, height)
                debris_x = max(1, min(MAP_SIZE - 3, cx + dx))
                debris_y = max(1, min(MAP_SIZE - 3, cy + dy))
                if parent.contains(debris_x, debris_y):
                    add_wreck_piece(
                        label + f' — фрагмент {debris_index + 1}',
                        (debris_x, debris_y,
                         debris_x + rnd.randint(1, 3),
                         debris_y + rnd.randint(1, 2)),
                        False, 84
                    )

    # 23 крупных обломка из списка оригинальной игры.
    LARGE_WRECKS = [
        ('1',  'Травянистое плато',  320,   431),
        ('2',  'Травянистое плато', -630,    -2),
        ('3',  'Зона Куша',          910,   600),
        ('4',  'Подводные острова', -128,   884),
        ('5',  'Горы',               701,  1224),
        ('6',  'Дюны',             -1448,   732),
        ('7',  'Морской путь',     -1148,  -706),
        ('8',  'Бурые водоросли (юго-запад)', -1208, -390),
        ('9',  'Грибной лес (запад)', -672, 750),
        ('10', 'Большой риф',       -290,  -773),
        ('11', 'Большой риф',       -865, -1390),
        ('12', 'Травянистое плато', -393,   630),
        ('13', 'Травянистое плато',  -15,  -624),
        ('14', 'Травянистое плато', -418,  -261),
        ('15', 'Безопасные отмели',  -33,  -398),
        ('16', 'Безопасные отмели',  343,  -190),
        ('17', 'Водоросли',           64,   376),
        ('18', 'Водоросли',         -317,   223),
        ('19', 'Горы',              1074,  1335),
        ('20', 'Редкий риф',        -781,  -730),
        ('43', 'Дюны',             -1214,    11),
        ('44', 'Дюны',             -1625,   100),
        ('45', 'Зона Куша',         1319,   567),
    ]

    for wreck_id, parent_name, original_x, original_z in LARGE_WRECKS:
        add_wreck_structure(
            wreck_id, parent_name,
            original_x, original_z,
            large=True
        )

    # 12 мелких обломков: 6 в Безопасных отмелях и 6 на Травянистых плато.
    SMALL_WRECKS = [
        ('S1', 'Безопасные отмели',   20,  300),
        ('S2', 'Безопасные отмели',   90,  120),
        ('S3', 'Безопасные отмели',   65,  -85),
        ('S4', 'Безопасные отмели', -160, -225),
        ('S5', 'Безопасные отмели',  175, -253),
        ('S6', 'Безопасные отмели',  310, -119),
        ('G1', 'Травянистое плато',  165, -520),
        ('G2', 'Травянистое плато',  322,  222),
        ('G3', 'Травянистое плато',  270,   70),
        ('G4', 'Травянистое плато', -370,  475),
        ('G5', 'Травянистое плато', -284,  606),
        ('G6', 'Травянистое плато', -520, -215),
    ]

    for wreck_id, parent_name, original_x, original_z in SMALL_WRECKS:
        add_wreck_structure(
            wreck_id, parent_name,
            original_x, original_z,
            large=False
        )

    # Отдельный небольшой обломок в Зоне крушения, указанный как POI.
    add_wreck_structure(
        'CZ', 'Зона крушения', 527, -43, large=False
    )

    # -----------------------------------------------------
    # РЕЕСТР ВСЕХ ПРЕДМЕТОВ ДЛЯ START_INVENTORY
    # -----------------------------------------------------
    # Часть игровых типов объявлена global, а часть существует только
    # как локальные переменные init_assets(). Сохраняем обе группы,
    # пока локальные ссылки ещё доступны.
    registry = {}

    def register_start_item(variable_name, value):
        if not isinstance(value, (ObjectType, AnimalType)):
            return
        registry.setdefault(value.name, value)
        if variable_name:
            registry.setdefault(variable_name, value)

    for variable_name, value in list(globals().items()):
        register_start_item(variable_name, value)

    for variable_name, value in list(locals().items()):
        register_start_item(variable_name, value)

    # На случай типов, созданных без отдельной локальной переменной,
    # дополнительно собираем предметы из рецептов и биомов.
    for recipe in recipes:
        register_start_item(None, recipe.result)
        for ingredient in recipe.ingredients:
            register_start_item(None, ingredient)

    for biome in biomes:
        for entry in biome.objects:
            if isinstance(entry, (tuple, list)) and entry:
                register_start_item(None, entry[0])
        for entry in biome.animals:
            if isinstance(entry, (tuple, list)) and entry:
                register_start_item(None, entry[0])

    START_ITEM_REGISTRY = registry


# =========================================================
# МИР, ЖИВОТНОЕ, ПЕЩЕРЫ
# =========================================================

class World:

    def __init__(self):
        self.biomes = biomes
        self.object_grid = {}
        self.flora_grid = {}
        self.animals = []
        self.biome_chunks = {}
        self.biome_cache = {}
        self.animal_chunks = {}

        self._build_biome_index()
        self._generate_objects()
        self._generate_animals()
        self._generate_flora()
        self.rebuild_animal_index()

    def _build_biome_index(self):
        chunk = WORLD_CHUNK_SIZE
        max_chunk = (MAP_SIZE - 1) // chunk
        declaration_order = {
            id(biome): index
            for index, biome in enumerate(self.biomes)
        }

        for biome in self.biomes:
            x1, y1, x2, y2 = biome.rect
            cx1 = max(0, x1 // chunk)
            cy1 = max(0, y1 // chunk)
            cx2 = min(max_chunk, x2 // chunk)
            cy2 = min(max_chunk, y2 // chunk)

            for cy in range(cy1, cy2 + 1):
                for cx in range(cx1, cx2 + 1):
                    key = (cx, cy)
                    self.biome_chunks.setdefault(key, []).append(biome)

        # Сначала проверяем наиболее приоритетные биомы. При равном
        # приоритете сохраняем прежнюю семантику: более поздний биом
        # перекрывает более ранний.
        for candidates in self.biome_chunks.values():
            candidates.sort(
                key=lambda biome: (
                    biome.priority, declaration_order[id(biome)]
                ),
                reverse=True
            )

    def get_biome_at(self, x, y):
        x = int(x)
        y = int(y)

        if not (0 <= x < MAP_SIZE and 0 <= y < MAP_SIZE):
            return None

        cache_key = (x, y)
        if cache_key in self.biome_cache:
            return self.biome_cache[cache_key]

        chunk_key = (x // WORLD_CHUNK_SIZE, y // WORLD_CHUNK_SIZE)
        result = None

        for biome in self.biome_chunks.get(chunk_key, ()):
            if biome.contains(x, y):
                result = biome
                break

        if len(self.biome_cache) >= MAX_BIOME_CACHE:
            self.biome_cache.clear()

        self.biome_cache[cache_key] = result
        return result

    def get_object_at(self, x, y):
        return self.object_grid.get((int(x), int(y)))

    def remove_object_at(self, x, y):
        return self.object_grid.pop((int(x), int(y)), None)

    def _generate_objects(self):
        object_grid = self.object_grid

        for biome in self.biomes:
            x1, y1, x2, y2 = biome.rect
            area = biome.area()

            for (object_type, density) in biome.objects:
                count = int((area / 400) * density)

                for _ in range(count):
                    x = random.randint(x1, x2)
                    y = random.randint(y1, y2)
                    key = (x, y)

                    effective_biome = self.get_biome_at(x, y)

                    if (effective_biome is biome
                            and biome.passable
                            and key not in object_grid):
                        object_grid[key] = object_type

        # Один случайный экземпляр оружия на каждые три крупных обломка.
        # Оружие появляется только на свободной клетке внутри пола обломка.
        self._spawn_weapons_in_large_wrecks()

    def _spawn_weapons_in_large_wrecks(self):
        weapon_types = [
            laser_pistol, underwater_rifle, plasma_cannon,
            lang_cannon, schweer_cannon, diamond_cutter,
            flamethrower, golden_pistol,
        ]

        large_wrecks = [
            biome for biome in self.biomes
            if getattr(biome, "is_large_wreck", False)
        ]

        # Используем обычную случайность мира: при новом запуске
        # оружие и конкретный обломок в каждой тройке могут отличаться.
        rng = random

        for group_start in range(0, len(large_wrecks), 3):
            group = large_wrecks[group_start:group_start + 3]
            if len(group) < 3:
                break

            wreck = rng.choice(group)
            weapon = rng.choice(weapon_types)
            x1, y1, x2, y2 = wreck.rect

            candidates = []
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    key = (x, y)
                    if (self.get_biome_at(x, y) is wreck
                            and key not in self.object_grid):
                        candidates.append(key)

            if candidates:
                self.object_grid[rng.choice(candidates)] = weapon

    def _generate_animals(self):
        append = self.animals.append

        for biome in self.biomes:
            for animal_type, count in biome.animals:
                if animal_type.schooling:
                    count = int(count * FISH_COUNT_MULTIPLIER)

                for _ in range(count):
                    spawn = None

                    for _attempt in range(100):
                        x, y = biome.random_point()

                        if self.get_biome_at(int(x), int(y)) is biome:
                            spawn = (x, y)
                            break

                    if spawn is None:
                        continue

                    append(
                        Animal(spawn[0], spawn[1], animal_type, biome)
                    )


    def _generate_flora(self):
        """Детерминированно размещает декоративную флору поверхности."""
        self.flora_grid.clear()

        for biome_index, biome in enumerate(self.biomes):
            if not getattr(biome, 'flora', None):
                continue
            if not biome.passable:
                continue

            area = max(1.0, biome.area())
            for flora_index, (flora_type, density) in enumerate(biome.flora):
                count = int((area / 400.0) * float(density))
                if density > 0 and count <= 0:
                    count = 1
                count = min(count, 2200)

                seed = (
                    310000
                    + biome_index * 10007
                    + flora_index * 379
                    + sum((i + 1) * ord(ch)
                          for i, ch in enumerate(biome.name))
                )
                rnd = random.Random(seed)

                placed = 0
                attempts = 0
                max_attempts = max(40, count * 12)
                while placed < count and attempts < max_attempts:
                    attempts += 1
                    rx, ry = biome.random_point(rnd)
                    x = int(rx)
                    y = int(ry)
                    key = (x, y)

                    if self.get_biome_at(x, y) is not biome:
                        continue
                    if key in self.object_grid or key in self.flora_grid:
                        continue

                    self.flora_grid[key] = flora_type
                    placed += 1

    @staticmethod
    def _animal_chunk_key(x, y):
        return (
            int(x) // ANIMAL_CHUNK_SIZE,
            int(y) // ANIMAL_CHUNK_SIZE
        )

    def rebuild_animal_index(self):
        self.animal_chunks.clear()
        for order, animal in enumerate(self.animals):
            animal.world_order = order
            key = self._animal_chunk_key(animal.x, animal.y)
            self.animal_chunks.setdefault(key, set()).add(animal)

    def get_animals_near(self, x, y, radius):
        """Возвращает животных только из соседних пространственных чанков."""
        chunk = ANIMAL_CHUNK_SIZE
        min_cx = int(math.floor(x - radius)) // chunk
        max_cx = int(math.floor(x + radius)) // chunk
        min_cy = int(math.floor(y - radius)) // chunk
        max_cy = int(math.floor(y + radius)) // chunk

        result = []
        append = result.append

        for cy in range(min_cy, max_cy + 1):
            for cx in range(min_cx, max_cx + 1):
                for animal in self.animal_chunks.get((cx, cy), ()):
                    if (abs(animal.x - x) <= radius
                            and abs(animal.y - y) <= radius):
                        append(animal)

        # Сохраняем исходный порядок списка животных, чтобы порядок
        # атак и отрисовки не менялся из-за разбиения на чанки.
        result.sort(key=lambda animal: animal.world_order)
        return result

    def update_animal_index(self, animal, old_x, old_y):
        old_key = self._animal_chunk_key(old_x, old_y)
        new_key = self._animal_chunk_key(animal.x, animal.y)

        if old_key == new_key:
            return

        old_bucket = self.animal_chunks.get(old_key)
        if old_bucket is not None:
            old_bucket.discard(animal)
            if not old_bucket:
                self.animal_chunks.pop(old_key, None)

        self.animal_chunks.setdefault(new_key, set()).add(animal)

    def remove_animal(self, animal):
        key = self._animal_chunk_key(animal.x, animal.y)
        bucket = self.animal_chunks.get(key)
        if bucket is not None:
            bucket.discard(animal)
            if not bucket:
                self.animal_chunks.pop(key, None)

        try:
            self.animals.remove(animal)
        except ValueError:
            pass


class Animal:

    def __init__(self, x, y, animal_type, home_biome):
        self.x = x
        self.y = y
        self.type = animal_type
        self.home_biome = home_biome

        # Свободное плавание: непрерывный курс с плавными изменениями,
        # а не случайная точка назначения раз в 40–80 кадров.
        self.swim_heading = random.uniform(0.0, math.tau)
        self.cruise_heading = self.swim_heading
        self.swim_phase = random.uniform(0.0, math.tau)
        self.speed_phase = random.uniform(0.0, math.tau)
        self.phase_rate = random.uniform(0.075, 0.135)
        self.swim_turn_sign = random.choice((-1, 1))
        self.fleeing = False
        self.stuck_frames = 0
        self.move_timer = random.randint(28, 75)
        self.dx = math.cos(self.swim_heading) * animal_type.speed
        self.dy = math.sin(self.swim_heading) * animal_type.speed
        self.active = False
        self.rotated_image = None
        self.rotated_glow = None

        self.hp = animal_type.hp
        self.max_hp = animal_type.hp

        self.attack_timer = 0
        self.attack_cooldown = 60

        # Спутники создаются из рыб в инвентаре по H. Обычные животные
        # оставляют эти значения без изменений.
        self.is_companion = False
        self.companion_orbit_angle = random.uniform(0.0, math.tau)
        self.companion_orbit_radius = random.uniform(1.8, 2.7)
        self.companion_target = None
        self.companion_attack_timer = 0
        self.companion_attack_cooldown = 28
        self.companion_state = "свободно плавает"

        # Set on an ordinary predator when a predator companion attacks it.
        # Such a predator fights the pet instead of attacking the diver.
        self.pet_combat_target = None

        self._update_rotation()

    def _update_rotation(self):
        if self.type.image is None:
            return

        if self.dx == 0 and self.dy == 0:
            angle = 0
        elif self.type.fish_style:
            angle = -math.degrees(math.atan2(self.dy, self.dx))
        else:
            angle = math.degrees(
                math.atan2(self.dy, self.dx) + math.pi / 2
            )

        self.visual_angle = angle
        self.rotated_image = self.type.get_rotated(angle)
        self.rotated_glow = self.type.get_rotated_glow(angle)

    @staticmethod
    def _angle_difference(target, current):
        return math.atan2(math.sin(target-current), math.cos(target-current))

    def _can_swim_to(self, x, y, world):
        """Одна проверка для стен, границ, пещер и стартовой капсулы."""
        if not (0 <= x < MAP_SIZE and 0 <= y < MAP_SIZE):
            return False
        cave_lookup = getattr(world, "cave_lookup", None)
        if cave_lookup is not None:
            # В пещере возможен переход в соседний соединённый туннель.
            if cave_lookup(x, y) is None:
                return False
        elif not self.home_biome.contains(x, y):
            return False
        obj = world.get_object_at(int(x), int(y))
        if obj is not None and obj.is_wall:
            return False
        extra_wall = getattr(world, "creature_blocked", None)
        return extra_wall is None or not extra_wall(int(x), int(y))

    def _find_open_heading(self, desired, speed, world):
        """При упоре в препятствие выбираем направление со свободным путём.

        Сканирование проводится ТОЛЬКО при упоре, а не для каждой рыбы
        каждый кадр, поэтому большая популяция не тормозит игру.
        """
        sign = self.swim_turn_sign
        offsets = (0.0, sign*.36, -sign*.36, sign*.72, -sign*.72,
                   sign*1.10, -sign*1.10, sign*1.55, -sign*1.55,
                   sign*2.15, -sign*2.15, math.pi)
        best_angle = None
        best_score = -float("inf")
        for offset in offsets:
            a = desired + offset
            ux, uy = math.cos(a), math.sin(a)
            if not self._can_swim_to(
                    self.x + ux*speed, self.y + uy*speed, world):
                continue
            # Предпочтение направлениям, которые не упрутся тут же снова.
            openness = 0
            for lookahead in (.35, .8, 1.45):
                if self._can_swim_to(
                        self.x + ux*lookahead,
                        self.y + uy*lookahead, world):
                    openness += 1
                else:
                    break
            score = 0.65*math.cos(offset) + 0.65*openness
            if score > best_score:
                best_score = score
                best_angle = a
        return best_angle

    def update(self, player_x, player_y, world):
        self.active = (
            abs(self.x-player_x) <= VIEW_RADIUS
            and abs(self.y-player_y) <= VIEW_RADIUS
        )
        if self.hp <= 0:
            return

        dx_player = player_x-self.x
        dy_player = player_y-self.y
        distance_sq = dx_player*dx_player + dy_player*dy_player

        # Маленькие рыбы НЕ пытаются покинуть экран при виде игрока.
        # Например, Peeper паникует ближе трёх клеток, но после достижения
        # этой дистанции снова свободно плавает (даже если игрок виден).
        flee = (
            self.active and self.type.behavior == "prey"
            and 0.00001 < distance_sq < self.type.fear_distance**2
        )
        if self.fleeing and not flee:
            # Сохраняем курс обычного плавания, а не курс бегства.
            self.move_timer = max(12, self.move_timer)
        self.fleeing = flee

        self.swim_phase += self.phase_rate
        self.speed_phase += .055
        self.move_timer -= 1
        if self.move_timer <= 0:
            # Случайные постепенные повороты, без разворота на 180°.
            self.cruise_heading += random.uniform(-1.10, 1.10)
            self.move_timer = random.randint(30, 85)
            self.phase_rate = random.uniform(.075, .135)

        detection_range = PREDATOR_DETECTION_RANGE_BY_NAME.get(
            self.type.name, PREDATOR_DETECTION_RANGE_DEFAULT
        )
        player_detected = (
            self.active and self.type.behavior == "predator"
            and distance_sq <= detection_range * detection_range
        )

        if flee:
            # Быстрые зигзаги при бегстве + увеличение скорости.
            target_heading = math.atan2(-dy_player, -dx_player)
            target_heading += math.sin(self.swim_phase*1.8) * (
                .10 + .25*self.type.zigzag_strength
            )
        elif player_detected and distance_sq > .01:
            # Хищник начинает преследование только после обнаружения игрока.
            target_heading = math.atan2(dy_player, dx_player)
        else:
            # Одни виды плавают прямо, другие — зигзагами.
            target_heading = (
                self.cruise_heading
                + self.type.zigzag_strength*math.sin(self.swim_phase)
            )

        # Постепенно поворачиваем голову по курсу: без рывков при смене цели.
        max_turn = .48 if flee else (.28 if self.type.behavior == "predator" else .14)
        diff = self._angle_difference(target_heading, self.swim_heading)
        self.swim_heading += max(-max_turn, min(max_turn, diff))

        speed_wave = math.sin(self.speed_phase)
        # Рыбы иногда ускоряются и замедляются даже без угрозы.
        speed_factor = max(.55, 1.0 + self.type.speed_variation*speed_wave)
        if flee:
            speed_factor *= self.type.flee_speed_boost * (
                1.0 + .12*math.sin(self.swim_phase*2.3)
            )
        speed = max(.002, self.type.speed*speed_factor)
        heading = self.swim_heading
        nx = self.x + math.cos(heading)*speed
        ny = self.y + math.sin(heading)*speed

        if not self._can_swim_to(nx, ny, world):
            # Не меняем направление на случайное в стене: ищем реальный
            # путь вдоль края биома или в свободный участок туннеля.
            alternate = self._find_open_heading(target_heading, speed, world)
            if alternate is not None:
                heading = alternate
                nx = self.x + math.cos(heading)*speed
                ny = self.y + math.sin(heading)*speed
                self.swim_heading = heading
                if not flee and self.type.behavior != "predator":
                    self.cruise_heading = heading
                self.move_timer = random.randint(20, 48)
                self.stuck_frames = 0
            else:
                self.stuck_frames += 1
                # На случай появления рыбы внутри построенной игроком
                # стены — редкая аварийная релокация в ближайшую воду.
                if self.stuck_frames >= 12:
                    relocated = False
                    for radius in (.25, .65, 1.15, 2.0):
                        for i in range(16):
                            a = i*math.tau/16.0
                            tx = self.x + math.cos(a)*radius
                            ty = self.y + math.sin(a)*radius
                            if self._can_swim_to(tx, ty, world):
                                self.x, self.y = tx, ty
                                self.swim_heading = a
                                self.cruise_heading = a
                                self.move_timer = 35
                                self.stuck_frames = 0
                                relocated = True
                                break
                        if relocated:
                            break
                self.dx = self.dy = 0.0
                self._update_rotation()
                return
        else:
            self.stuck_frames = 0

        self.x, self.y = nx, ny
        self.dx = math.cos(heading)*speed
        self.dy = math.sin(heading)*speed
        new_visual = (-math.degrees(heading) if self.type.fish_style
                      else math.degrees(heading+math.pi/2))
        # Не пересобираем уже кешированный спрайт при микроповоротах.
        if abs(self._angle_difference(
                math.radians(new_visual),
                math.radians(getattr(self, "visual_angle", 9999.0)))) > .045:
            self._update_rotation()


class CaveWorldProxy:

    def __init__(self, object_grid):
        self.object_grid = object_grid
        self.cave_lookup = None  # Назначается после инициализации игры.

    def get_object_at(self, x, y):
        return self.object_grid.get((int(x), int(y)))

    def remove_object_at(self, x, y):
        return self.object_grid.pop((int(x), int(y)), None)


# =========================================================
# ИГРА
# =========================================================

class NightWaterSpark:
    """Ночной планктон/малёк: только декоративная точка без физики и лута.

    Координаты задаются в клетках мира; крошечные световые ореолы
    формируются уже на экране. Не влияет на спавн полноценных рыб.
    """

    __slots__ = (
        "x", "y", "vx", "vy", "phase", "blink_speed", "wander",
        "jitter", "radius", "color", "fry", "flee_distance", "flee_speed",
    )

    def __init__(self, rng, x, y):
        self.x = float(x)
        self.y = float(y)
        self.fry = rng.random() < NIGHT_FRY_CHANCE
        angle = rng.uniform(0.0, math.tau)
        # Мальки заметно быстрее планктона, но не заменяют настоящих рыб.
        speed = (rng.uniform(0.018, 0.065) if self.fry
                 else rng.uniform(0.002, 0.022))
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.wander = rng.uniform(0.0015, 0.012 if self.fry else 0.006)
        self.phase = rng.uniform(0, math.tau)
        self.blink_speed = rng.uniform(0.06, 0.27)
        self.jitter = rng.uniform(0.30, 1.50 if self.fry else 1.10)
        # Большинство — точки размером 1 px, редкие более крупные.
        roll = rng.random()
        if self.fry:
            self.radius = (rng.uniform(1.65, 2.45) if roll < 0.90
                           else rng.uniform(2.55, 3.25))
        else:
            self.radius = (rng.uniform(0.65, 1.40) if roll < 0.89
                           else rng.uniform(1.45, 2.35))
        palette = (
            (88, 204, 255), (113, 229, 255), (66, 158, 255),
            (155, 240, 255), (79, 195, 242), (58, 147, 239),
            (73, 235, 208), (114, 255, 208), (190, 157, 255),
            (245, 186, 255), (255, 215, 130), (156, 255, 158),
        )
        # Первые шесть (голубые/синие) встречаются чаще остальных.
        self.color = palette[rng.randrange(6) if rng.random() < 0.79
                             else rng.randrange(6, len(palette))]
        if rng.random() < NIGHT_FLEE_CHANCE + (0.10 if self.fry else 0.0):
            # У каждой особи своя дистанция прекращения бегства.
            self.flee_distance = rng.uniform(1.6, 5.7 if self.fry else 3.9)
            self.flee_speed = (rng.uniform(0.065, 0.145) if self.fry
                               else rng.uniform(0.024, 0.065))
        else:
            self.flee_distance = 0.0
            self.flee_speed = 0.0


# =========================================================
# МОБИЛЬНОЕ УПРАВЛЕНИЕ / СОХРАНЕНИЕ ИСХОДНОГО ГЕЙМПЛЕЯ
# Сенсорные события обрабатываются отдельно от клавиатуры и мыши.
# Экран 630 x 630 является игровым, масштабирование делает CSS.
# =========================================================

class MobileControls:
    """Мультисенсорный джойстик и контекстные кнопки Pygame.

    FINGERDOWN/FINGERMOTION/FINGERUP позволяют одновременно держать
    джойстик одним пальцем и стрелять другим. На мобильных браузерах,
    которые транслируют касания только в мышь, работает режим с одним
    указателем; остальные игровые функции по-прежнему доступны.
    """

    JOY_CENTER = (101, 527)
    JOY_RADIUS = 77
    JOY_STICK_LIMIT = 51

    def __init__(self, game):
        self.game = game
        # Все браузерные сборки могут пользоваться экранными кнопками.
        # На ПК по умолчанию остаётся обычная клавиатура/мышь (F9 — показать).
        self.enabled = sys.platform == "emscripten"
        self.joy_pointer = None
        self.joy_value = (0.0, 0.0)
        self.aim_pos = None
        self.more = False
        self.suppress_mouse_until = 0
        self.font = game_font(14, bold=True)
        self.font_small = game_font(12)
        self._last_pointer = None

    @staticmethod
    def _finger_position(event):
        return (max(0, min(SCREEN_SIZE-1, round(event.x * SCREEN_SIZE))),
                max(0, min(SCREEN_SIZE-1, round(event.y * SCREEN_SIZE))))

    def _top_buttons(self):
        return [
            ("inventory", "РЮКЗАК"),
            ("crafting", "КРАФТ"),
            ("map", "КАРТА"),
            ("pets", "ПИТОМЦЫ"),
            ("settings", "НАСТР."),
            ("zoom_out", "−"),
            ("zoom_in", "+"),
        ]

    def _bottom_buttons(self):
        game = self.game
        if game.settings_open:
            return [("back", "НАЗАД")]
        if game.state == "playing":
            if self.more:
                return [
                    ("headlights", "ФАРЫ"), ("destroy", "СЛОМАТЬ"),
                    ("return_menu", "МЕНЮ"),
                    ("inventory", "РЮКЗАК"), ("pets", "ПИТОМЦЫ"),
                    ("zoom_out", "МАСШ−"),
                    ("zoom_in", "МАСШ+"), ("settings", "НАСТР."),
                    ("more", "НАЗАД"),
                ]
            return [
                ("use", "УПОТР."), ("equip", "ЭКИП."),
                ("vehicle", "ТРАНСП."),
                ("pickup", "ПОДНЯТЬ"), ("attack", "УДАР"),
                ("scan", "СКАН"),
                ("build", "СТРОИТЬ"), ("cave", "ПЕЩЕРА"),
                ("more", "ЕЩЁ"),
            ]
        if game.state == "inventory":
            return [
                ("use", "УПОТР."), ("equip", "ЭКИП."),
                ("vehicle", "ТРАНСП."),
                ("drop", "ВЫБРОС"), ("release", "ПИТОМЕЦ"),
                ("back", "ЗАКРЫТЬ"),
            ]
        if game.state == "pets":
            return [
                ("pet_return", "ЗАБРАТЬ"), ("pet_heal", "ЛЕЧИТЬ"),
                ("page_prev", "←"), ("page_next", "→"),
                ("back", "ЗАКРЫТЬ"),
            ]
        if game.state == "crafting":
            return [
                ("station", "СТАНЦИЯ"), ("page_prev", "←"),
                ("page_next", "→"), ("back", "ЗАКРЫТЬ"),
            ]
        if game.state == "planting":
            return [
                ("page_prev", "←"), ("page_next", "→"),
                ("back", "ЗАКРЫТЬ"),
            ]
        if game.state == "map":
            return [
                ("zoom_out", "МАСШ−"), ("zoom_in", "МАСШ+"),
                ("back", "ЗАКРЫТЬ"),
            ]
        return [("back", "ЗАКРЫТЬ")]

    def _buttons(self):
        result = []
        for idx, (action, label) in enumerate(self._top_buttons()):
            result.append((action, label, pygame.Rect(7 + idx*88, 7, 82, 43)))
        items = self._bottom_buttons()
        # Во время игры — матрица 3х3 в правом нижнем углу.
        if self.game.state == "playing" and not self.game.settings_open:
            for idx, (action, label) in enumerate(items):
                col, row = idx % 3, idx // 3
                result.append((action, label,
                               pygame.Rect(353 + col*91, 443 + row*57, 87, 51)))
        else:
            # Контекстные панели не закрывают список инвентаря/крафта/питомцев.
            count = len(items)
            width = 104 if count <= 5 else 96
            gap = 7
            left = (SCREEN_SIZE - (width*count + gap*(count-1)))//2
            for idx, (action, label) in enumerate(items):
                result.append((action, label,
                               pygame.Rect(left + idx*(width+gap), 565, width, 52)))
        return result

    def _joystick_region(self, pos):
        if self.game.state not in ("playing", "map") or self.game.settings_open:
            return False
        return (pos[0] - self.JOY_CENTER[0])**2 + (pos[1] - self.JOY_CENTER[1])**2 < 92**2

    def _move_joystick(self, pos):
        dx = pos[0] - self.JOY_CENTER[0]
        dy = pos[1] - self.JOY_CENTER[1]
        d = math.hypot(dx, dy)
        if d < 8:
            self.joy_value = (0.0, 0.0)
        else:
            strength = min(1.0, d/self.JOY_STICK_LIMIT)
            self.joy_value = (dx/d*strength, dy/d*strength)

    def movement(self):
        return self.joy_value if self.enabled else (0.0, 0.0)

    def _key(self, key):
        # Используем ИСХОДНЫЕ обработчики клавиш, рецептов и питомцев.
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key,
                                             unicode="", mod=0, scancode=0))

    def _action(self, action):
        game = self.game
        keys = {
            "inventory": pygame.K_r, "crafting": pygame.K_i,
            "map": pygame.K_m, "pets": pygame.K_t,
            "settings": pygame.K_n, "vehicle": pygame.K_f,
            "pickup": pygame.K_e, "attack": pygame.K_SPACE,
            "use": pygame.K_u, "equip": pygame.K_q,
            "build": pygame.K_b, "cave": pygame.K_c,
            "destroy": pygame.K_x, "release": pygame.K_h,
            "drop": pygame.K_p, "headlights": pygame.K_l,
            "pet_return": pygame.K_e, "pet_heal": pygame.K_u,
            "station": pygame.K_TAB, "page_prev": pygame.K_LEFT,
            "page_next": pygame.K_RIGHT, "back": pygame.K_ESCAPE,
            "return_menu": pygame.K_ESCAPE,
        }
        if action == "more":
            self.more = not self.more
            return
        if action in ("zoom_in", "zoom_out"):
            step = 1 if action == "zoom_in" else -1
            if game.state == "map":
                game.map_zoom = max(game.map_min_zoom,
                                    min(game.map_max_zoom, game.map_zoom * 1.2**step))
            else:
                game._change_camera_zoom(step)
            return
        if action == "scan":
            if game._is_scanner_selected():
                game.scan_with_scanner()
            else:
                game.open_planting_menu_at_cursor()
            return
        # Переключение на другую панель из текущей: первый такт открывает
        # именно нужную панель, а не просто возвращается к игре.
        if action in ("inventory", "crafting", "map", "settings"):
            target = {"inventory": "inventory", "crafting": "crafting",
                      "map": "map", "settings": "playing"}[action]
            if game.state != "playing" and game.state != target:
                game.state = "playing"
        self._key(keys[action])

    def _tap_content(self, pos):
        game = self.game
        x, y = pos
        # Списки, которые раньше выбирались с клавиатуры (цифры 1–9).
        if game.state == "crafting" and 78 <= y < 550 and 30 <= x <= 595:
            row = (y-82)//52
            if 0 <= row < 9:
                self._key(pygame.K_1 + row)
                return
        elif game.state == "pets" and 127 <= y < 555 and 14 <= x <= 616:
            row = (y-127)//47
            if 0 <= row < 9:
                self._key(pygame.K_1 + row)
                return
        elif game.state == "planting" and 130 <= y < 535 and 105 <= x <= 525:
            row = (y-130)//45
            if 0 <= row < 9:
                self._key(pygame.K_1 + row)
                return
        if game.state == "scanner":
            game.state = "playing"
            game.scanner_target = None
            return
        # Для инвентаря/карты/настроек — родной обработчик попадания мышью.
        # У события есть метка, чтобы оно не перехватывалось второй раз.
        if game.state != "playing" or game.settings_open:
            pygame.event.post(pygame.event.Event(
                pygame.MOUSEBUTTONDOWN, button=1, pos=pos,
                mobile_forwarded=True))
            return
        # Касание игрового мира означает один выстрел в ТУ ТОЧКУ,
        # а не в предыдущую позицию мыши.
        self.aim_pos = pos
        wx, wy = game.screen_to_world(*pos)
        game.mouse_world_x, game.mouse_world_y = wx, wy
        dx, dy = x - SCREEN_SIZE/2, y - SCREEN_SIZE/2
        if dx or dy:
            game.player_angle = math.degrees(math.atan2(dy, dx))
        if game.active_vehicle is not None:
            game.fire_vehicle_torpedo(wx, wy)
        else:
            game.shoot(wx, wy)

    def _down(self, pointer, pos):
        for action, label, rect in self._buttons():
            if rect.collidepoint(pos):
                self._action(action)
                return
        if self._joystick_region(pos) and self.joy_pointer is None:
            self.joy_pointer = pointer
            self._move_joystick(pos)
            return
        self._tap_content(pos)

    def _move(self, pointer, pos):
        if pointer == self.joy_pointer:
            self._move_joystick(pos)

    def _up(self, pointer):
        if pointer == self.joy_pointer:
            self.joy_pointer = None
            self.joy_value = (0.0, 0.0)

    def intercept_event(self, event):
        """Вернуть True, когда событие уже обработано сенсорным контроллером."""
        if getattr(event, "mobile_forwarded", False):
            return False
        fingerdown = getattr(pygame, "FINGERDOWN", -1000)
        fingermotion = getattr(pygame, "FINGERMOTION", -1001)
        fingerup = getattr(pygame, "FINGERUP", -1002)
        if event.type in (fingerdown, fingermotion, fingerup):
            self.enabled = True
            self.suppress_mouse_until = pygame.time.get_ticks() + 320
            pointer = ("finger", getattr(event, "finger_id", 0))
            if event.type == fingerdown:
                self._down(pointer, self._finger_position(event))
            elif event.type == fingermotion:
                self._move(pointer, self._finger_position(event))
            else:
                self._up(pointer)
            return True
        if not self.enabled:
            return False
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            if getattr(event, "button", None) != 1:
                return False
            if pygame.time.get_ticks() < self.suppress_mouse_until:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._down(("mouse", 0), event.pos)
            else:
                self._up(("mouse", 0))
            return True
        if event.type == pygame.MOUSEMOTION:
            if pygame.time.get_ticks() < self.suppress_mouse_until:
                return True
            self._move(("mouse", 0), event.pos)
            if self.joy_pointer is None or self.joy_pointer == ("mouse", 0):
                self.aim_pos = None  # браузер с обычной мышью
            return self.joy_pointer == ("mouse", 0)
        return False

    def draw(self, screen):
        if not self.enabled:
            return
        panel = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA)
        for action, label, rect in self._buttons():
            active = ((action == "inventory" and self.game.state == "inventory")
                      or (action == "crafting" and self.game.state == "crafting")
                      or (action == "map" and self.game.state == "map")
                      or (action == "pets" and self.game.state == "pets"))
            pygame.draw.rect(panel, (5, 23, 38, 172), rect, border_radius=10)
            pygame.draw.rect(panel, (81, 225, 231, 205 if active else 120),
                             rect, 2, border_radius=10)
            font = self.font_small if len(label) > 8 else self.font
            text_surf = font.render(label, True, (230, 250, 252))
            panel.blit(text_surf, text_surf.get_rect(center=rect.center))
        if self.game.state in ("playing", "map") and not self.game.settings_open:
            cx, cy = self.JOY_CENTER
            pygame.draw.circle(panel, (3, 29, 49, 109), (cx, cy), self.JOY_RADIUS)
            pygame.draw.circle(panel, (112, 226, 249, 180), (cx, cy), self.JOY_RADIUS, 3)
            vx, vy = self.joy_value
            knob = (int(cx + vx*self.JOY_STICK_LIMIT),
                    int(cy + vy*self.JOY_STICK_LIMIT))
            pygame.draw.circle(panel, (14, 88, 117, 211), knob, 29)
            pygame.draw.circle(panel, (150, 238, 252, 245), knob, 29, 3)
            hint = self.font_small.render("ДЖОЙСТИК", True, (190, 245, 252))
            panel.blit(hint, hint.get_rect(center=(cx, cy-93)))
        screen.blit(panel, (0, 0))


class Game:

    def __init__(self):
        pygame.init()

        # Логическое игровое поле остаётся 21x21 клетка, как и раньше.
        # pygame.SCALED растягивает весь кадр (клетки, спрайты, текстуры,
        # интерфейс и текст) до высоты физического экрана, а FULLSCREEN
        # переводит игру в настоящий полноэкранный режим.
        self.screen = create_game_display()
        pygame.display.set_caption(
            "2D Subnautica — каноническая фауна и флора"
        )

        self.clock = pygame.time.Clock()

        # Touch controller requires no changes to creature graphics or collision.
        self.mobile_controls = MobileControls(self)

        self.font = game_font(20)
        self.large_font = game_font(32)
        self.small_font = game_font(15)
        self.tiny_font = game_font(13)

        self.screen.fill((8, 18, 30))
        loading = self.large_font.render(
            "Генерация мира...", True, (200, 230, 255)
        )
        self.screen.blit(
            loading,
            loading.get_rect(
                center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2)
            )
        )
        pygame.display.flip()

        init_assets()

        self.player_x = MAP_SIZE // 2
        self.player_y = MAP_SIZE // 2

        self.world = World()

        # -------- СТАРТОВАЯ КАПСУЛА --------
        capsule_x1 = int(self.player_x) - START_CAPSULE_WIDTH // 2
        capsule_y1 = int(self.player_y) - START_CAPSULE_HEIGHT // 2
        capsule_x2 = capsule_x1 + START_CAPSULE_WIDTH - 1
        capsule_y2 = capsule_y1 + START_CAPSULE_HEIGHT - 1

        self.start_capsule_rect = (
            capsule_x1, capsule_y1, capsule_x2, capsule_y2
        )
        self.start_capsule_inner_rect = (
            capsule_x1 + 1, capsule_y1 + 1,
            capsule_x2 - 1, capsule_y2 - 1
        )

        door_y = capsule_y2
        door_x1 = capsule_x1 + START_CAPSULE_WIDTH // 2 - 1
        self.start_capsule_door_cells = {
            (door_x1, door_y),
            (door_x1 + 1, door_y),
        }

        for cy in range(capsule_y1, capsule_y2 + 1):
            for cx in range(capsule_x1, capsule_x2 + 1):
                self.world.object_grid.pop((cx, cy), None)
                self.world.flora_grid.pop((cx, cy), None)

        self.world.animals = [
            animal for animal in self.world.animals
            if not (
                capsule_x1 <= int(animal.x) <= capsule_x2
                and capsule_y1 <= int(animal.y) <= capsule_y2
            )
        ]
        self.world.rebuild_animal_index()
        # Дикие рыбы также учитывают коллизию стартовой капсулы.
        self.world.creature_blocked = self.is_start_capsule_wall

        # -------- ПЕЩЕРЫ --------
        self.in_cave = False
        self.cave_tunnels = []
        self.cave_animals = []
        self.cave_object_grid = {}
        self.cave_flora_grid = {}
        self.cave_world = CaveWorldProxy(self.cave_object_grid)
        self.cave_world.cave_lookup = self.get_cave_tunnel_at
        self.cave_entrances = []
        self.cave_tunnel_chunks = {}
        self.cave_tunnel_cache = {}
        self.surface_cave_entrance_cells = {}
        self.cave_exit_cells = {}
        self._init_caves()

        # Опасные атаки флоры и существ. Координаты всех снарядов — в клетках.
        self.hostile_projectiles = []
        self.gas_pods = []
        self.special_explosions = []
        self.plant_attack_timers = {}
        # Каждое серное растение — убежище для одной рыбы-камикадзе.
        # После взрыва убежище восстанавливает рыбу через 30 секунд реального времени.
        self.crashfish_shelters = {
            (x, y): {"animal": None, "respawn_at": 0}
            for (x, y), flora in self.cave_flora_grid.items()
            if getattr(flora, "kind", "") == "sulfur_plant"
        }

        self.running = True
        self.state = "playing"

        # Настройки графики (N открывает/закрывает панель).
        self.settings_open = False
        self.setting_plankton_enabled = NIGHT_PLANKTON_ENABLED
        self.setting_seabed_details_enabled = True
        self.setting_water_darkening_enabled = True
        self.setting_music_enabled = True
        self.setting_effects_enabled = True
        self._sounds = {}
        self._sound_times = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            music_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "underwater_music.ogg")
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(0.35)
            pygame.mixer.music.play(-1)
            for key, filename in (("spark", "electric_spark.wav"), ("sonar", "sonar_ping.ogg"), ("swim", "swim.ogg")):
                try:
                    self._sounds[key] = pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename))
                except (pygame.error, OSError) as exc:
                    print("Sound unavailable:", filename, exc)
        except (pygame.error, OSError) as exc:
            print("Music unavailable:", exc)

        self.player_hp = 25
        self.max_player_hp = 25

        self.player_attack_damage = 5
        self.player_attack_range = 1.5

        self.max_hunger = 100
        self.max_thirst = 100

        self.player_hunger = self.max_hunger
        self.player_thirst = self.max_thirst

        self.hunger_timer = 0
        self.thirst_timer = 0

        self.equipped_weapon = None
        self.cooldown_animals = set()

        self.mouse_world_x = 0
        self.mouse_world_y = 0
        self.player_angle = 0.0

        self.inventory = [None] * INVENTORY_SIZE
        self.inventory_counts = {}
        self.active_slot_index = -1
        self._stored_companion_hp = {}

        # Заполняем инвентарь из редактируемого блока START_INVENTORY
        # в начале файла. init_assets() уже выполнен, поэтому все типы
        # предметов к этому моменту созданы.
        self._load_start_inventory()

        self.pet_list_page = 0
        # По девять питомцев: каждый выбирается клавишами 1–9.
        self.pets_per_page = 9
        self.selected_pet = None

        # Выброшенные по P предметы хранятся отдельно от object_grid,
        # чтобы ресурс, оружие или строительный предмет не превращался
        # в часть геометрии мира. Для поверхности и пещер — разные слои.
        self.surface_dropped_items = {}
        self.cave_dropped_items = {}

        self.craft_page = 0
        self.craft_station_index = 0
        self.recipes_per_page = 9
        self.max_craft_page = max(
            0, (len(recipes) - 1) // self.recipes_per_page
        )

        self.notification = ""
        self.notification_timer = 0

        self.flashlight_on = False
        self.vehicle_headlights_on = VEHICLE_HEADLIGHTS_DEFAULT
        self.seaglide_on = False
        self.active_flare_timer = 0
        self.speed_boost_timer = 0
        self.damage_resist_timer = 0
        self.damage_vignette_flash = 0
        self.damage_vignette_surface = None
        self.scanner_highlight_timer = 0
        self.scanner_highlight_cells = set()

        # Персональный сканер: исследованные записи и текущая полноэкранная карточка.
        self.scanned_entries = set()
        self.researched_flora = set()
        self.scanner_target = None
        self.scanner_preview_cache = {}

        # Посаженные растения хранятся отдельно от природной flora_grid.
        # Ключ: (слой_пещеры, x, y), значение: список FloraType.
        self.planted_flora = {}
        self.planting_target = None
        self.planting_page = 0
        self.plants_per_page = 9

        self.active_decoys = []
        self.base_effect_tick = 0

        self.diver_sprite = generate_diver_sprite(
            size=CELL_SIZE,
            suit_color=(30, 100, 180),
            accent_color=(255, 200, 50),
            tank_color=(200, 205, 215)
        )

        self.diver_rotated_cache = {}
        self.weapon_rotated_cache = {}
        self.vehicle_rotated_cache = {}
        self.inventory_image_cache = {}

        # -------- УПРАВЛЯЕМЫЙ ТРАНСПОРТ --------
        self.active_vehicle = None
        self.vehicle_max_hp = {
            seamoth_type: 50,
            cyclops_type: 400,
        }
        self.vehicle_hp = dict(self.vehicle_max_hp)
        self.vehicle_wrecks = []
        self.vehicle_torpedoes = []
        self.vehicle_torpedo_cooldown = 0

        self.inventory_overlay = pygame.Surface(
            (SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA
        ).convert_alpha()
        self.inventory_overlay.fill((0, 0, 0, 180))

        self.crafting_overlay = pygame.Surface(
            (SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA
        ).convert_alpha()
        self.crafting_overlay.fill((0, 0, 0, 200))

        # Независимое от карты приближение игрового мира.
        self.camera_zoom = 1.0
        self._render_view_radius = VIEW_RADIUS
        self._render_canvas_size = SCREEN_SIZE
        self._world_render_surface = None
        self._blue_edge_haze = self._make_blue_edge_haze()
        self._night_edge_vignette = self._make_night_edge_vignette()
        self._hd_source_cache = {}
        self._hd_glow_source_cache = {}
        self._hd_sprite_cache = OrderedDict()
        self._hd_floor_cache = OrderedDict()

        self.map_zoom = 1.0
        self.map_min_zoom = 0.3
        self.map_max_zoom = 20.0
        self.map_base_scale = SCREEN_SIZE / MAP_SIZE
        self.map_center_x = self.player_x
        self.map_center_y = self.player_y
        self.selected_biome = None

        self.day_time = 0.30
        self.day_cycle_seconds = 180.0
        self.day_speed = 1.0 / (self.day_cycle_seconds * 60.0)

        # Счётчик игровых суток и восстановление экосистемы.
        # Каждые 4 полностью прошедших игровых дня возвращаем только
        # недостающую часть исходной фауны и ресурсов.
        self.elapsed_game_days = 0.0
        self.ecosystem_refresh_interval_days = 4.0
        self.next_ecosystem_refresh_day = self.ecosystem_refresh_interval_days
        self._capture_ecosystem_targets()

        self.day_overlay = pygame.Surface(
            (SCREEN_SIZE, SCREEN_SIZE)
        ).convert()
        # Отдельный слой с поклеточной/секторной прозрачностью для света.
        self.lighting_overlay = pygame.Surface(
            (SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA
        ).convert_alpha()
        # Генерируем маски только при первом использовании. Слои света
        # вычитают прозрачность чёрной ночной завесы, не выбеляя мир.
        self._radial_light_cache = {}
        self._beam_light_cache = {}
        self._emitter_glow_cache = {}
        self._day_overlay_key = None
        self.frame_count = 0
        # F8 позволяет посмотреть полную полночь, не изменяя хода игры.
        self.force_midnight_preview = False
        self._bio_planted_scaled_cache = {}

        # Планктон живёт только в окне камеры и обновляется независимо от
        # тяжёлой системы животных. Свой RNG сохраняет генерацию мира.
        self._night_rng = random.Random(56021026)
        self._night_sparks = []
        self._night_sparks_visible = 0
        self._night_spark_surface = None

        # Кэш декоративных тайлов дна: позволяет заметно улучшить вид
        # поверхности (морские звёзды, мелкие камни, кораллы, обрастания
        # и вариации тона), не перегружая каждый кадр.
        self._seabed_tile_cache = {}
        self._visual_cell_cache = {}
        self._seabed_theme_cache = {}
        # Кэш пещерных тайлов: отдельные варианты пола и стен с
        # каменными прожилками, мелкими камнями, кристаллами и
        # натёками, чтобы пещеры были такими же живыми, как поверхность.
        self._cave_floor_tile_cache = {}
        self._cave_wall_tile_cache = {}
        self._cave_theme_cache = {}

        pygame.mouse.set_visible(True)

    # =====================================================
    # ВОССТАНОВЛЕНИЕ ЭКОСИСТЕМЫ КАЖДЫЕ 4 ИГРОВЫХ ДНЯ
    # =====================================================

    @staticmethod
    def _increment_target(counter, key, amount=1):
        counter[key] = counter.get(key, 0) + amount

    def _capture_ecosystem_targets(self):
        """Запоминает исходную численность ресурсов и дикой фауны.

        Целевые значения снимаются уже после создания стартовой капсулы и
        пещер, поэтому восстановление не пытается вернуть то, что генератор
        намеренно убрал из стартовой зоны. Питомцы в целевую популяцию не
        входят: приручение существа уменьшает дикую популяцию, и позже
        недостающий дикий экземпляр может восстановиться.
        """
        self.surface_resource_targets = {}
        self.cave_resource_targets = {}
        self.surface_fauna_targets = {}
        self.cave_fauna_targets = {}

        for (x, y), obj in self.world.object_grid.items():
            if (getattr(obj, "is_buildable", False)
                    or getattr(obj, "is_weapon", False)):
                continue
            biome = self.world.get_biome_at(x, y)
            if biome is None:
                continue
            self._increment_target(
                self.surface_resource_targets, (biome, obj)
            )

        for (x, y), obj in self.cave_object_grid.items():
            if getattr(obj, "is_buildable", False):
                continue
            tunnel = self.get_cave_tunnel_at(x, y)
            if tunnel is None:
                continue
            self._increment_target(
                self.cave_resource_targets, (tunnel, obj)
            )

        for animal in self.world.animals:
            if getattr(animal, "is_companion", False):
                continue
            home = getattr(animal, "home_biome", None)
            if home is None:
                continue
            self._increment_target(
                self.surface_fauna_targets, (home, animal.type)
            )

        for animal in self.cave_animals:
            if getattr(animal, "is_companion", False):
                continue
            home = getattr(animal, "home_biome", None)
            if home is None:
                continue
            self._increment_target(
                self.cave_fauna_targets, (home, animal.type)
            )

    def _surface_cell_in_start_capsule(self, x, y):
        x1, y1, x2, y2 = self.start_capsule_rect
        return x1 <= x <= x2 and y1 <= y <= y2

    def _spawn_missing_surface_resource(self, biome, object_type):
        """Пытается разместить один ресурс в случайной точке его биома."""
        for _attempt in range(160):
            rx, ry = biome.random_point()
            x = int(rx)
            y = int(ry)
            key = (x, y)

            if self.world.get_biome_at(x, y) is not biome:
                continue
            if not biome.passable:
                continue
            if self._surface_cell_in_start_capsule(x, y):
                continue
            if key in self.surface_cave_entrance_cells:
                continue
            if self.world.get_object_at(x, y) is not None:
                continue
            if self.surface_dropped_items.get(key):
                continue

            self.world.object_grid[key] = object_type
            return True

        return False

    def _spawn_missing_cave_resource(self, tunnel, object_type):
        """Пытается разместить один ресурс в случайной точке пещерной секции."""
        for _attempt in range(160):
            rx, ry = tunnel.random_point()
            x = int(rx)
            y = int(ry)
            key = (x, y)

            if self.get_cave_tunnel_at(x, y) is not tunnel:
                continue
            if key in self.cave_exit_cells:
                continue
            if key in self.cave_object_grid:
                continue
            if self.cave_dropped_items.get(key):
                continue

            self.cave_object_grid[key] = object_type
            return True

        return False

    def _spawn_missing_surface_animal(self, biome, animal_type):
        """Возвращает одну дикую рыбу/существо в случайную точку биома."""
        for _attempt in range(120):
            x, y = biome.random_point()
            if self.world.get_biome_at(int(x), int(y)) is not biome:
                continue
            if self._surface_cell_in_start_capsule(int(x), int(y)):
                continue

            self.world.animals.append(
                Animal(x, y, animal_type, biome)
            )
            return True

        return False

    def _spawn_missing_cave_animal(self, tunnel, animal_type):
        """Возвращает одно дикое существо в случайную точку пещерной секции."""
        for _attempt in range(120):
            x, y = tunnel.random_point()
            if self.get_cave_tunnel_at(int(x), int(y)) is not tunnel:
                continue

            self.cave_animals.append(
                Animal(x, y, animal_type, tunnel)
            )
            return True

        return False

    def _count_current_surface_resources(self):
        counts = {}

        for (x, y), obj in self.world.object_grid.items():
            if getattr(obj, "is_buildable", False):
                continue
            biome = self.world.get_biome_at(x, y)
            key = (biome, obj)
            if key in self.surface_resource_targets:
                self._increment_target(counts, key)

        # Выброшенный ресурс по-прежнему существует в мире и поэтому не
        # считается исчезнувшим. Предметы, которых не было в исходной
        # популяции ресурсов (оружие, компоненты и т.п.), игнорируются.
        for (x, y), stack in self.surface_dropped_items.items():
            biome = self.world.get_biome_at(x, y)
            for item in stack:
                key = (biome, item)
                if key in self.surface_resource_targets:
                    self._increment_target(counts, key)

        return counts

    def _count_current_cave_resources(self):
        counts = {}

        for (x, y), obj in self.cave_object_grid.items():
            if getattr(obj, "is_buildable", False):
                continue
            tunnel = self.get_cave_tunnel_at(x, y)
            key = (tunnel, obj)
            if key in self.cave_resource_targets:
                self._increment_target(counts, key)

        for (x, y), stack in self.cave_dropped_items.items():
            tunnel = self.get_cave_tunnel_at(x, y)
            for item in stack:
                key = (tunnel, item)
                if key in self.cave_resource_targets:
                    self._increment_target(counts, key)

        return counts

    def _count_current_fauna(self, animals, targets):
        counts = {}
        for animal in animals:
            if getattr(animal, "is_companion", False):
                continue
            home = getattr(animal, "home_biome", None)
            key = (home, animal.type)
            if key in targets:
                self._increment_target(counts, key)
        return counts

    def refresh_ecosystem(self):
        """Восполняет недостающую фауну и ресурсы до стартовых значений."""
        restored_resources = 0
        restored_fauna = 0

        surface_resource_counts = self._count_current_surface_resources()
        cave_resource_counts = self._count_current_cave_resources()

        for (biome, object_type), target_count in (
                self.surface_resource_targets.items()):
            missing = max(
                0,
                target_count - surface_resource_counts.get(
                    (biome, object_type), 0
                )
            )
            for _ in range(missing):
                if self._spawn_missing_surface_resource(biome, object_type):
                    restored_resources += 1

        for (tunnel, object_type), target_count in (
                self.cave_resource_targets.items()):
            missing = max(
                0,
                target_count - cave_resource_counts.get(
                    (tunnel, object_type), 0
                )
            )
            for _ in range(missing):
                if self._spawn_missing_cave_resource(tunnel, object_type):
                    restored_resources += 1

        surface_fauna_counts = self._count_current_fauna(
            self.world.animals, self.surface_fauna_targets
        )
        cave_fauna_counts = self._count_current_fauna(
            self.cave_animals, self.cave_fauna_targets
        )

        surface_added = False
        for (biome, animal_type), target_count in (
                self.surface_fauna_targets.items()):
            missing = max(
                0,
                target_count - surface_fauna_counts.get(
                    (biome, animal_type), 0
                )
            )
            for _ in range(missing):
                if self._spawn_missing_surface_animal(biome, animal_type):
                    restored_fauna += 1
                    surface_added = True

        for (tunnel, animal_type), target_count in (
                self.cave_fauna_targets.items()):
            missing = max(
                0,
                target_count - cave_fauna_counts.get(
                    (tunnel, animal_type), 0
                )
            )
            for _ in range(missing):
                if self._spawn_missing_cave_animal(tunnel, animal_type):
                    restored_fauna += 1

        if surface_added:
            self.world.rebuild_animal_index()

        refresh_day = int(round(self.next_ecosystem_refresh_day))
        if restored_fauna or restored_resources:
            self.notification = (
                f"Обновление экосистемы — день {refresh_day}: "
                f"восстановлено рыб/существ {restored_fauna}, "
                f"ресурсов {restored_resources}"
            )
        else:
            self.notification = (
                f"Обновление экосистемы — день {refresh_day}: "
                "пополнение не требуется"
            )
        self.notification_timer = 240

    # =====================================================
    # КЭШ СПРАЙТОВ
    # =====================================================

    def get_diver_rotated(self, angle):
        angle = quantize_angle(angle)
        image = self.diver_rotated_cache.get(angle)

        if image is None:
            image = pygame.transform.rotate(self.diver_sprite, -angle)
            self.diver_rotated_cache[angle] = image

        return image

    def get_weapon_rotated(self, weapon, angle):
        if weapon is None or weapon.image is None:
            return None

        angle = quantize_angle(angle)
        key = (id(weapon), angle)

        image = self.weapon_rotated_cache.get(key)
        if image is None:
            image = pygame.transform.rotate(weapon.image, -angle)
            self.weapon_rotated_cache[key] = image

        return image

    def get_vehicle_rotated(self, vehicle_type, angle):
        if vehicle_type is None or vehicle_type.image is None:
            return None

        angle = quantize_angle(angle)
        key = (id(vehicle_type), angle)
        image = self.vehicle_rotated_cache.get(key)
        if image is None:
            image = pygame.transform.rotate(vehicle_type.image, -angle)
            self.vehicle_rotated_cache[key] = image
        return image

    def _remove_inventory_items_of_type(self, item_type, amount=1):
        amount = max(0, int(amount))
        if amount == 0:
            return True
        if self.inventory_counts.get(item_type, 0) < amount:
            return False

        remaining = amount
        for index, item in enumerate(self.inventory):
            if remaining <= 0:
                break
            if item is item_type:
                self.inventory[index] = None
                self._stored_companion_hp.pop(index, None)
                if index == self.active_slot_index:
                    self.active_slot_index = -1
                remaining -= 1

        new_count = self.inventory_counts.get(item_type, 0) - amount
        if new_count > 0:
            self.inventory_counts[item_type] = new_count
        else:
            self.inventory_counts.pop(item_type, None)
        return remaining == 0

    def _nearest_vehicle_wreck(self, radius=1.7):
        best = None
        radius_sq = radius * radius
        for wreck in self.vehicle_wrecks:
            if wreck["in_cave"] != self.in_cave:
                continue
            dx = wreck["x"] - self.player_x
            dy = wreck["y"] - self.player_y
            dist_sq = dx * dx + dy * dy
            if dist_sq <= radius_sq and (best is None or dist_sq < best[0]):
                best = (dist_sq, wreck)
        return best[1] if best is not None else None

    def _preferred_inventory_vehicle(self):
        # В окне инвентаря выбранный Мотылёк/Циклоп имеет приоритет.
        if 0 <= self.active_slot_index < len(self.inventory):
            selected = self.inventory[self.active_slot_index]
            if selected in self.vehicle_max_hp:
                return selected

        # Иначе берём первый транспорт по фактическому порядку слотов.
        for item in self.inventory:
            if item in self.vehicle_max_hp:
                return item
        return None

    def handle_vehicle_action(self):
        if self.state not in ("playing", "inventory"):
            return

        # F во время управления — покинуть транспорт. Сам транспорт остаётся
        # предметом в инвентаре и сохраняет текущее HP.
        if self.active_vehicle is not None:
            name = self.active_vehicle.name
            self.active_vehicle = None
            self.state = "playing"
            self.notification = f"Вы покинули: {name}"
            self.notification_timer = 60
            return

        # На месте уничтожения F сначала пытается восстановить обломки.
        wreck = self._nearest_vehicle_wreck()
        if wreck is not None:
            vehicle_type = wreck["type"]
            kits_needed = 2 if vehicle_type is cyclops_type else 1
            kits_have = self.inventory_counts.get(repair_kit, 0)
            if kits_have < kits_needed:
                self.notification = (
                    f"Для ремонта {vehicle_type.name} нужно ремкомплектов: "
                    f"{kits_needed} (есть {kits_have})"
                )
                self.notification_timer = 100
                return

            if not self._remove_inventory_items_of_type(repair_kit, kits_needed):
                return

            if not self.add_to_inventory(vehicle_type):
                # На практике место появляется после расхода ремкомплектов,
                # но на случай нестандартного инвентаря откатываем расход.
                for _ in range(kits_needed):
                    self.add_to_inventory(repair_kit)
                self.notification = "Нет места для восстановленного транспорта"
                self.notification_timer = 90
                return

            self.vehicle_hp[vehicle_type] = self.vehicle_max_hp[vehicle_type]
            self.vehicle_wrecks.remove(wreck)
            self.active_vehicle = vehicle_type
            self.state = "playing"
            self.notification = (
                f"{vehicle_type.name} восстановлен за {kits_needed} "
                f"ремкомплект(а) и снова готов к работе"
            )
            self.notification_timer = 120
            return

        vehicle_type = self._preferred_inventory_vehicle()
        if vehicle_type is None:
            self.notification = "В инвентаре нет Мотылька или Циклопа"
            self.notification_timer = 75
            return

        if self.vehicle_hp.get(vehicle_type, 0) <= 0:
            self.notification = (
                f"{vehicle_type.name} уничтожен. Вернитесь к месту крушения для ремонта"
            )
            self.notification_timer = 90
            return

        self.active_vehicle = vehicle_type
        self.state = "playing"
        self.notification = (
            f"Управление: {vehicle_type.name} | WASD — движение | "
            "ЛКМ — торпеда | F — выйти"
        )
        self.notification_timer = 120

    def vehicle_take_damage(self, damage):
        if self.active_vehicle is None:
            self.player_take_damage(damage)
            return

        vehicle_type = self.active_vehicle
        damage = max(1, int(round(damage)))
        self.vehicle_hp[vehicle_type] = max(
            0, self.vehicle_hp.get(vehicle_type, self.vehicle_max_hp[vehicle_type]) - damage
        )
        hp = self.vehicle_hp[vehicle_type]
        self.notification = f"{vehicle_type.name}: -{damage} HP, осталось {hp}"
        self.notification_timer = 45

        if hp <= 0:
            self._destroy_active_vehicle()

    def _destroy_active_vehicle(self):
        vehicle_type = self.active_vehicle
        if vehicle_type is None:
            return

        self.vehicle_wrecks.append({
            "type": vehicle_type,
            "x": float(self.player_x),
            "y": float(self.player_y),
            "in_cave": bool(self.in_cave),
            "angle": float(self.player_angle),
        })
        self._remove_inventory_items_of_type(vehicle_type, 1)
        self.vehicle_hp[vehicle_type] = 0
        self.active_vehicle = None

        kits_needed = 2 if vehicle_type is cyclops_type else 1
        self.notification = (
            f"{vehicle_type.name} уничтожен! Игрок не получил урона. "
            f"Вернитесь сюда с ремкомплектами: {kits_needed}"
        )
        self.notification_timer = 180

    def fire_vehicle_torpedo(self, target_x, target_y):
        vehicle_type = self.active_vehicle
        if vehicle_type is None or self.state != "playing":
            return
        if self.vehicle_torpedo_cooldown > 0:
            return

        dx = target_x - self.player_x
        dy = target_y - self.player_y
        length = math.hypot(dx, dy)
        if length <= 0.001:
            radians = math.radians(self.player_angle)
            dx, dy = math.cos(radians), math.sin(radians)
        else:
            dx /= length
            dy /= length

        if vehicle_type is cyclops_type:
            speed, damage, cooldown = 0.34, 45, 26
        else:
            speed, damage, cooldown = 0.44, 30, 18

        self.vehicle_torpedoes.append({
            "x": self.player_x + dx * 0.9,
            "y": self.player_y + dy * 0.9,
            "vx": dx * speed,
            "vy": dy * speed,
            "damage": damage,
            "ttl": 85,
            "in_cave": bool(self.in_cave),
        })
        self.vehicle_torpedo_cooldown = cooldown

    def _update_vehicle_torpedoes(self):
        if self.vehicle_torpedo_cooldown > 0:
            self.vehicle_torpedo_cooldown -= 1

        if not self.vehicle_torpedoes:
            return

        survivors = []
        current_animals = self.get_current_animals()
        for torpedo in self.vehicle_torpedoes:
            if torpedo["in_cave"] != self.in_cave:
                continue

            torpedo["x"] += torpedo["vx"]
            torpedo["y"] += torpedo["vy"]
            torpedo["ttl"] -= 1

            if torpedo["ttl"] <= 0:
                continue
            if not (0 <= torpedo["x"] < MAP_SIZE and 0 <= torpedo["y"] < MAP_SIZE):
                continue
            if self.in_cave and not self.cave_is_passable(torpedo["x"], torpedo["y"]):
                continue

            hit = None
            for animal in current_animals:
                if animal.hp <= 0 or getattr(animal, "is_companion", False):
                    continue
                dx = animal.x - torpedo["x"]
                dy = animal.y - torpedo["y"]
                visual_radius = max(0.35, animal.type.size / max(1, CELL_SIZE) * 0.32)
                if dx * dx + dy * dy <= visual_radius * visual_radius:
                    hit = animal
                    break

            if hit is not None:
                hit.hp -= torpedo["damage"]
                self.notification = (
                    f"Торпеда поразила {hit.type.name}: HP {max(0, int(hit.hp))}"
                )
                self.notification_timer = 45
                if hit.hp <= 0:
                    self.handle_animal_death(hit)
                continue

            survivors.append(torpedo)

        self.vehicle_torpedoes = survivors

    def draw_vehicle_wrecks(self, camera_x, camera_y):
        for wreck in self.vehicle_wrecks:
            if wreck["in_cave"] != self.in_cave:
                continue
            sx = int((wreck["x"] - camera_x) * CELL_SIZE + CELL_SIZE // 2)
            sy = int((wreck["y"] - camera_y) * CELL_SIZE + CELL_SIZE // 2)
            if not (-220 <= sx <= self._render_canvas_size + 220 and -220 <= sy <= self._render_canvas_size + 220):
                continue

            image = self.get_vehicle_rotated(wreck["type"], wreck["angle"])
            if image is not None:
                wreck_image = image.copy()
                wreck_image.set_alpha(115)
                self.screen.blit(wreck_image, wreck_image.get_rect(center=(sx, sy)))

            r = 13 if wreck["type"] is seamoth_type else 18
            pygame.draw.circle(self.screen, (190, 45, 35), (sx, sy), r, 2)
            pygame.draw.line(self.screen, (255, 80, 55), (sx-r, sy-r), (sx+r, sy+r), 3)
            pygame.draw.line(self.screen, (255, 80, 55), (sx-r, sy+r), (sx+r, sy-r), 3)

    def draw_vehicle_torpedoes(self, camera_x, camera_y):
        for torpedo in self.vehicle_torpedoes:
            if torpedo["in_cave"] != self.in_cave:
                continue
            sx = int((torpedo["x"] - camera_x) * CELL_SIZE + CELL_SIZE // 2)
            sy = int((torpedo["y"] - camera_y) * CELL_SIZE + CELL_SIZE // 2)
            dx, dy = torpedo["vx"], torpedo["vy"]
            length = max(0.001, math.hypot(dx, dy))
            nx, ny = dx / length, dy / length
            tail = (int(sx - nx * 10), int(sy - ny * 10))
            pygame.draw.line(self.screen, (85, 210, 235), tail, (sx, sy), 5)
            pygame.draw.circle(self.screen, (240, 245, 210), (sx, sy), 3)

    def _draw_hostile_attacks(self, camera_x, camera_y):
        """Рисует иглы, огненные шары, газовые пузырьки и взрывы."""
        now = pygame.time.get_ticks()

        for projectile in self.hostile_projectiles:
            if projectile["in_cave"] != self.in_cave:
                continue
            sx = int((projectile["x"] - camera_x) * CELL_SIZE + CELL_SIZE // 2)
            sy = int((projectile["y"] - camera_y) * CELL_SIZE + CELL_SIZE // 2)
            kind = projectile["kind"]
            if kind == "needle":
                length = max(7, int(CELL_SIZE * 0.28))
                mag = max(0.001, math.hypot(projectile["vx"], projectile["vy"]))
                ux = projectile["vx"] / mag
                uy = projectile["vy"] / mag
                tail = (int(sx - ux * length), int(sy - uy * length))
                pygame.draw.line(self.screen, (55, 75, 35), tail, (sx, sy), 5)
                pygame.draw.line(self.screen, (205, 235, 125), tail, (sx, sy), 2)
                pygame.draw.circle(self.screen, (240, 250, 180), (sx, sy), 2)
            elif kind == "fireball":
                pygame.draw.circle(self.screen, (180, 35, 20), (sx, sy), 10)
                pygame.draw.circle(self.screen, (255, 90, 25), (sx, sy), 7)
                pygame.draw.circle(self.screen, (255, 220, 95), (sx, sy), 3)
            else:
                pygame.draw.circle(self.screen, (45, 115, 65), (sx, sy), 7)
                pygame.draw.circle(self.screen, (155, 225, 120), (sx, sy), 5)
                pygame.draw.circle(self.screen, (215, 250, 165), (sx - 1, sy - 2), 2)

        for pod in self.gas_pods:
            if pod["in_cave"] != self.in_cave:
                continue
            sx = int((pod["x"] - camera_x) * CELL_SIZE + CELL_SIZE // 2)
            sy = int((pod["y"] - camera_y) * CELL_SIZE + CELL_SIZE // 2)
            pulse = 1 + int((math.sin(now * 0.012 + pod["phase"]) + 1) * 1.2)
            pygame.draw.circle(self.screen, (55, 115, 65), (sx, sy), 7 + pulse)
            pygame.draw.circle(self.screen, (145, 210, 115), (sx, sy), 5 + pulse // 2)
            pygame.draw.circle(self.screen, (220, 250, 165), (sx - 1, sy - 2), 2)

        survivors = []
        for effect in self.special_explosions:
            if effect["in_cave"] != self.in_cave:
                survivors.append(effect)
                continue
            if now >= effect["expires_at"]:
                continue
            duration = max(1, effect["expires_at"] - effect["created_at"])
            progress = max(0.0, min(1.0, (now - effect["created_at"]) / duration))
            sx = int((effect["x"] - camera_x) * CELL_SIZE + CELL_SIZE // 2)
            sy = int((effect["y"] - camera_y) * CELL_SIZE + CELL_SIZE // 2)
            max_radius = max(5, int(effect.get("radius", 1.0) * CELL_SIZE))
            radius = max(3, int(max_radius * (0.35 + 0.65 * progress)))
            if effect["kind"] in ("crashfish", "fireball"):
                pygame.draw.circle(self.screen, (170, 40, 20), (sx, sy), radius)
                pygame.draw.circle(self.screen, (255, 120, 35), (sx, sy), max(2, radius * 2 // 3))
                pygame.draw.circle(self.screen, (255, 230, 120), (sx, sy), max(2, radius // 3))
            else:
                pygame.draw.circle(self.screen, (100, 190, 85), (sx, sy), radius, 3)
                pygame.draw.circle(self.screen, (185, 235, 125), (sx, sy), max(2, radius // 2), 2)
            survivors.append(effect)
        self.special_explosions = survivors

    def get_inventory_image(self, item):
        if item.image is None:
            return None

        key = id(item)
        cached = self.inventory_image_cache.get(key)
        if cached is not None:
            return cached

        image = item.image
        max_size = SLOT_SIZE - 6

        scale = min(
            max_size / image.get_width(),
            max_size / image.get_height(),
            1.0
        )

        if scale < 1.0:
            width = max(1, int(image.get_width() * scale))
            height = max(1, int(image.get_height() * scale))
            image = pygame.transform.smoothscale(image, (width, height))

        self.inventory_image_cache[key] = image
        return image

    # =====================================================
    # ПЕЩЕРЫ
    # =====================================================

    @staticmethod
    def _move_point_inside_biome(biome, x, y, target_x, target_y):
        """Pull a point towards the biome center until it is inside."""
        for _ in range(30):
            if biome.contains(x, y):
                return x, y

            x = (x + target_x) / 2.0
            y = (y + target_y) / 2.0

        return target_x, target_y

    def _find_cave_entrance_point(self, biome, angle, inset=18):
        cx, cy = biome.center()
        dx = math.cos(angle)
        dy = math.sin(angle)

        x1, y1, x2, y2 = biome.rect
        max_distance = max(x2 - x1, y2 - y1) * 0.8 + 30

        last_x = cx
        last_y = cy
        distance = 0.0

        while distance <= max_distance:
            px = cx + dx * distance
            py = cy + dy * distance

            if not biome.contains(px, py):
                break

            last_x = px
            last_y = py
            distance += 2.0

        last_x -= dx * inset
        last_y -= dy * inset

        return self._move_point_inside_biome(
            biome, last_x, last_y, cx, cy
        )

    def _init_caves(self):
        """Создаёт единую связанную подземную сеть.

        Каждый поверхностный биом получает:
        - один крупный центральный зал;
        - три независимых выхода на поверхность;
        - три боковых зала;
        - локальные коридоры между ними.

        После этого центральные залы всех биомов соединяются минимальным
        остовным деревом и дополнительными перемычками. Поэтому из любой
        пещеры можно под землёй добраться до любой другой, а у каждого
        локального узла существенно больше двух направлений движения.
        """
        self.cave_tunnels = []
        self.cave_entrances = []
        self.cave_object_grid.clear()
        self.cave_flora_grid.clear()
        self.cave_animals = []
        self.cave_hubs = []
        self.cave_connections = []
        self.cave_tunnel_chunks.clear()
        self.cave_tunnel_cache.clear()
        self.surface_cave_entrance_cells.clear()
        self.cave_exit_cells.clear()

        surface_biomes = [
            biome
            for biome in self.world.biomes
            if biome.cave_enabled
        ]

        # -------------------------------------------------
        # ЛОКАЛЬНЫЕ СЕТИ: 3 ВЫХОДА + 3 ВЕТКИ НА БИОМ
        # -------------------------------------------------
        for biome_index, parent in enumerate(surface_biomes):
            seed = (
                5000
                + biome_index * 7919
                + sum(
                    (i + 1) * ord(ch)
                    for i, ch in enumerate(parent.name)
                )
            )
            rnd = random.Random(seed)

            cx, cy = parent.center()
            x1, y1, x2, y2 = parent.rect
            biome_w = max(20, x2 - x1)
            biome_h = max(20, y2 - y1)
            min_size = min(biome_w, biome_h)

            cave_color = (
                max(15, parent.color[0] // 3),
                max(18, parent.color[1] // 3),
                max(24, parent.color[2] // 3)
            )
            deep_color = (
                max(10, cave_color[0] - 8),
                max(12, cave_color[1] - 8),
                max(18, cave_color[2] - 8)
            )

            # Центральный зал — главный развилочный узел.
            hub_rx = max(15, min(30, biome_w * 0.105))
            hub_ry = max(14, min(28, biome_h * 0.105))
            hub_poly = make_blob_points(
                cx, cy,
                hub_rx, hub_ry,
                seed + 99,
                point_count=18,
                jitter=0.10
            )

            cave_resources = [(rock_type, 3)]
            for resource, density in parent.objects:
                if resource in (seaweed_type, sand_type):
                    continue
                cave_resources.append(
                    (resource, max(1, density // 2))
                )
                if len(cave_resources) >= 6:
                    break

            # На карте нет отдельных Inactive/Active Lava Zone, поэтому
            # кианит появляется только в глубоких пещерах наиболее
            # опасных регионов, а не на поверхности.
            if parent.name in (
                    "Большой риф", "Горы",
                    "Бурые водоросли (север)"):
                cave_resources.append((kyanite_type, 1))

            hub = Biome(
                f'{parent.name}: центральный пещерный узел',
                deep_color,
                0, 0, 0, 0,
                cave_resources,
                [],
                polygon=hub_poly,
                clip_biome=parent,
                priority=5
            )
            hub.parent_surface_biome = parent
            hub.cave_kind = 'hub'
            self.cave_tunnels.append(hub)

            hub_record = {
                'biome': parent,
                'hub': hub,
                'point': (cx, cy),
                'color': cave_color,
                'deep_color': deep_color,
                'seed': seed,
            }
            self.cave_hubs.append(hub_record)

            tunnel_width = max(
                8,
                min(15, min_size * 0.065)
            )

            # Три выхода расположены приблизительно через 120 градусов.
            entrance_base_angle = rnd.uniform(0, math.tau)
            for entrance_index in range(3):
                entrance_angle = (
                    entrance_base_angle
                    + entrance_index * (math.tau / 3.0)
                    + rnd.uniform(-0.16, 0.16)
                )

                entrance_x, entrance_y = self._find_cave_entrance_point(
                    parent,
                    entrance_angle,
                    inset=max(10, int(tunnel_width * 1.7))
                )
                entrance_x = int(entrance_x)
                entrance_y = int(entrance_y)

                # Направление внутрь к центральному залу.
                inward_x = cx - entrance_x
                inward_y = cy - entrance_y
                inward_len = math.hypot(inward_x, inward_y)
                if inward_len <= 0.001:
                    inward_x = 1.0
                    inward_y = 0.0
                    inward_len = 1.0
                inward_x /= inward_len
                inward_y /= inward_len

                spawn_x = entrance_x + inward_x * max(5, tunnel_width * 0.8)
                spawn_y = entrance_y + inward_y * max(5, tunnel_width * 0.8)
                spawn_x, spawn_y = self._move_point_inside_biome(
                    parent, spawn_x, spawn_y, cx, cy
                )

                self.cave_entrances.append({
                    'name': (
                        f'{parent.name}: выход {entrance_index + 1}'
                    ),
                    'surface_rect': (
                        entrance_x, entrance_y,
                        entrance_x, entrance_y
                    ),
                    'cave_rect': (
                        entrance_x, entrance_y,
                        entrance_x, entrance_y
                    ),
                    'cave_spawn': (
                        spawn_x + 0.5,
                        spawn_y + 0.5
                    ),
                    'surface_spawn': (
                        entrance_x + 0.5,
                        entrance_y + 0.5
                    ),
                    'parent_biome': parent,
                })
                self.world.object_grid.pop(
                    (entrance_x, entrance_y), None
                )
                self.world.flora_grid.pop(
                    (entrance_x, entrance_y), None
                )

                # Через промежуточную точку коридор получается менее прямым.
                side = (-1 if entrance_index % 2 else 1)
                perp_x = -inward_y
                perp_y = inward_x
                bend = min_size * rnd.uniform(0.04, 0.10) * side
                mid_x = entrance_x + (cx - entrance_x) * 0.48 + perp_x * bend
                mid_y = entrance_y + (cy - entrance_y) * 0.48 + perp_y * bend
                mid_x, mid_y = self._move_point_inside_biome(
                    parent, mid_x, mid_y, cx, cy
                )

                for segment_index, (a, b) in enumerate((
                    ((entrance_x, entrance_y), (mid_x, mid_y)),
                    ((mid_x, mid_y), (cx, cy)),
                )):
                    corridor_poly = make_corridor_polygon(
                        a[0], a[1], b[0], b[1], tunnel_width
                    )
                    corridor = Biome(
                        (
                            f'{parent.name}: выходной тоннель '
                            f'{entrance_index + 1}.{segment_index + 1}'
                        ),
                        cave_color,
                        0, 0, 0, 0,
                        [(rock_type, 2)],
                        [],
                        polygon=corridor_poly,
                        clip_biome=parent,
                        priority=2
                    )
                    corridor.parent_surface_biome = parent
                    corridor.cave_kind = 'local_corridor'
                    self.cave_tunnels.append(corridor)

            # Три боковых зала дают дополнительные тупики/кольцевые ветви.
            branch_base_angle = entrance_base_angle + math.pi / 3.0
            branch_points = []
            branch_radius = min_size * 0.24

            for branch_index in range(3):
                branch_angle = (
                    branch_base_angle
                    + branch_index * (math.tau / 3.0)
                    + rnd.uniform(-0.18, 0.18)
                )
                bx = cx + math.cos(branch_angle) * branch_radius
                by = cy + math.sin(branch_angle) * branch_radius
                bx, by = self._move_point_inside_biome(
                    parent, bx, by, cx, cy
                )
                branch_points.append((bx, by))

                room_rx = max(9, min(20, hub_rx * 0.70))
                room_ry = max(8, min(18, hub_ry * 0.70))
                branch_poly = make_blob_points(
                    bx, by,
                    room_rx, room_ry,
                    seed + 300 + branch_index * 17,
                    point_count=14,
                    jitter=0.13
                )
                branch_room = Biome(
                    f'{parent.name}: боковой зал {branch_index + 1}',
                    deep_color,
                    0, 0, 0, 0,
                    cave_resources[:4],
                    [],
                    polygon=branch_poly,
                    clip_biome=parent,
                    priority=4
                )
                branch_room.parent_surface_biome = parent
                branch_room.cave_kind = 'branch_room'
                self.cave_tunnels.append(branch_room)

                branch_corridor = Biome(
                    f'{parent.name}: ответвление {branch_index + 1}',
                    cave_color,
                    0, 0, 0, 0,
                    [(rock_type, 2)],
                    [],
                    polygon=make_corridor_polygon(
                        cx, cy, bx, by,
                        max(7, tunnel_width * 0.80)
                    ),
                    clip_biome=parent,
                    priority=2
                )
                branch_corridor.parent_surface_biome = parent
                branch_corridor.cave_kind = 'branch_corridor'
                self.cave_tunnels.append(branch_corridor)

            # Соединяем боковые залы между собой треугольником — внутри
            # каждого биома получается не дерево, а сеть с альтернативными
            # маршрутами.
            for branch_index in range(3):
                a = branch_points[branch_index]
                b = branch_points[(branch_index + 1) % 3]
                loop_corridor = Biome(
                    f'{parent.name}: кольцевой тоннель {branch_index + 1}',
                    cave_color,
                    0, 0, 0, 0,
                    [(rock_type, 1)],
                    [],
                    polygon=make_corridor_polygon(
                        a[0], a[1], b[0], b[1],
                        max(6, tunnel_width * 0.62)
                    ),
                    clip_biome=parent,
                    priority=1
                )
                loop_corridor.parent_surface_biome = parent
                loop_corridor.cave_kind = 'local_loop'
                self.cave_tunnels.append(loop_corridor)

        # -------------------------------------------------
        # ЕДИНАЯ СЕТЬ МЕЖДУ БИОМАМИ
        # -------------------------------------------------
        # Сначала строим минимальное остовное дерево по расстоянию между
        # центральными залами. Это математически гарантирует связность.
        if self.cave_hubs:
            connected = {0}
            global_edges = set()

            while len(connected) < len(self.cave_hubs):
                best = None
                best_distance = None

                for i in connected:
                    ax, ay = self.cave_hubs[i]['point']
                    for j in range(len(self.cave_hubs)):
                        if j in connected:
                            continue
                        bx, by = self.cave_hubs[j]['point']
                        distance = (ax - bx) ** 2 + (ay - by) ** 2
                        if best_distance is None or distance < best_distance:
                            best_distance = distance
                            best = (i, j)

                if best is None:
                    break

                i, j = best
                global_edges.add(tuple(sorted((i, j))))
                connected.add(j)

            # Дополнительные перемычки: каждому узлу добавляем до двух
            # ближайших соседей. Сеть получает циклы и множество маршрутов.
            for i, hub_record in enumerate(self.cave_hubs):
                ax, ay = hub_record['point']
                candidates = []
                for j, other in enumerate(self.cave_hubs):
                    if i == j:
                        continue
                    bx, by = other['point']
                    distance = (ax - bx) ** 2 + (ay - by) ** 2
                    candidates.append((distance, j))
                candidates.sort()

                for _, j in candidates[:2]:
                    global_edges.add(tuple(sorted((i, j))))

            # Рисуем межбиомные тоннели. Они не имеют clip_biome, потому
            # что находятся на отдельном подземном уровне и могут пересекать
            # границы поверхностных биомов.
            for edge_index, (i, j) in enumerate(sorted(global_edges)):
                hub_a = self.cave_hubs[i]
                hub_b = self.cave_hubs[j]
                ax, ay = hub_a['point']
                bx, by = hub_b['point']

                link_width = 8
                link_color = (18, 62, 70)

                link = Biome(
                    (
                        f'Межбиомный тоннель: '
                        f'{hub_a["biome"].name} ↔ {hub_b["biome"].name}'
                    ),
                    link_color,
                    0, 0, 0, 0,
                    [(rock_type, 2), (quartz_type, 1)],
                    [],
                    polygon=make_corridor_polygon(
                        ax, ay, bx, by, link_width
                    ),
                    clip_biome=None,
                    priority=1
                )
                link.cave_kind = 'interbiome_corridor'
                self.cave_tunnels.append(link)
                self.cave_connections.append((i, j))

                # Малый узел в середине длинных переходов облегчает
                # навигацию и визуально разбивает прямой коридор.
                distance = math.hypot(bx - ax, by - ay)
                if distance > 170:
                    mx = (ax + bx) / 2.0
                    my = (ay + by) / 2.0
                    junction = Biome(
                        f'Межбиомная развилка {edge_index + 1}',
                        (15, 48, 58),
                        0, 0, 0, 0,
                        [(rock_type, 2), (quartz_type, 2)],
                        [],
                        polygon=make_blob_points(
                            mx, my, 13, 11,
                            88000 + edge_index,
                            point_count=14,
                            jitter=0.10
                        ),
                        clip_biome=None,
                        priority=3
                    )
                    junction.cave_kind = 'interbiome_junction'
                    self.cave_tunnels.append(junction)


        # -------------------------------------------------
        # ФЛОРА ПЕЩЕРНЫХ СЕКЦИЙ
        # -------------------------------------------------
        # Центральные/боковые залы получают полную плотность, локальные
        # коридоры — пониженную. Межбиомные соединительные тоннели остаются
        # почти голыми, чтобы навигация сохранялась читаемой.
        for tunnel in self.cave_tunnels:
            override = CAVE_TUNNEL_ECOSYSTEM_OVERRIDES.get(
                tunnel.name, {}
            )
            # Персональный профиль имеет приоритет над профилем биома.
            # Это также позволяет настраивать межбиомные тоннели без parent.
            if 'flora' in override:
                custom_flora = []
                for flora_key, density in override.get('flora', {}).items():
                    flora_type = flora_types.get(flora_key)
                    try:
                        density = float(density)
                    except (TypeError, ValueError):
                        continue
                    if flora_type is not None and density > 0:
                        custom_flora.append((flora_type, density))
                tunnel.flora = custom_flora
                continue

            parent = getattr(tunnel, 'parent_surface_biome', None)
            if parent is None:
                tunnel.flora = []
                continue

            profile = cave_flora_profiles.get(parent.name, ())
            kind = getattr(tunnel, 'cave_kind', '')
            if kind in ('hub', 'branch_room'):
                scale = 1.0
            elif kind in ('local_corridor', 'branch_corridor', 'local_loop'):
                scale = 0.38
            elif kind == 'interbiome_corridor':
                scale = 0.16
            elif kind == 'interbiome_junction':
                scale = 0.30
            else:
                scale = 0.0

            tunnel.flora = [
                (flora_type, density * scale)
                for flora_type, density in profile
                if density * scale > 0
            ]

        # Индексы строятся после формирования всей геометрии тоннелей.
        # Это резко сокращает число polygon-проверок и не меняет форму
        # ни одной пещеры.
        self._build_cave_spatial_index()
        self._build_cave_entrance_index()

        # -------------------------------------------------
        # РЕСУРСЫ ПЕЩЕР
        # -------------------------------------------------
        cave_exit_cells = set()
        for entrance in self.cave_entrances:
            ex1, ey1, ex2, ey2 = entrance['cave_rect']
            for ey in range(ey1, ey2 + 1):
                for ex in range(ex1, ex2 + 1):
                    cave_exit_cells.add((ex, ey))

        for tunnel_index, tunnel in enumerate(self.cave_tunnels):
            rnd = random.Random(70000 + tunnel_index * 101)
            area = max(1, tunnel.area())

            for object_type, density in tunnel.objects:
                count = int((area / 400) * density)
                # Длинные соединительные коридоры не должны быть забиты
                # сотнями камней.
                if getattr(tunnel, 'cave_kind', '') == 'interbiome_corridor':
                    count = min(count, 12)

                for _ in range(count):
                    for _attempt in range(50):
                        rx, ry = tunnel.random_point(rnd)
                        x = int(rx)
                        y = int(ry)
                        key = (x, y)

                        if key in cave_exit_cells:
                            continue
                        if key in self.cave_object_grid:
                            continue
                        if self.get_cave_tunnel_at(x, y) is not tunnel:
                            continue

                        self.cave_object_grid[key] = object_type
                        break


        # -------------------------------------------------
        # ДЕКОРАТИВНАЯ ФЛОРА ПЕЩЕР
        # -------------------------------------------------
        for tunnel_index, tunnel in enumerate(self.cave_tunnels):
            if not getattr(tunnel, 'flora', None):
                continue

            area = max(1.0, tunnel.area())
            for flora_index, (flora_type, density) in enumerate(tunnel.flora):
                count = int((area / 400.0) * float(density))
                if density > 0 and count <= 0 and area >= 80:
                    count = 1
                count = min(count, 420)

                rnd = random.Random(
                    470000 + tunnel_index * 6151 + flora_index * 487
                )
                placed = 0
                attempts = 0
                max_attempts = max(30, count * 14)

                while placed < count and attempts < max_attempts:
                    attempts += 1
                    rx, ry = tunnel.random_point(rnd)
                    x = int(rx)
                    y = int(ry)
                    key = (x, y)

                    if key in cave_exit_cells:
                        continue
                    if key in self.cave_object_grid:
                        continue
                    if key in self.cave_flora_grid:
                        continue
                    if self.get_cave_tunnel_at(x, y) is not tunnel:
                        continue

                    self.cave_flora_grid[key] = flora_type
                    placed += 1

        # -------------------------------------------------
        # ФАУНА ПЕЩЕР
        # -------------------------------------------------
        # Пещерная геометрия остаётся прежней. Животные появляются только
        # в центральных и боковых залах, поэтому не перекрывают узкие
        # соединительные коридоры и выходы.
        cave_fauna_by_parent = {
            "Безопасные отмели": [
                (bladderfish_type, 32), (crabsnake_type, 1),
            ],
            "Водоросли": [
                (ghost_leviathan_type, 2), (eyeye_type, 2),
            ],
            "Травянистое плато": [
                (oculus_type, 5), (crabsnake_type, 4),
                (biter_type, 2),
            ],
            "Грибной лес (запад)": [
                (spadefish_type, 4), (jellyray_type, 2),
                (holefish_type, 2),
            ],
            "Грибной лес (восток)": [
                (spadefish_type, 4), (jellyray_type, 2),
                (holefish_type, 2),
            ],
            "Подводные острова": [
                (boneshark_type, 2), (hoopfish_type, 3),
            ],
            "Горы": [
                (reginald_type, 4), (biter_type, 2),
                (warper_type, 1),
            ],
            "Зона Куша": [
                (mesmer_type, 2), (boneshark_type, 2),
                (eyeye_type, 2),
            ],
            "Бурые водоросли (север)": [
                (spinefish_type, 5), (blighter_type, 3),
                (crabsquid_type, 1),
            ],
            "Бурые водоросли (юго-запад)": [
                (spinefish_type, 5), (blighter_type, 3),
                (crabsquid_type, 1),
            ],
            "Редкий риф": [
                (reginald_type, 3), (spadefish_type, 3),
                (crabsquid_type, 4)
            ],
            "Морской путь": [
                (spadefish_type, 3), (reginald_type, 2),
            ],
            "Большой риф": [
                (crabsquid_type, 3), (jellyray_type, 3),
                (reginald_type, 3), (warper_type, 1),
            ],
            "Зона крушения": [
                (crashfish_type, 2), (biter_type, 2),
                (boneshark_type, 1),
            ],
            "Дюны": [
                (biter_type, 6), (sand_shark_type, 1),
            ],
            "Скалистое поле": [
                (boneshark_type, 2), (mesmer_type, 1),
            ],
        }

        cave_rooms_by_parent = {}
        for tunnel in self.cave_tunnels:
            parent = getattr(tunnel, 'parent_surface_biome', None)
            if parent is None:
                continue
            if getattr(tunnel, 'cave_kind', '') not in ('hub', 'branch_room'):
                continue
            cave_rooms_by_parent.setdefault(parent.name, []).append(tunnel)

        for parent_name, species in cave_fauna_by_parent.items():
            rooms = cave_rooms_by_parent.get(parent_name, ())
            if not rooms:
                continue

            seed = 99000 + sum((i + 1) * ord(ch)
                               for i, ch in enumerate(parent_name))
            rnd = random.Random(seed)

            for species_index, (animal_type, total_count) in enumerate(species):
                for spawn_index in range(total_count):
                    room = rooms[(spawn_index + species_index) % len(rooms)]
                    spawn = None

                    for _attempt in range(40):
                        x, y = room.random_point(rnd)
                        if self.get_cave_tunnel_at(int(x), int(y)) is room:
                            spawn = (x, y)
                            break

                    if spawn is not None:
                        self.cave_animals.append(
                            Animal(spawn[0], spawn[1], animal_type, room)
                        )

        # Рыба живёт НЕ только в больших залах: каждый туннель и каждый
        # межбиомный переход получает небольшую популяцию мелкой рыбы.
        # Если tunnel.name есть в CAVE_TUNNEL_ECOSYSTEM_OVERRIDES и там
        # задан ключ "fauna", стандартное заселение для него пропускается.
        default_fish_by_parent = {
            "Безопасные отмели": bladderfish_type,
            "Водоросли": peeper_type,
            "Травянистое плато": oculus_type,
            "Грибной лес (запад)": spadefish_type,
            "Грибной лес (восток)": spadefish_type,
            "Подводные острова": hoopfish_type,
            "Горы": reginald_type,
            "Зона Куша": eyeye_type,
            "Бурые водоросли (север)": spinefish_type,
            "Бурые водоросли (юго-запад)": spinefish_type,
            "Редкий риф": reginald_type,
            "Морской путь": spadefish_type,
            "Большой риф": reginald_type,
            "Зона крушения": hoverfish_type,
            "Дюны": boomerang_type,
            "Скалистое поле": peeper_type,
        }
        for tunnel_index, tunnel in enumerate(self.cave_tunnels):
            override = CAVE_TUNNEL_ECOSYSTEM_OVERRIDES.get(
                tunnel.name, {}
            )
            if 'fauna' in override:
                continue

            parent = getattr(tunnel, 'parent_surface_biome', None)
            fish_type = default_fish_by_parent.get(
                getattr(parent, 'name', None)
            )
            if fish_type is None:
                # Межбиомные коридоры также населены. Чередуем виды,
                # чтобы длинные переходы не выглядели одинаковыми.
                fish_type = (
                    peeper_type, boomerang_type, bladderfish_type
                )[tunnel_index % 3]

            # Два экземпляра гарантируют наличие рыбы в каждом проходе;
            # более просторные секции получают третью рыбу.
            fish_count = 3 if tunnel.area() >= 900 else 2
            rnd = random.Random(126000 + tunnel_index * 733)
            placed = 0
            for _fish_index in range(fish_count):
                for _attempt in range(80):
                    x, y = tunnel.random_point(rnd)
                    ix, iy = int(x), int(y)
                    if self.get_cave_tunnel_at(ix, iy) is not tunnel:
                        continue
                    self.cave_animals.append(
                        Animal(x, y, fish_type, tunnel)
                    )
                    placed += 1
                    break

        # Точные переопределения фауны применяются после стандартного
        # заселения. Они заменяют состав только в указанном туннеле.
        cave_animal_registry = {
            'peeper': peeper_type,
            'bladderfish': bladderfish_type,
            'boomerang': boomerang_type,
            'garryfish': garryfish_type,
            'holefish': holefish_type,
            'hoverfish': hoverfish_type,
            'hoopfish': hoopfish_type,
            'reginald': reginald_type,
            'spadefish': spadefish_type,
            'eyeye': eyeye_type,
            'oculus': oculus_type,
            'spinefish': spinefish_type,
            'blighter': blighter_type,
            'biter': biter_type,
            'crashfish': crashfish_type,
            'stalker': stalker_type,
            'sand_shark': sand_shark_type,
            'boneshark': boneshark_type,
            'ampeel': ampeel_type,
            'mesmer': mesmer_type,
            'crabsquid': crabsquid_type,
            'crabsnake': crabsnake_type,
            'gasopod': gasopod_type,
            'warper': warper_type,
            'rabbit_ray': rabbit_ray_type,
            'jellyray': jellyray_type,
            'reefback': reefback_type,
            'reaper': reaper_type,
            'ghost_leviathan': ghost_leviathan_type,
            'sea_treader': sea_treader_type,
            'sea_dragon': sea_dragon_type,
        }
        for tunnel in self.cave_tunnels:
            override = CAVE_TUNNEL_ECOSYSTEM_OVERRIDES.get(
                tunnel.name, {}
            )
            if 'fauna' not in override:
                continue

            # Удаляем только существ, закреплённых за этим туннелем.
            self.cave_animals = [
                animal for animal in self.cave_animals
                if animal.home_biome is not tunnel
            ]
            for animal_key, amount in override.get('fauna', {}).items():
                animal_type = cave_animal_registry.get(animal_key)
                try:
                    amount = max(0, min(100, int(amount)))
                except (TypeError, ValueError):
                    continue
                if animal_type is None or amount <= 0:
                    continue

                rnd = random.Random(
                    191000 + sum((i + 1) * ord(ch)
                                 for i, ch in enumerate(tunnel.name))
                    + len(animal_key) * 97
                )
                placed = 0
                for _spawn_index in range(amount):
                    for _attempt in range(80):
                        x, y = tunnel.random_point(rnd)
                        ix, iy = int(x), int(y)
                        if self.get_cave_tunnel_at(ix, iy) is not tunnel:
                            continue
                        self.cave_animals.append(
                            Animal(x, y, animal_type, tunnel)
                        )
                        placed += 1
                        break

        # Панель карты читает biome.animals. Раньше животные физически
        # появлялись в пещерах, но у самих пещерных секций список animals
        # оставался пустым, поэтому интерфейс показывал «— нет».
        # Заполняем список по фактически созданной фауне каждой комнаты.
        cave_room_counts = {}
        for animal in self.cave_animals:
            room_counts = cave_room_counts.setdefault(
                animal.home_biome, {}
            )
            room_counts[animal.type] = room_counts.get(animal.type, 0) + 1

        for tunnel in self.cave_tunnels:
            counts = cave_room_counts.get(tunnel, {})
            tunnel.animals = [
                (animal_type, count)
                for animal_type, count in counts.items()
            ]

    def _build_cave_spatial_index(self):
        self.cave_tunnel_chunks.clear()
        self.cave_tunnel_cache.clear()
        chunk = CAVE_CHUNK_SIZE
        max_chunk = (MAP_SIZE - 1) // chunk

        for tunnel in self.cave_tunnels:
            x1, y1, x2, y2 = tunnel.rect
            cx1 = max(0, int(x1) // chunk)
            cy1 = max(0, int(y1) // chunk)
            cx2 = min(max_chunk, int(x2) // chunk)
            cy2 = min(max_chunk, int(y2) // chunk)

            for cy in range(cy1, cy2 + 1):
                for cx in range(cx1, cx2 + 1):
                    self.cave_tunnel_chunks.setdefault(
                        (cx, cy), []
                    ).append(tunnel)

    def _build_cave_entrance_index(self):
        self.surface_cave_entrance_cells.clear()
        self.cave_exit_cells.clear()

        for entrance in self.cave_entrances:
            sx1, sy1, sx2, sy2 = entrance["surface_rect"]
            for y in range(sy1, sy2 + 1):
                for x in range(sx1, sx2 + 1):
                    self.surface_cave_entrance_cells[(x, y)] = entrance

            cx1, cy1, cx2, cy2 = entrance["cave_rect"]
            for y in range(cy1, cy2 + 1):
                for x in range(cx1, cx2 + 1):
                    self.cave_exit_cells[(x, y)] = entrance

    @staticmethod
    def _point_in_rect(x, y, rect):
        x1, y1, x2, y2 = rect
        return x1 <= x <= x2 and y1 <= y <= y2

    def get_cave_tunnel_at(self, x, y):
        if not (0 <= x < MAP_SIZE and 0 <= y < MAP_SIZE):
            return None

        integer_x = int(x)
        integer_y = int(y)
        cacheable = (x == integer_x and y == integer_y)
        cache_key = (integer_x, integer_y)

        if cacheable and cache_key in self.cave_tunnel_cache:
            return self.cave_tunnel_cache[cache_key]

        chunk_key = (
            integer_x // CAVE_CHUNK_SIZE,
            integer_y // CAVE_CHUNK_SIZE
        )
        result = None

        # reversed() сохраняет прежнее правило перекрытия тоннелей:
        # последний добавленный тоннель имеет приоритет.
        for tunnel in reversed(
                self.cave_tunnel_chunks.get(chunk_key, ())):
            if tunnel.contains(x, y):
                result = tunnel
                break

        if cacheable:
            if len(self.cave_tunnel_cache) >= MAX_CAVE_CACHE:
                self.cave_tunnel_cache.clear()
            self.cave_tunnel_cache[cache_key] = result

        return result

    def cave_is_passable(self, x, y):
        if self.get_cave_tunnel_at(x, y) is None:
            return False

        # Построенные в пещере стены блокируют движение так же,
        # как стены на поверхности. Пол и обычные ресурсы проходимы.
        obj = self.cave_world.get_object_at(int(x), int(y))
        return obj is None or not obj.is_wall

    def get_surface_cave_entrance_at(self, x, y):
        integer_x = int(x)
        integer_y = int(y)
        if x == integer_x and y == integer_y:
            return self.surface_cave_entrance_cells.get(
                (integer_x, integer_y)
            )

        # Редкий fallback для дробных координат.
        for entrance in self.cave_entrances:
            if self._point_in_rect(x, y, entrance["surface_rect"]):
                return entrance
        return None

    def get_cave_exit_at(self, x, y):
        integer_x = int(x)
        integer_y = int(y)
        if x == integer_x and y == integer_y:
            return self.cave_exit_cells.get((integer_x, integer_y))

        for entrance in self.cave_entrances:
            if self._point_in_rect(x, y, entrance["cave_rect"]):
                return entrance
        return None

    def get_current_animals(self):
        if self.in_cave:
            return self.cave_animals
        return self.world.animals

    def get_nearby_animals(self, radius):
        if self.in_cave:
            player_x = self.player_x
            player_y = self.player_y
            return [
                animal for animal in self.cave_animals
                if (abs(animal.x - player_x) <= radius
                    and abs(animal.y - player_y) <= radius)
            ]

        return self.world.get_animals_near(
            self.player_x, self.player_y, radius
        )

    def remove_current_animal(self, animal):
        if self.in_cave:
            if animal in self.cave_animals:
                self.cave_animals.remove(animal)
            return

        self.world.remove_animal(animal)

    def _get_all_companions(self):
        result = []
        seen = set()
        for animal in list(self.world.animals) + list(self.cave_animals):
            if not getattr(animal, "is_companion", False):
                continue
            marker = id(animal)
            if marker in seen:
                continue
            seen.add(marker)
            result.append(animal)
        return result

    def _get_visible_companions(self):
        companions = []
        for animal in self.get_current_animals():
            if not getattr(animal, "is_companion", False):
                continue
            if (abs(animal.x - self.player_x) <= VIEW_RADIUS
                    and abs(animal.y - self.player_y) <= VIEW_RADIUS):
                companions.append(animal)
        return companions

    def _companion_follow_distance(self, animal):
        # Creature length is in sprite pixels. Convert it to comfortable world
        # spacing and clamp it so even leviathans remain inside the visible area.
        length = float(getattr(animal.type, "fish_length",
                               max(20, animal.type.size * 3)))
        return max(1.7, min(VIEW_RADIUS * 0.68, 1.35 + length / 55.0))

    def _companion_orbit_distance(self, animal):
        follow = self._companion_follow_distance(animal)
        return max(1.5, min(VIEW_RADIUS * 0.72, follow * 0.92))

    def _position_is_passable_for_companion(self, x, y):
        if not (0 <= x < MAP_SIZE and 0 <= y < MAP_SIZE):
            return False

        if self.in_cave:
            return self.cave_is_passable(x, y)

        cell_x = int(x)
        cell_y = int(y)
        target_object = self.world.get_object_at(cell_x, cell_y)
        if target_object is not None and target_object.is_wall:
            return False

        if self.is_start_capsule_wall(cell_x, cell_y):
            return False

        biome = self.world.get_biome_at(cell_x, cell_y)
        if self.is_start_capsule_passage(cell_x, cell_y):
            return True
        return biome is None or biome.passable

    def _find_nearby_passable_position(self, radius=1.25):
        candidates = [(self.player_x, self.player_y)]
        for ring in (radius, radius * 1.6):
            for index in range(12):
                angle = index / 12.0 * math.tau
                candidates.append((
                    self.player_x + math.cos(angle) * ring,
                    self.player_y + math.sin(angle) * ring
                ))

        for x, y in candidates:
            if self._position_is_passable_for_companion(x, y):
                return x, y
        return None

    def _add_animal_to_current_layer(self, animal):
        if self.in_cave:
            self.cave_animals.append(animal)
        else:
            self.world.animals.append(animal)
            self.world.rebuild_animal_index()

    def _clear_companion_target(self, animal):
        target = getattr(animal, "companion_target", None)
        if target is not None and getattr(target, "pet_combat_target", None) is animal:
            target.pet_combat_target = None
        animal.companion_target = None

    def _transfer_visible_companions(self, companions, target_in_cave):
        if not companions:
            return

        # self.in_cave and player position already point at the destination layer.
        for index, animal in enumerate(companions):
            self._clear_companion_target(animal)
            if target_in_cave:
                self.world.remove_animal(animal)
                if animal not in self.cave_animals:
                    self.cave_animals.append(animal)
                animal.home_biome = self.get_cave_tunnel_at(
                    self.player_x, self.player_y
                ) or animal.home_biome
            else:
                if animal in self.cave_animals:
                    self.cave_animals.remove(animal)
                if animal not in self.world.animals:
                    self.world.animals.append(animal)
                animal.home_biome = self.world.get_biome_at(
                    self.player_x, self.player_y
                ) or animal.home_biome

            angle = animal.companion_orbit_angle + index * 0.8
            radius = min(
                self._companion_follow_distance(animal),
                VIEW_RADIUS * 0.6
            )
            target_x = self.player_x + math.cos(angle) * radius
            target_y = self.player_y + math.sin(angle) * radius
            if self._position_is_passable_for_companion(target_x, target_y):
                animal.x = target_x
                animal.y = target_y
            else:
                animal.x = self.player_x
                animal.y = self.player_y
            animal.dx = 0.0
            animal.dy = 0.0
            animal.active = True
            animal.companion_state = "следует за игроком"

        if not target_in_cave:
            self.world.rebuild_animal_index()

    def _find_companion_hunt_target(self, companion):
        # Besides ordinary predators, creatures with special attacks can use
        # those attacks as pets (Sea Dragon fireballs and Gasopod gas pods).
        special_combatants = {"Sea Dragon Leviathan", "Dragon Leviathan", "Gasopod"}
        if (companion.type.behavior != "predator"
                and companion.type.name not in special_combatants):
            return None

        best = None
        best_distance_sq = float("inf")
        for animal in self.get_nearby_animals(VIEW_RADIUS):
            if animal is companion or animal.hp <= 0:
                continue
            if getattr(animal, "is_companion", False):
                continue

            # The pet only reacts to fauna that is actually inside the visible
            # area and not farther than one view radius from the pet itself.
            if (abs(animal.x - self.player_x) > VIEW_RADIUS
                    or abs(animal.y - self.player_y) > VIEW_RADIUS):
                continue
            dx = animal.x - companion.x
            dy = animal.y - companion.y
            distance_sq = dx * dx + dy * dy
            if distance_sq > VIEW_RADIUS * VIEW_RADIUS:
                continue
            if distance_sq < best_distance_sq:
                best = animal
                best_distance_sq = distance_sq
        return best

    def _move_companion_towards(self, animal, target_x, target_y, move_speed):
        to_target_x = target_x - animal.x
        to_target_y = target_y - animal.y
        distance = math.hypot(to_target_x, to_target_y)
        if distance <= 0.001:
            animal.dx = 0.0
            animal.dy = 0.0
            return False

        step = min(move_speed, distance)
        velocity_x = to_target_x / distance * step
        velocity_y = to_target_y / distance * step
        new_x = animal.x + velocity_x
        new_y = animal.y + velocity_y

        moved = False
        if self._position_is_passable_for_companion(new_x, new_y):
            animal.x = new_x
            animal.y = new_y
            moved = True
        elif self._position_is_passable_for_companion(new_x, animal.y):
            animal.x = new_x
            velocity_y = 0.0
            moved = True
        elif self._position_is_passable_for_companion(animal.x, new_y):
            animal.y = new_y
            velocity_x = 0.0
            moved = True
        else:
            animal.companion_orbit_angle += 0.35

        if moved:
            animal.dx = velocity_x
            animal.dy = velocity_y
            animal._update_rotation()
        else:
            animal.dx = 0.0
            animal.dy = 0.0
        return moved

    def _finish_companion_kill(self, companion, target):
        target.hp = 0
        if getattr(target, "pet_combat_target", None) is companion:
            target.pet_combat_target = None
        companion.companion_target = None

        if self.add_to_inventory(target.type):
            self.remove_current_animal(target)
            companion.companion_state = "добыча отправлена в инвентарь"
            self.notification = (
                f"{companion.type.name} поймал {target.type.name}: "
                "добыча в инвентаре"
            )
        else:
            # Do not destroy loot when the inventory has no empty slot.
            companion.companion_state = "инвентарь полон"
            self.notification = (
                f"{companion.type.name} убил {target.type.name}, "
                "но инвентарь полон"
            )
        self.notification_timer = 75

    def _update_companion(self, animal, player_move_x, player_move_y):
        dx_to_player = self.player_x - animal.x
        dy_to_player = self.player_y - animal.y
        distance_to_player = math.hypot(dx_to_player, dy_to_player)

        if animal.companion_attack_timer > 0:
            animal.companion_attack_timer -= 1

        # Outside the screen a pet freezes and does not teleport to the diver.
        if (abs(dx_to_player) > VIEW_RADIUS
                or abs(dy_to_player) > VIEW_RADIUS):
            self._clear_companion_target(animal)
            animal.active = False
            animal.dx = 0.0
            animal.dy = 0.0
            animal.companion_state = "ждёт вне видимости"
            return

        animal.active = True
        player_move_length = math.hypot(player_move_x, player_move_y)
        follow_distance = self._companion_follow_distance(animal)
        orbit_distance = self._companion_orbit_distance(animal)
        animal.companion_orbit_radius = orbit_distance

        # Priority 1: following the player. Moving player always wins over hunt;
        # a stationary player also pulls back a pet that chased too far away.
        must_follow = (
            player_move_length > 0.001
            or distance_to_player > follow_distance * 1.35
        )

        if must_follow:
            self._clear_companion_target(animal)
            if player_move_length > 0.001:
                move_x = player_move_x / player_move_length
                move_y = player_move_y / player_move_length
            elif distance_to_player > 0.001:
                move_x = -dx_to_player / distance_to_player
                move_y = -dy_to_player / distance_to_player
            else:
                move_x, move_y = 1.0, 0.0

            side_x = -move_y
            side_y = move_x
            animal.companion_orbit_angle = (
                animal.companion_orbit_angle + 0.012
            ) % math.tau
            lateral = math.sin(animal.companion_orbit_angle) * min(1.2, follow_distance * 0.22)
            target_x = self.player_x - move_x * follow_distance + side_x * lateral
            target_y = self.player_y - move_y * follow_distance + side_y * lateral

            speed_scale = 0.75 + min(0.55, follow_distance / 10.0)
            move_speed = max(0.22, min(1.15, animal.type.speed * 8.0 * speed_scale))
            if distance_to_player > VIEW_RADIUS * 0.65:
                move_speed *= 1.35
            self._move_companion_towards(animal, target_x, target_y, move_speed)
            animal.companion_state = "следует за игроком"
            return

        # Priority 2: predator pets immediately hunt visible non-pet fauna.
        target = getattr(animal, "companion_target", None)
        current_animals = self.get_current_animals()
        target_valid = (
            target is not None
            and target in current_animals
            and target.hp > 0
            and not getattr(target, "is_companion", False)
            and abs(target.x - self.player_x) <= VIEW_RADIUS
            and abs(target.y - self.player_y) <= VIEW_RADIUS
        )
        if not target_valid:
            self._clear_companion_target(animal)
            target = self._find_companion_hunt_target(animal)
            animal.companion_target = target

        if target is not None:
            # A predator target fights back against the attacking pet.
            if target.type.behavior == "predator":
                target.pet_combat_target = animal

            hunt_dx = target.x - animal.x
            hunt_dy = target.y - animal.y
            hunt_distance = math.hypot(hunt_dx, hunt_dy)
            animal.companion_state = f"охотится: {target.type.name}"

            length = float(getattr(animal.type, "fish_length", animal.type.size * 3))
            uses_projectiles = animal.type.name in (
                "Sea Dragon Leviathan", "Dragon Leviathan", "Gasopod"
            )
            # Ranged pets stop at a comfortable distance and let their native
            # special attack deal damage instead of biting the target.
            attack_range = (3.5 if uses_projectiles else
                            max(0.9, min(2.2, 0.75 + length / 150.0)))

            if hunt_distance > attack_range:
                hunt_speed = max(
                    0.28,
                    min(1.25, animal.type.speed * 9.5)
                )
                self._move_companion_towards(
                    animal, target.x, target.y, hunt_speed
                )
            else:
                animal.dx = 0.0
                animal.dy = 0.0
                if animal.companion_attack_timer <= 0 and not uses_projectiles:
                    damage = max(1, int(animal.type.damage))
                    target.hp -= damage
                    animal.companion_attack_timer = animal.companion_attack_cooldown
                    animal.companion_state = f"атакует: {target.type.name}"
                    if target.hp <= 0:
                        self._finish_companion_kill(animal, target)
                elif uses_projectiles:
                    animal.companion_state = f"готовит особую атаку: {target.type.name}"
            return

        # Priority 3: if there is nobody to hunt, circle around the diver.
        animal.companion_orbit_angle = (
            animal.companion_orbit_angle + 0.028
        ) % math.tau
        target_x = (
            self.player_x
            + math.cos(animal.companion_orbit_angle) * orbit_distance
        )
        target_y = (
            self.player_y
            + math.sin(animal.companion_orbit_angle) * orbit_distance
        )
        orbit_speed = max(0.16, min(0.42, animal.type.speed * 3.4))
        self._move_companion_towards(animal, target_x, target_y, orbit_speed)
        animal.companion_state = "плавает вокруг игрока"

    def handle_animal_death(self, animal):
        if self.add_to_inventory(animal.type):
            self.remove_current_animal(animal)
            self.notification = (
                f"{animal.type.name} убит и подобран!"
            )
        else:
            self.notification = (
                f"{animal.type.name} убит, но инвентарь полон!"
            )
        self.notification_timer = 60

    def use_cave_entrance(self):
        if self.state != "playing":
            return

        px = int(self.player_x)
        py = int(self.player_y)

        if not self.in_cave:
            entrance = self.get_surface_cave_entrance_at(px, py)
            if entrance is None:
                self.notification = "Здесь нет входа в пещеру"
                self.notification_timer = 45
                return

            visible_companions = self._get_visible_companions()
            self.in_cave = True
            self.player_x, self.player_y = entrance["cave_spawn"]
            self._transfer_visible_companions(
                visible_companions, target_in_cave=True
            )
            self.map_center_x = self.player_x
            self.map_center_y = self.player_y
            self.selected_biome = None
            self.notification = (
                f"Вы вошли в пещеру: {entrance['name']}"
            )
            self.notification_timer = 90
            return

        exit_data = self.get_cave_exit_at(px, py)
        if exit_data is None:
            self.notification = (
                "Всплыть можно только у выхода на поверхность"
            )
            self.notification_timer = 60
            return

        visible_companions = self._get_visible_companions()
        self.in_cave = False
        self.player_x, self.player_y = exit_data["surface_spawn"]
        self._transfer_visible_companions(
            visible_companions, target_in_cave=False
        )
        self.map_center_x = self.player_x
        self.map_center_y = self.player_y
        self.selected_biome = None
        self.notification = (
            f"Вы всплыли: {exit_data['name']}"
        )
        self.notification_timer = 90

    # =====================================================
    # ИНВЕНТАРЬ
    # =====================================================

    def _start_inventory_registry(self):
        """Возвращает словарь доступных типов предметов по имени.

        Поддерживаются:
        1) отображаемое имя из игры, например "Мотылёк" или "Нож";
        2) внутреннее имя переменной, если оно было доступно при init_assets().

        START_ITEM_REGISTRY формируется в конце init_assets(), поэтому сюда
        попадают и глобальные, и локальные игровые типы.
        """
        registry = dict(START_ITEM_REGISTRY)

        # Дополнительная страховка для глобальных типов.
        for variable_name, value in globals().items():
            if isinstance(value, (ObjectType, AnimalType)):
                registry.setdefault(value.name, value)
                registry.setdefault(variable_name, value)

        return registry

    def _load_start_inventory(self):
        """Заполняет инвентарь согласно START_INVENTORY из начала файла."""
        if not isinstance(START_INVENTORY, dict):
            print(
                "[START_INVENTORY] Ошибка: START_INVENTORY должен быть словарём, "
                "например {'Сканер': 1, 'Титан': 5}."
            )
            return

        registry = self._start_inventory_registry()
        added_total = 0

        for item_name, amount in START_INVENTORY.items():
            try:
                amount = int(amount)
            except (TypeError, ValueError):
                print(
                    f"[START_INVENTORY] Пропущено '{item_name}': "
                    f"количество должно быть целым числом, получено {amount!r}."
                )
                continue

            if amount <= 0:
                continue

            item_type = registry.get(item_name)
            if item_type is None:
                print(
                    f"[START_INVENTORY] Не найден предмет: {item_name!r}. "
                    "Проверьте точное игровое название."
                )
                continue

            for _ in range(amount):
                if not self.add_to_inventory(item_type):
                    print(
                        "[START_INVENTORY] Инвентарь заполнен. "
                        f"Не удалось добавить оставшиеся предметы, начиная с "
                        f"{item_type.name!r}."
                    )
                    return
                added_total += 1

        if added_total:
            print(
                f"[START_INVENTORY] Добавлено стартовых предметов: "
                f"{added_total}/{INVENTORY_SIZE}."
            )

    def add_to_inventory(self, item_type):
        for index, slot in enumerate(self.inventory):
            if slot is None:
                self._stored_companion_hp.pop(index, None)
                self.inventory[index] = item_type
                self.inventory_counts[item_type] = (
                    self.inventory_counts.get(item_type, 0) + 1
                )
                return True
        return False

    def _remove_inventory_slot(self, index):
        if not (0 <= index < INVENTORY_SIZE):
            return None
        item = self.inventory[index]
        if item is None:
            return None

        self.inventory[index] = None
        self._stored_companion_hp.pop(index, None)
        current_count = self.inventory_counts.get(item, 0) - 1
        if current_count > 0:
            self.inventory_counts[item] = current_count
        else:
            self.inventory_counts.pop(item, None)
            if self.equipped_weapon is item:
                self.equipped_weapon = None

        self.active_slot_index = -1
        return item

    def _current_dropped_items(self):
        return (
            self.cave_dropped_items
            if self.in_cave
            else self.surface_dropped_items
        )

    def _spawn_animal_from_inventory_item(self, animal_type, companion=False):
        spawn = self._find_nearby_passable_position(1.25)
        if spawn is None:
            return None

        if self.in_cave:
            home_biome = self.get_cave_tunnel_at(spawn[0], spawn[1])
        else:
            home_biome = self.world.get_biome_at(spawn[0], spawn[1])

        if home_biome is None and not companion:
            return None
        if home_biome is None:
            home_biome = (
                self.get_cave_tunnel_at(self.player_x, self.player_y)
                if self.in_cave
                else self.world.get_biome_at(self.player_x, self.player_y)
            )
        if home_biome is None:
            return None

        animal = Animal(spawn[0], spawn[1], animal_type, home_biome)
        if companion:
            animal.is_companion = True
            animal.hp = animal.max_hp
            animal.companion_orbit_angle = random.uniform(0.0, math.tau)
            animal.companion_orbit_radius = self._companion_orbit_distance(animal)
            animal.companion_target = None
            animal.companion_attack_timer = 0
            animal.companion_state = "следует за игроком"

        self._add_animal_to_current_layer(animal)
        return animal

    def drop_selected_item(self):
        if self.state != "inventory":
            return
        if self.active_slot_index == -1:
            self.notification = "Выберите предмет в инвентаре"
            self.notification_timer = 60
            return

        item = self.inventory[self.active_slot_index]
        if item is None:
            self.notification = "Слот пуст"
            self.notification_timer = 45
            return

        if isinstance(item, AnimalType):
            spawned = self._spawn_animal_from_inventory_item(
                item, companion=False
            )
            if spawned is None:
                self.notification = "Здесь нельзя выпустить это существо"
                self.notification_timer = 60
                return
            self._remove_inventory_slot(self.active_slot_index)
            self.notification = f"Выпущено: {item.name}"
            self.notification_timer = 60
            return

        cell = (int(self.player_x), int(self.player_y))
        dropped = self._current_dropped_items()
        dropped.setdefault(cell, []).append(item)
        self._remove_inventory_slot(self.active_slot_index)
        self.notification = f"Выброшено: {item.name}"
        self.notification_timer = 60

    def spawn_selected_companion(self):
        if self.state != "inventory":
            return
        if self.active_slot_index == -1:
            self.notification = "Выберите рыбу или хищника"
            self.notification_timer = 60
            return

        item = self.inventory[self.active_slot_index]
        if item is None:
            self.notification = "Слот пуст"
            self.notification_timer = 45
            return
        if not isinstance(item, AnimalType):
            self.notification = "Спутником может стать только существо"
            self.notification_timer = 60
            return

        slot_index = self.active_slot_index
        companion = self._spawn_animal_from_inventory_item(
            item, companion=True
        )
        if companion is None:
            self.notification = "Здесь недостаточно места для существа"
            self.notification_timer = 60
            return

        stored = self._stored_companion_hp.get(slot_index)
        if stored is not None and stored[0] is item:
            companion.hp = max(1, min(companion.max_hp, stored[1]))
        self._remove_inventory_slot(slot_index)
        self.notification = f"{item.name} теперь ваш спутник"
        self.notification_timer = 90

    def player_take_damage(self, damage):
        damage_multiplier = 1.0
        if self.inventory_counts.get(reinforced_suit, 0) > 0:
            damage_multiplier *= 0.75
        if self.damage_resist_timer > 0:
            damage_multiplier *= 0.5

        final_damage = max(1, int(round(damage * damage_multiplier)))
        self.player_hp -= final_damage
        self.damage_vignette_flash = max(self.damage_vignette_flash, 18)
        self.notification = (
            f"Получено {final_damage} урона! HP: {self.player_hp}"
        )
        self.notification_timer = 60

        if self.player_hp <= 0:
            self.player_hp = 0
            self.notification = "Игрок погиб! Игра окончена."
            self.notification_timer = 9999
            # External scene manager switches to the death screen.
            # Do not terminate the browser's Python runtime on death.
            self.state = "dead"

    def equip_weapon(self):
        if self.state not in ("playing", "inventory"):
            return

        if self.active_slot_index == -1:
            self.notification = "Выберите предмет в инвентаре"
            self.notification_timer = 60
            return

        item = self.inventory[self.active_slot_index]

        if item is None:
            self.notification = "Слот пуст"
            self.notification_timer = 60
            return

        if not item.is_weapon:
            self.notification = "Этот предмет не является оружием"
            self.notification_timer = 60
            return

        self.equipped_weapon = item
        self.notification = f"Экипировано: {item.name}"
        self.notification_timer = 60

    def _consume_selected_item(self, item=None):
        if self.active_slot_index == -1:
            return False

        if item is None:
            item = self.inventory[self.active_slot_index]
        if item is None:
            return False

        self.inventory[self.active_slot_index] = None
        self._stored_companion_hp.pop(self.active_slot_index, None)
        current_count = self.inventory_counts.get(item, 0) - 1
        if current_count > 0:
            self.inventory_counts[item] = current_count
        else:
            self.inventory_counts.pop(item, None)
            if self.equipped_weapon is item:
                self.equipped_weapon = None

        self.active_slot_index = -1
        return True

    def _get_current_object_grid(self):
        return self.cave_object_grid if self.in_cave else self.world.object_grid

    def _nearby_buildables(self, radius=3.0):
        grid = self._get_current_object_grid()
        result = []
        radius_sq = radius * radius
        for (x, y), obj in grid.items():
            if not getattr(obj, "is_buildable", False):
                continue
            dx = x - self.player_x
            dy = y - self.player_y
            dist_sq = dx * dx + dy * dy
            if dist_sq <= radius_sq:
                result.append((obj, x, y, dist_sq))
        return result

    def _nearest_resource_info(self, radius=8):
        grid = self._get_current_object_grid()
        radius_sq = radius * radius
        best = None
        highlights = []
        counts = {}
        for (x, y), obj in grid.items():
            if getattr(obj, "is_buildable", False) or getattr(obj, "is_weapon", False):
                continue
            dx = x - self.player_x
            dy = y - self.player_y
            dist_sq = dx * dx + dy * dy
            if dist_sq > radius_sq:
                continue
            highlights.append((x, y))
            counts[obj.name] = counts.get(obj.name, 0) + 1
            if best is None or dist_sq < best[0]:
                best = (dist_sq, obj, x, y)
        return best, counts, highlights

    def _direction_hint(self, target_x, target_y):
        dx = target_x - self.player_x
        dy = target_y - self.player_y
        parts = []
        if abs(dx) >= 0.5:
            parts.append("восток" if dx > 0 else "запад")
        if abs(dy) >= 0.5:
            parts.append("юг" if dy > 0 else "север")
        return "-".join(parts) if parts else "здесь"

    def _find_nearest_path_target(self):
        points = []
        if self.in_cave:
            for (x, y), exit_data in self.cave_exit_cells.items():
                points.append((x, y, "выход на поверхность"))
        else:
            for (x, y), entrance in self.surface_cave_entrance_cells.items():
                points.append((x, y, "вход в пещеру"))
            x1, y1, x2, y2 = self.start_capsule_rect
            points.append(((x1 + x2) / 2, (y1 + y2) / 2, "стартовая капсула"))
            for (x, y), obj in self.world.object_grid.items():
                if obj is beacon_type:
                    points.append((x, y, "радиомаяк"))
        if not points:
            return None
        best = None
        for x, y, label in points:
            dx = x - self.player_x
            dy = y - self.player_y
            dist_sq = dx * dx + dy * dy
            if best is None or dist_sq < best[0]:
                best = (dist_sq, x, y, label)
        return best

    def _play_effect(self, key, volume=0.5, interval=0):
        if not self.setting_effects_enabled or key not in self._sounds:
            return
        now = pygame.time.get_ticks()
        if now - self._sound_times.get(key, -100000) < interval:
            return
        self._sound_times[key] = now
        channel = self._sounds[key].play()
        if channel is not None:
            channel.set_volume(max(0.0, min(1.0, volume)))

    def _scan_environment(self, passive=False):
        self._play_effect("sonar", 0.4, 1200)
        radius = 8
        if self.inventory_counts.get(scanner_range, 0) > 0:
            radius += 3

        best, counts, highlights = self._nearest_resource_info(radius)
        self.scanner_highlight_cells = set(highlights[:24])
        self.scanner_highlight_timer = 300
        predator_count = 0
        for animal in self.get_current_animals():
            if animal.hp <= 0:
                continue
            dx = animal.x - self.player_x
            dy = animal.y - self.player_y
            if dx * dx + dy * dy <= radius * radius and animal.type.behavior == "predator":
                predator_count += 1

        if best is None:
            if not passive:
                self.notification = f"Сканер: поблизости ничего не найдено. Хищников: {predator_count}"
                self.notification_timer = 120
            return

        _, obj, x, y = best
        direction = self._direction_hint(x, y)
        details = ", ".join(
            f"{name}×{count}" for name, count in list(sorted(counts.items()))[:3]
        )
        if passive:
            self.notification = (
                f"Комната сканирования: {obj.name} ({direction}), хищников: {predator_count}"
            )
            self.notification_timer = 90
        else:
            self.notification = (
                f"Сканер: ближайший ресурс — {obj.name} ({direction}). "
                f"Рядом: {details}. Хищников: {predator_count}"
            )
            self.notification_timer = 150

    def _selected_inventory_item(self):
        if not (0 <= self.active_slot_index < len(self.inventory)):
            return None
        return self.inventory[self.active_slot_index]

    def _is_scanner_selected(self):
        return self._selected_inventory_item() is scanner_type

    def _current_flora_grid(self):
        return self.cave_flora_grid if self.in_cave else self.world.flora_grid

    def _current_location_name(self, x, y):
        if self.in_cave:
            area = self.get_cave_tunnel_at(x, y)
        else:
            area = self.world.get_biome_at(x, y)
        return area.name if area is not None else "Неизвестная область"

    def _scan_target_at_cursor(self):
        """Возвращает объект под прицелом сканера.

        Приоритет отдаётся существам, потому что их спрайт может занимать
        несколько клеток. Затем проверяются предметы/ресурсы, растения и
        выброшенные предметы в клетке курсора.
        """
        mx = float(self.mouse_world_x)
        my = float(self.mouse_world_y)

        best_animal = None
        for animal in self.get_current_animals():
            if animal.hp <= 0:
                continue
            radius = max(0.55, min(3.8, animal.type.size / CELL_SIZE * 0.55))
            dist_sq = (animal.x - mx) ** 2 + (animal.y - my) ** 2
            if dist_sq <= radius * radius:
                if best_animal is None or dist_sq < best_animal[0]:
                    best_animal = (dist_sq, animal)
        if best_animal is not None:
            animal = best_animal[1]
            return {
                "kind": "animal",
                "entity": animal.type,
                "animal": animal,
                "x": animal.x,
                "y": animal.y,
            }

        x = int(math.floor(mx))
        y = int(math.floor(my))
        if not (0 <= x < MAP_SIZE and 0 <= y < MAP_SIZE):
            return None

        obj = self._get_current_object_grid().get((x, y))
        if obj is not None:
            return {"kind": "object", "entity": obj, "x": x, "y": y}

        flora = self._current_flora_grid().get((x, y))
        if flora is not None:
            return {"kind": "flora", "entity": flora, "x": x, "y": y}

        dropped = self._current_dropped_items().get((x, y))
        if dropped:
            return {
                "kind": "dropped",
                "entity": dropped[-1],
                "x": x,
                "y": y,
            }

        return None

    @staticmethod
    def _behavior_name(behavior):
        return {
            "predator": "хищник",
            "prey": "мирное / добыча",
            "neutral": "нейтральное",
        }.get(behavior, str(behavior))

    def _scanner_details(self, target):
        entity = target["entity"]
        location = self._current_location_name(target["x"], target["y"])
        lines = []

        if target["kind"] == "flora":
            lines.extend([
                "Класс: флора",
                f"Вид: {entity.kind}",
                f"Размер природного экземпляра: {entity.size}px",
                f"Обнаружено: {location}",
                "Статус базы данных: исследовано",
                "Практическое применение: после исследования этот вид можно "
                "высаживать в построенные грядки и горшки.",
            ])
        elif isinstance(entity, AnimalType):
            lines.extend([
                "Класс: живое существо",
                f"Поведение: {self._behavior_name(entity.behavior)}",
                f"Здоровье: {entity.hp}",
                f"Урон при атаке: {entity.damage}",
                f"Скорость: {entity.speed:.3f}",
                f"Съедобность: {'да' if entity.edible else 'нет'}",
                f"Объём в инвентаре: {entity.volume}",
                f"Обнаружено: {location}",
            ])
        else:
            if getattr(entity, "is_buildable", False):
                category = "постройка / устройство"
            elif getattr(entity, "is_weapon", False):
                category = "оружие"
            elif getattr(entity, "edible", False):
                category = "съедобный предмет / ресурс"
            else:
                category = "предмет / ресурс"

            lines.extend([
                f"Класс: {category}",
                f"Размер: {getattr(entity, 'size', 0)}px",
                f"Объём в инвентаре: {getattr(entity, 'volume', 1)}",
                f"Обнаружено: {location}",
            ])
            if getattr(entity, "is_weapon", False):
                lines.append(f"Урон: {entity.damage}")
                lines.append(f"Дальность: {entity.weapon_range}")
                lines.append(f"Тип оружия: {entity.weapon_type or 'не указан'}")
            if getattr(entity, "edible", False):
                lines.append(f"Питательность: +{entity.hunger_value} голода")
                lines.append(f"Жидкость: +{entity.thirst_value} жажды")
            if entity in self._planter_types():
                lines.append("Контейнер для выращивания: ПКМ без выбранного сканера открывает посадку.")

        return lines

    def _scanner_preview_source(self, target):
        entity = target["entity"]
        cache_key = (target["kind"], id(entity))
        cached = self.scanner_preview_cache.get(cache_key)
        if cached is not None:
            return cached

        source = None
        if isinstance(entity, FloraType):
            # Для карточки сканера растение перерисовывается заново в большом
            # разрешении, а не просто растягивается из клеточного спрайта.
            source = generate_subnautica_flora_sprite(
                entity.kind, 260, seed=entity.seed
            )
        elif isinstance(entity, AnimalType):
            if entity.sprite_kind is not None:
                length = 420
                width = max(75, int(length * entity.fish_width / max(1.0, entity.fish_length)))
                source = generate_subnautica_creature_sprite(
                    entity.sprite_kind, length, width
                )
            elif entity.image is not None:
                source = entity.image.copy()
        elif getattr(entity, "is_buildable", False):
            source = generate_building_sprite(
                entity.name, 220, entity.color,
                wall=getattr(entity, "is_wall", False)
            )
        else:
            # Resources are redrawn directly at scanner resolution. Enlarging
            # the 10-40 px world/inventory icon made them visibly blurry.
            source = generate_highres_resource_preview(entity, 280)
            if source is None and getattr(entity, "image", None) is not None:
                source = entity.image.copy()

        if source is None:
            source = pygame.Surface((180, 180), pygame.SRCALPHA)
            if getattr(entity, "shape", "rect") == "circle":
                pygame.draw.circle(source, entity.color, (90, 90), 70)
            else:
                pygame.draw.rect(source, entity.color, (25, 25, 130, 130), border_radius=18)

        self.scanner_preview_cache[cache_key] = source
        return source

    @staticmethod
    def _fit_surface(source, max_width, max_height):
        sw, sh = source.get_size()
        if sw <= 0 or sh <= 0:
            return source
        scale = min(max_width / sw, max_height / sh)
        nw = max(1, int(sw * scale))
        nh = max(1, int(sh * scale))
        return pygame.transform.smoothscale(source, (nw, nh))

    def scan_with_scanner(self):
        self._play_effect("sonar", 0.4, 1200)
        if not self._is_scanner_selected():
            return False

        target = self._scan_target_at_cursor()
        if target is None:
            self.notification = "Сканер: наведите прицел на предмет, ресурс, существо или растение"
            self.notification_timer = 100
            return False

        entity = target["entity"]
        entry_key = (target["kind"], entity.name)
        first_scan = entry_key not in self.scanned_entries
        self.scanned_entries.add(entry_key)

        if isinstance(entity, FloraType):
            self.researched_flora.add(entity.kind)

        target["first_scan"] = first_scan
        target["details"] = self._scanner_details(target)
        self.scanner_target = target
        self.state = "scanner"
        self.notification = ""
        self.notification_timer = 0
        return True

    def _planter_types(self):
        return (
            exterior_growbed,
            indoor_growbed,
            plant_pot,
            composite_pot,
            chic_pot,
            plant_shelf,
        )

    def _planter_capacity(self, planter):
        if planter is exterior_growbed:
            return 6
        if planter is indoor_growbed:
            return 4
        if planter is plant_shelf:
            return 2
        return 1

    def _planter_key(self, x, y):
        return (bool(self.in_cave), int(x), int(y))

    def open_planting_menu_at_cursor(self):
        x = int(math.floor(self.mouse_world_x))
        y = int(math.floor(self.mouse_world_y))
        obj = self._get_current_object_grid().get((x, y))
        if obj not in self._planter_types():
            return False

        researched = [
            flora for flora in flora_types.values()
            if flora.kind in self.researched_flora
        ]
        researched.sort(key=lambda flora: flora.name.lower())
        if not researched:
            self.notification = "Сначала исследуйте растение сканером"
            self.notification_timer = 100
            return True

        self.planting_target = {
            "x": x,
            "y": y,
            "planter": obj,
        }
        self.planting_page = 0
        self.state = "planting"
        return True

    def _researched_plant_list(self):
        plants = [
            flora for flora in flora_types.values()
            if flora.kind in self.researched_flora
        ]
        plants.sort(key=lambda flora: flora.name.lower())
        return plants

    def plant_researched_flora(self, visible_index):
        if self.state != "planting" or self.planting_target is None:
            return
        plants = self._researched_plant_list()
        index = self.planting_page * self.plants_per_page + visible_index
        if not (0 <= index < len(plants)):
            return

        x = self.planting_target["x"]
        y = self.planting_target["y"]
        planter = self.planting_target["planter"]
        key = self._planter_key(x, y)
        planted = self.planted_flora.setdefault(key, [])
        capacity = self._planter_capacity(planter)
        if len(planted) >= capacity:
            self.notification = "В этой грядке/горшке больше нет свободных мест"
            self.notification_timer = 100
            return

        flora = plants[index]
        # Защита от обхода ограничения через вызов функции вручную.
        if flora.kind not in self.researched_flora:
            self.notification = "Этот вид ещё не исследован"
            self.notification_timer = 100
            return

        planted.append(flora)
        self.notification = f"Посажено: {flora.name} ({len(planted)}/{capacity})"
        self.notification_timer = 100

    def _draw_planted_flora_at(self, x, y, screen_x, screen_y):
        plants = self.planted_flora.get(self._planter_key(x, y), ())
        if not plants:
            return

        offsets = [
            (0, 1), (-8, -3), (8, -3), (-8, 7),
            (8, 7), (0, -8), (0, 9),
        ]
        for index, flora in enumerate(plants):
            image = flora.image
            if image is None:
                continue
            max_size = 20 if len(plants) <= 2 else 15
            fitted = self._fit_surface(image, max_size, max_size)
            ox, oy = offsets[index % len(offsets)]
            rect = fitted.get_rect(
                center=(
                    screen_x + CELL_SIZE // 2 + ox,
                    screen_y + CELL_SIZE // 2 + oy,
                )
            )
            self.screen.blit(fitted, rect)

    def _draw_wrapped_lines(self, lines, x, y, max_width, color=(220, 235, 240), line_height=22):
        cursor_y = y
        for source_line in lines:
            words = str(source_line).split()
            current = ""
            wrapped = []
            for word in words:
                test = word if not current else current + " " + word
                if self.small_font.size(test)[0] <= max_width:
                    current = test
                else:
                    if current:
                        wrapped.append(current)
                    current = word
            if current:
                wrapped.append(current)
            if not wrapped:
                wrapped = [""]
            for line in wrapped:
                surf = self.small_font.render(line, True, color)
                self.screen.blit(surf, (x, cursor_y))
                cursor_y += line_height
            cursor_y += 3
        return cursor_y

    def draw_scanner_view(self):
        if self.scanner_target is None:
            self.state = "playing"
            return

        target = self.scanner_target
        entity = target["entity"]
        self.screen.fill((4, 20, 28))

        margin = 28
        header_h = 70
        pygame.draw.rect(
            self.screen, (8, 55, 68),
            (margin, margin, SCREEN_SIZE - margin * 2, SCREEN_SIZE - margin * 2),
            border_radius=14,
        )
        pygame.draw.rect(
            self.screen, (60, 210, 220),
            (margin, margin, SCREEN_SIZE - margin * 2, SCREEN_SIZE - margin * 2),
            2, border_radius=14,
        )

        title = self.large_font.render(entity.name, True, (170, 250, 250))
        self.screen.blit(title, (margin + 22, margin + 16))
        status_text = "НОВАЯ ЗАПИСЬ" if target.get("first_scan") else "ИССЛЕДОВАНО"
        status = self.small_font.render(status_text, True, (130, 255, 170))
        self.screen.blit(
            status,
            (SCREEN_SIZE - margin - status.get_width() - 22, margin + 25),
        )

        content_top = margin + header_h
        preview_w = int((SCREEN_SIZE - margin * 2) * 0.46)
        preview_rect = pygame.Rect(
            margin + 18, content_top + 10,
            preview_w - 28, SCREEN_SIZE - content_top - margin - 60,
        )
        pygame.draw.rect(self.screen, (3, 26, 35), preview_rect, border_radius=12)
        pygame.draw.rect(self.screen, (35, 130, 150), preview_rect, 2, border_radius=12)

        preview = self._fit_surface(
            self._scanner_preview_source(target),
            preview_rect.width - 30,
            preview_rect.height - 30,
        )
        preview_pos = preview.get_rect(center=preview_rect.center)
        self.screen.blit(preview, preview_pos)

        # Тонкие линии сканирования поверх изображения.
        scan_y = preview_rect.top + (self.frame_count * 3) % max(1, preview_rect.height)
        pygame.draw.line(
            self.screen, (90, 245, 245),
            (preview_rect.left + 6, scan_y),
            (preview_rect.right - 6, scan_y), 1,
        )

        info_x = preview_rect.right + 24
        info_width = SCREEN_SIZE - margin - info_x - 20
        heading = self.font.render("Подробная информация", True, (255, 235, 150))
        self.screen.blit(heading, (info_x, content_top + 14))
        self._draw_wrapped_lines(
            target.get("details", ()),
            info_x, content_top + 48, info_width,
        )

        footer = self.small_font.render(
            "ESC или ПКМ — закрыть карточку сканера",
            True, (170, 210, 215),
        )
        self.screen.blit(
            footer,
            footer.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE - margin - 20)),
        )

    def draw_planting_menu(self):
        if self.planting_target is None:
            self.state = "playing"
            return

        overlay = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 205))
        self.screen.blit(overlay, (0, 0))

        plants = self._researched_plant_list()
        max_page = max(0, (len(plants) - 1) // self.plants_per_page)
        self.planting_page = min(self.planting_page, max_page)
        start = self.planting_page * self.plants_per_page
        shown = plants[start:start + self.plants_per_page]

        x = self.planting_target["x"]
        y = self.planting_target["y"]
        planter = self.planting_target["planter"]
        key = self._planter_key(x, y)
        planted = self.planted_flora.get(key, ())
        capacity = self._planter_capacity(planter)

        title = self.large_font.render(
            f"{planter.name}: посадка растений", True, (150, 245, 190)
        )
        self.screen.blit(title, title.get_rect(center=(SCREEN_SIZE // 2, 60)))
        occupancy = self.small_font.render(
            f"Занято мест: {len(planted)}/{capacity}. Доступны только исследованные сканером виды.",
            True, (225, 225, 225),
        )
        self.screen.blit(occupancy, occupancy.get_rect(center=(SCREEN_SIZE // 2, 96)))

        start_y = 130
        row_h = 45
        for i, flora in enumerate(shown):
            row_y = start_y + i * row_h
            pygame.draw.rect(
                self.screen, (15, 55, 52),
                (105, row_y, SCREEN_SIZE - 210, row_h - 5),
                border_radius=8,
            )
            pygame.draw.rect(
                self.screen, (55, 140, 110),
                (105, row_y, SCREEN_SIZE - 210, row_h - 5),
                1, border_radius=8,
            )
            number = self.font.render(f"{i + 1}.", True, (255, 235, 135))
            self.screen.blit(number, (120, row_y + 9))
            icon = self._fit_surface(flora.image, 30, 30)
            self.screen.blit(icon, icon.get_rect(center=(170, row_y + 20)))
            label = self.font.render(flora.name, True, (225, 245, 235))
            self.screen.blit(label, (195, row_y + 9))

        footer = self.small_font.render(
            f"1–9 — посадить | ← → — страница {self.planting_page + 1}/{max_page + 1} | ESC — закрыть",
            True, (205, 220, 220),
        )
        self.screen.blit(footer, footer.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE - 35)))

    def _apply_repulsion(self, radius=5.0, push=1.6):
        affected = 0
        for animal in self.get_current_animals():
            if animal.hp <= 0 or getattr(animal, "is_companion", False):
                continue
            dx = animal.x - self.player_x
            dy = animal.y - self.player_y
            dist_sq = dx * dx + dy * dy
            if dist_sq <= 0 or dist_sq > radius * radius:
                continue
            dist = math.sqrt(dist_sq)
            old_x, old_y = animal.x, animal.y
            candidate_x = animal.x + (dx / dist) * push
            candidate_y = animal.y + (dy / dist) * push
            if animal.home_biome.contains(candidate_x, candidate_y):
                animal.x = candidate_x
                animal.y = candidate_y
            animal.attack_timer = max(animal.attack_timer, 60)
            animal._update_rotation()
            if not self.in_cave:
                self.world.update_animal_index(animal, old_x, old_y)
            affected += 1
        return affected

    def _use_special_item(self, item):
        if item is first_aid_kit:
            heal = 12
            self.player_hp = min(self.max_player_hp, self.player_hp + heal)
            self._consume_selected_item(item)
            self.notification = f"Аптечка использована. HP: {self.player_hp}/{self.max_player_hp}"
            self.notification_timer = 90
            return True

        if item is flashlight_type:
            self.flashlight_on = not self.flashlight_on
            self.notification = "Фонарик включён" if self.flashlight_on else "Фонарик выключен"
            self.notification_timer = 60
            return True

        if item is seaglide_type:
            self.seaglide_on = not self.seaglide_on
            self.notification = "Морской глайдер активирован" if self.seaglide_on else "Морской глайдер выключен"
            self.notification_timer = 60
            return True

        if item is flare_type:
            self.active_flare_timer = max(self.active_flare_timer, 18 * 60)
            self._consume_selected_item(item)
            self.notification = (
                "Ракета горит: ночью она не отпугивает хищников"
                if self._is_dark_night()
                else "Ракета горит: часть хищников отступает"
            )
            self.notification_timer = 150
            return True

        if item is fire_extinguisher:
            self.damage_resist_timer = max(self.damage_resist_timer, 20 * 60)
            self._consume_selected_item(item)
            self.notification = "Огнетушитель использован: временно снижает получаемый урон"
            self.notification_timer = 120
            return True

        if item is air_bladder:
            self.speed_boost_timer = max(self.speed_boost_timer, 8 * 60)
            self.player_thirst = min(self.max_thirst, self.player_thirst + 10)
            self._consume_selected_item(item)
            self.notification = "Воздушный пузырь использован: краткий рывок и восстановление жажды"
            self.notification_timer = 120
            return True

        if item is scanner_type:
            self.notification = (
                "Сканер выбран: наведите прицел на цель и нажмите ПКМ"
            )
            self.notification_timer = 120
            return True

        if item is pathfinder_tool:
            best = self._find_nearest_path_target()
            if best is None:
                self.notification = "Инструмент исследователя: ориентир не найден"
            else:
                _, x, y, label = best
                self.notification = (
                    f"Инструмент исследователя: ближайший ориентир — {label} ({self._direction_hint(x, y)})"
                )
            self.notification_timer = 120
            return True

        if item is repair_tool:
            healed = min(self.max_player_hp - self.player_hp, 5)
            if healed <= 0:
                self.notification = "Ремонтный инструмент: скафандр не требует обслуживания"
            else:
                self.player_hp += healed
                self.notification = f"Ремонтный инструмент обслужил скафандр. HP +{healed}"
            self.notification_timer = 90
            return True

        if item is propulsion_cannon:
            grid = self._get_current_object_grid()
            best = None
            for (x, y), obj in grid.items():
                if getattr(obj, "is_buildable", False) or getattr(obj, "is_weapon", False):
                    continue
                dx = x - self.player_x
                dy = y - self.player_y
                dist_sq = dx * dx + dy * dy
                if dist_sq <= 16 and (best is None or dist_sq < best[0]):
                    best = (dist_sq, x, y, obj)
            if best is None:
                self.notification = "Пропульсионная пушка: поблизости нет подходящего предмета"
            else:
                _, x, y, obj = best
                if self.add_to_inventory(obj):
                    grid.pop((x, y), None)
                    self.notification = f"Пропульсионная пушка притянула: {obj.name}"
                else:
                    self.notification = "Нет места в инвентаре"
            self.notification_timer = 90
            return True

        if item is repulsion_cannon:
            affected = self._apply_repulsion(radius=5.5, push=1.9)
            self.notification = f"Репульсионная пушка отбросила существ: {affected}"
            self.notification_timer = 90
            return True

        if item is stasis_rifle:
            frozen = 0
            for animal in self.get_current_animals():
                if animal.hp <= 0 or getattr(animal, "is_companion", False):
                    continue
                dx = animal.x - self.player_x
                dy = animal.y - self.player_y
                dist_sq = dx * dx + dy * dy
                if dist_sq <= 36:
                    animal.stasis_timer = max(getattr(animal, "stasis_timer", 0), 6 * 60)
                    frozen += 1
                    if frozen >= 3:
                        break
            self.notification = f"Стазис-винтовка обездвижила существ: {frozen}"
            self.notification_timer = 90
            return True

        if item is laser_cutter:
            hit = False
            for animal in self.get_current_animals():
                if animal.hp <= 0 or getattr(animal, "is_companion", False):
                    continue
                dx = animal.x - self.player_x
                dy = animal.y - self.player_y
                dist_sq = dx * dx + dy * dy
                if dist_sq <= 9:
                    animal.hp -= 18
                    self.notification = f"Лазерный резак повредил {animal.type.name} (HP: {animal.hp})"
                    self.notification_timer = 90
                    if animal.hp <= 0:
                        self.handle_animal_death(animal)
                    hit = True
                    break
            if not hit:
                self.notification = "Лазерный резак: цель слишком далеко"
                self.notification_timer = 90
            return True

        if item is creature_decoy:
            self.active_decoys.append({
                "x": float(self.player_x),
                "y": float(self.player_y),
                "timer": 14 * 60,
                "in_cave": self.in_cave,
            })
            self._consume_selected_item(item)
            self.notification = "Приманка для существ выброшена"
            self.notification_timer = 90
            return True

        return False

    def _base_light_bonus(self):
        # Фонарик и стационарные лампы обрабатываются локальными зонами света
        # в draw_day_night_overlay(), поэтому здесь они больше не осветляют
        # весь экран целиком.
        bonus = 0
        if self.seaglide_on:
            bonus += 12
        if self.active_flare_timer > 0:
            bonus += 28
        return min(55, bonus)

    def _update_base_effects(self):
        self.frame_count += 1
        if self.active_flare_timer > 0:
            self.active_flare_timer -= 1
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
        if self.damage_resist_timer > 0:
            self.damage_resist_timer -= 1
        if self.scanner_highlight_timer > 0:
            self.scanner_highlight_timer -= 1
            if self.scanner_highlight_timer <= 0:
                self.scanner_highlight_cells.clear()

        if self.active_decoys:
            for decoy in self.active_decoys:
                decoy["timer"] -= 1
            self.active_decoys = [d for d in self.active_decoys if d["timer"] > 0]

        if self.frame_count % 15 == 0:
            grid = self._get_current_object_grid()
            traps = [
                (x, y) for (x, y), obj in list(grid.items())
                if obj is grav_trap
            ]
            for tx, ty in traps:
                moved = []
                for (x, y), obj in list(grid.items()):
                    if (x, y) == (tx, ty):
                        continue
                    if getattr(obj, "is_buildable", False) or getattr(obj, "is_weapon", False):
                        continue
                    dx = tx - x
                    dy = ty - y
                    if dx * dx + dy * dy > 9:
                        continue
                    step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
                    step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
                    nx = x + step_x if abs(dx) >= abs(dy) else x
                    ny = y + step_y if abs(dy) > abs(dx) else y
                    if (nx, ny) == (tx, ty) or (nx, ny) not in grid:
                        moved.append(((x, y), (nx, ny), obj))
                for old_pos, new_pos, obj in moved:
                    if old_pos in grid and new_pos not in grid:
                        grid.pop(old_pos, None)
                        grid[new_pos] = obj

        if self.frame_count % 180 != 0:
            return

        nearby = self._nearby_buildables(radius=3.2)
        if not nearby:
            return

        nearby_types = {obj for obj, _x, _y, _d in nearby}

        if any(obj in nearby_types for obj in (bed_type, bench_type, chair_type)):
            self.player_hp = min(self.max_player_hp, self.player_hp + 1)

        if vending_machine in nearby_types:
            self.player_hunger = min(self.max_hunger, self.player_hunger + 2)

        if coffee_machine in nearby_types:
            self.player_thirst = min(self.max_thirst, self.player_thirst + 3)

        if water_filtration_machine in nearby_types:
            self.player_thirst = min(self.max_thirst, self.player_thirst + 2)

        if medical_fabricator in nearby_types and self.frame_count % 720 == 0:
            if self.add_to_inventory(first_aid_kit):
                self.notification = "Изготовитель аптечек выдал новую аптечку"
                self.notification_timer = 90

        if scanner_room_type in nearby_types and self.frame_count % 540 == 0:
            self._scan_environment(passive=True)

        if radio_type in nearby_types and self.frame_count % 900 == 0:
            best = self._find_nearest_path_target()
            if best is not None:
                _, x, y, label = best
                self.notification = f"Радио: ориентир — {label} ({self._direction_hint(x, y)})"
                self.notification_timer = 90

    def use_item(self):
        if self.state not in ("playing", "inventory"):
            return

        if self.active_slot_index == -1:
            self.notification = "Выберите предмет в инвентаре"
            self.notification_timer = 60
            return

        item = self.inventory[self.active_slot_index]

        if item is None:
            self.notification = "Слот пуст"
            self.notification_timer = 60
            return

        if item.edible:
            self.player_hunger = min(
                self.max_hunger, self.player_hunger + item.hunger_value
            )
            self.player_thirst = min(
                self.max_thirst, self.player_thirst + item.thirst_value
            )
            self.player_hp = min(self.max_player_hp, self.player_hp + 2)
            self._consume_selected_item(item)
            self.notification = (
                f"Использовано: {item.name}. HP +2, "
                f"Голод: {self.player_hunger:.0f}, "
                f"Жажда: {self.player_thirst:.0f}"
            )
            self.notification_timer = 60
            return

        if self._use_special_item(item):
            return

        self.notification = "У этого предмета пока нет активного применения"
        self.notification_timer = 60

    def pick_up(self):
        player_x = int(self.player_x)
        player_y = int(self.player_y)

        dropped = self._current_dropped_items()
        dropped_stack = dropped.get((player_x, player_y))
        if dropped_stack:
            item = dropped_stack[-1]
            if self.add_to_inventory(item):
                dropped_stack.pop()
                if not dropped_stack:
                    dropped.pop((player_x, player_y), None)
                self.notification = f"Подобрано: {item.name}"
                self.notification_timer = 40
            else:
                self.notification = "Нет места в инвентаре!"
                self.notification_timer = 60
            return

        if self.in_cave:
            obj = self.cave_world.get_object_at(player_x, player_y)
        else:
            obj = self.world.get_object_at(player_x, player_y)

        if obj is not None and not obj.is_buildable:
            if self.add_to_inventory(obj):
                if self.in_cave:
                    self.cave_world.remove_object_at(player_x, player_y)
                else:
                    self.world.remove_object_at(player_x, player_y)

                self.notification = f"Подобрано: {obj.name}"
                self.notification_timer = 40
            else:
                self.notification = "Нет места в инвентаре!"
                self.notification_timer = 60
            return

        animals = self.get_current_animals()

        for animal in list(animals):
            if getattr(animal, "is_companion", False):
                continue
            if (int(animal.x) != player_x
                    or int(animal.y) != player_y):
                continue

            if animal.hp > 0 and animal.type.behavior == "predator":
                self.notification = "Хищник жив, убейте его!"
                self.notification_timer = 60
                return

            if self.add_to_inventory(animal.type):
                self.remove_current_animal(animal)
                self.notification = f"Подобран {animal.type.name}"
                self.notification_timer = 60
            else:
                self.notification = "Нет места в инвентаре!"
                self.notification_timer = 60
            return

    def build(self):
        if self.state != "playing":
            return

        if self.active_slot_index == -1:
            self.notification = "Выберите предмет в инвентаре"
            self.notification_timer = 60
            return

        item = self.inventory[self.active_slot_index]

        if item is None:
            self.notification = "Слот пуст"
            self.notification_timer = 60
            return

        if not item.is_buildable:
            self.notification = "Этот предмет нельзя установить"
            self.notification_timer = 60
            return

        if (getattr(item, "requires_habitat_builder", False)
                and self.inventory_counts.get(habitat_builder_type, 0) <= 0):
            self.notification = "Для установки нужен Строитель"
            self.notification_timer = 90
            return

        player_x = int(self.player_x)
        player_y = int(self.player_y)

        active_world = self.cave_world if self.in_cave else self.world

        if active_world.get_object_at(player_x, player_y) is not None:
            self.notification = "Клетка занята"
            self.notification_timer = 60
            return

        active_world.object_grid[(player_x, player_y)] = item
        self.inventory[self.active_slot_index] = None
        self.inventory_counts[item] -= 1

        if self.inventory_counts[item] <= 0:
            del self.inventory_counts[item]

        self.active_slot_index = -1
        self.notification = f"Установлено: {item.name}"
        self.notification_timer = 60

        if item.is_wall:
            self.notification = "Стена установлена под игроком"
            self.notification_timer = 120

    def destroy_build(self):
        if self.state != "playing":
            return

        player_x = int(self.player_x)
        player_y = int(self.player_y)

        active_world = self.cave_world if self.in_cave else self.world
        obj = active_world.get_object_at(player_x, player_y)

        if obj is None or not obj.is_buildable:
            self.notification = "Здесь нет постройки"
            self.notification_timer = 60
            return

        active_world.remove_object_at(player_x, player_y)
        self.planted_flora.pop(
            (bool(self.in_cave), player_x, player_y), None
        )

        if self.add_to_inventory(obj):
            self.notification = f"Разрушено: {obj.name}"
        else:
            self.notification = "Инвентарь полон. Предмет потерян."

        self.notification_timer = 60

    # =====================================================
    # БЛИЖНИЙ БОЙ / СТРЕЛЬБА
    # =====================================================

    def attack(self):
        if self.state != "playing":
            return

        player_x = self.player_x
        player_y = self.player_y

        max_distance_squared = (
            self.player_attack_range ** 2
        )

        for animal in list(self.get_current_animals()):
            if animal.hp <= 0:
                continue
            if getattr(animal, "is_companion", False):
                continue

            dx = animal.x - player_x
            dy = animal.y - player_y

            distance_squared = dx * dx + dy * dy

            if distance_squared > max_distance_squared:
                continue

            animal.hp -= self.player_attack_damage

            self.notification = (
                f"Атакован {animal.type.name}, HP: {animal.hp}"
            )
            self.notification_timer = 30

            if animal.hp <= 0:
                self.handle_animal_death(animal)
            break

    def shoot(self, target_x, target_y):
        if self.state != "playing":
            return

        weapon = self.equipped_weapon
        if weapon is None:
            self.notification = "Нет экипированного оружия!"
            self.notification_timer = 60
            return

        target_dx = target_x - self.player_x
        target_dy = target_y - self.player_y

        target_distance_squared = target_dx ** 2 + target_dy ** 2
        if target_distance_squared <= 0:
            return

        target_length = math.sqrt(target_distance_squared)
        target_dx /= target_length
        target_dy /= target_length

        best_animal = None
        best_distance_squared = float("inf")

        max_range_squared = weapon.weapon_range ** 2
        cos_threshold = math.cos(math.radians(30))

        for animal in self.get_current_animals():
            if animal.hp <= 0:
                continue
            if getattr(animal, "is_companion", False):
                continue

            dx = animal.x - self.player_x
            dy = animal.y - self.player_y

            distance_squared = dx * dx + dy * dy
            if distance_squared > max_range_squared:
                continue
            if distance_squared <= 0:
                continue

            distance = math.sqrt(distance_squared)
            direction_x = dx / distance
            direction_y = dy / distance

            dot = direction_x * target_dx + direction_y * target_dy

            if (dot >= cos_threshold
                    and distance_squared < best_distance_squared):
                best_distance_squared = distance_squared
                best_animal = animal

        if best_animal is None:
            self.notification = "Промах!"
            self.notification_timer = 30
            return

        best_animal.hp -= weapon.damage

        self.notification = (
            f"{weapon.name} поразил {best_animal.type.name} "
            f"(HP: {best_animal.hp})"
        )
        self.notification_timer = 60

        if best_animal.hp <= 0:
            self.handle_animal_death(best_animal)

    # =====================================================
    # СТАРТОВАЯ КАПСУЛА / ЗОНА КРАФТА
    # =====================================================

    def is_inside_start_capsule(self, x, y):
        x1, y1, x2, y2 = self.start_capsule_rect
        return x1 <= int(x) <= x2 and y1 <= int(y) <= y2

    def is_inside_capsule_crafting_area(self, x, y):
        x1, y1, x2, y2 = self.start_capsule_inner_rect
        return x1 <= int(x) <= x2 and y1 <= int(y) <= y2

    def is_start_capsule_wall(self, x, y):
        x = int(x)
        y = int(y)

        if not self.is_inside_start_capsule(x, y):
            return False

        if (x, y) in self.start_capsule_door_cells:
            return False

        x1, y1, x2, y2 = self.start_capsule_rect
        return x in (x1, x2) or y in (y1, y2)

    def is_start_capsule_passage(self, x, y):
        cell = (int(x), int(y))
        return (
            self.is_inside_capsule_crafting_area(*cell)
            or cell in self.start_capsule_door_cells
        )

    def get_available_crafting_stations(self):
        """Return crafting stations currently usable by the player."""
        stations = []
        player_x = int(self.player_x)
        player_y = int(self.player_y)
        active_world = self.cave_world if self.in_cave else self.world
        obj = active_world.get_object_at(player_x, player_y)

        # The old 2D rule is retained: the escape pod and a crafted floor
        # act as the basic Fabricator access point.
        if self.in_cave:
            if obj is floor_type:
                stations.append("Изготовитель")
        else:
            if self.is_inside_capsule_crafting_area(player_x, player_y):
                stations.append("Изготовитель")
            elif obj is floor_type:
                stations.append("Изготовитель")

        station_name = getattr(obj, "crafting_station_name", None)
        if station_name and station_name not in stations:
            stations.append(station_name)

        # Habitat Builder is a hand tool in the original game, so its recipes
        # are available wherever the player carries one.
        if self.inventory_counts.get(habitat_builder_type, 0) > 0:
            if "Строитель" not in stations:
                stations.append("Строитель")

        return stations

    def get_active_crafting_station(self):
        stations = self.get_available_crafting_stations()
        if not stations:
            return None
        self.craft_station_index %= len(stations)
        return stations[self.craft_station_index]

    def get_crafting_location_name(self):
        return self.get_active_crafting_station()

    def get_current_station_recipes(self):
        station = self.get_active_crafting_station()
        if station is None:
            return []
        return [recipe for recipe in recipes if recipe.station == station]

    def can_craft_here(self):
        return bool(self.get_available_crafting_stations())

    def draw_start_capsule_cell(self, x, y, screen_x, screen_y):
        """Рисует детализированную клетку стартовой капсулы."""
        if not self.is_inside_start_capsule(x, y):
            return False

        x1, y1, x2, y2 = self.start_capsule_rect
        cell_rect = pygame.Rect(
            screen_x, screen_y, CELL_SIZE, CELL_SIZE
        )
        inner_rect = cell_rect.inflate(-4, -4)
        cell = (x, y)

        if self.is_inside_capsule_crafting_area(x, y):
            pygame.draw.rect(self.screen, (34, 58, 68), cell_rect)
            pygame.draw.rect(self.screen, (54, 82, 92), inner_rect)
            pygame.draw.rect(self.screen, (90, 118, 124), inner_rect, 1)

            pygame.draw.line(
                self.screen, (42, 68, 78),
                (screen_x + CELL_SIZE // 2, screen_y + 3),
                (screen_x + CELL_SIZE // 2, screen_y + CELL_SIZE - 3),
                1
            )
            pygame.draw.line(
                self.screen, (42, 68, 78),
                (screen_x + 3, screen_y + CELL_SIZE // 2),
                (screen_x + CELL_SIZE - 3, screen_y + CELL_SIZE // 2),
                1
            )

            for rx, ry in ((6, 6), (CELL_SIZE - 7, 6),
                           (6, CELL_SIZE - 7),
                           (CELL_SIZE - 7, CELL_SIZE - 7)):
                pygame.draw.circle(
                    self.screen, (150, 170, 174),
                    (screen_x + rx, screen_y + ry), 1
                )

            if y == y1 + 1 and x in (x1 + 2, x2 - 2):
                pygame.draw.rect(
                    self.screen, (15, 45, 58),
                    (screen_x + 7, screen_y + 5, CELL_SIZE - 14, 6),
                    border_radius=2
                )
                pygame.draw.rect(
                    self.screen, (70, 220, 240),
                    (screen_x + 9, screen_y + 7, CELL_SIZE - 18, 2)
                )

            if x == x1 + 1 and y in (y1 + 2, y2 - 2):
                pygame.draw.rect(
                    self.screen, (70, 78, 82),
                    (screen_x + 4, screen_y + 6, 5, CELL_SIZE - 12),
                    border_radius=2
                )
                pygame.draw.circle(
                    self.screen, (80, 255, 150),
                    (screen_x + 6, screen_y + CELL_SIZE // 2), 2
                )
            return True

        if cell in self.start_capsule_door_cells:
            pygame.draw.rect(self.screen, (44, 52, 58), cell_rect)
            pygame.draw.rect(self.screen, (105, 116, 120), inner_rect, 2)
            pygame.draw.line(
                self.screen, (230, 150, 45),
                (screen_x + 4, screen_y + 6),
                (screen_x + CELL_SIZE - 4, screen_y + CELL_SIZE - 6),
                3
            )
            pygame.draw.line(
                self.screen, (40, 45, 48),
                (screen_x + 4, screen_y + 12),
                (screen_x + CELL_SIZE - 4, screen_y + CELL_SIZE - 0),
                3
            )
            pygame.draw.circle(
                self.screen, (80, 235, 255),
                (screen_x + CELL_SIZE // 2, screen_y + 5), 2
            )
            return True

        pygame.draw.rect(self.screen, (126, 139, 143), cell_rect)
        pygame.draw.rect(self.screen, (74, 86, 90), inner_rect)
        pygame.draw.rect(self.screen, (177, 188, 190), cell_rect, 2)
        pygame.draw.rect(self.screen, (36, 47, 52), inner_rect, 1)

        pygame.draw.line(
            self.screen, (105, 118, 122),
            (screen_x + 4, screen_y + CELL_SIZE // 2),
            (screen_x + CELL_SIZE - 4, screen_y + CELL_SIZE // 2),
            1
        )
        pygame.draw.circle(
            self.screen, (210, 218, 220),
            (screen_x + 5, screen_y + 5), 1
        )
        pygame.draw.circle(
            self.screen, (210, 218, 220),
            (screen_x + CELL_SIZE - 6, screen_y + CELL_SIZE - 6), 1
        )

        if y == y1 and x in (x1 + 2, x1 + 5):
            pygame.draw.ellipse(
                self.screen, (18, 45, 62),
                (screen_x + 6, screen_y + 8, CELL_SIZE - 12, 13)
            )
            pygame.draw.ellipse(
                self.screen, (72, 185, 215),
                (screen_x + 8, screen_y + 10, CELL_SIZE - 16, 9), 2
            )
            pygame.draw.line(
                self.screen, (185, 235, 245),
                (screen_x + 11, screen_y + 12),
                (screen_x + CELL_SIZE - 12, screen_y + 12), 1
            )

        if x in (x1, x2) and y in (y1 + 1, y2 - 1):
            pygame.draw.rect(
                self.screen, (214, 116, 28),
                (screen_x + 3, screen_y + 5, 4, CELL_SIZE - 10)
            )
        if y == y2 and x in (x1 + 1, x2 - 1):
            pygame.draw.circle(
                self.screen, (255, 190, 55),
                (screen_x + CELL_SIZE // 2, screen_y + 7), 2
            )

        return True

    # =====================================================
    # АВРОРА (стиль стартовой капсулы)
    # =====================================================

    def is_aurora_biome(self, biome):
        """Проверяет, нужно ли рисовать клетку металлическим стилем Авроры."""
        if biome is None:
            return False

        if getattr(biome, "aurora_style", False):
            return True

        name = biome.name
        return ("Аврор" in name) or ("Двигательный отсек" in name)

    def draw_aurora_cell(self, x, y, screen_x, screen_y, biome):
        """Рисует клетку Авроры в стиле стартовой капсулы:
        непроходимые клетки — как наружный корпус,
        проходимые — как внутренний металлический настил."""
        cell_rect = pygame.Rect(
            screen_x, screen_y, CELL_SIZE, CELL_SIZE
        )
        inner_rect = cell_rect.inflate(-4, -4)

        if not biome.passable:
            # -------- Стена Авроры: наружный корпус капсулы --------
            pygame.draw.rect(self.screen, (126, 139, 143), cell_rect)
            pygame.draw.rect(self.screen, (74, 86, 90), inner_rect)
            pygame.draw.rect(self.screen, (177, 188, 190), cell_rect, 2)
            pygame.draw.rect(self.screen, (36, 47, 52), inner_rect, 1)

            pygame.draw.line(
                self.screen, (105, 118, 122),
                (screen_x + 4, screen_y + CELL_SIZE // 2),
                (screen_x + CELL_SIZE - 4, screen_y + CELL_SIZE // 2),
                1
            )
            pygame.draw.circle(
                self.screen, (210, 218, 220),
                (screen_x + 5, screen_y + 5), 1
            )
            pygame.draw.circle(
                self.screen, (210, 218, 220),
                (screen_x + CELL_SIZE - 6,
                 screen_y + CELL_SIZE - 6), 1
            )

            # Иллюминатор детерминированно на части стен.
            if (x * 7 + y * 3) % 11 == 0:
                pygame.draw.ellipse(
                    self.screen, (18, 45, 62),
                    (screen_x + 6, screen_y + 8,
                     CELL_SIZE - 12, 13)
                )
                pygame.draw.ellipse(
                    self.screen, (72, 185, 215),
                    (screen_x + 8, screen_y + 10,
                     CELL_SIZE - 16, 9), 2
                )
                pygame.draw.line(
                    self.screen, (185, 235, 245),
                    (screen_x + 11, screen_y + 12),
                    (screen_x + CELL_SIZE - 12, screen_y + 12), 1
                )

            # Сигнальные аварийные лампы.
            if (x + y) % 13 == 0:
                pygame.draw.circle(
                    self.screen, (255, 190, 55),
                    (screen_x + CELL_SIZE // 2, screen_y + 6), 2
                )

            # Аварийная оранжевая полоса на некоторых стенах.
            if (x * 3 + y * 5) % 17 == 0:
                pygame.draw.rect(
                    self.screen, (214, 116, 28),
                    (screen_x + 3, screen_y + 5,
                     4, CELL_SIZE - 10)
                )
            return

        # -------- Помещение Авроры: внутренний настил капсулы --------
        pygame.draw.rect(self.screen, (34, 58, 68), cell_rect)
        pygame.draw.rect(self.screen, (54, 82, 92), inner_rect)
        pygame.draw.rect(self.screen, (90, 118, 124), inner_rect, 1)

        pygame.draw.line(
            self.screen, (42, 68, 78),
            (screen_x + CELL_SIZE // 2, screen_y + 3),
            (screen_x + CELL_SIZE // 2, screen_y + CELL_SIZE - 3),
            1
        )
        pygame.draw.line(
            self.screen, (42, 68, 78),
            (screen_x + 3, screen_y + CELL_SIZE // 2),
            (screen_x + CELL_SIZE - 3, screen_y + CELL_SIZE // 2),
            1
        )

        for rx, ry in ((6, 6), (CELL_SIZE - 7, 6),
                       (6, CELL_SIZE - 7),
                       (CELL_SIZE - 7, CELL_SIZE - 7)):
            pygame.draw.circle(
                self.screen, (150, 170, 174),
                (screen_x + rx, screen_y + ry), 1
            )

        # Встроенные панели подсветки.
        if (x + y) % 5 == 0:
            pygame.draw.rect(
                self.screen, (15, 45, 58),
                (screen_x + 7, screen_y + 5,
                 CELL_SIZE - 14, 6),
                border_radius=2
            )
            pygame.draw.rect(
                self.screen, (70, 220, 240),
                (screen_x + 9, screen_y + 7,
                 CELL_SIZE - 18, 2)
            )

    # =====================================================
    # МЕНЮ
    # =====================================================

    def toggle_inventory(self):
        if self.state == "playing":
            self.state = "inventory"
        elif self.state == "inventory":
            self.state = "playing"
            self.notification = ""
        else:
            self.state = "playing"
            self.selected_biome = None

    def toggle_crafting(self):
        if self.state == "crafting":
            self.state = "playing"
            self.notification = ""
            return

        if not self.can_craft_here():
            self.notification = (
                "Крафт доступен только в капсуле или на построенном полу"
            )
            self.notification_timer = 120
            return

        self.state = "crafting"
        self.craft_page = 0
        self.craft_station_index = 0
        self.selected_biome = None

    def toggle_map(self):
        if self.state == "playing":
            self.state = "map"
            self.map_center_x = self.player_x
            self.map_center_y = self.player_y
            self.selected_biome = None
        elif self.state == "map":
            self.state = "playing"
            self.selected_biome = None

    def toggle_pet_list(self):
        if self.state == "pets":
            self.state = "playing"
            self.notification = ""
            return
        self.state = "pets"
        self.pet_list_page = 0
        self.selected_pet = None
        self.selected_biome = None

    def select_pet_from_list(self, number):
        """Клавиши 1–9 выбирают питомца именно на текущей странице."""
        pets = self._get_all_companions()
        index = self.pet_list_page * self.pets_per_page + number - 1
        if 1 <= number <= 9 and 0 <= index < len(pets):
            self.selected_pet = pets[index]
        else:
            self.selected_pet = None
            self.notification = "На этой позиции нет питомца"
            self.notification_timer = 70

    def _get_selected_pet(self):
        pet = self.selected_pet
        if pet is not None and pet in self._get_all_companions() and pet.hp > 0:
            return pet
        self.selected_pet = None
        self.notification = "Сначала выберите питомца клавишей 1–9"
        self.notification_timer = 80
        return None

    def return_selected_pet_to_inventory(self):
        """E: отозвать выбранного спутника с поверхности или из пещеры."""
        pet = self._get_selected_pet()
        if pet is None:
            return
        free_slot = next(
            (i for i, item in enumerate(self.inventory) if item is None), None
        )
        if free_slot is None or not self.add_to_inventory(pet.type):
            self.notification = "Инвентарь заполнен — забрать питомца нельзя"
            self.notification_timer = 110
            return
        self._stored_companion_hp[free_slot] = (pet.type, pet.hp)
        self._clear_companion_target(pet)
        for animal in list(self.world.animals) + list(self.cave_animals):
            if getattr(animal, "pet_combat_target", None) is pet:
                animal.pet_combat_target = None
        if pet in self.cave_animals:
            self.cave_animals.remove(pet)
        else:
            self.world.remove_animal(pet)
        self.selected_pet = None
        self.pet_list_page = min(
            self.pet_list_page,
            max(0, (len(self._get_all_companions()) - 1) // self.pets_per_page)
        )
        self.notification = f"{pet.type.name} возвращён в инвентарь (HP {int(pet.hp)})"
        self.notification_timer = 110

    def heal_selected_pet(self):
        """U: одна аптечка восстанавливает до 35 HP выбранному питомцу."""
        pet = self._get_selected_pet()
        if pet is None:
            return
        if pet.hp >= pet.max_hp:
            self.notification = f"У {pet.type.name} уже полное здоровье"
            self.notification_timer = 80
            return
        if self.inventory_counts.get(first_aid_kit, 0) <= 0:
            self.notification = "Для лечения питомца нужна аптечка"
            self.notification_timer = 100
            return
        if not self._remove_inventory_items_of_type(first_aid_kit, 1):
            self.notification = "Не удалось использовать аптечку"
            self.notification_timer = 90
            return
        restored = min(35, pet.max_hp - pet.hp)
        pet.hp += restored
        self.notification = (
            f"{pet.type.name}: +{int(restored)} HP "
            f"({int(pet.hp)}/{int(pet.max_hp)}), потрачена 1 аптечка"
        )
        self.notification_timer = 110

    # =====================================================
    # КАРТА
    # =====================================================

    def map_screen_to_world(self, screen_x, screen_y):
        scale = self.map_base_scale * self.map_zoom
        center_x = SCREEN_SIZE / 2
        center_y = SCREEN_SIZE / 2

        world_x = (screen_x - center_x) / scale + self.map_center_x
        world_y = (screen_y - center_y) / scale + self.map_center_y

        return world_x, world_y

    def map_select_biome(self, screen_x, screen_y):
        world_x, world_y = self.map_screen_to_world(
            screen_x, screen_y
        )

        self.selected_biome = None

        if self.in_cave:
            for tunnel in reversed(self.cave_tunnels):
                if tunnel.contains(world_x, world_y):
                    self.selected_biome = tunnel
                    self.notification = f"Выбрано: {tunnel.name}"
                    self.notification_timer = 60
                    return

        biome = self.world.get_biome_at(world_x, world_y)

        if biome is not None:
            self.selected_biome = biome
            self.notification = f"Выбран биом: {biome.name}"
            self.notification_timer = 60
            return

        self.notification = "Открытый океан"
        self.notification_timer = 30

    def update_map_pan(self):
        keys = pygame.key.get_pressed()
        pan = 12 / self.map_zoom

        if keys[pygame.K_LEFT]:
            self.map_center_x -= pan
        if keys[pygame.K_RIGHT]:
            self.map_center_x += pan
        if keys[pygame.K_UP]:
            self.map_center_y -= pan
        if keys[pygame.K_DOWN]:
            self.map_center_y += pan
        joy_x, joy_y = self.mobile_controls.movement()
        self.map_center_x += joy_x * pan
        self.map_center_y += joy_y * pan

        self.map_center_x = max(0, min(MAP_SIZE, self.map_center_x))
        self.map_center_y = max(0, min(MAP_SIZE, self.map_center_y))

    def biome_screen_polygon(self, biome, scale, center_x, center_y):
        points = []

        for world_x, world_y in biome.map_points():
            screen_x = (
                center_x
                + (world_x - self.map_center_x) * scale
            )
            screen_y = (
                center_y
                + (world_y - self.map_center_y) * scale
            )
            points.append((int(screen_x), int(screen_y)))

        return points

    def draw_map_biome_label(self, biome, scale, center_x, center_y):
        if not biome.map_label or self.map_zoom < 0.55:
            return

        wx, wy = biome.center()
        sx = int(center_x + (wx - self.map_center_x) * scale)
        sy = int(center_y + (wy - self.map_center_y) * scale)

        lines = biome.map_label.split("\n")
        line_height = 16
        start_y = sy - (len(lines) * line_height) // 2

        for index, line in enumerate(lines):
            shadow = self.tiny_font.render(line, True, (0, 0, 0))
            label = self.tiny_font.render(line, True, (245, 245, 245))
            rect = label.get_rect(
                center=(sx, start_y + index * line_height)
            )
            shadow_rect = rect.copy()
            shadow_rect.x += 2
            shadow_rect.y += 2
            self.screen.blit(shadow, shadow_rect)
            self.screen.blit(label, rect)

    def draw_caves_on_world_map(self, scale, center_x, center_y):
        overlay = pygame.Surface(
            (SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA
        )
        base_alpha = 115 if self.in_cave else 65
        current_tunnel = None

        if self.in_cave:
            current_tunnel = self.get_cave_tunnel_at(
                self.player_x, self.player_y
            )

        for tunnel in self.cave_tunnels:
            points = self.biome_screen_polygon(
                tunnel, scale, center_x, center_y
            )

            if len(points) < 3:
                continue

            if tunnel is current_tunnel:
                fill = (40, 245, 255, 165)
                border = (210, 255, 255, 220)
            else:
                fill = (20, 205, 220, base_alpha)
                border = (
                    120, 245, 250,
                    min(190, base_alpha + 60)
                )

            pygame.draw.polygon(overlay, fill, points)
            pygame.draw.polygon(overlay, border, points, 1)

        self.screen.blit(overlay, (0, 0))

        for entrance in self.cave_entrances:
            x1, y1, _, _ = entrance["surface_rect"]
            sx = int(center_x + (x1 - self.map_center_x) * scale)
            sy = int(center_y + (y1 - self.map_center_y) * scale)
            radius = max(3, int(5 * self.map_zoom))
            radius = min(radius, 8)

            pygame.draw.circle(
                self.screen, (15, 40, 45),
                (sx, sy), radius + 2
            )
            pygame.draw.circle(
                self.screen, (90, 245, 255),
                (sx, sy), radius, 2
            )

    def draw_map(self):
        self.screen.fill((4, 6, 9))

        scale = self.map_base_scale * self.map_zoom
        center_x = SCREEN_SIZE // 2
        center_y = SCREEN_SIZE // 2

        ordered_biomes = sorted(
            self.world.biomes,
            key=lambda biome: biome.priority
        )

        for biome in ordered_biomes:
            points = self.biome_screen_polygon(
                biome, scale, center_x, center_y
            )

            if len(points) < 3:
                continue

            xs = [p[0] for p in points]
            ys = [p[1] for p in points]

            if (
                max(xs) < -30
                or min(xs) > SCREEN_SIZE + 30
                or max(ys) < -30
                or min(ys) > SCREEN_SIZE + 30
            ):
                continue

            pygame.draw.polygon(self.screen, biome.color, points)

            if biome is self.selected_biome:
                border_color = (255, 235, 80)
                border_width = 3
            else:
                border_color = (
                    max(0, biome.color[0] - 50),
                    max(0, biome.color[1] - 50),
                    max(0, biome.color[2] - 50)
                )
                border_width = 1

            pygame.draw.polygon(
                self.screen, border_color, points, border_width
            )

        self.draw_caves_on_world_map(scale, center_x, center_y)

        for biome in self.world.biomes:
            if biome.cave_enabled:
                self.draw_map_biome_label(
                    biome, scale, center_x, center_y
                )

        player_screen_x = int(
            center_x + (self.player_x - self.map_center_x) * scale
        )
        player_screen_y = int(
            center_y + (self.player_y - self.map_center_y) * scale
        )

        if (
            -20 <= player_screen_x <= SCREEN_SIZE + 20
            and -20 <= player_screen_y <= SCREEN_SIZE + 20
        ):
            pygame.draw.circle(
                self.screen, (0, 90, 230),
                (player_screen_x, player_screen_y), 7
            )
            pygame.draw.circle(
                self.screen, (255, 255, 255),
                (player_screen_x, player_screen_y), 7, 2
            )

        map_title = (
            "КАРТА МИРА — ПЕЩЕРНЫЙ УРОВЕНЬ"
            if self.in_cave
            else "КАРТА МИРА"
        )
        title = self.large_font.render(
            map_title, True, (255, 255, 255)
        )
        self.screen.blit(
            title,
            title.get_rect(center=(SCREEN_SIZE // 2, 26))
        )

        zoom_text = self.small_font.render(
            f"Зум: {self.map_zoom:.2f}x", True, (255, 255, 255)
        )
        self.screen.blit(zoom_text, (10, 10))

        if self.selected_biome:
            self.draw_biome_info_panel()

        controls = self.tiny_font.render(
            "M/ESC: закрыть | +/-: зум | "
            "стрелки: движение | клик: биом",
            True, (220, 220, 220)
        )
        self.screen.blit(
            controls,
            controls.get_rect(
                center=(SCREEN_SIZE // 2, SCREEN_SIZE - 15)
            )
        )

    def draw_cave_map(self):
        self.screen.fill((8, 8, 12))

        scale = self.map_base_scale * self.map_zoom
        center_x = SCREEN_SIZE // 2
        center_y = SCREEN_SIZE // 2

        for tunnel in self.cave_tunnels:
            x1, y1, x2, y2 = tunnel.rect
            sx1 = center_x + (x1 - self.map_center_x) * scale
            sy1 = center_y + (y1 - self.map_center_y) * scale
            sx2 = center_x + (x2 + 1 - self.map_center_x) * scale
            sy2 = center_y + (y2 + 1 - self.map_center_y) * scale

            rect = pygame.Rect(
                int(sx1), int(sy1),
                max(2, int(sx2 - sx1)),
                max(2, int(sy2 - sy1))
            )
            pygame.draw.rect(self.screen, tunnel.color, rect)
            border = (
                (255, 230, 90) if tunnel is self.selected_biome
                else (85, 95, 110)
            )
            pygame.draw.rect(
                self.screen, border, rect,
                3 if tunnel is self.selected_biome else 1
            )

        for entrance in self.cave_entrances:
            x1, y1, x2, y2 = entrance["cave_rect"]
            sx1 = center_x + (x1 - self.map_center_x) * scale
            sy1 = center_y + (y1 - self.map_center_y) * scale
            sx2 = center_x + (x2 + 1 - self.map_center_x) * scale
            sy2 = center_y + (y2 + 1 - self.map_center_y) * scale
            rect = pygame.Rect(
                int(sx1), int(sy1),
                max(4, int(sx2 - sx1)),
                max(4, int(sy2 - sy1))
            )
            pygame.draw.rect(self.screen, (20, 80, 110), rect)
            pygame.draw.rect(
                self.screen, (180, 235, 255), rect, 2
            )

        player_x = center_x + (self.player_x - self.map_center_x) * scale
        player_y = center_y + (self.player_y - self.map_center_y) * scale
        pygame.draw.circle(
            self.screen, (0, 120, 230),
            (int(player_x), int(player_y)), 8
        )
        pygame.draw.circle(
            self.screen, (255, 255, 255),
            (int(player_x), int(player_y)), 8, 2
        )

        title = self.large_font.render(
            "КАРТА ПЕЩЕР", True, (255, 255, 255)
        )
        self.screen.blit(
            title, title.get_rect(center=(SCREEN_SIZE // 2, 26))
        )

        zoom_text = self.small_font.render(
            f"Зум: {self.map_zoom:.2f}x", True, (255, 255, 255)
        )
        self.screen.blit(zoom_text, (10, 10))

        if self.selected_biome:
            self.draw_biome_info_panel()

        controls = self.tiny_font.render(
            "M/ESC: закрыть | +/-: зум | "
            "стрелки: движение | клик: секция",
            True, (220, 220, 220)
        )
        self.screen.blit(
            controls,
            controls.get_rect(
                center=(SCREEN_SIZE // 2, SCREEN_SIZE - 15)
            )
        )

    def draw_biome_info_panel(self):
        biome = self.selected_biome
        if biome is None:
            return

        panel_width = 250
        panel_height = SCREEN_SIZE - 100
        panel_x = 10
        panel_y = 70

        panel = pygame.Surface(
            (panel_width, panel_height), pygame.SRCALPHA
        )
        panel.fill((15, 15, 25, 235))
        self.screen.blit(panel, (panel_x, panel_y))

        pygame.draw.rect(
            self.screen, (255, 215, 0),
            (panel_x, panel_y, panel_width, panel_height), 2
        )

        y = panel_y + 10

        name = self.small_font.render(
            biome.name, True, (255, 255, 200)
        )
        self.screen.blit(name, (panel_x + 10, y))
        y += 28

        x1, y1, x2, y2 = biome.rect
        lines = [
            f"({x1}, {y1}) — ({x2}, {y2})",
            f"Площадь: ~{int(biome.area())} клеток",
            "Проходимость: " + ("Да" if biome.passable else "Нет")
        ]

        for line in lines:
            text = self.tiny_font.render(
                line, True, (230, 230, 230)
            )
            self.screen.blit(text, (panel_x + 10, y))
            y += 18

        y += 8

        heading = self.small_font.render(
            "Ресурсы:", True, (180, 255, 180)
        )
        self.screen.blit(heading, (panel_x + 10, y))
        y += 20

        if biome.objects:
            for (obj, density) in biome.objects:
                text = self.tiny_font.render(
                    f"• {obj.name} (пл. {density})",
                    True, (220, 220, 220)
                )
                self.screen.blit(text, (panel_x + 15, y))
                y += 17
        else:
            text = self.tiny_font.render(
                "— нет", True, (150, 150, 150)
            )
            self.screen.blit(text, (panel_x + 15, y))
            y += 17

        y += 8

        heading = self.small_font.render(
            "Флора:", True, (170, 235, 255)
        )
        self.screen.blit(heading, (panel_x + 10, y))
        y += 20

        if getattr(biome, "flora", None):
            for flora, density in biome.flora:
                text = self.tiny_font.render(
                    f"• {flora.name} (пл. {density:.2g})",
                    True, (220, 220, 220)
                )
                self.screen.blit(text, (panel_x + 15, y))
                y += 17
                if y > panel_y + panel_height - 105:
                    more = self.tiny_font.render(
                        "• …", True, (160, 160, 160)
                    )
                    self.screen.blit(more, (panel_x + 15, y))
                    y += 17
                    break
        else:
            text = self.tiny_font.render(
                "— нет", True, (150, 150, 150)
            )
            self.screen.blit(text, (panel_x + 15, y))
            y += 17

        y += 8

        heading = self.small_font.render(
            "Живность:", True, (255, 200, 200)
        )
        self.screen.blit(heading, (panel_x + 10, y))
        y += 20

        if biome.animals:
            for (animal, count) in biome.animals:
                text = self.tiny_font.render(
                    f"• {animal.name} ×{count}",
                    True, (220, 220, 220)
                )
                self.screen.blit(text, (panel_x + 15, y))
                y += 17
        else:
            text = self.tiny_font.render(
                "— нет", True, (150, 150, 150)
            )
            self.screen.blit(text, (panel_x + 15, y))

    # =====================================================
    # КАМЕРА
    # =====================================================

    def get_camera_origin(self):
        """Исходное положение камеры (используется логикой игры)."""
        return (
            self.player_x - VIEW_RADIUS,
            self.player_y - VIEW_RADIUS
        )

    def get_render_camera_origin(self):
        """Камера отрисовки: радиус меняется с масштабом изображения."""
        return (
            self.player_x - self._render_view_radius,
            self.player_y - self._render_view_radius
        )

    def screen_to_world(self, mouse_x, mouse_y):
        """Точное наведение, взаимодействие и сканирование с учётом зума."""
        tile_pixels = CELL_SIZE * self.camera_zoom
        return (
            self.player_x + 0.5 + (mouse_x - SCREEN_SIZE / 2) / tile_pixels,
            self.player_y + 0.5 + (mouse_y - SCREEN_SIZE / 2) / tile_pixels
        )

    @staticmethod
    def _make_blue_edge_haze():
        """Голубая дымка: максимальна по краям, прозрачна в центре."""
        haze = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA)
        fade_width = int(SCREEN_SIZE * 0.39)
        for inset in range(fade_width):
            fraction = 1.0 - inset / max(1, fade_width - 1)
            alpha = round(195 * fraction ** 2.15)
            if alpha < 1:
                continue
            length = SCREEN_SIZE - 2 * inset
            if length <= 0:
                break
            pygame.draw.rect(
                haze, (50, 167, 224, alpha),
                pygame.Rect(inset, inset, length, length), 1
            )
        return haze.convert_alpha()

    def _draw_blue_edge_haze(self):
        if self.camera_zoom >= 1.0:
            return
        amount = (1.0 - self.camera_zoom) / (1.0 - CAMERA_ZOOM_MIN)
        self._blue_edge_haze.set_alpha(round(255 * max(0.0, min(1.0, amount))))
        self.screen.blit(self._blue_edge_haze, (0, 0))

    def _change_camera_zoom(self, wheel_steps):
        if not wheel_steps:
            return
        new_zoom = self.camera_zoom * CAMERA_ZOOM_STEP ** wheel_steps
        self.camera_zoom = max(CAMERA_ZOOM_MIN,
                               min(CAMERA_ZOOM_MAX, new_zoom))
        self.mouse_world_x, self.mouse_world_y = self.screen_to_world(
            *pygame.mouse.get_pos()
        )

    # =====================================================
    # LOD: ДЕТАЛЬНАЯ ПРОРИСОВКА ПРИ ПРИБЛИЖЕНИИ
    # =====================================================

    @staticmethod
    def _make_night_edge_vignette():
        """Непрозрачный чёрный край с мягким сходом к центру."""
        surface = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA)
        width = max(1, int(SCREEN_SIZE * NIGHT_EDGE_FADE))
        for inset in range(width):
            t = 1.0 - inset / max(1, width - 1)
            alpha = round(255 * t ** 2.0)
            if alpha > 0:
                pygame.draw.rect(
                    surface, (0, 0, 0, alpha),
                    (inset, inset, SCREEN_SIZE - 2 * inset,
                     SCREEN_SIZE - 2 * inset), 1
                )
        return surface.convert_alpha()

    def _draw_night_edge_vignette(self):
        if (not NIGHT_EDGE_VIGNETTE
                or not getattr(self, "setting_water_darkening_enabled", True)):
            return
        # В дневное время виньетка исчезает. На максимуме ночи края
        # непрозрачны, независимо от масштаба камеры и голубой дымки.
        brightness = self._solar_brightness()
        if self.in_cave:
            strength = 0.76
        else:
            strength = max(0.0, min(1.0, (0.74 - brightness) / 0.74))
            strength = strength ** 1.55
        if strength <= 0.002:
            return
        self._night_edge_vignette.set_alpha(round(strength * 255))
        self.screen.blit(self._night_edge_vignette, (0, 0))

    def _hd_source(self, entity):
        """Не увеличиваем пиксели: создаём фигуры заново из исходных данных.

        Первый запрос для вида выполняется один раз, затем результат
        переиспользуется всеми экземплярами данного вида.
        """
        key = id(entity)
        if key in self._hd_source_cache:
            return self._hd_source_cache[key]
        base = getattr(entity, 'image', None)
        if base is None:
            self._hd_source_cache[key] = None
            return None
        factor = ZOOM_DETAIL_SOURCE_FACTOR
        source = None
        try:
            if isinstance(entity, FloraType):
                source = generate_subnautica_flora_sprite(
                    entity.kind, round(entity.size * factor), seed=entity.seed)
            elif isinstance(entity, AnimalType):
                if entity.sprite_kind is not None:
                    source = generate_subnautica_creature_sprite(
                        entity.sprite_kind,
                        max(12, round(entity.fish_length * factor)),
                        max(6, round(entity.fish_width * factor)))
                elif getattr(entity, '_hd_fish_palette', None) is not None:
                    # Создание нового рисунка не должно менять случайное
                    # размещение диких рыб и ресурсов в игровом мире.
                    state = random.getstate()
                    try:
                        random.seed(_stable_preview_seed(entity.name))
                        source = generate_pike_style_sprite(
                            max(12, round(entity.fish_length * factor)),
                            max(6, round(entity.fish_width * factor)),
                            *entity._hd_fish_palette)
                    finally:
                        random.setstate(state)
                elif 'Ghost' in entity.name or 'призрачн' in entity.name.lower():
                    source = generate_ghost_leviathan_sprite(
                        entity.fish_length * factor, entity.fish_width * factor)
            elif isinstance(entity, ObjectType):
                high_size = max(100, round(entity.size * factor * 1.4))
                if getattr(entity, 'is_buildable', False):
                    source = generate_building_sprite(
                        entity.name, high_size, entity.color,
                        wall=getattr(entity, 'is_wall', False))
                elif entity.name in _HIGH_RES_RESOURCE_NAMES:
                    source = generate_highres_resource_preview(entity, high_size)
                else:
                    source = generate_tech_item_sprite(
                        entity.name, high_size, entity.color,
                        is_weapon=getattr(entity, 'is_weapon', False),
                        weapon_type=getattr(entity, 'weapon_type', ''))
        except (ValueError, TypeError, pygame.error):
            # Неизвестные декоративные типы по-прежнему отрисовываются.
            source = None
        if source is None:
            source = pygame.transform.smoothscale(
                base, (max(2, round(base.get_width() * factor)),
                       max(2, round(base.get_height() * factor))))
        self._hd_source_cache[key] = source
        return source

    def _hd_image(self, entity, zoom, angle=None, glow=False):
        """Кэшированный экранный LOD без изменения игровых размеров объекта."""
        base = entity.glow_image if glow else entity.image
        if base is None:
            return None
        # Квантование предотвращает создание новой текстуры каждый кадр.
        # Используется исходный *игровой* размер изображения, а не размер
        # заново созданной фигуры, чтобы размеры рыб не изменились.
        bucket = round(zoom / .04) * .04
        rotation = (round(angle / ZOOM_DETAIL_ROTATION_STEP) *
                    ZOOM_DETAIL_ROTATION_STEP) % 360 if angle is not None else None
        key = (id(entity), bucket, rotation, glow)
        result = self._hd_sprite_cache.get(key)
        if result is not None:
            self._hd_sprite_cache.move_to_end(key)
            return result
        src = self._hd_source(entity)
        if src is None:
            return None
        if glow:
            src = self._hd_glow_source_cache.get(id(entity))
            if src is None:
                src = generate_bioluminescence_sprite(
                    self._hd_source(entity),
                    entity.kind if isinstance(entity, FloraType) else
                    (entity.sprite_kind or entity.name),
                    is_plant=isinstance(entity, FloraType),
                    seed=getattr(entity, 'seed', 0))
                self._hd_glow_source_cache[id(entity)] = src
            if src is None:
                return None
        sz = (max(1, round(base.get_width() * bucket)),
              max(1, round(base.get_height() * bucket)))
        result = pygame.transform.smoothscale(src, sz)
        if rotation is not None:
            result = pygame.transform.rotate(result, rotation)
        self._hd_sprite_cache[key] = result
        if len(self._hd_sprite_cache) > ZOOM_DETAIL_ROTATED_CACHE_MAX:
            self._hd_sprite_cache.popitem(last=False)
        return result

    def _hd_micro_tile(self, x, y, tile_px, cave=False, biome=None):
        """Рисует НОВЫЕ мини-детали дна на итоговой сетке пикселей."""
        variant = self._stable_visual_hash('zoom_details', x, y) % 48
        theme_id = 'cave' if cave else (biome.name if biome else 'none')
        key = (theme_id, variant, tile_px)
        cached = self._hd_floor_cache.get(key)
        if cached is not None:
            self._hd_floor_cache.move_to_end(key)
            return cached
        seed = self._stable_visual_hash('zoom_micro', theme_id, variant)
        rng = random.Random(seed)
        surf = pygame.Surface((tile_px, tile_px), pygame.SRCALPHA)
        scale = tile_px / CELL_SIZE
        if cave:
            palette = ((86, 100, 120), (106, 112, 132),
                       (43, 47, 60), (162, 174, 191))
        else:
            theme = self._surface_theme_for_biome(biome)
            if not theme:
                return None
            palette = tuple(theme['pebble_palette']) + (
                theme['highlight'], theme['shadow'])
        # Гранулы, отпечатки, блики отдельных песчинок и камешков.
        for i in range(22):
            px = rng.randint(1, tile_px - 2)
            py = rng.randint(1, tile_px - 2)
            color = palette[rng.randrange(len(palette))]
            radius = rng.choice((1, 1, 1, max(1, round(scale))))
            pygame.draw.circle(surf, (*color, rng.randint(75, 170)),
                               (px, py), radius)
            if i % 5 == 0 and radius > 1:
                pygame.draw.circle(surf, (220, 232, 232, 120),
                                   (max(0, px - 1), max(0, py - 1)), 1)
        # Тонкие минеральные жилки, песчаные полоски, отложения.
        for j in range(rng.randint(2, 4)):
            cx = rng.randint(3, tile_px - 4)
            cy = rng.randint(3, tile_px - 4)
            delta = max(3, round(4 * scale))
            pts = [(cx, cy),
                   (cx + rng.randint(-delta, delta),
                    cy + rng.randint(-delta, delta)),
                   (cx + rng.randint(-delta * 2, delta * 2),
                    cy + rng.randint(-delta * 2, delta * 2))]
            pygame.draw.lines(surf, (*palette[j % len(palette)], 115),
                              False, pts, 1)
        # При крупном масштабе появляются прожилки на мини-кораллах,
        # сетчатые водорослевые фрагменты и дополнительные морские звёзды.
        if scale >= 1.4 and not cave and rng.random() < .28:
            px = rng.randint(tile_px // 4, tile_px * 3 // 4)
            py = rng.randint(tile_px // 4, tile_px * 3 // 4)
            radius = max(3, round(2.2 * scale))
            color = (205, 136, 109, 180)
            for i in range(5):
                a = i * math.tau / 5
                xx = round(px + math.cos(a) * radius)
                yy = round(py + math.sin(a) * radius)
                pygame.draw.line(surf, color, (px, py), (xx, yy),
                                 max(1, round(.8 * scale)))
            pygame.draw.circle(surf, (242, 189, 133, 210), (px, py),
                               max(1, round(scale)))
        self._hd_floor_cache[key] = surf
        if len(self._hd_floor_cache) > 550:
            self._hd_floor_cache.popitem(last=False)
        return surf

    def _draw_zoom_details(self, zoom, canvas_px, screen_offset):
        """Второй проход В ИСТИННОМ разрешении экрана, под ночной маской."""
        if not ZOOM_DETAIL_ENABLED or zoom < ZOOM_DETAIL_START:
            return
        tile_px = CELL_SIZE * zoom
        tile_int = max(4, round(tile_px))
        layer = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA)
        half = SCREEN_SIZE * .5

        def position(x, y):
            return (round(half + (x - self.player_x) * tile_px),
                    round(half + (y - self.player_y) * tile_px))

        def sprite(entity, center, angle=None, fit=None):
            image = self._hd_image(entity, zoom, angle)
            if image is None:
                return
            if fit is not None:
                image = self._fit_surface(image, *fit)
            layer.blit(image, image.get_rect(center=center))

        margin = SCREEN_SIZE / (2 * tile_px) + 2
        left = max(0, math.floor(self.player_x - margin))
        right = min(MAP_SIZE - 1, math.ceil(self.player_x + margin))
        top = max(0, math.floor(self.player_y - margin))
        bottom = min(MAP_SIZE - 1, math.ceil(self.player_y + margin))
        objects = self._get_current_object_grid()
        plants = self._current_flora_grid()
        dropped = self._current_dropped_items()
        planter_types = self._planter_types()

        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                at = position(x, y)
                if not (-tile_px * 2 < at[0] < SCREEN_SIZE + tile_px * 2 and
                        -tile_px * 2 < at[1] < SCREEN_SIZE + tile_px * 2):
                    continue
                cave_tunnel = self.get_cave_tunnel_at(x, y) if self.in_cave else None
                biome = None if self.in_cave else self.world.get_biome_at(x, y)
                if self.in_cave:
                    can_detail = cave_tunnel is not None
                else:
                    can_detail = (biome is not None and
                                  not self.is_aurora_biome(biome) and
                                  not (self.start_capsule_rect[0] <= x <= self.start_capsule_rect[2] and self.start_capsule_rect[1] <= y <= self.start_capsule_rect[3]))
                if can_detail:
                    micro = self._hd_micro_tile(x, y, tile_int,
                                                self.in_cave, biome)
                    if micro is not None:
                        layer.blit(micro, micro.get_rect(center=at))

        # Слои отрисовываются в том же порядке, что в обычном renderer.
        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                at = position(x, y)
                if not (-130 < at[0] < SCREEN_SIZE + 130 and
                        -130 < at[1] < SCREEN_SIZE + 130):
                    continue
                flora = plants.get((x, y))
                if flora is not None:
                    sprite(flora, at)
                obj = objects.get((x, y))
                if obj is not None and not getattr(obj, "is_buildable", False):
                    sprite(obj, at)
                contents = dropped.get((x, y))
                if contents:
                    item = contents[-1]
                    sprite(item, at)

        for animal in self.get_nearby_animals(margin + 2):
            if animal.hp <= 0 or animal.type.image is None:
                continue
            at = position(animal.x, animal.y)
            if -400 < at[0] < SCREEN_SIZE + 400 and -400 < at[1] < SCREEN_SIZE + 400:
                sprite(animal.type, at, getattr(animal, 'visual_angle', 0))

        # Постройки поверх растительности и ресурсов, включая соседние клетки.
        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                obj = objects.get((x, y))
                if obj is None or not getattr(obj, "is_buildable", False):
                    continue
                at = position(x, y)
                sprite(obj, at)
                if obj in planter_types:
                    planted = self.planted_flora.get(self._planter_key(x, y), ())
                    offsets = ((0, 1), (-8, -3), (8, -3), (-8, 7),
                               (8, 7), (0, -8), (0, 9))
                    max_size = 20 if len(planted) <= 2 else 15
                    for i, plant in enumerate(planted):
                        ox, oy = offsets[i % len(offsets)]
                        sprite(plant, (round(at[0] + ox * zoom),
                                       round(at[1] + oy * zoom)),
                               fit=(round(max_size * zoom),
                                    round(max_size * zoom)))

        # Активный транспорт либо игрок — самый верхний игровой спрайт.
        # Без этого второй HD-проход снова закрывал бы их водорослями.
        center = (round(half), round(half))
        def blit_zoomed(image, at):
            if image is None:
                return
            size = (max(1, round(image.get_width() * zoom)),
                    max(1, round(image.get_height() * zoom)))
            enlarged = pygame.transform.smoothscale(image, size)
            layer.blit(enlarged, enlarged.get_rect(center=at))

        if self.active_vehicle is not None:
            blit_zoomed(self.get_vehicle_rotated(
                self.active_vehicle, self.player_angle), center)
        else:
            if self.equipped_weapon is not None:
                radians = math.radians(self.player_angle)
                weapon_pos = (round(half + math.cos(radians) * tile_px * .55),
                              round(half + math.sin(radians) * tile_px * .55))
                blit_zoomed(self.get_weapon_rotated(
                    self.equipped_weapon, self.player_angle), weapon_pos)
            blit_zoomed(self.get_diver_rotated(self.player_angle), center)

        # Ночная завеса уже применена к основному миру. Применяем ту же
        # прозрачность к детальному слою, чтобы рыбы НЕ светились сами.
        if self._night_scene_alpha() > 0:
            mask = pygame.transform.smoothscale(
                self.lighting_overlay, (canvas_px, canvas_px))
            layer.blit(mask, (screen_offset, screen_offset),
                       special_flags=pygame.BLEND_RGBA_SUB)
        self.screen.blit(layer, (0, 0))

        # Светящиеся части сохраняются поверх чёрной маски.
        if BIOLUMINESCENCE_ENABLED:
            night = 1.0 if self.in_cave else max(
                0.0, 1.0 - self._solar_brightness() * 1.35)
            alpha = round((BIOGLOW_DAY_ALPHA +
                     (BIOGLOW_NIGHT_ALPHA - BIOGLOW_DAY_ALPHA) * night) *
                     (0.88 + 0.12 * math.sin(self.frame_count * .045)))
            for y in range(top, bottom + 1):
                for x in range(left, right + 1):
                    at = position(x, y)
                    flora = plants.get((x, y))
                    if flora is None or flora.glow_image is None:
                        continue
                    image = self._hd_image(flora, zoom, glow=True)
                    if image is not None:
                        image.set_alpha(alpha)
                        self.screen.blit(image, image.get_rect(center=at))
                        image.set_alpha(None)
            for animal in self.get_nearby_animals(margin + 2):
                if animal.hp <= 0 or animal.type.glow_image is None:
                    continue
                at = position(animal.x, animal.y)
                image = self._hd_image(animal.type, zoom,
                                       getattr(animal, 'visual_angle', 0), glow=True)
                if image is not None:
                    image.set_alpha(alpha)
                    self.screen.blit(image, image.get_rect(center=at))
                    image.set_alpha(None)

    def _night_scene_alpha(self):
        if not getattr(self, "setting_water_darkening_enabled", True):
            return 0
        if self.in_cave:
            return 250
        brightness = self._solar_brightness()
        if MIDNIGHT_BLACKOUT and (
                min(self._visual_day_time(), 1.0 - self._visual_day_time())
                <= MIDNIGHT_BLACKOUT_HALF_WINDOW):
            return 255
        twilight = max(0.0, min(1.0, (0.72 - brightness) / 0.72))
        return round(255 * twilight ** 1.5)

    # =====================================================
    # СОБЫТИЯ
    # =====================================================

    def handle_events(self):
        pending_events = pygame.event.get()
        # SDL может сгенерировать MouseDown раньше FingerDown в той же пачке.
        # Приоритет FINGER исключает дублирование выстрелов/открытий панелей.
        finger_types = (getattr(pygame, "FINGERDOWN", -1000),
                        getattr(pygame, "FINGERMOTION", -1001),
                        getattr(pygame, "FINGERUP", -1002))
        if any(e.type in finger_types for e in pending_events):
            self.mobile_controls.suppress_mouse_until = pygame.time.get_ticks() + 320
        for event in pending_events:
            if self.mobile_controls.intercept_event(event):
                continue
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F9:
                self.mobile_controls.enabled = not self.mobile_controls.enabled
                self.mobile_controls.joy_value = (0.0, 0.0)
                self.mobile_controls.joy_pointer = None
                continue
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                self.mouse_world_x, self.mouse_world_y = self.screen_to_world(
                    mouse_x, mouse_y
                )

            elif event.type == pygame.MOUSEWHEEL:
                if self.state == "map":
                    if event.y > 0:
                        self.map_zoom = min(
                            self.map_max_zoom, self.map_zoom * 1.15
                        )
                    elif event.y < 0:
                        self.map_zoom = max(
                            self.map_min_zoom, self.map_zoom / 1.15
                        )
                elif self.state == "playing":
                    # Карта и игровой мир масштабируются независимо.
                    self._change_camera_zoom(event.y)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    if self.state == "playing" or self.settings_open:
                        self.settings_open = not self.settings_open
                elif event.key == pygame.K_ESCAPE:
                    if self.settings_open:
                        self.settings_open = False
                    elif self.state != "playing":
                        self.state = "playing"
                        self.notification = ""
                        self.selected_biome = None
                    else:
                        self.running = False

                elif event.key == pygame.K_F8:
                    self.force_midnight_preview = not self.force_midnight_preview
                    self.notification = (
                        'Предпросмотр полной ночи: ВКЛ (F8)' if self.force_midnight_preview
                        else 'Предпросмотр полной ночи: ВЫКЛ (F8)'
                    )
                    self.notification_timer = 110
                elif (event.key == pygame.K_l and self.active_vehicle is not None
                      and self.state == "playing"):
                    self.vehicle_headlights_on = not self.vehicle_headlights_on
                    self.notification = (
                        "Фары подлодки включены" if self.vehicle_headlights_on
                        else "Фары подлодки выключены"
                    )
                    self.notification_timer = 75
                elif event.key == pygame.K_r:
                    self.toggle_inventory()
                elif event.key == pygame.K_i:
                    self.toggle_crafting()
                elif event.key == pygame.K_m:
                    self.toggle_map()
                elif event.key == pygame.K_t:
                    self.toggle_pet_list()
                elif (event.key == pygame.K_f
                      and self.state in ("playing", "inventory")):
                    self.handle_vehicle_action()
                elif (event.key == pygame.K_c
                      and self.state == "playing"):
                    self.use_cave_entrance()
                elif (event.key == pygame.K_b
                      and self.state == "playing"):
                    self.build()
                elif (event.key == pygame.K_x
                      and self.state == "playing"):
                    self.destroy_build()
                elif (event.key == pygame.K_e
                      and self.state == "playing"):
                    self.pick_up()
                elif (event.key == pygame.K_SPACE
                      and self.state == "playing"):
                    self.attack()
                elif (event.key == pygame.K_u
                      and self.state in ("playing", "inventory")):
                    self.use_item()
                elif (event.key == pygame.K_q
                      and self.state in ("playing", "inventory")):
                    self.equip_weapon()
                elif (event.key == pygame.K_p
                      and self.state == "inventory"):
                    self.drop_selected_item()
                elif (event.key == pygame.K_h
                      and self.state == "inventory"):
                    self.spawn_selected_companion()

                if self.state == "pets":
                    pets = self._get_all_companions()
                    max_page = max(0, (len(pets) - 1) // self.pets_per_page)
                    if event.key in (pygame.K_RIGHT, pygame.K_PAGEDOWN):
                        self.pet_list_page = min(max_page, self.pet_list_page + 1)
                        self.selected_pet = None
                    elif event.key in (pygame.K_LEFT, pygame.K_PAGEUP):
                        self.pet_list_page = max(0, self.pet_list_page - 1)
                        self.selected_pet = None
                    elif pygame.K_1 <= event.key <= pygame.K_9:
                        self.select_pet_from_list(event.key - pygame.K_0)
                    elif pygame.K_KP1 <= event.key <= pygame.K_KP9:
                        self.select_pet_from_list(event.key - pygame.K_KP1 + 1)
                    elif event.key == pygame.K_e:
                        self.return_selected_pet_to_inventory()
                    elif event.key == pygame.K_u:
                        self.heal_selected_pet()

                if self.state == "planting":
                    plants = self._researched_plant_list()
                    max_page = max(
                        0, (len(plants) - 1) // self.plants_per_page
                    )
                    if event.key in (pygame.K_RIGHT, pygame.K_PAGEDOWN):
                        self.planting_page = min(
                            max_page, self.planting_page + 1
                        )
                    elif event.key in (pygame.K_LEFT, pygame.K_PAGEUP):
                        self.planting_page = max(0, self.planting_page - 1)
                    elif pygame.K_1 <= event.key <= pygame.K_9:
                        self.plant_researched_flora(
                            event.key - pygame.K_1
                        )

                if self.state == "map":
                    if event.key in (
                        pygame.K_EQUALS,
                        pygame.K_PLUS,
                        pygame.K_KP_PLUS,
                        pygame.K_PAGEUP
                    ):
                        self.map_zoom = min(
                            self.map_max_zoom, self.map_zoom * 1.2
                        )
                    elif event.key in (
                        pygame.K_MINUS,
                        pygame.K_KP_MINUS,
                        pygame.K_PAGEDOWN
                    ):
                        self.map_zoom = max(
                            self.map_min_zoom, self.map_zoom / 1.2
                        )

                if self.state == "crafting":
                    if event.key == pygame.K_TAB:
                        stations = self.get_available_crafting_stations()
                        if stations:
                            self.craft_station_index = (
                                self.craft_station_index + 1
                            ) % len(stations)
                            self.craft_page = 0
                    else:
                        station_recipes = self.get_current_station_recipes()
                        max_station_page = max(
                            0,
                            (len(station_recipes) - 1)
                            // self.recipes_per_page
                        )
                        if event.key == pygame.K_RIGHT:
                            if self.craft_page < max_station_page:
                                self.craft_page += 1
                        elif event.key == pygame.K_LEFT:
                            if self.craft_page > 0:
                                self.craft_page -= 1
                        elif pygame.K_1 <= event.key <= pygame.K_9:
                            index = event.key - pygame.K_1
                            recipe_index = (
                                self.craft_page
                                * self.recipes_per_page + index
                            )

                            if recipe_index < len(station_recipes):
                                if not self.can_craft_here():
                                    self.state = "playing"
                                    self.notification = (
                                        "Здесь нет доступной станции крафта"
                                    )
                                    self.notification_timer = 120
                                    continue

                                recipe = station_recipes[recipe_index]

                                if recipe.can_craft(self.inventory_counts):
                                    free_slots = sum(
                                        1 for slot in self.inventory
                                        if slot is None
                                    )
                                    # Ингредиенты исчезнут перед выдачей
                                    # результата и освободят свои слоты.
                                    possible_slots = (
                                        free_slots
                                        + sum(recipe.ingredients.values())
                                    )
                                    if possible_slots < recipe.result_count:
                                        self.notification = (
                                            "Нет места в инвентаре!"
                                        )
                                        self.notification_timer = 60
                                        continue

                                    result = recipe.craft(
                                        self.inventory,
                                        self.inventory_counts
                                    )

                                    if result is not None:
                                        crafted = 0
                                        for _ in range(recipe.result_count):
                                            if self.add_to_inventory(result):
                                                crafted += 1
                                        suffix = (
                                            f" x{crafted}"
                                            if crafted > 1 else ""
                                        )
                                        self.notification = (
                                            f"Создано: {result.name}{suffix}"
                                        )
                                        self.notification_timer = 60
                                else:
                                    self.notification = (
                                        "Не хватает ресурсов"
                                    )
                                    self.notification_timer = 60

            elif (event.type == pygame.MOUSEBUTTONDOWN
                  and self.settings_open):
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    panel_x = (SCREEN_SIZE - 520) // 2
                    panel_y = (SCREEN_SIZE - 400) // 2
                    option_rects = [
                        pygame.Rect(panel_x + 24, panel_y + 84, 472, 48),
                        pygame.Rect(panel_x + 24, panel_y + 142, 472, 48),
                        pygame.Rect(panel_x + 24, panel_y + 200, 472, 48),
                        pygame.Rect(panel_x + 24, panel_y + 258, 472, 48),
                        pygame.Rect(panel_x + 24, panel_y + 316, 472, 48),
                    ]
                    if option_rects[0].collidepoint(mouse_x, mouse_y):
                        self.setting_plankton_enabled = not self.setting_plankton_enabled
                        if not self.setting_plankton_enabled:
                            self._night_sparks_visible = 0
                            self._night_sparks.clear()
                    elif option_rects[1].collidepoint(mouse_x, mouse_y):
                        self.setting_seabed_details_enabled = not self.setting_seabed_details_enabled
                    elif option_rects[2].collidepoint(mouse_x, mouse_y):
                        self.setting_water_darkening_enabled = not self.setting_water_darkening_enabled
                    elif option_rects[3].collidepoint(mouse_x, mouse_y):
                        self.setting_music_enabled = not self.setting_music_enabled
                        if pygame.mixer.get_init():
                            pygame.mixer.music.set_volume(0.35 if self.setting_music_enabled else 0.0)
                    elif option_rects[4].collidepoint(mouse_x, mouse_y):
                        self.setting_effects_enabled = not self.setting_effects_enabled
                        if not self.setting_effects_enabled and pygame.mixer.get_init():
                            pygame.mixer.stop()
            elif (event.type == pygame.MOUSEBUTTONDOWN
                  and event.button == 1):
                if self.state == "playing":
                    if self.active_vehicle is not None:
                        self.fire_vehicle_torpedo(
                            self.mouse_world_x, self.mouse_world_y
                        )
                    else:
                        self.shoot(
                            self.mouse_world_x, self.mouse_world_y
                        )

                elif self.state == "inventory":
                    mouse_x, mouse_y = event.pos

                    total_width = (
                        INVENTORY_COLS * (SLOT_SIZE + SLOT_MARGIN)
                        - SLOT_MARGIN
                    )
                    total_height = (
                        INVENTORY_ROWS * (SLOT_SIZE + SLOT_MARGIN)
                        - SLOT_MARGIN
                    )

                    start_x = (SCREEN_SIZE - total_width) // 2
                    start_y = (SCREEN_SIZE - total_height) // 2

                    if (start_x <= mouse_x <= start_x + total_width
                            and
                            start_y <= mouse_y <= start_y + total_height):
                        col = (mouse_x - start_x) // (
                            SLOT_SIZE + SLOT_MARGIN
                        )
                        row = (mouse_y - start_y) // (
                            SLOT_SIZE + SLOT_MARGIN
                        )

                        if (col < INVENTORY_COLS
                                and row < INVENTORY_ROWS):
                            index = row * INVENTORY_COLS + col

                            if index < INVENTORY_SIZE:
                                self.active_slot_index = index
                                item = self.inventory[index]

                                if item:
                                    self.notification = (
                                        f"Выбран: {item.name}"
                                    )
                                else:
                                    self.notification = "Слот пуст"

                                self.notification_timer = 60

                elif self.state == "map":
                    mouse_x, mouse_y = event.pos

                    if not (10 <= mouse_x <= 260
                            and 70 <= mouse_y <= SCREEN_SIZE - 30):
                        self.map_select_biome(mouse_x, mouse_y)

            elif (event.type == pygame.MOUSEBUTTONDOWN
                  and event.button == 3):
                if self.state == "playing":
                    if self._is_scanner_selected():
                        self.scan_with_scanner()
                    else:
                        self.open_planting_menu_at_cursor()
                elif self.state == "inventory":
                    mouse_x, mouse_y = event.pos
                    total_width = (
                        INVENTORY_COLS * (SLOT_SIZE + SLOT_MARGIN)
                        - SLOT_MARGIN
                    )
                    total_height = (
                        INVENTORY_ROWS * (SLOT_SIZE + SLOT_MARGIN)
                        - SLOT_MARGIN
                    )
                    start_x = (SCREEN_SIZE - total_width) // 2
                    start_y = (SCREEN_SIZE - total_height) // 2

                    if (start_x <= mouse_x <= start_x + total_width
                            and start_y <= mouse_y <= start_y + total_height):
                        col = (mouse_x - start_x) // (SLOT_SIZE + SLOT_MARGIN)
                        row = (mouse_y - start_y) // (SLOT_SIZE + SLOT_MARGIN)
                        if col < INVENTORY_COLS and row < INVENTORY_ROWS:
                            index = row * INVENTORY_COLS + col
                            if index < INVENTORY_SIZE:
                                self.active_slot_index = index
                                item = self.inventory[index]
                                if item is None:
                                    self.notification = "Слот пуст"
                                    self.notification_timer = 60
                                elif getattr(item, "edible", False):
                                    self.use_item()
                                else:
                                    self.notification = (
                                        f"{item.name}: этот предмет нельзя съесть"
                                    )
                                    self.notification_timer = 60
                elif self.state == "scanner":
                    self.state = "playing"
                    self.scanner_target = None

    # =====================================================
    # ДЕНЬ / НОЧЬ
    # =====================================================

    def _visual_day_time(self):
        return 0.0 if self.force_midnight_preview else self.day_time

    def get_time_string(self):
        t = self._visual_day_time()
        hours = t * 24.0
        h = int(hours) % 24
        m = int((hours - int(hours)) * 60)

        if 5 <= h < 11:
            period = "Утро"
        elif 11 <= h < 17:
            period = "День"
        elif 17 <= h < 21:
            period = "Вечер"
        else:
            period = "Ночь"
        suffix = " [F8: тест ночи]" if self.force_midnight_preview else ""
        return f"{period} {h:02d}:{m:02d}{suffix}"

    def _solar_brightness(self):
        # 0.0 -- полночь; 0.5 -- полдень.
        return (1.0 - math.cos(self._visual_day_time() * math.tau)) * 0.5

    def _is_dark_night(self):
        """Ночь или подземелье; F8 также влияет на поведение хищников."""
        return self.in_cave or self._solar_brightness() < 0.25

    def _night_plankton_strength(self):
        """0 днём; плавный рост от заката до полуночи и спад к рассвету.

        F8 для проверки глубокой ночи автоматически влияет и на планктон.
        Темнота пещер сама по себе не включает дневной планктон.
        """
        if (not NIGHT_PLANKTON_ENABLED
                or not getattr(self, "setting_plankton_enabled", True)):
            return 0.0
        light = self._solar_brightness()
        if light >= NIGHT_VISIBLE_BRIGHTNESS - 1e-8:
            return 0.0
        progress = max(0.0, min(1.0, (
            NIGHT_VISIBLE_BRIGHTNESS - light) / NIGHT_VISIBLE_BRIGHTNESS
        ))
        return progress ** 1.18

    def _night_spawn_spark(self, radius):
        rng = self._night_rng
        x = self.player_x + rng.uniform(-radius, radius)
        y = self.player_y + rng.uniform(-radius, radius)
        return NightWaterSpark(
            rng,
            max(0.0, min(MAP_SIZE - 0.01, x)),
            max(0.0, min(MAP_SIZE - 0.01, y)),
        )

    def _update_night_plankton(self):
        """Перемещаем только активные точки, обходясь без тысяч объектов мира."""
        night = self._night_plankton_strength()
        if night <= 0.001:
            self._night_sparks_visible = 0
            # Следующий вечер создаст новую живую россыпь около игрока.
            self._night_sparks.clear()
            return

        total = int(NIGHT_PLANKTON_MAX * night ** 1.35)
        total = max(0, min(NIGHT_PLANKTON_MAX, total))
        self._night_sparks_visible = total
        # Рассыпаем частицы чуть за краями текущей камеры, без появления
        # ярких точек непосредственно из центра экрана.
        radius = self._render_view_radius + 2.5
        rng = self._night_rng
        while len(self._night_sparks) < total:
            self._night_sparks.append(self._night_spawn_spark(radius))

        px, py = self.player_x, self.player_y
        for spark in self._night_sparks[:total]:
            spark.phase = (spark.phase + spark.blink_speed) % math.tau
            # Разная скорость и мелкая дрожь направлений даже без игрока.
            drift_x = spark.vx + math.sin(spark.phase * 0.77) * spark.wander
            drift_y = spark.vy + math.cos(spark.phase * 1.13) * spark.wander
            if spark.flee_distance:
                dx = spark.x - px
                dy = spark.y - py
                distance_sq = dx * dx + dy * dy
                limit_sq = spark.flee_distance * spark.flee_distance
                if distance_sq < limit_sq:
                    distance = max(0.001, math.sqrt(distance_sq))
                    # Чем ближе игрок, тем сильнее рывок; по достижении
                    # индивидуальной границы малёк снова просто плавает.
                    impulse = spark.flee_speed * (
                        0.45 + 0.55 * (1.0 - distance / spark.flee_distance)
                    )
                    if distance_sq < 1e-6:
                        dx, dy = math.cos(spark.phase), math.sin(spark.phase)
                        distance = 1.0
                    drift_x += dx / distance * impulse
                    drift_y += dy / distance * impulse
            spark.x += drift_x
            spark.y += drift_y

            # Возврат с противоположного края камерного квадрата: частицы
            # не следуют за игроком бесконечно и не размножаются на карте.
            offset_x, offset_y = spark.x - px, spark.y - py
            if abs(offset_x) > radius or abs(offset_y) > radius:
                if abs(offset_x) > radius * 2 or abs(offset_y) > radius * 2:
                    spark.x = px + rng.uniform(-radius, radius)
                    spark.y = py + rng.uniform(-radius, radius)
                elif abs(offset_x) > radius:
                    spark.x = px + (-radius if offset_x > 0 else radius)
                    spark.y = py + rng.uniform(-radius, radius)
                else:
                    spark.y = py + (-radius if offset_y > 0 else radius)
                    spark.x = px + rng.uniform(-radius, radius)
            spark.x = max(0.0, min(MAP_SIZE - 0.01, spark.x))
            spark.y = max(0.0, min(MAP_SIZE - 0.01, spark.y))

    def draw_night_plankton(self):
        """Мерцающие точки поверх ночи, но ниже HUD и без перекрытия игрока.

        Рисуем в реальном разрешении окна после LOD-прохода. Так светящиеся
        мальки сохраняют чёткость и при приближении, и при отдалении.
        """
        if self._night_sparks_visible <= 0:
            return
        strength = self._night_plankton_strength()
        if strength <= 0.001:
            return
        size = self.screen.get_size()
        if (self._night_spark_surface is None or
                self._night_spark_surface.get_size() != size):
            self._night_spark_surface = pygame.Surface(
                size, pygame.SRCALPHA
            ).convert_alpha()
        layer = self._night_spark_surface
        layer.fill((0, 0, 0, 0))
        zoom = self.camera_zoom
        pixels_per_cell = CELL_SIZE * zoom
        cx = size[0] * 0.5
        cy = size[1] * 0.5
        margin = 7
        rngless_flicker = self.frame_count * 0.026

        # Перед игроком/корпусом лодки точки не появляются: силуэт
        # остаётся выше планктона при любой ориентации транспорта.
        if self.active_vehicle is not None:
            sprite = self.get_vehicle_rotated(
                self.active_vehicle, self.player_angle
            )
        else:
            sprite = self.get_diver_rotated(self.player_angle)
        protected = (pygame.Rect(0, 0, 1, 1) if sprite is None
                     else sprite.get_rect())
        if sprite is not None:
            protected.size = (
                max(1, round(sprite.get_width() * zoom)),
                max(1, round(sprite.get_height() * zoom)),
            )
        protected.center = (round(cx), round(cy))
        protected.inflate_ip(3, 3)

        objects = self._get_current_object_grid()
        for spark in self._night_sparks[:self._night_sparks_visible]:
            # Небольшое дрожание в пикселях поверх реального плавания.
            sx = int(cx + (spark.x - self.player_x) * pixels_per_cell +
                     math.sin(spark.phase * 7.2) * spark.jitter * zoom)
            sy = int(cy + (spark.y - self.player_y) * pixels_per_cell +
                     math.cos(spark.phase * 6.7) * spark.jitter * zoom)
            if not (margin <= sx < size[0] - margin and
                    margin <= sy < size[1] - margin):
                continue
            if protected.collidepoint(sx, sy):
                continue
            gx, gy = int(spark.x), int(spark.y)
            if self.in_cave:
                if self.get_cave_tunnel_at(gx, gy) is None:
                    continue
            elif self.is_inside_start_capsule(gx, gy):
                continue
            obj = objects.get((gx, gy))
            if obj is not None and getattr(obj, "is_buildable", False):
                continue

            # Два быстрых несинхронных ритма: лёгкий блеск и редкая вспышка.
            flicker = 0.5 + 0.5 * math.sin(spark.phase * 2.9 +
                                            rngless_flicker)
            flash = max(0.0, math.sin(spark.phase * 5.1 +
                                      rngless_flicker * 1.7)) ** 10
            twinkle = 0.10 + 0.65 * flicker + 0.25 * flash
            if twinkle < 0.18:
                continue
            alpha = int(232 * strength ** 0.74 * twinkle)
            if alpha < 9:
                continue
            radius_px = max(1, min(8, round(spark.radius * zoom)))
            color = spark.color
            # Полупрозрачный ореол + насыщенная точка + редкий блик.
            pygame.draw.circle(layer, (*color, max(3, alpha // 9)),
                               (sx, sy), radius_px + 4)
            pygame.draw.circle(layer, (*color, min(220, alpha // 3)),
                               (sx, sy), radius_px + 2)
            pygame.draw.circle(layer, (*color, alpha),
                               (sx, sy), radius_px)
            if spark.fry and radius_px >= 2:
                # Совсем короткий след движения для мальков (не рыбный спрайт).
                speed = math.hypot(spark.vx, spark.vy) or 0.001
                tail = max(2, round(radius_px * 1.7))
                tx = round(sx - spark.vx / speed * tail)
                ty = round(sy - spark.vy / speed * tail)
                pygame.draw.line(layer, (*color, alpha // 3),
                                 (sx, sy), (tx, ty), max(1, radius_px // 2))
            if flash > 0.55:
                pygame.draw.circle(layer, (235, 250, 255, int(alpha * flash)),
                                   (sx, sy), max(1, radius_px // 2))
        self.screen.blit(layer, (0, 0))

    @staticmethod
    def _make_light_source(x, y, radius, power=255, angle=None,
                           width=40, color=(205, 230, 255), kind="lamp",
                           reacts=True):
        """Координаты и размеры в КЛЕТКАХ, угол и ширина — в градусах."""
        return {"x": float(x), "y": float(y), "radius": float(radius),
                "power": max(0, min(255, int(power))), "angle": angle,
                "width": width, "color": color, "kind": kind,
                "reacts": reacts}

    def _collect_light_sources(self):
        """Общий источник данных для отрисовки света и реакции существ.

        Сканирование ограничено видимыми клетками + несколькими вокруг;
        не обходит гигантскую карту и не создаёт новых построек.
        """
        if not LIGHTING_ENABLED:
            return []
        out = []
        add = out.append
        px, py = self.player_x, self.player_y
        radius_view = VIEW_RADIUS + 9

        if not self.in_cave:
            x1, y1, x2, y2 = self.start_capsule_rect
            if (x1 - radius_view < px < x2 + radius_view and
                    y1 - radius_view < py < y2 + radius_view):
                # Два мягких потолочных светильника освещают интерьер.
                cy = (y1 + y2) * 0.5
                add(self._make_light_source(x1 + 2, cy, 4.3, 255,
                    color=(220, 242, 255), kind="capsule", reacts=False))
                add(self._make_light_source(x2 - 2, cy, 4.3, 255,
                    color=(220, 242, 255), kind="capsule", reacts=False))
                # Наружная подсветка входа и два аварийных маячка.
                door_cx = sum(p[0] for p in self.start_capsule_door_cells) / 2
                add(self._make_light_source(door_cx, y2 + 0.35, 5.0, 235,
                    angle=90, width=45, color=(255, 228, 167),
                    kind="capsule_beacon"))
                for bx in (x1 + 0.45, x2 + 0.55):
                    add(self._make_light_source(bx, y1 + 0.5, 1.8, 205,
                        color=(160, 220, 255), kind="capsule_beacon"))

        grid = self._get_current_object_grid()
        cx = int(px)
        cy = int(py)
        xr = range(max(0, cx - radius_view), min(MAP_SIZE, cx + radius_view + 1))
        yr = range(max(0, cy - radius_view), min(MAP_SIZE, cy + radius_view + 1))
        interior_names = {
            "Многоцелевая комната", "Большая комната", "Комната сканирования",
            "Обсерватория", "Стыковочная шахта", "Прямой отсек",
            "Угловой отсек", "T-образный отсек", "Крестообразный отсек",
            "Прямой стеклянный отсек", "Угловой стеклянный отсек",
            "Стеклянный купол многоцелевой комнаты",
            "Стеклянный купол большой комнаты", "Вертикальный соединитель",
            "Люк", "Окно", "Фундамент", "Пол",
        }
        for iy in yr:
            for ix in xr:
                obj = grid.get((ix, iy))
                if obj is None:
                    continue
                x = ix
                y = iy
                if obj is spotlight_type:
                    # Прожектор следит за ближайшей живностью, иначе
                    # смотрит в заранее выбранную постоянную сторону.
                    angle = (ix * 73 + iy * 31) % 360
                    nearest_sq = 10.0 * 10.0
                    for animal in self.get_nearby_animals(VIEW_RADIUS + 3):
                        if animal.hp <= 0 or getattr(animal, "is_companion", False):
                            continue
                        d2 = (animal.x - x)**2 + (animal.y - y)**2
                        if 0.01 < d2 < nearest_sq:
                            nearest_sq = d2
                            angle = math.degrees(math.atan2(animal.y-y, animal.x-x))
                    add(self._make_light_source(x, y, 8.5, 255, angle=angle,
                        width=34, color=(255, 246, 193), kind="spotlight"))
                    add(self._make_light_source(x, y, 1.4, 230,
                        color=(255, 242, 204), kind="lamp_near"))
                elif obj is floodlight_type:
                    add(self._make_light_source(x, y, 6.3, 248,
                        color=(255, 238, 185), kind="floodlight"))
                elif obj in (seamoth_type, cyclops_type):
                    # Поставленные на карту подлодки (если такая постройка есть).
                    if self.vehicle_headlights_on:
                        add(self._make_light_source(x, y, 5.0, 220,
                            angle=0, width=42, kind="vehicle_parked"))
                    add(self._make_light_source(x, y, 1.9, 185,
                        color=(105, 210, 240), kind="engine", reacts=False))
                elif getattr(obj, "name", "") in interior_names:
                    size = 3.5 if obj.name not in ("Фундамент", "Пол") else 1.8
                    add(self._make_light_source(x, y, size, 215,
                        color=(219, 240, 255), kind="room", reacts=False))
                elif getattr(obj, "is_buildable", False) and obj.name in (
                    "Изготовитель", "Модификационная станция", "Биореактор",
                    "Ядерный реактор", "Кофейный торговый автомат",
                    "Радио", "Водоочистная станция", "Изготовитель аптечек",
                    "Консоль улучшения транспорта", "Зарядное устройство батарей",
                    "Зарядное устройство энергоячеек"):
                    add(self._make_light_source(x, y, 1.7, 145,
                        color=(135, 210, 235), kind="console", reacts=False))

        # Переносной источник света прикреплён к игроку; фара машины
        # направлена туда же, куда смотрит её нос.
        if self.active_vehicle is not None:
            if self.vehicle_headlights_on:
                angle = self.player_angle
                rad = math.radians(angle)
                forward = 1.0 if self.active_vehicle is seamoth_type else 2.1
                nose_x = px + math.cos(rad) * forward
                nose_y = py + math.sin(rad) * forward
                beam_r = 7.7 if self.active_vehicle is seamoth_type else 9.0
                add(self._make_light_source(nose_x, nose_y, beam_r, 255,
                    angle=angle, width=35,
                    color=(205, 240, 255), kind="vehicle_headlight"))
                add(self._make_light_source(nose_x, nose_y, 2.1, 225,
                    color=(205, 243, 255), kind="vehicle_bulb"))
            add(self._make_light_source(px, py, 2.2, 185,
                color=(80, 195, 230), kind="engine", reacts=False))
        else:
            if self.flashlight_on:
                rad = math.radians(self.player_angle)
                add(self._make_light_source(
                    px + math.cos(rad) * 0.3, py + math.sin(rad) * 0.3,
                    5.1, 255, angle=self.player_angle, width=33,
                    color=(230, 247, 255), kind="flashlight"))
                add(self._make_light_source(px, py, 0.85, 230,
                    color=(215, 235, 255), kind="flashlight_bulb"))
            if self.seaglide_on:
                add(self._make_light_source(px, py, 3.0, 216,
                    color=(140, 210, 255), kind="seaglide"))
            if self.active_flare_timer > 0:
                flicker = 0.94 + 0.06 * math.sin(self.frame_count * 0.27)
                add(self._make_light_source(px, py, 4.2,
                    int(253 * flicker), color=(255, 112, 62), kind="flare"))
        return out

    def _radial_light_sprite(self, radius_px, power):
        """Кэшируемая круговая альфа-маска с плавным спадом яркости."""
        radius_px = max(2, int(radius_px))
        power = max(0, min(255, int(power)))
        key = (radius_px, power)
        surf = self._radial_light_cache.get(key)
        if surf is not None:
            return surf
        surf = pygame.Surface((radius_px*2+2, radius_px*2+2), pygame.SRCALPHA)
        c = radius_px + 1
        # Каждый внутренний круг ПЕРЕЗАПИСЫВАЕТ значение альфы маски.
        steps = max(24, min(80, radius_px // 2))
        for step in range(steps, -1, -1):
            f = step / max(1, steps)
            r = max(1, int(radius_px * f))
            intensity = int(power * max(0, 1 - f**1.65))
            pygame.draw.circle(surf, (0, 0, 0, intensity), (c, c), r)
        self._radial_light_cache[key] = surf
        return surf

    def _beam_light_sprite(self, radius_px, power, angle, width):
        """Кэшированный конус: затухает к концу и боковым границам."""
        radius_px = max(3, int(radius_px))
        power = min(255, max(0, int(power)))
        angle_bin = (round(float(angle) / 15) * 15) % 360
        width_bin = int(round(float(width) / 5) * 5)
        key = (radius_px, power, angle_bin, width_bin)
        cached = self._beam_light_cache.get(key)
        if cached is not None:
            return cached
        R = radius_px
        surface = pygame.Surface((2*R+2, 2*R+2), pygame.SRCALPHA)
        c = R + 1
        # От внешнего кольца к центру: расстояние и отклонение от
        # оси конуса независимо ослабляют луч.
        rings = 32
        half = math.radians(width_bin)
        for i in range(rings, -1, -1):
            frac = max(0.015, i / rings)
            rad = max(1, int(R * frac))
            distance_fade = (1.0 - frac**1.7)
            for angular_fraction, angular_power in (
                (1.0, .40), (.85, .69), (.65, 1.0)):
                points = [(c, c)]
                for j in range(13):
                    a = -half*angular_fraction + 2*half*angular_fraction*j/12
                    points.append((int(c + rad*math.cos(a)),
                                   int(c + rad*math.sin(a))))
                light = int(power * distance_fade * angular_power)
                pygame.draw.polygon(surface, (0, 0, 0, light), points)
        # Направление в pygame вращается против часовой стрелки.
        if angle_bin:
            surface = pygame.transform.rotate(surface, -angle_bin)
        if len(self._beam_light_cache) > 110:
            self._beam_light_cache.clear()
        self._beam_light_cache[key] = surface
        return surface

    def _light_hits_creature(self, source, ax, ay):
        dx = ax - source["x"]
        dy = ay - source["y"]
        ds = dx*dx + dy*dy
        if ds > source["radius"]**2:
            return 0.0
        if source["angle"] is not None and ds > 0.35:
            aim = math.radians(source["angle"])
            cos_angle = (dx*math.cos(aim) + dy*math.sin(aim)) / max(0.001, math.sqrt(ds))
            if cos_angle < math.cos(math.radians(source["width"])):
                return 0.0
        return max(0.0, 1.0 - math.sqrt(ds)/max(.01, source["radius"])) * (source["power"]/255)

    def _apply_light_behavior(self, animal, world, sources):
        """Притяжение и бегство без телепортации и прохода сквозь стены."""
        if getattr(animal, "is_companion", False) or animal.hp <= 0:
            return False
        name = animal.type.name
        attraction = LIGHT_ATTRACTION.get(name, 0.0)
        aversion = LIGHT_AVERSION.get(name, 0.0)
        if not (attraction or aversion):
            return False
        nearest = None
        score = 0.0
        for source in sources:
            if not source["reacts"]:
                continue
            # Специальное правило: ракета ночью — только видимый свет,
            # она не служит ни приманкой, ни защитой от хищников.
            if (source["kind"] == "flare"
                    and FLARES_DO_NOT_AFFECT_PREDATORS_AT_NIGHT
                    and self._is_dark_night()):
                continue
            effect = self._light_hits_creature(source, animal.x, animal.y)
            if effect > score:
                score, nearest = effect, source
        if nearest is None or score < .035:
            return False
        dx = nearest["x"] - animal.x
        dy = nearest["y"] - animal.y
        dist = math.hypot(dx, dy)
        if dist < 0.05:
            return False
        sign = -1 if aversion else 1
        sensitivity = aversion or attraction
        speed = animal.type.speed
        # В световом конусе реакция сильнее; у слабых видов свет лишь
        # корректирует движение, а не создаёт несоразмерный рывок.
        factor = min(1.0, .55 + score*.9) * sensitivity
        ux, uy = dx / dist * sign, dy / dist * sign
        old_x, old_y = animal.x, animal.y
        nx = old_x + ux * speed * (0.5 + factor)
        ny = old_y + uy * speed * (0.5 + factor)
        if not animal.home_biome.contains(nx, ny):
            return False
        tile = world.get_object_at(int(nx), int(ny))
        if tile is not None and tile.is_wall:
            return False
        if not self.in_cave and self.is_start_capsule_wall(int(nx), int(ny)):
            return False
        animal.x, animal.y = nx, ny
        animal.dx, animal.dy = ux * speed, uy * speed
        animal.move_timer = min(animal.move_timer, 10)
        animal._update_rotation()
        if not self.in_cave:
            self.world.update_animal_index(animal, old_x, old_y)
        return bool(aversion)

    @staticmethod
    def _color_mix(color_a, color_b, t):
        t = max(0.0, min(1.0, float(t)))
        return tuple(
            max(0, min(255, int(round(a + (b - a) * t))))
            for a, b in zip(color_a[:3], color_b[:3])
        )

    @staticmethod
    def _color_scale(color, factor):
        factor = max(0.0, float(factor))
        return tuple(
            max(0, min(255, int(round(channel * factor))))
            for channel in color[:3]
        )

    @staticmethod
    def _stable_visual_hash(*parts):
        value = 2166136261
        for part in parts:
            for ch in str(part):
                value ^= ord(ch)
                value = (value * 16777619) & 0xffffffff
        return value

    @staticmethod
    def _draw_starfish_shape(surface, x, y, radius, color, seed=0):
        rng = random.Random(seed)
        points = []
        inner = max(2, int(radius * 0.46))
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rr = radius if i % 2 == 0 else inner
            rr *= rng.uniform(0.90, 1.08)
            points.append((int(x + math.cos(ang) * rr), int(y + math.sin(ang) * rr)))
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, Game._color_scale(color, 0.65), points, 1)
        pygame.draw.circle(surface, Game._color_mix(color, (255, 240, 220), 0.35), (int(x), int(y)), max(1, radius // 3))

    def _surface_theme_for_biome(self, biome):
        if biome is None:
            return None

        cache_key = (biome.name, tuple(biome.color))
        cached = self._seabed_theme_cache.get(cache_key)
        if cached is not None:
            return cached

        name = biome.name.lower()
        base = tuple(biome.color)

        theme = {
            'key': 'generic',
            'base_mix': Game._color_mix(base, (165, 176, 184), 0.16),
            'highlight': Game._color_mix(base, (230, 238, 245), 0.22),
            'shadow': Game._color_scale(base, 0.72),
            'sand_ripples': False,
            'pebble_range': (2, 5),
            'algae_chance': 0.10,
            'coral_chance': 0.08,
            'starfish_chance': 0.02,
            'mottle_count': (3, 5),
            'coral_palette': [(188, 122, 92), (210, 160, 110), (122, 170, 170)],
            'algae_palette': [(78, 112, 78), (62, 93, 67)],
            'pebble_palette': [Game._color_mix(base, (185, 185, 185), 0.28), (92, 98, 103)],
        }

        if 'безопасные отмели' in name:
            theme.update({
                'key': 'safe_shallows',
                'base_mix': Game._color_mix(base, (222, 205, 158), 0.55),
                'highlight': Game._color_mix(base, (243, 233, 193), 0.50),
                'shadow': Game._color_mix(base, (148, 137, 102), 0.48),
                'sand_ripples': True,
                'pebble_range': (4, 8),
                'algae_chance': 0.18,
                'coral_chance': 0.22,
                'starfish_chance': 0.14,
                'mottle_count': (5, 7),
                'coral_palette': [(242, 123, 118), (255, 177, 97), (160, 110, 205), (116, 206, 205)],
                'algae_palette': [(92, 128, 83), (63, 96, 74)],
                'pebble_palette': [(177, 165, 151), (130, 121, 112), (99, 102, 105)],
            })
        elif 'бурые водоросли' in name or name == 'водоросли':
            theme.update({
                'key': 'kelp',
                'base_mix': Game._color_mix(base, (95, 110, 72), 0.36),
                'highlight': Game._color_mix(base, (145, 171, 96), 0.30),
                'shadow': Game._color_mix(base, (52, 69, 41), 0.46),
                'sand_ripples': True,
                'pebble_range': (3, 6),
                'algae_chance': 0.34,
                'coral_chance': 0.12,
                'starfish_chance': 0.06,
                'mottle_count': (5, 7),
                'coral_palette': [(212, 161, 78), (182, 108, 92), (121, 162, 170)],
                'algae_palette': [(74, 118, 54), (98, 140, 66), (55, 88, 48)],
                'pebble_palette': [(126, 122, 102), (98, 102, 87), (75, 79, 68)],
            })
        elif 'грибной лес' in name:
            theme.update({
                'key': 'mushroom',
                'base_mix': Game._color_mix(base, (77, 104, 150), 0.42),
                'highlight': Game._color_mix(base, (126, 150, 198), 0.30),
                'shadow': Game._color_mix(base, (35, 49, 77), 0.45),
                'sand_ripples': False,
                'pebble_range': (5, 8),
                'algae_chance': 0.10,
                'coral_chance': 0.14,
                'starfish_chance': 0.03,
                'mottle_count': (4, 6),
                'coral_palette': [(126, 160, 225), (178, 123, 214), (101, 194, 186)],
                'algae_palette': [(76, 108, 114), (60, 91, 100)],
                'pebble_palette': [(112, 128, 148), (88, 96, 112), (67, 72, 81)],
            })
        elif ('травянистое плато' in name or 'зона куша' in name
              or 'редкий риф' in name or 'большой риф' in name):
            theme.update({
                'key': 'reef_plateau',
                'base_mix': Game._color_mix(base, (116, 112, 124), 0.20),
                'highlight': Game._color_mix(base, (183, 161, 175), 0.18),
                'shadow': Game._color_mix(base, (74, 57, 69), 0.24),
                'sand_ripples': False,
                'pebble_range': (4, 7),
                'algae_chance': 0.22,
                'coral_chance': 0.24,
                'starfish_chance': 0.08,
                'mottle_count': (5, 7),
                'coral_palette': [(234, 130, 151), (255, 181, 106), (129, 221, 186), (142, 173, 248)],
                'algae_palette': [(76, 117, 88), (96, 145, 98), (63, 101, 85)],
                'pebble_palette': [(150, 123, 128), (119, 93, 101), (86, 76, 83)],
            })
        elif ('горы' in name or 'скалистое поле' in name or 'подводные острова' in name
              or 'зона крушения' in name):
            theme.update({
                'key': 'rocky',
                'base_mix': Game._color_mix(base, (92, 88, 82), 0.18),
                'highlight': Game._color_mix(base, (132, 127, 119), 0.18),
                'shadow': Game._color_mix(base, (38, 37, 39), 0.24),
                'sand_ripples': False,
                'pebble_range': (6, 10),
                'algae_chance': 0.08,
                'coral_chance': 0.10,
                'starfish_chance': 0.02,
                'mottle_count': (4, 7),
                'coral_palette': [(176, 120, 102), (129, 132, 145), (110, 164, 169)],
                'algae_palette': [(78, 82, 66), (66, 74, 58)],
                'pebble_palette': [(142, 137, 132), (103, 100, 96), (72, 71, 74)],
            })
        elif 'дюны' in name or 'морской путь' in name:
            theme.update({
                'key': 'dunes',
                'base_mix': Game._color_mix(base, (208, 188, 132), 0.34),
                'highlight': Game._color_mix(base, (235, 218, 174), 0.30),
                'shadow': Game._color_mix(base, (144, 128, 91), 0.28),
                'sand_ripples': True,
                'pebble_range': (3, 6),
                'algae_chance': 0.05,
                'coral_chance': 0.07,
                'starfish_chance': 0.05,
                'mottle_count': (5, 7),
                'coral_palette': [(225, 150, 99), (204, 131, 115), (112, 176, 180)],
                'algae_palette': [(90, 105, 70), (66, 84, 58)],
                'pebble_palette': [(179, 166, 140), (138, 125, 103), (111, 103, 87)],
            })

        self._seabed_theme_cache[cache_key] = theme
        return theme

    def _build_seabed_tile_surface(self, biome, variant):
        theme = self._surface_theme_for_biome(biome)
        if theme is None:
            return None

        rng = random.Random(variant * 9173 + self._stable_visual_hash(biome.name, theme['key']))
        surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        surf.fill(theme['base_mix'])

        # Мягкий градиент: верх чуть светлее, низ глубже по тону.
        for y in range(CELL_SIZE):
            frac = y / max(1, CELL_SIZE - 1)
            top_color = theme['highlight']
            low_color = theme['shadow']
            row_color = Game._color_mix(top_color, low_color, frac * 0.65)
            alpha = 36
            pygame.draw.line(surf, (*row_color, alpha), (0, y), (CELL_SIZE, y))

        # Пятна неоднородности — имитируют смену тона, песчаные/илистые участки.
        mottle_min, mottle_max = theme['mottle_count']
        for _ in range(rng.randint(mottle_min, mottle_max)):
            w = rng.randint(8, 18)
            h = rng.randint(5, 14)
            x = rng.randint(-3, CELL_SIZE - 4)
            y = rng.randint(-3, CELL_SIZE - 4)
            tint = theme['highlight'] if rng.random() < 0.45 else theme['shadow']
            alpha = rng.randint(26, 52)
            pygame.draw.ellipse(surf, (*tint, alpha), (x, y, w, h))

        # Лёгкая рябь на песке, как в отмелях и дюнах оригинала.
        if theme['sand_ripples']:
            ripple = Game._color_mix(theme['shadow'], theme['highlight'], 0.40)
            for _ in range(rng.randint(2, 4)):
                base_y = rng.randint(4, CELL_SIZE - 5)
                phase = rng.uniform(0.0, math.tau)
                amp = rng.uniform(0.8, 1.8)
                pts = []
                for xx in range(-2, CELL_SIZE + 3, 3):
                    yy = base_y + math.sin(xx * 0.33 + phase) * amp
                    pts.append((xx, int(round(yy))))
                pygame.draw.lines(surf, (*ripple, 58), False, pts, 1)

        # Маленькие камни / галька.
        pebble_count = rng.randint(*theme['pebble_range'])
        for _ in range(pebble_count):
            px = rng.randint(2, CELL_SIZE - 3)
            py = rng.randint(2, CELL_SIZE - 3)
            pw = rng.randint(2, 5)
            ph = rng.randint(2, 4)
            pcol = rng.choice(theme['pebble_palette'])
            rect = pygame.Rect(px - pw // 2, py - ph // 2, pw, ph)
            pygame.draw.ellipse(surf, pcol, rect)
            pygame.draw.ellipse(surf, Game._color_mix(pcol, (240, 240, 240), 0.22), rect.inflate(-1, -1))

        # Водорослевые обрастания и короткие донные кустики.
        if rng.random() < theme['algae_chance']:
            clump_x = rng.randint(5, CELL_SIZE - 6)
            clump_y = rng.randint(6, CELL_SIZE - 5)
            base_y = min(CELL_SIZE - 3, clump_y + rng.randint(2, 5))
            for _ in range(rng.randint(4, 7)):
                height = rng.randint(6, 12)
                bend = rng.randint(-4, 4)
                tip_x = clump_x + bend + rng.randint(-3, 3)
                tip_y = max(2, base_y - height)
                col = rng.choice(theme['algae_palette'])
                mid_x = (clump_x + tip_x) // 2 + rng.randint(-2, 2)
                mid_y = base_y - height // 2
                pygame.draw.lines(surf, (*col, 200), False,
                                  [(clump_x, base_y), (mid_x, mid_y), (tip_x, tip_y)], 1)
                pygame.draw.circle(surf, Game._color_mix(col, (220, 240, 210), 0.16),
                                   (tip_x, tip_y), 1)

        # Небольшие коралловые кустики / пластинки.
        if rng.random() < theme['coral_chance']:
            coral_x = rng.randint(5, CELL_SIZE - 6)
            coral_y = rng.randint(5, CELL_SIZE - 6)
            coral_color = rng.choice(theme['coral_palette'])
            style_roll = rng.random()
            if style_roll < 0.34:
                # Ветвистый коралл.
                base_point = (coral_x, coral_y + 3)
                for _ in range(rng.randint(3, 5)):
                    tip = (coral_x + rng.randint(-5, 5), coral_y - rng.randint(2, 6))
                    mid = ((base_point[0] + tip[0]) // 2 + rng.randint(-2, 2),
                           (base_point[1] + tip[1]) // 2 - rng.randint(0, 2))
                    pygame.draw.lines(surf, coral_color, False, [base_point, mid, tip], 2)
                    pygame.draw.circle(surf, Game._color_mix(coral_color, (250, 240, 215), 0.28), tip, 1)
            elif style_roll < 0.67:
                # Кустистый круглый коралл.
                for _ in range(rng.randint(2, 4)):
                    rr = rng.randint(2, 4)
                    ox = rng.randint(-3, 3)
                    oy = rng.randint(-3, 3)
                    pygame.draw.circle(surf, coral_color, (coral_x + ox, coral_y + oy), rr)
                    pygame.draw.circle(surf, Game._color_mix(coral_color, (255, 240, 230), 0.22),
                                       (coral_x + ox - 1, coral_y + oy - 1), max(1, rr - 1))
            else:
                # Пластинчатый коралл.
                rect = pygame.Rect(coral_x - 5, coral_y - 3, 11, 6)
                pygame.draw.ellipse(surf, coral_color, rect)
                pygame.draw.ellipse(surf, Game._color_scale(coral_color, 0.68), rect, 1)
                pygame.draw.line(surf, Game._color_mix(coral_color, (250, 240, 225), 0.25),
                                 (rect.left + 2, coral_y), (rect.right - 2, coral_y), 1)

        # Морские звёзды — редкий, но узнаваемый декоративный элемент.
        if rng.random() < theme['starfish_chance']:
            sx = rng.randint(6, CELL_SIZE - 7)
            sy = rng.randint(6, CELL_SIZE - 7)
            star_color = rng.choice([(227, 102, 86), (250, 172, 77), (189, 114, 210)])
            self._draw_starfish_shape(surf, sx, sy, rng.randint(4, 5), star_color, seed=variant * 13 + sx + sy)

        # Редкие рассеянные точки песка/детрита.
        grit = Game._color_mix(theme['highlight'], (230, 225, 210), 0.30)
        for _ in range(rng.randint(6, 11)):
            gx = rng.randint(0, CELL_SIZE - 1)
            gy = rng.randint(0, CELL_SIZE - 1)
            surf.set_at((gx, gy), (*grit, 105))

        return surf

    def _get_seabed_tile_surface(self, biome, x, y):
        if biome is None:
            return None
        cell_key = ("surface", id(biome), x, y)
        cached = self._visual_cell_cache.get(cell_key)
        if cached is not None:
            return cached
        theme = self._surface_theme_for_biome(biome)
        if theme is None:
            return None
        variant = self._stable_visual_hash(biome.name, x // 2, y // 2, x % 3, y % 3) % 24
        key = (theme['key'], tuple(theme['base_mix']), tuple(theme['highlight']), tuple(theme['shadow']), variant)
        tile = self._seabed_tile_cache.get(key)
        if tile is None:
            tile = self._build_seabed_tile_surface(biome, variant)
            self._seabed_tile_cache[key] = tile
        if len(self._visual_cell_cache) >= 20000:
            self._visual_cell_cache.clear()
        self._visual_cell_cache[cell_key] = tile
        return tile

    def _cave_theme_for_tunnel(self, tunnel):
        if tunnel is None:
            return {
                'key': 'solid_wall',
                'base_mix': (18, 18, 23),
                'highlight': (40, 40, 49),
                'shadow': (8, 8, 11),
                'mottle_count': (5, 8),
                'pebble_range': (2, 5),
                'crystal_chance': 0.10,
                'fungus_chance': 0.02,
                'fossil_chance': 0.03,
                'mineral_palette': [(80, 102, 132), (72, 84, 98), (90, 78, 68)],
            }

        parent = getattr(tunnel, 'parent_surface_biome', None)
        parent_name = parent.name if parent is not None else 'interbiome'
        cache_key = (
            tunnel.name,
            tuple(tunnel.color),
            parent_name,
            getattr(tunnel, 'cave_kind', '')
        )
        cached = self._cave_theme_cache.get(cache_key)
        if cached is not None:
            return cached

        base = tuple(tunnel.color)
        name = parent_name.lower()
        kind = getattr(tunnel, 'cave_kind', '')

        theme = {
            'key': 'generic_cave',
            'base_mix': Game._color_mix(base, (68, 77, 88), 0.24),
            'highlight': Game._color_mix(base, (126, 140, 158), 0.16),
            'shadow': Game._color_mix(base, (14, 18, 25), 0.44),
            'mottle_count': (4, 6),
            'pebble_range': (4, 8),
            'crystal_chance': 0.14,
            'fungus_chance': 0.08,
            'fossil_chance': 0.06,
            'mineral_palette': [(119, 146, 186), (106, 128, 149), (122, 109, 95)],
        }

        if 'безопасные отмели' in name:
            theme.update({
                'key': 'shallow_cave',
                'base_mix': Game._color_mix(base, (101, 88, 76), 0.24),
                'highlight': Game._color_mix(base, (158, 141, 120), 0.18),
                'shadow': Game._color_mix(base, (28, 24, 24), 0.40),
                'mottle_count': (5, 7),
                'pebble_range': (5, 9),
                'crystal_chance': 0.10,
                'fungus_chance': 0.04,
                'fossil_chance': 0.08,
                'mineral_palette': [(145, 128, 103), (98, 94, 90), (122, 154, 171)],
            })
        elif ('грибной лес' in name or 'большой риф' in name or 'редкий риф' in name):
            theme.update({
                'key': 'fungal_cave',
                'base_mix': Game._color_mix(base, (74, 83, 109), 0.26),
                'highlight': Game._color_mix(base, (138, 155, 192), 0.18),
                'shadow': Game._color_mix(base, (18, 20, 32), 0.42),
                'crystal_chance': 0.19,
                'fungus_chance': 0.18,
                'fossil_chance': 0.05,
                'mineral_palette': [(145, 176, 229), (168, 116, 206), (115, 188, 184)],
            })
        elif ('бурые водоросли' in name or 'водоросли' == name or 'зона куша' in name):
            theme.update({
                'key': 'kelp_cave',
                'base_mix': Game._color_mix(base, (76, 84, 63), 0.24),
                'highlight': Game._color_mix(base, (118, 138, 96), 0.16),
                'shadow': Game._color_mix(base, (18, 24, 18), 0.44),
                'crystal_chance': 0.10,
                'fungus_chance': 0.10,
                'fossil_chance': 0.05,
                'mineral_palette': [(122, 136, 96), (84, 92, 72), (113, 154, 120)],
            })
        elif ('горы' in name or 'скалистое поле' in name or 'зона крушения' in name
              or 'подводные острова' in name):
            theme.update({
                'key': 'rock_cave',
                'base_mix': Game._color_mix(base, (82, 78, 82), 0.18),
                'highlight': Game._color_mix(base, (132, 126, 136), 0.14),
                'shadow': Game._color_mix(base, (13, 14, 18), 0.48),
                'mottle_count': (5, 8),
                'pebble_range': (6, 10),
                'crystal_chance': 0.09,
                'fungus_chance': 0.04,
                'fossil_chance': 0.10,
                'mineral_palette': [(122, 124, 136), (92, 94, 104), (126, 110, 96)],
            })
        elif ('дюны' in name or 'морской путь' in name):
            theme.update({
                'key': 'dune_cave',
                'base_mix': Game._color_mix(base, (118, 103, 76), 0.24),
                'highlight': Game._color_mix(base, (176, 158, 114), 0.16),
                'shadow': Game._color_mix(base, (30, 24, 18), 0.44),
                'crystal_chance': 0.07,
                'fungus_chance': 0.03,
                'fossil_chance': 0.10,
                'mineral_palette': [(150, 129, 91), (124, 111, 88), (162, 166, 154)],
            })

        if kind in ('hub', 'branch_room'):
            theme['highlight'] = Game._color_mix(theme['highlight'], (190, 206, 220), 0.14)
            theme['crystal_chance'] = min(0.24, theme['crystal_chance'] + 0.04)
            theme['fungus_chance'] = min(0.22, theme['fungus_chance'] + 0.03)
            theme['mottle_count'] = (theme['mottle_count'][0] + 1, theme['mottle_count'][1] + 1)
        elif kind in ('interbiome_corridor', 'local_corridor'):
            theme['shadow'] = Game._color_mix(theme['shadow'], (7, 8, 10), 0.18)
            theme['crystal_chance'] = max(0.05, theme['crystal_chance'] - 0.03)
            theme['fungus_chance'] = max(0.02, theme['fungus_chance'] - 0.02)
        elif kind == 'interbiome_junction':
            theme['highlight'] = Game._color_mix(theme['highlight'], (166, 174, 188), 0.10)
            theme['fossil_chance'] = min(0.12, theme['fossil_chance'] + 0.03)

        self._cave_theme_cache[cache_key] = theme
        return theme

    def _build_cave_floor_tile_surface(self, tunnel, variant):
        theme = self._cave_theme_for_tunnel(tunnel)
        if theme is None:
            return None

        seed = self._stable_visual_hash(tunnel.name, theme['key'], variant)
        rng = random.Random(seed)
        surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        surf.fill(theme['base_mix'])

        # Градиент глубины и влажные затемнения.
        for y in range(CELL_SIZE):
            frac = y / max(1, CELL_SIZE - 1)
            row_color = Game._color_mix(theme['highlight'], theme['shadow'], frac * 0.80)
            alpha = 40 + int(18 * frac)
            pygame.draw.line(surf, (*row_color, alpha), (0, y), (CELL_SIZE, y))

        # Пятна, имитирующие смену породы и мокрые участки.
        mottle_min, mottle_max = theme['mottle_count']
        for _ in range(rng.randint(mottle_min, mottle_max)):
            w = rng.randint(6, 18)
            h = rng.randint(5, 14)
            x = rng.randint(-4, CELL_SIZE - 4)
            y = rng.randint(-3, CELL_SIZE - 4)
            tint = theme['highlight'] if rng.random() < 0.42 else theme['shadow']
            alpha = rng.randint(24, 54)
            pygame.draw.ellipse(surf, (*tint, alpha), (x, y, w, h))

        # Каменные прожилки и мелкие трещины.
        vein_color = Game._color_mix(theme['shadow'], theme['highlight'], 0.30)
        for _ in range(rng.randint(2, 4)):
            sx = rng.randint(-2, CELL_SIZE // 3)
            sy = rng.randint(1, CELL_SIZE - 2)
            pts = [(sx, sy)]
            cx = sx
            cy = sy
            for _step in range(rng.randint(2, 4)):
                cx += rng.randint(3, 7)
                cy += rng.randint(-3, 3)
                pts.append((max(-2, min(CELL_SIZE + 2, cx)), max(0, min(CELL_SIZE - 1, cy))))
            pygame.draw.lines(surf, (*vein_color, 65), False, pts, 1)

        # Россыпь мелких камней и щебня.
        for _ in range(rng.randint(*theme['pebble_range'])):
            px = rng.randint(2, CELL_SIZE - 3)
            py = rng.randint(2, CELL_SIZE - 3)
            pw = rng.randint(2, 5)
            ph = rng.randint(2, 4)
            pcol = rng.choice(theme['mineral_palette'])
            rect = pygame.Rect(px - pw // 2, py - ph // 2, pw, ph)
            pygame.draw.ellipse(surf, pcol, rect)
            inner = rect.inflate(-1, -1)
            if inner.width > 0 and inner.height > 0:
                pygame.draw.ellipse(surf, Game._color_mix(pcol, (222, 226, 232), 0.20), inner)

        # Сталагмитики / каменные зубцы.
        if rng.random() < 0.22:
            base_x = rng.randint(5, CELL_SIZE - 6)
            base_y = rng.randint(CELL_SIZE // 2, CELL_SIZE - 3)
            count = rng.randint(2, 4)
            ridge_col = Game._color_mix(theme['shadow'], theme['base_mix'], 0.45)
            for idx in range(count):
                height = rng.randint(5, 10)
                width = rng.randint(3, 5)
                cx = base_x + idx * rng.randint(2, 4) - count
                pts = [
                    (cx - width // 2, base_y),
                    (cx, base_y - height),
                    (cx + width // 2, base_y),
                ]
                pygame.draw.polygon(surf, ridge_col, pts)
                pygame.draw.line(surf, Game._color_mix(ridge_col, (190, 195, 205), 0.18), pts[0], pts[1], 1)

        # Кристаллические жилы / небольшие скопления.
        if rng.random() < theme['crystal_chance']:
            crystal_color = rng.choice(theme['mineral_palette'])
            crystal_color = Game._color_mix(crystal_color, (185, 220, 255), 0.24)
            origin_x = rng.randint(4, CELL_SIZE - 5)
            origin_y = rng.randint(4, CELL_SIZE - 5)
            for _ in range(rng.randint(2, 4)):
                cx = origin_x + rng.randint(-4, 4)
                cy = origin_y + rng.randint(-3, 3)
                h = rng.randint(4, 8)
                w = rng.randint(2, 4)
                pts = [(cx, cy - h), (cx + w, cy), (cx, cy + 1), (cx - w, cy)]
                pygame.draw.polygon(surf, crystal_color, pts)
                pygame.draw.polygon(surf, Game._color_scale(crystal_color, 0.55), pts, 1)
                pygame.draw.line(surf, Game._color_mix(crystal_color, (245, 250, 255), 0.45), (cx, cy - h + 1), (cx, cy), 1)

        # Пещерные грибки / коралловые натёки.
        if rng.random() < theme['fungus_chance']:
            stem = Game._color_mix(theme['highlight'], (208, 214, 224), 0.22)
            cap = Game._color_mix(rng.choice(theme['mineral_palette']), (208, 170, 224), 0.30)
            base_x = rng.randint(5, CELL_SIZE - 6)
            base_y = rng.randint(7, CELL_SIZE - 5)
            for _ in range(rng.randint(2, 3)):
                cx = base_x + rng.randint(-4, 4)
                h = rng.randint(4, 7)
                pygame.draw.line(surf, stem, (cx, base_y), (cx, base_y - h), 1)
                rect = pygame.Rect(cx - 3, base_y - h - 2, 7, 4)
                pygame.draw.ellipse(surf, cap, rect)
                pygame.draw.ellipse(surf, Game._color_scale(cap, 0.60), rect, 1)

        # Отпечатки / окаменелости в породе.
        if rng.random() < theme['fossil_chance']:
            fossil = Game._color_mix(theme['shadow'], theme['highlight'], 0.55)
            fx = rng.randint(6, CELL_SIZE - 7)
            fy = rng.randint(6, CELL_SIZE - 7)
            style = rng.random()
            if style < 0.5:
                pygame.draw.arc(surf, (*fossil, 130), (fx - 5, fy - 4, 10, 8), math.pi * 0.15, math.pi * 1.75, 1)
                pygame.draw.arc(surf, (*fossil, 90), (fx - 3, fy - 2, 6, 4), math.pi * 0.15, math.pi * 1.75, 1)
            else:
                for off in range(-3, 4, 2):
                    pygame.draw.line(surf, (*fossil, 120), (fx - 4, fy + off), (fx + 4, fy + off // 2), 1)

        # Пыль, ил и микро-детрит.
        grit = Game._color_mix(theme['highlight'], (220, 220, 225), 0.24)
        for _ in range(rng.randint(6, 12)):
            gx = rng.randint(0, CELL_SIZE - 1)
            gy = rng.randint(0, CELL_SIZE - 1)
            surf.set_at((gx, gy), (*grit, 95))

        return surf

    def _build_cave_wall_tile_surface(self, variant):
        rng = random.Random(310000 + variant * 271)
        surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        base = (13, 13, 18)
        high = (34, 34, 42)
        deep = (5, 5, 8)
        surf.fill(base)

        for y in range(CELL_SIZE):
            frac = y / max(1, CELL_SIZE - 1)
            row = Game._color_mix(high, deep, frac * 0.78)
            pygame.draw.line(surf, (*row, 42), (0, y), (CELL_SIZE, y))

        for _ in range(rng.randint(6, 10)):
            x = rng.randint(-4, CELL_SIZE - 4)
            y = rng.randint(-3, CELL_SIZE - 4)
            w = rng.randint(7, 16)
            h = rng.randint(5, 14)
            col = high if rng.random() < 0.42 else deep
            pygame.draw.ellipse(surf, (*col, rng.randint(24, 52)), (x, y, w, h))

        for _ in range(rng.randint(2, 4)):
            sx = rng.randint(0, CELL_SIZE - 1)
            sy = rng.randint(0, CELL_SIZE - 1)
            pts = [(sx, sy)]
            cx = sx
            cy = sy
            for _step in range(rng.randint(2, 5)):
                cx += rng.randint(-4, 4)
                cy += rng.randint(2, 6)
                pts.append((max(0, min(CELL_SIZE - 1, cx)), max(0, min(CELL_SIZE - 1, cy))))
            pygame.draw.lines(surf, (48, 48, 57, 90), False, pts, 1)

        # Вкрапления породы.
        for _ in range(rng.randint(5, 9)):
            cx = rng.randint(2, CELL_SIZE - 3)
            cy = rng.randint(2, CELL_SIZE - 3)
            rr = rng.randint(1, 3)
            col = rng.choice([(62, 65, 76), (78, 84, 92), (56, 48, 44)])
            pygame.draw.circle(surf, col, (cx, cy), rr)
            if rr > 1:
                pygame.draw.circle(surf, Game._color_mix(col, (170, 176, 184), 0.18), (cx - 1, cy - 1), rr - 1)

        # Виньетка: центр немного читаемее, углы темнее.
        pygame.draw.rect(surf, (0, 0, 0, 34), (0, 0, CELL_SIZE, CELL_SIZE), 2)
        return surf

    def _get_cave_floor_tile_surface(self, tunnel, x, y):
        if tunnel is None:
            return None
        cell_key = ("cave", id(tunnel), x, y)
        cached = self._visual_cell_cache.get(cell_key)
        if cached is not None:
            return cached
        theme = self._cave_theme_for_tunnel(tunnel)
        variant = self._stable_visual_hash(tunnel.name, x // 2, y // 2, x % 3, y % 3) % 24
        key = (theme['key'], tuple(theme['base_mix']), tuple(theme['highlight']), tuple(theme['shadow']), variant)
        tile = self._cave_floor_tile_cache.get(key)
        if tile is None:
            tile = self._build_cave_floor_tile_surface(tunnel, variant)
            self._cave_floor_tile_cache[key] = tile
        if len(self._visual_cell_cache) >= 20000:
            self._visual_cell_cache.clear()
        self._visual_cell_cache[cell_key] = tile
        return tile

    def _get_cave_wall_tile_surface(self, x, y):
        cell_key = ("wall", x, y)
        cached = self._visual_cell_cache.get(cell_key)
        if cached is not None:
            return cached
        variant = self._stable_visual_hash('cave_wall', x // 2, y // 2, x % 5, y % 5) % 32
        tile = self._cave_wall_tile_cache.get(variant)
        if tile is None:
            tile = self._build_cave_wall_tile_surface(variant)
            self._cave_wall_tile_cache[variant] = tile
        if len(self._visual_cell_cache) >= 20000:
            self._visual_cell_cache.clear()
        self._visual_cell_cache[cell_key] = tile
        return tile

    def draw_cave_cell(self, x, y, screen_x, screen_y, tunnel):
        if tunnel is None:
            wall = self._get_cave_wall_tile_surface(x, y)
            self.screen.blit(wall, (screen_x, screen_y))
            return

        tile = (self._get_cave_floor_tile_surface(tunnel, x, y)
                if getattr(self, "setting_seabed_details_enabled", True)
                else None)
        if tile is not None:
            self.screen.blit(tile, (screen_x, screen_y))
        else:
            pygame.draw.rect(
                self.screen, tunnel.color,
                (screen_x, screen_y, CELL_SIZE, CELL_SIZE)
            )

        # Плавное затемнение у стен — тоннели читаются объёмнее.
        edge_shadow = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        neighbors = {
            'top': self.get_cave_tunnel_at(x, y - 1) is None,
            'bottom': self.get_cave_tunnel_at(x, y + 1) is None,
            'left': self.get_cave_tunnel_at(x - 1, y) is None,
            'right': self.get_cave_tunnel_at(x + 1, y) is None,
        }
        if neighbors['top']:
            pygame.draw.rect(edge_shadow, (0, 0, 0, 56), (0, 0, CELL_SIZE, 4))
        if neighbors['bottom']:
            pygame.draw.rect(edge_shadow, (0, 0, 0, 60), (0, CELL_SIZE - 4, CELL_SIZE, 4))
        if neighbors['left']:
            pygame.draw.rect(edge_shadow, (0, 0, 0, 52), (0, 0, 4, CELL_SIZE))
        if neighbors['right']:
            pygame.draw.rect(edge_shadow, (0, 0, 0, 52), (CELL_SIZE - 4, 0, 4, CELL_SIZE))
        if (neighbors['top'] and neighbors['left']):
            pygame.draw.circle(edge_shadow, (0, 0, 0, 48), (2, 2), 4)
        if (neighbors['top'] and neighbors['right']):
            pygame.draw.circle(edge_shadow, (0, 0, 0, 48), (CELL_SIZE - 3, 2), 4)
        if (neighbors['bottom'] and neighbors['left']):
            pygame.draw.circle(edge_shadow, (0, 0, 0, 48), (2, CELL_SIZE - 3), 4)
        if (neighbors['bottom'] and neighbors['right']):
            pygame.draw.circle(edge_shadow, (0, 0, 0, 48), (CELL_SIZE - 3, CELL_SIZE - 3), 4)
        self.screen.blit(edge_shadow, (screen_x, screen_y))

        border = Game._color_mix(tuple(tunnel.color), (165, 176, 190), 0.32)
        pygame.draw.rect(self.screen, border, (screen_x, screen_y, CELL_SIZE, CELL_SIZE), 1)

    def draw_surface_seabed_cell(self, x, y, screen_x, screen_y, biome):
        if not getattr(self, "setting_seabed_details_enabled", True):
            return
        tile = self._get_seabed_tile_surface(biome, x, y)
        if tile is not None:
            self.screen.blit(tile, (screen_x, screen_y))

    def draw_day_night_overlay(self):
        """Маски света вырезают плавные пятна и лучи в чёрной завесе."""
        if not getattr(self, "setting_water_darkening_enabled", True):
            return
        if self.in_cave:
            alpha = 250
        else:
            brightness = self._solar_brightness()
            if MIDNIGHT_BLACKOUT and (
                    min(self._visual_day_time(), 1.0-self._visual_day_time())
                    <= MIDNIGHT_BLACKOUT_HALF_WINDOW):
                alpha = 255
            else:
                twilight = max(0.0, min(1.0, (.72-brightness)/.72))
                alpha = round(255 * twilight**1.5)
        if alpha <= 0:
            return
        overlay = self.lighting_overlay
        overlay.fill((0, 0, 0, alpha))
        camera_x, camera_y = self.get_render_camera_origin()
        if LIGHTING_ENABLED:
            for src in self._collect_light_sources():
                sx = int((src["x"] - camera_x) * CELL_SIZE + CELL_SIZE//2)
                sy = int((src["y"] - camera_y) * CELL_SIZE + CELL_SIZE//2)
                radius = max(3, int(src["radius"] * CELL_SIZE))
                if (sx < -radius or sy < -radius or
                        sx > self._render_canvas_size+radius or sy > self._render_canvas_size+radius):
                    continue
                if src["angle"] is None:
                    light = self._radial_light_sprite(radius, src["power"])
                else:
                    light = self._beam_light_sprite(radius, src["power"],
                                                     src["angle"], src["width"])
                # Вычитаем освещённость из непрозрачности ночной завесы.
                overlay.blit(light, light.get_rect(center=(sx,sy)),
                             special_flags=pygame.BLEND_RGBA_SUB)
        self.screen.blit(overlay, (0, 0))

    def draw_light_emitters(self, camera_x, camera_y):
        """Яркие сердцевины источников видны даже среди чёрной воды."""
        if not LIGHTING_ENABLED:
            return
        for src in self._collect_light_sources():
            if src["kind"] == "room":
                continue  # комната светит изнутри, но не точечный прожектор
            sx = int((src["x"] - camera_x) * CELL_SIZE + CELL_SIZE//2)
            sy = int((src["y"] - camera_y) * CELL_SIZE + CELL_SIZE//2)
            if not (-20 <= sx <= self._render_canvas_size+20 and -20 <= sy <= self._render_canvas_size+20):
                continue
            # Экран с RGBA: небольшая мягкая ореольная подсветка.
            color = src["color"]
            glow = self._emitter_glow_cache.get(color)
            if glow is None:
                glow = pygame.Surface((50, 50), pygame.SRCALPHA)
                pygame.draw.circle(glow, (*color, 16), (25, 25), 23)
                pygame.draw.circle(glow, (*color, 27), (25, 25), 14)
                pygame.draw.circle(glow, (*color, 75), (25, 25), 7)
                self._emitter_glow_cache[color] = glow
            self.screen.blit(glow, (sx-25, sy-25))
            pygame.draw.circle(self.screen,
                tuple(min(255, channel+28) for channel in color),
                (sx,sy), 2)

    def _draw_one_bioglow(self, image, center, alpha):
        if image is None:
            return
        image.set_alpha(max(0, min(255, int(alpha))))
        self.screen.blit(image, image.get_rect(center=center))

    def draw_bioluminescence(self, camera_x, camera_y):
        """Динамическое свечение ВСЕХ видимых растений и животных.

        Работает и в пещерах, и с питомцами, и с высаженной флорой.
        Сканер, инвентарь и крафт не меняют свой исходный интерфейс.
        """
        if not BIOLUMINESCENCE_ENABLED:
            return

        night_strength = 1.0 if self.in_cave else max(
            0.0, 1.0 - self._solar_brightness() * 1.35
        )
        base_alpha = (BIOGLOW_DAY_ALPHA
                      + (BIOGLOW_NIGHT_ALPHA - BIOGLOW_DAY_ALPHA) * night_strength)
        pulse = 0.88 + 0.12 * math.sin(self.frame_count * 0.045)
        alpha = round(base_alpha * pulse)

        start_x = max(0, int(math.floor(camera_x)) - 2)
        start_y = max(0, int(math.floor(camera_y)) - 2)
        end_x = min(MAP_SIZE - 1, int(math.ceil(camera_x + self._render_view_radius * 2)) + 2)
        end_y = min(MAP_SIZE - 1, int(math.ceil(camera_y + self._render_view_radius * 2)) + 2)
        flora_grid = self._current_flora_grid()
        object_grid = self._get_current_object_grid()
        planter_types = self._planter_types()

        for y in range(start_y, end_y + 1):
            sy = int(round((y - camera_y) * CELL_SIZE + CELL_SIZE // 2))
            for x in range(start_x, end_x + 1):
                sx = int(round((x - camera_x) * CELL_SIZE + CELL_SIZE // 2))
                flora = flora_grid.get((x, y))
                if flora is not None:
                    self._draw_one_bioglow(flora.glow_image, (sx, sy), alpha)

                obj = object_grid.get((x, y))
                if obj is not None:
                    # Светящиеся съедобные водоросли, грибы и кораллы.
                    self._draw_one_bioglow(
                        getattr(obj, 'glow_image', None), (sx, sy), alpha
                    )

                if obj in planter_types:
                    planted = self.planted_flora.get(self._planter_key(x, y), ())
                    offsets = ((0, 1), (-8, -3), (8, -3), (-8, 7),
                               (8, 7), (0, -8), (0, 9))
                    max_size = 20 if len(planted) <= 2 else 15
                    for index, plant in enumerate(planted):
                        if plant.glow_image is None:
                            continue
                        key = (plant, max_size)
                        glow = self._bio_planted_scaled_cache.get(key)
                        if glow is None:
                            # Размер должен совпадать с обычной картинкой
                            # с учётом дополнительных полей свечения.
                            original = plant.image
                            scale = min(max_size / max(1, original.get_width()),
                                        max_size / max(1, original.get_height()))
                            target = (max(1, round(plant.glow_image.get_width() * scale)),
                                      max(1, round(plant.glow_image.get_height() * scale)))
                            glow = pygame.transform.smoothscale(plant.glow_image, target)
                            self._bio_planted_scaled_cache[key] = glow
                        ox, oy = offsets[index % len(offsets)]
                        self._draw_one_bioglow(glow, (sx + ox, sy + oy), alpha)

        for animal in self.get_nearby_animals(self._render_view_radius + 2):
            if animal.hp <= 0:
                continue
            sx = int((animal.x - camera_x) * CELL_SIZE + CELL_SIZE // 2)
            sy = int((animal.y - camera_y) * CELL_SIZE + CELL_SIZE // 2)
            phase = (animal.x * 0.27 + animal.y * 0.39)
            creature_pulse = 0.93 + 0.07 * math.sin(
                self.frame_count * 0.052 + phase
            )
            bioglow = animal.rotated_glow or animal.type.glow_image
            if animal.type.electric_glow_frames:
                # Электрические импульсы пробегают между концами ампул.
                # У разных угрей импульсы не синхронизированы.
                phase = (self.frame_count // 5 +
                         int(animal.x * 3 + animal.y * 7)) % 6
                bioglow = animal.type.get_rotated_glow(
                    getattr(animal, 'visual_angle', 0), phase
                )
            self._draw_one_bioglow(
                bioglow, (sx, sy), round(alpha * creature_pulse)
            )

    # =====================================================
    # ОБНОВЛЕНИЕ
    # =====================================================

    def update(self):
        if self.state == "map":
            self.update_map_pan()
            self.update_notification()
            return

        if self.state != "playing":
            self.update_notification()
            return
        if self.settings_open:
            self.update_notification()
            return

        # -------------------------------------------------
        # ВРЕМЯ СУТОК
        # -------------------------------------------------

        self.day_time = (self.day_time + self.day_speed) % 1.0
        self.elapsed_game_days += self.day_speed

        while (self.elapsed_game_days + 1e-9
               >= self.next_ecosystem_refresh_day):
            self.refresh_ecosystem()
            self.next_ecosystem_refresh_day += (
                self.ecosystem_refresh_interval_days
            )

        # -------------------------------------------------
        # ДВИЖЕНИЕ ИГРОКА
        # -------------------------------------------------

        keys = pygame.key.get_pressed()

        # Игрок и транспорт используют одну координату камеры, но разные скорости.
        # Мотылёк быстрее, Циклоп тяжелее; модификаторы пловца на судно не действуют.
        if self.active_vehicle is seamoth_type:
            move_speed = 0.78
        elif self.active_vehicle is cyclops_type:
            move_speed = 0.46
        else:
            move_speed = 0.5
            if self.inventory_counts.get(fins_type, 0) > 0:
                move_speed *= 1.15
            if self.seaglide_on:
                move_speed *= 1.55
            if self.speed_boost_timer > 0:
                move_speed *= 1.35

        dx = 0
        dy = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -move_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = move_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -move_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = move_speed

        joy_x, joy_y = self.mobile_controls.movement()
        if abs(joy_x) > 0.05 or abs(joy_y) > 0.05:
            dx = joy_x * move_speed
            dy = joy_y * move_speed

        old_player_x = self.player_x
        old_player_y = self.player_y

        new_x = self.player_x + dx
        new_y = self.player_y + dy

        if (0 <= new_x < MAP_SIZE and 0 <= new_y < MAP_SIZE):
            if self.in_cave:
                if self.cave_is_passable(new_x, new_y):
                    self.player_x = new_x
                    self.player_y = new_y
            else:
                target_object = self.world.get_object_at(
                    int(new_x), int(new_y)
                )
                biome = self.world.get_biome_at(
                    int(new_x), int(new_y)
                )

                object_passable = (
                    target_object is None
                    or not target_object.is_wall
                )

                target_cell_x = int(new_x)
                target_cell_y = int(new_y)
                capsule_wall = self.is_start_capsule_wall(
                    target_cell_x, target_cell_y
                )

                if self.is_start_capsule_passage(
                        target_cell_x, target_cell_y):
                    biome_passable = True
                else:
                    biome_passable = (
                        biome is None or biome.passable
                    )

                if (object_passable and biome_passable
                        and not capsule_wall):
                    self.player_x = new_x
                    self.player_y = new_y

        player_move_x = self.player_x - old_player_x
        player_move_y = self.player_y - old_player_y
        if self.active_vehicle is None and player_move_x * player_move_x + player_move_y * player_move_y > 0.00001:
            self._play_effect("swim", 0.22, 2200)

        # -------------------------------------------------
        # ПОВОРОТ ИГРОКА
        # -------------------------------------------------

        mouse_x, mouse_y = (self.mobile_controls.aim_pos
                             if self.mobile_controls.enabled
                             and self.mobile_controls.aim_pos is not None
                             else pygame.mouse.get_pos())

        for decoy in self.active_decoys:
            if decoy["in_cave"] != self.in_cave:
                continue
            screen_x = int((decoy["x"] - camera_x) * CELL_SIZE + CELL_SIZE // 2)
            screen_y = int((decoy["y"] - camera_y) * CELL_SIZE + CELL_SIZE // 2)
            pulse = 8 + (self.frame_count // 6) % 6
            pygame.draw.circle(self.screen, (255, 170, 70), (screen_x, screen_y), pulse, 2)
            pygame.draw.circle(self.screen, (255, 235, 120), (screen_x, screen_y), 3)

        player_screen_x = VIEW_RADIUS * CELL_SIZE + CELL_SIZE // 2
        player_screen_y = VIEW_RADIUS * CELL_SIZE + CELL_SIZE // 2

        mouse_dx = mouse_x - player_screen_x
        mouse_dy = mouse_y - player_screen_y

        if mouse_dx != 0 or mouse_dy != 0:
            self.player_angle = math.degrees(
                math.atan2(mouse_dy, mouse_dx)
            )

        # Камера движется вместе с игроком даже без движения мыши,
        # поэтому мировая координата прицела обновляется каждый кадр.
        self.mouse_world_x, self.mouse_world_y = self.screen_to_world(
            mouse_x, mouse_y
        )

        self._update_vehicle_torpedoes()

        # -------------------------------------------------
        # ЖИВОТНЫЕ
        # -------------------------------------------------

        active_radius = VIEW_RADIUS + 2
        active_radius_squared = active_radius ** 2

        player_x = self.player_x
        player_y = self.player_y
        active_world = self.cave_world if self.in_cave else self.world
        light_sources = self._collect_light_sources()
        self._update_crashfish_shelters()

        # Таймер атаки продолжает идти и у хищников вне экрана, как и
        # в исходной версии, но без полного обхода всех животных.
        for animal in tuple(self.cooldown_animals):
            if animal.hp <= 0:
                self.cooldown_animals.discard(animal)
                continue
            if animal.attack_timer > 0:
                animal.attack_timer -= 1
            if animal.attack_timer <= 0:
                self.cooldown_animals.discard(animal)

        for animal in self.get_nearby_animals(active_radius):
            if animal.hp <= 0:
                continue

            if getattr(animal, "stasis_timer", 0) > 0:
                animal.stasis_timer -= 1
                animal.active = True
                continue

            animal_dx = animal.x - player_x
            animal_dy = animal.y - player_y

            distance_squared = animal_dx ** 2 + animal_dy ** 2

            if distance_squared > active_radius_squared:
                animal.active = False
                continue

            old_animal_x = animal.x
            old_animal_y = animal.y

            if getattr(animal, "is_shelter_crashfish", False):
                self._update_shelter_crashfish(animal, active_world)
            elif getattr(animal, "is_companion", False):
                self._update_companion(
                    animal, player_move_x, player_move_y
                )
            else:
                pet_target = getattr(animal, "pet_combat_target", None)
                pet_target_valid = (
                    pet_target is not None
                    and getattr(pet_target, "is_companion", False)
                    and pet_target.hp > 0
                    and pet_target in self.get_current_animals()
                    and abs(pet_target.x - player_x) <= VIEW_RADIUS
                    and abs(pet_target.y - player_y) <= VIEW_RADIUS
                    and animal.type.behavior == "predator"
                )
                if not pet_target_valid:
                    animal.pet_combat_target = None
                    pet_target = None

                if pet_target is not None:
                    # Reuse the normal predator locomotion, but use the pet as
                    # the chase target instead of the diver.
                    animal.update(pet_target.x, pet_target.y, active_world)
                else:
                    animal.update(player_x, player_y, active_world)

            # Прожекторы/фары влияют только на диких существ,
            # не перебивая защиту питомца от конкретного хищника.
            light_frightened = False
            if (not getattr(animal, "is_companion", False)
                    and not getattr(animal, "is_shelter_crashfish", False)
                    and getattr(animal, "pet_combat_target", None) is None):
                light_frightened = self._apply_light_behavior(
                    animal, active_world, light_sources)

            if (not self.in_cave
                    and not getattr(animal, "is_companion", False)
                    and self.is_start_capsule_wall(
                        int(animal.x), int(animal.y))):
                animal.x = old_animal_x
                animal.y = old_animal_y
                animal.dx = -animal.dx
                animal.dy = -animal.dy
                animal._update_rotation()

            if not self.in_cave:
                self.world.update_animal_index(
                    animal, old_animal_x, old_animal_y
                )

            if (animal.type.behavior == "predator"
                    and not getattr(animal, "is_companion", False)
                    and not getattr(animal, "is_shelter_crashfish", False)):
                same_layer_decoys = [
                    d for d in self.active_decoys if d["in_cave"] == self.in_cave
                ]
                if same_layer_decoys:
                    nearest_decoy = min(
                        same_layer_decoys,
                        key=lambda d: (animal.x - d["x"]) ** 2 + (animal.y - d["y"]) ** 2
                    )
                    ddx = nearest_decoy["x"] - animal.x
                    ddy = nearest_decoy["y"] - animal.y
                    dist = math.hypot(ddx, ddy)
                    if 0.1 < dist <= 6.0:
                        effect_old_x, effect_old_y = animal.x, animal.y
                        candidate_x = animal.x + (ddx / dist) * animal.type.speed * 1.6
                        candidate_y = animal.y + (ddy / dist) * animal.type.speed * 1.6
                        if animal.home_biome.contains(candidate_x, candidate_y):
                            animal.x = candidate_x
                            animal.y = candidate_y
                        animal.attack_timer = max(animal.attack_timer, 45)
                        animal._update_rotation()
                        if not self.in_cave:
                            self.world.update_animal_index(
                                animal, effect_old_x, effect_old_y
                            )
                if (self.active_flare_timer > 0
                        and not self._is_dark_night()
                        and animal.type.name not in LIGHT_ATTRACTION):
                    flare_dx = animal.x - player_x
                    flare_dy = animal.y - player_y
                    flare_dist_sq = flare_dx ** 2 + flare_dy ** 2
                    if 0.01 < flare_dist_sq <= 49.0:
                        flare_dist = math.sqrt(flare_dist_sq)
                        effect_old_x, effect_old_y = animal.x, animal.y
                        candidate_x = animal.x + (flare_dx / flare_dist) * animal.type.speed * 2.2
                        candidate_y = animal.y + (flare_dy / flare_dist) * animal.type.speed * 2.2
                        if animal.home_biome.contains(candidate_x, candidate_y):
                            animal.x = candidate_x
                            animal.y = candidate_y
                        animal.attack_timer = max(animal.attack_timer, 45)
                        animal._update_rotation()
                        if not self.in_cave:
                            self.world.update_animal_index(
                                animal, effect_old_x, effect_old_y
                            )

            if (getattr(animal, "is_shelter_crashfish", False)
                    or getattr(animal, "is_companion", False)
                    or animal.type.behavior != "predator"
                    or not animal.active
                    or light_frightened):
                continue

            pet_target = getattr(animal, "pet_combat_target", None)
            if (pet_target is not None
                    and getattr(pet_target, "is_companion", False)
                    and pet_target.hp > 0
                    and pet_target in self.get_current_animals()):
                attack_dx = animal.x - pet_target.x
                attack_dy = animal.y - pet_target.y
                attack_distance_squared = attack_dx ** 2 + attack_dy ** 2
                if (attack_distance_squared <= 2.25
                        and animal.attack_timer <= 0):
                    if animal.type is ampeel_type:
                        self._play_effect("spark", 0.7 * max(0.0, 1.0 - math.sqrt(distance_squared) / 18.0), 800)
                    pet_target.hp -= max(1, int(animal.type.damage))
                    animal.attack_timer = animal.attack_cooldown
                    self.cooldown_animals.add(animal)
                    if pet_target.hp <= 0:
                        pet_target.hp = 0
                        self._clear_companion_target(pet_target)
                        self.remove_current_animal(pet_target)
                        animal.pet_combat_target = None
                        self.notification = (
                            f"{pet_target.type.name} погиб в бою с "
                            f"{animal.type.name}"
                        )
                        self.notification_timer = 90
                continue

            attack_dx = animal.x - player_x
            attack_dy = animal.y - player_y
            attack_distance_squared = (
                attack_dx ** 2 + attack_dy ** 2
            )

            if (attack_distance_squared <= 2.25
                    and animal.attack_timer <= 0):
                if animal.type is ampeel_type:
                    self._play_effect("spark", 0.7 * max(0.0, 1.0 - math.sqrt(attack_distance_squared) / 18.0), 800)
                if self.active_vehicle is not None:
                    self.vehicle_take_damage(animal.type.damage)
                else:
                    self.player_take_damage(animal.type.damage)
                animal.attack_timer = animal.attack_cooldown
                self.cooldown_animals.add(animal)

        self._update_special_creature_attacks()

        # -------------------------------------------------
        # ГОЛОД / ЖАЖДА
        # -------------------------------------------------

        self.hunger_timer += 1
        self.thirst_timer += 1

        hunger_loss = 0.2
        thirst_loss = 0.2
        if self.inventory_counts.get(water_filtration_suit, 0) > 0:
            thirst_loss *= 0.7
        if self.inventory_counts.get(rebreather_type, 0) > 0:
            hunger_loss *= 0.85

        if self.hunger_timer >= 60:
            self.hunger_timer = 0
            self.player_hunger = max(0, self.player_hunger - hunger_loss)
            if self.player_hunger <= 0:
                self.player_take_damage(1)

        if self.thirst_timer >= 60:
            self.thirst_timer = 0
            self.player_thirst = max(0, self.player_thirst - thirst_loss)
            if self.player_thirst <= 0:
                self.player_take_damage(1)

        self._update_night_plankton()
        self._update_base_effects()
        self.update_notification()

    def _damage_player_or_vehicle(self, damage):
        if self.active_vehicle is not None:
            self.vehicle_take_damage(damage)
        else:
            self.player_take_damage(damage)

    def _add_special_explosion(self, x, y, kind, in_cave, radius=1.0, duration_ms=420):
        now = pygame.time.get_ticks()
        self.special_explosions.append({
            "x": float(x), "y": float(y), "kind": kind,
            "in_cave": bool(in_cave), "radius": float(radius),
            "created_at": now, "expires_at": now + int(duration_ms),
        })

    def _spawn_hostile_projectile(self, x, y, target_x, target_y, kind,
                                  speed, damage, in_cave, spread=0.0,
                                  target_animal=None, companion_owner=None):
        dx = target_x - x
        dy = target_y - y
        length = math.hypot(dx, dy)
        if length < 0.001:
            angle = random.uniform(0.0, math.tau)
        else:
            angle = math.atan2(dy, dx)
        angle += random.uniform(-spread, spread) if spread else 0.0
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        self.hostile_projectiles.append({
            "x": float(x), "y": float(y), "vx": vx, "vy": vy,
            "damage": int(damage), "ttl": 100 if kind == "needle" else 90,
            "in_cave": bool(in_cave), "kind": kind,
            "hit_radius": 0.30 if kind == "needle" else 0.43,
            # Pet projectiles are bound to fauna targets; they never collide
            # with the diver or the diver's vehicle.
            "target_animal": target_animal,
            "companion_owner": companion_owner,
        })

    def _update_crashfish_shelters(self):
        """Пробуждает Crashfish из серных растений и контролирует респавн."""
        if not self.in_cave or not self.crashfish_shelters:
            return
        now = pygame.time.get_ticks()
        player_x, player_y = self.player_x, self.player_y
        for key, shelter in self.crashfish_shelters.items():
            animal = shelter.get("animal")
            if animal is not None and (animal.hp <= 0 or animal not in self.cave_animals):
                shelter["animal"] = None
                shelter["respawn_at"] = max(
                    shelter.get("respawn_at", 0), now + 30000
                )
                animal = None

            if animal is not None or now < shelter.get("respawn_at", 0):
                continue
            sx, sy = key
            dx, dy = player_x - sx, player_y - sy
            if dx * dx + dy * dy > 4.5 * 4.5:
                continue
            home = self.get_cave_tunnel_at(sx, sy)
            if home is None:
                continue
            crashfish = Animal(float(sx), float(sy), crashfish_type, home)
            crashfish.is_shelter_crashfish = True
            crashfish.shelter_key = key
            crashfish.active = True
            crashfish.attack_cooldown = 0
            shelter["animal"] = crashfish
            self.cave_animals.append(crashfish)

    def _update_shelter_crashfish(self, animal, active_world):
        """Crashfish rushes directly at the diver instead of ordinary swimming."""
        animal.active = True
        dx = self.player_x - animal.x
        dy = self.player_y - animal.y
        distance = math.hypot(dx, dy)
        if distance < 0.001:
            animal.dx = animal.dy = 0.0
            return
        heading = math.atan2(dy, dx)
        speed = 0.17
        nx = animal.x + math.cos(heading) * speed
        ny = animal.y + math.sin(heading) * speed
        if not animal._can_swim_to(nx, ny, active_world):
            alternate = animal._find_open_heading(heading, speed, active_world)
            if alternate is None:
                animal.dx = animal.dy = 0.0
                return
            heading = alternate
            nx = animal.x + math.cos(heading) * speed
            ny = animal.y + math.sin(heading) * speed
        animal.x, animal.y = nx, ny
        animal.dx = math.cos(heading) * speed
        animal.dy = math.sin(heading) * speed
        animal.swim_heading = heading
        animal._update_rotation()

    def _update_special_creature_attacks(self):
        """Шипы Tiger Plant, очереди Морского дракона, газовые шары и взрывы."""
        now = pygame.time.get_ticks()
        player_x, player_y = self.player_x, self.player_y
        in_cave = bool(self.in_cave)

        # Tiger Plant: шипы с 5 клеток, в 1.5 раза быстрее торпеды Seamoth.
        flora_grid = self._current_flora_grid()
        center_x, center_y = int(player_x), int(player_y)
        for y in range(center_y - 5, center_y + 6):
            for x in range(center_x - 5, center_x + 6):
                flora = flora_grid.get((x, y))
                if flora is None or getattr(flora, "kind", "") != "tiger_plant":
                    continue
                dx, dy = player_x - x, player_y - y
                distance_sq = dx * dx + dy * dy
                if distance_sq < 0.15 or distance_sq > 25.0:
                    continue
                key = (in_cave, x, y)
                if now < self.plant_attack_timers.get(key, 0):
                    continue
                self._spawn_hostile_projectile(
                    x, y, player_x, player_y, "needle",
                    speed=0.66, damage=4, in_cave=in_cave,
                    spread=0.025,
                )
                self.plant_attack_timers[key] = now + 1150

        # Sea Dragon: wild dragons shoot at the diver; a tamed dragon shoots
        # at its current fauna target. Pet fireballs are target-bound and can
        # never damage the player or vehicle, even if the player crosses them.
        for animal in self.get_nearby_animals(VIEW_RADIUS + 2):
            if animal.hp <= 0 or getattr(animal, "is_shelter_crashfish", False):
                continue
            is_companion = bool(getattr(animal, "is_companion", False))
            target_animal = None
            companion_owner = None

            if animal.type.name in ("Sea Dragon Leviathan", "Dragon Leviathan"):
                if is_companion:
                    target_animal = getattr(animal, "companion_target", None)
                    current_animals = self.get_current_animals()
                    if (target_animal is None
                            or target_animal not in current_animals
                            or target_animal.hp <= 0
                            or getattr(target_animal, "is_companion", False)
                            or abs(target_animal.x - player_x) > VIEW_RADIUS
                            or abs(target_animal.y - player_y) > VIEW_RADIUS):
                        continue
                    companion_owner = animal
                    target_x, target_y = target_animal.x, target_animal.y
                    distance_sq = ((target_x - animal.x) ** 2
                                   + (target_y - animal.y) ** 2)
                else:
                    target_x, target_y = player_x, player_y
                    dx, dy = target_x - animal.x, target_y - animal.y
                    distance_sq = dx * dx + dy * dy

                if distance_sq > 8.0 * 8.0 or distance_sq < 1.1 * 1.1:
                    continue
                if not hasattr(animal, "fire_burst_remaining"):
                    animal.fire_burst_remaining = 0
                    animal.fire_burst_next_at = now + random.randint(450, 950)
                    animal.fire_next_attack_at = animal.fire_burst_next_at
                if animal.fire_burst_remaining > 0:
                    if now < animal.fire_burst_next_at:
                        continue
                    self._spawn_hostile_projectile(
                        animal.x, animal.y, target_x, target_y, "fireball",
                        speed=0.44, damage=8, in_cave=in_cave,
                        spread=0.065, target_animal=target_animal,
                        companion_owner=companion_owner,
                    )
                    animal.fire_burst_remaining -= 1
                    if animal.fire_burst_remaining > 0:
                        animal.fire_burst_next_at = now + 190
                    else:
                        animal.fire_next_attack_at = now + 2100
                elif now >= animal.fire_next_attack_at:
                    animal.fire_burst_remaining = 3
                    self._spawn_hostile_projectile(
                        animal.x, animal.y, target_x, target_y, "fireball",
                        speed=0.44, damage=8, in_cave=in_cave,
                        spread=0.065, target_animal=target_animal,
                        companion_owner=companion_owner,
                    )
                    animal.fire_burst_remaining = 2
                    animal.fire_burst_next_at = now + 190

            elif animal.type.name == "Gasopod":
                if is_companion:
                    target_animal = getattr(animal, "companion_target", None)
                    current_animals = self.get_current_animals()
                    if (target_animal is None
                            or target_animal not in current_animals
                            or target_animal.hp <= 0
                            or getattr(target_animal, "is_companion", False)
                            or abs(target_animal.x - player_x) > VIEW_RADIUS
                            or abs(target_animal.y - player_y) > VIEW_RADIUS):
                        continue
                    dx, dy = target_animal.x - animal.x, target_animal.y - animal.y
                    distance_sq = dx * dx + dy * dy
                else:
                    dx, dy = player_x - animal.x, player_y - animal.y
                    distance_sq = dx * dx + dy * dy
                if distance_sq > 3.0 * 3.0:
                    continue
                next_at = getattr(animal, "gas_pods_next_at", 0)
                if now < next_at:
                    continue
                pod_count = random.randint(3, 10)
                for _ in range(pod_count):
                    if is_companion:
                        # Aim gas pods broadly toward the hostile/prey target.
                        base_angle = math.atan2(target_animal.y - animal.y,
                                                target_animal.x - animal.x)
                        angle = base_angle + random.uniform(-0.65, 0.65)
                    else:
                        angle = random.uniform(0.0, math.tau)
                    speed = random.uniform(0.025, 0.045)
                    self.gas_pods.append({
                        "x": float(animal.x), "y": float(animal.y),
                        "origin_x": float(animal.x), "origin_y": float(animal.y),
                        "vx": math.cos(angle) * speed,
                        "vy": math.sin(angle) * speed,
                        "explode_at": now + random.randint(2000, 3000),
                        "in_cave": in_cave, "damage": 4, "radius": 1.0,
                        "phase": random.uniform(0.0, math.tau),
                        "companion_owner": animal if is_companion else None,
                    })
                animal.gas_pods_next_at = now + random.randint(6500, 8500)

        # Движение игл/огненных шаров; проверяем не только конечную точку,
        # чтобы быстрый шип не пролетал сквозь игрока между кадрами.
        projectile_survivors = []
        for projectile in self.hostile_projectiles:
            if projectile["in_cave"] != in_cave:
                projectile_survivors.append(projectile)
                continue
            old_x, old_y = projectile["x"], projectile["y"]
            new_x = old_x + projectile["vx"]
            new_y = old_y + projectile["vy"]
            projectile["ttl"] -= 1
            if projectile["ttl"] <= 0 or not (0 <= new_x < MAP_SIZE and 0 <= new_y < MAP_SIZE):
                continue
            if in_cave and not self.cave_is_passable(new_x, new_y):
                continue

            sx, sy = projectile["vx"], projectile["vy"]
            seg_len_sq = sx * sx + sy * sy
            target_animal = projectile.get("target_animal")
            if target_animal is not None:
                # Pet shot: collision is checked only against the selected
                # animal, never against the diver or the vehicle.
                if (target_animal.hp <= 0
                        or target_animal not in self.get_current_animals()
                        or getattr(target_animal, "is_companion", False)):
                    continue
                target_x, target_y = target_animal.x, target_animal.y
                if seg_len_sq > 1e-9:
                    t = max(0.0, min(1.0, ((target_x - old_x) * sx
                                          + (target_y - old_y) * sy) / seg_len_sq))
                else:
                    t = 0.0
                closest_x = old_x + sx * t
                closest_y = old_y + sy * t
                hit_dx = target_x - closest_x
                hit_dy = target_y - closest_y
                if hit_dx * hit_dx + hit_dy * hit_dy <= (projectile["hit_radius"] + 0.35) ** 2:
                    target_animal.hp -= projectile["damage"]
                    owner = projectile.get("companion_owner")
                    if target_animal.hp <= 0:
                        target_animal.hp = 0
                        if owner is not None and owner.hp > 0:
                            self._finish_companion_kill(owner, target_animal)
                        else:
                            self.remove_current_animal(target_animal)
                    if projectile["kind"] == "fireball":
                        self._add_special_explosion(new_x, new_y, "fireball", in_cave, 0.65, 260)
                    continue
            else:
                if seg_len_sq > 1e-9:
                    t = max(0.0, min(1.0, ((player_x - old_x) * sx + (player_y - old_y) * sy) / seg_len_sq))
                else:
                    t = 0.0
                closest_x = old_x + sx * t
                closest_y = old_y + sy * t
                hit_dx = player_x - closest_x
                hit_dy = player_y - closest_y
                if hit_dx * hit_dx + hit_dy * hit_dy <= projectile["hit_radius"] ** 2:
                    self._damage_player_or_vehicle(projectile["damage"])
                    if projectile["kind"] == "fireball":
                        self._add_special_explosion(new_x, new_y, "fireball", in_cave, 0.65, 260)
                    continue
            projectile["x"], projectile["y"] = new_x, new_y
            projectile_survivors.append(projectile)
        self.hostile_projectiles = projectile_survivors

        # Газовые шары дрейфуют наружу не дальше 5 клеток и взрываются через 2–3 с.
        pod_survivors = []
        for pod in self.gas_pods:
            if pod["in_cave"] != in_cave:
                pod_survivors.append(pod)
                continue
            if now >= pod["explode_at"]:
                self._add_special_explosion(pod["x"], pod["y"], "gas", in_cave, 1.0, 520)
                companion_owner = pod.get("companion_owner")
                if companion_owner is not None:
                    # A pet's gas cloud is hostile to nearby wild fauna only;
                    # it is harmless to the player, vehicles, and other pets.
                    for target in tuple(self.get_current_animals()):
                        if (target.hp <= 0 or target is companion_owner
                                or getattr(target, "is_companion", False)):
                            continue
                        dx = target.x - pod["x"]
                        dy = target.y - pod["y"]
                        if dx * dx + dy * dy <= pod["radius"] ** 2:
                            target.hp -= pod["damage"]
                            if target.hp <= 0:
                                target.hp = 0
                                if companion_owner.hp > 0:
                                    self._finish_companion_kill(companion_owner, target)
                                else:
                                    self.remove_current_animal(target)
                else:
                    dx = player_x - pod["x"]
                    dy = player_y - pod["y"]
                    if dx * dx + dy * dy <= pod["radius"] ** 2:
                        self._damage_player_or_vehicle(pod["damage"])
                continue
            nx = pod["x"] + pod["vx"]
            ny = pod["y"] + pod["vy"]
            from_origin = math.hypot(nx - pod["origin_x"], ny - pod["origin_y"])
            if from_origin > 5.0:
                ratio = 5.0 / max(0.001, from_origin)
                nx = pod["origin_x"] + (nx - pod["origin_x"]) * ratio
                ny = pod["origin_y"] + (ny - pod["origin_y"]) * ratio
                pod["vx"] = pod["vy"] = 0.0
            if not (0 <= nx < MAP_SIZE and 0 <= ny < MAP_SIZE):
                continue
            if in_cave and not self.cave_is_passable(nx, ny):
                # У стены пузырь не исчезает: он дрейфует на месте до взрыва.
                pod["vx"] = pod["vy"] = 0.0
            else:
                pod["x"], pod["y"] = nx, ny
            pod_survivors.append(pod)
        self.gas_pods = pod_survivors

        # Проверяем, не достигла ли рыба-камикадзе игрока.
        if in_cave:
            for animal in tuple(self.cave_animals):
                if not getattr(animal, "is_shelter_crashfish", False) or animal.hp <= 0:
                    continue
                dx = player_x - animal.x
                dy = player_y - animal.y
                if dx * dx + dy * dy > 0.72 * 0.72:
                    continue
                self._add_special_explosion(animal.x, animal.y, "crashfish", True, 1.25, 560)
                if dx * dx + dy * dy <= 1.25 * 1.25:
                    self._damage_player_or_vehicle(12)
                shelter = self.crashfish_shelters.get(getattr(animal, "shelter_key", None))
                if shelter is not None:
                    shelter["animal"] = None
                    shelter["respawn_at"] = now + 30000
                animal.hp = 0
                if animal in self.cave_animals:
                    self.cave_animals.remove(animal)
                self.notification = "Рыба-камикадзе взорвалась! Убегайте от серных растений."
                self.notification_timer = 75

        # Убираем просроченные визуальные эффекты, даже если слой сменился.
        self.special_explosions = [
            effect for effect in self.special_explosions
            if now < effect["expires_at"]
        ]

    def update_notification(self):
        if self.notification_timer > 0:
            self.notification_timer -= 1
            if self.notification_timer == 0:
                self.notification = ""


# ===== КОНЕЦ ЧАСТИ 1/2 =====
# Вторая часть начинается с метода render() класса Game.
# =========================================================
# ЧАСТЬ 2/2: RENDER, HUD, ИНВЕНТАРЬ, КРАФТ, ГЛАВНЫЙ ЦИКЛ
# =========================================================

    # =====================================================
    # РЕНДЕР МИРА
    # =====================================================

    def draw_dropped_item_at(self, x, y, screen_x, screen_y):
        dropped = self._current_dropped_items().get((x, y))
        if not dropped:
            return

        item = dropped[-1]
        center = (screen_x + CELL_SIZE // 2, screen_y + CELL_SIZE // 2)
        if item.image:
            image = self.get_inventory_image(item)
            rect = image.get_rect(center=center)
            self.screen.blit(image, rect)
        elif item.shape == "circle":
            pygame.draw.circle(
                self.screen, item.color, center,
                min(item.size // 2, CELL_SIZE // 2 - 3)
            )
        else:
            size = min(item.size, CELL_SIZE - 6)
            rect = pygame.Rect(0, 0, size, size)
            rect.center = center
            pygame.draw.rect(self.screen, item.color, rect)

        if len(dropped) > 1:
            count_text = self.tiny_font.render(
                str(len(dropped)), True, (255, 255, 255)
            )
            self.screen.blit(
                count_text,
                (screen_x + CELL_SIZE - count_text.get_width() - 2,
                 screen_y + CELL_SIZE - count_text.get_height() - 1)
            )

    def render(self):
        if self.state == "map":
            self.draw_map()
            self.mobile_controls.draw(self.screen)
            self.draw_damage_vignette()
            pygame.display.flip()
            return

        # Мир рисуется с исходной детализацией в буфере, площадь которого
        # зависит от масштаба. Поэтому отдаление действительно показывает
        # соседние клетки, а не пустые поля по сторонам прежнего кадра.
        world_zoom = self.camera_zoom
        self._render_view_radius = max(
            1, math.ceil((SCREEN_SIZE / (CELL_SIZE * world_zoom) - 1) / 2)
        )
        self._render_canvas_size = (self._render_view_radius * 2 + 1) * CELL_SIZE
        display_surface = pygame.display.get_surface()
        if abs(world_zoom - 1.0) < 1e-8:
            self.screen = display_surface
        else:
            need_size = (self._render_canvas_size, self._render_canvas_size)
            if (self._world_render_surface is None or
                    self._world_render_surface.get_size() != need_size):
                self._world_render_surface = pygame.Surface(need_size).convert()
            self.screen = self._world_render_surface

        if self.lighting_overlay.get_size() != self.screen.get_size():
            self.lighting_overlay = pygame.Surface(
                self.screen.get_size(), pygame.SRCALPHA
            ).convert_alpha()

        self.screen.fill((0, 0, 0))

        camera_x, camera_y = self.get_render_camera_origin()
        start_x = math.floor(camera_x)
        start_y = math.floor(camera_y)
        end_x = math.ceil(camera_x + self._render_view_radius * 2)
        end_y = math.ceil(camera_y + self._render_view_radius * 2)

        for y in range(start_y, end_y + 1):
            if not (0 <= y < MAP_SIZE):
                continue

            screen_y = int(round((y - camera_y) * CELL_SIZE))

            for x in range(start_x, end_x + 1):
                if not (0 <= x < MAP_SIZE):
                    continue

                screen_x = int(round((x - camera_x) * CELL_SIZE))

                if self.in_cave:
                    tunnel = self.get_cave_tunnel_at(x, y)
                    self.draw_cave_cell(x, y, screen_x, screen_y, tunnel)

                    flora = self.cave_flora_grid.get((x, y))
                    if flora is not None and flora.image is not None:
                        flora_rect = flora.image.get_rect(
                            center=(
                                screen_x + CELL_SIZE // 2,
                                screen_y + CELL_SIZE // 2
                            )
                        )
                        self.screen.blit(flora.image, flora_rect)

                    obj = self.cave_object_grid.get((x, y))
                    if obj is not None and not getattr(obj, "is_buildable", False):
                        center_x = screen_x + CELL_SIZE // 2
                        center_y = screen_y + CELL_SIZE // 2

                        if obj.image:
                            rect = obj.image.get_rect(
                                center=(center_x, center_y)
                            )
                            self.screen.blit(obj.image, rect)
                        elif obj.shape == "circle":
                            pygame.draw.circle(
                                self.screen, obj.color,
                                (center_x, center_y),
                                obj.size // 2
                            )
                        else:
                            rect = pygame.Rect(
                                0, 0, obj.size, obj.size
                            )
                            rect.center = (center_x, center_y)
                            pygame.draw.rect(
                                self.screen, obj.color, rect
                            )

                    exit_data = self.get_cave_exit_at(x, y)
                    if exit_data is not None:
                        pygame.draw.rect(
                            self.screen, (16, 74, 100),
                            (screen_x, screen_y,
                             CELL_SIZE, CELL_SIZE)
                        )
                        pygame.draw.rect(
                            self.screen, (175, 230, 255),
                            (screen_x, screen_y,
                             CELL_SIZE, CELL_SIZE),
                            2
                        )

                    self.draw_dropped_item_at(
                        x, y, screen_x, screen_y
                    )
                    if (x, y) in self.scanner_highlight_cells:
                        pygame.draw.rect(
                            self.screen, (70, 250, 170),
                            (screen_x + 1, screen_y + 1, CELL_SIZE - 2, CELL_SIZE - 2), 2
                        )
                    continue

                biome = self.world.get_biome_at(x, y)
                color = (
                    biome.color if biome is not None
                    else (128, 128, 128)
                )

                if self.is_aurora_biome(biome):
                    # Аврора (кроме реактора) рисуется в стиле капсулы.
                    self.draw_aurora_cell(
                        x, y, screen_x, screen_y, biome
                    )
                else:
                    pygame.draw.rect(
                        self.screen, color,
                        (screen_x, screen_y, CELL_SIZE, CELL_SIZE)
                    )

                    if biome is None:
                        center = (
                            screen_x + CELL_SIZE // 2,
                            screen_y + CELL_SIZE // 2
                        )
                        pygame.draw.line(
                            self.screen, (40, 40, 40),
                            (center[0] - 6, center[1] - 6),
                            (center[0] + 6, center[1] + 6), 2
                        )
                        pygame.draw.line(
                            self.screen, (40, 40, 40),
                            (center[0] + 6, center[1] - 6),
                            (center[0] - 6, center[1] + 6), 2
                        )
                    else:
                        # Рисуем декоративный слой дна: оттенки, камни,
                        # кораллы, обрастания и морские звёзды.
                        self.draw_surface_seabed_cell(
                            x, y, screen_x, screen_y, biome
                        )

                    self.draw_start_capsule_cell(
                        x, y, screen_x, screen_y
                    )

                flora = self.world.flora_grid.get((x, y))
                if flora is not None and flora.image is not None:
                    flora_rect = flora.image.get_rect(
                        center=(
                            screen_x + CELL_SIZE // 2,
                            screen_y + CELL_SIZE // 2
                        )
                    )
                    self.screen.blit(flora.image, flora_rect)

                obj = self.world.object_grid.get((x, y))

                if obj is not None and not getattr(obj, "is_buildable", False):
                    center_x = screen_x + CELL_SIZE // 2
                    center_y = screen_y + CELL_SIZE // 2

                    if obj.image:
                        rect = obj.image.get_rect(
                            center=(center_x, center_y)
                        )
                        self.screen.blit(obj.image, rect)
                    elif obj.shape == "circle":
                        pygame.draw.circle(
                            self.screen, obj.color,
                            (center_x, center_y),
                            obj.size // 2
                        )
                    else:
                        rect = pygame.Rect(
                            0, 0, obj.size, obj.size
                        )
                        rect.center = (center_x, center_y)
                        pygame.draw.rect(
                            self.screen, obj.color, rect
                        )

                entrance = self.get_surface_cave_entrance_at(x, y)
                if entrance is not None:
                    pygame.draw.rect(
                        self.screen, (8, 8, 12),
                        (screen_x, screen_y,
                         CELL_SIZE, CELL_SIZE)
                    )
                    pygame.draw.rect(
                        self.screen, (40, 45, 55),
                        (screen_x, screen_y,
                         CELL_SIZE, CELL_SIZE),
                        1
                    )

                self.draw_dropped_item_at(
                    x, y, screen_x, screen_y
                )
                if (x, y) in self.scanner_highlight_cells:
                    pygame.draw.rect(
                        self.screen, (70, 250, 170),
                        (screen_x + 1, screen_y + 1, CELL_SIZE - 2, CELL_SIZE - 2), 2
                    )

        foreground_objects = self._get_current_object_grid()
        foreground_planters = self._planter_types()
        # Передний слой: корпус капсулы и все постройки рисуются ПОСЛЕ
        # водорослей/минералов, даже если спрайт растения пересекает клетку.
        # Игрок и подлодка отрисуются ещё позже и останутся поверх всего.
        for y in range(start_y, end_y + 1):
            if not (0 <= y < MAP_SIZE):
                continue
            for x in range(start_x, end_x + 1):
                if not (0 <= x < MAP_SIZE):
                    continue
                screen_x = int(round((x - camera_x) * CELL_SIZE))
                screen_y = int(round((y - camera_y) * CELL_SIZE))
                if not self.in_cave and self.is_inside_start_capsule(x, y):
                    self.draw_start_capsule_cell(x, y, screen_x, screen_y)
                obj = foreground_objects.get((x, y))
                if obj is None or not getattr(obj, "is_buildable", False):
                    continue
                center = (screen_x + CELL_SIZE // 2,
                          screen_y + CELL_SIZE // 2)
                if obj.image is not None:
                    self.screen.blit(obj.image, obj.image.get_rect(center=center))
                elif obj.shape == "circle":
                    pygame.draw.circle(self.screen, obj.color, center,
                                       max(1, obj.size // 2))
                else:
                    pygame.draw.rect(self.screen, obj.color,
                                     pygame.Rect(0, 0, obj.size, obj.size).move(
                                         center[0] - obj.size // 2,
                                         center[1] - obj.size // 2))
                if obj in foreground_planters:
                    self._draw_planted_flora_at(x, y, screen_x, screen_y)

        player_x = self.player_x
        player_y = self.player_y

        self.draw_vehicle_wrecks(camera_x, camera_y)
        self.draw_vehicle_torpedoes(camera_x, camera_y)

        for animal in self.get_nearby_animals(self._render_view_radius):
            if animal.hp <= 0:
                continue

            screen_x = int(
                (animal.x - camera_x) * CELL_SIZE + CELL_SIZE // 2
            )
            screen_y = int(
                (animal.y - camera_y) * CELL_SIZE + CELL_SIZE // 2
            )

            animal_type = animal.type

            if animal_type.image:
                image = animal.rotated_image or animal_type.image
                rect = image.get_rect(center=(screen_x, screen_y))
                self.screen.blit(image, rect)
            elif animal_type.shape == "circle":
                pygame.draw.circle(
                    self.screen, animal_type.color,
                    (screen_x, screen_y),
                    animal_type.size // 2
                )
            else:
                rect = pygame.Rect(
                    0, 0, animal_type.size, animal_type.size
                )
                rect.center = (screen_x, screen_y)
                pygame.draw.rect(
                    self.screen, animal_type.color, rect
                )

            if getattr(animal, "is_companion", False):
                marker_radius = max(9, min(28, animal_type.size // 2 + 6))
                pygame.draw.circle(
                    self.screen, (80, 245, 225),
                    (screen_x, screen_y), marker_radius, 2
                )

            if 0 < animal.hp < animal.max_hp:
                bar_width = 20
                bar_height = 4
                bar_x = screen_x - bar_width // 2
                bar_y = (screen_y - animal_type.size // 2 - 8)

                pygame.draw.rect(
                    self.screen, (120, 0, 0),
                    (bar_x, bar_y, bar_width, bar_height)
                )

                fill = int(
                    bar_width * animal.hp / animal.max_hp
                )
                pygame.draw.rect(
                    self.screen, (0, 220, 0),
                    (bar_x, bar_y, fill, bar_height)
                )

        self._draw_hostile_attacks(camera_x, camera_y)

        player_screen_x = self._render_view_radius * CELL_SIZE + CELL_SIZE // 2
        player_screen_y = self._render_view_radius * CELL_SIZE + CELL_SIZE // 2

        if self.active_vehicle is not None:
            vehicle_image = self.get_vehicle_rotated(
                self.active_vehicle, self.player_angle
            )
            if vehicle_image is not None:
                vehicle_rect = vehicle_image.get_rect(
                    center=(player_screen_x, player_screen_y)
                )
                self.screen.blit(vehicle_image, vehicle_rect)
        else:
            if self.equipped_weapon is not None:
                weapon_image = self.get_weapon_rotated(
                    self.equipped_weapon, self.player_angle
                )

                if weapon_image:
                    radians = math.radians(self.player_angle)
                    offset = CELL_SIZE * 0.55

                    weapon_x = (player_screen_x
                                + math.cos(radians) * offset)
                    weapon_y = (player_screen_y
                                + math.sin(radians) * offset)

                    rect = weapon_image.get_rect(
                        center=(int(weapon_x), int(weapon_y))
                    )
                    self.screen.blit(weapon_image, rect)

            diver_image = self.get_diver_rotated(self.player_angle)
            diver_rect = diver_image.get_rect(
                center=(player_screen_x, player_screen_y)
            )
            self.screen.blit(diver_image, diver_rect)

            pygame.draw.circle(
                self.screen, (255, 255, 255),
                (player_screen_x, player_screen_y),
                CELL_SIZE // 2 + 2, 1
            )

        # -------------------------------------------------
        # ДЕНЬ / НОЧЬ (поверх мира, но под HUD)
        # -------------------------------------------------

        self.draw_day_night_overlay()
        self.draw_light_emitters(camera_x, camera_y)
        # Живое свечение поверх абсолютной темноты, но ниже игрового HUD.
        self.draw_bioluminescence(camera_x, camera_y)

        # -------------------------------------------------
        # Перенос виртуальной камеры на настоящий экран (HUD отдельно).
        # -------------------------------------------------
        if self.screen is not display_surface:
            target_px = max(1, round(self._render_canvas_size * world_zoom))
            scaled_world = pygame.transform.smoothscale(
                self.screen, (target_px, target_px)
            )
            self.screen = display_surface
            display_surface.fill((0, 0, 0))
            screen_offset = (SCREEN_SIZE - target_px) // 2
            self.screen.blit(scaled_world, (screen_offset, screen_offset))

        if world_zoom > ZOOM_DETAIL_START and self.screen is display_surface:
            # Реальное новое разрешение после масштабирования буфера.
            self._draw_zoom_details(world_zoom, target_px, screen_offset)
        self.draw_night_plankton()
        self._draw_blue_edge_haze()
        self._draw_night_edge_vignette()

        # -------------------------------------------------
        # HUD: не увеличивается и не уменьшается вместе с миром.
        # -------------------------------------------------

        self.draw_hud()

        if self.state == "inventory":
            self.draw_inventory()
        elif self.state == "crafting":
            self.draw_crafting()
        elif self.state == "pets":
            self.draw_pet_list()
        elif self.state == "scanner":
            self.draw_scanner_view()
        elif self.state == "planting":
            self.draw_planting_menu()

        if self.settings_open:
            self.draw_settings_panel()

        if self.notification_timer > 0 and self.notification and not self.settings_open:
            text = self.large_font.render(
                self.notification, True, (255, 255, 0)
            )
            rect = text.get_rect(
                center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2 + 100)
            )
            pygame.draw.rect(
                self.screen, (0, 0, 0), rect.inflate(20, 10)
            )
            self.screen.blit(text, rect)

        if self.state == "playing":
            mouse_x, mouse_y = (self.mobile_controls.aim_pos
                                 if self.mobile_controls.enabled
                                 and self.mobile_controls.aim_pos is not None
                                 else pygame.mouse.get_pos())

            pygame.draw.line(
                self.screen, (255, 255, 255),
                (mouse_x - 8, mouse_y),
                (mouse_x + 8, mouse_y), 2
            )
            pygame.draw.line(
                self.screen, (255, 255, 255),
                (mouse_x, mouse_y - 8),
                (mouse_x, mouse_y + 8), 2
            )
            pygame.draw.circle(
                self.screen, (255, 255, 255),
                (mouse_x, mouse_y), 3, 1
            )

        self.mobile_controls.draw(self.screen)
        self.draw_damage_vignette()
        pygame.display.flip()



    def _create_damage_vignette_surface(self):
        """Prebuild a red edge gradient whose centre stays fully transparent."""
        vignette = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA)
        fade_width = max(90, int(SCREEN_SIZE * 0.34))

        for inset in range(fade_width):
            t = 1.0 - inset / max(1, fade_width - 1)
            # Quadratic falloff: strong at the very edge, soft toward the centre.
            alpha = int(235 * (t ** 2.15))
            if alpha <= 0:
                continue
            w = SCREEN_SIZE - inset * 2
            h = SCREEN_SIZE - inset * 2
            if w <= 0 or h <= 0:
                break
            pygame.draw.rect(
                vignette,
                (235, 8, 8, alpha),
                pygame.Rect(inset, inset, w, h),
                1,
            )

        return vignette.convert_alpha()

    def draw_damage_vignette(self):
        """Tint screen edges red according to lost HP, with a brief boost on each hit."""
        if self.max_player_hp <= 0:
            return

        missing_ratio = 1.0 - max(0.0, min(1.0, self.player_hp / self.max_player_hp))
        if missing_ratio <= 0.0 and self.damage_vignette_flash <= 0:
            return

        if self.damage_vignette_surface is None:
            self.damage_vignette_surface = self._create_damage_vignette_surface()

        persistent_alpha = 0
        if missing_ratio > 0.0:
            persistent_alpha = int(38 + 182 * (missing_ratio ** 0.78))

        flash_alpha = 0
        if self.damage_vignette_flash > 0:
            flash_t = self.damage_vignette_flash / 18.0
            flash_alpha = int(255 * (flash_t ** 0.55))
            self.damage_vignette_flash -= 1

        alpha = max(persistent_alpha, flash_alpha)
        self.damage_vignette_surface.set_alpha(max(0, min(255, alpha)))
        self.screen.blit(self.damage_vignette_surface, (0, 0))
        self.damage_vignette_surface.set_alpha(None)


    # =====================================================
    # ПАНЕЛЬ НАСТРОЕК (N)
    # =====================================================

    def draw_settings_panel(self):
        """Модальная панель графических настроек с кликабельными пунктами."""
        overlay = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        self.screen.blit(overlay, (0, 0))

        panel = pygame.Rect((SCREEN_SIZE - 520) // 2,
                            (SCREEN_SIZE - 400) // 2, 520, 400)
        pygame.draw.rect(self.screen, (13, 32, 47), panel, border_radius=12)
        pygame.draw.rect(self.screen, (74, 174, 205), panel, 2, border_radius=12)

        title = self.large_font.render("Настройки", True, (225, 247, 255))
        self.screen.blit(title, title.get_rect(center=(panel.centerx, panel.y + 36)))
        subtitle = self.small_font.render("N — закрыть панель", True, (155, 190, 205))
        self.screen.blit(subtitle, subtitle.get_rect(center=(panel.centerx, panel.y + 62)))

        options = [
            ("Отключить планктон", not self.setting_plankton_enabled),
            ("Отключить мелкие объекты на дне", not self.setting_seabed_details_enabled),
            ("Отключить затемнение воды", not self.setting_water_darkening_enabled),
            ("Отключить музыку", not self.setting_music_enabled),
            ("Отключить звуковые эффекты", not self.setting_effects_enabled),
        ]
        for index, (label, disabled) in enumerate(options):
            rect = pygame.Rect(panel.x + 24, panel.y + 84 + index * 58, 472, 48)
            pygame.draw.rect(self.screen, (25, 55, 72), rect, border_radius=7)
            pygame.draw.rect(self.screen, (69, 112, 132), rect, 1, border_radius=7)
            check = pygame.Rect(rect.x + 14, rect.y + 12, 24, 24)
            pygame.draw.rect(self.screen, (8, 20, 29), check, border_radius=4)
            pygame.draw.rect(self.screen, (124, 205, 221), check, 2, border_radius=4)
            if disabled:
                pygame.draw.line(self.screen, (255, 190, 105),
                                 (check.x + 5, check.y + 12),
                                 (check.x + 10, check.y + 18), 3)
                pygame.draw.line(self.screen, (255, 190, 105),
                                 (check.x + 10, check.y + 18),
                                 (check.x + 20, check.y + 5), 3)
            text = self.font.render(label, True, (230, 241, 247))
            self.screen.blit(text, text.get_rect(midleft=(rect.x + 52, rect.centery)))

        hint = self.tiny_font.render("Изменения применяются сразу и сохраняются при закрытии меню.",
                                     True, (153, 183, 195))
        self.screen.blit(hint, hint.get_rect(center=(panel.centerx, panel.bottom - 16)))

    # =====================================================
    # HUD
    # =====================================================

    def draw_hud(self):
        hp_text = self.font.render(
            f"HP: {self.player_hp}/{self.max_player_hp}",
            True, (255, 255, 255)
        )
        self.screen.blit(hp_text, (10, 10))

        bar_width = 100
        bar_height = 12
        bar_x = 10

        pygame.draw.rect(
            self.screen, (100, 0, 0),
            (bar_x, 35, bar_width, bar_height)
        )
        fill = int(
            bar_width * self.player_hp / self.max_player_hp
        )
        pygame.draw.rect(
            self.screen, (0, 200, 0),
            (bar_x, 35, fill, bar_height)
        )

        hunger_text = self.font.render(
            f"Голод: {int(self.player_hunger)}",
            True, (255, 255, 255)
        )
        self.screen.blit(hunger_text, (10, 55))

        pygame.draw.rect(
            self.screen, (50, 50, 50),
            (bar_x, 75, bar_width, bar_height)
        )
        fill = int(
            bar_width * self.player_hunger / self.max_hunger
        )
        pygame.draw.rect(
            self.screen, (0, 255, 0),
            (bar_x, 75, fill, bar_height)
        )

        thirst_text = self.font.render(
            f"Жажда: {int(self.player_thirst)}",
            True, (255, 255, 255)
        )
        self.screen.blit(thirst_text, (10, 95))

        pygame.draw.rect(
            self.screen, (50, 50, 50),
            (bar_x, 115, bar_width, bar_height)
        )
        fill = int(
            bar_width * self.player_thirst / self.max_thirst
        )
        pygame.draw.rect(
            self.screen, (0, 100, 255),
            (bar_x, 115, fill, bar_height)
        )

        if self.active_vehicle is not None:
            vehicle_hp = self.vehicle_hp.get(self.active_vehicle, 0)
            vehicle_max = self.vehicle_max_hp[self.active_vehicle]
            text = self.font.render(
                f"{self.active_vehicle.name} HP: {vehicle_hp}/{vehicle_max} "
                f"| Фары L: {'ВКЛ' if self.vehicle_headlights_on else 'ВЫКЛ'}",
                True, (120, 225, 245)
            )
            self.screen.blit(text, (10, 140))
            pygame.draw.rect(self.screen, (75, 30, 30), (10, 165, 130, 10))
            vehicle_fill = int(130 * vehicle_hp / max(1, vehicle_max))
            pygame.draw.rect(self.screen, (45, 190, 215), (10, 165, vehicle_fill, 10))
        elif self.equipped_weapon is not None:
            text = self.font.render(
                f"Оружие: {self.equipped_weapon.name}",
                True, (230, 220, 80)
            )
            self.screen.blit(text, (10, 140))

            stats = self.small_font.render(
                f"Урон: {self.equipped_weapon.damage} "
                f"| Дальность: {self.equipped_weapon.weapon_range}",
                True, (210, 210, 210)
            )
            self.screen.blit(stats, (10, 165))

        layer_text = self.small_font.render(
            "Слой: пещера" if self.in_cave else "Слой: поверхность",
            True, (180, 220, 240)
        )
        self.screen.blit(layer_text, (10, 190))

        zoom_text = self.tiny_font.render(
            f"Камера: {self.camera_zoom:.2f}x  |  Колесо мыши: +/-",
            True, (160, 220, 245)
        )
        self.screen.blit(zoom_text, (SCREEN_SIZE - zoom_text.get_width() - 10, 35))

        time_text = self.small_font.render(
            self.get_time_string(), True, (235, 235, 250)
        )
        time_rect = time_text.get_rect()
        time_rect.topright = (SCREEN_SIZE - 10, 10)
        self.screen.blit(time_text, time_rect)

        statuses = []
        if self.flashlight_on:
            statuses.append("Фонарик")
        if self.seaglide_on:
            statuses.append("Глайдер")
        if self.active_flare_timer > 0:
            statuses.append("Ракета")
        if self.damage_resist_timer > 0:
            statuses.append("Защита")
        if self.speed_boost_timer > 0:
            statuses.append("Рывок")
        if statuses:
            status_text = self.small_font.render(
                "Активно: " + ", ".join(statuses),
                True, (255, 220, 120)
            )
            self.screen.blit(status_text, (10, 215))

        hint = self.small_font.render(
            "C — вход/всплыть | M — карта | R — инвентарь | F — транспорт | "
            "T — питомцы | I — крафт | U — использовать | ЛКМ — торпеда в судне | ПКМ — сканер/посадка",
            True, (210, 210, 210)
        )
        self.screen.blit(hint, (10, SCREEN_SIZE - 25))

    # =====================================================
    # СПИСОК ПИТОМЦЕВ
    # =====================================================

    def draw_pet_list(self):
        self.screen.blit(self.inventory_overlay, (0, 0))

        pets = self._get_all_companions()
        total = len(pets)
        max_page = max(0, (total - 1) // self.pets_per_page)
        self.pet_list_page = min(self.pet_list_page, max_page)
        if self.selected_pet not in pets:
            self.selected_pet = None

        title = self.large_font.render(
            f"Питомцы: {total}", True, (120, 245, 225)
        )
        self.screen.blit(
            title, title.get_rect(center=(SCREEN_SIZE // 2, 47))
        )
        for i, instruction in enumerate((
            "1–9 — выбрать | E — вернуть в инвентарь | U — лечить (+35 HP/аптечка)",
            "T или ESC — закрыть | ←/→ — страницы",
        )):
            subtitle = self.small_font.render(instruction, True, (215, 225, 230))
            self.screen.blit(subtitle, subtitle.get_rect(
                center=(SCREEN_SIZE // 2, 77 + i * 24)))

        if not pets:
            empty = self.small_font.render(
                "Нет питомцев. Выберите существо в инвентаре и нажмите H.",
                True, (225, 225, 225)
            )
            self.screen.blit(
                empty, empty.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
            )
            return

        start = self.pet_list_page * self.pets_per_page
        page_pets = pets[start:start + self.pets_per_page]
        y = 130
        row_height = 47

        for number, pet in enumerate(page_pets, start=1):
            selected = pet is self.selected_pet
            row_rect = pygame.Rect(14, y - 3, SCREEN_SIZE - 28, row_height - 3)
            pygame.draw.rect(
                self.screen, (24, 85, 76) if selected else (14, 35, 43),
                row_rect, border_radius=6)
            if selected:
                pygame.draw.rect(self.screen, (95, 255, 199),
                                 row_rect, width=2, border_radius=6)

            layer = "пещера" if pet in self.cave_animals else "поверхность"
            visible_here = (
                pet in self.get_current_animals()
                and abs(pet.x - self.player_x) <= VIEW_RADIUS
                and abs(pet.y - self.player_y) <= VIEW_RADIUS
            )
            state_text = getattr(pet, "companion_state", "следует за игроком")
            if not visible_here and pet in self.get_current_animals():
                state_text = "ждёт вне видимости"
            follow_distance = self._companion_follow_distance(pet)
            hp_text = f"HP {max(0, int(pet.hp))}/{int(pet.max_hp)}"

            text_color = (170, 255, 204) if selected else (235, 240, 245)
            line_1 = self.small_font.render(
                f"{number}. {pet.type.name}  |  {hp_text}", True, text_color
            )
            line_2 = self.tiny_font.render(
                f"{layer}  |  дистанция {follow_distance:.1f}  |  {state_text}",
                True, (177, 207, 216)
            )
            self.screen.blit(line_1, (24, y))
            self.screen.blit(line_2, (42, y + 24))
            y += row_height

        page_text = self.small_font.render(
            f"Страница {self.pet_list_page + 1}/{max_page + 1}",
            True, (180, 210, 220)
        )
        self.screen.blit(
            page_text,
            page_text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE - 33))
        )

    # =====================================================
    # ИНВЕНТАРЬ
    # =====================================================

    def draw_inventory(self):
        self.screen.blit(self.inventory_overlay, (0, 0))

        total_width = (
            INVENTORY_COLS * (SLOT_SIZE + SLOT_MARGIN)
            - SLOT_MARGIN
        )
        total_height = (
            INVENTORY_ROWS * (SLOT_SIZE + SLOT_MARGIN)
            - SLOT_MARGIN
        )

        start_x = (SCREEN_SIZE - total_width) // 2
        start_y = (SCREEN_SIZE - total_height) // 2

        title = self.font.render(
            "Инвентарь (R или ESC — закрыть)",
            True, (255, 255, 255)
        )
        title_rect = title.get_rect(
            center=(SCREEN_SIZE // 2, start_y - 30)
        )
        self.screen.blit(title, title_rect)

        used = sum(1 for slot in self.inventory if slot is not None)
        counter = self.font.render(
            f"{used} / {INVENTORY_SIZE}", True, (200, 200, 200)
        )
        counter_rect = counter.get_rect(
            center=(SCREEN_SIZE // 2,
                    start_y + total_height + 20)
        )
        self.screen.blit(counter, counter_rect)

        if self.active_slot_index != -1:
            hint = self.small_font.render(
                "U — использовать | Q — экипировать | B — построить | F — сесть в транспорт",
                True, (210, 210, 210)
            )
            hint_rect = hint.get_rect(
                center=(SCREEN_SIZE // 2,
                        start_y + total_height + 45)
            )
            self.screen.blit(hint, hint_rect)

            companion_hint = self.small_font.render(
                "P — выбросить | H — выпустить существо как спутника",
                True, (120, 235, 225)
            )
            companion_hint_rect = companion_hint.get_rect(
                center=(SCREEN_SIZE // 2,
                        start_y + total_height + 68)
            )
            self.screen.blit(companion_hint, companion_hint_rect)

            eat_hint = self.small_font.render(
                "ПКМ по съедобной рыбе — съесть прямо в инвентаре",
                True, (255, 215, 125)
            )
            eat_hint_rect = eat_hint.get_rect(
                center=(SCREEN_SIZE // 2,
                        start_y + total_height + 91)
            )
            self.screen.blit(eat_hint, eat_hint_rect)

        for row in range(INVENTORY_ROWS):
            for col in range(INVENTORY_COLS):
                index = row * INVENTORY_COLS + col

                x = start_x + col * (SLOT_SIZE + SLOT_MARGIN)
                y = start_y + row * (SLOT_SIZE + SLOT_MARGIN)

                pygame.draw.rect(
                    self.screen, (55, 55, 65),
                    (x, y, SLOT_SIZE, SLOT_SIZE)
                )

                border_color = (
                    (0, 255, 0) if index == self.active_slot_index
                    else (110, 110, 120)
                )
                pygame.draw.rect(
                    self.screen, border_color,
                    (x, y, SLOT_SIZE, SLOT_SIZE), 3
                )

                item = self.inventory[index]
                if item is None:
                    continue

                center = (x + SLOT_SIZE // 2, y + SLOT_SIZE // 2)

                if item.image:
                    image = self.get_inventory_image(item)
                    rect = image.get_rect(center=center)
                    self.screen.blit(image, rect)
                elif item.shape == "circle":
                    pygame.draw.circle(
                        self.screen, item.color, center,
                        min(item.size // 2, SLOT_SIZE // 2 - 5)
                    )
                else:
                    size = min(item.size, SLOT_SIZE - 8)
                    rect = pygame.Rect(0, 0, size, size)
                    rect.center = center
                    pygame.draw.rect(
                        self.screen, item.color, rect
                    )

                if item.is_weapon:
                    weapon_mark = self.small_font.render(
                        "W", True, (255, 230, 0)
                    )
                    self.screen.blit(weapon_mark, (x + 3, y + 2))

    # =====================================================
    # КРАФТ
    # =====================================================

    def draw_crafting(self):
        self.screen.blit(self.crafting_overlay, (0, 0))

        title = self.large_font.render(
            "Крафт", True, (255, 255, 255)
        )
        self.screen.blit(
            title, title.get_rect(center=(SCREEN_SIZE // 2, 30))
        )

        location_name = self.get_crafting_location_name()
        location_text = self.tiny_font.render(
            f"Зона крафта: {location_name or 'недоступна'}",
            True, (120, 230, 245)
        )
        self.screen.blit(
            location_text,
            location_text.get_rect(center=(SCREEN_SIZE // 2, 55))
        )

        station_recipes = self.get_current_station_recipes()
        self.max_craft_page = max(
            0, (len(station_recipes) - 1) // self.recipes_per_page
        )
        self.craft_page = min(
            self.craft_page, self.max_craft_page
        )

        start = self.craft_page * self.recipes_per_page
        end = min(start + self.recipes_per_page, len(station_recipes))
        current_recipes = station_recipes[start:end]

        y = 82
        for index, recipe in enumerate(current_recipes):
            can_craft = recipe.can_craft(self.inventory_counts)

            color = (
                (80, 255, 100) if can_craft
                else (255, 100, 100)
            )

            output_suffix = (
                f" x{recipe.result_count}" if recipe.result_count > 1 else ""
            )
            title_text = self.small_font.render(
                f"{index + 1}. {recipe.name}{output_suffix}", True, color
            )
            self.screen.blit(title_text, (40, y))

            ingredients = ", ".join(
                f"{item.name} x{count}"
                for (item, count) in recipe.ingredients.items()
            )
            meta = f"[{recipe.station} / {recipe.category}] " + ingredients

            ingredient_text = self.tiny_font.render(
                meta, True, (210, 210, 210)
            )
            self.screen.blit(ingredient_text, (55, y + 21))

            y += 52

        page_text = self.small_font.render(
            f"Страница {self.craft_page + 1}/"
            f"{self.max_craft_page + 1} | ← → | TAB: станция",
            True, (220, 220, 220)
        )
        self.screen.blit(
            page_text,
            page_text.get_rect(
                center=(SCREEN_SIZE // 2, SCREEN_SIZE - 30)
            )
        )

    # =====================================================
    # ГЛАВНЫЙ ЦИКЛ
    # =====================================================

    async def run(self):
        """Standalone async game loop (the entrypoint below handles the menu)."""
        while self.running and self.state != "dead":
            self.handle_events()
            if not self.running:
                break
            self.update()
            if self.state == "dead":
                break
            self.render()
            self.clock.tick(60)
            await asyncio.sleep(0)


# =========================================================
# ЭКРАНЫ МЕНЮ / ИНФОРМАЦИИ / СМЕРТИ
# Рисунки существ берутся ИЗ САМОГО ИГРОВОГО КОДА.
# =========================================================

class Frontend:
    """Экранные сцены с анимированными существами в размерах игрового мира.

    У всех изображений используется тот же генератор спрайтов, что и у
    животных в мире, и ровно те же fish_length / fish_width. Спрайты не
    растягиваются по осям независимо друг от друга.
    """

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.title_font = game_font(43, bold=True)
        self.heading_font = game_font(29, bold=True)
        self.font = game_font(20)
        self.small_font = game_font(15)
        self.tiny_font = game_font(13)
        self.background = self._background()
        self.animals = []
        self.seconds = 0.0
        self.rng = random.Random(4546)
        self._load_original_creature_drawings()
        self.buttons = {
            "start": pygame.Rect(168, 333, 294, 54),
            "info": pygame.Rect(168, 400, 294, 54),
            "exit": pygame.Rect(168, 467, 294, 54),
            "back": pygame.Rect(168, 533, 294, 52),
            "again": pygame.Rect(168, 362, 294, 54),
            "main": pygame.Rect(168, 429, 294, 52),
        }
        self.particles = []
        for _ in range(75):
            self.particles.append((self.rng.randint(7, SCREEN_SIZE - 7),
                                   self.rng.randint(14, SCREEN_SIZE - 14),
                                   self.rng.randint(1, 3),
                                   self.rng.random() * math.tau))

    @staticmethod
    def _background():
        surf = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE)).convert()
        for y in range(SCREEN_SIZE):
            t = y / max(1, SCREEN_SIZE - 1)
            color = (int(4 + 9*t), int(22 + 17*t), int(44 + 13*t))
            pygame.draw.line(surf, color, (0, y), (SCREEN_SIZE, y))
        floor = [(0, SCREEN_SIZE), (0, 543), (66, 523), (135, 555),
                 (222, 534), (320, 561), (427, 526), (530, 550),
                 (630, 520), (630, 630)]
        pygame.draw.polygon(surf, (10, 44, 52), floor)
        rng = random.Random(2026)
        for i in range(28):
            x = i * 24 + rng.randint(-11, 11)
            h = rng.randint(45, 137)
            top = 598 - h
            pygame.draw.lines(surf, (15, 70, 67), False,
                              [(x, 605), (x - 11, (top + 605) // 2),
                               (x + 7, top)], 3)
            pygame.draw.ellipse(surf, (23, 94, 69), (x - 9, top + 8, 21, 8))
        return surf

    def _load_original_creature_drawings(self):
        # Длины и ширины ниже В ТОЧНОСТИ взяты из AnimalType в init_assets().
        # Большие хищники не уравниваются по размеру с маленькими рыбами.
        # Порядок: вид, тип спрайта, длина, ширина, старт X, Y, направление,
        # скорость в пикселях/секунду, величина вертикального покачивания.
        specs = [
            ("Морской дракон", "sea_dragon", 300, 35, 475, 203, -1, 19, 7),
            ("Сталкер", "stalker", 118, 24, 94, 291, 1, 36, 5),
            ("Кальмарокраб", "crabsquid", 118, 52, 552, 242, -1, 18, 6),
            ("Костяная акула", "boneshark", 120, 31, 245, 577, 1, 31, 6),
            ("Газобрюх", "gasopod", 92, 40, 550, 578, -1, 24, 5),
            ("Пискун", "peeper", 38, 12, 75, 556, 1, 61, 3),
            ("Бумеранг", "boomerang", 37, 12, 185, 601, 1, 56, 4),
            ("Лопаточник", "spadefish", 29, 11, 62, 224, 1, 52, 3),
            ("Рыба-пузырь", "bladderfish", 34, 13, 429, 548, -1, 48, 4),
        ]
        for index, (name, kind, length, width, x, y, direction,
                    speed, bob) in enumerate(specs):
            try:
                image = generate_subnautica_creature_sprite(kind, length, width)
                trimmed = image.get_bounding_rect(min_alpha=1)
                if not trimmed.width or not trimmed.height:
                    continue
                # Только удаление прозрачных полей: никакого повторного
                # масштабирования, искажающего размеры или пропорции.
                sprite = image.subsurface(trimmed).copy()
                self.animals.append({
                    "name": name, "sprite": sprite,
                    "reverse": pygame.transform.flip(sprite, True, False),
                    "x": float(x), "y": float(y),
                    "direction": direction, "speed": float(speed),
                    "bob": bob, "phase": index * 1.47,
                })
            except Exception as exc:
                print("Menu creature error:", name, repr(exc))

    def text_center(self, string, y, font, color=(231, 242, 249)):
        rendered = font.render(str(string), True, color)
        self.screen.blit(rendered,
                         rendered.get_rect(center=(SCREEN_SIZE // 2, y)))

    def draw_button(self, name, label, active=True):
        rect = self.buttons[name]
        hovered = active and rect.collidepoint(pygame.mouse.get_pos())
        fill = (18, 115, 148) if hovered else (11, 70, 92)
        edge = (107, 232, 244) if hovered else (66, 161, 183)
        pygame.draw.rect(self.screen, (3, 16, 26), rect.move(0, 5),
                         border_radius=13)
        pygame.draw.rect(self.screen, fill, rect, border_radius=13)
        pygame.draw.rect(self.screen, edge, rect, 2, border_radius=13)
        self.text_center(label, rect.centery, self.font,
                         (255, 255, 255) if hovered else (216, 238, 246))

    def scene_background(self, creatures=True):
        # Скорость не зависит от FPS: от этого цикл основного меню не тормозит
        # движение существ при просадках кадров в браузере.
        dt = max(0.0, min(0.05, self.clock.get_time() / 1000.0))
        if dt == 0:
            dt = 1 / 60
        self.seconds += dt
        self.screen.blit(self.background, (0, 0))
        for x, y, radius, phase in self.particles:
            yy = int((y - self.seconds * (6.0 + radius * 5.4)) % SCREEN_SIZE)
            bright = (math.sin(phase + self.seconds * 2.1) + 1) / 2
            color = (int(24 + bright*48), int(79 + bright*105),
                     int(93 + bright*140))
            pygame.draw.circle(self.screen, color, (x, yy), radius)

        # Рыбы непрерывно плывут с разными скоростями, некоторые вправо,
        # другие влево. Когда особь покидает экран, она появляется за
        # противоположной границей. Изображение отражается, НЕ растягивается.
        for animal in self.animals:
            animal["x"] += animal["direction"] * animal["speed"] * dt
            img = (animal["sprite"] if animal["direction"] > 0
                   else animal["reverse"])
            half_width = img.get_width() / 2
            if animal["direction"] > 0 and animal["x"] - half_width > SCREEN_SIZE + 10:
                animal["x"] = -half_width - self.rng.randrange(10, 70)
            elif animal["direction"] < 0 and animal["x"] + half_width < -10:
                animal["x"] = SCREEN_SIZE + half_width + self.rng.randrange(10, 70)
            if creatures:
                yy = animal["y"] + math.sin(
                    self.seconds * (0.65 + animal["speed"] / 125.0)
                    + animal["phase"]) * animal["bob"]
                self.screen.blit(img, img.get_rect(
                    center=(round(animal["x"]), round(yy))))

    def draw_main(self):
        self.scene_background()
        # Полупрозрачные пластины обеспечивают читаемость поверх движущихся рыб.
        top_plate = pygame.Surface((SCREEN_SIZE - 24, 142), pygame.SRCALPHA)
        top_plate.fill((3, 21, 37, 169))
        self.screen.blit(top_plate, (12, 12))
        button_plate = pygame.Surface((338, 214), pygame.SRCALPHA)
        button_plate.fill((2, 20, 33, 174))
        self.screen.blit(button_plate, (146, 317))
        self.text_center("МЕГОСУБНАТИКА 2D", 72, self.title_font,
                         (189, 242, 251))
        self.text_center("Планета 4546B", 112, self.font, (140, 220, 241))
        self.text_center("Исследуй океан, строй базы и приручай существ",
                         137, self.small_font, (162, 216, 224))
        self.draw_button("start", "НАЧАТЬ ИГРУ")
        self.draw_button("info", "ИНФОРМАЦИЯ ОБ ИГРЕ")
        self.draw_button("exit", "ВЫХОД")
        self.text_center("Фанатская игра • Python / Pygame", 616,
                         self.tiny_font, (145, 196, 206))
        pygame.display.flip()

    def draw_info(self):
        self.scene_background(creatures=False)
        self.text_center("ИНФОРМАЦИЯ ОБ ИГРЕ", 62, self.heading_font)
        lines = [
            "Мегосубнатика 2D — исследование планеты 4546B,",
            "существа, пещеры, ресурсы и строительство.",
            "",
            "WASD / стрелки — передвижение",
            "Мышь — направление, ЛКМ — выстрел",
            "E — подобрать    SPACE — атаковать",
            "R — инвентарь    I — крафт    M — карта",
            "T — список питомцев    H — выпустить питомца",
            "U — использовать / лечить    P — выбросить",
            "F — управление транспортом",
            "N — настройки    F8 — ночной режим (тест)",
            "Колесо мыши — масштаб камеры",
            "",
            "Исходная игровая графика и механики сохранены.",
            "На телефоне: джойстик + экранные кнопки.",
            "Касание игрового мира — выстрел в выбранную точку.",
        ]
        for i, line in enumerate(lines):
            self.text_center(line, 125 + i * 25, self.small_font,
                             (160, 222, 231) if i in (0, 1, 13, 14)
                             else (218, 235, 242))
        self.draw_button("back", "НАЗАД В МЕНЮ")
        pygame.display.flip()

    def draw_loading(self):
        self.scene_background()
        self.text_center("СОЗДАНИЕ МИРА", 288, self.heading_font)
        self.text_center("Генерируем биомы, флору, фауну и пещеры...",
                         332, self.small_font)
        pygame.display.flip()

    def draw_death(self, stats):
        self.scene_background()
        shade = pygame.Surface((SCREEN_SIZE, SCREEN_SIZE), pygame.SRCALPHA)
        shade.fill((13, 7, 18, 155))
        self.screen.blit(shade, (0, 0))
        self.text_center("ВЫ ПОГИБЛИ", 191, self.title_font, (251, 109, 116))
        self.text_center("Исследование планеты 4546B завершено.",
                         254, self.font)
        self.text_center(stats, 297, self.small_font, (177, 213, 225))
        self.draw_button("again", "ИГРАТЬ СНОВА")
        self.draw_button("main", "ГЛАВНОЕ МЕНЮ")
        self.text_center("Enter — начать заново   •   Esc — меню",
                         554, self.small_font, (174, 208, 218))
        pygame.display.flip()

    def draw_exit(self):
        # JS не позволяет закрывать обычную вкладку, не открытую скриптом.
        # Для браузера показывается корректный экран завершения с возвратом.
        self.scene_background()
        self.text_center("ВЫХОД ИЗ ИГРЫ", 202, self.heading_font)
        self.text_center("Игровая сессия завершена.", 267, self.font)
        self.text_center("Теперь можно закрыть вкладку браузера.",
                         309, self.small_font, (175, 221, 229))
        self.draw_button("main", "ВЕРНУТЬСЯ В МЕНЮ")
        pygame.display.flip()

    def draw_error(self, error):
        self.scene_background(creatures=False)
        self.text_center("ОШИБКА ЗАПУСКА", 172, self.heading_font,
                         (255, 144, 144))
        self.text_center("Не удалось создать игровой мир.", 233, self.font)
        for i in range(0, min(3, (len(error) + 54) // 55)):
            self.text_center(error[i * 55:(i + 1) * 55], 286 + i * 27,
                             self.tiny_font)
        self.draw_button("back", "ВЕРНУТЬСЯ В МЕНЮ")
        pygame.display.flip()


async def main():
    """Pygbag entrypoint. Never block the event loop with a while True loop."""
    pygame.init()
    screen = create_game_display()
    pygame.display.set_caption("Мегосубнатика 2D — планета 4546B")
    interface = Frontend(screen)
    scene = "menu"
    game = None
    death_stats = ""
    error_message = ""
    running = True

    while running:
        if scene == "playing":
            game.handle_events()  # The original event processing is preserved.
            if not game.running:
                # Escape from the game returns to the main menu.
                if pygame.mixer.get_init():
                    pygame.mixer.music.stop()
                game = None
                scene = "menu"
            else:
                game.update()
                if game.player_hp <= 0 or game.state == "dead":
                    death_stats = "Прожито игровых суток: {:.1f}".format(
                        game.elapsed_game_days)
                    if pygame.mixer.get_init():
                        pygame.mixer.music.stop()
                    game = None  # New game = new world, health, inventory, fauna.
                    scene = "dead"
                else:
                    game.render()  # Original renderer, untouched.
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if scene == "menu":
                        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            scene = "loading"
                        elif event.key == pygame.K_i:
                            scene = "info"
                        elif event.key == pygame.K_ESCAPE:
                            if sys.platform == "emscripten":
                                scene = "exit"
                            else:
                                running = False
                    elif scene == "info" and event.key == pygame.K_ESCAPE:
                        scene = "menu"
                    elif scene == "dead":
                        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            scene = "loading"
                        elif event.key == pygame.K_ESCAPE:
                            scene = "menu"
                    elif scene == "error" and event.key == pygame.K_ESCAPE:
                        scene = "menu"
                    elif scene == "exit" and event.key == pygame.K_ESCAPE:
                        scene = "menu"
                elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                      or event.type == getattr(pygame, "FINGERDOWN", -1000)):
                    pos = (event.pos if event.type == pygame.MOUSEBUTTONDOWN
                           else (round(event.x * SCREEN_SIZE),
                                 round(event.y * SCREEN_SIZE)))
                    if scene == "menu":
                        if interface.buttons["start"].collidepoint(pos):
                            scene = "loading"
                        elif interface.buttons["info"].collidepoint(pos):
                            scene = "info"
                        elif interface.buttons["exit"].collidepoint(pos):
                            # Обычную вкладку браузера нельзя закрыть из игры.
                            # На ПК завершаем процесс, в браузере — экран выхода.
                            if sys.platform == "emscripten":
                                scene = "exit"
                            else:
                                running = False
                    elif scene in ("info", "error"):
                        if interface.buttons["back"].collidepoint(pos):
                            scene = "menu"
                    elif scene == "dead":
                        if interface.buttons["again"].collidepoint(pos):
                            scene = "loading"
                        elif interface.buttons["main"].collidepoint(pos):
                            scene = "menu"
                    elif scene == "exit":
                        if interface.buttons["main"].collidepoint(pos):
                            scene = "menu"
            if scene == "menu":
                interface.draw_main()
            elif scene == "info":
                interface.draw_info()
            elif scene == "dead":
                interface.draw_death(death_stats)
            elif scene == "error":
                interface.draw_error(error_message)
            elif scene == "exit":
                interface.draw_exit()
            elif scene == "loading":
                interface.draw_loading()
                # Yield a frame so loading is visible BEFORE the world is generated.
                await asyncio.sleep(0)
                try:
                    game = Game()
                    scene = "playing"
                except Exception as exc:
                    import traceback
                    traceback.print_exc()
                    error_message = "{}: {}".format(type(exc).__name__, exc)
                    scene = "error"
        interface.clock.tick(60)
        # Pygbag's WebAssembly runtime REQUIRES this yield each frame.
        await asyncio.sleep(0)

    if sys.platform != "emscripten":
        pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
