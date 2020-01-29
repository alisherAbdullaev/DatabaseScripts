# imports packages 
import mysql.connector 
from mysql.connector import errorcode


# asksuser to input hostname, user_name, and password
host_name = input("Please enter your DMBS\'s hostname: ")
user_name = input("Please enter your username: ")
password = input("Please enter your password: ")



# tries to conncet the to the server
try:
    connect = mysql.connector.connect(
        host = host_name,
        user = user_name,
        password = password,
        database = user_name
        )

# if there is any error...
except mysql.connector.Error as err:
    
  # ... if something is wrong with the user name or password  
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: 
    print("Something is wrong with your username or password.")
    
  # ... if the database does not exist  
  elif err.errno == errorcode.ER_BAD_DB_ERROR: 
    print("Database does not exist.")
    
  # if there is any other error...  
  else: 
    print(err)


# creates a cursor for SQL that will be used for executing future queries
cursor = connect.cursor()


# Creating table for dealerm
TABLES = {}
TABLES['dealer'] = ( 
    "  CREATE TABLE dealer ( " 
    "  DName VARCHAR(20),    "
    "  ZIPCode INT,          "
    "  PhoneNumber CHAR(13), "
    "  PRIMARY KEY (DName) ) "
    )

# Creating table for manufacturer
TABLES['manufacturer'] = (
        "  CREATE TABLE manufacturer ( "
        "  MFAbbr CHAR(3),             "
        "  MFName VARCHAR(20),         "
        "  PRIMARY KEY (MFAbbr)      ) "
        )
        
#Creating table for car
TABLES['car'] = (
    "  CREATE TABLE car ( "
    "  Model CHAR(14),    "
    "  Miles INT,         "
    "  DName VARCHAR(20), "
    "  Price INT,         "
    "  MFAbbr CHAR(3),    "
    "  PRIMARY KEY (Model, MFAbbr),                           "
    "  FOREIGN KEY (DName) references dealer(DName),          "
    "  FOREIGN KEY (MFAbbr) references manufacturer(MFAbbr) ) "
    )
    

# Creates each table if does not exist yet
for table_name in TABLES:
    table_description = TABLES[table_name]  
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")
        
        
while True:
    our_input = input("Please enter your command: ") # Reads an input
    our_input = our_input.split(' ') # Splits the input by space and stores it in a list
    
    if our_input[0] == 'a': # If first letter from the input is "a" ... 
        if our_input[1] == 'c': # If second letter from the input is "c" ... 
            
            vin_num = our_input[2] # stores vin number
            
            code = vin_num[:3] #stores the code 
            model = vin_num[3:]#stores the model
    
            # stores the car miles, dealership name, and car price
            miles = our_input[3]
            dealership = our_input[4]
            car_price = our_input[5]
            
            # tries to add the car
            try:
                addCar = "INSERT INTO car (Model, Miles, DName, Price, MFAbbr) VALUES(%s, %s, %s, %s, %s)"    
                values = (model, int(miles), dealership, int(car_price), code)
                cursor.execute(addCar, values)
            # if there is an error, print the error message     
            except mysql.connector.Error as err:
                print("Error: {}".format(err))
            
            #makes sure the changes are made
            connect.commit()
            
        elif our_input[1] == 'm': # Else if the second letter from the input is "m" ... 
            
            # Stores the manufacturer name and the 3 letter code
            manufacturer = our_input[3]
            code = our_input[2]                   
            
            #tries to add the manufacturer
            try:
                addManufacturer = "INSERT INTO manufacturer(MFAbbr, MFName) VALUES(%s, %s)"
                values = (code, manufacturer)
                cursor.execute(addManufacturer, values)
            # if there is an error, prints the error message
            except mysql.connector.Error as err:
                print("Error: {}".format(err))
            
            #makes sure the changes are made
            connect.commit()
        
        elif our_input[1] == 'd': # Else if second letter from the input is "d" ... 
            
            #Stores dealer's name, their zip code, and the phone number
            dealer_name = our_input[2]
            zip_code = our_input[3]
            phone_number = our_input[4] 
            
            
            #tries to add the dealer
            try:
                addDealer = "INSERT INTO dealer(DName, ZIPCode, PhoneNumber) Values(%s, %s, %s)"
                values = (dealer_name, int(zip_code), phone_number)
                cursor.execute(addDealer, values)
            #if there is an error, prints the error message    
            except mysql.connector.Error as err:
                print("Error: {}".format(err))   
            
            #makes sure the changes are made
            connect.commit()
        
    elif our_input[0] == 'l': # Else if first letter from the input is "l" ... 
        if our_input[1] == 'c': # If second letter from the input is "c" ...       
            
            
            #selects all the cars prints them
            cursor.execute("SELECT MFAbbr, Model, Miles, DName, Price FROM car ORDER BY MFAbbr, Model")
            for (Code, Model, Miles, DName, Price) in cursor:
                print("{}{} {} {} {}".format(Code, Model, Miles, DName, Price))
                
        if our_input[1] == 'd': # If the second letter from the input is "d"...
            
            #selects all the dealerships and prints them
            cursor.execute("SELECT * FROM dealer ORDER BY ZIPCode, DName")
            for(name, zipcode, number) in cursor:
                print("{0:<20} {1:<5} {2:<5}".format(name, zipcode, number))
            

    
    elif our_input[0] == 'f': # If th first letter from the input is "f" ...
        if our_input[1] == 'm': # If the second letter from the input is "m" ...
            
            searched = str(our_input[2]) #Stores the specified manufacturer name 
            
            
            # selects all the cars that are made by that manufacturer
            sql = "SELECT MFName, Miles, Price, car.DName, PhoneNumber FROM car, dealer, manufacturer WHERE manufacturer.MFName = %s AND manufacturer.MFAbbr = car.MFAbbr AND car.DName = dealer.DName ORDER BY PRICE DESC, Miles ASC, car.DName"               
            value = (searched, )
            cursor.execute(sql, value)
            
            # prints all those cars with the specified formatting
            for(MFName, Miles, Price, Dname, num) in cursor:
                number = '(' + num[:3] + ')' + num[3:6] + '-' + num[6:]  
                print("{}:{} miles, ${}: {}[{}]".format(MFName, Miles, Price, Dname, number))
                
        if our_input[1] == 'z': # Else if the second letter from the input is "z" ...
            
            searched = our_input[2] # Stores the specified zip code
            
            # selects all the cars that are coming from the specified zip code
            sql = "SELECT MFName, Miles, Price, car.DName, PhoneNumber FROM car, dealer, manufacturer WHERE dealer.ZIPCode = %s AND car.DName = dealer.DName AND car.MFAbbr = manufacturer.MFAbbr ORDER BY MFName ASC, Price DESC, car.DName"
            value = (int(searched), )
            cursor.execute(sql, value)
            
            #prints all those cars with the specified formatting
            for(MFName, Miles, Price, Dname, num) in cursor:
                number = '(' + num[:3] + ')' + num[3:6] + '-' + num[6:]  
                print("{}:{} miles, ${}: {}[{}]".format(MFName, Miles, Price, Dname, number))
            
    elif our_input[0] == 'd': # If th first letter from the input is "d" ...
        if our_input[1] == 'c': # If the second letter from the input is "c" ...
            
            # stores the specified vin number of the car
            vin_num = our_input[2]
            code = vin_num[:3]
            model = vin_num[3:]
            
            # sql query that deletes that car with specified vin number
            sql = "DELETE FROM car WHERE Model = %s AND MFAbbr = %s"
            val = (model, code)
            cursor.execute(sql, val)
            
            #makes sure the changes are made
            connect.commit()
            
        elif our_input[1] == 'd': # If the second letter from the input is "d" ...
            
            # Stores the specified dealer name
            searched = our_input[2]
            
            # sql query that deletes that cars from that dealership 
            sql = "DELETE FROM car WHERE car.DName = %s "
            val = (searched, )
            cursor.execute(sql, val)
            
            #sql query that deletes that dealer
            sql = "DELETE FROM dealer WHERE dealer.DName = %s"
            cursor.execute(sql, val)
            
            #makes sure the changes are made
            connect.commit()
     
    elif our_input[0] == 's': # If th first letter from the input is "s" ...
        
        # sql query that calculates the average price for each manufacturer
        sql = "SELECT MFName, AVG(Price) AS AveragePrice FROM manufacturer, car WHERE car.MFAbbr = manufacturer.MFAbbr group by MFName"
        cursor.execute(sql)
        
        
        # prints the output of the query
        for (name, avg) in cursor:
            print("{} ${}".format(name, avg))
    
    #Stops taking the input if "q" is passed down from the input        
    elif our_input[0] == 'q':
        break      