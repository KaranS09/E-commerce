from asyncio.windows_events import NULL
from cProfile import run
from unicodedata import category
from website import app
from flask import render_template, redirect, url_for, flash, request, sessions, session
from website.models import User, Item, user_cart1, Temp, Stemp, Fert, Tempf
from website.forms import LoginForm, SignInForm, PurchaseItemForm, SellItemForm
from website import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/produce', methods=['GET', 'POST'])
@login_required
def produce_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    if request.method == "POST":
        # buy
        quantity_bought = purchase_form.bquantity.data

        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object, quantity_bought):
                p_item_object.buy(current_user, quantity_bought)
                flash(
                    f"You purchased { p_item_object.name } for ₹{ quantity_bought*p_item_object.price }", category="success")
            else:
                flash(
                    f"Error while purchasing {p_item_object.name}", category="danger")
        # sell
        quantity_sold = sell_form.bquantity.data
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            s_item_object.sell(current_user, quantity_sold)
            flash(
                f"You sold { s_item_object.name } for ₹{ quantity_bought*s_item_object.price }", category="success")

        return redirect(url_for('produce_page'))

    if request.method == "GET":
        items = Item.query.all()

        return render_template('produce.html', items=items, purchase_form=purchase_form, sell_form=sell_form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data,
                              phone_number=form.phone_number.data, password=form.password1.data, address=form.address.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(
            f'Account created successfully! You are now logged in as {user_to_create.username}', category='success')
        return redirect(url_for('produce_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('login.html', form=form)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in_page():
    form = SignInForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(
                f'Success! You are logged in as { attempted_user.username }', category='success')
            return redirect(url_for('produce_page'))

        else:
            flash('Username and password do not match! Please try again',
                  category='danger')
    return render_template('sign_in.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


@app.route('/fertilizer', methods=['GET', 'POST'])
@login_required
def fertilizer_page():
    purchase_form_f = PurchaseItemForm()
    if request.method == "POST":
        # buy
        quantity_bought_f = purchase_form_f.bquantity.data

        purchased_fert = request.form.get('purchased_fert')
        p_fert_object = Fert.query.filter_by(name=purchased_fert).first()
        if p_fert_object:
            if current_user.can_purchase(p_fert_object, quantity_bought_f):
                p_fert_object.buy(current_user, quantity_bought_f)
                flash(
                    f"You purchased { p_fert_object.name } for ₹{ quantity_bought_f*p_fert_object.price }", category="success")
            else:
                flash(
                    f"Not enough cash in account to purchase {p_fert_object.name}", category="danger")

        return redirect(url_for('fertilizer_page'))

    if request.method == "GET":
        ferts = Fert.query.all()

        return render_template('fertilizer.html', ferts=ferts, purchase_form_f=purchase_form_f)


@app.route('/alt')
@login_required
def alt_page():
    return render_template('includes/alt.html')


@app.route('/cart')
@login_required
def cart_page():
    # user = User.query.filter_by(username=current_user.username).first()
    temps = Temp.query.all()
    quantity = 0
    items = Item.query.all()
    stemps = Stemp.query.all()
    ferts = Fert.query.all()
    # purchase_form = PurchaseItemForm()
    # if request.method == "POST":
    #   quantity_bought = purchase_form.bquantity.data

    return render_template('cart.html', user=current_user, temps=temps, quantity=quantity, items=items, stemps=stemps, ferts=ferts)

# @app.context_processor
# def context_processor():
#   return dict(quantity_bought = quantity_bought)


@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Tempf.query.get(id)
    quantity = item_to_delete.bought
    user = current_user
    item = Fert.query.filter_by(id=item_to_delete.fertid).first()
    user.budget += float(quantity)*float(item.price)
    item.quantity += float(1)*float(quantity)
    db.session.delete(item_to_delete)
    db.session.commit()
    flash(f"The chosen item was returned. The balance is added to your account")
    return redirect('/cart')


@app.route('/dfruit/<int:id>')
def dfruit(id):
    item_to_delete = Temp.query.get(id)
    quantity = item_to_delete.bought
    user = current_user
    item = Item.query.filter_by(id=item_to_delete.itemid).first()
    user.budget += float(quantity)*float(item.price)
    item.quantity += float(1)*float(quantity)
    db.session.delete(item_to_delete)
    db.session.commit()
    flash(f"The chosen item was returned. The balance is added to your account", category="info")
    return redirect('/cart')


@app.route('/cancel/<int:id>')
def cancel(id):
    item_to_cancel = Stemp.query.get(id)
    quantity = item_to_cancel.sold
    user = current_user
    item = Item.query.filter_by(id=item_to_cancel.itemid).first()
    user.budget -= float(quantity)*float(item.price)
    item.quantity -= float(1)*float(quantity)
    db.session.delete(item_to_cancel)
    db.session.commit()
    flash(f"The chosen item was returned. The balance is added to your account", category="info")
    return redirect('/cart')


@app.route('/blog')
def blog_page():
    return render_template('blog.html')


@app.route('/base')
def base_page():
    return render_template('base.html')
