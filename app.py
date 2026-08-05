from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)
from decimal import Decimal

import mysql.connector

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


app = Flask(__name__)

app.secret_key = "departmental_store_secret"


# DATABASE CONNECTION

db = mysql.connector.connect(

    host="localhost",

    user="root",

    password="23ka1a0530@92",

    database="departmental_store"

)


# HOME PAGE

@app.route("/")

def home():

    cursor = db.cursor(
        dictionary=True
    )

    cursor.execute(

        """

        SELECT *

        FROM products

        WHERE stock > 0

        """

    )

    products = cursor.fetchall()

    cursor.close()

    return render_template(

        "products.html",

        products=products

    )


# REGISTER

@app.route(

    "/register",

    methods=["GET", "POST"]

)

def register():

    if request.method == "POST":

        full_name = request.form[
            "full_name"
        ]

        username = request.form[
            "username"
        ]

        password = request.form[
            "password"
        ]


        hashed_password = (

            generate_password_hash(

                password

            )

        )


        cursor = db.cursor()


        try:

            cursor.execute(

                """

                INSERT INTO users

                (

                    full_name,

                    username,

                    password,

                    role

                )

                VALUES

                (

                    %s,

                    %s,

                    %s,

                    'customer'

                )

                """,

                (

                    full_name,

                    username,

                    hashed_password

                )

            )


            db.commit()


            flash(

                "Registration successful. Please login."

            )


            return redirect(

                url_for("login")

            )


        except:

            db.rollback()


            flash(

                "Username already exists."

            )


        finally:

            cursor.close()


    return render_template(

        "register.html"

    )


# LOGIN

@app.route(

    "/login",

    methods=["GET", "POST"]

)

def login():

    if request.method == "POST":

        username = request.form[
            "username"
        ]

        password = request.form[
            "password"
        ]


        cursor = db.cursor(

            dictionary=True

        )


        cursor.execute(

            """

            SELECT *

            FROM users

            WHERE username = %s

            """,

            (username,)

        )


        user = cursor.fetchone()

        cursor.close()


        if user and check_password_hash(

            user["password"],

            password

        ):


            session["user_id"] = (

                user["user_id"]

            )


            session["username"] = (

                user["username"]

            )


            session["role"] = (

                user["role"]

            )


            return redirect(

                url_for(

                    "dashboard"

                )

            )


        flash(

            "Invalid username or password."

        )


    return render_template(

        "login.html"

    )


# LOGOUT

@app.route("/logout")

def logout():

    session.clear()


    return redirect(

        url_for("login")

    )


# DASHBOARD

@app.route("/dashboard")

def dashboard():

    if "user_id" not in session:

        return redirect(

            url_for("login")

        )


    return render_template(

        "dashboard.html"

    )


# ADD PRODUCT

@app.route(

    "/add-product",

    methods=["POST"]

)

def add_product():

    if session.get("role") != "admin":

        return "Access Denied"


    name = request.form["name"]

    price = request.form["price"]

    stock = request.form["stock"]


    cursor = db.cursor()


    cursor.execute(

        """

        INSERT INTO products

        (

            product_name,

            price,

            stock

        )

        VALUES

        (

            %s,

            %s,

            %s

        )

        """,

        (

            name,

            price,

            stock

        )

    )


    db.commit()

    cursor.close()


    flash(

        "Product added successfully."

    )


    return redirect(

        url_for("home")

    )


# ADD PRODUCT TO CART

@app.route(

    "/add-to-cart/<int:product_id>",

    methods=["POST"]

)

def add_to_cart(

    product_id

):

    if "user_id" not in session:

        return redirect(

            url_for("login")

        )


    user_id = session["user_id"]


    cursor = db.cursor(

        dictionary=True

    )


    cursor.execute(

        """

        SELECT *

        FROM products

        WHERE product_id = %s

        """,

        (product_id,)

    )


    product = cursor.fetchone()


    if not product:

        return "Product not found."


    cursor.execute(

        """

        SELECT *

        FROM cart

        WHERE user_id = %s

        AND product_id = %s

        """,

        (

            user_id,

            product_id

        )

    )


    existing_item = (

        cursor.fetchone()

    )


    if existing_item:

        cursor.execute(

            """

            UPDATE cart

            SET quantity = quantity + 1

            WHERE user_id = %s

            AND product_id = %s

            """,

            (

                user_id,

                product_id

            )

        )


    else:

        cursor.execute(

            """

            INSERT INTO cart

            (

                user_id,

                product_id,

                quantity

            )

            VALUES

            (

                %s,

                %s,

                1

            )

            """,

            (

                user_id,

                product_id

            )

        )


    db.commit()

    cursor.close()


    return redirect(

        url_for("home")

    )


# VIEW CART

@app.route("/cart")

def view_cart():

    if "user_id" not in session:

        return redirect(

            url_for("login")

        )


    user_id = session["user_id"]


    cursor = db.cursor(

        dictionary=True

    )


    cursor.execute(

        """

        SELECT

            cart.cart_id,

            products.product_name,

            products.price,

            cart.quantity,

            (

                products.price

                * cart.quantity

            ) AS subtotal

        FROM cart

        JOIN products

        ON

        cart.product_id

        = products.product_id

        WHERE cart.user_id = %s

        """,

        (user_id,)

    )


    cart_items = (

        cursor.fetchall()

    )


    total = sum(
        (
        item["subtotal"]

        for item in cart_items

    ),
        Decimal("0.00")
    )
    gst = total * Decimal("0.05")


    grand_total = (

        total + gst

    )


    cursor.close()


    return render_template(

        "cart.html",

        cart_items=cart_items,

        total=total,

        gst=gst,

        grand_total=grand_total

    )


# REMOVE CART ITEM

@app.route(

    "/remove-cart/<int:cart_id>"

)

def remove_cart_item(

    cart_id

):

    if "user_id" not in session:

        return redirect(

            url_for("login")

        )


    cursor = db.cursor()


    cursor.execute(

        """

        DELETE FROM cart

        WHERE cart_id = %s

        AND user_id = %s

        """,

        (

            cart_id,

            session["user_id"]

        )

    )


    db.commit()

    cursor.close()


    return redirect(

        url_for("view_cart")

    )


# CHECKOUT

@app.route(

    "/checkout",

    methods=["POST"]

)

def checkout():

    if "user_id" not in session:

        return redirect(

            url_for("login")

        )


    user_id = session["user_id"]


    customer_name = request.form[

        "customer_name"

    ]


    phone = request.form[

        "phone"

    ]


    payment_method = request.form[

        "payment_method"

    ]


    cursor = db.cursor(

        dictionary=True

    )


    try:
        
        if db.in_transaction:
          db.rollback()

        db.start_transaction()
        cursor.execute(

            """

            SELECT

                cart.product_id,

                cart.quantity,

                products.product_name,

                products.price,

                products.stock

            FROM cart

            JOIN products

            ON

            cart.product_id

            = products.product_id

            WHERE cart.user_id = %s

            """,

            (user_id,)

        )


        items = cursor.fetchall()


        if len(items) == 0:

            db.rollback()

            return "Cart is empty."


        for item in items:

            if (

                item["quantity"]

                > item["stock"]

            ):

                db.rollback()

                return (

                    "Insufficient stock for "

                    + item["product_name"]

                )


        subtotal = sum(

            item["price"]

            * item["quantity"]

            for item in items

        )


        gst = subtotal * Decimal("0.05")


        grand_total = (

            subtotal + gst

        )


        # ADD CUSTOMER

        cursor.execute(

            """

            INSERT INTO customers

            (

                customer_name,

                phone

            )

            VALUES

            (

                %s,

                %s

            )

            """,

            (

                customer_name,

                phone

            )

        )


        customer_id = (

            cursor.lastrowid

        )


        # CREATE ORDER

        cursor.execute(

            """

            INSERT INTO orders

            (

                customer_id,

                total_amount,

                payment_method

            )

            VALUES

            (

                %s,

                %s,

                %s

            )

            """,

            (

                customer_id,

                grand_total,

                payment_method

            )

        )


        order_id = (

            cursor.lastrowid

        )


        # ADD ORDER ITEMS

        for item in items:

            cursor.execute(

                """

                INSERT INTO order_items

                (

                    order_id,

                    product_id,

                    quantity,

                    price

                )

                VALUES

                (

                    %s,

                    %s,

                    %s,

                    %s

                )

                """,

                (

                    order_id,

                    item["product_id"],

                    item["quantity"],

                    item["price"]

                )

            )


        # DELETE CART

        cursor.execute(

            """

            DELETE FROM cart

            WHERE user_id = %s

            """,

            (user_id,)

        )


        db.commit()


        return render_template(

            "bill.html",

            order_id=order_id,

            customer_name=customer_name,

            phone=phone,

            items=items,

            subtotal=subtotal,

            gst=gst,

            grand_total=grand_total,

            payment_method=payment_method

        )


    except Exception as error:

        db.rollback()

        return (

            "Transaction failed: "

            + str(error)

        )


    finally:

        cursor.close()


if __name__ == "__main__":

    app.run(

        debug=True

    )