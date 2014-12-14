#!/usr/bin/env python

from models import PostHandler as PH
PH().make_db()
from models import db, User
db.session.add(User('Mark','admin'))
db.session.commit()
print "[*] Populated users!"
