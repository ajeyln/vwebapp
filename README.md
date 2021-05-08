<h1 align="Center"> VWebapp</h1>

## Table of Content

* [Background](#back)
* [Tasks](#task)
    + [Creating Database](#database)
    + [Registration](#register)
    + [Update user](#update)
    + [Delete user](#delete)
    + [User Details](#details)
    + [Statistic](#stat)
* [Technical Specification](#tech)
* [Useful Links](#useful)

## <a name="back"></a> Background

This repository is an attempt to create web application using Python Flask module.

The following prerequisites are required: 

1. A website for local Temple Sri Venkataramana Temple Karkala <Br />
2. A Home page contains information on temple <Br />
3. Users can register themselves and see other registered users <Br />
4. Users can Change/update their information using their registration numbers. <Br />
5. Admin can Remove the User(Currently User can remove can themself.) <Br />
6. User can see their Information in User Details. <Br />
7. Statistical Informations on Users Details. <Br />
8. Contact Information of Temple 

The following Specifications has to be done: 

1. Flask webserver listening on localhost at certain specified port for user requests <Br />
2. Endpoints <Br />
    * / or /home - renders index.html, homepage of the temple with images and useful links <Br />
    * /register - user can register here  <Br />
        - GET method - form for registration gets displayed <Br />
	    - PUT/POST method - user values for registration will be accepted by server <Br />
    * /update <Br />
        - GET method - for changing user information of existing registered users, here a webpage must be rendered <Br />
        - POST method  -  user values to be sent to flask for updation <Br />
    * /delete <Br />
        - GET Method - a form for deleting user <Br />
        - POST method - user request must be sent to flask for deletion <Br />
    * /list - renders dynamic webpgae of list of registered users <Br />
    * /statistic <Br />
        - GET Method - a form for statistical informations on users details <Br />
        - POST method - user request must be sent to flask to generate graphs <Br />
    * /contact - renders contact.html, contact information of temple <Br />
    * /* - any other endpoints will display error.html <Br />

Persistence storage
   * The Registered User information will be stored in a database

## <a name="task"></a> Tasks

User needs to execute the python script  before doing the following and make sure that the webserver is running in background. <p>

### <a name="database"></a>1. Creating Database<br />
User can create the database using python script and do the manipulations (SQLITE3 CRUD operations) for the Endpoints <br />

### <a name="register"></a>2. Registration <br />

User can register with their details in registration form by click on "Register" Button on Home page or using "/register" Endpoint 
and these user details will be updated in Database <br />

user needs to click on Register once after all information are updated.
### <a name="update"></a>3. Update user <br />

User can update or change their information by click on "Update user" Button on Home page or using "/Update" Endpoint <br />

User can change their details, If they know their registration number. These Information can be seen by click "User Details" Button 
on Home page or using "/list" Endpoint <br />

### <a name="delete"></a>4. Delete user <br />

If Admin wants to delete any user, he can delete by click on "Remove user" Button on Home page or using "/delete" Endpoint <br />

Please note, currently user having full access to delete any user and these can be changed.

### <a name="details"></a>5. User Details <br />

User can check their details by click on "User Details" Button on Home page or using "/list" Endpoint <br />


### <a name="stat"></a>6. Statistic <br />

User will get Statistical Information of user details by click on "Statistics" Button on Home page or using "/statistic" Endpoint <br />

In this the datas from database will get converted to Python data structures and using this, we are going to plot different kind of 
graphs using the module Matplotlib for data analysis.<br />

Based on the python data structure, we have plotted 5 kind of graphs, which has follows: <br />

### 1. Line Graph

The line graph shows Employee count with respect to their Cities

### 2.Bar Graph

The bar graph shows Employee count with respect to their Second Names.

### 3. Histogram

In this section, we are plotting the graph based on User age with duration of 10 Years

### 4. Scatter Plot

The scatter graph shows the Age of Male and Female based on their Cities.

### 5. Pie Chart

In the Piechart, we can see the Percentagewise City of Users

