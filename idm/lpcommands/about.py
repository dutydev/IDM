from ..objects import DB, __version__
from .utils import msg_op
from . import dlp

@dlp.register('info','инфа','инфо')
def about(nd):
    db = nd.db
    message = f"""Информация о LP модуле:
    IDM-SC-mod v{__version__}
    
    CallBack модуль: {'✅' if db.adv[0] == 'LP-CB' else '❌'}

    Код лежит здесь:
    https://github.com/Elchinchel/IDM
    """.replace('    ', '')

    msg_op(2, nd[3], message, nd[1])
    return "ok"
