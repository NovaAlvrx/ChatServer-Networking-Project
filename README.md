##  📌 Requirement 1 — Object-Based Protocol Design
# Overview

Our chat system uses an object-based communication protocol over TCP.
Although users type IRC-style commands (such as /nick or /join), the client translates those commands into JSON objects, sends them to the server, and receives JSON objects in return.

This ensures all communication is structured, machine-parseable, and fully compatible with the system’s requirements.

# Message Format & Encoding
All messages exchanged between client and server follow these rules:

 - **Transport**: TCP socket
 - **Encoding**: UTF-8
 - **Framing**: One complete JSON object per line, ending with **\n**
 - **Parsing**: Receiver reads a line, then applies **json.loads**

Example message on the wire:
{"type":"command","action":"join","channel":"#general"}
