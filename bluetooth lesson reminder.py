import datetime
from gtts import gTTS
import os
import time
import bluetooth

# Define the timetable dictionary
timetable = {
    "Monday": {
        "8:00-8:40": "FORM 4 GEOGRAPHY",
        "8:40-9:20": "FORM 3 HISTORY",
        "9:20-10:00": "BREAK",
        "10:00-10:40": "FORM 4",
        "10:40-11:20": "FORM 1",
        "11:20-12:00": "FORM 2",
        "12:00-12:40": "FORM 3",
        "12:40-13:20": "FORM 4",
        "13:20-14:00": "FORM 1",
        "14:00-14:40": "FORM 2",
        "14:40-15:00": "FORM 3",
        "15:00-15:40": "FORM 4",
        "15:40-16:20": "FORM 2",
        "16:20-17:00": "FORM 3"
        
    },
    
    "Tuesday": {
        "8:00-8:40": "FORM 4 GEOGRAPHY",
        "8:40-9:20": "FORM 3 HISTORY",
        "9:20-10:00": "BREAK",
        "10:00-10:40": "FORM 4",
        "10:40-11:20": "FORM 1",
        "11:20-12:00": "FORM 2",
        "12:00-12:40": "FORM 3",
        "12:40-13:20": "FORM 4",
        "13:20-14:00": "FORM 1",
        "14:00-14:40": "FORM 2",
        "14:40-15:00": "FORM 3",
        "15:00-15:40": "FORM 4",
        "15:40-16:20": "FORM 2",
        "16:20-17:00": "FORM 3"
        
    },
    
    "Wednesday": {
        "8:00-8:40": "FORM 4 GEOGRAPHY",
        "8:40-9:20": "FORM 3 HISTORY",
        "9:20-10:00": "BREAK",
        "10:00-10:40": "FORM 4",
        "10:40-11:20": "FORM 1",
        "11:20-12:00": "FORM 2",
        "12:00-12:40": "FORM 3",
        "12:40-13:20": "FORM 4",
        "13:20-14:00": "FORM 1",
        "14:00-14:40": "FORM 2",
        "14:40-15:00": "FORM 3",
        "15:00-15:40": "FORM 4",
        "15:40-16:20": "FORM 2",
        "16:20-17:00": "FORM 3"
        
    },
    "Thursday": {
        "8:00-8:40": "FORM 4 GEOGRAPHY",
        "8:40-9:20": "FORM 3 HISTORY",
        "9:20-10:00": "BREAK",
        "10:00-10:40": "FORM 4",
        "10:40-11:20": "FORM 1",
        "11:20-12:00": "FORM 2",
        "12:00-12:40": "FORM 3",
        "12:40-13:20": "FORM 4",
        "13:20-14:00": "FORM 1",
        "14:00-14:40": "FORM 2",
        "14:40-15:00": "FORM 3",
        "15:00-15:40": "FORM 4",
        "15:40-16:20": "FORM 2",
        "16:20-17:00": "FORM 3"
        
    },
    "Friday": {
        "8:00-8:40": "FORM 4 GEOGRAPHY",
        "8:40-9:20": "FORM 3 HISTORY",
        "9:20-10:00": "BREAK",
        "10:00-10:40": "FORM 4",
        "10:40-11:20": "FORM 1",
        "11:20-12:00": "FORM 2",
        "12:00-12:40": "FORM 3",
        "12:40-13:20": "FORM 4",
        "13:20-14:00": "FORM 1",
        "14:00-14:40": "FORM 2",
        "14:40-15:00": "FORM 3",
        "15:00-15:40": "FORM 4",
        "15:40-16:20": "FORM 2",
        "16:20-17:00": "FORM 3"
        
    }
    
    
    
}

current_day = datetime.datetime.now().strftime("%A") # get the current day's name

# Check if the day name is valid
if current_day not in timetable:
    print("Invalid day name!")
else:
    while True:  # repeat forever
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        # Loop through the timetable to find the matching class
        for day, classes in timetable.items():
            if day == current_day:
                for time_range, class_name in classes.items():
                    start_time, end_time = time_range.split("-")
                    if start_time <= current_time <= end_time:
                        message = f"On today {day}, you have {class_name} from {time_range}. Please be punctual!"
                        tts = gTTS(message)
                        tts.save('message.mp3')
                        
                        # Open a Bluetooth connection
                        server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
                        server_sock.bind(("",bluetooth.PORT_ANY))
                        server_sock.listen(1)
                        port = server_sock.getsockname()[1]
                        
                        # Print the port number for other devices to connect to
                        print("Waiting for connection on RFCOMM channel", port)
                        
                        bluetooth.advertise_service( server_sock, "SampleServer",
                            service_classes=[bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            )
                        
                        # Accept a connection from a client
                        client_sock, client_info = server_sock.accept()
                        print("Accepted connection from", client_info)
                        
                        # Send the audio data in chunks of 1024 bytes
                        with open('message.mp3', 'rb') as f:
                            data = f.read(1024)
                            while data:
                                client_sock.send(data)
                                data = f.read(1024)
                        
                        # Close the client and server sockets
                        client_sock.close()
                        server_sock.close()
                        
                        os.remove('message.mp3')
                        break
        time.sleep(30)  # wait for 30 seconds
