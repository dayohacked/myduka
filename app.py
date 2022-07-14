# import flask Class
# from dbm import _Database
# from crypt import methods
from cProfile import label
from datetime import datetime
from flask import Flask, redirect, render_template, request, url_for
import psycopg2
from datetime import datetime


# we create an object/variable tha will be used to access the methods
# we add the _name_ argument so as to pass the context of the app
app = Flask( __name__ )
conn=psycopg2.connect(user="postgres",host="localhost", password="",database="myduka",port="5432")
# print(conn)
db =conn.cursor()


# Add a declaration to define the route
# Every route attached to a function
# And this is where all logic isprocessed
# home route
@app.route("/")
def home():
    # jina = "Felix"
    # print(jina)
   
    # return the template to be rendered here-html file
    # the html files should be placed in a folder called templates
    return render_template("index.html")

    # invetory route
@app.route("/inventory")
def inventory():
    db.execute("SELECT * FROM products;")
    items= db.fetchall()
    # print(items)
    # shoppinglist = ["tea","Books", 2, "data"]
    # for item in shoppinglist:
    #      print(item)

    return render_template("inventory.html", products=items)

@app.route("/sales")
def sales():
    db.execute("SELECT * FROM sales;")
    sales= db.fetchall()
    # print(sales)
    # shoppinglist = ["tea","Books", 2, "data"]
    # for item in shoppinglist:
    #      print(item)
    return render_template("sales.html", moved=sales)

@app.route("/add_product", methods=["POST"])
# add method to show how it gets data
def add_product():
    productname= request.form["product_name"]
    buyingprice= request.form["buying_price"]
    sellingprice= request.form["selling_price"]
    quantity= request.form["quantity"]
    # category=request.form["category"]
    print(productname, buyingprice,sellingprice,quantity)
    db.execute("INSERT INTO products (name,buying_price,selling_price,quantity) VALUES (%s,%s,%s,%s)",(productname, buyingprice,sellingprice,quantity))
    conn.commit()
    
    # use the redirect to make sure the user stays in teh same page
    # url for is used to call the function of the page to redirect to
    # you can use /add_product in the form action o html file or {{ url_for('add_product') }}"
    return redirect(url_for("inventory"))
    
@app.route("/dashboard")
def Dashboard():
    # Display every product Vs Total sales
    # Fetch the data using psycopg2 cur
    db.execute("SELECT products.name,sum(products.selling_price*sales.quantity) as total_sales FROM products INNER JOIN sales ON products.id = sales.pid GROUP BY name order  by total_sales;")
    items= db.fetchall()
    # print(items)
   
    # Use for loop/if statement to create 2 lists, one with the name of the product and the other with the value of the sales
    # Create 2 empty lists to hold the expected graph data
    labels=[]
    data = []
    for i in items:
        labels.append(i[0])
        data.append(float(i[1]))
    # import json
    # labels=json.dumps(labels)
    # data=json.dumps(data)
    # print(labels)
    # print(data)
    # Push to the HTML file

    db.execute("select to_char(sales.created_at,'YYYY-MM') as sales,sum(sales.quantity*products.selling_price) as amount from products join sales on sales.pid=products.id group by sales;")
    amount=db.fetchall()
    print(amount)
    lables1=[]
    data1=[]
    for j in amount:
        lables1.append(j[0])
        data1.append(float(j[1]))
    
    # print(lables1)
    # print(data1)
    # pie chart data
    db.execute("select to_char(created_at,'YYYY') as dates, sum( revenue) from sales group by dates")
    yearly=db.fetchall()
    labels2=[]
    data2=[]
    for k in yearly:
        labels2.append(k[0])
        data2.append(float(k[1]))
    print(labels2)
    print(data2)

    

    return render_template("dashboard.html",labels=labels,data=data, lables1=lables1, data1=data1,labels2=labels2,data2=data2)

# make sales route
@app.route("/make_sale",methods=["GET","POST"])
def make_sale():
    quantity= request.form["quantity"]
    product_id=request.form["productID"]
    created_at = datetime.now()
    category=request.form["category"]
    db.execute ("INSERT INTO Sales (pid, quantity, created_at,category) VALUES (%s, %s, %s,%s)",(product_id,quantity,created_at,category))
    conn.commit()

    print(product_id,quantity,created_at,category)
    return redirect(url_for("sales"))

# delete product rute
@app.route("/delete_product",methods=["GET","POST"])
def delete_product():
    product_id=request.form["productID"]
    print(product_id)
    db.execute("DELETE FROM sales where pid=%s",[product_id])
    conn.commit()
    message="Sale deleted succesfully"
    # return redirect(url_for("inventory"))
    return render_template("test.html",message=message)


@app.route("/view_sale/<int:pid>")
def view_sale(pid):
    # query the sales for that product_id
    print(pid)
    db.execute("SELECT * FROM sales where pid=%s;",[pid])
    rows=db.fetchall()
    
    # we use the same varible name Moved-since its the one we are rendering in the sales template-using jinja
    return render_template ("sales.html", moved = rows) 

@app.route("/stock")
def stock():
    # db.execute("SELECT * FROM products;")
    # items= db.fetchall()
    # print(items)
    # shoppinglist = ["tea","Books", 2, "data"]
    # for item in shoppinglist:
    #      print(item)
    return render_template("stock.html")

# create a graph route


@app.route("/test")
def graphs():
    labels1= []
    data1=[]
    db.execute("select count(revenue),pid from sales group by pid;")
    values= db.fetchall()
    for i in values:
        labels1.append(i[0])
        data1.append(i[1])
    # print(labels1)   
    # print(data1)
    return render_template("test.html", labels1=labels1,data1=data1)


if __name__ == "__main__":
    app.run()
