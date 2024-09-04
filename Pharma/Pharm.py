import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Database connection details
db_name = "db1"
db_user = "root"
db_password = "abhi"
db_host = "localhost"

# Establishing database connection
try:
    connection = mysql.connector.connect(
        host=db_host, user=db_user, password=db_password, database=db_name
    )
    cursor = connection.cursor()
except mysql.connector.Error as err:
    print("Error connecting to database:", err)
    exit()

# Main tkinter application
class PharmacyManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management System")

        self.style = ttk.Style()
        self.style.theme_use('clam')  # Choose a theme ('clam', 'alt', 'default', 'classic')

        # Main menu buttons
        customer_button = tk.Button(root, text="Customer Management", command=self.customer_management)
        customer_button.pack(pady=10)

        prescription_button = tk.Button(root, text="Prescription Management", command=self.prescription_management)
        prescription_button.pack(pady=10)

        medicine_button = tk.Button(root, text="Medicine Management", command=self.medicine_management)
        medicine_button.pack(pady=10)

        order_button = tk.Button(root, text="Order Management", command=self.order_management)
        order_button.pack(pady=10)

        exit_button = tk.Button(root, text="Exit", command=root.quit)
        exit_button.pack(pady=10)

    def customer_management(self):
        # Create customer management window
        self.customer_window = tk.Toplevel(self.root)
        self.customer_window.title("Customer Management")

        # Customer management buttons
        add_customer_button = tk.Button(self.customer_window, text="Add Customer", command=self.add_customer)
        add_customer_button.pack(pady=10)

        view_customer_button = tk.Button(self.customer_window, text="View Customer Details", command=self.view_customer)
        view_customer_button.pack(pady=10)

        update_customer_button = tk.Button(self.customer_window, text="Update Customer Details", command=self.update_customer)
        update_customer_button.pack(pady=10)

        delete_customer_button = tk.Button(self.customer_window, text="Delete Customer", command=self.delete_customer)
        delete_customer_button.pack(pady=10)

    def add_customer(self):
        # Create add customer window
        self.add_customer_window = tk.Toplevel(self.customer_window)
        self.add_customer_window.title("Add Customer")

        # Labels and Entry fields
        tk.Label(self.add_customer_window, text="SSN:").grid(row=0, column=0)
        self.ssn_entry = tk.Entry(self.add_customer_window)
        self.ssn_entry.grid(row=0, column=1)

        tk.Label(self.add_customer_window, text="Name:").grid(row=1, column=0)
        self.name_entry = tk.Entry(self.add_customer_window)
        self.name_entry.grid(row=1, column=1)

        tk.Label(self.add_customer_window, text="Date of Birth (YYYY-MM-DD):").grid(row=2, column=0)
        self.dob_entry = tk.Entry(self.add_customer_window)
        self.dob_entry.grid(row=2, column=1)

        tk.Label(self.add_customer_window, text="Phone Number:").grid(row=3, column=0)
        self.phone_entry = tk.Entry(self.add_customer_window)
        self.phone_entry.grid(row=3, column=1)

        tk.Label(self.add_customer_window, text="Address:").grid(row=4, column=0)
        self.address_entry = tk.Entry(self.add_customer_window)
        self.address_entry.grid(row=4, column=1)

        tk.Label(self.add_customer_window, text="Gender (M/F):").grid(row=5, column=0)
        self.gender_entry = tk.Entry(self.add_customer_window)
        self.gender_entry.grid(row=5, column=1)

        # Submit button
        submit_button = tk.Button(self.add_customer_window, text="Add Customer", command=self.submit_add_customer)
        submit_button.grid(row=6, columnspan=2, pady=10)

    def submit_add_customer(self):
        # Get values from entry fields
        ssn = self.ssn_entry.get()
        name = self.name_entry.get()
        dob = self.dob_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        gender = self.gender_entry.get()

        # Insert into database
        sql = """
            INSERT INTO customer (ssn, name, dob, phone, address, gender)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (ssn, name, dob, phone, address, gender)
        cursor.execute(sql, values)
        connection.commit()

        # Show success message
        messagebox.showinfo("Success", "Customer added successfully!")

        # Clear entry fields
        self.ssn_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.gender_entry.delete(0, tk.END)

    def view_customer(self):
        # Create view customer window
        self.view_customer_window = tk.Toplevel(self.customer_window)
        self.view_customer_window.title("View Customer Details")

        # Labels and Entry field for SSN
        tk.Label(self.view_customer_window, text="Enter SSN:").grid(row=0, column=0)
        self.view_ssn_entry = tk.Entry(self.view_customer_window)
        self.view_ssn_entry.grid(row=0, column=1)

        # Submit button
        submit_button = tk.Button(self.view_customer_window, text="View Details", command=self.submit_view_customer)
        submit_button.grid(row=1, columnspan=2, pady=10)

        # Result area
        self.result_text = tk.Text(self.view_customer_window, height=10, width=50)
        self.result_text.grid(row=2, columnspan=2, pady=10)

    def submit_view_customer(self):
        # Get SSN from entry field
        ssn = self.view_ssn_entry.get()

        # Query database
        sql = """
            SELECT * FROM customer
            WHERE ssn = %s
        """
        cursor.execute(sql, (ssn,))
        customer = cursor.fetchone()

        # Display customer details if found
        if customer:
            details = (
                f"SSN: {customer[0]}\n"
                f"Name: {customer[1]}\n"
                f"DOB: {customer[2]}\n"
                f"Phone: {customer[3]}\n"
                f"Address: {customer[4]}\n"
                f"Gender: {customer[5]}\n"
            )
            self.result_text.delete(1.0, tk.END)  # Clear previous text
            self.result_text.insert(tk.END, details)
        else:
            messagebox.showerror("Error", "Customer not found!")

    def update_customer(self):
        # Create update customer window
        self.update_customer_window = tk.Toplevel(self.customer_window)
        self.update_customer_window.title("Update Customer Details")

        # Labels and Entry fields
        tk.Label(self.update_customer_window, text="Enter SSN:").grid(row=0, column=0)
        self.update_ssn_entry = tk.Entry(self.update_customer_window)
        self.update_ssn_entry.grid(row=0, column=1)

        tk.Label(self.update_customer_window, text="What do you want to update? (name/dob/phone/address/gender):").grid(row=1, column=0)
        self.update_choice_entry = tk.Entry(self.update_customer_window)
        self.update_choice_entry.grid(row=1, column=1)

        tk.Label(self.update_customer_window, text="Enter new value:").grid(row=2, column=0)
        self.update_value_entry = tk.Entry(self.update_customer_window)
        self.update_value_entry.grid(row=2, column=1)

        # Submit button
        submit_button = tk.Button(self.update_customer_window, text="Update", command=self.submit_update_customer)
        submit_button.grid(row=3, columnspan=2, pady=10)

    def submit_update_customer(self):
        # Get values from entry fields
        ssn = self.update_ssn_entry.get()
        choice = self.update_choice_entry.get()
        new_value = self.update_value_entry.get()

        # Check if customer exists
        sql_check_customer = "SELECT * FROM customer WHERE ssn = %s"
        cursor.execute(sql_check_customer, (ssn,))
        customer = cursor.fetchone()

        if customer:
            # Update customer information
            if choice == "name":
                sql_update = "UPDATE customer SET name = %s WHERE ssn = %s"
            elif choice == "dob":
                sql_update = "UPDATE customer SET dob = %s WHERE ssn = %s"
            elif choice == "phone":
                sql_update = "UPDATE customer SET phone = %s WHERE ssn = %s"
            elif choice == "address":
                sql_update = "UPDATE customer SET address = %s WHERE ssn = %s"
            elif choice == "gender":
                sql_update = "UPDATE customer SET gender = %s WHERE ssn = %s"
            else:
                messagebox.showerror("Error", "Invalid choice!")
                return

            cursor.execute(sql_update, (new_value, ssn))
            connection.commit()

            messagebox.showinfo("Success", "Customer information updated successfully!")
        else:
            messagebox.showerror("Error", "Customer not found!")

    def delete_customer(self):
        # Create delete customer window
        self.delete_customer_window = tk.Toplevel(self.customer_window)
        self.delete_customer_window.title("Delete Customer")

        # Labels and Entry field for SSN
        tk.Label(self.delete_customer_window, text="Enter SSN:").grid(row=0, column=0)
        self.delete_ssn_entry = tk.Entry(self.delete_customer_window)
        self.delete_ssn_entry.grid(row=0, column=1)

        # Submit button
        submit_button = tk.Button(self.delete_customer_window, text="Delete", command=self.submit_delete_customer)
        submit_button.grid(row=1, columnspan=2, pady=10)

    def submit_delete_customer(self):
        # Get SSN from entry field
        ssn = self.delete_ssn_entry.get()

        # Check if customer exists
        sql_check_customer = "SELECT * FROM customer WHERE ssn = %s"
        cursor.execute(sql_check_customer, (ssn,))
        customer = cursor.fetchone()

        if customer:
            # Delete customer
            sql_delete = "DELETE FROM customer WHERE ssn = %s"
            cursor.execute(sql_delete, (ssn,))
            connection.commit()

            messagebox.showinfo("Success", "Customer deleted successfully!")
        else:
            messagebox.showerror("Error", "Customer not found!")

    def prescription_management(self):
        # Create prescription management window
        self.prescription_window = tk.Toplevel(self.root)
        self.prescription_window.title("Prescription Management")

        # Prescription management buttons
        add_prescription_button = tk.Button(self.prescription_window, text="Add Prescription", command=self.add_prescription)
        add_prescription_button.pack(pady=10)

        view_prescription_button = tk.Button(self.prescription_window, text="View Prescription Details", command=self.view_prescription)
        view_prescription_button.pack(pady=10)

    def add_prescription(self):
        # Create add prescription window
        self.add_prescription_window = tk.Toplevel(self.prescription_window)
        self.add_prescription_window.title("Add Prescription")

        # Labels and Entry fields
        tk.Label(self.add_prescription_window, text="Prescription ID:").grid(row=0, column=0)
        self.prescription_id_entry = tk.Entry(self.add_prescription_window)
        self.prescription_id_entry.grid(row=0, column=1)

        tk.Label(self.add_prescription_window, text="Customer SSN:").grid(row=1, column=0)
        self.prescription_ssn_entry = tk.Entry(self.add_prescription_window)
        self.prescription_ssn_entry.grid(row=1, column=1)

        tk.Label(self.add_prescription_window, text="Medicine Name:").grid(row=2, column=0)
        self.medicine_name_entry = tk.Entry(self.add_prescription_window)
        self.medicine_name_entry.grid(row=2, column=1)

        tk.Label(self.add_prescription_window, text="Dosage (mg):").grid(row=3, column=0)
        self.dosage_entry = tk.Entry(self.add_prescription_window)
        self.dosage_entry.grid(row=3, column=1)

        tk.Label(self.add_prescription_window, text="Instructions:").grid(row=4, column=0)
        self.instructions_entry = tk.Entry(self.add_prescription_window)
        self.instructions_entry.grid(row=4, column=1)

        # Submit button
        submit_button = tk.Button(self.add_prescription_window, text="Add Prescription", command=self.submit_add_prescription)
        submit_button.grid(row=5, columnspan=2, pady=10)

    def submit_add_prescription(self):
        # Get values from entry fields
        prescription_id = self.prescription_id_entry.get()
        ssn = self.prescription_ssn_entry.get()
        medicine_name = self.medicine_name_entry.get()
        dosage = self.dosage_entry.get()
        instructions = self.instructions_entry.get()

        # Fetch medicine_id based on medicine_name
        sql_fetch_medicine_id = "SELECT medicine_id FROM medicine WHERE medicine_name = %s"
        cursor.execute(sql_fetch_medicine_id, (medicine_name,))
        result = cursor.fetchone()
        if result:
            medicine_id = result[0]
        else:
            messagebox.showerror("Error", f"Medicine '{medicine_name}' not found!")
            return

        # Insert into database
        sql = """
            INSERT INTO prescription (prescription_id, ssn, medicine_id, dosage, instructions)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (prescription_id, ssn, medicine_id, dosage, instructions)
        cursor.execute(sql, values)
        connection.commit()

        # Show success message
        messagebox.showinfo("Success", "Prescription added successfully!")

        # Clear entry fields
        self.prescription_id_entry.delete(0, tk.END)
        self.prescription_ssn_entry.delete(0, tk.END)
        self.medicine_name_entry.delete(0, tk.END)
        self.dosage_entry.delete(0, tk.END)
        self.instructions_entry.delete(0, tk.END)


    def view_prescription(self):
        # Create view prescription window
        self.view_prescription_window = tk.Toplevel(self.prescription_window)
        self.view_prescription_window.title("View Prescription Details")

        # Labels and Entry field for Prescription ID
        tk.Label(self.view_prescription_window, text="Enter Prescription ID:").grid(row=0, column=0)
        self.view_prescription_id_entry = tk.Entry(self.view_prescription_window)
        self.view_prescription_id_entry.grid(row=0, column=1)

        # Submit button
        submit_button = tk.Button(self.view_prescription_window, text="View Details", command=self.submit_view_prescription)
        submit_button.grid(row=1, columnspan=2, pady=10)

        # Result area
        self.result_text_prescription = tk.Text(self.view_prescription_window, height=10, width=50)
        self.result_text_prescription.grid(row=2, columnspan=2, pady=10)

    def submit_view_prescription(self):
        # Get Prescription ID from entry field
        prescription_id = self.view_prescription_id_entry.get()

        # Query database
        sql = """
            SELECT * FROM prescription
            WHERE prescription_id = %s
        """
        cursor.execute(sql, (prescription_id,))
        prescription = cursor.fetchone()

        # Display prescription details if found
        if prescription:
            details = (
                f"Prescription ID: {prescription[0]}\n"
                f"Customer SSN: {prescription[1]}\n"
                f"Medicine ID: {prescription[2]}\n"
                f"Dosage (mg): {prescription[3]}\n"
                f"Instructions: {prescription[4]}\n"
            )
            self.result_text_prescription.delete(1.0, tk.END)  # Clear previous text
            self.result_text_prescription.insert(tk.END, details)
        else:
            messagebox.showerror("Error", "Prescription not found!")

    def medicine_management(self):
        # Create medicine management window
        self.medicine_window = tk.Toplevel(self.root)
        self.medicine_window.title("Medicine Management")

        # Medicine management buttons
        add_medicine_button = tk.Button(self.medicine_window, text="Add Medicine", command=self.add_medicine)
        add_medicine_button.pack(pady=10)

        view_medicine_button = tk.Button(self.medicine_window, text="View Medicine Details", command=self.view_medicine)
        view_medicine_button.pack(pady=10)

    def add_medicine(self):
        # Create add medicine window
        self.add_medicine_window = tk.Toplevel(self.medicine_window)
        self.add_medicine_window.title("Add Medicine")

        # Labels and Entry fields
        tk.Label(self.add_medicine_window, text="Medicine Name:").grid(row=0, column=0)
        self.medicine_name_entry_add = tk.Entry(self.add_medicine_window)
        self.medicine_name_entry_add.grid(row=0, column=1)

        tk.Label(self.add_medicine_window, text="Price:").grid(row=1, column=0)
        self.medicine_price_entry_add = tk.Entry(self.add_medicine_window)
        self.medicine_price_entry_add.grid(row=1, column=1)

        tk.Label(self.add_medicine_window, text="Stock:").grid(row=2, column=0)
        self.medicine_stock_entry_add = tk.Entry(self.add_medicine_window)
        self.medicine_stock_entry_add.grid(row=2, column=1)

        # Submit button
        submit_button = tk.Button(self.add_medicine_window, text="Add Medicine", command=self.submit_add_medicine)
        submit_button.grid(row=3, columnspan=2, pady=10)

    def submit_add_medicine(self):


        # Assuming 'conn' is your MySQL connection and 'cursor' is your cursor object
        medicine_name = self.medicine_name_entry_add.get()
        stock = self.medicine_stock_entry_add.get()
        price = self.medicine_price_entry_add.get()

        # SQL query to insert into the 'medicine' table
        sql = "INSERT INTO medicine (medicine_name, stockqty, price) VALUES (%s, %s, %s)"
        values = (medicine_name, stock, price)

        try:
            cursor.execute(sql, values)
            connection.commit()
            messagebox.showinfo("Success", "Medicine added successfully!")
        except mysql.connector.Error as err:
            connection.rollback()
            messagebox.showerror("Error", f"Error: {err}")

        # Clear entry fields after insertion
        self.medicine_name_entry_add.delete(0, tk.END)
        self.medicine_stock_entry_add.delete(0, tk.END)
        self.medicine_price_entry_add.delete(0, tk.END)



    def view_medicine(self):
        # Create view medicine window
        self.view_medicine_window = tk.Toplevel(self.medicine_window)
        self.view_medicine_window.title("View Medicine Details")

        # Labels and Entry field for Medicine Name
        tk.Label(self.view_medicine_window, text="Enter Medicine Name:").grid(row=0, column=0)
        self.view_medicine_name_entry = tk.Entry(self.view_medicine_window)
        self.view_medicine_name_entry.grid(row=0, column=1)

        # Submit button
        submit_button = tk.Button(self.view_medicine_window, text="View Details", command=self.submit_view_medicine)
        submit_button.grid(row=1, columnspan=2, pady=10)

        # Result area
        self.result_text_medicine = tk.Text(self.view_medicine_window, height=10, width=50)
        self.result_text_medicine.grid(row=2, columnspan=2, pady=10)

    def submit_view_medicine(self):
        # Assuming 'conn' is your MySQL connection and 'cursor' is your cursor object
        medicine_name = self.view_medicine_name_entry.get()

        # SQL query to select from the 'medicine' table
        sql = "SELECT * FROM medicine WHERE medicine_name = %s"

        try:
            cursor.execute(sql, (medicine_name,))
            result = cursor.fetchall()
            if not result:
                messagebox.showwarning("Warning", "No medicine found with that name.")
            else:

                      details = (
                          f"Medicine ID: {result[0][0]}\n"           
                          f"Drug Name: {result[0][1]}\n"              
                          f"Stock: {result[0][2]}\n"               
                          f"Price: {result[0][3]}\n"

                      )
                      self.result_text_medicine.delete(1.0, tk.END)
                      self.result_text_medicine.insert(tk.END, details)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")


    def order_management(self):
        # Create order management window
        self.order_window = tk.Toplevel(self.root)
        self.order_window.title("Order Management")

        # Order management buttons
        create_order_button = tk.Button(self.order_window, text="Create Order", command=self.create_order)
        create_order_button.pack(pady=10)

        view_order_button = tk.Button(self.order_window, text="View Order Details", command=self.view_order)
        view_order_button.pack(pady=10)

    def create_order(self):
        # Create create order window
        self.create_order_window = tk.Toplevel(self.order_window)
        self.create_order_window.title("Create Order")

        # Labels and Entry fields
        tk.Label(self.create_order_window, text="Order ID:").grid(row=0, column=0)
        self.order_id_entry = tk.Entry(self.create_order_window)
        self.order_id_entry.grid(row=0, column=1)

        tk.Label(self.create_order_window, text="Customer SSN:").grid(row=1, column=0)
        self.order_ssn_entry = tk.Entry(self.create_order_window)
        self.order_ssn_entry.grid(row=1, column=1)

        tk.Label(self.create_order_window, text="Medicine Name:").grid(row=2, column=0)
        self.medicine_name_entry_order = tk.Entry(self.create_order_window)
        self.medicine_name_entry_order.grid(row=2, column=1)

        tk.Label(self.create_order_window, text="Quantity:").grid(row=3, column=0)
        self.order_quantity_entry = tk.Entry(self.create_order_window)
        self.order_quantity_entry.grid(row=3, column=1)

        # Submit button
        submit_button = tk.Button(self.create_order_window, text="Create Order", command=self.submit_create_order)
        submit_button.grid(row=4, columnspan=2, pady=10)

    def submit_create_order(self):
        # Get values from entry fields
        order_id = self.order_id_entry.get()
        ssn = self.order_ssn_entry.get()
        medicine_name = self.medicine_name_entry_order.get()
        quantity = self.order_quantity_entry.get()

        # Fetch medicine_id based on medicine_name
        sql_fetch_medicine_id = "SELECT medicine_id FROM medicine WHERE medicine_name = %s"
        cursor.execute(sql_fetch_medicine_id, (medicine_name,))
        result = cursor.fetchone()
        if result:
            medicine_id = result[0]
        else:
            messagebox.showerror("Error", f"Medicine '{medicine_name}' not found!")
            return

        # Insert into database
        sql = """
            INSERT INTO orders (order_id, ssn, medicine_id, quantity)
            VALUES (%s, %s, %s, %s)
        """
        values = (order_id, ssn, medicine_id, quantity)
        cursor.execute(sql, values)
        connection.commit()

        # Show success message
        messagebox.showinfo("Success", "Order created successfully!")

        # Clear entry fields
        self.order_id_entry.delete(0, tk.END)
        self.order_ssn_entry.delete(0, tk.END)
        self.medicine_name_entry_order.delete(0, tk.END)
        self.order_quantity_entry.delete(0, tk.END)


    def view_order(self):
        # Create view order window
        self.view_order_window = tk.Toplevel(self.order_window)
        self.view_order_window.title("View Order Details")

        # Labels and Entry field for Order ID
        tk.Label(self.view_order_window, text="Enter Order ID:").grid(row=0, column=0)
        self.view_order_id_entry = tk.Entry(self.view_order_window)
        self.view_order_id_entry.grid(row=0, column=1)

        # Submit button
        submit_button = tk.Button(self.view_order_window, text="View Details", command=self.submit_view_order)
        submit_button.grid(row=1, columnspan=2, pady=10)

        # Result area
        self.result_text_order = tk.Text(self.view_order_window, height=10, width=50)
        self.result_text_order.grid(row=2, columnspan=2, pady=10)

    def submit_view_order(self):
        # Get Order ID from entry field
        order_id = self.view_order_id_entry.get()

        # Query database
        sql = """
            SELECT * FROM orders
            WHERE order_id = %s
        """
        cursor.execute(sql, (order_id,))
        order = cursor.fetchone()

        # Display order details if found
        if order:
            details = (
                f"Order ID: {order[0]}\n"
                f"Customer SSN: {order[1]}\n"
                f"Medicine ID: {order[2]}\n"
                f"Quantity: {order[3]}\n"
            )
            self.result_text_order.delete(1.0, tk.END)  # Clear previous text
            self.result_text_order.insert(tk.END, details)
        else:
            messagebox.showerror("Error", "Order not found!")


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = PharmacyManagementSystem(root)
    root.mainloop()

# Closing database connection
cursor.close()
connection.close()
