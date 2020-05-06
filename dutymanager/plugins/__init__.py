from .base_events.base_events import bot as base_bp
from .base_events.delete_messages import bot as delete_bp
from .base_events.return_user import bot as return_bp
from .additions.unbind_chat import bot as unbind_bp
from .additions.templates import bot as template_bp
from .additions.ping import bot as ping_bp
from .additions.settings import bot as limit_bp
from ..units.utils import bp as util_bp
from ..units.vk_script import bot as script_bp

# LongPoll
from .longpoll.ping import bot as lp_ping

blueprints = (
    base_bp, util_bp, unbind_bp,
    delete_bp, return_bp,
    template_bp, ping_bp,
    lp_ping, script_bp,
    limit_bp
)