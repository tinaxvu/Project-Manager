[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/bknTyRar)
# B-19 Software Engineering Project

__Names:__ Youness Charfaoui, Jerry Gu, Samyu Krishnasamy, Tina Vu, Grant Zou

__Computing IDs:__ cru8jn, ncq9fn, frv9sc, kmp3xr, sth3mm

# PLEASE READ:
- please do not push to main haphazardly, this is the Heroku production branch. Heroku will auto deploy main pushes right now


# How to install required dependencies:
`pip install -r requirements.txt`

# Heroku database migrations
`heroku run python AcademicProjectTracker/manage.py migrate --app academic-project-tracker`

# Check web dynos are running
`heroku ps:scale web=1 --app academic-project-tracker`

# Collect static files
`heroku run python AcademicProjectTracker/manage.py --app academic-project-tracker`

# Check Heroku Logs
`heroku logs --tail --app academic-project-tracker`