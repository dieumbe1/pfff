from django.db import migrations, models
import django.db.models.functions as functions

class Migration(migrations.Migration):

    dependencies = [
        ('rh_app', '0006_remove_primes_deductions'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='departement',
            constraint=models.UniqueConstraint(functions.Lower('nom'), name='unique_departement_nom_ci'),
        ),
    ]
