import globals
import pygame

from events import events
from layer import Layer
from screen import Display


class Mouse:

    def __init__(self):
        self.rect = pygame.draw.circle(Display.fake_display, (250, 0, 0, 0), pygame.mouse.get_pos(), 5, 0)
        self.highlight_rect = None
        self.calced = False
        self.point_at_click = None
        self.move_offset = None

    def get_pos(self):
        return pygame.mouse.get_pos()

    def get_rect(self):
        return self.rect

    def button_pressed(self, button, layer="layer_0"):
        if layer == Layer.get_layer() or layer == "layer_all":
            mappings = {"MONE": 0, "MMIDDLE": 1, "MTWO": 2, "WUP": 4, "WDOWN": 5}
            return self.__dict__["MOUSEBUTTON"][mappings[button]]
        return False

    def contains(self, rect):
        self.rect.contains(rect)

    def eval_highlight_color(self, color):
        r, g, b = 0, 0 ,0

        if color[0] + 100 <= 255:
            r = color[0] + 100
        else:
            r = color[0] - 155
        if color[1] + 100 <= 255:
            g = color[1] + 100
        else:
            g = color[1] - 155
        if color[2] + 100 <= 255:
            b = color[2] + 100
        else:
            b = color[2] - 155
        return (r, g, b)

    def get_starting_point(self):
        if not events.button_pressed("MTWO"):
            self.calced = False
        if not self.calced:
            self.calced = True
            return pygame.mouse.get_pos()

    def move_rect(self, obj):
        if self.rect.colliderect(obj.rect):
            if self.move_offset is not None:
                for i, _ in enumerate(obj.points):
                    obj.points[i] = (self.get_pos()[0] + self.move_offset[i][0], self.get_pos()[1] + self.move_offset[i][1])
            else:
                self.move_offset = [(obj.points[i][0] - mouse.get_pos()[0], obj.points[i][1] - mouse.get_pos()[1]) for i, _ in enumerate(obj.points)]

    def update(self):
        if globals.editor:
            self.rect = pygame.draw.circle(Display.fake_display, (250, 0, 0, 0), pygame.mouse.get_pos(), 5, 0)

            if globals.selection_list:
                for obj in globals.selection_list:
                    color = self.eval_highlight_color(obj.color)
                    pygame.draw.polygon(Display.fake_display, color, tuple(obj.points), 3)

            if events.button_pressed_once("MONE"):
                found_obj = None
                #this needs to traverse the list from top to bottom layer later
                for obj in globals.poly_dict:
                    if obj.contains(self.rect):
                        found_obj = obj

                if found_obj:
                    if found_obj not in globals.selection_list:
                        if not events.key_pressed("LSHIFT"):
                            globals.selection_list = []
                        globals.selection_list.append(found_obj)
                else:
                    globals.selection_list = []

            if events.button_pressed_once("MTWO"):
                self.point_at_click = pygame.mouse.get_pos()

            if events.button_pressed("MTWO"):
                self.selection_box = pygame.draw.rect(Display.fake_display, [100, 100, 100], (self.point_at_click[0], self.point_at_click[1], pygame.mouse.get_pos()[0] - self.point_at_click[0], pygame.mouse.get_pos()[1] - self.point_at_click[1]), 3)

            if events.button_released("MTWO"):
                self.point_at_click = None
                globals.selection_list = []
                for obj in globals.poly_dict:
                    if self.selection_box.colliderect(obj.rect):
                        globals.selection_list.append(obj)

                if globals.selection_list:
                    globals.selection = None

            if events.button_pressed("MONE") and not events.key_pressed("LSHIFT"):
                for obj in globals.selection_list:
                    self.move_rect(obj)
            else:
                self.move_offset = None
        else:
            pass


mouse = Mouse()
