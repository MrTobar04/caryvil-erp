# -*- coding: utf-8 -*-
from . import models  # noqa: F401
from . import controllers  # noqa: F401
from . import wizards  # noqa: F401


def post_init_hook(env):
    """Configura el almacenamiento de adjuntos y assets compilados en base de datos.

    En entornos efímeros (como Render), evita errores 500 garantizando que
    los bundles de assets se persistan en PostgreSQL.
    """
    env["ir.config_parameter"].sudo().set_param("ir_attachment.location", "db")
