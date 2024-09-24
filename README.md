# Django on Kubernetes

This is the Kubernetes version of the Django restaurant system developed in the repository [here](https://github.com/calmcat2/littlelemon/tree/v1).

Before applying the YAML files, ensure the following:

1. **Django Configuration**:
   - You may need to modify `yml-files/Django-app/django-config.yml` for Django server customization. The original Django `settings.py` can be found [here](https://github.com/calmcat2/littlelemon/blob/v1/app/littlelemon/littlelemon/settings.py).

2. **Persistent Volume Configuration**:
   - Modify `yml-files/Django-app/staticfiles-pv.yml` and `yml-files/DB/mysql-pv.yml` as necessary to suit your storage requirements.

3. **MySQL Credentials**:
   - Update your preferred credentials for the MySQL server in `mysql-secret.yml`.