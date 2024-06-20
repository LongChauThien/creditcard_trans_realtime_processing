from django.db import models

# Create your models here.
class Creditcard(models.Model):
    id = models.CharField(db_column='Id', max_length=255, primary_key=True)  # Field name made lowercase.
    time = models.FloatField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    amount = models.FloatField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    v1 = models.FloatField(db_column='V1', blank=True, null=True)  # Field name made lowercase.
    v2 = models.FloatField(db_column='V2', blank=True, null=True)  # Field name made lowercase.
    v3 = models.FloatField(db_column='V3', blank=True, null=True)  # Field name made lowercase.
    v4 = models.FloatField(db_column='V4', blank=True, null=True)  # Field name made lowercase.
    v5 = models.FloatField(db_column='V5', blank=True, null=True)  # Field name made lowercase.
    v6 = models.FloatField(db_column='V6', blank=True, null=True)  # Field name made lowercase.
    v7 = models.FloatField(db_column='V7', blank=True, null=True)  # Field name made lowercase.
    v8 = models.FloatField(db_column='V8', blank=True, null=True)  # Field name made lowercase.
    v9 = models.FloatField(db_column='V9', blank=True, null=True)  # Field name made lowercase.
    v10 = models.FloatField(db_column='V10', blank=True, null=True)  # Field name made lowercase.
    v11 = models.FloatField(db_column='V11', blank=True, null=True)  # Field name made lowercase.
    v12 = models.FloatField(db_column='V12', blank=True, null=True)  # Field name made lowercase.
    v13 = models.FloatField(db_column='V13', blank=True, null=True)  # Field name made lowercase.
    v14 = models.FloatField(db_column='V14', blank=True, null=True)  # Field name made lowercase.
    v15 = models.FloatField(db_column='V15', blank=True, null=True)  # Field name made lowercase.
    v16 = models.FloatField(db_column='V16', blank=True, null=True)  # Field name made lowercase.
    v17 = models.FloatField(db_column='V17', blank=True, null=True)  # Field name made lowercase.
    v18 = models.FloatField(db_column='V18', blank=True, null=True)  # Field name made lowercase.
    v19 = models.FloatField(db_column='V19', blank=True, null=True)  # Field name made lowercase.
    v20 = models.FloatField(db_column='V20', blank=True, null=True)  # Field name made lowercase.
    v21 = models.FloatField(db_column='V21', blank=True, null=True)  # Field name made lowercase.
    v22 = models.FloatField(db_column='V22', blank=True, null=True)  # Field name made lowercase.
    v23 = models.FloatField(db_column='V23', blank=True, null=True)  # Field name made lowercase.
    v24 = models.FloatField(db_column='V24', blank=True, null=True)  # Field name made lowercase.
    v25 = models.FloatField(db_column='V25', blank=True, null=True)  # Field name made lowercase.
    v26 = models.FloatField(db_column='V26', blank=True, null=True)  # Field name made lowercase.
    v27 = models.FloatField(db_column='V27', blank=True, null=True)  # Field name made lowercase.
    v28 = models.FloatField(db_column='V28', blank=True, null=True)  # Field name made lowercase.
    class_field = models.IntegerField(db_column='Class', blank=True, null=True)  # Field name made lowercase. Field renamed because it was a Python reserved word.

    class Meta:
        # managed = False
        db_table = 'creditcard'
