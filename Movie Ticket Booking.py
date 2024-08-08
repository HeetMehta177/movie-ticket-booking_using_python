import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class User:
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.booking_history=[]

    def add_booking(self,booking_details):
        self.booking_history.append(booking_details)

class BookingDetails:
    def __init__(self,theatre,movie_name,date,time,row,col,price):
        self.theatre=theatre
        self.movie_name=movie_name
        self.date=date
        self.time=time
        self.row=row
        self.col=col
        self.price=price

class Theatre:
    def __init__(self,name,movies):
        self.name=name
        self.movies=movies

class MovieTicketBookingSystem:
    def __init__(self):
        self.users={} #key-username value-user object
        self.logged_in_user=None
        self.theatres=[ Theatre("PVR", [("Dune:Part Two", "10:00", np.zeros((10, 10), dtype=int), 100), 
                                        ("Dune:Part Two", "15:00", np.zeros((10, 10), dtype=int), 150), 
                                        ("Dune:Part Two", "19:15", np.zeros((10, 10), dtype=int), 200), 
                                          ("Joker 2", "10:00", np.zeros((10, 10), dtype=int), 150),
                                          ("Joker 2", "16:00", np.zeros((10, 10), dtype=int), 200),
                                          ("Joker 2", "22:45", np.zeros((10, 10), dtype=int), 350),
                                          ("Borderlands", "11:00", np.zeros((10, 10), dtype=int), 120),
                                          ("Borderlands", "16:30", np.zeros((10, 10), dtype=int), 150),
                                          ("Borderlands", "20:00", np.zeros((10, 10), dtype=int), 230)]),
            Theatre("INOX", [("Red One", "10:30", np.zeros((10, 10), dtype=int), 180),
                             ("Red One", "14:15", np.zeros((10, 10), dtype=int), 250),
                             ("Red One", "23:00", np.zeros((10, 10), dtype=int), 330),
                             ("Dune:Part Two", "13:30", np.zeros((10, 10), dtype=int), 110),
                              ("Dune:Part Two", "14:10", np.zeros((10, 10), dtype=int), 190),
                               ("Dune:Part Two", "20:20", np.zeros((10, 10), dtype=int), 270),
                             ("Wicked", "09:30", np.zeros((10, 10), dtype=int), 140),
                             ("Wicked", "13:10", np.zeros((10, 10), dtype=int), 240),
                             ("Wicked", "18:20", np.zeros((10, 10), dtype=int), 340)]),
            Theatre("City Gold", [("Crew", "11:20", np.zeros((10, 10), dtype=int), 90),
                                  ("Crew", "14:00", np.zeros((10, 10), dtype=int), 190),
                                  ("Crew", "20:00", np.zeros((10, 10), dtype=int), 240),
                                  ("Bhakshak", "14:00", np.zeros((10, 10), dtype=int), 160),
                                  ("Bhakshak", "15:30", np.zeros((10, 10), dtype=int), 160),
                                  ("Bhakshak", "20:10", np.zeros((10, 10), dtype=int), 260),
                                  ("Joker 2", "11:00", np.zeros((10, 10), dtype=int), 180),
                                  ("Joker 2", "14:00", np.zeros((10, 10), dtype=int), 180),
                                  ("Joker 2", "19:00", np.zeros((10, 10), dtype=int), 250)])]

    def register(self,username,password):
        if username in self.users:
            print("Username already exists. Please choose a different username.")
            return False
        else:
            self.users[username]=User(username, password)
            print("Registration successful.")
            return True

    def login(self,username,password):
        if username in self.users and self.users[username].password==password:
            self.logged_in_user=self.users[username]
            print(f"Welcome {username}")
            return True
        else:
            print("Invalid username or password.")
            return False

    def logout(self):
        self.logged_in_user=None
        print("Logged out successfully.")

    def display(self):
        print("Available Movies:")
        for theatre in self.theatres:
            print(f"Theatre: {theatre.name}")
            print("Movies: ")
            for movie,time,_,price in theatre.movies:
                print(f"-{movie} ({time})- Rs. {price}")
            print()

    def select_theatre(self):
        print("Available Theatres:")
        for index in range(len(self.theatres)):
            print(f"{index}. {self.theatres[index].name}")
        choice = int(input("Enter the number of the theatre you want to select: "))
        return self.theatres[choice]

    def select_movie(self,theatre):
        print(f"Available Movies for {theatre.name}:")
        for index in range(len(theatre.movies)):
            movie,time,_,price=theatre.movies[index]
            print(f"{index}. {movie} ({time})- Rs. {price}")
        choice=int(input("Enter the number of the movie you want to watch: "))
        return theatre.movies[choice]

    def book_ticket(self):
        if not self.logged_in_user:
            print("Please login first.")
            return

        total_price=0

        while True:
            theatre=self.select_theatre()
            movie,time,seats,price=self.select_movie(theatre)

            print("Available seats:")
            print(seats)

            row=int(input("Enter row number: "))
            col=int(input("Enter column number: "))

            if seats[row][col]==1:
                print("Seat already booked. Please choose another seat.")
                continue

            seats[row][col]=1

            while True:
                date_str=input("Enter date (YYYY-MM-DD): ")
                try:
                    booking_date=datetime.strptime(date_str,"%Y-%m-%d")
                    current_date=datetime.now()
                    if booking_date < current_date:
                        print("Please enter a future date.")
                        continue
                    else:
                        break
                except ValueError:
                    print("Invalid date format. Please enter date in YYYY-MM-DD format.")
                    continue

            print("Ticket booked successfully.")

            total_price+=price

            booking_details=BookingDetails(theatre.name,movie,date_str,time,row,col,price)
            self.logged_in_user.add_booking(booking_details)

            choice= input("Do you want to book another ticket? (yes/no): ")
            if choice.lower()!= 'yes':
                break

            print(f"Total amount to be paid: Rs. {total_price}")

    def display_seats(self):
        theatre=self.select_theatre()
        movie,time,seats,price =self.select_movie(theatre)

        plt.imshow(seats,cmap='coolwarm',interpolation='nearest')
        plt.grid()
        plt.xlabel('Seats')
        plt.ylabel('Rows')
        plt.title('Seat Availability')
        plt.colorbar(label='0: Available, 1: Booked')
        plt.show()

    def display_booking_history(self):
        if not self.logged_in_user:
            print("Please login first.")
            return

        print("Booking History:")
        for i in range(len(self.logged_in_user.booking_history)):
            booking = self.logged_in_user.booking_history[i]
            print(f"Booking {i+1}:")
            print(f"Theatre: {booking.theatre}")
            print(f"Movie: {booking.movie_name}")
            print(f"Date: {booking.date}")
            print(f"Time: {booking.time}")
            print(f"Seat: Row {booking.row},Column{booking.col}")
            print(f"Price: Rs. {booking.price}")
            print()

# Main function
booking_system = MovieTicketBookingSystem() 
def main():
    while True:
        print()
        print("1. Register")
        print("2. Login")
        print("3. Logout")
        print("4. display movies")
        print("5. Book Ticket")
        print("6. Display Seats")
        print("7. Display Booking History")
        print("8. Exit!")
        print()
        choice=input("Enter your choice: ")

        if choice== '1':
            username =input("Enter username: ")
            password= input("Enter password: ")
            booking_system.register(username,password)

        elif choice =='2':
            if booking_system.logged_in_user:
                print("Already logged in.")
            else:
                username = input("Enter username: ")
                password = input("Enter password: ")
                booking_system.login(username, password)  
        elif choice == '3':
            booking_system.logout() 

        elif choice == '4':
            booking_system.display()  
        elif choice == '5':
            booking_system.book_ticket()  

        elif choice == '6':
            booking_system.display_seats()  
        elif choice == '7':
            booking_system.display_booking_history()  
        
        elif choice == '8':
            print("Exiting program.\nThank You!")
            break
        else:
            print("Invalid choice. Please try again.")


main()