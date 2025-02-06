# Project Manager Application 

__Names:__ Youness Charfaoui, Jerry Gu, Samyu Krishnasamy, Tina Vu, Grant Zou

# PLEASE READ:
- please do not push to main haphazardly, this is the Heroku production branch. Heroku will auto deploy main pushes right now

# Start Django locally
1. `python manage.py makemigrations`
2. `python manage.py migrate`
3. `python manage.py runserver`

# How to install required dependencies:
`pip install -r requirements.txt`

# Create django superuser
`python manage.py createsuperuser`

# Set heroku default to this app so you don't have to type "--app academic-project-tracker"
`heroku git:remote -a academic-project-tracker`

# Heroku database migrations
`heroku run python AcademicProjectTracker/manage.py migrate --app academic-project-tracker`

# Check web dynos are running
`heroku ps:scale web=1 --app academic-project-tracker`

# Collect static files
`heroku run python AcademicProjectTracker/manage.py --app academic-project-tracker`

# Check Heroku Logs
`heroku logs --tail --app academic-project-tracker`

# Resources
Overall: https://docs.djangoproject.com/en/5.1/intro/tutorial01/

Google Auth: https://www.youtube.com/watch?v=yO6PP0vEOMc

S3 Bucket Implementation: https://www.youtube.com/watch?v=JQVQcNN0cXE

Event Listener: https://www.w3schools.com/js/js_htmldom_eventlistener.asp

Frontend: 
- https://mkdev.me/posts/fundamentals-of-front-end-django
- https://www.w3schools.com/css/tryit.asp?filename=trycss_buttons_hover
- https://rafaltomal.com/tips/move-button-on-hover/
- https://medium.com/@kaileegray/creating-a-calendar-app-using-full-calendar-javascript-bootstrap-34366ce3745d


ChatGPT


