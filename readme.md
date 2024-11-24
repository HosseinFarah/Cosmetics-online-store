# Flask Authentication and E-commerce Application

This project is a Flask-based web application that provides user authentication, product management, ticketing system, and e-commerce functionalities. The application supports multiple languages and includes features for both regular users and administrators.

## Features

- User Authentication (Login, Registration, Password Reset)
- User Profile Management
- Product Management (Create, Update, Delete, View)
- Category and Brand Management
- Shopping Basket and Checkout with Stripe Payment Gateway
- Ticketing System for User Support
- Multi-language Support
- Admin Dashboard for Managing Users, Products, Orders, and Tickets

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Flask-Authentication-Ecommerce.git
   cd Flask-Authentication-Ecommerce
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:** Create a `.env` file in the root directory and add the following variables:
   ```plaintext
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   SQLALCHEMY_DATABASE_URI=sqlite:///site.db
   MAIL_SERVER=smtp.googlemail.com
   MAIL_PORT=587
   MAIL_USE_TLS=1
   MAIL_USERNAME=your_email@example.com
   MAIL_PASSWORD=your_email_password
   STRIPE_SECRET_KEY=your_stripe_secret_key
   STRIPE_ENDPOINT_SECRET=your_stripe_endpoint_secret
   ```

5. **Initialize the database:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

6. **Run the application:**
   ```bash
   flask run
   ```

## Usage

### User Authentication
- **Register:** Users can register by providing their details including a profile picture.
- **Login:** Registered users can log in using their email and password.
- **Profile Management:** Users can update their profile information and change their password.
- **Password Reset:** Users can request a password reset link via email.

### Product Management
- **Create Product:** Admins can create new products by providing details such as name, price, description, images, etc.
- **Update Product:** Admins can update existing product details.
- **Delete Product:** Admins can delete products from the database.
- **View Products:** Users can view all products, filter by categories and brands, and search for specific products.

### Shopping Basket and Checkout
- **Add to Basket:** Users can add products to their shopping basket.
- **View Basket:** Users can view the contents of their basket and update quantities.
- **Checkout:** Users can proceed to checkout and make payments using Stripe.

### Ticketing System
- **Create Ticket:** Users can create support tickets by providing a title, description, and optional image.
- **View Tickets:** Users can view their tickets and admins can view all tickets.
- **Update Ticket:** Users and admins can update ticket details.
- **Answer Ticket:** Users and admins can add messages to tickets for communication.

### Admin Dashboard
- **Manage Users:** Admins can view, update, and delete user accounts.
- **Manage Orders:** Admins can view all orders and their details.
- **Manage Tickets:** Admins can view and manage all support tickets.

### Multi-language Support
The application supports multiple languages. Users can select their preferred language from the dropdown menu.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- Flask
- Bootstrap
- Stripe
- Flask-Babel

This documentation provides an overview of the project's features, installation steps, usage instructions, and other relevant information. For more details, please refer to the project's source code and documentation.
