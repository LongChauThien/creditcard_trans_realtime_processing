from django.db import models

# Create your models here.
class Creditcard(models.Model):
    id = models.CharField(db_column='Id', max_length=255, primary_key=True)  # Field name made lowercase.
    time = models.FloatField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.

    class Meta:
        # managed = False
        db_table = 'creditcard'
