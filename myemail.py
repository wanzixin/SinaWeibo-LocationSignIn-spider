import configparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 用于发送附件
from email.mime.base import MIMEBase
# 用于图片编码
from email import encoders

def read_ini(inipath='config.ini'):
    config = configparser.ConfigParser()
    config.read(inipath,encoding='utf-8')
    email_address=config.get('Email','email_address')
    return email_address

# 授权码：aimowgoppmbvcbbb
class Email(object):
    def __init__(self,sender='zixinwan@foxmail.com',receiver=['347335189@qq.com']):
        email_address=read_ini()
        self.sender = email_address
        self.receiver = receiver.append(email_address)

        global msg
        msg = MIMEMultipart()

    def send(self,content):
        # 发信方邮箱,授权码,
        sender = self.sender
        password = 'aimowgoppmbvcbbb'        

        # 收信方,可以添加多个
        receiver = self.receiver

        # 服务器地址
        mail_host = 'smtp.qq.com'

        # 设置email信息
        # msg = self.msg

        # 邮件主题
        msg['Subject'] = 'from python'
        # 发送方信息
        msg['From'] = sender
        # 邮件正文是MIMEText:
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        

        #登录并发送邮件
        try:
            #QQsmtp服务器的端口号为465或587
            s = smtplib.SMTP_SSL(mail_host, 465)
            s.set_debuglevel(1)
            s.login(sender,password)
            
            #给receivers列表中的联系人逐个发送邮件
            for item in receiver:
                msg['To'] = to = item
                s.sendmail(sender,to,msg.as_string())
                print('Success!')
            s.quit()
            print ("All emails have been sent over!")
        except smtplib.SMTPException as e:
            print ("Falied,%s",e)
    
    def add_pic(self,filepath):
        # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
        with open(filepath, 'rb') as f:
            # 设置附件的MIME和文件名，这里是jpg类型,可以换png或其他类型:
            mime = MIMEBase('image', 'jpg', filename=filepath)
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename=filepath)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            msg.attach(mime)
        return msg