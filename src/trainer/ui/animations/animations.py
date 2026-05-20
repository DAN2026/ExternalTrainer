import time
import dearpygui.dearpygui as dpg


def lerp(a, b, t):
    return a + (b - a) * t


def lerp_color(c1, c2, t):
    return (
        int(lerp(c1[0], c2[0], t)),
        int(lerp(c1[1], c2[1], t)),
        int(lerp(c1[2], c2[2], t)),
        int(lerp(c1[3], c2[3], t)),
    )


class ColorTransition:

    def __init__(
        self,
        target: str | int,
        color_slot: int,
        initial: tuple,
        final: tuple,
        duration: float = 0.2,
    ):
        self.__target = target
        self.__initial = initial
        self.__final = final
        self.__duration = duration
        self.__t = 0.0
        self.__last = time.time()

        with dpg.theme() as self.__theme:
            with dpg.theme_component(dpg.mvAll):
                self.__color_item = dpg.add_theme_color(color_slot, initial)

        dpg.bind_item_theme(self.__target, self.__theme)

    def tick(self):
        now = time.time()
        delta = now - self.__last
        self.__last = now

        hovered = dpg.is_item_hovered(self.__target)
        direction = 1 if hovered else -1

        if (direction == 1 and self.__t < 1.0) or (direction == -1 and self.__t > 0.0):
            self.__t += direction * (delta / self.__duration)
            self.__t = max(0.0, min(1.0, self.__t))
            dpg.set_value(
                self.__color_item, lerp_color(self.__initial, self.__final, self.__t)
            )


class UnderlineTransition:

    def __init__(
        self, target: str | int, width: float, color: tuple, duration: float = 0.2
    ):
        self.__target = target
        self.__width = width
        self.__color = color
        self.__duration = duration
        self.__t = 0.0
        self.__last = time.time()

        self.__drawlist = dpg.add_drawlist(width=width, height=4, parent=target)
        self.__line = dpg.draw_line(
            p1=(0, 0),
            p2=(0, 0),
            color=color,
            thickness=2,
            parent=self.__drawlist,
        )

    def tick(self):
        now = time.time()
        delta = now - self.__last
        self.__last = now

        hovered = dpg.is_item_hovered(self.__target)
        direction = 1 if hovered else -1

        if (direction == 1 and self.__t < 1.0) or (direction == -1 and self.__t > 0.0):
            self.__t += direction * (delta / self.__duration)
            self.__t = max(0.0, min(1.0, self.__t))

            centre = self.__width / 2
            half = lerp(0, self.__width / 2, self.__t)

            dpg.configure_item(
                self.__line,
                p1=(centre - half, 0),
                p2=(centre + half, 0),
            )


class ScaleTransition:

    def __init__(
        self,
        target: str | int,
        base_w: int,
        base_h: int,
        scale: float = 1.2, 
        duration: float = 0.15,
    ):
        self.__target = target
        self.__base_w = base_w
        self.__base_h = base_h
        self.__final_w = int(base_w * scale)
        self.__final_h = int(base_h * scale)
        self.__duration = duration
        self.__t = 0.0
        self.__last = time.time()

    def tick(self):
        now = time.time()
        delta = now - self.__last
        self.__last = now

        hovered = dpg.is_item_hovered(self.__target)
        direction = 1 if hovered else -1

        if (direction == 1 and self.__t < 1.0) or (direction == -1 and self.__t > 0.0):
            self.__t += direction * (delta / self.__duration)
            self.__t = max(0.0, min(1.0, self.__t))

            w = int(lerp(self.__base_w, self.__final_w, self.__t))
            h = int(lerp(self.__base_h, self.__final_h, self.__t))

            dpg.configure_item(self.__target, width=w, height=h)


class SlideTransition:
    def __init__(
        self,
        target: str | int,
        active_x: float,
        offscreen_x: float,
        y: float,
        duration: float = 0.25,
    ):
        self.__target = target
        self.__active_x = active_x  
        self.__offscreen_x = offscreen_x  
        self.__y = y
        self.__duration = duration
        self.__t = 0.0
        self.__active = False
        self.__last = time.time()

    def set_state(self, active: bool):
        self.__active = active
        
        dpg.configure_item(self.__target, show=True)

    def tick(self):
        now = time.time()
        delta = now - self.__last
        self.__last = now

        direction = 1 if self.__active else -1

        if (direction == 1 and self.__t < 1.0) or (direction == -1 and self.__t > 0.0):
            self.__t += direction * (delta / self.__duration)
            self.__t = max(0.0, min(1.0, self.__t))

            current_x = lerp(self.__offscreen_x, self.__active_x, self.__t)
            dpg.set_item_pos(self.__target, [current_x, self.__y])

            if self.__t <= 0.0 and not self.__active:
                dpg.configure_item(self.__target, show=False)
