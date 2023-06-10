from os import remove
import Pyro5
from Pyro5 import *
from Pyro5.api import *
import datetime



@expose
@Pyro5.server.expose
@behavior(instance_mode="single")
class library(object):
    def __init__(self):
        self.users = {}
        self.user_borrowed = {}
        self.user_history = {}
        self.author = {}
        self.book_copy = {}
        self.not_onloan = []
        self.loan_books = []
        self.details=[]
        self.book_date=[]
        self.period={}
        self.history= []
        self.return_history=[]

# task 1: adds a user to the system
    @Pyro5.server.expose
    def add_user(self, user_name, user_number):
        if user_name not in self.users.keys():
            self.users[user_name] = user_number
            self.user_borrowed[user_name] = []
            #New user added to library system,taking two arguments user_name and user_number, and adds the user to the users 
            # dictionary with their name as the key and their number as the value. It also initializes an empty list in the 
            # user _borrowed dictionary for the user.Self refers to an instance of the class library, and self.users and 
            # self.user _borrowed are dictionaries that store the users and their borrowed books, respectively. The if statement 
            # checks whether the user already exists in the users dictionary, and only adds them if they don't already exist.

# task 2: displays the inputed added user data
    @Pyro5.server.expose
    def return_users(self):
        user_info = []
        for name, number in self.users.items():
            user_info.append((name, number))
        return "List of users and contact numbers-", user_info
        #The purpose of the function is to return a list of tuples containing the names and corresponding numbers of users stored 
        # in a dictionary called self.users .The function first creates an empty list called user_info. It then iterates through the
        #  self.users dictionary using a for loop, assigning each key-value pair to the variables name and number. The function then 
        # creates a tuple containing these variables and appends the tuple to the user_info list.Finally, the function returns the 
        # user_info list, which now contains all of the user information as tuples.

# task 3: Add an author to the system
    @Pyro5.server.expose
    def add_author(self, author_name, author_genre):
        if author_name not in self.author.keys():
            self.author[author_name] = author_genre
#add_author is a method in a class that has a dictionary attribute called author. The method takes two arguments: author_name and 
# author_genre.The code checks if the author_name is not already a key in the author dictionary using the not in operator. If it is
#  not, the method adds a new key-value pair to the author dictionary where the author_name is the key and the author_genre is the 
# value.If the author_name already exists as a key in the author dictionary, the method does not perform any action.


# task 4: returns all associated pieces of information relating to the set of authors
    @Pyro5.server.expose
    def return_authors(self):
        name_author = []
        for a_name, genre in self.author.items():
            name_author.append((a_name, genre))
        return "List of authors and author genre of each author-",name_author
#The return_authors  method retrieves all the authors and their genres from the class attribute author and returns them as a
#  list of tuples.The method starts by creating an empty list called name_author.Then, the for loop iterates over the items in the
#  self.author dictionary using the .items() method. For each item, the loop retrieves the a_name (author name) and genre values and 
# creates a tuple with these values using the parentheses (a_name, genre).The tuple is then appended to the name_author list using 
# the .append() method.Finally, the name_author list is returned by the method.


# task 5: Add a copy of a book to the system
    @Pyro5.server.expose
    def add_book_copy(self, author_name, book_title):
        #if book_title not in self.book_copy.keys():
         self.book_copy[book_title] = author_name
         self.not_onloan.append(book_title)
#To ensure book titles are unique,it is checked in the key values of book_copy dictionary.Name of corresponding author
# stored in value of corresponding book_title key.Each newly added book added to a list of books not on any loan self.not_onloan[]

# task 6: Return all associated pieces of information relating to the set of book copies currently not on loan
    @Pyro5.server.expose
    def return_books_not_loan(self):
        book_info = []
        for book_title in self.not_onloan:
            book_info.append(( self.book_copy[book_title],book_title))
        return "List of book authors and book titles available to loan-",book_info
#a list book_info intialized .If book not loaned currently,it is added to book_info[] and returned.
      
# task 7: rents only one of a specific book model, to a specific user, on a specific date etc.
    @Pyro5.server.expose
    def loan_book(self, user_name, book_title, year, month, day):
        if (book_title) not in self.not_onloan:   #Rents only if book is available to loan and returns 0
            return 0
        else:
            self.not_onloan.remove(book_title)   #Removes from list of available books
            self.loan_books.append(book_title)   #Adds to list of loaned books
            if user_name not in self.user_history.keys(): 
                self.user_history[user_name] = {}
            
            
            self.history.append((user_name, book_title, year, month, day)) #list of all books rented
            self.period={ "year" : year,
                "month": month,
                "day" : day}
            self.user_history={
                "user name" : user_name,
                "book_title": book_title,
                "period":self.period #list of all books rented and returned
            }
            
            
            # 
            self.user_borrowed[user_name].append(book_title)
            # 
            return 1

# task 8: returns information about books currently rented
    @Pyro5.server.expose
    def return_books_loan(self):
        book_info = []
        for book in self.loan_books:
            book_info.append((book, self.book_copy[book]))
        return "Books currently on loan",book_info

# task 9: returns rented book and amends to user's library history
    @Pyro5.server.expose
    def end_book_loan(self, user_name, book_title, year, month, day):
        if book_title not in self.user_borrowed[user_name]:
            return
        self.user_borrowed[user_name].remove(book_title)
        self.not_onloan.append(book_title)
        self.loan_books.remove(book_title)
        
        self.period={ "year" : year,
                "month": month,
                "day" : day}
        self.user_history={
                "user name" : user_name,
                "book_title": book_title,
                "period":self.period
            }
        self.return_history.append((user_name, book_title, year, month, day))

# task 10: Delete from the system all copies of a specified book which are currently not on loan.
    @Pyro5.server.expose
    def delete_book(self, book_title):
        for book in self.not_onloan:
            if book == book_title:
                self.not_onloan.remove(book)

# task 11: Delete from the system a specified user. A user should only be deleted if they currently are not loaning and have 
# never loaned a book.
    @Pyro5.server.expose
    def delete_user(self, user_name):
        for entry in self.history:
         if entry[0] == user_name:
           return 0
         
    
        self.users.pop(user_name)
        
        # if they're not in the user history POP IT OUT
        self.user_borrowed.pop(user_name)
        return 1
# task 12: returns all book modules rented previously by a user where the corresponding library and return dates both lie between a specified start and end date
   
    @Pyro5.server.expose
    
    
    def user_loans_date(self, user_name, start_year, start_month, start_day, end_year, end_month, end_day):
        loans = []
        start_date = datetime.datetime(start_year, start_month, start_day)
        end_date = datetime.datetime(end_year, end_month, end_day)
        if start_date > end_date :
            return "Loan Start date entered greater than Loan end date"
        for loan in self.return_history:
            if loan[0] == user_name :
            
             date_now= datetime.datetime(loan[2],loan[3],loan[4])
             if(date_now>=start_date and date_now<=end_date):
              loans.append(loan[1])
        return "Books rented by",user_name,"between",start_date,"and",end_date,"-",loans


daemon = Daemon()
serve({library: "example.library"}, daemon=daemon, use_ns=True)
