vwebapp

This is an attempt to create web application using Flask module for python.

A. Requirements
1. A website for local Temple Sri Venkataramana Temple Karkala
2. Users can register themselves and see other registered users
3. A Home page contains information on temple
4. Contact Information of Temple 

B. Specification
1. Flask webserver listening on localhost at certain specified port for user requests
2. Endpoints
   * / or /home - renders index.html, homepage of the temple with images and useful links
   * /contact - renders contact.html, contact information of temple
   * /register - user can register here 
      - GET method - form for registration gets displayed
	  - PUT/POST method - user values for registration will be accepted by server
   * /list - renders dynamic webpgae of list of registered users
   * /* - any other endpoints will display error.html
3. Persistence storage
   At phase 1 - user information is stored as a file in user_data.csv 
   At phase 2 - the information will be stored in a database

4. Static and Dynamic webpages
   static : i) index.html ii) register.html iii) contact.html iv) error.html
   dynamic: registered_users_list.html - every time the file must be created, whenever user requests a list of registered users

C. Development Phases
Phase 1:
 * render all static files - done 
 * accept post request from user - done
 * save the user information and append it to user_data.csv  - Not working !!!
 * render dynamic registered list - Not working !!!
 
Phase 2:
  * remove file storage as persistent storage
  * introduce SQLite DB with SQL for storing user information and do CRUD operations
    - create a table for registered users 
	- TABLE - USER_REGISTER ( PK: USER_ID, USER_NAME, USER_AGE, USER_LOCATION)
  * introduce additional endpoints
    - /update 
	      * GET method - for changing user information of existing registered users, here a webpage must be rendered 
	      * POST method  -  user values to be sent to flask for update
	- /delete 
	      * GET Method - a form for deleting user 
		  * POST method - user request must be sent to flask for delete
Phase 3:
transfer the code and logic to cloud EC2 machine
install SQLIte DB on EC2 machine
Access the webpage from outside EC2 machine (no more local host)

Tools
1. Flask 
2. HTML
3. Sqlite DB
4. SQL Queries
5. python