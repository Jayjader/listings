# listings
A minimal craigslist clone.

Setup: 

    > git clone https://github.com/Jayjader/listings.git
    > cd listings
    // Setup virtual environment
    > virtualenv listings_env
    // Install dependencies (like django)
    > pip install -r requirements.txt
    // Create database & update it to the most current model
    > python manage.py migrate
    // Start local server
    > python manage.py runserver
Then go to [localhost:8000/listings/](http://localhost:8000/listings/).

Currently, any emails generated are sent through the django
 email console backend (
 `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`
  in `settings.py`). They are simply printed to the console. Thus, if you need the edit link for a listing, you'll need to check whatever console you used to launch the server to find the creation email that contains that link.
  
  You can get around this somewhat by creating an admin account and accessing the site's admin app:
  
      > python manage.py createsuperuser
      Username: admin
      Password: *****
      Password (again): *****
      Email address: admin@listings.com
      Superuser created successfully.
  
  Next, while the server's running, go to [localhost:8000/admin/](http://localhost:8000/admin), login, and select Listings.
  You can now view, edit, delete & create announcements manually through this interface.
  Thus, you can access the proper edit page for any listing. 
  
  The database only stores the token, and then dynamically maps a url to it. The "full" url is `localhost:8000/listings/edit/<token>`.
