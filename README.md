# DjangoCoreApp
A Django app with a custom user model setup.  This uses an email address instead of a username to login.

## Instructions

1. Clone this repository into a folder named core within your Django folder.
2. Open your project settings.py file
3. Add this setting to the bottom of the file
```
	AUTH_USER_MODEL = "core.CoreUser"
```
4. Add core to the list of INSTALLED_APPS
5. Run:
```
	python manage.py makemigrations core
	python manage.py migrate
```
6. That should be it!