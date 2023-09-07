# Name: Esat Duman
# UIN: 662726641
# Date: 2/9/2023
# Instructor: Patrick Troy
# Project 01 : Analyzing CTA2 L data in Python
# Overview: console-based Python program that inputs commands from the user and outputs data from the CTA2 L daily ridership database. The program starts by outputting some basic stats
#retrieved from the database



import sqlite3
import matplotlib.pyplot as plt

#----------------------------------------------------------------------------------------------------------------------

# My functions are listed here:

def NumOfStations(dbConn):
  dbCursor = dbConn.cursor()
  query = "Select count(*) From Stations;" # reads the table 
  dbCursor.execute(query)
  row = dbCursor.fetchone();
  print("  # of stations:", f"{row[0]:,}")
# This function simply counts the total number of stops and outputs the result.

# This function reads the CTA table and calculates the number of stops.
def NumOfStops(dbConn):
  dbCursor = dbConn.cursor()
  query = "Select count(*) From Stops;" 
  dbCursor.execute(query)
  row = dbCursor.fetchone();
  print("  # of stops:", f"{row[0]:,}") 

#This function simply counts the total number of entries and outputs the result.
def NumOfEntries(dbConn):  
  dbCursor = dbConn.cursor()
  query = "Select count(*) From Ridership;" # reading the cta table and counting the number of entries
  dbCursor.execute(query)
  row = dbCursor.fetchone();
  print("  # of ride entries:", f"{row[0]:,}")

#This function identifies the start and end dates for the table.
def Date(dbConn):
  dbCursor = dbConn.cursor()  #This reads the CTA table and determines the date range.
  query = "Select min(date(Ride_Date)),max(date(Ride_Date))From Ridership;"
  dbCursor.execute(query)
  row = dbCursor.fetchone();
  print("  date range:", row[0],"-", row[1])
  
# This function calculates the overall number of riders and returns the total, as it will be used for further operations.
def totalRidership(dbConn):
  dbCursor = dbConn.cursor()
  query = ("Select sum(Num_Riders) From Ridership;") # selects the CTA table and counts the stops.
  dbCursor.execute(query)
  row = dbCursor.fetchone();
  total = row
  return total
  
# In this function all we are doing is counting the total number of riders on weekdays and printing it. 
  
def weekDayRidership(dbConn,total):
  dbCursor = dbConn.cursor()
  query = "Select sum(Num_Riders) From Ridership where Type_of_Day = 'W';"
  # reading the cta table and counting the number of riders on weekdays
  dbCursor.execute(query)
  row1 = dbCursor.fetchone();
  print(f"  Weekday ridership: {row1[0]:,} ({(row1[0]/(total[0])*100):.2f}%)")
# In this function all we are doing is counting the total number of riders on saturday and printing it. 
  
def SaturdayRidership(dbConn,total):
  dbCursor = dbConn.cursor()
  query = "Select sum(Num_Riders) From Ridership where Type_of_Day = 'A';"
    # reading the cta table and counting the number of riders on saturday
  dbCursor.execute(query)
  row1 = dbCursor.fetchone();
  print(f"  Saturday ridership: {row1[0]:,} ({(row1[0]/(total[0])*100):.2f}%)")
# In this function all we are doing is counting the total number of riders on sunday and printing it. 
  
def SundayRidership(dbConn,total):
  dbCursor = dbConn.cursor()
  query = "Select sum(Num_Riders) From Ridership where Type_of_Day = 'U';"
  dbCursor.execute(query)  # reading the cta table and counting the number of riders on sunday
  row1 = dbCursor.fetchone();
  print(f"  Sunday/holiday ridership: {row1[0]:,} ({(row1[0]/(total[0])*100):.2f}%)")
# what this function does is print all the functions we created prev.   
  
def print_stats(dbConn):
    print("General stats:")
    NumOfStations(dbConn)
    NumOfStops(dbConn)
    NumOfEntries(dbConn)
    Date(dbConn)
  
    total = totalRidership(dbConn)
    print("  Total ridership:", f"{total[0]:,}")
    weekDayRidership(dbConn,total)
    SaturdayRidership(dbConn, total)
    SundayRidership(dbConn, total)
  
# Print the station name and it's ID from the user input from the station table 

  #--------------------------------------------Command One Start---------------------------------------------------------

def command_One(dbConn):
  stationName = input('\nEnter partial station name (wildcards _ and %): ')
  StationNum = dbConn.cursor()
  query1 = """Select Station_ID, 
              Station_Name From Stations
              Where Station_Name like ?
              group by Station_Name;
              """
  # All this does is print the id and name of the station that was choosen.
  StationNum.execute(query1, [stationName])
  row = StationNum.fetchall()
  if len(row)==0: # So if the station they wrote is incorrect or not in the table.
    print("**No stations found...")
  for row in row:
    print(f"{row[0]:}",":", f"{row[1]:}")
    
#-------------------------------------------------Command Two Start------------------------------------------------------
    
# This displays the ridership for each station and calculates the percentage of the stations with the highest population.
def command_Two(dbConn, total):
   print(" ** ridership all stations **")
   StationNum = dbConn.cursor()
   query1 = """Select Station_Name, Sum(Num_Riders) From Stations join  Ridership on (Ridership.Station_ID  = Stations.Station_ID)
              group by Station_Name
              order by Station_Name;
              """
  # reads the station name and the sum of the total riders.
   StationNum.execute(query1)
   row = StationNum.fetchall()
   #print(row)
   for row in row:
    print(f"{row[0]:}",":",f"{row[1]:,}",f"({(row[1]/(total[0])*100):.2f}%)")
     # Because we previously constructed the totalridership function and passed it by refrence down below, we don't need to keep writing the total.
# This prints out the top 10 busiest stations.

#---------------------------------------------------Command Three Start--------------------------------------------------------
def command_Three(dbConn, total):
   print(" ** top-10 stations **")
   StationNum = dbConn.cursor()
   query1 = """Select Station_Name, Sum(Num_Riders) as total_Riders From Stations join  Ridership on (Ridership.Station_ID  = Stations.Station_ID)
              group by Station_Name
              order by total_Riders desc limit 10;
              """
  # reads the station name and the sum of the total riders and limits to only printing the busiest 10.
   StationNum.execute(query1)
   row = StationNum.fetchall()
   #print(row)
   for row in row:
    print(f"{row[0]:}",":",f"{row[1]:,}",f"({(row[1]/(total[0])*100):.2f}%)")
    # the total is the totalridership function we created before and passed it by refrence down here so we don't have to keep writing the total. 
# what this does is it prints the top 10 least busiest station.  

#--------------------------------------------------Command Four Start----------------------------------------------------
def command_Four(dbConn, total):
  print(" ** least-10 stations **")
  StationNum = dbConn.cursor()
  query1 = """Select Station_Name, Sum(Num_Riders) as total_Riders From Stations join  Ridership on (Ridership.Station_ID  =   Stations.Station_ID)
              group by Station_Name
              order by total_Riders asc limit 10;
              """
    # reads the station name and the sum of the total riders and prints the least 10 popular stations using limit.
  StationNum.execute(query1)
  row = StationNum.fetchall()
   #print(row)
  for row in row:
    print(f"{row[0]:}",":",f"{row[1]:,}",f"({(row[1]/(total[0])*100):.2f}%)")
    # the total is the totalridership function we created before and passed it by refrence down here so we don't have to keep writing the total.
#All this command does is ask the user the write a color and prints all the name of that color and prints the direction and accessivle.    

#-------------------------------------------------Command Five Start-----------------------------------------------------
def command_Five(dbConn):
  choose_Color = input('\nEnter a line color (e.g. Red or Yellow): ')
  StationNum = dbConn.cursor()
  query1 = """Select Stop_Name, Direction, ADA FROM Lines join 
  StopDetails on (StopDetails.Line_ID = Lines.Line_ID)
  join Stops on (StopDetails.Stop_ID = Stops.Stop_ID)
  Where Color like ? 
  order by Stop_Name;"""
  # Prints every piece of data from the table and the table's joining.
  StationNum.execute(query1, [choose_Color])
  row = StationNum.fetchall()
  if len(row)==0: # this is used if the color is not presented in the table.
    print("**No such line...")
  for row in row:
    #Dempster-Skokie (Arrival) : direction = N (accessible? yes)
    if row[2] == 1:
      flag = 'yes'
    else:
      flag = 'no'
    print(f"{row[0]:}",": direction =", f"{row[1]:}", f"(accessible? {flag})" )
# total number of ridership by months and plotting it.

#----------------------------------------------Command Six Start---------------------------------------------------------

#This function calculates the overall ridership by year and utilizes the user's input to generate a plot.
def command_Six(dbConn):
  print(" ** ridership by month **")
  StationNum = dbConn.cursor()
  query1 = """Select strftime('%m', Ride_Date) as months, sum(Num_Riders) as total_Riders from Ridership 
  group by months
  order by months;"""
  
  StationNum.execute(query1)  # determines the cumulative number of riders based on the monthly data.
  rows = StationNum.fetchall()
  for row in rows:
    print(f"{row[0]:}",":", f"{row[1]:,}")  # we use this matplot to plot the graph.
  print("\n")
  plotGraph = input('Plot? (y/n) ')  # Asking the use if they want the map to be plotted
  if plotGraph == 'y':
    x = []      
    y = []
    for row in rows: 
       x.append(row[0])
       y.append(row[1])
    plt.ioff()
    plt.xlabel("month")
    plt.ylabel("number of riders(x*10^8)")
    plt.title("monthly ridership")
    plt.plot(x, y)
    plt.show()

    
#------------------------------------------Command Seven Start-----------------------------------------------------------
def command_Seven(dbConn):
  print(" ** ridership by year **")
  StationNum = dbConn.cursor()
  query1 = """SELECT strftime('%Y', Ride_Date) as years, sum(Num_Riders) as total_Riders from Ridership
  WHERE years BETWEEN '2001' AND '2021'
  group by years
order by years"""
  
  StationNum.execute(query1)    #SELECTS the total number of riders in the month. 
  rows = StationNum.fetchall()
  for row in rows:
    print(f"{row[0]:}",":", f"{row[1]:,}") # plot the map using python
    print("\n")
  plotGraph = input("Plot? (y/n) ") 
  if plotGraph == 'y':
    x = [] 
    y = []
    for row in rows: 
       x.append(row[0])
       y.append(row[1])
    plt.ioff()
    plt.xlabel("year")
    plt.ylabel("number of riders(x*10^8)")
    plt.title("yearly ridership")
    plt.plot(x, y)
    plt.show()


    
#This function requires three inputs from the user and locates the initial elements of the second input and the last five elements of the third input. The user is asked to specify the desired year to view, and whether they would like a plot to be displayed or not.

#--------------------------------------------Command Eight Start---------------------------------------------------------
def command_Eight(dbConn):
  StationNum = dbConn.cursor()
  userYear = input("\nYear to compare against? ")
  print()
  userStation1 = input("Enter station 1 (wildcards _ and %): ")
  command1 = """SELECT Station_ID, Station_Name FROM Stations WHERE Station_Name Like ?"""
  StationNum.execute(command1, [userStation1])
  prerow = StationNum.fetchall()
  
  if (len(prerow) > 1): # this if there are trying to print the same stations.
    print("**Multiple stations found...") 
  elif(len(prerow) == 1):
      print()
      userStation2 = input("Enter station 2 (wildcards _ and %): ")
      StationNum.execute(command1, [userStation2])
      prerow2 = StationNum.fetchall()
    
      if (len(prerow2) > 1): 
        print("**Multiple stations found...")
      #given a year and 2 stations 
      elif(len(prerow2) == 1):
          query1 = """SELECT SUBSTRING(Ride_Date, 1, 10), sum(Num_Riders), Ridership.Station_ID, Station_Name FROM Ridership 
          JOIN Stations on Ridership.Station_ID = Stations.Station_ID
          WHERE Station_Name Like ?
          GROUP BY Ride_Date ORDER BY Ride_Date ASC"""
          #display results in ascending order 
          StationNum.execute(query1, [userStation1])
          row = StationNum.fetchall()
          
          StationNum.execute(query1, [userStation2])
          row2 = StationNum.fetchall()
          print(f"Station 1: {row[0][2]} {row[0][3]}") # Station Display
          
          newRow = []
          for i in row:
            if (userYear in i[0]):
              newRow.append(i)
          newRowShort = newRow[0:5] + newRow[-5:]    
          
          for i in newRowShort:
            print(f"{i[0]} {i[1]}")
          print(f"Station 2: {row2[0][2]} {row2[0][3]}") 
          newRow2 = []
          for i in row2:
            if (userYear in i[0]):
              newRow2.append(i)
          row2Total = newRow2[0:5] + newRow2[-5:]    
          for i in row2Total:
            print(f"{i[0]} {i[1]}")
          print()
          userInput = input("Plot? (y/n) ")
          if (userInput == 'y'):
            x = []    
            y = []
            counter = 0
            for i in newRow:  
              x.append(counter)
              y.append(i[1])
              counter = counter + 1
            plt.xlabel("Day")
            plt.ylabel("Number of Riders")
            plt.title("Riders each day of")
            plt.plot(x, y)
            a = []    
            b = []
            counter = 0
            for i in newRow2:  
              a.append(counter)
              b.append(i[1])
              counter = counter + 1
            plt.xlabel("Day")
            plt.ylabel("Number of Riders")
            plt.title("Riders each day of")
            plt.plot(a, b)
            plt.show()
          else:
            pass
      else:
          print("**No station found...")           
  else:
     print("**No station found...")      
  print()    #This program requests a yellow color from the user before locating the latitude, displaying it, and plotting it.
 

#----------------------------------------------------Command Nine Start--------------------------------------------------
def command_Nine(dbConn):
    colorCommand = input('\nEnter a line color (e.g. Red or Yellow): ')
    cursor = dbConn.cursor()
    query1 = """select Distinct Station_Name, Latitude, longitude From stops 
     join stations on stops.station_ID = stations.station_ID  
     join StopDetails on stops.stop_ID = StopDetails.stop_ID
     join Lines on StopDetails.Line_ID = Lines.Line_ID
     where color like ?
     order by Station_Name asc
     """
    # Query Finished retrieves the distinct station name, latitude, and longitude of stops in the database based on a specified color.
    cursor.execute(query1, [colorCommand])
    rows = cursor.fetchall()
    if not rows:
        print("No such line.")
        return
    print("\n".join([f"{row[0]}: ({row[1]}, {row[2]})" for row in rows]))
    print("\n")
    plot_graph = input("Plot graph (y/n)? ")
    if plot_graph != "y":
        return
    x, y = zip(*[(row[2], row[1]) for row in rows])
    color = "Purple" if colorCommand == "Purple-Express" else colorCommand
    plt.scatter(x, y, c=color)
    plt.title(colorCommand + " line")
    for row in rows:
        plt.annotate(row[0], (row[2], row[1]))

    image = plt.imread("chicago.png")  # This so the Map of Chicago can be displayed 
    plt.imshow(image, extent=[-87.9277, -87.5569, 41.7012, 42.0868], alpha=0.5)
    plt.xlim([-87.9277, -87.5569])
    plt.ylim([41.7012, 42.0868])
    plt.show()

#
#---------------------------------------------------Main Start----------------------------------------------------------
#
print('** Welcome to CTA L analysis app **\n')

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
# used to check for the commands.
choice = ['x','1','2', '3', '4', '5', '6', '7', '8','9']
print_stats(dbConn)
print()

while True:
    val = input("Please enter a command (1-9, x to exit):")
    if val == 'x':
        break
    elif val not in choice:
        print(' **Error, unknown command, try again...\n')
    else:
        total = totalRidership(dbConn) if val in ['2', '3', '4'] else None
        if val == '1':              # Command Inputs so when '1' is typed start Command same goes for the other commands
            command_One(dbConn)
        elif val == '2':
            command_Two(dbConn, total)
        elif val == '3':
            command_Three(dbConn, total)
        elif val == '4':
            command_Four(dbConn, total)
        elif val == '5':
            command_Five(dbConn)
        elif val == '6':
            command_Six(dbConn)
        elif val == '7':
            command_Seven(dbConn)
        elif val == '8':
            command_Eight(dbConn)
        elif val == '9':
            command_Nine(dbConn)

#
# done
#
