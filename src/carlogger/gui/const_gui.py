from customtkinter import CTkImage
from PIL import Image

from carlogger.const import PATH


# ===== Colors ===== #

BG_GRAY_PRIMARY = '#1b1c1b'
BG_GRAY_SECONDARY = '#2e2e2e'
BLUE_1 = '#35383d'


car_png = Image.open(PATH.joinpath("./src/carlogger/gui/img/car.png"))
collection_png = Image.open(PATH.joinpath("./src/carlogger/gui/img/collection.png"))
component_png = Image.open(PATH.joinpath("./src/carlogger/gui/img/component.png"))

car_icon = CTkImage(light_image=car_png,
                    dark_image=car_png,
                    size=(165, 165))

collection_icon = CTkImage(light_image=collection_png,
                           dark_image=collection_png,
                           size=(165, 165))

component_icon = CTkImage(light_image=component_png,
                          dark_image=component_png,
                          size=(165, 165))


def get_img_from_path(path, item) -> CTkImage:
    try:
        img = Image.open(path)
    except OSError:
        return item.image

    return CTkImage(light_image=img, dark_image=img, size=(165, 165))
