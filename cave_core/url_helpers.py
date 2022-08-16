from cave_core import models


def get_extra_content():
    try:
        return {"globals": models.Globals.get_solo()}
    except:
        return {}
