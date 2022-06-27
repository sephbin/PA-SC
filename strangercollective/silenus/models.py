from django.db import models
import django.utils.html as dhtml
import json
import uuid
from django import forms
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save, m2m_changed, pre_init, post_init, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import date
from .models_utils import *


class graphObject(parentModel):
	pass

class geometryObject(parentModel):
	pass