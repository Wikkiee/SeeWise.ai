# SeeWise.ai Task One Installation Guide

This guide will walk you through setting up Task One of the SeeWise.ai interview task repository on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- [Python](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en)
- [Git](https://git-scm.com/downloads)

## Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Wikkiee/SeeWise.ai.git
   ```
2. **Navigate to Task One**
```bash
cd SeeWise.ai/TaskOne
```
3. **Install Backend Dependencies**<br>
Navigate to the backend directory and install Python libraries:
```bash
cd backend
pip install -r requirements.txt
```
4. **Set Up Environment Variables**<br>
Create a .env file in the backend directory and set environment variables. Use .sample-env as a reference.
5. **Run the Django Backend** <br>
Apply migrations and start the Django development server:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
The backend will be accessible at `http://localhost:8000`.
6. **Install Frontend Dependencies**<br>
Open a new terminal window/tab.Navigate to the frontend directory within Task One:
```bash
cd TaskOne/frontend
npm install
```
7. **Set Up Frontend Environment Variables**<br>
Create a .env file in the frontend directory and set environment variables similar to .sample-env.
8. **Run the React Frontend**<br>
Start the React development server:
```bash
npm run dev

```
The frontend will be accessible at `http://localhost:3000`.

# Backend API Endpoints

**Base URL:** `http://localhost:8000/`

### Authentication Endpoints

- **Register User:** `POST /api/user/register/`
- **Get Access Token:** `POST /api/token/`
- **Refresh Access Token:** `POST /api/token/refresh/`

### Video Endpoints

- **List/Create All Videos:** `GET/POST api/videos/` - `all-video-list`
- **Get Video by Bucket ID:** `GET api/videos/get/<str:bucket_id>/` - `get_video_by_id`
- **Retrieve and Upload Video:** `GET/POST api/videos/retrive-and-upload/` - `user-video-list`
- **Delete Video by ID:** `DELETE api/videos/delete/<int:pk>/` - `video-delete`
- **Update Video Title:** `PUT api/videos/update/<int:pk>/` - `video-title-update`
- **Search Videos by Term:** `GET api/videos/search/<str:search_term>/` - `search-video-list`
- **Stream Video:** `GET api/videos/stream/` - `video-stream`

# API Endpoint Testing with Postman

For testing the API endpoints of this application, you can use the provided Postman collection:

[Postman API Endpoint Collection](https://www.postman.com/vignesh7550/workspace/seewise-ai-assignment/request/13982664-9fa5043c-e2ea-410f-b7b2-e9815c6cbda5)

## How to Use the Postman Collection

1. **Download Postman**: If you don't have Postman installed, [download and install it](https://www.postman.com/downloads/).

2. **Import Collection**:
   - Click on the provided [Postman API Endpoint Collection](https://www.postman.com/vignesh7550/workspace/seewise-ai-assignment/request/13982664-9fa5043c-e2ea-410f-b7b2-e9815c6cbda5) link.
   - Click on the "Run in Postman" button.
   - Open Postman and import the collection into your workspace.

3. **Configure Environment (Optional)**:
   - If the collection requires environment variables, set up a new environment in Postman.
   - Update the environment variables with appropriate values (e.g., `base_url`).

4. **Test Endpoints**:
   - Navigate through the collection folders to find specific endpoints.
   - Click on an endpoint to view its details and send requests (e.g., `POST`, `GET`, `PUT`, `DELETE`).

5. **Review Responses**:
   - After sending requests, review the responses to ensure the API endpoints are functioning correctly.

## Additional Notes

- Ensure that the backend server is running (`python manage.py runserver`) before testing the API endpoints.
- Modify the request payloads and parameters in Postman according to the API endpoint requirements.
- Refer to the API documentation or source code for more details on request formats and expected responses.

These endpoints allow you to interact with the backend API of your Django application. Replace `<str:bucket_id>` and `<int:pk>` with actual values when making requests.

## Additional Notes

- Ensure to replace `localhost` with the appropriate domain or IP address if deploying your application.
- For detailed usage instructions and payload examples, refer to the API documentation or view the Django views associated with these endpoints.
1. **Obtain Access Token**
   - First, make a `POST` request to `/api/token/` endpoint to obtain an access token. You will need to provide valid credentials (username and password) in the request body.
   - Copy the access token from the response.

2. **Add Authorization to Requests**
   - For protected endpoints that require authentication, select the request in Postman.
   - Click on the "Authorization" tab.
   - Choose "Bearer Token" from the dropdown menu.
   - Paste the copied access token into the "Token" field.


## Running Tests for Task One

To run the test on the Task One, execute the following command in your terminal:
```bash
python manage.py test
```
This command will run the tests defined in api/test.py and display the test results directly in the terminal.

# Running Task Two

Follow these steps to set up and run Task Two of the project:

1. **Navigate to TaskTwo and Backend Folder**

   Change directories to TaskTwo and then to the backend folder:
   ```bash
    cd TaskTwo/backend
    ```

2. **Install Required Packages**

Install the necessary packages using pip based on the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

3. **Set Up Environment Variables**

Create a `.env` file in the root of the backend folder. You can use `.sample-env` as a reference to configure the environment variables.

4. **Apply Migrations**

Run database migrations to apply changes to the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Run the Application**

Start the Django development server to run the application:

```bash
python manage.py runserver
```

6. **Running Tests**

To run tests for Task Two, use the following command:

```bash
python manage.py test
```

This command will execute the tests defined in the project and display the test results.

# Task Two API Endpoints

The following endpoints are available for Task Two of the project:

**Base URL:** `http://localhost:8000`

## Endpoints

### Machines

- **List/Create Machines:**
  - URL: `/api/machines/`
  - Method: `GET` (List), `POST` (Create)
  - View: `MachineListCreateView`
  - Name: `machine-list`

- **Retrieve/Update/Delete Machine:**
  - URL: `/api/machines/<int:pk>/`
  - Method: `GET` (Retrieve), `PUT` (Update), `DELETE` (Delete)
  - View: `MachineDetailView`
  - Name: `machine-detail`

### Production Logs

- **List/Create Production Logs:**
  - URL: `/api/production_logs/`
  - Method: `GET` (List), `POST` (Create)
  - View: `ProductionLogListCreateView`
  - Name: `production-log-list`

- **Retrieve/Update/Delete Production Log:**
  - URL: `/api/production_logs/<int:pk>/`
  - Method: `GET` (Retrieve), `PUT` (Update), `DELETE` (Delete)
  - View: `ProductionLogDetailView`
  - Name: `production-log-detail`

## Additional Notes

- Replace `<int:pk>` with the specific ID of the machine or production log when making requests for individual resources.
- Use appropriate HTTP methods (`GET`, `POST`, `PUT`, `DELETE`) based on the desired operation.
- Ensure that you have configured the backend environment and have the Django development server running to access these endpoints.






