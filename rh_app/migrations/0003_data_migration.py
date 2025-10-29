from django.db import migrations

def create_departments(apps, schema_editor):
    Departement = apps.get_model('rh_app', 'Departement')
    Employe = apps.get_model('rh_app', 'Employe')
    
    # Créer les départements basés sur les données existantes
    departements_data = {}
    for employe in Employe.objects.all():
        dept_name = employe.departement
        if dept_name and dept_name not in departements_data:
            departement = Departement.objects.create(
                nom=dept_name,
                description=f"Département {dept_name}",
                actif=True
            )
            departements_data[dept_name] = departement
    
    # Mettre à jour les employés avec les nouveaux départements
    for employe in Employe.objects.all():
        if employe.departement and employe.departement in departements_data:
            employe.departement = departements_data[employe.departement]
            employe.save()

def reverse_create_departments(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('rh_app', '0002_alter_contrat_type_contrat_departement_and_more'),
    ]

    operations = [
        migrations.RunPython(create_departments, reverse_create_departments),
    ]
