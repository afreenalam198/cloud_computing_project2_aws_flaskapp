# Cloud Computing Project 2: Interactive Web Application on AWS

This project demonstrates the deployment of an interactive web application on an Amazon EC2 instance using Flask, SQLite3, and Apache.  
The application allows users to register, log in, view personal information, and interact with a file upload/download feature.

## Project Requirements and Implementation

This project fulfills the following requirements:

1.  **EC2 Instance Launch:**

    *   Set up my AWS portal.
    *   Launched an EC2 instance.
    *   Used Ubuntu Server 24.04 LTS as Amazon Machine Image (AMI).
    *   Created a key pair for login and set up network and storage settings.

2.  **Web Server and Database Configuration:**

    *   Connected to the instance via SSH.
    *   Configured Apache web server to serve the Flask application using mod\_wsgi.
    *   Set up SQLite3 database to store user data.

3.  **Interactive Web Page Design:**

    *   The interactive web page implements the following functionalities:

    *   **a. Registration Page:**
        *   Allows users to register with their first name, last name, email, address, username and password.
        *   Includes a button to upload a text file.
        *   Data is securely stored in the SQLite3 database using password hashing with bcrypt.  
            <img width="1470" alt="Screenshot 2025-02-15 at 2 28 30 AM" src="https://github.com/user-attachments/assets/4397b793-71cd-4ab0-a07c-36575a626861" />  
  

    *   **b. User Profile Page:**
        *   Redirects to a display page after successful registration form submission.
        *   Displays the user information entered during registration.
        *   If the user uploaded a file during registration, it displays the word count from the uploaded file on this page  
            and provides a button to download the uploaded file.
        *   Includes a log out button.
            <img width="1470" alt="Screenshot 2025-02-15 at 2 33 23 AM" src="https://github.com/user-attachments/assets/43e23f4d-b80f-409f-9bfb-ecb394bf0593" />
            <img width="1470" alt="Screenshot 2025-02-18 at 7 22 45 PM" src="https://github.com/user-attachments/assets/0946467a-50d7-4d98-95ae-1dd86752dc92" />  

 
    *   **c. Login Page:**
        *   Allows users to log in using their username and password.
        *   Retrieves and displays user information upon successful login.
            <img width="1470" alt="Screenshot 2025-02-15 at 2 24 45 AM" src="https://github.com/user-attachments/assets/4d6f13aa-99aa-46eb-8afd-a0e2dc999f68" />  

## AWS URL

The web application is accessible at the following URL:

*  [Site Link](http://ec2-3-137-218-214.us-east-2.compute.amazonaws.com)

## Technologies Used:

*   Amazon EC2
*   Apache
*   mod\_wsgi
*   Flask
*   SQLite3
*   Python
*   HTML
*   CSS
