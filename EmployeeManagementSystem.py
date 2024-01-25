import cx_Oracle
import random
import string
from datetime import datetime


dsn = "system/1122@localhost:5439/xe"
# Making Connection
con = cx_Oracle.connect(dsn)


# Function to Generate Employee ID
def generate_employee_id():
    timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"E{timestamp_str}{random_str}"

# Function to Generate Job ID
def generate_job_id():
    timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"J{timestamp_str}{random_str}"

# Function to Add Employee
def Add_Employ():
    # Automatically generate Employee ID
    employee_id = generate_employee_id()

    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")

    # Automatically generate Job ID
    job_id = generate_job_id()

    try:
        # Attempt to convert input to float (numeric)
        salary = float(input("Enter Salary: "))
    except ValueError:
        print("Invalid input for Salary. Please enter a numeric value.")
        menu()
        return

    # Hardcoding some values for simplicity
    email = f'{first_name.lower()}.{last_name.lower()}@gmail.com'


    manager_id = None  # You might have a manager ID or set it to None if not applicable
    department_id = None  # You might have a department ID or set it to None if not applicable

    data = (employee_id, first_name, last_name, email, job_id, salary, manager_id, department_id)

    # Inserting Employee details into the employee Table
    sql = '''
        INSERT INTO employee 
        (employee_id, first_name, last_name, email, job_id, salary, manager_id, department_id) 
        VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
    '''

    c = con.cursor()

    try:
        # Executing the SQL Query
        c.execute(sql, data)

        # commit() method to make changes in the table
        con.commit()
        print("Employee Added Successfully ")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print("Error:", error)
    finally:
        c.close()

    menu()

# Function to Promote Employee
def Promote_Employee():
    employee_id = input("Enter Employee's ID: ")

    # Checking if Employee with given ID Exists or Not
    if not check_employee(employee_id):
        print("Employee with ID {} does not exist\nTry Again\n".format(employee_id))
        menu()
    else:
        amount = float(input("Enter increase in Salary: "))

        # Query to Fetch Salary of Employee with given ID
        sql = 'SELECT salary FROM employee WHERE employee_id = :1'
        data = (employee_id,)
        c = con.cursor()

        # Executing the SQL Query
        c.execute(sql, data)

        # Fetching Salary of Employee with given ID
        current_salary = c.fetchone()[0]
        new_salary = current_salary + amount

        # Query to Update Salary of Employee with given ID
        sql = 'UPDATE employee SET salary = :1 WHERE employee_id = :2'
        updated_data = (new_salary, employee_id)

        # Executing the SQL Query
        c.execute(sql, updated_data)

        # commit() method to make changes in the table
        con.commit()
        print("Employee Promoted")
        menu()

# Function to Remove Employee with given ID
def Remove_Employ():
    employee_id = input("Enter Employee ID: ")

    # Checking if Employee with given ID Exists or Not
    if not check_employee(employee_id):
        print("Employee with ID {} does not exist\nTry Again\n".format(employee_id))
        menu()
    else:
        # Query to Delete Employee from Table
        sql = 'DELETE FROM employee WHERE employee_id = :1'
        data = (employee_id,)
        c = con.cursor()

        # Executing the SQL Query
        c.execute(sql, data)

        # commit() method to make changes in 
        # the table
        con.commit()
        print("Employee Removed")
        menu()

# Function To Check if Employee with
# given ID Exists or Not
def check_employee(employee_id):
    # Query to select all Rows from
    # employee Table
    sql = 'SELECT 1 FROM employee WHERE employee_id = :1'

    # Creating a cursor
    c = con.cursor()

    # Executing the SQL Query
    c.execute(sql, (employee_id,))

    # Fetching the result
    result = c.fetchone()

    return result is not None

# Function to Display All Employees
# from employee Table
def Display_Employees():
    # query to select all rows from 
    # employee Table
    sql = 'SELECT * FROM employee'
    c = con.cursor()

    try:
        # Executing the SQL Query
        c.execute(sql)

        # Fetching all details of all the
        # Employees
        rows = c.fetchall()
        for row in rows:
            print("Employee ID : ", row[0])
            print("First Name : ", row[1])
            print("Last Name : ", row[2])
            print("Email : ", row[3])
            print("Phone Number : ", row[4])
            print("Job ID : ", row[5])
            print("Salary : ", row[6])
            print("Manager ID : ", row[7])
            print("Department ID : ", row[8])
            print("---------------------\
            -----------------------------\
            ------------------------------\
            ---------------------")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print("Error:", error)
    finally:
        c.close()

    menu()

# menu function to display menu
def menu():
    print("Welcome to Employee Management Record")
    print("Press ")
    print("1 to Add Employee")
    print("2 to Remove Employee ")
    print("3 to Promote Employee")
    print("4 to Display Employees")
    print("5 to Exit")

    ch = int(input("Enter your Choice "))
    if ch == 1:
        Add_Employ()
    elif ch == 2:
        Remove_Employ()
    elif ch == 3:    
        Promote_Employee()
    elif ch == 4:
        Display_Employees()
    elif ch == 5:
        exit(0)
    else:
        print("Invalid Choice")
        menu()

# Calling menu function
menu()
