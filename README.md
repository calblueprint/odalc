# Bridge
This project is a platform to allow tech and design professionals around the Bay Area to come and teach courses at the
Oakland Digital office.


## About Blueprint
We strive to make beautiful engineering accessible and useful for those who create communities and promote public welfare. Our vision is a world where the good, passionate, and visionary have the biggest impact on our communities and society.


## About ODALC
Oakland Digital Arts & Literacy Center (ODALC) is a 501(c)(3) community building organization working to bridge the digital literacy and opportunity divide. Oakland Digital educates, inspires, and empowers underserved communities to participate and succeed in the digital economy.


## Project Structure
`odalc/courses` - module for the `Course` and `CourseFeedback` models and their related views/forms.

`odalc/users` - module for the base `User` model and its subclasses for individual user types. Also includes forms/views
for authentication and mixins for permissions.

`odalc/lib` - module for interfaces with third-party services. This includes emails, Stripe, and Amazon S3.

`odalc/base` - module the views for the home page and other static pages, along with custom `manage.py` commands

`odalc/odalc_admin` - module for pages that ODALC admins interact with

`odalc/students` - module for pages that students interact with

`odalc/teachers` - module for pages that teachers interact with

`odalc/templates` and `odalc/static` is structured in the same way as above, so that templates and static files are namespaced and we won't have to worry about clashing names


## Installation
All Python dependencies can be installed with
```bash
pip install -r requirements.txt
```

We use Bower and django-bower for front-end package management. To install these depdendencies, run
```bash
python manage.py bower_install
```

We also use grunt to automate tasks - for now, it's used specifically for compiling SASS and Javascript files, but we can look into using it more generally for our entire project. To set grunt up (it requires Node.js versions >= 0.8.0)
```bash
npm install -g grunt-cli
```
Change to the project root directory, then install the project's dependencies in ``package.json`` by running ``npm install``.
Run ``grunt`` to begin watching files.

All SASS files are all imported into a `main.scss` which is compiled into a single `main.css`.


## Deployment (Heroku)
There are environment variables we need to set up on Heroku.
```
# Heroku confs
BUILDPACK_URL               https://github.com/heroku/heroku-buildpack-python
PYTHONPATH                  /app


# Project confs
DJANGO_SECRET_KEY           <django secret key>
SITE_URL                    <domain of site>
# IS_PROD is set on staging and production servers
# IS_DEV is set on the dev server - don't set this when working on this locally
# These environment variables are only checked that they exist, so the actual
# value of these don't matter (i.e. setting them to 0 is still setting them to
# "true")
IS_PROD                     1
IS_DEV                      1
# These are for the initial admin user that is created when the project is
# deployed
INITIAL_ADMIN_EMAIL         <admin_user_email>
INITIAL_ADMIN_PASSWORD      <admin_user_password>
INITIAL_ADMIN_FIRST_NAME    <admin_user_first_name>
INITIAL_ADMIN_LAST_NAME     <admin_user_last_name>


# Amazon S3 confs
AWS_ACCESS_KEY_ID           <aws_access_key_id>
AWS_SECRET_ACCESS_KEY       <aws_secret_access_key>
S3_BUCKET                   <s3_bucket_name>


# Email confs - using Gmail to send emails
EMAIL_HOST                  smtp.gmail.com
EMAIL_HOST_PASSWORD         <gmail_password>
EMAIL_HOST_USER             <gmail_account>
EMAIL_PORT                  587
EMAIL_USE_TLS               1


# Stripe confs
STRIPE_PUBLIC_KEY           <stripe public key>
STRIPE_SECRET_KEY           <stripe secret key>
```

If deploying for the first time, there are a few commands that need to be run to set up the project:
```bash
heroku run python manage.py migrate --app <app_name>
heroku run python manage.py initialize --app <app_name>

# Run the following if you want to add seed data
heroku run python manage.py seed_data --app <app_name>
```

