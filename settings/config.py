from dotenv import load_dotenv
import os

# Manually load the .env file
load_dotenv()

# Print the value to check if it's being loaded
DATABASE_URL= os.getenv("DATABASE_URL")

# Define Allowed IPs
ALLOWED_IPS = {"*"}  # Set specific IPs to restrict access, or "*" to allow all

