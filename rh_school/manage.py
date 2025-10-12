#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # DÉBUT : CORRECTION CRITIQUE POUR L'ENCODAGE SOUS WINDOWS
    # Cette étape force l'environnement à utiliser l'UTF-8 pour l'I/O, 
    # ce qui résout le problème de décodage lié aux accents dans les chemins de fichiers.
    if sys.platform == "win32":
        try:
            sys.stdin.reconfigure(encoding='utf-8')
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        except AttributeError:
            # Fallback si 'reconfigure' n'est pas disponible (versions Python < 3.7)
            pass
    # FIN : CORRECTION CRITIQUE

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rh_school.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
