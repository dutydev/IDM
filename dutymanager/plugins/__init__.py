from .base_events.base_events import bot as base_bp
from .base_events.delete_messages import bot as base_delete
from .base_events.delete_by_type import bot as type_bp
from .base_events.return_user import bot as return_bp
from .base_events.meet_duty import bot as meet_bp
from .base_events.to_group import bot as group_bp
from .additions.trusted import bot as trusted_bp
from .additions.unbind_chat import bot as unbind_bp
from .additions.templates import bot as template_bp
from .additions.ping import bot as ping_bp
from .additions.settings import bot as limit_bp
from .additions.repeat import bot as repeat_bp
from .additions.delete_messages import bot as delete_bp
from .additions.add_friends import bot as friend_bp
from ..units.utils import bp as util_bp
from ..units.vk_script import bot as script_bp
from ..core.error_handler import bot as error_bp

# LongPoll
from .longpoll.ping import bot as lp_ping
from .longpoll.middleware import bot as block_bp

# Workers
from ..units.dataclasses.workers import bot as worker_bp
from .additions.workers.friends import bot as friends_bp
from .additions.workers.online import bot as online_bp
from .additions.workers.out_friends import bot as out_bp

blueprints = (
    base_bp, util_bp, unbind_bp,
    base_delete, return_bp, ping_bp,
    template_bp, lp_ping, script_bp,
    limit_bp, error_bp, trusted_bp,
    repeat_bp, friends_bp, out_bp,
    online_bp, worker_bp, meet_bp,
    block_bp, delete_bp, friend_bp,
    type_bp, group_bp
)