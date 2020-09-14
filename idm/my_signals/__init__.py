import os
for name in os.listdir(os.path.dirname(__file__)):
    if not name.endswith('.py') or name in {'__init__.py', '__pycache__'}:
        continue
    name = name.replace('.py', '')
    exec(f"from .{name} import __name__")

from .built_in_anims.anims import __name__

from .templates.anims import __name__
from .templates.voices import __name__
from .templates.template import __name__
