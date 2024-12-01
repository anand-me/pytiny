PyTiny Deployment Guide
Local Development Setup

Clone the repository:

bashCopygit clone https://github.com/anand-me/pytiny.git
cd pytiny

Create and activate virtual environment:

bashCopypython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

bashCopypip install -r requirements.txt

Run development server:

bashCopypython wsgi.py
Production Deployment
Method 1: Using Gunicorn (Linux/Unix)

Install requirements:

bashCopypip install -r requirements.txt

Create a .env file:

bashCopyPYTINY_HOST=0.0.0.0
PYTINY_PORT=5000
PYTINY_BASE_URL=https://your-domain.com  # Replace with your domain
PYTINY_DEBUG=false
PYTINY_SECRET_KEY=your-secure-secret-key
PYTINY_DB_PATH=/path/to/your/database.db

Run with Gunicorn:

bashCopygunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
Method 2: Using Docker

Build the Docker image:

bashCopydocker build -t pytiny .

Run the container:

bashCopydocker run -d -p 5000:5000 \
  -e PYTINY_BASE_URL=https://your-domain.com \
  -e PYTINY_SECRET_KEY=your-secure-secret-key \
  -v /path/to/data:/app/data \
  pytiny
Important Notes

Always use HTTPS in production
Set a secure SECRET_KEY
Use a proper database path with write permissions
Consider using a reverse proxy (nginx/Apache)
Set up proper monitoring and logging

Quick Start (Your Current Setup)
For FSU network setup (146.201.18.60):

Clone and setup:

bashCopygit clone https://github.com/anand-me/pytiny.git
cd pytiny
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Create .env file:

bashCopyPYTINY_HOST=0.0.0.0
PYTINY_PORT=5000
PYTINY_BASE_URL=http://146.201.18.60:5000
PYTINY_DEBUG=false

Run the server:

bashCopypython wsgi.py
The service will be available at http://146.201.18.60:5000
Security Considerations

Use HTTPS in production
Set proper firewall rules
Keep dependencies updated
Use secure session management
Implement rate limiting
