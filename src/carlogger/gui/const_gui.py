from customtkinter import CTkImage
from PIL import Image

from carlogger.const import PATH

# ===== Colors ===== #

BG_GRAY_PRIMARY = '#1b1c1b'
BG_GRAY_SECONDARY = '#2e2e2e'
BLUE_1 = '#35383d'

house_png = Image.open(PATH.joinpath("./src/carlogger/gui/img/house.png"))
car_png = Image.open(PATH.joinpath("./src/carlogger/gui/img/car.png"))
collection_png = Image.open(PATH.joinpath("./src/carlogger/gui/img/collection.png"))
component_png = Image.open(PATH.joinpath("./src/carlogger/gui/img/component.png"))

# ===== Item Icons ===== #

car_icon = CTkImage(light_image=car_png,
                    dark_image=car_png,
                    size=(165, 165))

collection_icon = CTkImage(light_image=collection_png,
                           dark_image=collection_png,
                           size=(165, 165))

component_icon = CTkImage(light_image=component_png,
                          dark_image=component_png,
                          size=(165, 165))

# ===== Mini Icons ===== #

house_icon_mini = CTkImage(light_image=house_png,
                           dark_image=house_png,
                           size=(25, 25))

car_icon_mini = CTkImage(light_image=car_png,
                         dark_image=car_png,
                         size=(25, 25))

collection_icon_mini = CTkImage(light_image=collection_png,
                                dark_image=collection_png,
                                size=(25, 25))

component_icon_mini = CTkImage(light_image=component_png,
                               dark_image=component_png,
                               size=(25, 25))


def get_img_from_path(path, item) -> CTkImage:
    try:
        img = Image.open(path)
    except OSError:
        return item.image

    return CTkImage(light_image=img, dark_image=img, size=(165, 165))


def get_img_from_class(item) -> CTkImage:
    match item.__class__.__name__:
        case 'Car':
            return car_icon_mini
        case 'ComponentCollection':
            return collection_icon_mini
        case 'CarComponent':
            return component_icon_mini
        case _:
            return house_icon_mini
