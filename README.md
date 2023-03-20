# Advance USA Visa Appointment

A tool that helps to advance an appintment to USA-visa in Israel by performing human like operations on the site.  
**Important:** The use in under responsability of the user - irresponsible usage might block your account.

## Usage Guide:  
This tool able to run on both Desktop and Containerized mode.

### Desktop mode:
```
pip install -r requirements
python3 ./app.py
Enter requested parameters
```

### Containerized mode:
```
docker build -t <image-name> .
docker run -it <image-name> -e email=<account-email>,password=<account-password>,accepted_location<Tel Aviv/Jerusalem>,runon=<all/username>
```
