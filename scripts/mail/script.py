import csv
import os
import configparser
import logging
import time
from os.path import basename
import xml.etree.ElementTree as ET
import smtplib
import datetime

from email.utils import make_msgid, formatdate
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.message import MIMEMessage
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
import dkim

from jinja2 import Environment, Template


def extract_maires():
    with open('maires.csv') as csvfile:
        with open('maires-to-mail-0.csv', 'w') as outputcsv:
            with open('maires-no-mail-0.csv', 'w') as missingcsv:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                writer = csv.writer(outputcsv, delimiter=',', quotechar='"')
                missing = csv.writer(missingcsv, delimiter=',', quotechar='"')
                for row in reader:
                    email = get_email(row[0], row[2])
                    if email is not None:
                        if email == '':
                            row.append('NoMail')
                            missing.writerow(row)
                        else:
                            row.append(email)
                            writer.writerow(row)
                    else:
                        row.append('NoFile')
                        missing.writerow(row)

def get_email(dpt, insee):
    dom = {'ZA' : '971', 'ZB': '972', 'ZC': '973', 'ZD': '974', 'ZM': '976', 'ZN': '988', 'ZP': '987', 'ZS': '975'}
    if len(dpt) == 1:
        dpt = '0' + dpt
    if len(insee) == 1:
        insee = '00' + insee
    elif len(insee) == 2:
        insee = '0' + insee
    if dpt in dom:
        dpt = dom[dpt]
        return None
    
    path = 'organismes/' + dpt + '/mairie-' + dpt + insee + '-01.xml'
    if not os.path.exists(path):
        return None
    
    tree = ET.parse(path)
    root = tree.getroot()
    email = root.find('CoordonnéesNum')
    if email is None:
        return ''
    email = email.find('Email')
    if email is None:
        return ''
    else:
        return email.text

def init():
    global server
    server = smtplib.SMTP_SSL(host='mail.gandi.net', port=465)
    server.ehlo()
    server.login(config['DEFAULT']['Login'], config['DEFAULT']['Password'])

def end():
    server.quit()

def send_mail(adress, maire = {}, real_send=False):
    with open('mail.private', 'rb') as f:
        private_key = f.read()
    
    msg = MIMEMultipart()
    msg['Subject'] = 'Élection présidentielle française de 2017'
    msg['From'] = 'Vincent Lamotte <me@vlamotte.fr>'
    msg['To'] = adress
    msg['Date'] = formatdate(localtime=True)
    msg['Message-Id'] = make_msgid(domain='vlamotte.fr')

    with open('template.jinja', 'r') as t:
        template = Template(t.read())
        msg_text = MIMEText(template.render(maire=maire))
        msg.attach(msg_text)
    
    with open('ProgrammeLamotte2017.pdf', 'rb') as pdf:
        msg_pdf = MIMEBase('application', "octet-stream")
        msg_pdf.set_payload(pdf.read())
        encoders.encode_base64(msg_pdf)
        msg_pdf.add_header('Content-Disposition', 'attachment; filename="ProgrammeLamotte2017.pdf"')
        msg.attach(msg_pdf)

    msg_byte = bytes(msg.as_string(), encoding='utf-8')
    sign = dkim.sign(msg_byte, domain=b'vlamotte.fr', selector=b'mail', privkey=private_key, include_headers=[b'From',b'To', b'Date', b'Subject']) 
    msg_byte = sign + msg_byte

    if real_send:
        try:
            result = server.sendmail(msg['From'], msg['To'], msg_byte)
            result = 'OK'
        except smtplib.SMTPServerDisconnected as e:
            result = 'KO'
            logging.warning('#' + str(e))
            time.sleep(180)
            init()
        except smtplib.SMTPSenderRefused as e:
            result = 'KO'
            logging.warning('#' + str(e))
            end()
            time.sleep(180)
            init()
        except Exception as e:
            result = 'KO'
            logging.warning('#' + str(e))
    else:
        result = 'OK'
    return result

def analyze_log(processed_maires, log_name):
    with open(log_name, 'r') as textfile:
        for line in textfile:
            if line[-3:-1] == 'OK' or line[-3:-1] == 'KO':
                line = line[10:-1]
                splitted = line.split(',')
                processed_maires.add((splitted[0], splitted[2]))

def batch_send(processed_maires, file_name='test-maires-to-mail.csv', real_send=False):
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        row_count = sum(1 for row in reader)
        csvfile.seek(0)
        row_current = 0
        for row in reader:
            if (row[0], row[2]) in processed_maires:
                row_current = row_current + 1
                continue
            row_current = row_current + 1
            maire = { "departement_nombre" : row[0],
                      "departement_nom" : row[1],
                      "commune_insee" : row[2],
                      "commune_nom" : row[3],
                      "commune_population" : row[4],
                      "nom" : row[5],
                      "prenom" : row[6],
                      "civilite" : row[7],
                      "date" : row[8]}
            result = send_mail(row[11], maire=maire, real_send=real_send)
            if real_send:
                logging.info(','.join(row + [result]))
            else:
                print(','.join(row + [result]))
            print('# ' + str(row_current) + '/' + str(row_count) + ' (' 
                  + str(int(row_current*100.0/row_count)) + '%)')
            time.sleep(10)

config = configparser.ConfigParser()
config['DEFAULT'] = {'Login': '', 'Password': ''}
config.read('cfg.ini')

run_number = 0
log_name = 'run-' + str(run_number) + '.log'
input_name='maires-to-mail-' + str(run_number) + '.csv'
processed_maires = set()


logging.basicConfig(filename=log_name, level=logging.INFO)
init()

#extract_maires()
analyze_log(processed_maires, log_name)
batch_send(processed_maires, file_name=input_name, real_send=False)
#print(send_mail('me@vlamotte.fr', maire=[], real_send=True))

end()

