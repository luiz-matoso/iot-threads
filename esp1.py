import network
import time
from umqtt.simple import MQTTClient
import dht
from machine import Pin, PWM
import _thread

ssid = 'Wokwi-GUEST'
password = ''
mqtt_server = 'mqtt-dashboard.com'
client_id = 'esp_pub'
topic = 'esp/sensors'

# Configuração da conexão Wi-Fi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    time.sleep(1)
    print("Conectando ao Wi-Fi...")

print("Conectado! IP:", station.ifconfig()[0])

client = MQTTClient(client_id, mqtt_server)
client.connect()

# Configuração dos sensores DHT22 e dos servos
sensor1 = dht.DHT22(Pin(14))
sensor2 = dht.DHT22(Pin(18))
servo1 = PWM(Pin(12), freq=50)
servo2 = PWM(Pin(17), freq=50)
switch = Pin(16, Pin.IN, Pin.PULL_UP)

# Função para configurar o ângulo correto do servo
def configurarAnguloCorreto(angle):
    # Calcula o duty cycle correspondente ao ângulo desejado (0-180 graus)
    duty = (angle / 180) * (12.5 - 2.5) + 2.5
    return int(duty * 10)

# Funções para abrir e fechar as comportas dos servos
def abrirComportaServo1():
    servo1.duty(configurarAnguloCorreto(50))  

def fecharComportaServo1():
    servo1.duty(configurarAnguloCorreto(0))

def abrirComportaServo2():
    servo2.duty(configurarAnguloCorreto(180))

def fecharComportaServo2():
    servo2.duty(configurarAnguloCorreto(0))

# Função para publicar os dados dos sensores no tópico MQTT
def publish_sensor_data():
    if switch.value() == 0:  # Se o interruptor estiver desligado, não envia dados
        return

    # Mede a temperatura e umidade dos sensores
    sensor1.measure()
    temp1 = sensor1.temperature()
    humidity1 = sensor1.humidity()

    sensor2.measure()
    temp2 = sensor2.temperature()
    humidity2 = sensor2.humidity()

    # Cria a mensagem com os dados de umidade
    message = (f"Humidity1:{humidity1},Humidity2:{humidity2}")
    client.publish(topic, message)  # Publica a mensagem no tópico MQTT
    print("Mensagem publicada:", message)

# Thread para gerenciar a leitura dos sensores e controle dos servos
def sensor_thread():
    while True:
        if switch.value() == 0:  # Se o interruptor estiver desligado, fecha as comportas
            fecharComportaServo1()
            fecharComportaServo2()
            time.sleep(2)
        else:
            publish_sensor_data()  # Publica os dados dos sensores

            # Verifica a temperatura do Sensor 1 e ajusta a comporta do Servo 1
            if sensor1.temperature() >= 60:
                abrirComportaServo1()
            else:
                fecharComportaServo1()

            # Verifica a temperatura do Sensor 2 e ajusta a comporta do Servo 2
            if sensor2.temperature() >= 60:
                abrirComportaServo2()
            else:
                fecharComportaServo2()

        time.sleep(2)  # Aguarda 2 segundos antes de repetir

# Inicia a thread para monitorar os sensores e controlar os servos
_thread.start_new_thread(sensor_thread, ())
