from customtkinter import CTkImage
from PIL import Image


car_png = Image.open("./src/carlogger/gui/img/car.png")
collection_png = Image.open("./src/carlogger/gui/img/collection.png")
component_png = Image.open("./src/carlogger/gui/img/component.png")

car_icon = CTkImage(light_image=car_png,
                    dark_image=car_png,
                    size=(165, 165))

collection_icon = CTkImage(light_image=collection_png,
                           dark_image=collection_png,
                           size=(165, 165))

component_icon = CTkImage(light_image=component_png,
                          dark_image=component_png,
                          size=(165, 165))


def get_img_from_path(path) -> CTkImage:
        img = Image.open(path)
        return CTkImage(light_image=img, dark_image=img, size=(165, 165))
