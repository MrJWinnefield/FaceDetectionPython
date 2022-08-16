#!/usr/bin/env python

from __future__ import division
from smtplib import SMTPSenderRefused
import cv2
import numpy as np
import socket
import struct
import time

MAX_DGRAM = 2**16

def dump_buffer(s):
    """ Emptying buffer frame """
    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        print(seg[0])
        if struct.unpack("B", seg[0:1])[0] == 1:
            print("finish emptying buffer")
            break

def resend_timestamp(s, timestamp, sender_addr):
    sender_port = 12345
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sender_socket.bind((sender_addr, sender_port))
    print(timestamp)
    print(struct.pack("q", timestamp))
    print(type(struct.pack("q", timestamp)))
    sender_socket.sendto(struct.pack("q", timestamp))

def main():
    """ Getting image udp frame &
    concate before decode and output image """
    
    # Set up socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('192.168.1.102', 12345))    #127.0.0.1
    dat = b''
    dump_buffer(s)

    while True:
        seg, sender_addr = s.recvfrom(MAX_DGRAM)
        #print(addr)
        #print(struct.unpack("B", seg[0:1]))
        if struct.unpack("B", seg[0:1])[0] > 1:
            #print(struct.unpack("B", seg[0:1]))
            #print(seg[1:50])
            #print(struct.unpack("q", seg[1:9]))
            dat += seg[1:]
        else:
            #print(struct.unpack("B", seg[0:1]))
            #print(struct.unpack("q", seg[1:9]))
            timestamp = struct.unpack("q", seg[1:9])[0]
            
            resend_timestamp(s, timestamp, sender_addr)

            #ping = int(time.time()*1000) - timestamp
            dat += seg[9:]
            img = cv2.imdecode(np.frombuffer(dat, dtype=np.uint8), 1)
            #cv2.putText(img, str(ping)+"ms", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('receiver', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            dat = b''

    # cap.release()
    cv2.destroyAllWindows()
    s.close()

if __name__ == "__main__":
    main()
