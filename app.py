from flask import Flask, render_template
from flask_mail import Mail, Message
from packets import sniffer
import random, datetime, psutil

app = Flask(__name__)
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'parshva.barbhaya@somaiya.edu',
	MAIL_PASSWORD = 'pwd'
	)
mail = Mail(app)

sniff = sniffer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/see')
def about():
    return render_template('about.html', items = sniff)

@app.route('/deploy')
def deploy():
    error = ''
    string = ''
    
    for i in range(0, 20):
        error += 'Error code: '+(str(random.randint(10,1000))) + 'at line '+(str(random.randint(1,10000)))+'\n'

    if random.randint(0, 100) % 10==0:
        # return "Error"
        try:
            msg = Message("Error while deploying, please check",
		  sender="parshva.barbhaya@somaiya.edu",
		  recipients=["parshva.barbhaya@somaiya.edu"])
            msg.body = error           
            mail.send(msg)
            string = 'Deployment successful!'
        except Exception as e:
            string = str(e)
    else:
        try:
            msg = Message("Service succesfully deployed",
		  sender="parshva.barbhaya@somaiya.edu",
		  recipients=["parshva.barbhaya@somaiya.edu"])
            msg.body = 'No errors found\n Service dployed at '+(str(datetime.datetime.now()))
            mail.send(msg)
            string = 'Deployment unsuccessful!!'
        except Exception as e:
            string = str(e)
        # return "Can be deployed"
    
    return render_template('mail.html', string = string)

@app.route('/check')
def health():
    disk =str(psutil.disk_usage('/'))
    networks = psutil.net_io_counters(pernic=True)

    netio = []
    for interfaces, matches in networks.items():
        netio.append({'interface':interfaces,'usage':str(matches)})
    return render_template('health.html', disk = disk, networks = netio)

if __name__ == '__main__':
    app.run(debug=True)