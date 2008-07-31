from django.db import models
from gestorpsi.person.models import Person

class Employee(models.Model):
    person = models.OneToOneField(Person)
    hiredate = models.DateField(blank=True)
    job = models.CharField(max_length=30, blank=True)
    active = models.BooleanField(default=True)
    def __unicode__(self):
        return u"%s" % self.person.firstName