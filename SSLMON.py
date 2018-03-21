import ssl
from datetime import datetime
import OpenSSL
import socket

#Dominios a serem verificados
#Adicionar o dominio por linha seguindo o exemplo abaixo:
#ex: netpoint.com.br:443
DOMINIOS=open('ceds.checks', 'r')
#Data de agora
cur_date = datetime.utcnow()
NTK105="189.14.105."
NTK106="189.14.106."
NTK187="187.16.24."
print ('<body style="background-color:grey;">')
print("<table border=1>")
print("<tr>")
print("<th>Certificados</th>")
print("<th>Dias para Expiração</th>")
print("</tr>")
print("<indent>")
PORT=443
for dominio in range(1,254):
    dominio=str(dominio)
    try:
        #HOST=dominio.strip().split(":")[0]
        #PORT=dominio.strip().split(":")[1]
        print("<tr>")
        CONTEXT = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)
        CONN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        CONN.connect((str(NTK105 + dominio), int(PORT)))
        CONT = OpenSSL.SSL.Connection(CONTEXT, CONN)
        CONT.set_connect_state()
        CONT.do_handshake()
        CERT=CONT.get_peer_certificate()
        CONN.close()
        edate = CERT.get_notAfter()
        edate = edate.decode()
        exp_date = datetime.strptime(edate,'%Y%m%d%H%M%SZ')
        days_to_expire = int((exp_date - cur_date).days)
        if days_to_expire <= 30:
            print('<td><h2><font color=#800000>', (CERT.get_subject().commonName), ' </h2></td></font>')
            print('<td><h2><font color=#800000>', days_to_expire, ' </td></h2></font>')
        elif days_to_expire <=60:
            print('<td><h2><font color=#e6ac00>', (CERT.get_subject().commonName), ' </td></h2></font>')
            print('<td><h2><font color=#e6ac00>', days_to_expire, ' </td></h2></font>')
        else:
            print('<td><h2><font color=#006600>', (CERT.get_subject().commonName), ' </td></h2></font>')
            print('<td><h2><font color=#006600>', days_to_expire, ' </td></h2></font>')

        print("</tr>")
    except:
        print("ERROR ON CONNECTION TO SERVER, ", NTK105 + dominio)
print("</indent>")
print("</table>")
print ('</body>')