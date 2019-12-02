# bTravel

This is project about budget traveling where users can easily find places in any city, country for certain budget. Here people choose country, city, category and enter the budget, then they will see places where they can go regarding the query. Or if they know part of the name of the place, they can search by name, the system will show places with names which similar to the query on 30%. If they liked some places, they can give a feedback or rate a place, but it will not shown while admin will not accept this rating. Also, users can buy tickets for some events, for example, for some concert. These tickets people can see in separate section. They can register and system will send to user email with activation link, if email is not sent, user can resend email. Through this activation link user complete registration, and then can login with email and password. In user’s profile, he can change a password, profile.

Project is written on python Django (DRF). 
To test the project, do following steps:
1. Clone the repo
2. create an environment
```
virtualenv env
```
3. activate the environment and install all required libraries
On Windows
```
env\Scripts\activate
```
On Unix based system
```
source env\bin\activate
```
Then install requirements
```
pip install -r requirements.txt
```
4. Run the project
```
python manage.py runserver
```
or 
```
./manage.py runserver
```
