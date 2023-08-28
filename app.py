from flask import Flask, request, jsonify
import psycopg2
app = Flask(__name__)

# Database configuration
db_connection = psycopg2.connect(
    dbname="your_db_name",
    user="your_db_user",
    password="your_db_password",
    host="localhost"
)

@app.route('/')
def hello():
    return 'Hello, Flask!'

@app.route('/get', methods=['GET'])
def get_string():
    return jsonify({"Hello": "World"})

@app.route('/about')
def about():
    return 'This is the about page'

@app.route('/contact')
def contact():
    return 'This is the contact page'

if __name__ == '__main__':
    app.run(debug=True)


#get and post from database example
# @app.route('/products', methods=['GET', 'POST'])
# def products():
#     if request.method == 'GET':
#         try:
#             cursor = db_connection.cursor()
#             query = "SELECT * FROM products;"
#             cursor.execute(query)
#             products = cursor.fetchall()

#             product_list = []
#             for product in products:
#                 product_dict = {
#                     "id": product[0],
#                     "name": product[1],
#                     "price": product[2],
#                     # Add more columns as needed
#                 }
#                 product_list.append(product_dict)

#             cursor.close()

#             return jsonify({"products": product_list})

#         except Exception as e:
#             return jsonify({"error": str(e)})

#     elif request.method == 'POST':
#         try:
#             data = request.json
#             name = data.get("name")
#             price = data.get("price")

#             cursor = db_connection.cursor()
#             query = "INSERT INTO products (name, price) VALUES (%s, %s);"
#             cursor.execute(query, (name, price))
#             db_connection.commit()
#             cursor.close()

#             return jsonify({"message": "Product added successfully!"})

#         except Exception as e:
#             return jsonify({"error": str(e)})