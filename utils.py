from aiogram.utils.media_group import MediaGroupBuilder
from dct import book
from aiogram.types import FSInputFile
from aiogram.types.input_file import URLInputFile

def get_album(type, product):
    dd = book["Номенклатура"][type][product]
    album_builder = MediaGroupBuilder(caption=dd["Описание"])
    for name in dd['photo']:
        album_builder.add(
            type="photo",
            media=FSInputFile(f"img/{name}.PNG"))
    return album_builder

def get_prod_in_type():
    names = []
    for i in book["Номенклатура"].keys():
        for j in book["Номенклатура"][i].keys():
            names.append(j)
    return names
