# Recipe Management - Web Application with FlaskRESTful

## Overview
The Recipe API is a backend service for managing users, recipes, categories, comments and images. 
It includes features for user authentication, profile management, recipe and category CRUD operations, and image handling through `Cloudinary`.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-ins)
- [Endpoints](#endpoints)
  - [User Management](#user-management)
  - [Category Management](#category-management)
  - [Recipe Management](#recipe-management)
  - [Comment Management](#comment-management)
  - [Photo Management](#photo-management)
- [Validation & Error Handling](#validation--error-handling)

## Features
- **User Registration & Authentication**: Supports user registration, login, and token-based authentication. Secure user registration and login with extensive validation.
- **Profile Management**: Personal information and profile photo management with unique endpoint-based access controls.Users can update their own personal details, change passwords, and manage profile photos.
- **Category & Recipe Creation**: Admins and authenticated users can create, update, and delete categories and recipes with authorization control.
- **Recipe Management**: Users can create, update, and delete their own recipes, with images hosted on Cloudinary.
- **Admin Privileges**: Only admins can manage categories.
- **Comments**: Allows authenticated users to add, edit, or delete comments on recipes.
- **Media Handling**: Upload and manage photos for user profiles and recipes with cloud-based storage integration - `Cloudinary`.

## Technologies Used

- **Backend**: Flask, Flask-RESTful, Flask-SQLAlchemy
- **Database**: PostgreSQL
- **Cloud Storage**: Cloudinary for image hosting and management
- **Email Service**: SendGrid for sending emails

## Setup Instructions 

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/DZalim/recipeAppFlask.git
    ```

2. **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Create a `.env` File**:
    - In the project root, create a `.env` file with the following keys:
      ```plaintext
        DB_USER=postgres
        DB_PASSWORD=YOUR_PASSWORD
        DB_PORT=YOUR_PORT
        DB_NAME=YOUR_DB_NAME
        SECRET_KEY=YOUR_SECRET_KEY
        CLOUDINARY_CLOUD_NAME=YOUR_CLOUDINARY_CLOUD_NAME
        CLOUDINARY_API_KEY=YOUR_CLOUDINARY_API_KEY
        CLOUDINARY_API_SECRET=YOUR_CLOUDINARY_API_SECRET
        SENDGRID_API_KEY=YOUR_SENDGRID_API_KEY
        EMAIL_SENDER=YOUR_EMAIL_SENDER
      ```

4. **Configure Cloudinary**:
   - Register at [Cloudinary](https://cloudinary.com) to get API credentials.
   - Add your Cloudinary API credentials to the `.env` file.

5. **Configure SendGrid**:
   - Sign up at [SendGrid](https://sendgrid.com) to obtain an API key.
   - Add your SendGrid API key to the `.env` file`.

6. **Run Migrations**:
   - BE SURE YOU ARE CONNECTING TO AN EXISTING DATABASE
   - Use Flask-Migrate to create and apply database migrations:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

8. **Start the Server**:
    ```bash
    flask run
    ```

9. **Test API**: After starting the server, you can interact with the API via HTTP requests or using tools like Postman. Refer to the Endpoints section for specific routes and request methods.


## Endpoints

### User Management
- **Register User (POST /register)**:
  - Registers a new user with `unique username and email` validation. Additionally, the username must be one word only and contain between 3 and 15 characters.
  - Validates password strength and required fields (first name, last name).
      - The password must contain a minimum of 8 and a maximum of 20 characters. They must be a combination of an uppercase letter, a lowercase letter, a number and a special character.
      - First name and Last name must be one word only and contain between 3 and 15 characters.
      - The phone number is not a required field during registration. But in case data is submitted, it must contain a minimum of 10 characters
  - Sends a welcome email upon successful registration using `Sendgrid` and returns a token.

- **Login User (POST /login)**:
  - Authenticates an existing user with email and password.
  - Issues a token valid for 2 days upon successful login.

- **Personal Information (GET/PUT /<username>/personal_info)**:
  - **GET**: Retrieves the personal information of the logged-in user.
  - **PUT**: Allows the user to update their first name, last name, and phone.

- **Deactivate Profile (PUT /<username>/deactivate_profile)**:
  - Deactivates the user’s profile, making it inaccessible.

- **Change Password (PUT /<username>/change-password)**:
  - Allows the user to update their password, given they provide the current one.

### Category Management
- **List/Create Categories (GET/POST /categories)**:
  - **GET**: Lists all available categories. Everyone can see the added categories.
  - **POST**: Allows only admins to add new categories with unique names.

- **Update/Delete Category (PUT/DELETE /category/<category_id>)**:
  - **PUT**: Allows only admins to update an existing category.
  - **DELETE**: Allows only admins to delete an existing category.

### Recipe Management
- **User Recipes (GET/POST /<username>/recipes)**:
  - **GET**: Lists recipes for the specified user. Admin has access to each user's recipes, while each user can only access their own recipes.
  - **POST**: Allows users with specific roles (beginner and advanced) to create recipes. Admin can't add recipes.

- **Update/Delete Recipe (PUT/DELETE /<username>/recipes/<recipe_id>)**:
  - **PUT**: Allows the recipe owner to update details.
  - **DELETE**: Allows the recipe owner to delete the recipe.

- **Recipe Details (GET/PUT /recipe/<recipe_id>)**:
  - **GET**: Lists details for a specific recipe. Any user can access the recipe details.
  - **PUT**: Allows users with the admin role to be able to change the recipe category_id and diffivulty level. Advanced users can change only difficulty level. A user must have created a certain number of recipes to become an advanced user. Also if it was advanced and subsequently deleted recipes it goes into beginner.

- **Recipes by Category (GET /categories/<category_id>/recipes)**:
  - **GET**: Lists recipes under a specified category.Any user can access this endpoint.

### Comment Management
- **Recipe Comments (GET/POST /recipe/<recipe_id>/comment)**:
  - **GET**: Lists all comments for a specified recipe. Any user can access this endpoint.
  - **POST**: Allows logged-in users to add a comment to a recipe.

- **Update/Delete Comment (PUT/DELETE /recipe/<recipe_id>/comment/<comment_id>)**:
  - **PUT**: Allows the comment owner to edit the comment.
  - **DELETE**: Allows the comment owner to delete their comment.

### Photo Management
- **Profile Photo Management (GET/POST/DELETE /<username>/personal_photo)**: Еach user can access their own profile photos info.
  - **GET**: Access the user's profile photo.
  - **POST**: Upload a new profile photo (one per user). We have one-to-one relation UserModel <=> UserPhotosModel
  - **DELETE**: Remove the profile photo from both the database and cloud storage.
    
- **List Recipe Photos (GET /recipe/<recipe_id>/photos)**:
  - **GET**: Lists all photos for a specific recipe. Any user can access this endpoint.

- **Create Recipe Photos (POST username/recipes/<recipe_id>/photos)**:
  - **POST**: Аny user can add photos to their created recipe.
  
- **Delete Recipe Photo (DELETE username/recipes/<recipe_id>/photos/photo_id)**:
  - **DELETE**: Any user can delete photos added to the recipe they created.
 
  ## Validation & Error Handling

- **User Registration**: Enforces unique constraints on `username` and `email`, requires password strength validation, and checks required fields.
- **Profile Updates**: Validates that only certain fields (`first_name`, `last_name`, `phone`) can be modified by the user.
- **Photo Uploads**: Restricts each user to one profile photo and allows a one-to-many relationship for recipe photos.
- **Access Control**: Ensures users can only modify their own data, with role-based access for certain routes (e.g., only admins can manage categories).
- **Error Messages**: Provides consistent error handling across endpoints, with HTTP status codes like:
  - `401 Unauthorized`
  - `403 Forbidden`
  - `404 Not Found`
  - `Others`
  - Includes descriptive messages for each error type.
