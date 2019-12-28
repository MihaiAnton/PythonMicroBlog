# demo for mail sending

import app

from flask_mail import Message

with app.app.app_context():
    # test code
    msg = Message('test subject', sender=app.app.config['ADMINS'][0], recipients=['antonmihai58@gmail.com'])
    msg.text = 'text body'
    msg.html = '<h1>HTML body</h1>'
    app.mail.send(msg)