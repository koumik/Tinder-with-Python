
import mysql.connector #for connecting to the Wampserver

class ishqzaade: #class used
    def __init__(self): #Constructor used for accessing the server localhost.
        self.conn=mysql.connector.connect(user="root",password="",host="localhost",database="ishqzaade")
        self.mycursor=self.conn.cursor()
        self.program_menu()


    def program_menu(self): #function used
        program_input=input("""Kya haal hai?kya chaiye
        1. Enter 1 to Register
        2. Enter 2 to Login
        3. Enter 3 to exit""")

        if program_input=="1":
            self.register()
        elif program_input=="2":
            self.login()
        elif program_input=="3":
            self.bye()

    def register(self):
        name=input("Enter your name")
        email=input("Enter your email")
        password=input("Enter the password")
        gender=input("Enter the gender")
        city=input("Enter the city")

        self.mycursor.execute("""INSERT INTO `ishqzaade`.`users` (`user_id`, `name`, `email`, `password`, `gender`, `city`) VALUES
(NULL, '%s', '%s', '%s', '%s', '%s');""" % (name,email,password,gender,city))

        self.conn.commit()
        print("Ho gaya bhai")
        self.user_menu()

    def login(self):
        email_for_login=input("Enter your email")
        password_for_login=input("Enter the password")
        self.mycursor.execute("""SELECT * FROM `users` WHERE
`email` LIKE '%s' AND `password` LIKE '%s'""" % (email_for_login,password_for_login))

        user_list=self.mycursor.fetchall()

        self.user_ka_id=user_list[0][0]

        counter=0

        for i in user_list:
            counter=counter+1

        if counter==1:
            print("You have logged in")
            self.user_menu()
        else:
            print("Bhak saale")
            self.program_menu()


    def user_menu(self):
        user_input=input("""What operation would you like to perform
        1. View all users
        2. See who proposed you
        3. You proposed whom
        4. All matches
        5. Logout""")

        if user_input=="1":
            self.view_users()
        elif user_input=="2":
            self.view_proposals()
        elif user_input=="4":
            self.view_match()

    def view_users(self):
        self.mycursor.execute("SELECT * FROM `users` WHERE 1")
        all_user_list=self.mycursor.fetchall()

        for i in all_user_list:
            print("---------------------------------------------------------")
            print(i[0],"|",i[1],"|",i[2],"|",i[4],"|",i[5])
            print("---------------------------------------------------------")

        juliet_ka_id=input("Enter the Id of the user whom would you like to propose?")
        self.propose(juliet_ka_id)

    def propose(self,juliet_id):
        self.mycursor.execute("""INSERT INTO `ishqzaade`.`proposal`
(`proposal_id`, `romeo_id`, `juliet_id`) VALUES (NULL, '%s', '%s');""" % (self.user_ka_id,juliet_id))
        self.conn.commit()
        print("Lo bhai ho gayi baat")
        self.user_menu()

    def view_proposals(self):
        self.mycursor.execute("""SELECT * FROM `proposal` p
         JOIN `users` u ON p.`juliet_id`=u.`user_id`
          WHERE p.`romeo_id` LIKE '%s'""" % (self.user_ka_id))
        proposal_list=self.mycursor.fetchall()

        for i in proposal_list:
            print("---------------------------------------------")
            print(i[4],"|",i[7],"|",i[8])
            print("---------------------------------------------")

        self.user_menu()

    def view_match(self):
        self.mycursor.execute("""SELECT * FROM `proposal` p JOIN `users` u 
        ON p.`juliet_id`=u.`user_id` WHERE p.`juliet_id` IN 
        (SELECT p.`romeo_id` FROM `proposal` p WHERE p.`juliet_id` LIKE '%s')""" % (self.user_ka_id))

        match_user_list=self.mycursor.fetchall()

        for i in match_user_list:
            print("---------------------------------------------")
            print(i[4], "|", i[7], "|", i[8])
            print("---------------------------------------------")

        self.user_menu()


    def bye(self):
        print("You choose to exit")

newobj=ishqzaade()
