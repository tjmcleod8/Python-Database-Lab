import sqlite3
from contextlib import closing
import re 


def insertHorse():
    conn = sqlite3.connect("lab4.db")

    horse = input("\tEnter the horse name: ")
    owner = input("\tEnter the horse owner: ")

    with closing(conn.cursor()) as c:
        query = "insert into horse (horseName, horseOwner) values (?, ?)"
        c.execute(query, (horse, owner)) #horseid is primary key and it is autoincremented in sql
        conn.commit()


def insertMedical():
    conn = sqlite3.connect("lab4.db")
    c = conn.cursor()

    horse = input("\tEnter the horse name: ")
    query = "select horseID from horse where horseName = ?" #use primary key instead of horse name
    c.execute(query, (horse,))
    horseid = c.fetchone()
    if horseid == None: #make sure horse is in database if not send user back
       print("\t'{}' profile is not in the database. (You must enter the horse’s profile before adding med records.)".format(horse))
       return()
    horseid = horseid[0] #make sure horseid isnt a tuple for later use

    treatment = input("\tEnter treatment: ")

    while(True):
        date = input("\tEnter treatement date (mm/dd/yyyy): ")
        match = re.search("\d{2}\/\d{2}\/\d{4}", date) #make sure date is inputted correctly
        if(match == None):
            print("\tInvalid date. Try again.")
            continue
        break
    
    while(True):
        cost = input("\tEnter cost: ")
        try: #make sure cost can be cast as a float
            float(cost)
        except Exception: #if cost cannot be a float have user re-enter cost
            print("\tInvalid cost. Try again.")
            continue
        break

    query = "insert into invoice (horseID, treatment, date, cost) values (?, ?, ?, ?)"
    c.execute(query, (horseid, treatment, date, cost))

    conn.commit()
    if conn:
        conn.close


def displayHorse():
    conn = sqlite3.connect("lab4.db")
    with closing(conn.cursor()) as c:
        query = '''select horseName, horseOwner, count(treatment), sum(cost) 
        from horse left join invoice on horse.horseID = invoice.horseID
        group by horse.horseID''' #left join to get all horses and not just ones that have had treatments
        c.execute(query) 
        table = c.fetchall()
        
        if len(table) == 0: #if there is nothing returned because horse table is empty
            print("There are no horses in the database.")
            return()
        
        print("\t{:20s}{:15s}{:25s}{:15s}".format("Name", "Owner", "Number of Treatments", "Total Cost"))
        for row in table:
            cost = row[3] #cant reassign tuple so must put cost in variable in case cost = None
            if cost == None: #breaks print statment if cost = None
                cost = 0
            print("\t{:20s}{:15s}{:<25d}{:<15.2f}".format(row[0],row[1],row[2],cost))


def displayMedical():
    conn = sqlite3.connect("lab4.db")
    c = conn.cursor()

    horse = input("\tEnter the horse name: ")
    query = "select horseID from horse where horseName = ?"
    c.execute(query, (horse,))
    horseid = c.fetchone()
    if horseid == None: #make sure horse is in database
        print("\t{} profile is not in the database. (You must enter the horse’s profile before displaying med records.)".format(horse))
        return()
    horseid = horseid[0] 

    query = "select treatment, date, cost from invoice where horseID = ?"
    c.execute(query, (horseid,))
    table = c.fetchall()

    print("\t{:25s}{:15s}{:15s}".format("Treatment", "Date", "Cost"))
    for row in table:
        print("\t{:25s}{:15s}{:<15.2f}".format(row[0],row[1],row[2]))

    if conn:
        conn.close

def clearDatabase():
    conn = sqlite3.connect("lab4.db")
    c = conn.cursor()

    print("\tCLEARING DATABASE CLEARS ALL DATA FROM ALL TABLES OF THE DATABASE")
    confirmation = input("\tAre you sure you want to clear the database(y/n)? ")
    if confirmation == "y":
        c.execute("delete from invoice") #delete all data but not the schema from the table so it can be reused without rebuilding tables
        c.execute("delete from horse")
        conn.commit()
        print("\tAll data has been deleted from the database")
    else:
        print("\tData has not been deleted from the database")

    if conn:
        conn.close