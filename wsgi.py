from manage import app as application
from flask_sslify import SSLify

if __name__ == "__main__":
    sslify = SSLify(application)
    application.run()
