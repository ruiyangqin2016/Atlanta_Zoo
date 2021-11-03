import tkinter as tk
from tkinter import *
from tkinter import messagebox

import tkinter.ttk as ttk
import pymysql
import hashlib
import datetime
import itertools
import re

# get pymysql connection
db = pymysql.connect(host='academic-mysql.cc.gatech.edu',
                     passwd='gCi5ozqX', user='cs4400_group22', db='cs4400_group22')
cursor = db.cursor()


class GUI:

    def __init__(self):
        self.toLogin()

        # after login, user GUI.user variable is created. if running just a one component, create a user handle
## note:

##1. constraints: check(<statement>)
##2. sql build table recheck


#========================================================================

#                        Login

#========================================================================
##LOGING IN AND CREATING NEW USER--------------------------------------
    def toLogin(self):
        """Main login screen"""
        # Main window
        self.main = Tk()
        self.main.title("User Login")

        # label/entry frame
        win = Frame(self.main)
        win.pack()

        # labels
        Label(win, text="Username:").grid(row=1, column=0, sticky=E, pady=5)
        Label(win, text="Password:").grid(row=2, column=0, sticky=E, pady=5)

        # Entries
        self.username_entry = Entry(win, width=50)
        self.username_entry.grid(row=1, column=1, padx=5)
        self.password_entry = Entry(win, show="*", width=50)
        self.password_entry.grid(row=2, column=1, padx=5)

        # button frames
        buttonframe = Frame(self.main)
        buttonframe.pack(anchor=E)

        # buttons
        Button(buttonframe, text="Login", command=self.connect).pack(side=RIGHT)
        Button(buttonframe, text="Register",
               command=self.toRegister).pack(side=RIGHT)

        # mainloop
        self.main.mainloop()
    def toRegister(self):
        """Register User Screen"""
        # creates new window
        self.main.destroy()
        self.reg = Tk()
        self.reg.title("Create New Account")

        # label/entries frame
        reg_frame = Frame(self.reg)
        reg_frame.pack()

        # labels
        Label(reg_frame, text="Username:").grid(
            row=2, column=0, sticky=E, pady=5)
        Label(reg_frame, text="Password:").grid(
            row=3, column=0, sticky=E, pady=5)
        Label(reg_frame, text="Confirm Password:").grid(
            row=4, column=0, sticky=E, pady=5)
        Label(reg_frame, text="Email:").grid(
            row=5, column=0, sticky=E, pady=5)

        Label(reg_frame, text="Type:").grid(
            row=6, column=0, sticky=E)


        # username,password,password_confirm,email entries
        self.username = Entry(reg_frame, width=50)
        self.username.grid(row=2, column=1, padx=5)
        self.password = Entry(reg_frame, show="*", width=50)
        self.password.grid(row=3, column=1, padx=5)
        self.password_confirm = Entry(reg_frame, show="*", width=50)
        self.password_confirm.grid(row=4, column=1, padx=5)
        self.email_entry = Entry(reg_frame, width=50)
        self.email_entry.grid(row=5, column=1, padx=5)

        self.userVar = StringVar()
        self.Types = {"staff", "visitor"}
        self.userVar.set("staff")
        self.userType = OptionMenu(reg_frame, self.userVar, *self.Types)
        self.userType.grid(row = 6, column = 1, sticky = "w")

        # button frame
        buttonframe = Frame(self.reg)
        buttonframe.pack(anchor=E)

        # buttons
        Button(buttonframe, text="Register",
               command=self.registerconfirm).pack(side=RIGHT)
        Button(buttonframe, text="Cancel",
               command=self.reg_cancel).pack(side=RIGHT)

        # mainloop
        self.reg.mainloop()
    def registerconfirm(self):
        """Helper function for toRegister, does actual action of registering and checking requirements"""
        error = False
        # check all fields filled in
        if self.username.get() is '' or self.password.get() is '' or self.password_confirm.get() is '' or self.email_entry.get() is '':
            messagebox.showerror(title="Warning", message="All fields are required")
            error = True

        # check that passwords are equal
        if self.password.get() != self.password_confirm.get():
            messagebox.showerror(title="Password Error", message="Passwords must match")
            error = True

        # check password is valid
        if len(self.password.get()) < 8:
            messagebox.showerror(title="Password Error", message="Password must be more than 8 characters")
            error = True

        emailMatching = re.search('^([A-Z, a-z, 0-9]+)@([A-Z, a-z, 0-9]+)(\.)([A-z, a-z, 0-9]+)', self.email_entry.get())
        if emailMatching is None:
            error = True
            messagebox.showerror(title="Error", message="Invalid Email address!")        

        if error is False:
            # check that username and email doesn't exist
            sql = "SELECT email, username FROM zoo_user where email = \'%s\' and username = \'%s\'" % (self.email_entry.get(), self.username.get())
            cursor.execute(sql)
            result = cursor.fetchall()
            if (len(result) != 0):
                messagebox.showerror(title="Error", message="This username or email already exists")

            try:
                print (self.password.get())
                sql = "INSERT INTO zoo_user(email, username, ppassword, usertype) VALUES (\'%s\', \'%s\', MD5(\'%s\'), \'%s\')" % (self.email_entry.get(), self.username.get(), self.password.get(), self.userVar.get())
                cursor.execute(sql)
                if (self.userVar.get() == "staff"):
                    sql = "INSERT INTO staff(email, username) VALUES ('" + self.email_entry.get() + "','" + self.username.get() + "');"
                else:
                    sql = "INSERT INTO visitor(email, username) VALUES ('" + self.email_entry.get() + "','" + self.username.get() + "');"
                cursor.execute(sql)
                db.commit()
                self.reg.destroy()
                self.toLogin()
            except:
                messagebox.showerror(title='Unknown Error', message='Invalid inputs')
    def reg_cancel(self):
        """Helper function for toRegister, cancels registration and returns to main login scree"""
        self.reg.destroy()
        self.toLogin()
    def connect(self):
        """Helper funtion for toLogin, logs in to system"""
        self.user = self.username_entry.get()
        string_user = self.username_entry.get()
        string_pw = self.password_entry.get()
        sql = "SELECT username, ppassword, usertype FROM zoo_user WHERE username=\'%s\' AND ppassword=MD5(\'%s\')" % (string_user, string_pw)
        cursor.execute(sql)
        isUser = cursor.fetchone()
        if isUser:
            sql_email = "SELECT email from zoo_user where username = \'%s\'" % (self.user)
            cursor.execute(sql_email)
            self.email = cursor.fetchone()[0]
            print(self.email)
            if isUser[2] == 'admin':
                self.main.destroy()
                self.adminMenu()

            elif isUser[2] == 'staff':
                self.main.destroy()
                self.staffMenu()
            else:
                self.main.destroy()
                self.visitorMenu()
        else:
            messagebox.showerror(
                title="Error", message="Invalid username/password combination.")
##Go different screen--------------------------------------------------
    def adminMenu(self):
        self.main = Tk()
        self.main.title('ADMIN')
        Label(self.main, text = 'Welcome, Admin ' +
            self.user).grid(row = 0, column = 1, columnspan = 5)
        Button(self.main, text='View Visitors', command = self.admin_view_visitors, width=20).grid(row=1, column=0, columnspan=3, sticky=W, pady=15, padx = 30)
        Button(self.main, text='View Staffs', command = self.admin_view_staffs, width=20).grid(row=2, column=0, columnspan=3, sticky=W, pady=15, padx = 30)
        Button(self.main, text='View Animals', command = self.admin_view_animals, width=20).grid(row=3, column=0, columnspan=3, sticky=W, pady=15, padx = 30)
        Button(self.main, text='View Shows', command = self.admin_view_shows, width=20).grid(row=1, column=5, columnspan=5, sticky=W, pady=15, padx = 30)
        Button(self.main, text='Add Shows', command = self.admin_add_shows, width=20).grid(row=2, column=5, columnspan=5, sticky=W, pady=15, padx = 30)
        Button(self.main, text='Log out', command = self.admin_log_out, width=20).grid(row=4, column=5, columnspan=5, sticky=W, pady=15, padx = 30)
        Button(self.main, text='Add Animal', command = self.admin_add_animal, width=20).grid(row=3, column=5, columnspan=5, sticky=W, pady=15, padx = 30)
        self.main.mainloop()
    def staffMenu(self):
        self.main = Tk()
        self.main.title('STAFF')
        Label(self.main, text='Welcome, Staff ' + self.user).grid(row=0, column=3, columnspan=5, sticky=W, pady=15, padx = 30)
        Button(self.main, text='Search Animals', command = self.staff_search_animals).grid(row=1, column=0, columnspan=5, sticky=W, pady=15, padx = 30)
        Button(self.main, text='View Shows', command = self.staff_view_shows).grid(row=2, column=0, columnspan=5, sticky=W, pady=15, padx = 30)
        Button(self.main, text='Log out', command = self.staff_log_out).grid(row=3, column=0, columnspan=5, sticky=W, pady=15, padx = 30)

        self.main.mainloop()
    def visitorMenu(self):
        self.main = Tk()
        self.main.title('VISITOR')
        Label(self.main, text='Welcome, Visitor ' +
                              self.user).grid(row=0, column=1, columnspan=5)
        Button(self.main, text='Search Exhibits', command = self.visitor_search_exhibits, width=20).grid(row=1, column=0, columnspan=3, sticky=W, pady=15, padx = 30)
        Button(self.main, text='Search Shows', command = self.visitor_search_shows, width=20).grid(row=2, column=0, columnspan=3, sticky=W, pady=15, padx = 30)
        Button(self.main, text='Search Animals', command = self.visitor_search_animals, width=20).grid(row=3, column=0, columnspan=3, sticky=W, pady=15, padx = 30)
        Button(self.main, text='View exhibit history', command = self.visitor_view_exhibit_history, width=20).grid(row=1, column=5, columnspan=5, sticky=W, pady=15, padx = 30)
        Button(self.main, text='View show history', command = self.visitor_view_show_history, width=20).grid(row=2, column=5, columnspan=5, sticky=W, pady=15, padx = 30)
        Button(self.main, text='Log Out', command = self.visitor_log_out, width=20).grid(row=3, column=5, columnspan=5, sticky=W, pady=15, padx = 30)

        self.main.mainloop()

#========================================================================

#                        sort

#========================================================================
## Animal-----------------------------------------
    def sort_animal_name_asc(self):
        print ('animal name asc')
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='age', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        Label(temp_view, text='type', font="Lucida 12 bold ").grid(
            row=1, column=4, sticky=W, padx=10)
        sql = "SELECT nname, species, animalexhibit, age, animal_type from animal %s ORDER BY nname ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            Label(temp_view, text=row[4], padx=10).grid(row=i, column=4, sticky=W)
            i += 1
    def sort_animal_name_desc(self):
        print ('animal name desc')
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='age', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        Label(temp_view, text='type', font="Lucida 12 bold ").grid(
            row=1, column=4, sticky=W, padx=10)
        sql = "SELECT nname, species, animalexhibit, age, animal_type from animal %s ORDER BY nname DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            Label(temp_view, text=row[4], padx=10).grid(row=i, column=4, sticky=W)
            i += 1
    def sort_animal_species_asc(self):
        print ('animal species asc')
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='age', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        Label(temp_view, text='type', font="Lucida 12 bold ").grid(
            row=1, column=4, sticky=W, padx=10)
        sql = "SELECT nname, species, animalexhibit, age, animal_type from animal  %s ORDER BY species ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            Label(temp_view, text=row[4], padx=10).grid(row=i, column=4, sticky=W)
            i += 1
    def sort_animal_species_desc(self):
        print ('animal species desc')
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='age', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        Label(temp_view, text='type', font="Lucida 12 bold ").grid(
            row=1, column=4, sticky=W, padx=10)
        sql = "SELECT nname, species, animalexhibit, age, animal_type from animal %s ORDER BY species DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            Label(temp_view, text=row[4], padx=10).grid(row=i, column=4, sticky=W)
            i += 1
    def sort_animal_exhibit_asc(self):
        print ('animal exhibit asc')
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='age', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        Label(temp_view, text='type', font="Lucida 12 bold ").grid(
            row=1, column=4, sticky=W, padx=10)
        sql = "SELECT nname, species, animalexhibit, age, animal_type from animal %s ORDER BY animalexhibit ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            Label(temp_view, text=row[4], padx=10).grid(row=i, column=4, sticky=W)
            i += 1
    def sort_animal_exhibit_desc(self):
        print ('animal exhibit desc')
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='age', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        Label(temp_view, text='type', font="Lucida 12 bold ").grid(
            row=1, column=4, sticky=W, padx=10)
        sql = "SELECT nname, species, animalexhibit, age, animal_type from animal %s ORDER BY animalexhibit DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            Label(temp_view, text=row[4], padx=10).grid(row=i, column=4, sticky=W)
            i += 1
    def sort_animal_age_asc(self):
        print ('animal age asc')
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='age', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        Label(temp_view, text='type', font="Lucida 12 bold ").grid(
            row=1, column=4, sticky=W, padx=10)
        sql = "SELECT nname, species, animalexhibit, age, animal_type from animal %s ORDER BY age ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            Label(temp_view, text=row[4], padx=10).grid(row=i, column=4, sticky=W)
            i += 1
    def sort_animal_age_desc(self):
        print ('animal age desc')
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='age', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        Label(temp_view, text='type', font="Lucida 12 bold ").grid(
            row=1, column=4, sticky=W, padx=10)
        sql = "SELECT nname, species, animalexhibit, age, animal_type from animal %s ORDER BY age DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            Label(temp_view, text=row[4], padx=10).grid(row=i, column=4, sticky=W)
            i += 1
    def sort_animal_type_asc(self):
        print ('animal type asc')
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='age', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        Label(temp_view, text='type', font="Lucida 12 bold ").grid(
            row=1, column=4, sticky=W, padx=10)
        sql = "SELECT nname, species, animalexhibit, age, animal_type from animal %s ORDER BY animal_type ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            Label(temp_view, text=row[4], padx=10).grid(row=i, column=4, sticky=W)
            i += 1
    def sort_animal_type_desc(self):
        print ('animal type desc')
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='age', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        Label(temp_view, text='type', font="Lucida 12 bold ").grid(
            row=1, column=4, sticky=W, padx=10)
        sql = "SELECT nname, species, animalexhibit, age, animal_type from animal %s ORDER BY animal_type DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            Label(temp_view, text=row[4], padx=10).grid(row=i, column=4, sticky=W)
            i += 1
## Show-----------------------------------------
    def sort_show_name_asc(self):
        temp_view = Tk()
        temp_view.title('Show')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Date', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        sql = "SELECT nname, showexhibit, dateandtime from zoo_show %s ORDER BY nname ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            i += 1
    def sort_show_name_desc(self):
        temp_view = Tk()
        temp_view.title('Show')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Date', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        sql = "SELECT nname, showexhibit, dateandtime from zoo_show %s ORDER BY nname DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            i += 1
    def sort_show_exhibit_asc(self):
        temp_view = Tk()
        temp_view.title('Show')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Date', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        sql = "SELECT nname, showexhibit, dateandtime from zoo_show %s ORDER BY showexhibit ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            i += 1
    def sort_show_exhibit_desc(self):
        temp_view = Tk()
        temp_view.title('Show')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Date', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        sql = "SELECT nname, showexhibit, dateandtime from zoo_show %s ORDER BY showexhibit DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            i += 1
    def sort_show_time_asc(self):
        temp_view = Tk()
        temp_view.title('Show')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Date', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        sql = "SELECT nname, showexhibit, dateandtime from zoo_show %s ORDER BY dateandtime ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            i += 1
    def sort_show_time_desc(self):
        temp_view = Tk()
        temp_view.title('Show')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Date', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        sql = "SELECT nname, showexhibit, dateandtime from zoo_show %s ORDER BY dateandtime DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            i += 1
## Exhibit-----------------------------------------
    def sort_exhibit_name_asc(self):
        temp_view = Tk()
        temp_view.title('Exhibit')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='size', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Number Animals', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='Water', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        sql = "SELECT L.A, L.B, L.C, L.D FROM (SELECT exhibit.nname A, size B, count(animal.nname) C, waterfeature D FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit GROUP BY exhibit.nname) AS L %s ORDER BY L.A ASC" % (self.clause)

        # sql = "SELECT exhibit.nname, size, count(animal.nname), waterfeature FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit %s GROUP BY exhibit.nname ORDER BY exhibit.nname ASC" % (self.clause)
        # sql = "SELECT AH, SIZE, NumAnimals, WF from (SELECT animalexhibit as AH, S.size AS SIZE, count(*) AS NumAnimals, S.waterfeature AS WF from (select animalexhibit, size, waterfeature from (exhibit AS A JOIN animal B) where A.nname = B.animalexhibit) AS S GROUP BY animalexhibit)  AS L %s ORDER BY AH ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            i += 1
    def sort_exhibit_name_desc(self):
        temp_view = Tk()
        temp_view.title('Exhibit')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='size', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Number Animals', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='Water', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        sql = "SELECT L.A, L.B, L.C, L.D FROM (SELECT exhibit.nname A, size B, count(animal.nname) C, waterfeature D FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit GROUP BY exhibit.nname) AS L %s ORDER BY L.A DESC" % (self.clause)
        # sql = "SELECT exhibit.nname, size, count(animal.nname), waterfeature FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit %s GROUP BY exhibit.nname ORDER BY exhibit.nname DESC" % (self.clause)
        # sql = "SELECT AH, SIZE, NumAnimals, WF from (SELECT animalexhibit as AH, S.size AS SIZE, count(*) AS NumAnimals, S.waterfeature AS WF from (select animalexhibit, size, waterfeature from (exhibit AS A JOIN animal B) where A.nname = B.animalexhibit) AS S GROUP BY animalexhibit)  AS L %s ORDER BY AH DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            i += 1
    def sort_exhibit_size_asc(self):
        temp_view = Tk()
        temp_view.title('Exhibit')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='size', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Number Animals', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='Water', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        sql = "SELECT L.A, L.B, L.C, L.D FROM (SELECT exhibit.nname A, size B, count(animal.nname) C, waterfeature D FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit GROUP BY exhibit.nname) AS L %s ORDER BY L.B ASC" % (self.clause)
        # sql = "SELECT exhibit.nname, size, count(animal.nname), waterfeature FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit %s GROUP BY exhibit.nname ORDER BY size ASC" % (self.clause)
        # sql = "SELECT AH, SIZE, NumAnimals, WF from (SELECT animalexhibit as AH, S.size AS SIZE, count(*) AS NumAnimals, S.waterfeature AS WF from (select animalexhibit, size, waterfeature from (exhibit AS A JOIN animal B) where A.nname = B.animalexhibit) AS S GROUP BY animalexhibit)  AS L %s ORDER BY SIZE ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            i += 1
    def sort_exhibit_size_desc(self):
        temp_view = Tk()
        temp_view.title('Exhibit')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='size', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Number Animals', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='Water', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        sql = "SELECT L.A, L.B, L.C, L.D FROM (SELECT exhibit.nname A, size B, count(animal.nname) C, waterfeature D FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit GROUP BY exhibit.nname) AS L %s ORDER BY L.B DESC" % (self.clause)
        # sql = "SELECT exhibit.nname, size, count(animal.nname), waterfeature FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit %s GROUP BY exhibit.nname ORDER BY size DESC" % (self.clause)
        # sql = "SELECT AH, SIZE, NumAnimals, WF from (SELECT animalexhibit as AH, S.size AS SIZE, count(*) AS NumAnimals, S.waterfeature AS WF from (select animalexhibit, size, waterfeature from (exhibit AS A JOIN animal B) where A.nname = B.animalexhibit) AS S GROUP BY animalexhibit)  AS L %s ORDER BY SIZE DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            i += 1
    def sort_exhibit_numAnimals_asc(self):
        temp_view = Tk()
        temp_view.title('Exhibit')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='size', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Number Animals', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='Water', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        sql = "SELECT L.A, L.B, L.C, L.D FROM (SELECT exhibit.nname A, size B, count(animal.nname) C, waterfeature D FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit GROUP BY exhibit.nname) AS L %s ORDER BY L.C ASC" % (self.clause)
        # sql = "SELECT exhibit.nname, size, count(animal.nname), waterfeature FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit %s GROUP BY exhibit.nname ORDER BY count(animal.nname) ASC" % (self.clause)
        # sql = "SELECT AH, SIZE, NumAnimals, WF from (SELECT animalexhibit as AH, S.size AS SIZE, count(*) AS NumAnimals, S.waterfeature AS WF from (select animalexhibit, size, waterfeature from (exhibit AS A JOIN animal B) where A.nname = B.animalexhibit) AS S GROUP BY animalexhibit)  AS L %s ORDER BY NumAnimals ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            i += 1
    def sort_exhibit_numAnimals_desc(self):
        temp_view = Tk()
        temp_view.title('Exhibit')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='size', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Number Animals', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='Water', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        sql = "SELECT L.A, L.B, L.C, L.D FROM (SELECT exhibit.nname A, size B, count(animal.nname) C, waterfeature D FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit GROUP BY exhibit.nname) AS L %s ORDER BY L.C DESC" % (self.clause)
        # sql = "SELECT exhibit.nname, size, count(animal.nname), waterfeature FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit %s GROUP BY exhibit.nname ORDER BY count(animal.nname) DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            i += 1
    def sort_exhibit_waterFeature_asc(self):
        temp_view = Tk()
        temp_view.title('Exhibit')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='size', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Number Animals', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='Water', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        sql = "SELECT L.A, L.B, L.C, L.D FROM (SELECT exhibit.nname A, size B, count(animal.nname) C, waterfeature D FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit GROUP BY exhibit.nname) AS L %s ORDER BY L.D ASC" % (self.clause)
        # sql = "SELECT exhibit.nname, size, count(animal.nname), waterfeature FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit %s GROUP BY exhibit.nname ORDER BY waterfeature ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            i += 1
    def sort_exhibit_waterFeature_desc(self):
        temp_view = Tk()
        temp_view.title('Exhibit')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='size', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Number Animals', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='Water', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        sql = "SELECT L.A, L.B, L.C, L.D FROM (SELECT exhibit.nname A, size B, count(animal.nname) C, waterfeature D FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit GROUP BY exhibit.nname) AS L %s ORDER BY L.D DESC" % (self.clause)
        # sql = "SELECT exhibit.nname, size, count(animal.nname), waterfeature FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit %s GROUP BY exhibit.nname ORDER BY waterfeature DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            i += 1
#========================================================================

#                        admin

#========================================================================
##=======================(admin) view visitors=========================##
    def admin_view_visitors(self):
        self.view_admin_view_visitors = Tk()
        self.view_admin_view_visitors.title('View Visitors')
        view_admin_frame = Frame(self.view_admin_view_visitors)
        view_admin_frame.pack()

        #delete visitor
        self.delete_visitor = Entry(view_admin_frame, width=30, textvariable=StringVar(view_admin_frame, value = 'email'))
        self.delete_visitor.grid(row=1, column = 0, padx = 5)
        button = Button(view_admin_frame, text = "delete", width=10, command = self.helper_admin_view_visitors)
        button.grid(row=1,column=1)

        # backend code
        sql = "SELECT username, email FROM visitor"
        cursor.execute(sql)
        # reivew = cursor.fetchall()
        review = []
        for row in cursor:
            review.append(row)

        # insert chart headers
        Label(view_admin_frame, text='username', font="Lucida 12 bold ").grid(
            row=2, column=0,  sticky=W)
        Label(view_admin_frame, text='email', font="Lucida 12 bold ").grid(
            row=2, column=1, sticky=W)

        i = 3
        for row in review:
            Label(view_admin_frame, text=row[0]).grid(row=i, column=0, sticky=W)
            Label(view_admin_frame, text=row[1]).grid(row=i, column=1, sticky=W)
            i += 1

        # sort
        button = Button(view_admin_frame, text = "Email ASC", width=15, command = self.helper_visitor_email_asc)
        button.grid(row=i,column=1, sticky=W)
        button = Button(view_admin_frame, text = "Email DESC", width=15, command = self.helper_visitor_email_desc)
        button.grid(row=i + 1,column=1, sticky=W)
        button = Button(view_admin_frame, text = "Username ASC", width=15, command = self.helper_visitor_username_asc)
        button.grid(row=i,column=0, sticky=W)
        button = Button(view_admin_frame, text = "Username DESC", width=15, command = self.helper_visitor_username_desc)
        button.grid(row=i + 1,column=0, sticky=W)
    #helpers   
    def helper_visitor_email_asc(self):
        view = Tk()
        view.title('Sorting Ascending by Email')

        sql = "SELECT username, email from visitor ORDER BY email ASC"
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        # insert chart headers
        Label(view, text='username', font="Lucida 12 bold ").grid(
            row=2, column=0,  sticky=W)
        Label(view, text='email', font="Lucida 12 bold ").grid(
            row=2, column=1, sticky=W)

        i = 3
        for row in review:
            Label(view, text=row[0]).grid(row=i, column=0, sticky=W)
            Label(view, text=row[1]).grid(row=i, column=1, sticky=W)
            i += 1
    def helper_visitor_email_desc(self):
        view = Tk()
        view.title('Sorting Descending by Email')

        sql = "SELECT username, email from visitor ORDER BY email DESC"
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        # insert chart headers
        Label(view, text='username', font="Lucida 12 bold ").grid(
            row=2, column=0,  sticky=W)
        Label(view, text='email', font="Lucida 12 bold ").grid(
            row=2, column=1, sticky=W)

        i = 3
        for row in review:
            Label(view, text=row[0]).grid(row=i, column=0, sticky=W)
            Label(view, text=row[1]).grid(row=i, column=1, sticky=W)
            i += 1
    def helper_visitor_username_asc(self):
        view = Tk()
        view.title('Sorting Ascending by Username')

        sql = "SELECT username, email from visitor ORDER BY username ASC"
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        # insert chart headers
        Label(view, text='username', font="Lucida 12 bold ").grid(
            row=2, column=0,  sticky=W)
        Label(view, text='email', font="Lucida 12 bold ").grid(
            row=2, column=1, sticky=W)

        i = 3
        for row in review:
            Label(view, text=row[0]).grid(row=i, column=0, sticky=W)
            Label(view, text=row[1]).grid(row=i, column=1, sticky=W)
            i += 1
    def helper_visitor_username_desc(self): 
        view = Tk()
        view.title('Sorting Decending by Username')

        sql = "SELECT username, email from visitor ORDER BY username DESC"
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        # insert chart headers
        Label(view, text='username', font="Lucida 12 bold ").grid(
            row=2, column=0,  sticky=W)
        Label(view, text='email', font="Lucida 12 bold ").grid(
            row=2, column=1, sticky=W)

        i = 3
        for row in review:
            Label(view, text=row[0]).grid(row=i, column=0, sticky=W)
            Label(view, text=row[1]).grid(row=i, column=1, sticky=W)
            i += 1
    def helper_admin_view_visitors(self):
        sql = "DELETE FROM zoo_user where email = \'%s\'" % (self.delete_visitor.get())
        cursor.execute(sql)
        self.view_admin_view_visitors.destroy()
        db.commit()
##=======================(admin) view staffs===========================##
    def admin_view_staffs(self):
        self.view_admin_view_staffs = Tk()
        self.view_admin_view_staffs.title('View Staffs')

        view = Frame(self.view_admin_view_staffs)
        view.pack()

        #delete staff
        self.delete_staff = Entry(view, width=30, textvariable=StringVar(view, value='email'))
        self.delete_staff.grid(row=1,column=0,padx=5)
        button = Button(view, text="delete", width=10, command=self.helper_admin_view_staffs)
        button.grid(row=1,column=1)

        sql = "SELECT username, email FROM staff"
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        # insert chart headers
        Label(view, text='username', font="Lucida 12 bold ").grid(
            row=2, column=0, sticky=W)
        Label(view, text='email', font="Lucida 12 bold ").grid(
            row=2, column=1, sticky=W)

        i = 3
        for row in review:
            Label(view, text=row[0]).grid(row=i, column=0, sticky=W)
            Label(view, text=row[1]).grid(row=i, column=1, sticky=W)
            i += 1
        button = Button(view, text = "Email ASC", width=15, command = self.helper_staff_email_asc)
        button.grid(row=i,column=1, sticky=W)
        button = Button(view, text = "Email DESC", width=15, command = self.helper_staff_email_desc)
        button.grid(row=i + 1,column=1, sticky=W)
        button = Button(view, text = "Username ASC", width=15, command = self.helper_staff_username_asc)
        button.grid(row=i,column=0, sticky=W)
        button = Button(view, text = "Username DESC", width=15, command = self.helper_staff_username_desc)
        button.grid(row=i + 1,column=0, sticky=W)
    #helpers   
    def helper_staff_email_asc(self):
        view = Tk()
        view.title('Sorting Ascending by Email')

        sql = "SELECT username, email from staff ORDER BY email ASC"
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        # insert chart headers
        Label(view, text='username', font="Lucida 12 bold ").grid(
            row=2, column=0,  sticky=W)
        Label(view, text='email', font="Lucida 12 bold ").grid(
            row=2, column=1, sticky=W)

        i = 3
        for row in review:
            Label(view, text=row[0]).grid(row=i, column=0, sticky=W)
            Label(view, text=row[1]).grid(row=i, column=1, sticky=W)
            i += 1
    def helper_staff_email_desc(self):
        view = Tk()
        view.title('Sorting Descending by Email')

        sql = "SELECT username, email from staff ORDER BY email DESC"
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        # insert chart headers
        Label(view, text='username', font="Lucida 12 bold ").grid(
            row=2, column=0,  sticky=W)
        Label(view, text='email', font="Lucida 12 bold ").grid(
            row=2, column=1, sticky=W)

        i = 3
        for row in review:
            Label(view, text=row[0]).grid(row=i, column=0, sticky=W)
            Label(view, text=row[1]).grid(row=i, column=1, sticky=W)
            i += 1
    def helper_staff_username_asc(self):
        view = Tk()
        view.title('Sorting Ascending by Username')

        sql = "SELECT username, email from staff ORDER BY username ASC"
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        # insert chart headers
        Label(view, text='username', font="Lucida 12 bold ").grid(
            row=2, column=0,  sticky=W)
        Label(view, text='email', font="Lucida 12 bold ").grid(
            row=2, column=1, sticky=W)

        i = 3
        for row in review:
            Label(view, text=row[0]).grid(row=i, column=0, sticky=W)
            Label(view, text=row[1]).grid(row=i, column=1, sticky=W)
            i += 1
    def helper_staff_username_desc(self): 
        view = Tk()
        view.title('Sorting Decending by Username')

        sql = "SELECT username, email from staff ORDER BY username DESC"
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        # insert chart headers
        Label(view, text='username', font="Lucida 12 bold ").grid(
            row=2, column=0,  sticky=W)
        Label(view, text='email', font="Lucida 12 bold ").grid(
            row=2, column=1, sticky=W)

        i = 3
        for row in review:
            Label(view, text=row[0]).grid(row=i, column=0, sticky=W)
            Label(view, text=row[1]).grid(row=i, column=1, sticky=W)
            i += 1
    def helper_admin_view_staffs(self):
        sql = "DELETE FROM zoo_user where email = \'%s\'" % (self.delete_staff.get())
        cursor.execute(sql)
        self.view_admin_view_staffs.destroy()
        db.commit()
##=======================(admin) view animals==========================##
    def admin_view_animals(self):
        self.view_admin_view_animals = Tk()
        self.view_admin_view_animals.title("View Animals")
        view = Frame(self.view_admin_view_animals)
        view.pack()

        #animal search
        Label(view, text='name', font="Lucida 12 bold ", width=15).grid(
            row=1, column=0, sticky=W)
        self.admin_view_animals_name = Entry(view, width=20, textvariable=StringVar(view, value='NAME'))
        self.admin_view_animals_name.grid(row=2,column=0)
        Label(view, text='species', font="Lucida 12 bold ", width=15).grid(
            row=1, column=1, sticky=W)
        self.admin_view_animals_species = Entry(view, width=20, textvariable=StringVar(view, value='SPECIES'))
        self.admin_view_animals_species.grid(row=2,column=1)
        Label(view, text='exhibit', font="Lucida 12 bold ", width=15).grid(
            row=1, column=2, sticky=W)
        self.exhibit_Types2 = {'Jungle','Pacific','Sahara','Mountainous', 'Birds', ''}
        self.admin_view_animals_exhibit_entry = StringVar(view, value='')
        self.admin_view_animals_exhibit = OptionMenu(view, self.admin_view_animals_exhibit_entry, *self.exhibit_Types2)
        self.admin_view_animals_exhibit.grid(row=2,column=2)
        Label(view, text='age', font="Lucida 12 bold ", width=15).grid(
            row=1, column=3, sticky=W)
        self.admin_view_animal_age_min = Entry(view, width=20, textvariable=IntVar(view, value=0))
        self.admin_view_animal_age_min.grid(row=2,column=3,pady=5)
        self.admin_view_animal_age_max = Entry(view, width=20, textvariable=IntVar(view, value=99999999))
        self.admin_view_animal_age_max.grid(row=3,column=3,pady=5)
        Label(view, text='type', font="Lucida 12 bold ", width=15).grid(
            row=1, column=4, sticky=W)
        self.animal_types = {'Mammal', 'Bird', 'Amphibian', 'Reptile', 'Fish', 'Invertebrate', ''}
        self.animal_types_entry = StringVar(view, value='')
        self.admin_view_animals_type = OptionMenu(view, self.animal_types_entry, *self.animal_types)
        self.admin_view_animals_type.grid(row=2,column=4)
        button = Button(view, text='search', width = 20, command=self.helper_admin_view_animals)
        button.grid(row=3,column=0)

        # animal delete
        self.admin_view_animals_name_delete = Entry(view, width=20, textvariable=StringVar(view, value='NAME'))
        self.admin_view_animals_name_delete.grid(row=6,column=0)
        self.admin_view_animals_species_delete = Entry(view, width=20, textvariable=StringVar(view, value='SPECIES'))
        self.admin_view_animals_species_delete.grid(row=6,column=1)
        button = Button(view, text='delete', width = 20, command=self.helper_delete_admin_view_animals)
        button.grid(row=6,column=2)
        db.commit()
    def helper_admin_view_animals(self):
    	# self.view_admin_view_animals = Tk()
        # self.view_admin_view_animals.title("View Animals")
        # view = Frame(self.view_admin_view_animals)
        # view.pack()
        self.view_helper_admin_view_animal = Tk()
        self.view_helper_admin_view_animal.title("View Animals")
        temp_view = Frame(self.view_helper_admin_view_animal)
        temp_view.pack()
        # temp_view = Tk()
        # temp_view.title('Animals')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='age', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        Label(temp_view, text='type', font="Lucida 12 bold ").grid(
            row=1, column=4, sticky=W, padx=10)
        name = self.admin_view_animals_name.get()
        species = self.admin_view_animals_species.get()
        exhibit = self.admin_view_animals_exhibit_entry.get()
        min_age = self.admin_view_animal_age_min.get()
        max_age = self.admin_view_animal_age_max.get()
        animal_type = self.animal_types_entry.get()
        clause = ''
        whereClauseStart = False
        if name != 'NAME':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where nname = \'%s\'" % (name)
            else:
                clause += "and nname = \'%s\'" % (name)
        if species != 'SPECIES':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where species = \'%s\'" % (species)
            else:
                clause += "and species = \'%s\'" % (species)
        if animal_type != '':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where animal_type = \'%s\'" % (animal_type)
            else:
                clause += "and animal_type = \'%s\'" % (animal_type)
        if exhibit != '':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where animalexhibit = \'%s\'" % (exhibit)
            else:
                clause += "and animalexhibit = \'%s\'" % (exhibit)

        if clause == '':
            clause = "where age >= %s and age <= %s" % (min_age, max_age)
        else:
            clause += "and age >= %s and age <= %s" % (min_age, max_age)
            


        sql = "SELECT nname, species, animalexhibit, age, animal_type from animal %s" % (clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        self.sql_admin_view_animals_list = review
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            Label(temp_view, text=row[4], padx=10).grid(row=i, column=4, sticky=W)
            i += 1
        db.commit()
        # sort
        self.clause = clause
        button = Button(temp_view, text = "Name ASC", width=15, command = self.sort_animal_name_asc)
        button.grid(row=i,column=0, sticky=W)
        button = Button(temp_view, text = "Name DESC", width=15, command = self.sort_animal_name_desc)
        button.grid(row=i + 1,column=0, sticky=W)
        button = Button(temp_view, text = "Species ASC", width=15, command = self.sort_animal_species_asc)
        button.grid(row=i,column=1, sticky=W)
        button = Button(temp_view, text = "Species DESC", width=15, command = self.sort_animal_species_desc)
        button.grid(row=i + 1,column=1, sticky=W)
        button = Button(temp_view, text = "Exhibit ASC", width=15, command = self.sort_animal_exhibit_asc)
        button.grid(row=i,column=2, sticky=W)
        button = Button(temp_view, text = "Exhibit DESC", width=15, command = self.sort_animal_exhibit_desc)
        button.grid(row=i + 1,column=2, sticky=W)
        button = Button(temp_view, text = "Age ASC", width=15, command = self.sort_animal_age_asc)
        button.grid(row=i,column=3, sticky=W)
        button = Button(temp_view, text = "Age DESC", width=15, command = self.sort_animal_age_desc)
        button.grid(row=i + 1,column=3, sticky=W)
        button = Button(temp_view, text = "Type ASC", width=15, command = self.sort_animal_type_asc)
        button.grid(row=i,column=4, sticky=W)
        button = Button(temp_view, text = "Type DESC", width=15, command = self.sort_animal_type_desc)
        button.grid(row=i + 1,column=4, sticky=W)
    def helper_delete_admin_view_animals(self):
        name_delete = self.admin_view_animals_name_delete.get()
        species_delete = self.admin_view_animals_species_delete.get()
        sql = "DELETE from animal where nname = \'%s\' and species = \'%s\'" % (name_delete, species_delete)
        cursor.execute(sql)
        db.commit()
        self.view_helper_admin_view_animal.destroy()
        self.view_admin_view_animals.destroy()
##=======================(admin) view shows============================##
    def admin_view_shows(self):
        self.view_shows = Tk()
        self.view_shows.title('View Shows')
        view = Frame(self.view_shows)
        view.pack()

        #search
        Label(view,text='Name').grid(row=1,column=0, sticky = W)
        self.admin_view_shows_searchname = Entry(view, width=20, textvariable=StringVar(view, value = 'NAME'))
        self.admin_view_shows_searchname.grid(row=2,column=0)
        Label(view,text='Exhibit').grid(row=1,column=1, sticky = W)
        self.exhibit_Types1 = {"Jungle","Pacific","Sahara","Mountainous", "Birds", ""}
        self.admin_view_shows_exhibit_entry = StringVar(view, value='')
        self.admin_view_shows_exhibit = OptionMenu(view, self.admin_view_shows_exhibit_entry, *self.exhibit_Types1)
        self.admin_view_shows_exhibit.grid(row=2,column=1)
        Label(view,text='Date').grid(row=1,column=2, sticky = W)
        self.admin_view_shows_date = Entry(view, width = 20, textvariable=StringVar(view, value = 'YYYY-MM-DD'))
        self.admin_view_shows_date.grid(row=2,column=2)
        button = Button(view, text = "search", width=20, command=self.helper_admin_view_shows_search)
        button.grid(row=3,column=0)

        # show delete
        self.admin_view_show_name_delete = Entry(view, width=20, textvariable=StringVar(view, value='NAME'))
        self.admin_view_show_name_delete.grid(row=4,column=0)
        self.admin_view_show_dateandtime_delete = Entry(view, width=20, textvariable=StringVar(view, value='YYYY-MM-DD 00:00:00'))
        self.admin_view_show_dateandtime_delete.grid(row=4,column=1)
        button = Button(view, text='delete', width = 20, command=self.helper_delete_admin_view_show)
        button.grid(row=4,column=2)
        db.commit()
    def helper_delete_admin_view_show(self):
        name = self.admin_view_show_name_delete.get()
        time = self.admin_view_show_dateandtime_delete.get()
        sql = "DELETE FROM zoo_show where nname = \'%s\' and dateandtime = \'%s\'" % (name, time)
        print (sql)
        cursor.execute(sql)
        db.commit()
        self.view_admin_show_result.destroy()
    def helper_admin_view_shows_search(self):
        self.view_admin_show_result = Tk()
        self.view_admin_show_result.title("Shows")
        temp_view = Frame(self.view_admin_show_result)
        temp_view.pack()
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W)
        Label(temp_view, text='date', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W)
        name = self.admin_view_shows_searchname.get()
        exhibit = self.admin_view_shows_exhibit_entry.get()
        date = self.admin_view_shows_date.get()

        clause = ''
        whereClauseStart = False
        if name != 'NAME':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where nname = \'%s\'" %(name)
            else:
                clause += "and nname = \'%s\'" %(name)
        if exhibit != '':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where showexhibit = \'%s\'" %(exhibit)
            else:
                clause += "and showexhibit = \'%s\'" %(exhibit)
        if date != 'YYYY-MM-DD':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where showdate = \'%s\'" %(date)
            else:
                clause += "and showdate = \'%s\'" %(date)

        sql = "SELECT nname, showexhibit, dateandtime from zoo_show %s" % (clause)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        self.clause = clause
        i = 2
        for row in review:
            Label(temp_view, text=row[0]).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1]).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2]).grid(row=i, column=2, sticky=W)
            i += 1
        button = Button(temp_view, text = "Name ASC", width=15, command = self.sort_show_name_asc)
        button.grid(row=i,column=0, sticky=W)
        button = Button(temp_view, text = "Name DESC", width=15, command = self.sort_show_name_desc)
        button.grid(row=i + 1,column=0, sticky=W)
        button = Button(temp_view, text = "Exhibit ASC", width=15, command = self.sort_show_exhibit_asc)
        button.grid(row=i,column=1, sticky=W)
        button = Button(temp_view, text = "Exhibit DESC", width=15, command = self.sort_show_exhibit_desc)
        button.grid(row=i + 1,column=1, sticky=W)
        button = Button(temp_view, text = "Date ASC", width=15, command = self.sort_show_time_asc)
        button.grid(row=i,column=2, sticky=W)
        button = Button(temp_view, text = "Date DESC", width=15, command = self.sort_show_time_desc)
        button.grid(row=i + 1,column=2, sticky=W)
        db.commit()
##=======================(admin) add shows=============================##
    def admin_add_shows(self):
        self.add_shows_view = Tk()
        self.add_shows_view.title('Add Shows')

        view_add_show = Frame(self.add_shows_view)
        view_add_show.pack()

        Label(view_add_show, text="Name:").grid(
        row=1, column=0, sticky=E, pady=5)
        self.showname = Entry(view_add_show, width = 20)
        self.showname.grid(row=1, column = 1, padx=5)


        Label(view_add_show, text="Exhibit:").grid(
            row=2, column=0, sticky=E)
        self.userVar1 = StringVar(view_add_show, value="Jungle")
        self.exhibit_Types = {"Jungle","Pacific","Sahara","Mountainous", "Birds"}
        self.showexhibit = OptionMenu(view_add_show, self.userVar1, *self.exhibit_Types)
        self.showexhibit.grid(row=2, column=1, sticky=W)


        Label(view_add_show, text="Staff:").grid(
            row=3, column=0, sticky=E, pady=5)
        sql = "SELECT email FROM staff"
        cursor.execute(sql)
        staff_list = cursor.fetchall()
        choice = [''] 
        if (len(staff_list) != 0) :
            for element in staff_list:
                choice.append(element[0])
        self.staff_choice = choice
        self.userVar2 = StringVar(view_add_show, value="staff name")
        self.showstaff = OptionMenu(view_add_show, self.userVar2, *self.staff_choice)
        self.showstaff.grid(row=3, column=1, sticky=W)


        Label(view_add_show, text="Date:").grid(
            row=4, column=0, sticky=E, pady=5)
        self.showdata = Entry(view_add_show, width = 20, textvariable=StringVar(view_add_show, value = 'yy/mm/dd'))
        self.showdata.grid(row=4, column = 1, padx=5)

        Label(view_add_show, text="Time:").grid(
            row=5, column=0, sticky=E, pady=5)
        self.showtime = Entry(view_add_show, width = 20, textvariable=StringVar(view_add_show, value = '00:00:00'))
        self.showtime.grid(row=5, column = 1, padx=5)

        buttonframe = Frame(self.add_shows_view)
        buttonframe.pack(anchor=E)
        Button(buttonframe, command=self.helper_admin_add_shows, text='ADD').pack(side=RIGHT)
    def helper_admin_add_shows(self):
        val1 = self.showname.get()
        val2 = self.showdata.get() + ' ' + self.showtime.get()
        val3 = self.userVar1.get()
        val4 = self.userVar2.get()
        sql = "INSERT INTO zoo_show(nname, dateandtime, showexhibit, showstaff, showdate) values(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\')" % (val1, val2, val3, val4, self.showdata.get())
        print(sql)
        if val1 != '' and self.showdata.get() != 'yy/mm/dd':
        	cursor.execute(sql)
        	db.commit()
        	sql_func = "SELECT showdate from zoo_show where nname = \'%s\' and dateandtime = \'%s\'" % (val1, val2)
        	print(sql_func)
        	cursor.execute(sql_func)
        	check_date = cursor.fetchone()[0]
        	print('date: ', check_date)
        	if (check_date == '0000-00-00'):
        		sql = "DELETE FROM zoo_show where nname = \'%s\' and dateandtime = \'%s\'" % (val1, '0000-00-00' + ' ' + self.showtime.get())
        		cursor.execute(sql)
        		db.commit()
        		messagebox.showerror(title="Warning", message="Input Error, Please type again!")
        	else:
        		db.commit()
        		self.add_shows_view.destroy()

        else:
        	messagebox.showerror(title="Warning", message="Input Error, Please type again!")
##=======================(admin) add animal============================##
    def admin_add_animal(self):
        self.view_add_animal = Tk()
        self.view_add_animal.title('Add animal')
        view = Frame(self.view_add_animal)
        view.pack()

        Label(view, text='name', font="Lucida 12 bold ", width=15).grid(
            row=1, column=0, sticky=W)
        self.admin_add_animals_name = Entry(view, width=20, textvariable=StringVar(view, value='NAME'))
        self.admin_add_animals_name.grid(row=2,column=0)
        Label(view, text='species', font="Lucida 12 bold ", width=15).grid(
            row=1, column=1, sticky=W)
        self.admin_add_animals_species = Entry(view, width=20, textvariable=StringVar(view, value='SPECIES'))
        self.admin_add_animals_species.grid(row=2,column=1)
        Label(view, text='exhibit', font="Lucida 12 bold ", width=15).grid(
            row=1, column=2, sticky=W)
        self.exhibit_Types2 = {'Jungle','Pacific','Sahara','Mountainous', 'Birds', ''}
        self.admin_add_animals_exhibit_entry = StringVar(view, value='')
        self.admin_add_animals_exhibit = OptionMenu(view, self.admin_add_animals_exhibit_entry, *self.exhibit_Types2)
        self.admin_add_animals_exhibit.grid(row=2,column=2)
        Label(view, text='age', font="Lucida 12 bold ", width=15).grid(
            row=1, column=3, sticky=W)
        self.admin_add_animal_age = Entry(view, width=20, textvariable=IntVar(view, value=0))
        self.admin_add_animal_age.grid(row=2,column=3,pady=5)
        Label(view, text='type', font="Lucida 12 bold ", width=15).grid(
            row=1, column=4, sticky=W)
        self.animal_types = {'Mammal', 'Bird', 'Amphibian', 'Reptile', 'Fish', 'Invertebrate', ''}
        self.animal_types_entry = StringVar(view, value='')
        self.admin_add_animals_type = OptionMenu(view, self.animal_types_entry, *self.animal_types)
        self.admin_add_animals_type.grid(row=2,column=4)
        button = Button(view, text='add', width = 20, command=self.helper_admin_add_animals)
        button.grid(row=3,column=0)
        db.commit()
    def helper_admin_add_animals(self):
        name = self.admin_add_animals_name.get()
        species = self.admin_add_animals_species.get()
        exhibit = self.admin_add_animals_exhibit_entry.get()
        # print(exhibit)
        age = self.admin_add_animal_age.get()   
        animal_type =self.animal_types_entry.get() 
        sql = "INSERT into animal(nname, species, animal_type, age, animalexhibit) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % (name, species, animal_type, age, exhibit)
        print (sql)
        if name != '' and name != 'NAME' and species != ''and species != 'SPECIES' and exhibit != '' and animal_type != '':
            cursor.execute(sql)
            db.commit()
            self.view_add_animal.destroy()
        else:
        	messagebox.showerror(title="Warning", message="Input Error, Please type again!")
##=======================(admin) log out===============================##
    def admin_log_out(self):
        self.main.destroy()
#========================================================================

#                        visitor

#========================================================================
##=======================(visitor) search exhibits=====================##
    def visitor_search_exhibits(self):
        self.view_visitor_search_exhibits = Tk()
        self.view_visitor_search_exhibits.title('search exhibits')
        view = Frame(self.view_visitor_search_exhibits)
        view.pack()

        #exhibit search
        Label(view, text='Name', font="Lucida 12 bold ", width=15).grid(
            row=1, column=0, sticky=W)
        self.visitor_search_exhibit_name = Entry(view, width=20, textvariable=StringVar(view, value='NAME'))
        self.visitor_search_exhibit_name.grid(row=2,column=0)
        Label(view, text='Water Feature', font="Lucida 12 bold ", width=15).grid(
            row=1, column=1, sticky=W)
        self.visitor_search_exhibit_waterFeature_Entry = StringVar(view, value = '')
        self.water_feature_option = [True, False, '']
        self.visitor_search_exhibit_waterFeature = OptionMenu(view, self.visitor_search_exhibit_waterFeature_Entry, *self.water_feature_option)
        self.visitor_search_exhibit_waterFeature.grid(row=2,column=1)
        Label(view, text='Size Min', font="Lucida 12 bold ", width=15).grid(
            row=1, column=2, sticky=W)
        self.visitor_search_exhibit_size_min = Entry(view, width=20, textvariable=IntVar(view, value=0))
        self.visitor_search_exhibit_size_min.grid(row=2,column=2)
        Label(view, text='Size Max', font="Lucida 12 bold ", width=15).grid(
            row=1, column=3, sticky=W)
        self.visitor_search_exhibit_size_max = Entry(view, width=20, textvariable=IntVar(view, value=9000))
        self.visitor_search_exhibit_size_max.grid(row=2,column=3)
        Label(view, text='Animal number Min', font="Lucida 12 bold ", width=15).grid(
            row=1, column=4, sticky=W)
        self.visitor_search_animal_number_min = Entry(view, width=20, textvariable=IntVar(view, value=0))
        self.visitor_search_animal_number_min.grid(row=2,column=4)
        Label(view, text='Animal number Max', font="Lucida 12 bold ", width=15).grid(
            row=1, column=5, sticky=W)
        self.visitor_search_animal_number_max = Entry(view, width=20, textvariable=IntVar(view, value=100))
        self.visitor_search_animal_number_max.grid(row=2,column=5)

        button = Button(view, text='search', width = 20, command=self.helper_visitor_search_exhibit)
        button.grid(row=3,column=0)
    def helper_visitor_search_exhibit(self):
        temp_view = Tk()
        temp_view.title('exhibit')
        Label(temp_view, text='Name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='Size', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='NumAnimals', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='Water', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)

        name = self.visitor_search_exhibit_name.get()
        waterFeature = self.visitor_search_exhibit_waterFeature_Entry.get()
        size_min = self.visitor_search_exhibit_size_min.get()
        size_max = self.visitor_search_exhibit_size_max.get()
        number_min = self.visitor_search_animal_number_min.get()
        number_max = self.visitor_search_animal_number_max.get()

        clause = ''
        whereClauseStart = False
        if name != 'NAME':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where L.A = \'%s\'" % (name)
            else:
                clause += "and L.A = \'%s\'" % (name)
        if waterFeature != '':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where L.D = \'%s\'" % (waterFeature)
            else:
                clause += "and L.D = \'%s\'" % (waterFeature)
        # if clause != '':
        if not whereClauseStart:
            whereClauseStart = True
            clause = "where L.B >= %s and L.B <= %s and L.C >= %s and L.C <= %s" % (size_min, size_max, number_min, number_max)
        else:
            clause += "and L.B >= %s and L.B <= %s and L.C >= %s and L.C <= %s" % (size_min, size_max, number_min, number_max)
        self.clause = clause;
        sql = "SELECT L.A, L.B, L.C, L.D FROM (SELECT exhibit.nname A, size B, count(animal.nname) C, waterfeature D FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit GROUP BY exhibit.nname) AS L %s" % (clause)
        print (sql)
        cursor.execute(sql)

        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            print(row)
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            i += 1

        #sorting
        i = i + 1
        button = Button(temp_view, text = "name ASC", width=15, command = self.sort_exhibit_name_asc)
        button.grid(row=i,column=0, sticky=W)
        button = Button(temp_view, text = "name DESC", width=15, command = self.sort_exhibit_name_desc)
        button.grid(row=i + 1,column=0, sticky=W)
        button = Button(temp_view, text = "size ASC", width=15, command = self.sort_exhibit_size_asc)
        button.grid(row=i,column=1, sticky=W)
        button = Button(temp_view, text = "size DESC", width=15, command = self.sort_exhibit_size_desc)
        button.grid(row=i + 1,column=1, sticky=W)
        button = Button(temp_view, text = "numAnimals ASC", width=15, command = self.sort_exhibit_numAnimals_asc)
        button.grid(row=i,column=2, sticky=W)
        button = Button(temp_view, text = "numAnimals DESC", width=15, command = self.sort_exhibit_numAnimals_desc)
        button.grid(row=i + 1,column=2, sticky=W)
        button = Button(temp_view, text = "Water ASC", width=15, command = self.sort_exhibit_waterFeature_asc)
        button.grid(row=i,column=3, sticky=W)
        button = Button(temp_view, text = "Water DESC", width=15, command = self.sort_exhibit_waterFeature_desc)
        button.grid(row=i + 1,column=3, sticky=W)
        #exhibit detail
        Label(temp_view, text='Name', font="Lucida 12 bold ").grid(
            row=i+2, column=0, sticky=W, padx=10)
        self.visitor_helper_search_exhibit_name = Entry(temp_view, width=15, textvariable=StringVar(temp_view, value='NAME'))
        self.visitor_helper_search_exhibit_name.grid(row=i+2,column=1)
        button = Button(temp_view, text='Detail', width = 15, command = self.helper_visitor_search_exhibit_detail)
        button.grid(row=i+2,column=2)
    def helper_visitor_search_exhibit_detail(self):
        temp_view = Tk()
        temp_view.title('Exhibit Detail')
        name = self.visitor_helper_search_exhibit_name.get()
        clause = "where L.A = \'%s\'" % (name)
        sql = "SELECT L.A, L.B, L.C, L.D FROM (SELECT exhibit.nname A, size B, count(animal.nname) C, waterfeature D FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit GROUP BY exhibit.nname) AS L %s" % (clause)
        # sql = "SELECT exhibit.nname, size, count(animal.nname), waterfeature FROM exhibit LEFT JOIN animal ON exhibit.nname = animalexhibit %s GROUP BY exhibit.nname" % (clause)
        # sql = "SELECT AH, SIZE, NumAnimals, WF from (SELECT animalexhibit as AH, S.size AS SIZE, count(*) AS NumAnimals, S.waterfeature AS WF from (select animalexhibit, size, waterfeature from (exhibit AS A JOIN animal B) where A.nname = B.animalexhibit) AS S GROUP BY animalexhibit)  AS L %s" % (clause)
        cursor.execute(sql)
        temp_tuple = cursor.fetchone() # holds the exhibit detail
        Label(temp_view, text='Exhibit Name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='Size', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='NumAnimals', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='Water', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)

        Label(temp_view, text=temp_tuple[0]).grid(
            row=2, column=0, sticky=W, padx=10)
        Label(temp_view, text=temp_tuple[1]).grid(
            row=2, column=1, sticky=W, padx=10)
        Label(temp_view, text=temp_tuple[2]).grid(
            row=2, column=2, sticky=W, padx=10)
        Label(temp_view, text=temp_tuple[3]).grid(
            row=2, column=3, sticky=W, padx=10)

        sql = "SELECT nname, species from animal where animalexhibit = \'%s\'" % (name)
        self.clause = "where animalexhibit = \'%s\'" % (name)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        Label(temp_view, text='Animal Name', font="Lucida 12 bold ").grid(
            row=3, column=0, sticky=W, padx=10)
        Label(temp_view, text='Species', font="Lucida 12 bold ").grid(
            row=3, column=1, sticky=W, padx=10)
        i = 4
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            i += 1

        #sort
        button = Button(temp_view, text = "Name ASC", width=15, command = self.sort_visitor_animal_name_asc)
        button.grid(row=i,column=0, sticky=W)
        button = Button(temp_view, text = "Name DESC", width=15, command = self.sort_visitor_animal_name_desc)
        button.grid(row=i + 1,column=0, sticky=W)
        button = Button(temp_view, text = "Species ASC", width=15, command = self.sort_visitor_animal_species_asc)
        button.grid(row=i,column=1, sticky=W)
        button = Button(temp_view, text = "Species DESC", width=15, command = self.sort_visitor_animal_species_desc)
        button.grid(row=i + 1,column=1, sticky=W)

        #log visit
        button = Button(temp_view, text='Log Visit', width = 20, command=self.helper_visitor_search_exhibit_logVisit)
        button.grid(row=i + 1,column=2)

        #animal detail
        Label(temp_view, text='Name', font="Lucida 12 bold ").grid(
            row=i+2, column=0, sticky=W, padx=10)
        self.visitor_helper_search_animal_name = Entry(temp_view, width=20, textvariable=StringVar(temp_view, value='NAME'))
        self.visitor_helper_search_animal_name.grid(row=i+2,column=1)
        button = Button(temp_view, text='Detail', width = 20, command = self.helper_visitor_search_animal_detail)
        button.grid(row=i+2,column=2)
    def sort_visitor_animal_name_asc(self):
        print ('animal name asc')
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        sql = "SELECT nname, species from animal %s ORDER BY nname ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            i += 1
    def sort_visitor_animal_name_desc(self):
        print ('animal name desc')
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        sql = "SELECT nname, species from animal %s ORDER BY nname DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            i += 1
    def sort_visitor_animal_species_asc(self):
        print ('animal species asc')
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        sql = "SELECT nname, species from animal  %s ORDER BY species ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            i += 1
    def sort_visitor_animal_species_desc(self):
        print ('animal species desc')
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        sql = "SELECT nname, species from animal %s ORDER BY species DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            i += 1
    def helper_visitor_search_exhibit_logVisit(self):
        # print (self.user)
        sql = "SELECT email from zoo_user where username = \'%s\'" % (self.user)
        cursor.execute(sql)
        email = cursor.fetchone()[0]
        print (email)
        sql_time = "SELECT NOW()"
        cursor.execute(sql_time)
        time = cursor.fetchone()[0]
        exhibit = self.visitor_helper_search_exhibit_name.get()
        print (exhibit)
        print (time)
        sql_func = "INSERT into exhibitvisits(email, nname, dateandtime) values (\'%s\',\'%s\',\'%s\')" % (email, exhibit, time)
        cursor.execute(sql_func)
        db.commit()
        # print ("helper_visitor_search_exhibit_logVisit")
    def helper_visitor_search_animal_detail(self):
        temp_view = Tk()
        temp_view.title('Animal Detail')
        name = self.visitor_helper_search_animal_name.get()
        Label(temp_view, text='name', font="Lucida 12 bold ", width=15).grid(
            row=1, column=0)
        Label(temp_view, text='species', font="Lucida 12 bold ", width=15).grid(
            row=1, column=1)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ", width=15).grid(
            row=1, column=2)
        Label(temp_view, text='age', font="Lucida 12 bold ", width=15).grid(
            row=1, column=3)
        Label(temp_view, text='type', font="Lucida 12 bold ", width=15).grid(
            row=1, column=4)
        sql = "SELECT * from animal where nname = \'%s\'" % (name)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3)
            Label(temp_view, text=row[4], padx=10).grid(row=i, column=4)
            i += 1
##=======================(visitor) search shows========================##
    def visitor_search_shows(self):
        self.view_visitor_search_shows = Tk()
        self.view_visitor_search_shows.title('search shows - Visitor')
        view = Frame(self.view_visitor_search_shows)
        view.pack()

        #search
        Label(view,text='Name').grid(row=1,column=0, sticky = W)
        self.visitor_view_shows_searchname = Entry(view, width=20, textvariable=StringVar(view, value = 'NAME'))
        self.visitor_view_shows_searchname.grid(row=2,column=0)
        Label(view,text='Exhibit').grid(row=1,column=1, sticky = W)
        self.exhibit_Types1 = {"Jungle","Pacific","Sahara","Mountainous", "Birds", ""}
        self.visitor_view_shows_exhibit_entry = StringVar(view, value='')
        self.visitor_view_shows_exhibit = OptionMenu(view, self.visitor_view_shows_exhibit_entry, *self.exhibit_Types1)
        self.visitor_view_shows_exhibit.grid(row=2,column=1)
        Label(view,text='Date').grid(row=1,column=2, sticky = W)
        self.visitor_view_shows_date = Entry(view, width = 20, textvariable=StringVar(view, value = 'YYYY-MM-DD'))
        self.visitor_view_shows_date.grid(row=2,column=2)
        button = Button(view, text = "search", width=20, command=self.helper_visitor_search_show)
        button.grid(row=3,column=0)
    def helper_visitor_search_show(self):
        temp_view = Tk()
        temp_view.title("Shows")
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W)
        Label(temp_view, text='date', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W)

        #pick a specific one
        
        self.helper_visitor_view_shows_name = Entry(temp_view, width=20, textvariable=StringVar(temp_view, value = 'NAME'))
        self.helper_visitor_view_shows_name.grid(row=2,column=0, sticky=W)
       
        self.helper_visitor_view_shows_time = Entry(temp_view, width=20, textvariable=StringVar(temp_view, value = 'YYYY-MM-DD 00:00:00'))
        self.helper_visitor_view_shows_time.grid(row=2,column=1, sticky=W)

        button = Button(temp_view, text = "Log Visit", width=20, command=self.helper_visitor_log_show)
        button.grid(row=2,column=2)

        name = self.visitor_view_shows_searchname.get()
        exhibit = self.visitor_view_shows_exhibit_entry.get()
        date = self.visitor_view_shows_date.get()

        clause = ''
        whereClauseStart = False
        if name != 'NAME':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where nname = \'%s\'" %(name)
            else:
                clause += "and nname = \'%s\'" %(name)
        if exhibit != '':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where showexhibit = \'%s\'" %(exhibit)
            else:
                clause += "and showexhibit = \'%s\'" %(exhibit)
        if date != 'YYYY-MM-DD':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where showdate = \'%s\'" %(date)
            else:
                clause += "and showdate = \'%s\'" %(date)

        sql = "SELECT nname, showexhibit, dateandtime from zoo_show %s" % (clause)
        self.clause = clause
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        i = 3
        for row in review:
            Label(temp_view, text=row[0]).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1]).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2]).grid(row=i, column=2, sticky=W)
            i += 1
        button = Button(temp_view, text = "Name ASC", width=15, command = self.sort_show_name_asc)
        button.grid(row=i,column=0, sticky=W)
        button = Button(temp_view, text = "Name DESC", width=15, command = self.sort_show_name_desc)
        button.grid(row=i + 1,column=0, sticky=W)
        button = Button(temp_view, text = "Exhibit ASC", width=15, command = self.sort_show_exhibit_asc)
        button.grid(row=i,column=1, sticky=W)
        button = Button(temp_view, text = "Exhibit DESC", width=15, command = self.sort_show_exhibit_desc)
        button.grid(row=i + 1,column=1, sticky=W)
        button = Button(temp_view, text = "Date ASC", width=15, command = self.sort_show_time_asc)
        button.grid(row=i,column=2, sticky=W)
        button = Button(temp_view, text = "Date DESC", width=15, command = self.sort_show_time_desc)
        button.grid(row=i + 1,column=2, sticky=W)
    def helper_visitor_log_show(self):
        sql_email = "SELECT email from visitor where username = \'%s\'" % (self.user)
        cursor.execute(sql_email)
        email = cursor.fetchone()[0]
        name = self.helper_visitor_view_shows_name.get()
        time = self.helper_visitor_view_shows_time.get()
        sql_func = "INSERT INTO showvisits(email, nname, dateandtime) values (\'%s\',\'%s\',\'%s\')" % (email, name, time)
        cursor.execute(sql_func)
        db.commit()
##=======================(visitor) search for animals==================##
    def visitor_search_animals(self):
        self.view_visitor_search_animals = Tk()
        self.view_visitor_search_animals.title('search animals')
        view = Frame(self.view_visitor_search_animals)
        view.pack()
        #animal search
        Label(view, text='name', font="Lucida 12 bold ", width=15).grid(
            row=1, column=0, sticky=W)
        self.visitor_view_animals_name = Entry(view, width=20, textvariable=StringVar(view, value='NAME'))
        self.visitor_view_animals_name.grid(row=2,column=0)
        Label(view, text='species', font="Lucida 12 bold ", width=15).grid(
            row=1, column=1, sticky=W)
        self.visitor_view_animals_species = Entry(view, width=20, textvariable=StringVar(view, value='SPECIES'))
        self.visitor_view_animals_species.grid(row=2,column=1)
        Label(view, text='exhibit', font="Lucida 12 bold ", width=15).grid(
            row=1, column=2, sticky=W)
        self.exhibit_Types2 = {'Jungle','Pacific','Sahara','Mountainous', 'Birds', ''}
        self.visitor_view_animals_exhibit_entry = StringVar(view, value='')
        self.visitor_view_animals_exhibit = OptionMenu(view, self.visitor_view_animals_exhibit_entry, *self.exhibit_Types2)
        self.visitor_view_animals_exhibit.grid(row=2,column=2)
        Label(view, text='age', font="Lucida 12 bold ", width=15).grid(
            row=1, column=3, sticky=W)
        self.visitor_view_animal_age_min = Entry(view, width=20, textvariable=IntVar(view, value=0))
        self.visitor_view_animal_age_min.grid(row=2,column=3,pady=5)
        self.visitor_view_animal_age_max = Entry(view, width=20, textvariable=IntVar(view, value=100))
        self.visitor_view_animal_age_max.grid(row=3,column=3,pady=5)
        Label(view, text='type', font="Lucida 12 bold ", width=15).grid(
            row=1, column=4, sticky=W)
        self.animal_types = {'Mammal', 'Bird', 'Amphibian', 'Reptile', 'Fish', 'Invertebrate', ''}
        self.animal_types_entry = StringVar(view, value='')
        self.visitor_view_animals_type = OptionMenu(view, self.animal_types_entry, *self.animal_types)
        self.visitor_view_animals_type.grid(row=2,column=4)
        button = Button(view, text='search', width = 20, command=self.helper_visitor_view_animals)
        button.grid(row=3,column=0)
    def helper_visitor_view_animals(self):
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        Label(temp_view, text='age', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W, padx=10)
        Label(temp_view, text='type', font="Lucida 12 bold ").grid(
            row=1, column=4, sticky=W, padx=10)
        name = self.visitor_view_animals_name.get()
        species = self.visitor_view_animals_species.get()
        exhibit = self.visitor_view_animals_exhibit_entry.get()
        min_age = self.visitor_view_animal_age_min.get()
        max_age = self.visitor_view_animal_age_max.get()
        animal_type = self.animal_types_entry.get()
        clause = ''
        whereClauseStart = False
        if name != 'NAME':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where nname = \'%s\'" % (name)
            else:
                clause += "and nname = \'%s\'" % (name)
        if species != 'SPECIES':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where species = \'%s\'" % (species)
            else:
                clause += "and species = \'%s\'" % (species)
        if animal_type != '':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where animal_type = \'%s\'" % (animal_type)
            else:
                clause += "and animal_type = \'%s\'" % (animal_type)
        if exhibit != '':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where animalexhibit = \'%s\'" % (exhibit)
            else:
                clause += "and animalexhibit = \'%s\'" % (exhibit)
        if clause == '':
            clause = "where age >= %s and age <= %s" % (min_age, max_age)
        else:
            clause += "and age >= %s and age <= %s" % (min_age, max_age)


        sql = "SELECT nname, species, animalexhibit, age, animal_type from animal %s" % (clause)
        # print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3], padx=10).grid(row=i, column=3, sticky=W)
            Label(temp_view, text=row[4], padx=10).grid(row=i, column=4, sticky=W)
            i += 1
         # sort
        self.clause = clause
        button = Button(temp_view, text = "Name ASC", width=15, command = self.sort_animal_name_asc)
        button.grid(row=i,column=0, sticky=W)
        button = Button(temp_view, text = "Name DESC", width=15, command = self.sort_animal_name_desc)
        button.grid(row=i + 1,column=0, sticky=W)
        button = Button(temp_view, text = "Species ASC", width=15, command = self.sort_animal_species_asc)
        button.grid(row=i,column=1, sticky=W)
        button = Button(temp_view, text = "Species DESC", width=15, command = self.sort_animal_species_desc)
        button.grid(row=i + 1,column=1, sticky=W)
        button = Button(temp_view, text = "Exhibit ASC", width=15, command = self.sort_animal_exhibit_asc)
        button.grid(row=i,column=2, sticky=W)
        button = Button(temp_view, text = "Exhibit DESC", width=15, command = self.sort_animal_exhibit_desc)
        button.grid(row=i + 1,column=2, sticky=W)
        button = Button(temp_view, text = "Age ASC", width=15, command = self.sort_animal_age_asc)
        button.grid(row=i,column=3, sticky=W)
        button = Button(temp_view, text = "Age DESC", width=15, command = self.sort_animal_age_desc)
        button.grid(row=i + 1,column=3, sticky=W)
        button = Button(temp_view, text = "Type ASC", width=15, command = self.sort_animal_type_asc)
        button.grid(row=i,column=4, sticky=W)
        button = Button(temp_view, text = "Type DESC", width=15, command = self.sort_animal_type_desc)
        button.grid(row=i + 1,column=4, sticky=W)
##=======================(visitor) view exhibit history================##
    def visitor_view_exhibit_history(self):
        self.view_exhibit_history = Tk()
        self.view_exhibit_history.title('exhibit history')
        view = Frame(self.view_exhibit_history)
        view.pack()

        #animal search
        Label(view, text='name', font="Lucida 12 bold ", width=15).grid(
            row=1, column=0, sticky=W, padx = 20)
        self.visitor_view_exhibit_name = Entry(view, width=20, textvariable=StringVar(view, value='NAME'))
        self.visitor_view_exhibit_name.grid(row=2,column=0, padx = 15)
        Label(view, text='Time', font="Lucida 12 bold ", width=15).grid(
            row=1, column=1, sticky=W, padx = 20)
        self.visitor_view_exhibit_time = Entry(view, width=20, textvariable=StringVar(view, value='YYYY-MM-DD 00:00:00'))
        self.visitor_view_exhibit_time.grid(row=2,column=1, padx = 15)
        Label(view, text='Number of Visits Max', font="Lucida 12 bold ", width=20).grid(
            row=1, column=2, sticky=W, padx = 20)
        self.visitor_view_exhibit_maxNum_entry = Entry(view, width=20, textvariable=IntVar(view, value=100))
        self.visitor_view_exhibit_maxNum_entry.grid(row=2,column=2, padx = 15)
        Label(view, text='Number of Visits Min', font="Lucida 12 bold ", width=20).grid(
            row=1, column=3, sticky=W, padx = 20)
        self.visitor_view_exhibit_minNum_entry = Entry(view, width=20, textvariable=IntVar(view, value=0))
        self.visitor_view_exhibit_minNum_entry.grid(row=2,column=3, padx = 15)
        button = Button(view, text='search', width = 20, command=self.helper_visitor_exhibit_history)
        button.grid(row=3,column=0, pady = 5)
    def helper_visitor_exhibit_history(self):
        temp_view = Tk()
        temp_view.title("History")
        Label(temp_view, text='Name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx = 10)
        Label(temp_view, text='Time', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx = 10)
        Label(temp_view, text='Number of Visits', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx = 10)

        name = self.visitor_view_exhibit_name.get()      
        time = self.visitor_view_exhibit_time.get()
        maxNum = self.visitor_view_exhibit_maxNum_entry.get()  
        minNum = self.visitor_view_exhibit_minNum_entry.get()
        clause = 'WHERE email = \'%s\'' % (self.email)
        whereClauseStart = False
        if name != 'NAME':
            clause += "and A.nname = \'%s\'" % (name)
        if time != 'YYYY-MM-DD 00:00:00':
            clause += "and A.dateandtime = \'%s\'" % (time)
        if not whereClauseStart:
            clause += "and B.count >= %s and B.count <= %s" % (minNum, maxNum)

        sql = "SELECT A.nname, A.dateandtime, B.count FROM exhibitvisits A INNER JOIN ((SELECT nname, count(*) as count FROM exhibitvisits GROUP BY nname)AS B)on A.nname = B.nname %s" % (clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        i = 3
        for row in review:
            Label(temp_view, text=row[0]).grid(row=i, column=0, sticky=W, padx = 10)
            Label(temp_view, text=row[1]).grid(row=i, column=1, sticky=W, padx = 10)
            Label(temp_view, text=row[2]).grid(row=i, column=2, sticky=W)
            i += 1
        # sort
        self.clause = clause
        button = Button(temp_view, text = "Name ASC", width=15, command = self.sort_exhibit_history_name_asc)
        button.grid(row=i,column=0, sticky=W)
        button = Button(temp_view, text = "Name DESC", width=15, command = self.sort_exhibit_history_name_desc)
        button.grid(row=i + 1,column=0, sticky=W)
        button = Button(temp_view, text = "Time ASC", width=15, command = self.sort_exhibit_history_time_asc)
        button.grid(row=i,column=1, sticky=W)
        button = Button(temp_view, text = "Time DESC", width=15, command = self.sort_exhibit_history_time_desc)
        button.grid(row=i + 1,column=1, sticky=W)
    def sort_exhibit_history_name_asc(self):
        temp_view = Tk()
        temp_view.title("History")
        Label(temp_view, text='Name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx = 10)
        Label(temp_view, text='Time', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx = 10)
        Label(temp_view, text='Number of Visits', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx = 10)
        sql = "SELECT A.nname, A.dateandtime, B.count FROM exhibitvisits A INNER JOIN ((SELECT nname, count(*) as count FROM exhibitvisits GROUP BY nname)AS B)on A.nname = B.nname %s order by A.nname asc" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        i = 3
        for row in review:
            Label(temp_view, text=row[0]).grid(row=i, column=0, sticky=W, padx = 10)
            Label(temp_view, text=row[1]).grid(row=i, column=1, sticky=W, padx = 10)
            Label(temp_view, text=row[2]).grid(row=i, column=2, sticky=W)
            i += 1
    def sort_exhibit_history_name_desc(self):
        temp_view = Tk()
        temp_view.title("History")
        Label(temp_view, text='Name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx = 10)
        Label(temp_view, text='Time', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx = 10)
        Label(temp_view, text='Number of Visits', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx = 10)
        sql = "SELECT A.nname, A.dateandtime, B.count FROM exhibitvisits A INNER JOIN ((SELECT nname, count(*) as count FROM exhibitvisits GROUP BY nname)AS B)on A.nname = B.nname %s order by A.nname desc" % (self.clause)  
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        i = 3
        for row in review:
            Label(temp_view, text=row[0]).grid(row=i, column=0, sticky=W, padx = 10)
            Label(temp_view, text=row[1]).grid(row=i, column=1, sticky=W, padx = 10)
            Label(temp_view, text=row[2]).grid(row=i, column=2, sticky=W)
            i += 1
    def sort_exhibit_history_time_asc(self):
        temp_view = Tk()
        temp_view.title("History")
        Label(temp_view, text='Name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx = 10)
        Label(temp_view, text='Time', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx = 10)
        Label(temp_view, text='Number of Visits', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx = 10)
        sql = "SELECT A.nname, A.dateandtime, B.count FROM exhibitvisits A INNER JOIN ((SELECT nname, count(*) as count FROM exhibitvisits GROUP BY nname)AS B)on A.nname = B.nname %s order by A.dateandtime asc" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        i = 3
        for row in review:
            Label(temp_view, text=row[0]).grid(row=i, column=0, sticky=W, padx = 10)
            Label(temp_view, text=row[1]).grid(row=i, column=1, sticky=W, padx = 10)
            Label(temp_view, text=row[2]).grid(row=i, column=2, sticky=W)
            i += 1
    def sort_exhibit_history_time_desc(self):
        temp_view = Tk()
        temp_view.title("History")
        Label(temp_view, text='Name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx = 10)
        Label(temp_view, text='Time', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx = 10)
        Label(temp_view, text='Number of Visits', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx = 10)
        sql = "SELECT A.nname, A.dateandtime, B.count FROM exhibitvisits A INNER JOIN ((SELECT nname, count(*) as count FROM exhibitvisits GROUP BY nname)AS B)on A.nname = B.nname %s order by A.dateandtime desc" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        i = 3
        for row in review:
            Label(temp_view, text=row[0]).grid(row=i, column=0, sticky=W, padx = 10)
            Label(temp_view, text=row[1]).grid(row=i, column=1, sticky=W, padx = 10)
            Label(temp_view, text=row[2]).grid(row=i, column=2, sticky=W)
            i += 1
##=======================(visitor) view show history===================##
    def visitor_view_show_history(self):
        self.view_show_history = Tk()
        self.view_show_history.title('show history')
        view = Frame(self.view_show_history)
        view.pack()

        #search
        Label(view,text='Name', width = 20).grid(row=1,column=0, sticky = W, padx = 5, pady = 10)
        self.visitor_view_shows_searchname = Entry(view, width=20, textvariable=StringVar(view, value = 'NAME'))
        self.visitor_view_shows_searchname.grid(row=2,column=0)
        Label(view,text='Exhibit', width = 20).grid(row=1,column=1, sticky = W, padx = 5, pady = 10)
        self.exhibit_Types1 = {"Jungle","Pacific","Sahara","Mountainous", "Birds", ""}
        self.visitor_view_shows_exhibit_entry = StringVar(view, value='')
        self.visitor_view_shows_exhibit = OptionMenu(view, self.visitor_view_shows_exhibit_entry, *self.exhibit_Types1)
        self.visitor_view_shows_exhibit.grid(row=2,column=1)
        Label(view,text='Date', width = 20).grid(row=1,column=2, sticky = W, padx = 5, pady = 10)
        self.visitor_view_shows_date = Entry(view, width = 20, textvariable=StringVar(view, value = 'YYYY-MM-DD'))
        self.visitor_view_shows_date.grid(row=2,column=2)
        button = Button(view, text = "search", width=20, command=self.helper_visitor_view_shows_search)
        button.grid(row=3,column=0, padx = 5, pady = 10)
    def helper_visitor_view_shows_search(self):
        temp_view = Tk()
        temp_view.title("Shows")
        Label(temp_view, text='name', font="Lucida 12 bold ", width = 20).grid(
            row=1, column=0, sticky=W, padx = 5)
        Label(temp_view, text='date', font="Lucida 12 bold ", width = 20).grid(
            row=1, column=1, sticky=W, padx = 5)
        Label(temp_view, text='exhibit', font="Lucida 12 bold ", width = 20).grid(
            row=1, column=2, sticky=W, padx = 5)
        name = self.visitor_view_shows_searchname.get()
        exhibit = self.visitor_view_shows_exhibit_entry.get()
        date = self.visitor_view_shows_date.get()

        clause = 'WHERE A.nname = B.nname and A.email = \'%s\'' % (self.email)
        if name != 'NAME':
            clause += "and B.nname = \'%s\'" %(name)
        if exhibit != '':
            clause += "and B.showexhibit = \'%s\'" %(exhibit)
        if date != 'YYYY-MM-DD':    
            clause += "and B.showdate = \'%s\'" %(date)
        sql = "SELECT B.nname, A.dateandtime, B.showexhibit FROM (showvisits A JOIN zoo_show B) %s" % (clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        i = 2
        for row in review:
            Label(temp_view, text=row[0], width = 20).grid(row=i, column=0, sticky=W, padx = 2, pady = 5)
            Label(temp_view, text=row[1], width = 20).grid(row=i, column=1, sticky=W, padx = 2, pady = 5)
            Label(temp_view, text=row[2], width = 20).grid(row=i, column=2, sticky=W, padx = 2, pady = 5)
            i += 1
        # sort
        self.clause = clause
        button = Button(temp_view, text = "Name ASC", width=15, command = self.sort_show_history_name_asc)
        button.grid(row=i,column=0, sticky=W)
        button = Button(temp_view, text = "Name DESC", width=15, command = self.sort_show_history_name_desc)
        button.grid(row=i + 1,column=0, sticky=W)
        button = Button(temp_view, text = "Time ASC", width=15, command = self.sort_show_history_time_asc)
        button.grid(row=i,column=1, sticky=W)
        button = Button(temp_view, text = "Time DESC", width=15, command = self.sort_show_history_time_desc)
        button.grid(row=i + 1,column=1, sticky=W)
    def sort_show_history_name_asc(self):
        temp_view = Tk()
        temp_view.title("History")
        Label(temp_view, text='Name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx = 10)
        Label(temp_view, text='Time', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx = 10)
        Label(temp_view, text='Number of Visits', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx = 10)
        sql = "SELECT B.nname, A.dateandtime, B.showexhibit FROM (showvisits A JOIN zoo_show B) %s ORDER BY B.nname asc" % (self.clause)
        # sql = "SELECT nname, showexhibit, dateandtime from zoo_show %s ORDER BY nname ASC" % (self.clause)        
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        i = 3
        for row in review:
            Label(temp_view, text=row[0]).grid(row=i, column=0, sticky=W, padx = 10)
            Label(temp_view, text=row[1]).grid(row=i, column=1, sticky=W, padx = 10)
            Label(temp_view, text=row[2]).grid(row=i, column=2, sticky=W)
            i += 1
    def sort_show_history_name_desc(self):
        temp_view = Tk()
        temp_view.title("History")
        Label(temp_view, text='Name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx = 10)
        Label(temp_view, text='Time', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx = 10)
        Label(temp_view, text='Number of Visits', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx = 10)
        sql = "SELECT B.nname, A.dateandtime, B.showexhibit FROM (showvisits A JOIN zoo_show B) %s ORDER BY B.nname desc" % (self.clause)
        # sql = "SELECT nname, showexhibit, dateandtime from zoo_show %s ORDER BY nname DESC" % (self.clause) 
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        i = 3
        for row in review:
            Label(temp_view, text=row[0]).grid(row=i, column=0, sticky=W, padx = 10)
            Label(temp_view, text=row[1]).grid(row=i, column=1, sticky=W, padx = 10)
            Label(temp_view, text=row[2]).grid(row=i, column=2, sticky=W)
            i += 1
    def sort_show_history_time_asc(self):
        temp_view = Tk()
        temp_view.title("History")
        Label(temp_view, text='Name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx = 10)
        Label(temp_view, text='Time', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx = 10)
        Label(temp_view, text='Number of Visits', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx = 10)
        sql = "SELECT B.nname, A.dateandtime, B.showexhibit FROM (showvisits A JOIN zoo_show B) %s ORDER BY A.dateandtime asc" % (self.clause)
        # sql = "SELECT nname, showexhibit, dateandtime from zoo_show %s ORDER BY dateandtime ASC" % (self.clause) 
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        i = 3
        for row in review:
            Label(temp_view, text=row[0]).grid(row=i, column=0, sticky=W, padx = 10)
            Label(temp_view, text=row[1]).grid(row=i, column=1, sticky=W, padx = 10)
            Label(temp_view, text=row[2]).grid(row=i, column=2, sticky=W)
            i += 1
    def sort_show_history_time_desc(self):
        temp_view = Tk()
        temp_view.title("History")
        Label(temp_view, text='Name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx = 10)
        Label(temp_view, text='Time', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx = 10)
        Label(temp_view, text='Number of Visits', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx = 10)
        # sql = "SELECT nname, showexhibit, dateandtime from zoo_show %s ORDER BY dateandtime DESC" % (self.clause) 
        sql = "SELECT B.nname, A.dateandtime, B.showexhibit FROM (showvisits A JOIN zoo_show B) %s ORDER BY A.dateandtime desc" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        i = 3
        for row in review:
            Label(temp_view, text=row[0]).grid(row=i, column=0, sticky=W, padx = 10)
            Label(temp_view, text=row[1]).grid(row=i, column=1, sticky=W, padx = 10)
            Label(temp_view, text=row[2]).grid(row=i, column=2, sticky=W)
            i += 1
##=======================(visitor) log out=============================##
    def visitor_log_out(self):
        self.main.destroy()
#========================================================================

#                        staff

#========================================================================
##=======================(staff) log out===============================##
    def staff_log_out(self):
        self.main.destroy()
##=======================(staff) view shows============================##
    def staff_view_shows(self):
        self.staff_view_shows = Tk()
        self.staff_view_shows.title('View Shows')
        view_show_frame = Frame(self.staff_view_shows)
        view_show_frame.pack()

        # backend code
        sql = "SELECT nname, showexhibit, dateandtime FROM zoo_show where showstaff = \'%s\'" % (self.email)
        print (sql)
        cursor.execute(sql)
        # reivew = cursor.fetchall()
        review = []
        for row in cursor:
            review.append(row)

        # insert chart headers
        Label(view_show_frame, text='Name', font="Lucida 12 bold ").grid(
            row=1, column=0,  sticky=W)
        Label(view_show_frame, text='Exhibit', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W)
        Label(view_show_frame, text='Time', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W)

        i = 2
        for row in review:
            Label(view_show_frame, text=row[0]).grid(row=i, column=0, sticky=W)
            Label(view_show_frame, text=row[1]).grid(row=i, column=1, sticky=W)
            Label(view_show_frame, text=row[2]).grid(row=i, column=2, sticky=W)
            i += 1

        #sort
        self.clause = "where showstaff = \'%s\'" % (self.email)
        button = Button(view_show_frame, text = "Name ASC", width=15, command = self.sort_show_name_asc)
        button.grid(row=i,column=0, sticky=W)
        button = Button(view_show_frame, text = "Name DESC", width=15, command = self.sort_show_name_desc)
        button.grid(row=i + 1,column=0, sticky=W)
        button = Button(view_show_frame, text = "Exhibit ASC", width=15, command = self.sort_show_exhibit_asc)
        button.grid(row=i,column=1, sticky=W)
        button = Button(view_show_frame, text = "Exhibit DESC", width=15, command = self.sort_show_exhibit_desc)
        button.grid(row=i + 1,column=1, sticky=W)
        button = Button(view_show_frame, text = "Date ASC", width=15, command = self.sort_show_time_asc)
        button.grid(row=i,column=2, sticky=W)
        button = Button(view_show_frame, text = "Date DESC", width=15, command = self.sort_show_time_desc)
        button.grid(row=i + 1,column=2, sticky=W)
##=======================(staff) search animals========================##
    def staff_search_animals(self):
        self.staff_search_animals = Tk()
        self.staff_search_animals.title('Search animals')
        view = Frame(self.staff_search_animals)
        view.pack()

        #search
        Label(view,text='Name').grid(row=1,column=0, sticky = W)
        self.staff_view_shows_searchname = Entry(view, width=20, textvariable=StringVar(view, value = 'NAME'))
        self.staff_view_shows_searchname.grid(row=2,column=0)

        Label(view,text='Species').grid(row=1,column=1, sticky = W)
        self.staff_view_shows_searchspecies = Entry(view, width=20, textvariable=StringVar(view, value = 'SPECIES'))
        self.staff_view_shows_searchspecies.grid(row=2,column=1)

        Label(view,text='Exhibit').grid(row=1,column=2, sticky = W)
        self.exhibit_Types1 = {'Jungle','Pacific','Sahara','Mountainous', 'Birds', ''}
        self.staff_view_exhibit_entry = StringVar(view,value='')
        self.staff_view_exhibit = OptionMenu(view, self.staff_view_exhibit_entry, *self.exhibit_Types1)
        self.staff_view_exhibit.grid(row=2,column=2)

        Label(view,text='Age').grid(row=1, column=3, sticky = W)
        self.min_age_entry = Entry(view, width=10, textvariable=IntVar(view, value = 0))
        self.min_age_entry.grid(row=2, column=3)
        self.max_age_entry = Entry(view, width=10, textvariable=IntVar(view, value = 100))
        self.max_age_entry.grid(row=3, column=3)

        Label(view,text='Type').grid(row=1,column=4, sticky = W)
        self.animal_Types1 = {'Fish','Bird','Reptile','Mammal', 'Amphibian', 'Invertebrate', ''}
        self.staff_view_animal_entry = StringVar(view, value='')
        self.staff_view_animal = OptionMenu(view, self.staff_view_animal_entry, *self.animal_Types1)
        self.staff_view_animal.grid(row=2,column=4)
        button = Button(view, text = "search", width=20, command=self.helper_staff_search_animal)
        button.grid(row=4,column=0)       
    def helper_staff_search_animal(self):
        temp_view = Tk()
        temp_view.title("Animals")
        Label(temp_view, text='Name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W)
        Label(temp_view, text='Species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W)
        Label(temp_view, text='Exhibit', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W)
        Label(temp_view, text='Age', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W)
        Label(temp_view, text='Type', font="Lucida 12 bold ").grid(
            row=1, column=4, sticky=W)

        name = self.staff_view_shows_searchname.get()
        species = self.staff_view_shows_searchspecies.get()
        animalexhibit = self.staff_view_exhibit_entry.get()
        min_age = self.min_age_entry.get()
        max_age = self.max_age_entry.get()
        animal_type = self.staff_view_animal_entry.get()

        clause = ''
        whereClauseStart = False
        if name != 'NAME':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where nname = \'%s\'" %(name)
            else:
                clause += "and nname = \'%s\'" %(name)
        if species != 'SPECIES':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where species = \'%s\'" %(species)
            else:
                clause += "and species = \'%s\'" %(species)
        if animal_type != '':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where animal_type = \'%s\'" %(animal_type)
            else:
                clause += "and animal_type = \'%s\'" %(animal_type)
        if animalexhibit != '':
            if not whereClauseStart:
                whereClauseStart = True
                clause = "where animalexhibit = \'%s\'" %(animalexhibit)
            else:
                clause += "and animalexhibit = \'%s\'" %(animalexhibit)
        if clause == '':
            clause = "where age >= %s and age <= %s" % (min_age, max_age)
        else:
            clause += "and age >= %s and age <= %s" % (min_age, max_age)



        sql = "SELECT nname, species, animalexhibit, age, animal_type FROM animal %s" % (clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        i = 2
        for row in review:
            Label(temp_view, text=row[0]).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1]).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2]).grid(row=i, column=2, sticky=W)
            Label(temp_view, text=row[3]).grid(row=i, column=3, sticky=W)
            Label(temp_view, text=row[4]).grid(row=i, column=4, sticky=W)
            i += 1
        # sort
        self.clause = clause
        button = Button(temp_view, text = "Name ASC", width=15, command = self.sort_animal_name_asc)
        button.grid(row=i,column=0, sticky=W)
        button = Button(temp_view, text = "Name DESC", width=15, command = self.sort_animal_name_desc)
        button.grid(row=i + 1,column=0, sticky=W)
        button = Button(temp_view, text = "Species ASC", width=15, command = self.sort_animal_species_asc)
        button.grid(row=i,column=1, sticky=W)
        button = Button(temp_view, text = "Species DESC", width=15, command = self.sort_animal_species_desc)
        button.grid(row=i + 1,column=1, sticky=W)
        button = Button(temp_view, text = "Exhibit ASC", width=15, command = self.sort_animal_exhibit_asc)
        button.grid(row=i,column=2, sticky=W)
        button = Button(temp_view, text = "Exhibit DESC", width=15, command = self.sort_animal_exhibit_desc)
        button.grid(row=i + 1,column=2, sticky=W)
        button = Button(temp_view, text = "Age ASC", width=15, command = self.sort_animal_age_asc)
        button.grid(row=i,column=3, sticky=W)
        button = Button(temp_view, text = "Age DESC", width=15, command = self.sort_animal_age_desc)
        button.grid(row=i + 1,column=3, sticky=W)
        button = Button(temp_view, text = "Type ASC", width=15, command = self.sort_animal_type_asc)
        button.grid(row=i,column=4, sticky=W)
        button = Button(temp_view, text = "Type DESC", width=15, command = self.sort_animal_type_desc)
        button.grid(row=i + 1,column=4, sticky=W)

        # animal detail
        self.staff_view_animal_name = Entry(temp_view, width=20, textvariable=StringVar(temp_view, value = 'NAME'))
        self.staff_view_animal_name.grid(row=i + 2,column=0)

        self.staff_view_animal_species = Entry(temp_view, width=20, textvariable=StringVar(temp_view, value = 'SPECIES'))
        self.staff_view_animal_species.grid(row=i + 2,column=1)
        button = Button(temp_view, text = "Animal Care", width=15, command = self.helper_staff_animal_care)
        button.grid(row=i + 2,column=2, sticky=W)
    def helper_staff_animal_care(self):
        self.view_helper_staff_animal_care = Tk()
        self.view_helper_staff_animal_care.title('Animal Care')
        temp_view = Frame(self.view_helper_staff_animal_care)
        temp_view.pack()
        Label(temp_view, text='Name', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W)
        Label(temp_view, text='Species', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W)
        Label(temp_view, text='Exhibit', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W)
        Label(temp_view, text='Age', font="Lucida 12 bold ").grid(
            row=1, column=3, sticky=W)
        Label(temp_view, text='Type', font="Lucida 12 bold ").grid(
            row=1, column=4, sticky=W)

        name = self.staff_view_animal_name.get()
        species = self.staff_view_animal_species.get()
        sql = "SELECT nname, species, animalexhibit, age, animal_type FROM animal where nname = \'%s\' and species = \'%s\'" % (name, species)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)

        i = 2
        Label(temp_view, text=review[0][0]).grid(row=i, column=0, sticky=W)
        Label(temp_view, text=review[0][1]).grid(row=i, column=1, sticky=W)
        Label(temp_view, text=review[0][2]).grid(row=i, column=2, sticky=W)
        Label(temp_view, text=review[0][3]).grid(row=i, column=3, sticky=W)
        Label(temp_view, text=review[0][4]).grid(row=i, column=4, sticky=W)

        # animal care history
        Label(temp_view, text='Staff', font="Lucida 12 bold ").grid(
            row=i + 1, column=0, sticky=W)
        Label(temp_view, text='Note', font="Lucida 12 bold ").grid(
            row=i + 1, column=1, sticky=W)
        Label(temp_view, text='Time', font="Lucida 12 bold ").grid(
            row=i + 1, column=2, sticky=W)
        sql = "SELECT email, notetext, notetime FROM note WHERE nname = \'%s\'" % (name)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        a = i + 2
        for row in review:
            Label(temp_view, text=row[0]).grid(row=a, column=0, sticky=W)
            Label(temp_view, text=row[1]).grid(row=a, column=1, sticky=W)
            Label(temp_view, text=row[2]).grid(row=a, column=2, sticky=W)
            a += 1
        # sort
        self.clause = "WHERE nname = \'%s\'" % (name)
        button = Button(temp_view, text = "Staff ASC", width=15, command = self.sort_animal_care_staff_asc)
        button.grid(row=a,column=0, sticky=W)
        button = Button(temp_view, text = "Staff DESC", width=15, command = self.sort_animal_care_staff_desc)
        button.grid(row=a + 1,column=0, sticky=W)
        button = Button(temp_view, text = "Note ASC", width=15, command = self.sort_animal_care_note_asc)
        button.grid(row=a,column=1, sticky=W)
        button = Button(temp_view, text = "Note DESC", width=15, command = self.sort_animal_care_note_desc)
        button.grid(row=a + 1,column=1, sticky=W)
        button = Button(temp_view, text = "Time ASC", width=15, command = self.sort_animal_care_time_asc)
        button.grid(row=a,column=2, sticky=W)
        button = Button(temp_view, text = "Time DESC", width=15, command = self.sort_animal_care_time_desc)
        button.grid(row=a + 1,column=2, sticky=W)


        Label(temp_view, text='Note', font="Lucida 12 bold ").grid(
            row=a + 2, column=4, sticky=W)
        self.note = Entry(temp_view, width=100, textvariable=StringVar(temp_view, value = ''))
        self.note.grid(row=a + 2,column=5)
        button = Button(temp_view, text = "Log", width=15, command = self.helper_staff_log_animal_care)
        button.grid(row=a + 2,column=0, sticky=W)
    def sort_animal_care_staff_asc(self):
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='Staff', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='Note', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Time', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        sql = "SELECT email, notetext, notetime FROM note %s ORDER BY email ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            i += 1
    def sort_animal_care_staff_desc(self):
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='Staff', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='Note', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Time', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        sql = "SELECT email, notetext, notetime FROM note %s ORDER BY email DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            i += 1
    def sort_animal_care_note_asc(self):
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='Staff', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='Note', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Time', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        sql = "SELECT email, notetext, notetime FROM note %s ORDER BY notetext ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            i += 1
    def sort_animal_care_note_desc(self):
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='Staff', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='Note', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Time', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        sql = "SELECT email, notetext, notetime FROM note %s ORDER BY notetext DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            i += 1
    def sort_animal_care_time_asc(self):
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='Staff', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='Note', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Time', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        sql = "SELECT email, notetext, notetime FROM note %s ORDER BY notetime ASC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            i += 1
    def sort_animal_care_time_desc(self):
        temp_view = Tk()
        temp_view.title('Animals')
        Label(temp_view, text='Staff', font="Lucida 12 bold ").grid(
            row=1, column=0, sticky=W, padx=10)
        Label(temp_view, text='Note', font="Lucida 12 bold ").grid(
            row=1, column=1, sticky=W, padx=10)
        Label(temp_view, text='Time', font="Lucida 12 bold ").grid(
            row=1, column=2, sticky=W, padx=10)
        sql = "SELECT email, notetext, notetime FROM note %s ORDER BY notetime DESC" % (self.clause)
        print (sql)
        cursor.execute(sql)
        review = []
        for row in cursor:
            review.append(row)
        i = 2
        for row in review:
            Label(temp_view, text=row[0], padx=10).grid(row=i, column=0, sticky=W)
            Label(temp_view, text=row[1], padx=10).grid(row=i, column=1, sticky=W)
            Label(temp_view, text=row[2], padx=10).grid(row=i, column=2, sticky=W)
            i += 1 
    def helper_staff_log_animal_care(self):
        name = self.staff_view_animal_name.get()
        species = self.staff_view_animal_species.get()
        email = self.email
        text = self.note.get()
        sql_time = "SELECT NOW()"
        cursor.execute(sql_time)
        time = cursor.fetchone()[0]
        sql = "INSERT into note(nname, species, email, notetime, notetext) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')" % (name, species, email, time, text)
        print(sql)
        cursor.execute(sql)
        db.commit()
        self.view_helper_staff_animal_care.destroy()
a = GUI()
cursor.close()
db.close()