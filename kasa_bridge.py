import socket, time, json
from datetime import datetime
import asyncio
from kasa import SmartPlug

config_file = 'config.json'
with open(config_file, 'r') as file:
    config = json.load(file)


plug = SmartPlug(config['plug']['ip'])

def get_data(plug):
    
    try:
        asyncio.run(plug.update())
        data = plug.emeter_realtime

        var_list = ['voltage_mv', 'current_ma', 'power_mw']

        data = {s.split("_")[0]: data[s]/1e3 for s in var_list}
        timestamp = datetime.utcnow()
        
        return timestamp, data
    except:
        return None, None

class UDPSender():
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

        self.conn = (ip, port)

        self.sock = socket.socket(socket.AF_INET, # Internet
                                  socket.SOCK_DGRAM) # UDP

    def send(self, messages):
        for message in messages:
            message = bytearray(message, encoding='utf-8')
            self.sock.sendto(message, self.conn)

udp = UDPSender(config['udp']['ip'], config['udp']['port'])

def get_unix_timestamp(t):
    dt = t - datetime(1970,1,1)
    return int(dt.total_seconds()*1e9)


def prepare_udp_messages(alias, timestamp, data):
    unix_timestamp = get_unix_timestamp(timestamp)

    return [f"{name},alias={alias} value={value:0.3f} {unix_timestamp}"
            for name, value in data.items()]

while True:
    try:
        timestamp, data = get_data(plug)

        if(data is not None):
            messages = prepare_udp_messages(plug.alias, timestamp, data)
            udp.send(messages)

        time.sleep(config['time_period'])
    except (KeyboardInterrupt, SystemExit): # Exit program
        raise
