from common import app, db
from models import *


if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    user1 = UserModel(is_active=True)
    db.session.add(user1)

    user_email1 = UserEmailModel(user=user1)
    db.session.add(user_email1)

    user2 = UserModel(is_active=False)
    db.session.add(user2)

    user_email2 = UserEmailModel(user=user2)
    db.session.add(user_email2)
    db.session.commit()

    app.run(debug=True)
