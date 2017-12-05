# Main file for Shirts4Mike

# Import statement
from flask import  Flask,render_template,Markup, url_for,request, session, redirect
import model as db
import sqlite3 as sql


import sendgrid
from datetime import date

# App setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "some_really_long_random_string_here"

# Get details for sendgrid details


# Global Variables
products_info = [
    {
        "id": "101",
        "name": "Bolo Shirt",
        "img": "tshirt100.jpg",
        "price": 100,

        "sizes": ["Small", "Medium", "Large"],
        "quantities": [1, 2, 3, 4, 5, 6]
    },

    {
        "id": "102",
        "name": "NoLogo Black Denim Shirt",
        "img": "shirt102.jpg",
        "price": 200,
        "sizes": ["Small", "Medium", "Large"],
        "quantities": [1, 2, 3, 4, 5, 6]
    },

    {
        "id": "103",
        "name": "Bolo Shirt, Blue",
        "img": "shirt-105.jpg",
        "price": 150,

        "sizes": ["Small", "Medium", "Large"],
        "quantities": [1, 2, 3, 4, 5, 6]
    },

    {
        "id": "104",
        "name": "Bolo Shirt,Black",
        "img": "shirt-107.jpg",
        "price":170,

        "sizes": ["Small", "Medium", "Large"],
        "quantities": [1, 2, 3, 4, 5, 6]
    },

    {
        "id": "105",
        "name": "Bolo tshirt, Blue",

        "img": "shirt-103.jpg",
        "price": 180,

        "sizes": ["Small", "Medium", "Large"],
        "quantities": [1, 2, 3, 4, 5, 6]
    },

    {

        "id": "106",
        "name": "Logo Shirt, Gray",
        "img": "shirt106.jpg",
        "price": 110,
        "quantities":[1, 2, 3,4,5,6],
        "sizes": ["Small", "Medium", "Large"]
    },

    {
        "id": "107",
        "name": "Shirt, White",
        "img": "shirt-104.jpg",
        "price": 250,
        "quantities":[1, 2, 3,4,5,6],

        "sizes": ["Small", "Medium", "Large"]
    },

    {
        "id": "108",
        "name": "Shirt, Black",
        "img": "shirt-08.jpg",
        "price": 130,

        "sizes": ["Small", "Medium", "Large"],
        "quantities":[1, 2, 3,4,5,6]

    }
]

# Functions


def get_list_view_html(product):
    """Function to return html for given shirt

    The product argument should be a dictionary in this structure:
    {
        "id": "shirt_id",
        "name": "name_of_shirt",
        "img": "image_name.jpg",
        "price": price_of_shirt_as_int_or_flat,
        "paypal": "paypal_id"
        "sizes": ["array_of_sizes"]
    }

    The html is returned in this structure:
    <li>
      <a href="shirt/shirt_id">
        <img src="/static/shirt_img" alt="shirt_name">
        <p>View Details</p>
      </a>
    </li>
    """
    output = ""
    image_url = url_for("static", filename=product["img"])
    shirt_url = url_for("shirt", product_id=product["id"])
    output = output + "<li>"
    output = output + '<a href="' + shirt_url + '">'
    output = (
        output + '<img src="' + image_url +
        '" al  t="' + product["name"] + '">')
    output = output + "<p>View Details</p>"
    output = output + "</a>"
    output = output + "</li>"

    return output


# Routes
# All functions should have a page_title variables if they render templates

@app.route("/")
def index():
    """Function for Shirts4Mike Homepage"""
    context = {"page_title": "For your shirts", "current_year": date.today().year}
    counter = 0
    product_data = []
    for product in products_info:
        counter += 1
        if counter < 5:  # Get first 4 shirts
            product_data.append(
                Markup(get_list_view_html(product))
            )
    context["product_data"] = Markup("".join(product_data))
    #flash("This site is a demo do not buy anything")
    return render_template("index.html", **context)


@app.route("/shirts")
def shirts():
    """Function for the Shirts Listing Page"""
    context = {"page_title": "Your Designed Shirts", "current_year": date.today().year}
    product_data = []
    for product in products_info:
        product_data.append(Markup(get_list_view_html(product)))
    context["product_data"] = Markup("".join(product_data))
   # flash("This site is a demo do not buy anything")
    return render_template("shirts.html", **context)


@app.route("/shirt/<product_id>")
def shirt(product_id):
    """Function for Individual Shirt Page"""
    context = {"page_title": "Your design ", "current_year": date.today().year}
    # price = request.form['price']
    # print(price)
    my_product = ""
    for product in products_info:
        if product["id"] == product_id:
            my_product = product
    context["product"] = my_product
    #flash("This site is a demo do not buy anything")


    return render_template("shirt.html", **context)


@app.route("/login", methods=['POST', 'GET'])
def login():
    """Function to display receipt after purchase"""
    # context = {"page_title": "Shirts 4 Mike", "current_year": date.today().year}
    # price = int(request.form['price'])
    # quantity = int(request.form['quantity'])
    # total = price * quantity
    message = None


    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if db.userEixts(email) == True:
            if db.getPassword(email) == password:
                user = str(db.getNames(email))
                user = user.lstrip("[(")


                # firsname = user[0]
                # lastname = user[1]
                # userFullname = firsname + " " + lastname
                # print(userFullname)
                # print(user)
                print(user)
                # price = request.form['price']
                # print(price)

                session['email'] = email
                return render_template("receipt.html", user = user, email = email)

    return render_template("login.html", message=message)


@app.route("/contact")
def contact():
    """Function for contact page"""
    context = {"page_title": "Shirts 4 you", "current_year": date.today().year}
    return render_template("contact.html", **context)
@app.route("/receipt", methods=['get', 'post'])
def receipt():
    # price = request.form['price']
    # quantity = request.form['quantity']
    # total = int(price * quantity)
    # print(t)
    return  render_template("receipt.html")



@app.route('/registration', methods=['GET', 'POST'])
def registration():
    messages = []
    if request.method == 'POST':
        firname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        if(db.userEixts(email)) == True:
            messages.append("User with that email "+ email+" already exists")
            messages.append("Please login with your email")
            return render_template("registration.html", messages = messages)

        #print(email)
        else:
            db.insertUser(firname, lastname, email, password)
            firname = firname
            lastname = lastname
            return render_template("congrats.html", firstname = firname, lastname = lastname)
    return render_template("registration.html")



# Run application
if __name__ == "__main__":
    app.run(debug=True)
