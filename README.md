# Project Structure

video_platform/
│
├── manage.py
├── requirements.txt
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
├── videos/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── payments/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── webhooks.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── accounts/
│   └── videos/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── media/ 