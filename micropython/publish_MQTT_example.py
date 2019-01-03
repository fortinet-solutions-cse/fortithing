from simple import MQTTClient

server = "accountid.messaging.internetofthings.ibmcloud.com"
client_id = "d:accountid:DeviceType:DeviceId"
port = 1883
ssl = False
user = "use-token-auth"
password = "mypassword"

c = MQTTClient(client_id=client_id, server=server, port=port, ssl=ssl, user=user, password=password)
c.connect()
c.publish(b"iot-2/evt/pressure/fmt/json", b'{ "pressure":"901"}')    
c.disconnect()
