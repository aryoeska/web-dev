from market.models import db, User, Item
from market import app, routes

user1 = User(username='aryo', password_hash='123123', email_address='aryo@aryo.com')
item1 = Item(name="IPhone15", price=500, barcode="878224756", description="with A99 Bionic Chipset")
item2 = Item(name="Macbook Air M1", price=700, barcode="576788912", description="More Professional with M1")


with app.app_context():
    # db.drop_all()
    # db.create_all()
    # db.session.add(user1)
    # db.session.commit()
    # User.query.all()

    # db.session.add(item2)
    # db.session.commit()
    # print(Item.query.all())

    db.session.rollback()
    item1.owner = User.query.filter_by(username='aryo').first().id
    db.session.add(item1)
    db.session.commit
    print(item1.owner)

# if __name__ == '__main__':
#      app.run(debug=True, use_reloader=False)