"# template-backend"

Run locally
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python main.py

https://cloud.google.com/appengine/docs/standard/python3/building-app/deploying-web-service

Deploy to google cloud for the first time
Create project (not commands)
Create app
gcloud auth application-default login
gcloud app deploy

For a new project also need to do gcloud init

Do need to enable billing for the process to work

Here the APP is deployed

https://jinn-app-backend.ey.r.appspot.com


This is the tutorial for setting up stripe
Also has a section on setting the webhook stuff up for production
