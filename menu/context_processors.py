from django.conf import settings


def cfg_assets_root(request) -> None:

    return { 'ASSETS_ROOT' : settings.ASSETS_ROOT }
