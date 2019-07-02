from flask import Flask, render_template, request, redirect, url_for,flash

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/')
@app.route('/hello')
def HelloWorld():
    queryRestuarants = session.query(Restaurant).all()
    output = ''
    for restaurant in queryRestuarants:
        output += restaurant.name
        output += '</br>'

    return output


@app.route('/restaurantMenus/<restaurant_id>')
def restaurantMenu(restaurant_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    queryRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    menu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()

    return render_template('menu.html', restaurant=queryRestaurant, items=menu)


@app.route('/restaurantMenus')
def menuItem():
    restaurant = session.query(Restaurant).all()
    out = ''
    for r in restaurant:
        menuItems = session.query(MenuItem).filter_by(restaurant_id=r.id).all()

        for i in menuItems:
            out += i.name
            out += '</br>'
            out += i.price
            out += '</br>'
            out += i.description
            out += '</br></br>'
    return out


@app.route('/restaurantMenus/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newMenuItem.html', restaurant_id=restaurant_id)


@app.route('/restaurantMenus/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        item.name = request.form['newName']
        session.add(item)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenu.html', restaurant_id=restaurant_id,item=item)


@app.route('/restaurantMenus/<restaurant_id>/<menu_id>/delete/',methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method=='POST':
        if item:
            session.delete(item)
            session.commit()
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html',restaurant_id=restaurant_id,item=item)

if __name__ == '__main__':
    app.secret_key='super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=2121)
