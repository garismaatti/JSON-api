from app import db

class Catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(64), index=True)
    amount = db.Column(db.Integer index=True)
    price = db.Column(db.Float(), index=True)

    def __repr__(self):
        return '<Catalog %r>' % (self.name)


class Basket(db.Model):
    user_id = db.Column(db.String(64), primary_key=True, unique=True)
    product_id = db.Column(db.String(64), index=True)
    amount = db.Column(db.Integer index=True)
    mod_time = db.Column(db.DateTime(), index=True)

    def __repr__(self):
        return '<Basket %r>' % (self.user_id)
