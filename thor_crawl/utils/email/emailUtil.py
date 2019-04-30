"""
Created by lyj on 16/06/23.
邮件发送模块
"""

import smtplib
from email.mime.text import MIMEText

mailto_list = ["546223592@qq.com"]  # 目标邮箱
mail_host = "smtp.163.com"  # SMTP 服务器主机
mail_user = "luoyanjiewade@163.com"
mail_pass = "zucc416lyj"  # 163邮箱smtp生成的密码


class EmailUtils(object):
    @staticmethod
    def send_mail(sub, content, to_list=mailto_list):
        me = "lyj" + "<" + mail_user + ">"

        msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)

        try:
            server = smtplib.SMTP()
            server.connect(mail_host)
            server.login(mail_user, mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            return True
        except smtplib.SMTPException:
            return False


if __name__ == '__main__':
    EmailUtils.send_mail('紧急!!!', '爬虫被ban了!!!!赶紧去处理吧111==')
