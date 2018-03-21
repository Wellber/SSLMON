# coding: latin-1
from datetime import datetime
import OpenSSL
import socket

#path where the script will create the .html page
#Local onde será criada a pagina .html
page=open('C:\inetpub\wwwroot\index.html','w')

DOMINIOS=open('certs.mon', 'r')

#Date now
#Data de agora
cur_date = datetime.utcnow()
page.write("<title>SSL MONITOR</title>\n")
page.write("<body>\n")
page.write('<link rel="stylesheet" type="text/css" href="style.css">\n')
page.write('<table border=8>\n')
page.write('<tr>\n')
page.write('<th><h2>Certificados</h2></th>\n')
page.write('<th><h2>Dias para Expiração</h2></th>\n')
page.write('</tr>\n')
page.write("<indent>\n")
page.write('<font style="font-size:0px"> UP </font>')
for dominio in DOMINIOS:
    try:
        HOST=dominio.strip().split(":")[0]
        PORT=dominio.strip().split(":")[1]
        page.write("<tr>\n")
        CONTEXT = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)
        CONN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CONN.connect((str(HOST), int(PORT)))
        CONT = OpenSSL.SSL.Connection(CONTEXT, CONN)
        CONT.set_connect_state()
        CONT.do_handshake()
        CERT=CONT.get_peer_certificate()
        CONN.close()
        edate = CERT.get_notAfter()
        edate = edate.decode()
        exp_date = datetime.strptime(edate,'%Y%m%d%H%M%SZ')
        days_to_expire = int((exp_date - cur_date).days)
        if days_to_expire <= -1 :
            page.write('<td><h2><font color=#181407><strike>'+ (CERT.get_subject().commonName)+ ' </strike></td></h2></font>\n')
            pagae.write('<td><h2><font color=#181407><strike>'+ str(days_to_expire)+ ' </strike></td></h2></font>\n')
        elif days_to_expire <= 30:
            page.write('<td><h2><font color=#800000>'+ (CERT.get_subject().commonName)+ ' </h2></td></font>\n')
            page.write('<td><h2><font color=#800000>'+ str(days_to_expire)+ ' </td></h2></font>\n')
            if days_to_expire < 5:
                page.write('<td><h2><font color=#800000>PRECISA RENOVAR ' + (CERT.get_subject().commonName) + ' </h2></td></font>\n')

        elif days_to_expire <=60:
            page.write('<td><h2><font color=#e6ac00>' + (CERT.get_subject().commonName) + ' </td></h2></font>\n')
            page.write('<td><h2><font color=#e6ac00>'+ str(days_to_expire) + ' </td></h2></font>\n')

        else:
            page.write("<td><h2><font color=#006600>" + (CERT.get_subject().commonName)+ "</td></h2></font>\n")
            page.write("<td><h2><font color=#006600>" + str(days_to_expire) + " </td></h2></font>\n")
        page.write("</tr>\n")

    except:
        #print("ERROR ON CONNECTION TO SERVER,", HOST)
        continue
page.write("</table>\n")
page.write("</indent>\n")
page.write("</body>\n")
page.close()
DOMINIOS.close()

#verify if certificate needs renew
#if the certificate needs renew then the script gonna change the word UP to DOWN, so the whatsup monitor will send an alert.
if 'PRECISA RENOVAR' in open('C:\inetpub\wwwroot\index.html').read():
    with open('C:\inetpub\wwwroot\index.html', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('<font style="font-size:0px"> UP </font>','<font style="font-size:0px"> DOWN </font>')
    with open('C:\inetpub\wwwroot\index.html', 'w') as file:
        file.write(filedata)
