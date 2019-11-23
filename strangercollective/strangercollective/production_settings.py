DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sephbin$default',
        'USER': 'sephbin',
        'PASSWORD': '100%StrongPassword',
        'HOST': 'sephbin.mysql.pythonanywhere-services.com',
        'OPTIONS':{
	        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}