from flask.ext.login import UserMixin
from . import db

# Below, the __tablename__ attribute declares the table name and
# forces the creation of the table. So the engine must
# be available at the time of class declaration if done
# this way. This is done here with the 'from . import db' above
# more here
'''<!-- http://docs.sqlalchemy.org/en/rel_1_1/orm/
            extensions/declarative/api.html -->'''


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    social_id = db.Column(db.String(64), nullable=True, unique=False)
    nickname = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(255), nullable=True, unique=False)
    password = db.Column(db.String(255), nullable=True)


class Catalog(db.Model):
    __tablename__ = 'catalogs'
    catalog_id = db.Column(db.Integer, primary_key=True)
    catalog_name = db.Column(db.String(250), nullable=False)
    catalog_description = db.Column(db.String(1000), nullable=True)
    catalog_owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    catalog_owner = db.relationship(User, backref=db.backref('catalog_owner',
                                                             lazy='dynamic'))

    @property
    def serialize(self):
        return {
            'catalog_id': self.catalog_id,
            'catalog_name': self.catalog_name,
            'catalog_description': self.catalog_name
        }


class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    category_description = db.Column(db.String(500))
    category_owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_owner = db.relationship(User, backref=db.backref('category_owner',
                                                              lazy='dynamic'))

    @property
    def serialize(self):
        return {
            'category_name': self.category_name,
            'category_description': self.category_description,
            'category_id': self.category_id
        }


class Item(db.Model):
    __tablename__ = 'items'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(120), nullable=False)
    item_description = db.Column(db.String(1000))
    item_price = db.Column(db.Float)
    item_owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_category_id = db.Column(
        db.Integer, db.ForeignKey('categories.category_id'))
    item_catalog_id = db.Column(
        db.Integer, db.ForeignKey('catalogs.catalog_id'))
    item_photo_file_name = db.Column(db.String(512))
    item_owner = db.relationship(
        User, backref=db.backref('item_owner', lazy='dynamic'))
    item_category = db.relationship(Category,
                                    backref=db.backref('item_category',
                                                       lazy='dynamic'))
    item_catalog = db.relationship(Catalog, backref=db.backref('item_catalog',
                                                               lazy='dynamic'))

    @property
    def serialize(self):
        return {
            'item_catalog_id': self.item_catalog_id,
            'item_catalog_name': self.item_catalog.catalog_name,
            'item_name': self.item_name,
            'item_description': self.item_description,
            'item_id': self.item_id,
            'item_price': self.item_price,
            'category': self.item_category.category_name
        }
