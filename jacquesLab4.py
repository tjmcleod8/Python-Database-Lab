import jacquesLab4module as module

def main():
    message = '''COMMAND MENU:
    1) Enter a horse's profile into the database. (Include horse name and owner.)
    2) Enter a medical invoice. (Include horse name, date, treatment, and cost.)
    3) Display all horses in the database, sorted by horse name. (Include horse, owner, number of medical 
        invoices, and total cost. You should assume one treatment per invoice.)
    4) Display medical history for a horse, sorted by treatment date. (Include horse name, date, treatment and
        cost)
    5) Clear Database (THIS CLEARS ALL DATA FROM ALL TABLES OF THE DATABASE)
    6) Exit program.   
    '''
    print(message)

    while True:
        value = input("What do you want to do? ")
        if(value == "1"):
            module.insertHorse()
        elif(value == "2"):
            module.insertMedical()
        elif(value == "3"):
            module.displayHorse()
        elif(value == "4"):
            module.displayMedical()
        elif(value == "5"):
            module.clearDatabase()
        elif(value == "6"):
            print("\t<<Good Bye>>")
            exit()
        else:
            print("\tInvalid input. Try again")
        
        
if(__name__ == "__main__"): main()