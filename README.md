# Django on Kubernetes

This is the Kubernetes version of the Django restaurant system developed based on repository [here](https://github.com/calmcat2/littlelemon/).
A github Actions is set to analyze code using SonarQube, then create and push the image to docker hub.

Before applying the YAML files, ensure the following are updated:

1. **Django Configuration**:
   - You may need to modify `yml-files/Django-app/django-config.yml` for Django setttings customization. Look up for references in `littlelemon/littlelemon/settings.py`.

2. **Persistent Volume Configuration**:
   - Modify `yml-files/Django-app/staticfiles-pv.yml` and `yml-files/DB/mysql-pv.yml` as necessary to suit your storage requirements.

3. **MySQL Credentials**:
   - Update your credentials for the MySQL server in `mysql-secret.yml` as necessary.

## LittleLemon Restaurant Website

This Django-based web application essentially provides the following features:

1. **Table Reservation**
   - Customers can book reservations online. The reservation form only displays available time slots starting today.

2. **Menu and Reservation Management**
   - Admin users can manage (add, edit, delete) the menu through the Django admin portal.

3. **API Access for Both Customers and Administrators**
   - Admin users have full rights to manage menus and reservations via the API.
   - Anyone can use the API to register an account.
   - Users can view menus and reservations under their name and modify or delete their reservations via the API.
   
### Available API Endpoints

- **Authentication**
  - `GET http://127.0.0.1:8000/auth/users`: Embed with valid credentials to show all users.
  - `POST http://127.0.0.1:8000/auth/users`: Register a new user by embedding a username and password in the body.
  - `POST http://127.0.0.1:8000/auth/token/login/`: Embed with valid credentials to receive a token for the user.
  - `POST http://127.0.0.1:8000/auth/token/logout/`: Use this endpoint to log out a user (remove user authentication token).
  - Test Djoser API endpoints as shown in the [documentation](https://djoser.readthedocs.io/en/latest/getting_started.html).

- **Menu**
  - `GET http://127.0.0.1:8000/menu`: Shows all menu items with no authentication needed.
  - `GET http://127.0.0.1:8000/api/menu-items/<int:pk>`: Embed with valid credentials to show details of individual menu items.

- **Reservation**
  - `GET http://127.0.0.1:8000/api/reservations/`
    - Embed with admin credentials to show all reservations.
    - Embed with user credentials to show all reservations under the logged-in user's name.
  - `POST http://127.0.0.1:8000/api/reservations/`: All authenticated users can create a reservation.
  - `PATCH http://127.0.0.1:8000/api/reservations/<int:pk>`
    - Embed with admin credentials to modify any reservation.
    - Embed with user credentials to modify a reservation only if it is under the user's name.
  - `DELETE http://127.0.0.1:8000/api/reservations/<int:pk>`
    - Embed with admin credentials to delete any reservation.
    - Embed with user credentials to delete a reservation only if it is under the user's name.