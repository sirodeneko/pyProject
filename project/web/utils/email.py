import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send(to_who, file_names):
    server_address = 'smtp.qq.com'
    from_who = 'siro-neko@qq.com'
    from_who_password = 'dasunpahgxuddjhi'
    msg = MIMEMultipart()
    msg['Subject'] = '游客流量调查报告'

    content = '''
    来自:%(from_who)s<br>
    发往:%(to_who)s<br>
    主题:游客流量调查报告<br>
    <br>
    你好，这是您订阅的游客流量调查报告邮件，请您查收 Y_^-^_Y
    ''' % {'to_who': ','.join(to_who), 'from_who': from_who}
    content_part = MIMEText(content, 'html', 'utf-8')
    msg.attach(content_part)

    for item in file_names:

        attachment_part = MIMEApplication(open('./static/reports/'+item, 'rb').read())
        attachment_part["Content-Type"] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        attachment_part.add_header('Content-Disposition', 'attachment', filename=item)
        msg.attach(attachment_part)

    server = smtplib.SMTP_SSL(server_address, 465)
    server.login(from_who, from_who_password)
    response = server.sendmail(from_who, to_who, msg.as_string())
    server.quit()

    return
