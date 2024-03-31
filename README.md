# Hotel Reservation App Backend

This is a full-stack web application's backend built with Django, Firestore, PostgreSQL, Celery with Redis, and integrated with Stripe for payment processing. The application allows users to search for hotels, view details, make reservations, and process payments securely.

## Features

- User Authentication: Users can sign up, log in, and manage their accounts.
- Hotel Search: Users can search for hotels based on location, dates, and other criteria.
- Hotel Details: Information about each hotel, room types, and availability.
- Reservation Management & Payment Processing: Secure payment processing using Stripe integration.
- Background Task Processing: Celery with Redis integration for handling background tasks and asynchronous processing.

## Technologies Used

- Django: Backend server and API development using Django framework.
- Firebase Authentication: Used for user authentication and authorization.
- PostgreSQL: Relational database management system used for storing all data.
- Celery with Redis: Asynchronous task queue and message broker for background task processing.
- Stripe: Payment processing integration for handling secure transactions.

## Installation

1. Clone the repository:

```
git clone https://github.com/etorelan/reservation_app_backend.git
```

2. Install backend dependencies:

```
cd reservation_app_backend
pip install -r requirements.txt
```
3. Set up PostgreSQL:

- Create a PostgreSQL database.
- Configure the backend to connect to your PostgreSQL database.

4. Set up environment variables:

   - Create a `.env` file in the `backend` directory and set the following variables:

     ```
     STRIPE_API_KEY=
      DJANGO_SECRET_KEY=
      POSTGRES_PASSWORD=
      DEBUG=
      ALLOWED_HOSTS_DEV=".localhost,127.0.0.1,[::1]" #default django values
      CSRF_TRUSTED_ORIGINS_DEV="http://localhost:3000"
      CORS_ALLOWED_ORIGINS_DEV="http://localhost:3000,http://localhost:8000"
      DATABASE_URL=
     ```

5. Run migrations:

```
python manage.py migrate
```

6. Start the backend server:

```
python manage.py runserver
```

## License

This project is licensed under the MIT License

## Acknowledgments

- Special thanks to the developers of Django, Firestore, PostgreSQL, Celery, Redis, and Stripe for their amazing tools and documentation.
- Thanks to the open-source community for providing helpful resources and tutorials.
