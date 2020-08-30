import sqlite3
from sqlite3 import Error
from random import randint
from datetime import date

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)

	return conn


database = "./cart"
conn = create_connection(database)
print("+++++++++++++++++++++++++++++++\n")
print("Welcome to online shopping!!\n")
print("Would you like to order??\n\nOptions:\n1->Yes!!\n2->No.Thank you!\n3->Cancel Order\n")
op=input()
#if(op=="1"):
#	print("hello")
if(op=="1"):
	print("Enter your customer id:\n")
	cust_id=input()
	order_id = randint(1000,9999)
	cost=0
	while(True):
		print("Select the product category from below\nID--Category\n")
		## CATEGORY SELECTION
		cur = conn.cursor()
		cur.execute("SELECT * FROM Product_cat")

		rows = cur.fetchall()
		print("============================\n")
		for row in rows:
			for word in row:
				print (word,end=" "),
			#print(row)
			print("\n")
		##
		cat=input()
		print("Here is a list of products available--Select the required product\n\nID-NAME-------Quantity")
		print("========================\n")
		## PRODUCT SELECTION
		cur = conn.cursor()
		cur.execute("SELECT product_id,product_name,quantity from Product where category_id=?",(cat,))
		rows=cur.fetchall()
		for row in rows:
			for word in row:
				print (word,end=" ")
			#print(row)
			print("\n")
		
		##
		prod=input()
		cur.execute("select quantity from Product where product_id=?",(prod))
		avail=cur.fetchall()
		ava=avail[0][0]
		print("Enter the quantity")
		quant=input()
		availup=ava-int(quant)
		cur.execute("update Product set quantity=? where product_id=?",(availup,prod))
		
		cur.execute("select price from product where product_id=?",prod)
		price=cur.fetchone()
		cost=cost + (int(price[0])*int(quant))
		##ADD to datbase
		cur=conn.cursor()
		olid=randint(100000,999999)
		cur.execute("insert into orders values (?,?,?,?,?)",(order_id,cust_id,date.today(),prod,olid,))
		conn.commit()
		print("\n1->Check out? \n2->Do you want to continue shopping??")
		con=input()
		if(con=="1"):
			## update payment id
			cur=conn.cursor()
			pay_id=randint(100000,999999)
			cust=str(cust_id)
			payment_id=pay_id
			cur.execute("SELECT * FROM orders where customer_id = ?",cust)
			rows=cur.fetchall()
			print("order_id-customer_id-Date-Product_id-order_key\n")
			print("================================================\n")
			for row in rows:
				for word in row:
					print (word,end=" ")
				#print(row)
				print("\n")

			#selecting payment option
			print("select payment option")
			print("1.COD")
			print("2.card")
			val =input("Enter here: ")
			#print(val)
			p_option="cod"
			if val==2:
				p_option="card"
			#inserting values in payment table and commit
			cur.execute("INSERT INTO payment values(?,?,?)",(payment_id,p_option,olid))
			#cur.execute("update orders set payment_id=? where customer_id=? and order_id=?",(pay_id,cust_id,order_id,))
			conn.commit()
			conn.close()
			"""mode='BHIM'
			cur.execute("insert into payment values(?,?)",(pay_id,mode,))
			cur.execute("update orders set payment_id=? where customer_id=? and order_id=?",(pay_id,cust_id,order_id,))
			conn.commit()"""
			break;
	print("+++++++++++++++\nTotal cost = "+str(cost))

	

elif(op=="2"):
	##DERECTLY CANCEL WITHOUT ANYTHING
	print("Have a Good Day!!\n")
	print("+++++++++++++++++++\n")
elif op=="3":
	conn.execute("PRAGMA foreign_keys = 1")
	cur=conn.cursor()
	oid=input("enter order id: ")
	print("The cancelled order is:")
	cur.execute("SELECT * FROM orders WHERE order_id = ?",(oid,))
	rows=cur.fetchall()
	for row in rows:
		for word in row:
			print (word,end=" ")
		#print(row)
		print("\n")
	cur.execute("DELETE FROM orders WHERE order_id = ?",(oid,))
	conn.commit()
	conn.close()
