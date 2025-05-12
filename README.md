# Django on Kubernetes

This is the Kubernetes version of the Django restaurant system, originally developed in the [Little Lemon repository](https://github.com/calmcat2/littlelemon/), which provides a Django-based web application for restaurant management, including features like menu management, table reservations, and API access.

The helm chart can be used alone to deploy such an application in a Kubernetes cluster. Make sure to customize `Helm-chart/templates/values.yaml` before deployment. 

You may also fork the repository and make updates. The GitHub Actions workflow is configured as follows:

- It is triggered when changes are made to any of the following directories or files:
  - `littlelemon/`
  - `Dockerfile`
  - `requirements.txt`
  - `Helm-chart/` (excluding `values.yaml`)
- Upon detecting changes, the workflow:
  - If changes are outside `Helm-chart/`, build, test, and push a new Docker image to Docker Hub.
  - Automatically increments the Helm chart version (minor) in `Helm-chart/Chart.yaml` following semantic versioning.
  - Commits the updated version back to the main branch of the repository automatically without requiring a pull request.

To synchronize the application in the Kubernetes cluster, you can use ArgoCD. Ensure that you configure ArgoCD by connecting it to your repository and setting up the appropriate application manifests. Refer to the [ArgoCD documentation](https://argo-cd.readthedocs.io/en/stable/) for detailed setup instructions.

## Features of the LittleLemon Restaurant Website

This Django-based web application essentially provides the following features:

1. **Static content serving**
   - Static website contents such as Restaurant information is available to the public.
  
2. **Table Reservation**
   - Customers can book reservations online. The reservation form only displays available time slots starting today.

3. **Menu and Reservation Management**
   - Admin users can manage (add, edit, delete) the menu through the Django admin portal.

4. **API Access**
   - The API provides functionality for both customers and administrators.
   - Admin users have full rights to manage menus and reservations via the API.
   - Customers can register an account, view menus, and manage their reservations under their name.
   
### Available API Endpoints

- **Authentication**
  - `GET http://127.0.0.1:8000/auth/users`: Use Basic Auth or Bearer Token in the Authorization header with valid credentials to show all users.
  - `POST http://127.0.0.1:8000/auth/users`: Register a new user by embedding a username and password in the body.
  - `POST http://127.0.0.1:8000/auth/token/login/`: Embed with valid credentials to receive a token for the user.
  - `POST http://127.0.0.1:8000/auth/token/logout/`: Use this endpoint to log out a user (remove user authentication token).
  - Test Djoser API endpoints as shown in the [documentation](https://djoser.readthedocs.io/en/latest/getting_started.html).

- **Menu**
  - `GET http://127.0.0.1:8000/menu`: Shows all menu items with no authentication needed.
  - `GET http://127.0.0.1:8000/api/menu-items/<int:pk>`: Use a Bearer token in the Authorization header to show details of individual menu items. This endpoint is available to all authenticated users.

- **Reservation**
  - `GET http://127.0.0.1:8000/api/reservations/`
    - Use Basic Auth or Bearer Token in the Authorization header with **admin credentials** to show all reservations in the system.
    - Use Basic Auth or Bearer Token in the Authorization header with **user credentials** to show only the reservations under the logged-in user's name.
  - `POST http://127.0.0.1:8000/api/reservations/`: All authenticated users can create a reservation.
  - `PATCH http://127.0.0.1:8000/api/reservations/<int:pk>`
    - Embed with admin credentials to modify any reservation.
    - Embed with user credentials to modify a reservation only if it is under the user's name.
  - `DELETE http://127.0.0.1:8000/api/reservations/<int:pk>`
    - Embed with admin credentials to delete any reservation.
    - Embed with user credentials to delete a reservation only if it is under the user's name.
    - **Response Codes**:
      - `204 No Content`: Reservation successfully deleted.
      - `403 Forbidden`: User does not have permission to delete the reservation.
      - `404 Not Found`: Reservation with the specified ID does not exist.