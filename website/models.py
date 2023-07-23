from website import db, login_manager
from website import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


user_cart = db.Table('user_cart',
                     db.Column('user_id', db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('item_id', db.Integer, db.ForeignKey('item.id'))
                     )

user_cart1 = db.Table('user_cart1',
                      db.Column('usern_id', db.Integer,
                                db.ForeignKey('user.id')),
                      db.Column('itemn_id', db.Integer,
                                db.ForeignKey('item.id')),
                      db.Column('item_qbought', db.Integer, default=1)
                      )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50),
                              nullable=False, unique=True)
    phone_number = db.Column(db.Integer(), nullable=False, unique=True)
    password_hash = db.Column(db.String(), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)
    bought = db.relationship('Item', secondary=user_cart1, backref='boughtby')
    ibought = db.relationship('Temp', backref='buyer', lazy=True)
    isold = db.relationship('Stemp', backref='seller', lazy=True)
    iboughtf = db.relationship('Tempf', backref='buyerf', lazy=True)
    isoldf = db.relationship('Stempf', backref='sellerf', lazy=True)
    address = db.Column(db.String(length=1024), nullable=False)
    image = db.Column(db.String(length=1024))

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'₹{str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f'₹{self.budget}'

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj, quantity):
        if item_obj.quantity >= quantity:
            return self.budget >= float(item_obj.price)*float(quantity)
        else:
            return False


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    quantity = db.Column(db.Integer())
    description = db.Column(db.String(length=1024),
                            nullable=False, unique=True)
    fertilizer = db.Column(db.String(length=1024), nullable=False)
    pesticide = db.Column(db.String(length=1024), nullable=False)
    image = db.Column(db.String, nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    ubought = db.relationship('Temp', backref='buying', lazy=True)
    usold = db.relationship('Stemp', backref='selling', lazy=True)
    type = db.Column(db.String(length=1024))

    def __repr__(self):
        return f'Item {self.name}'

    def buy(self, user, quantity):
        if quantity == None:
            quantity = 1
        # self.boughtby.append(user)
        temp_to_create = Temp(userid=user.id, itemid=self.id, bought=quantity)
        db.session.add(temp_to_create)
        user.budget -= float(quantity)*float(self.price)
        self.quantity -= float(1)*float(quantity)
        db.session.commit()

    def sell(self, user, quantity):
        if quantity == None:
            quantity = 1
        stemp_to_create = Stemp(userid=user.id, itemid=self.id, sold=quantity)
        db.session.add(stemp_to_create)
        user.budget += float(quantity)*float(self.price)
        self.quantity += float(1)*float(quantity)
        db.session.commit()

    # def buy(self, user):
    #    self.owner = user.id
    #    user.budget -= self.price
    #    self.quantity -= 1
    #    db.session.commit()


class Temp(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    userid = db.Column(db.Integer(), db.ForeignKey('user.id'))
    itemid = db.Column(db.Integer(), db.ForeignKey('item.id'))
    bought = db.Column(db.Numeric(10, 2), default=1)


class Stemp(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    userid = db.Column(db.Integer(), db.ForeignKey('user.id'))
    itemid = db.Column(db.Integer(), db.ForeignKey('item.id'))
    sold = db.Column(db.Numeric(10, 2), default=1)


class Fert(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    quantity = db.Column(db.Integer())
    description = db.Column(db.String(length=1024),
                            nullable=False, unique=True)
    type = db.Column(db.String(length=1024))
    extra = db.Column(db.String(length=1024), nullable=False, unique=True)
    image = db.Column(db.String, nullable=False, unique=True)
    ubought = db.relationship('Tempf', backref='buying', lazy=True)
    usold = db.relationship('Stempf', backref='selling', lazy=True)

    def __repr__(self):
        return f'Item {self.name}'

    def back(self, user, quantity, item):
        if quantity == None:
            quantity = 1
        temp_to_delete = item
        user.budget += float(quantity)*float(self.price)
        self.quantity += float(1)*float(quantity)
        db.session.delete(temp_to_delete)
        db.session.delete()

    def buy(self, user, quantity):
        if quantity == None:
            quantity = 1
        # self.boughtby.append(user)
        temp_to_create = Tempf(userid=user.id, fertid=self.id, bought=quantity)
        db.session.add(temp_to_create)
        user.budget -= float(quantity)*float(self.price)
        self.quantity -= float(1)*float(quantity)
        db.session.commit()

    def sell(self, user, quantity):
        if quantity == None:
            quantity = 1
        stemp_to_create = Stemp(userid=user.id, itemid=self.id, sold=quantity)
        db.session.add(stemp_to_create)
        user.budget += float(quantity)*float(self.price)
        self.quantity += float(1)*float(quantity)
        db.session.commit()


class Tempf(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    userid = db.Column(db.Integer(), db.ForeignKey('user.id'))
    fertid = db.Column(db.Integer(), db.ForeignKey('fert.id'))
    bought = db.Column(db.Numeric(10, 2), default=1)


class Stempf(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    userid = db.Column(db.Integer(), db.ForeignKey('user.id'))
    fertid = db.Column(db.Integer(), db.ForeignKey('fert.id'))
    sold = db.Column(db.Numeric(10, 2), default=1)
