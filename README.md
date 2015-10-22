# Liveview-Stack
[RR] This repository implements components for using in LiveView feature.

Starting point for Liveview-Stack is liveviewstack.py

## processes /

#### eater.py
This process consume image frames on the robot and save it locally to a shared memory region. 

###### Related configurations

**eater.ip** : ip address of the robot  
Ex. eater.ip=192.168.2.232  

**eater.port** : port of the feeder process running on the robot  
Ex. eater.port=1234  

**eater.partial_file** : full path to a file for keeping partial image data  
Ex. eater.partial_file=tmp/full.partial.jpg  

**eater.complete_file**  : full path to a file for keeping completed image data  
Ex. eater.complete_file=tmp/full.jpg  

#### digester.py
This process resize image frames to a more suitable size for streaming.

###### Related configurations

**digester.source_file** : full path to original file from eater process  
Ex. digester.source_file=tmp/full.jpg  

**digester.stream_partial** : full path to a file for keeping partial resized image data.  
Ex. digester.stream_partial_file=tmp/stream.partial.jpg  

**digester.stream_complete_file** : full path to a file for keeping completed resized image data.
digester.stream_complete_file=tmp/stream.jpg

#### streamer.py
This process listen for requests from phone for image frames.  

**streamer.port** : port for streamer server to listen on  
Ex. streamer.port=5000  

**streamer.source_file** : full path to an image file for streaming  
Ex. streamer.source_file=tmp/stream.jpg  

#### recorder.py
This process listen for requests from phone for image frames.  

**recorder.port** : port for recorder server to listen on  
Ex. recorder.port=5001  

**recorder.source_file** : full path to an image file for recoding as video  
Ex. recorder.source_file=tmp/full.jpg  

#### feeder.py
This process listen for requests from phone for image frames.  

**feeder.port** : port for recorder server to listen on  
Ex. feeder.port=1234  

**feeder.source_file** : full path to an image file for sending over to server
Ex. feeder.source_file=/dev/shm/mjpeg/cam.jpg

## 3rd_bin/

Contains binary for raspimjpeg build with latest userland library.  

## /

#### config.conf

Contains configurations for each of the processes.

#### config_loader.py

Contains method for loading configuration file and parse as a dictionary.

#### exceptions.py

Contains exceptions classes used in BananaPacketBuilder and BananaPacketReader classes.

#### test.py

Contains tests. We believe that software without test is just a junk.

#### packet.py

Implements packet for sending and receiving record command via socket.

###### Packet Format

```
| _  _  | _        | _ _ | _ _ _    |
| TYPES | COMMANDS | RES | NOT USED |
```
###### TYPES
```
0 1 : REQ_TYPE  
1 0 : ACK_TYPE  
```

###### COMMANDS
```
1 : COMMAND_ON  
0 : COMMAND_OFF  
```

###### RES
```
0 0 : RES_480  
0 1 : RES_720  
1 0 : RES_1080  
```

## Setting up environment

```
pip3 install -r requirements.txt
```
