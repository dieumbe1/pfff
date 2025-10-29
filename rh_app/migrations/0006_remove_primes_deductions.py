# Generated manually: remove primes and deductions from Salaire
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('rh_app', '0005_alter_conge_type_conge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salaire',
            name='primes',
        ),
        migrations.RemoveField(
            model_name='salaire',
            name='deductions',
        ),
    ]
