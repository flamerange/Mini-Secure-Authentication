# Deploying the Mini Secure Authentication Server on Render.com

Follow these step-by-step instructions to take this application from local testing to a live, production-grade deployment on Render.

## Step 1: Pre-requisites
Make sure your project files (`main.py`, `requirements.txt`, `.env`, `templates/*`, etc.) are pushed to a public or private GitHub/GitLab repository. 

*Note: Render integrates seamlessly by directly connecting to your git repository.*

## Step 2: Create a New Web Service
1. Sign up or log in to your account at [Render.com](https://render.com).
2. Click the **"New +"** button in the top right corner.
3. Select **"Web Service"**.
4. Connect the repository where your project is stored.

## Step 3: Configure the Build Settings
Once connected, enter the following configurations carefully:
- **Name:** Choose a unique name (e.g., `mini-secure-auth-server`)
- **Region:** Ohio (US East) or Frankfurt (EU Central) based on your target audience
- **Branch:** `main` (or whichever branch holds your code)
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

> **Note on Start Command:** Render automatically injects the `$PORT` environment variable. Our app relies on `uvicorn` mapping to this specific port on `0.0.0.0`. 

## Step 4: Configure Environment Variables
Scroll down to the **"Environment Variables"** section. Click **"Add Environment Variable"** and define the following exact keys to match your `.env` configuration:

| Key | Value |
|---|---|
| `JWT_SECRET_KEY` | `superSecretKeyForMiniAuthServer2026_RishavProject_1234567890` (Or highly secure alternative) |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |

## Step 5: Deploy
1. Choose the **Free Plan** instance type for your initial deployment.
2. Click **Create Web Service**. 

Render will now build your application, fetch the requirements, and map the port. Once the dashboard indicates the instance is `Live`, you can access your deployment at the provided `*.onrender.com` URL.

## Important: Database Data Persistence limitations
Because we are utilizing the built-in SQLite framework, please remember that Render's free tier functions via Ephemeral Storage. 
This means any changes to `sql_app.db` (like newly registered users) will reset whenever your application is restarted or re-deployed. To migrate to persistent data, transition the SQLAlchemy connection string from SQLite to a fully managed **Render PostgreSQL** database.
