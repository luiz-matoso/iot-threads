import network
import time
from umqtt.simple import MQTTClient
from machine import Pin
import _thread

ssid = 'Wokwi-GUEST'
password = ''
mqtt_server = 'mqtt-dashboard.com'
client_id = 'esp_sub'
topic = 'esp/sensors'

buzzer = Pin(12, Pin.OUT)
led = Pin(14, Pin.OUT)
switch = Pin(16, Pin.IN, Pin.PULL_UP)

# Variável para armazenar o estado atual do alarme
estado_alarme = False

# Thread do alarme
def trigger_alarm():
    global estado_alarme
    while estado_alarme:
        buzzer.on()
        led.value(1)
        time.sleep(1)
        buzzer.off()
        led.value(0)
        time.sleep(1)

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    time.sleep(1)
    print("Conectando ao Wi-Fi...")

print("Conectado! IP:", station.ifconfig()[0])

client = MQTTClient(client_id, mqtt_server)
client.connect()

# Callback para lidar com mensagens MQTT
def sub_cb(topic, msg):
    global estado_alarme

    # Verifica se o interruptor está desligado
    if switch.value() == 0:
        led.off()
        buzzer.off()
        estado_alarme = False
        return

    print('Mensagem recebida no tópico {}: {}'.format(topic, msg))

    try:
        msg_str = msg.decode()
        data = msg_str.split(',')
        humidity1 = float(data[0].split(':')[1])
        humidity2 = float(data[1].split(':')[1])

        # Verifica se os valores de umidade estão abaixo do limite
        if humidity1 <= 20 or humidity2 <= 20:
            if not estado_alarme:  # Aciona o alarme se ele não estiver já acionado
                estado_alarme = True
                _thread.start_new_thread(trigger_alarm, ())  # Inicia o alarme em uma nova thread
        else:
            estado_alarme = False
            led.off()
            buzzer.off()

    except Exception as e:
        print('Erro ao processar a mensagem:', e)

client.set_callback(sub_cb)
client.subscribe(topic)

# Thread para verificar mensagens MQTT
def mqtt_thread():
    while True:
        try:
            client.check_msg()  # Verifica por novas mensagens MQTT
        except OSError as e:
            print('Erro ao verificar mensagens:', e)
        
        time.sleep(1)

_thread.start_new_thread(mqtt_thread, ())
