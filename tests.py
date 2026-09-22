'''
NEED TO ADD:
    REQUESTS FRAME / WHATEVER THE FUCK ITS CALLED (I HAVENT READ THE DOCS YET LOL)
     - WHEREVER THIS LEADS ME
    ALSO NEED TO ANNOTATE STUFF BUT LIKE I CAN DO THAT SOME OTHER TIME (NEVER)
    ADD SSH TO ALLOW FOR HTTPS BECAUSE HALF THE WEBSITES REJECT HTTP THESE DAYS
'''

from SettingsFrame import SettingsData
import socket

host = "example.com"

connection = socket.create_connection((host, 80))

connectionPreface = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
settingsFrame = SettingsData({
    "SETTINGS_MAX_CONCURRENT_STREAMS": bytes.fromhex("00000064"),
    "SETTINGS_INITIAL_WINDOW_SIZE": bytes.fromhex("0000ffff")
})

data = connectionPreface + settingsFrame.to_bytes()

print(data)

connection.send(data)
print(connection.recv(1024))
