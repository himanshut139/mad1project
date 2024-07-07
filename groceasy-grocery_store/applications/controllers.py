import os
from flask import render_template, redirect, url_for, request, session, flash
from datetime import date, datetime
from flask import current_app as app
from applications.database import db
from applications.data import User, Category, Product, Order 
import json                                           # json is for convering dictionary into string and vice versa

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("home.html") 

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method=='POST':
        user_name=request.form['username']
        pwd=request.form['password']

        if user_name not in [x.name for x in User.query.all()]:
            user=User(name=user_name, password=pwd, role="user")
            db.session.add(user)
            db.session.commit()
            session['user']=user_name
            session['cart'] = json.dumps(dict())
            return render_template('login.html', error="Successfully Signed Up!")
        return render_template('login.html', error="User already exists!")
    return render_template('signup.html')

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        username=request.form['username']
        pwd=request.form['password']

        try:
            user=User.query.filter(User.name==username, User.password==pwd, User.role=="user").one()
        except:
            return render_template('login.html', error='Incorrect Username or Password')
        session["user"]=username
        session["cart"] = json.dumps(dict())
        return redirect("user="+username+"/user/dashboard")
        
@app.route("/admin/login", methods=['GET','POST'])
def admin_login():
    if request.method == 'GET':
        return render_template("admin_login.html")
    if request.method == 'POST':
        username=request.form['user_name']
        pwd=request.form['password']
        try:
            user=User.query.filter(User.name==username, User.password==pwd, User.role=='admin').one()
        except:
            return render_template('admin_login.html', error='Incorrect username or Password for Admin')
        session["user"]=username
        return redirect("/admin/dashboard")
    
@app.route('/logout')
def logout():
    if "user" in session:
        session.pop("user", None)
        return render_template('login.html', error='Successfully logged out.')
    return redirect(url_for("home"))

@app.route("/admin/dashboard")
def admin_dashboard():
    try:
        user=session['user']
    except:
        return render_template('admin_login.html', error='You are not authorized to view this page. Please login first.')
    user_role = User.query.filter_by(name=user).first().role
    if user and user_role=='admin':
        return render_template("admin_dashboard.html", error="Hey there, admin! We missed you and are overjoyed to see you back!") 
    else:
        session.pop("user", None)
        flash("User logged out")
        return render_template('admin_login.html', error='You are not admin. Please login as admin.')
    
@app.route('/create/category', methods=['GET', 'POST'])
def create_category():
    try:
        user=session['user']
    except:
        return render_template('admin_login.html', error='You are not authorized to view this page. Please login first.')
    user_role = User.query.filter_by(name=user).first().role
    if user and user_role=='admin':
        if request.method=='POST':
            c_name=request.form['c_name']

            if Category.query.filter_by(name=c_name).first():
                all_categories=Category.query.all()
                return render_template('view_categories.html',all=all_categories, error="Category already exists.")
            else:
                cat=Category(name=c_name)

                db.session.add(cat)
                db.session.commit()
                return redirect('/categories')
        return render_template('create_category.html')
    else:
        session.pop("user", None)
        flash("User logged out")
        return render_template('admin_login.html', error='You are not admin. Please login as admin.')

@app.route("/categories")
def view_categories():
    try:
        user=session['user']
    except:
        return render_template('admin_login.html', error='You are not authorized to view this page. Please login first.')
    user_role = User.query.filter_by(name=user).first().role
    if user and user_role=='admin':
        all_categories=Category.query.all()
        return render_template("view_categories.html", all=all_categories) 
    else:
        session.pop("user", None)
        return render_template('admin_login.html', error='You are not admin. Please login as admin.')

@app.route('/add/product', methods=['GET','POST'])
def add_product():
    try:
        user=session['user']
    except:
        return render_template('admin_login.html', error='You are not authorized to view this page. Please login first.')
    user_role = User.query.filter_by(name=user).first().role
    all_categories=Category.query.all()
    if user and user_role=='admin':
        if request.method=='POST':
            p_name=request.form['prod_name']
            ex_date=request.form['expiry_date']
            rate_p_unit=request.form['unit_rate']
            avl_qnt=request.form['qnt_avl']
            ex_date=datetime.strptime(ex_date,"%Y-%m-%d")
            
            cat_name=request.form['cat']
            category_id=Category.query.filter_by(name=cat_name).first().id
            file=request.files['file']
            
            if(Product.query.filter_by(name=p_name).first()):
                products=Product.query.all()
                return render_template("view_products.html", all=products, error="Product already exists.")
            else:         
                prdct=Product(name=p_name, exp_date=ex_date, rate_per_unit=rate_p_unit, qnt_avl=avl_qnt, cat_id=category_id)
                db.session.add(prdct)
                db.session.commit()
                if file and allowed_file(file.filename):
                    filename = file.filename
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(prdct.id)+'.jpg'))
                return redirect(url_for("view_products"))
        return render_template("add_product.html", categories=all_categories)
    else:
        session.pop("user", None)
        return render_template('admin_login.html', error='You are not admin. Please login as admin.')


    # return render_template('add_product.html')

@app.route('/c_id=<category_id>/add/product', methods=['GET','POST'])
def add_product_from_category(category_id):
    try:
        user=session['user']
    except:
        return render_template('admin_login.html', error='You are not authorized to view this page. Please login first.')
    user_role = User.query.filter_by(name=user).first().role
    all_categories=Category.query.all()
    if user and user_role=='admin':
        if request.method=='POST':
            p_name=request.form['prod_name']
            ex_date=request.form['expiry_date']
            rate_p_unit=request.form['unit_rate']
            avl_qnt=request.form['qnt_avl']
            datetime.strptime(ex_date,"%Y-%m-%d")
            
            cat_name=request.form['cat']
            category_id=Category.query.filter_by(name=cat_name).first().id

            if(Product.query.filter_by(name=p_name).first()):
                products=Product.query.all()
                return render_template("view_products.html", all=products, error="Product already exists.")
            else:
                prdct=Product(name=p_name, exp_date=ex_date, rate_per_unit=rate_p_unit, qnt_avl=avl_qnt, cat_id=category_id)
                db.session.add(prdct)
                db.session.commit()
                return redirect(url_for("view_products"))
        return render_template("add_product.html", categories=all_categories)
    else:
        session.pop("user", None)
        return render_template('admin_login.html', error='You are not admin. Please login as admin.')


@app.route("/view/products")
def view_products():      #THIS ONE IS FOR ADMIN
    try:
        user=session['user']
    except:
        return render_template('admin_login.html', error='You are not authorized to view this page. Please login first.')
    user_role = User.query.filter_by(name=user).first().role
    if user and user_role=='admin':
        all_products=Product.query.all()
        return render_template("view_products.html", all=all_products) 
    else:
        session.pop("user", None)
        return render_template('admin_login.html', error='You are not admin. Please login as admin.')


@app.route('/c_id=<category_id>/delete/category')
def delete_category(category_id):
    try:
        user=session['user']
    except:
        return render_template('admin_login.html', error='You are not authorized to view this page. Please login first.')
    user_role = User.query.filter_by(name=user).first().role
    if user and user_role=='admin':
        cat = Category.query.filter_by(id=category_id).first()
        try:
            db.session.delete(cat)
            db.session.commit()
            return redirect("/categories")
        except:
            return render_template("admin_dashboard.html", error="The category contains products so it cannot be deleted.")
    else:
        session.pop("user", None)
        return render_template('admin_login.html', error='You are not admin. Please login as admin.')


@app.route('/p_id=<product_id>/delete/product')
def delete_product(product_id):
    try:
        user=session['user']
    except:
        return render_template('admin_login.html', error='You are not authorized to view this page. Please login first.')
    user_role = User.query.filter_by(name=user).first().role
    if user and user_role=='admin':
        prdct = Product.query.filter_by(id=product_id).first()
        db.session.delete(prdct)
        db.session.commit()
        return redirect("/view/products")
    else:
        session.pop("user", None)
        return render_template('admin_login.html', error='You are not admin. Please login as admin.')

@app.route('/c_id=<category_id>/update/category', methods=['GET','POST'])
def update_category(category_id):
    cat = Category.query.filter_by(id=category_id).first()
    try:
        user=session['user']
    except:
        return render_template('admin_login.html', error='You are not authorized to view this page. Please login first.')
    user_role = User.query.filter_by(name=user).first().role
    if user and user_role=='admin':
        if request.method=="POST":
            new_name=request.form["newname"]

                
            # if new_name!=cat.name:
            cat.name=new_name
            db.session.commit()
            return redirect("/categories")
        return render_template('update_category.html', id=category_id)
        # return 'Only admin can access this.'
    else:
        session.pop("user", None)
        return render_template('admin_login.html', error='You are not admin. Please login as admin.')

@app.route('/p_id=<product_id>/update/product', methods=['GET','POST'])
def update_product(product_id):
    #You cannot change the category of a product after it is added
    prdct = Product.query.filter_by(id=product_id).first()
    try:
        user=session['user']
    except:
        return render_template('admin_login.html', error='You are not authorized to view this page. Please login first.')
    user_role = User.query.filter_by(name=user).first().role
    if user and user_role=='admin':
        if request.method=="POST":
            new_name=request.form["newname"]
            new_exp=request.form["newexp"]
            new_rate=request.form["newrpu"]
            new_avl_qnt=request.form["newqntavl"]

            if new_name!='' and new_name!=prdct.name:
                prdct.name=new_name
            if new_exp!='' and new_exp!=prdct.exp_date:
                prdct.exp_date=new_exp
            if new_rate!='' and new_rate!=prdct.rate_per_unit:
                prdct.rate_per_unit=new_rate
            if new_avl_qnt!='' and new_exp!=prdct.qnt_avl:
                prdct.qnt_avl=new_avl_qnt
            db.session.commit()
            return redirect("/view/products")
        return render_template('update_product.html', id=product_id)
        # return 'Only admin can access this.'
    else:
        session.pop("user", None)
        return render_template('admin_login.html', error='You are not admin. Please login as admin.')

@app.route('/user=<username>/user/dashboard', methods=['GET','POST'])
def user_dashboard(username):
    if "user" in session and username==session["user"]:
        Name=username.capitalize()
        
        if request.method=='GET':   
            
            q = request.args.get('searched')
            if q:
                all_products = Product.query.filter(Product.name.like("%"+q+"%")).all()   
                if not all_products:
                    category = Category.query.filter(Category.name.like("%"+q+"%")).all()
                    all_products = Product.query.filter_by(cat_id=category[0].id)
                return render_template('result.html', user=Name, products=all_products, error="Products that matches your search:")
            else:
                all_categories=Category.query.all()
            return render_template('user_dashboard.html', user=Name, categories=all_categories)
        else:
            p_id=request.form["product_id"]
            count=request.form["count"]
            product=Product.query.filter_by(id=p_id).first()
            all_products=Product.query.all()

            cart=json.loads(session["cart"])
            if p_id not in cart:
                current=int(count)
                if current <= int(product.qnt_avl):
                    cart[p_id]=count
                else:
                    all_categories=Category.query.all()
                    return render_template('user_dashboard.html', user=Name, categories=all_categories, error="Selected quantity for the product is not available.")
            else:
                current = int(count) + int(cart[p_id])
                if current <= int(product.qnt_avl):
                    cart[p_id]=str(int(cart[p_id]) + int(count))
                else:
                    all_categories=Category.query.all()
                    return render_template('user_dashboard.html', user=Name, categories=all_categories, error="Selected quantity for the product is not available.")

            session['cart'] = json.dumps(cart)
            return redirect('/cart')
    else:
        return render_template('login.html', error="Please login first.")

@app.route("/cart", methods = ["GET", "POST"])
def cart():
    if "user" in session:
        username=session["user"]
        cart = json.loads(session["cart"])
        user = User.query.filter_by(name=session["user"]).first()
        products = [[Product.query.filter_by(id=p_id).first(), cart[p_id]] for p_id in cart.keys()]
        order_total=sum([int(Product.query.filter_by(id=p_id).first().rate_per_unit) * int(cart[p_id]) for p_id in cart.keys()])
        Name=username.capitalize()

        if request.method=='GET':
            return render_template("cart.html",user=Name, products = products, total = order_total, link="user="+username+"/user/dashboard")
        else:
            if "remove" in request.form:
                cart.pop(request.form["remove"])
                session["cart"] = json.dumps(cart)
                return redirect("/cart")
            
            else:
                for product, count in products:
                    product.qnt_avl-=int(count)
                    order = Order(product_id=product.id, product_name=product.name, user_id=user.id, amount=order_total)
                    db.session.add(order)
                    db.session.commit()
                session["cart"] = json.dumps(dict())
                return render_template('cart.html',user=Name,link="user="+username+"/user/dashboard", error='Thank You! Order Placed Successfully')
                # return redirect("user="+username+"/user/dashboard")
    else:
        return render_template('login.html', error='You are not authorized to view this page. Please login first.')
