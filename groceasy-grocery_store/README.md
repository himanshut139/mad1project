GROCEASY - Groceries at your doorstep!

Description:

Groceasy is a multi-user app that allows users to shop groceries and essential items from the comfort of their homes. The app has various features for the Store manager (admin) such as adding categories, products, deleting them,etc. The features provided to the users are they can shop multiple products from different categories and can search for some specific items.

#--------------------------------------------------------------------------------------------------------------------------------------------------
Technologies Used:

Python: Develop the controllers and serve as the host programming language for the application
HTML: Develop the required web-pages
CSS: Style the web-pages
Bootstrap: To make the frontend appealing and easy to navigate
SQLite: Serves as the database for the application
Flask: Serves as the web-framework for the application
Flask-SQLAlchemy: Used to access and modify the app’s SQLite database
Jinja2: Allows us to build expressive and extensible templates.


#--------------------------------------------------------------------------------------------------------------------------------------------------
Architecture and Features:

The application follows the standard MVC architecture.The Model is created using SQLite.
The View of the application is created using HTML, CSS, and Bootstrap. The Controller is created using Python and Flask.

The features of the application are as follows: 

Signup and Login for users
Login for admin (Store Manager)
Admin can create, view, update, and delete categories
Admin can create, view, update, and delete products
User can view all the products available for a given category
Ability to search specific products, category that includes various products
Navigate and view the user's cart
User can buy many products for one or multiple categories
System will automatically show the latest products added 
Ability to show out of stock for the products that are not available
Ability to show the total amount to be paid for the transaction


#--------------------------------------------------------------------------------------------------------------------------------------------------
Instructions to Run the App:

- Open terminal
- cd into the directory of the project
- Run python app.py
- If an error occurs regarding python dependencies, run pip install -r requirements.txt and then repeat the above step.
- For further details regarding the app, refer to Project Report from the docs folder.

- Default admin credentials:-  Username: admin, Password: abc