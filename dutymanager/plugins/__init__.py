from .base_events.base_events import bot as base_bp
from .additions.unbind_chat import bot as unbind_bp
from ..units.utils import bp as util_bp

blueprints = (base_bp, util_bp, unbind_bp)