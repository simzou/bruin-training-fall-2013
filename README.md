h1. bruin-training

A simple training app for Daily Bruin trainees

h2. Initial setup:

Set up a sandbox for your codebase using virtualenv.

<pre><code>$ virtualenv --no-site-packages training</code></pre>

Activate the virtualenv.

<pre><code>$ cd training
$ . bin/activate</code></pre>

Clone down the training repo.

<pre><code>$ git clone git@github.com:anthonyjpesce/bruin-training-fall-2013.git repo</code></pre>

Enter the project and install its dependencies.

<pre><code>$ cd reop
$ pip install -r requirements.txt</code></pre>

h2. Installing SQLite

Install SQLite

<pre><code>$ sudo apt-get install sqlite3</code></pre>

Then set up the test database

<pre><code>$ sqlite3 test
> .exit</code></pre>

h2. Starting up the Django project

Sync the database, and run our script to load in the data.

<pre><code>$ python manage.py syncdb
$ python manage.py load</code></pre>