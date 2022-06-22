# -*- coding: utf-8 -*-
# @Time    : 2022/6/5 14:51
# @Author  : dai
# @Email   : 320613249@qq.com


from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, GroupIncreaseNoticeEvent, Event
from nonebot import on_notice, on_command

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import configparser

import random
import string

# 加载配置
config = configparser.ConfigParser()
config.read(r'..\tx-bot\配置.ini', encoding='utf-8')
db_cfg = dict(config.items('发送邮箱配置'))

zh = db_cfg['发件人账号']
pw = db_cfg['密码']
smtp = db_cfg['smtp地址']
name = db_cfg['发件人名称']
tet = db_cfg['邮件标题']
c_s = db_cfg['管理员账号']


# 打开html
def email_html():

    with open('../tx-bot/html.txt', 'r', encoding='utf-8') as f:
        html0 = f.read()
        return html0


#  随机字符和时间
def ht():

    import time
    time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))   # 时间
    value = ''.join(random.sample(string.ascii_letters + string.digits, 8))  # 8位随机数
    html0 = email_html()
    html = html0 + time + value
    return html


lst0 = db_cfg['监控群号']
lst1 = lst0.split(',')

welcom = on_notice()


# 监控新人进群
@welcom.handle()
async def h_r(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):  # event: GroupIncreaseNoticeEvent  群成员增加事件
    # 监控群
    for i in lst1:
        item = int(i)
        if event.group_id == item:
            qq = str(event.user_id)
            mail = qq + '@qq.com'
            html = ht()
            sendmail(mail, zh, pw, smtp, name, tet, html)
            await bot.send_private_msg(user_id=c_s, message='发送成功')


ceshi = on_command('测试', priority=2, block=True)

# 发给自己的测试
@ceshi.handle()
async def cs(bot: Bot, event: Event):
    if int(event.get_user_id()) == 320613249:
        mail = c_s + '@qq.com'
        html = ht()
        sendmail(mail, zh, pw, smtp, name, tet, html)
        await bot.send_private_msg(user_id=c_s, message='测试邮件发送成功')

def sendmail(mail, zh, mm, smtp, name, tt, html):
    # 邮件文本

    msg = MIMEText(html, "html", "utf-8")
    # 邮件上显示的发件人
    msg["From"] = formataddr([name, zh])
    # 邮件上显示的主题
    msg["Subject"] = tt

    server = smtplib.SMTP_SSL(smtp)  # 这个就是上面的SMTP
    # 注意：不同邮箱的SMTP不同
    server.login(zh, mm)  # 登录邮箱

    # 发件人信箱
    server.sendmail(zh, mail, msg.as_string())
    server.quit()

