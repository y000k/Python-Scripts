#!/usr/bin/env python
"""
本代码使用了regex beautifulsoup4 qrcode这三个第三方库，只支持Python3以上的版本，在Linux下写成，请读者自行安装这三个第三方库，如果遇到任何运行问题请联系我。
如果觉得这个脚本帮到了你，不妨为我的GitHub项目加个星呗～
"""
try:
    import regex as re
    from bs4 import BeautifulSoup
    import qrcode
except ImportError:
    print('Python缺少依赖库，请使用pip install -U regex beautifulsoup4 qrcode或者其他方式安装此依赖。\n本软件在Linux下写成，Python版本为3.5，如果遇到任何错误，请到GitHub上提交Issue。\n')
    exit(0)

import sys
import requests
import base64
import json


__author__ = 'Charles Xu'
__email__ = 'charl3s.xu@gmail.com'
__my_girlfriend__ = '小胖儿～'
__url__ = 'https://github.com/the0demiurge/Python-Scripts/blob/master/src/MinorProjects/shadowsocks_free_qrcode.py'


def request_ss_list(url='https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7'):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')

    ss_list = list()

    for i in soup.find_all('p'):
        if re.match('\<p\>\s*服务器\d+[^:：]*[:：]', str(i)):
            ss_list.append(str(i))
    return ss_list


def get_servers(ss_list):
    servers = list()
    for i in ss_list:
        servers.append(dict())
        servers[-1]['string'] = i
        # name
        tmp = re.findall('服务器\d+[^:：]*(?=\s*[:：])', i)
        if tmp:
            servers[-1]['name'] = tmp[0]

        # server
        tmp = re.findall('(?<=服务器\s*\d+[^:：]*[:：])[\w\d\.]+', i)
        if tmp:
            servers[-1]['server'] = tmp[0]

        # server_port
        tmp = re.findall('(?<=端口\s*[^:：]*[:：])\d+', i)
        if tmp:
            servers[-1]['server_port'] = tmp[0]

        # password
        tmp = re.findall('(?<=密码\s*[^:：]*[:：])[\w\d\.\+\-_\*\\/]+', i)
        if tmp:
            servers[-1]['password'] = tmp[0]

        # method
        tmp = re.findall('(?<=加密方[式法]\s*[^:：]*[:：])[\w\d\.\+\-_\*\\/]+', i)
        if tmp:
            servers[-1]['method'] = tmp[0]

        # SSR协议
        tmp = re.findall('(?<=SSR协议\s*[^:：]*[:：])[\w\d\.\+\-_\*\\/]+', i)
        if tmp:
            servers[-1]['ssr_portal'] = tmp[0]

        # 混淆
        tmp = re.findall('(?<=混淆\s*[^:：]*[:：])[\w\d\.\+\-_\*\\/]+', i)
        if tmp:
            servers[-1]['confuse'] = tmp[0]
    return servers


def get_href(string, pattern='.*'):
    found = re.findall('(?<=<a\s+href=")[^"]+(?=">%s</a>)' % pattern, string)
    if found:
        return found[0]


def show_server_info(server_data):
    print('服务器名称为：', server_data['name'])
    try:
        decoded = '{method}:{password}@{hostname}:{port}'.format(
            method=server_data['method'],
            password=server_data['password'],
            hostname=server_data['server'],
            port=server_data['server_port'],
        )
    except KeyError:
        print('请点击此链接获得详细信息：')
        href = get_herf(server_data['string'], '.*查看连接信息.*')
        print(href)
        return href
    print('\nJSON格式的配置文件内容为：')
    json.dump(server_data, sys.stdout, ensure_ascii=False, indent=4)
    ss_uri = 'ss://{}'.format(str(base64.b64encode(bytes(decoded, encoding='utf8')), encoding='utf-8'))
    qr = qrcode.QRCode()
    qr.add_data(ss_uri)
    print('\n\n配置二维码：')
    # qr.print_tty()
    qr.print_ascii()
    print('服务器设置uri为：')
    print(ss_uri)


def main():
    ss_list = request_ss_list()
    servers = get_servers(ss_list)
    while True:
        try:
            print('序  号|服务器名称')
            print('------|---------------')
            for i, server_data in enumerate(servers):
                print(' ', i, ' ', server_data['name'])
            print('请输入左侧一列的序号（输入all可以获得全部服务器资料）：', end='')
            index = input()
            if re.findall('all', index.lower()):
                for server_data in servers:
                    show_server_info(server_data)
            else:
                ind = re.findall('\d+', index)
                while not ind:
                    print('序号输入错误！请重新输入数字：', end='')
                    ind = re.findall('\d+', index)
                ind = int(ind[0])
                show_server_info(servers[ind])
            input('\n如果要继续选择服务器请按回车，否则按Ctrl+C')

        except KeyboardInterrupt:
            print('''
     ____  _               _                ____             _
    / ___|| |__   __ _  __| | _____      __/ ___|  ___   ___| | _____
    \\___ \\| '_ \\ / _` |/ _` |/ _ \\ \\ /\\ / /\\___ \\ / _ \\ / __| |/ / __|
     ___) | | | | (_| | (_| | (_) \\ V  V /  ___) | (_) | (__|   <\\__ \\
    |____/|_| |_|\\__,_|\\__,_|\\___/ \\_/\\_/  |____/ \\___/ \\___|_|\\_\\___/
            ''')
            print('请支持SS帐号分享者，免费ShadowSocks帐号来源：\nhttps://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7')
            print('\n送给我的女朋友小胖儿～')
            print('作者', __author__, 'Email:', __email__)
            print('项目地址：', __url__)
            exit(0)


if __name__ == '__main__':
    main()