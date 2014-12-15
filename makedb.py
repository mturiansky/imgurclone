#!/usr/bin/env python

from models import PostHandler as PH
PH().make_db()
from models import db, User, Backends
db.session.add(User('Mark','admin'))
db.session.add(Backends('http://127.0.0.1:4999/'))
db.session.commit()
print "[*] Populated users!"
