
# Monitoramento de Ambiente com ESP32

Este projeto utiliza duas placas ESP32 para monitorar e controlar a temperatura e umidade em dois ambientes distintos. As ESPs se comunicam entre si para acionar alarmes e realizar ajustes automáticos em caso de variações nos parâmetros monitorados.

## Funcionalidades

1. **Monitoramento de Temperatura e Umidade:**
   - A **ESP1** monitora dois sensores de temperatura e um sensor de umidade.
   - Se a temperatura em qualquer ambiente atingir **60°C**, o sistema de ventilação será ativado:
     - **Servo Motor 1** abre a comporta em **50°** no primeiro ambiente.
     - **Servo Motor 2** abre a comporta em **180°** no segundo ambiente.
   - Se a umidade em qualquer ambiente cair abaixo de **20%**, a **ESP1** envia uma mensagem para a **ESP2** para ativar os alarmes.

2. **Alarmes e Alertas:**
   - A **ESP2** recebe mensagens da **ESP1** e aciona um alarme sonoro (buzzer) e pisca um LED a cada 1 segundo quando a umidade está baixa.
   - Quando a **ESP1** detecta que a umidade foi normalizada, ela envia uma mensagem para a **ESP2** desativar os alarmes.

3. **Controles Manuais:**
   - Na **ESP2**, um **Slide Switch** permite desativar manualmente os alarmes, mesmo que a umidade continue baixa.
   - Na **ESP1**, um **Slide Switch** permite desativar o envio de mensagens para a **ESP2** e resetar as posições dos servos motores para **0 graus**.

4. **Utilização de Threads:**
   - Todas as operações do projeto devem ser implementadas utilizando threads para garantir a execução simultânea de tarefas.

## Requisitos

- 2 placas ESP32
- 2 Sensores de Temperatura
- 1 Sensor de Umidade
- 2 Servo Motores
- 1 Buzzer
- 1 LED
- 2 Slide Switches

## Deploy

1. **Acesse o link do WOKWI:**
   - ESP1 [Wokwi](https://wokwi.com/projects/408134069448979457)
   - ESP2 [Wokwi](https://wokwi.com/projects/408134100199521281)

2. **Configure o acesso através do Socket Web HiveMQ:**
   - HiveMQ Socket Web [HiveMQ](https://www.hivemq.com/demos/websocket-client/)

3. **Rode os códigos no Wokwi:**
   - Se a configuração do HiveMQ estiver correta com seu respectivo topic o sistema entrará em execução.
   - Altere os parâmetros dos DHTs.

## Contribuição

**Este projeto foi criado por:**

- Guilherme Tuchanski Rocha
- Guilherme Teixeira de Freitas Chemim Guimarães
- Guilherme Augusto Santiago Abib
- Luiz Henrique Matoso
