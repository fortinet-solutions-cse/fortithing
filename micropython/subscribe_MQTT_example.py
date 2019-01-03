from simple import MQTTClient

server = "accountid.messaging.internetofthings.ibmcloud.com"
client_id = "d:accountid:DeviceType:DeviceId"
port = 1883
ssl = False
user = "use-token-auth"
password = "mypassword"


def sub_cb(topic, msg):
    print((topic, msg))


c = MQTTClient(client_id=client_id, server=server, port=port, ssl=ssl, user=user, password=password)
c.set_callback(sub_cb)
c.connect()
c.subscribe("iot-2/cmd/set_lights/fmt/json")

try:
    while 1:
        c.wait_msg()
finally:
        c.disconnect()
