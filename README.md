About Blueprint
=======
We strive to make beautiful engineering accessible and useful for those who create communities and promote public welfare. Our vision is a world where the good, passionate, and visionary have the biggest impact on our communities and society.

About ODALC
=======
Oakland Digital Arts & Literacy Center (ODALC) is a 501(c)(3) community building organization working to bridge the digital literacy and opportunity divide. Oakland Digital educates, inspires, and empowers underserved communities to participate and succeed in the digital economy.

Project Structure
=======
``odalc/base`` - common models and views that could be shared between different apps in this project, or are general to the entire project. Things like a Course model, an abstract User model and the views for the homepage and course pages could go here

``odalc/odalc_admin`` - things related to the ODALC admins. Models for the AdminUser and the views for the pages that the admin uses could go here

``odalc/students`` - things related to the students taking the class. Models for StudentUser and CourseFeedback and their related views could go here

``odalc/teachers`` - things related to the teachers. Models for TeacherUser and the views for the teacher dashboard could go here

``odalc/templates`` and ``odalc/static`` is structured in the same way as above, so that templates and static files are namespaced and we won't have to worry about clashing names

Installation
=======
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

To add a new SASS file, add the source-destination mapping in ``Gruntfile.js`` under ``sass: dist: files:``.

Deployment (Heroku)
==========
To ensure that Heroku correctly detects this as a Django app, specify the buildpack to be a Python project:
```bash
heroku config:set BUILDPACK_URL=https://github.com/heroku/heroku-buildpack-python
```

Installation of Node, npm, and Bower and configuration of static files happens in the build scripts in ``bin/``.
