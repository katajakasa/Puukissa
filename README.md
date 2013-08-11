Puukissa project
================

What is this ?
--------------
Puukissa is a very simple python-challenge website. Users may log in with openid, and then do exercises on 
python algorithms. User needs to type in the code to a Ace textfield, and the code is then checked on server
in a python sandbox. 

At the moment, most of the text in the project is only in Finnish, and so is the documentation. Sorry :P

License
-------
MIT. Please refer to `LICENSE` for more information.

Mikä on tämä?
-------------
Lue ylläoleva ;)

Projektin asentaminen
---------------------
1. Kloonaa tämä projekti gitillä (git clone ...).
2. Kopioi `settings.py-dist` tiedostoksi `settings.py`.
2. Suorita syncdb projektihakemistossa (`python manage.py syncdb`).
3. Suorita migrate projektihakemistossa (`python manage.py migrate`).
4. Testaa ajamalla runserver (`python manage.py runserver`). 

Kirjastot
---------
* [Django 1.5 tai uudempi] (https://www.djangoproject.com/download/) `pip install django`
* [django-openid-auth] (https://launchpad.net/django-openid-auth) `pip install django-openid-auth`
* [python-openid] (https://github.com/openid/python-openid/) `pip install python-openid`
* [South] (http://south.aeracode.org/) `pip install south`
* [django-crispy-forms] (http://django-crispy-forms.readthedocs.org/) `pip install django-crispy-forms`
* [pysandbox] (https://github.com/haypo/pysandbox/) `pip install pysandbox`
* [django-tinymce] (http://django-tinymce.readthedocs.org/en/latest/) `pip install django-tinymce`

Onelineri kirjastojen asentamiseen
----------------------------------
Seuraava koodirimpsu hakee kaikki tarpeelliset python-kirjastot ja dependenssit.

    pip install django django-openid-auth python-openid south django-crispy-forms pil pysandbox
