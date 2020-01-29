"""
Created on Saturday Aug 31 2019

@author: alisherabdullaev
"""

f_c = open('cars.txt', 'a+') # Creates a file for storing cars if does not exist, and just opens it otherwise
f_m = open('manufacturers.txt', 'a+') # Creates a file for storing manufacturers if does not exist, and just opens it otherwise
f_d = open('carDealers.txt', 'a+') # Creates a file for storing car dealers if does not exist, and just opens it otherwise

# Reads all lines from a file and stores them in seperate lists
# Takes one argument (file name)
# Returns a list of lists where each inner list contains a line from the file 
def getFileLines(file):
    
    line = []
    with open(file) as f:
        for our_line in f:
            our_line = our_line.rstrip('\n') # Removes "\n" from each line 
            line.append(our_line)             
    return [x.split(' ') for x in line]  

#Keeps taking in input
while True:
    our_input = input() # Reads an input
    our_input = our_input.split(' ') # Splits the input by space and stores it in a list
    
    if our_input[0] == 'a': # If first letter from the input is "a" ... 
        
        if our_input[1] == 'c': # If second letter from the input is "c" ... 
            f_c = open('cars.txt', 'a+') # Opens the cars file
            
            # Stores the VIN number, the code, miles driven, the dealership name, and the price of the car
            vin_num = our_input[2]
            code = vin_num[:3]
            miles = int(our_input[3])
            dealership = our_input[4]
            car_price = our_input[5]
            
            # If there is a manufacturer with such code, it just stores the manufacturer information in a list of list
            existing_manf = [x for x in getFileLines('manufacturers.txt') if code in x]
          
            # If the list is not empty ...
            if existing_manf:
                # Writes into the file just created variables and closes the file
                f_c.write(vin_num + ' %d' % miles + ' ' + dealership + ' ' + car_price + '\r\n')
                f_c.close()
            # Closes the file otherwise
            else:
                f_c.close() 
        
        elif our_input[1] == 'm': # Else if the second letter from the input is "m" ... 
            f_m = open('manufacturers.txt', 'a+') # Opens the manufacturers file
            
            # Stores the manufacturer name and the 3 letter code
            manufacturer = our_input[2]
            code = our_input[3]
            
            # Writes into the file just created variables and closes the file
            f_m.write(manufacturer + ' ' + code + '\r\n')
            f_m.close()
        
        elif our_input[1] == 'd': # Else if second letter from the input is "d" ... 
            f_d = open('carDealers.txt', 'a+') # Opens the car dealers file
            
            #Stores dealer's name, their zip code, and the phone number
            dealer_name = our_input[2]
            zip_code = int(our_input[3])
            phone_number = our_input[4] 
            
            
            
            bl = True
            
            for i in getFileLines('carDealers.txt'): # Loops over all dealerships
                # If just passed in dealership name is the same as current name in the loop
                if i[0] == dealer_name: 
                    # If zip codes do not match but phone numbers do, gives an error message and does not add a dealership
                    if int(i[1]) != zip_code and i[2] == phone_number:          
                        bl = False                                              
                        print('Error: Such dealership already exists :(')   
                    # If zip codes do match but phone numbers do not, gives an error message and does not add a dealership
                    elif int(i[1]) == zip_code and i[2] != phone_number:        
                        bl = False
                        print('Error: Such dealership already exists :(')
                    # Gives an error message if zip code and phone number are the same
                    elif int(i[1]) == zip_code and i[2] == phone_number:
                        bl = False
                        print('Error: Such dealership already exists :(')
                   
            if bl:
                # Writes into the file just created variables and closes the file
                f_d.write(dealer_name + ' %d' % zip_code + ' ' + phone_number + '\r\n')
                f_d.close()
            
    elif our_input[0] == 'l': # Else if first letter from the input is "l" ... 
        
        if our_input[1] == 'c': # If second letter from the input is "c" ...
            
            # Opens the cars file and reads all the contents
            f_c = open('cars.txt', 'r')
            print(f_c.read())
            
        elif our_input[1] == 'd': # If second letter from the input is "m" ...
                        
            # Found in Stack Overflow, (https://stackoverflow.com/questions/9989334/create-nice-column-output-in-python)
            data = getFileLines('carDealers.txt')
            
            if data:
                col_width = max(len(word) for row in data for word in row) + 3
                for row in data:
                    print ("".join(word.ljust(col_width) for word in row))

    elif our_input[0] == 'f': # If th first letter from the input is "f" ...
        
        if our_input[1] == 'm': # If the second letter from the input is "m" ...
            
            searched = our_input[2] #Stores the specified manufacturer name 
            
            # Stores the manufacturer information in list of list that matched with the searched name
            desiredLine_manf = [x for x in getFileLines('manufacturers.txt') if searched in x] 
            
            # If the list is not empty, stores the manufacturer code
            if desiredLine_manf:
                code = desiredLine_manf[0][0]

            # Stores each car information in list of lists whose code corresponds to the searched manufacturer name 
            desiredLine_cars = [x for x in getFileLines('cars.txt') if code in x[0]]
            
            # Loops over all cars that made by the specified manufacturer
            for x, car in enumerate(desiredLine_cars): 
                #Stores its dealer
                desired_dealer = car[2]
                # Stores dealer's information in list of list
                desiredLine_carDealers = [j for j in getFileLines('carDealers.txt')  if desired_dealer in j]
                #Stores phone number, formats it, and then prints car details
                num = desiredLine_carDealers[0][2]
                num = '(' + num[:3] + ')' + num[3:6] + '-' + num[6:]
                print(searched + ':' + desiredLine_cars[x][1] + ' miles, $' + desiredLine_cars[x][3] + ': ' + desiredLine_cars[x][2] + '[' + num + ']')             
            
        elif our_input[1] == 'z': # Else if the second letter from the input is "z" ...
            
            searched = our_input[2] # Stores the specified zip code
 
            #Stores car dealers infromation in list of lists that have specified zip code
            desiredLine_carDealers = [x for x in getFileLines('carDealers.txt') if searched in x]
            
            # Stores each dealer name in a list
            dealerships = []
            for i in desiredLine_carDealers:
                dealership = i[0]
                dealerships.append(dealership)
            
            # Stores all cars that are coming from the specified zip code
            desiredLine_cars = []
            for x in getFileLines('cars.txt'):
                for i in dealerships:
                    if i in x:
                      desiredLine_cars.append(x)  
                      
            # Loops over all cars that are coming from the specified zip code
            for x, car in enumerate(desiredLine_cars):
                # Stores the VIN number, the code, and the dealership name
                vin_num = car[0]
                code = vin_num[:3]
                dealership = car[2]
                # Loops over all manufacturers
                for i in getFileLines('manufacturers.txt'):
                    # If codes match, stores the coresponding name 
                    if i[0] == code:
                        name = i[1]
                # Loops over all dealers with specified zip code
                for i in desiredLine_carDealers:
                    #If dealership names match, stores the coresponding phone number
                    if i[0] == dealership:
                        num = i[2]
                # Formats the phone number and prints all cars available at dealers in specified zip code
                num = '(' + num[:3] + ')' + num[3:6] + '-' + num[6:]        
                print(name + ':' + desiredLine_cars[x][1] + ' miles, $' + desiredLine_cars[x][3] + ': ' + desiredLine_cars[x][2] + '[' + num + ']')   
            
    #Stops taking the input if "q" is passed down from the input        
    elif our_input[0] == 'q':
        break 