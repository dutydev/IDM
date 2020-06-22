from idm.objects import db_gen as db
from idm import app

if db.installed:
    if db.mode.startswith('LP'):
        from idm.lp import LPstart
        LPstart()

if __name__ == "__main__":
    app.run(host="0.0.0.0")