#  📌 Requirement 1 — Object-Based Protocol Design
## Overview

Our chat system uses an object-based communication protocol over TCP.
Although users type IRC-style commands (such as /nick or /join), the client translates those commands into JSON objects, sends them to the server, and receives JSON objects in return.

This ensures all communication is structured, machine-parseable, and fully compatible with the system’s requirements.

## Message Format & Encoding
All messages exchanged between client and server follow these rules:

 - **Transport**: TCP socket
 - **Encoding**: UTF-8
 - **Framing**: One complete JSON object per line, ending with **\n**
 - **Parsing**: Receiver reads a line, then applies **json.loads**

Example message on the wire:
**{"type":"command","action":"join","channel":"#general"}
**

## Project Overview
This project implements a simple object-based chat system modeled after a subset of IRC commands. 
It contains both a ChatServer and ChatClient that communicate over TCP using newline-delimited JSON objects. 
The client accepts IRC-style commands (e.g., `/nick`, `/join`, `/list`) and translates them into structured JSON objects using the protocol defined above. 
The server processes these commands, manages channels, broadcasts messages, and sends event/error objects back to clients.
This project was developed collaboratively as part of a networking assignment.

## Directory Structure
ChatServer-Networking-Project/
├── README.md
├── protocol.py      # Shared message helpers (send/receive JSON objects)
├── server.py        # ChatServer implementation
├── client.py        # ChatClient implementation
└── main.py          # Wrapper entry point

## Running the Server
[Fill later]


## Requirements & Contribution Breakdown

**Requirement 1 – Object-Based Protocol Design:**  
Completed by name (this README section). Designed JSON schema, command-mapping, server events, and error format.

**Requirement 2 – ChatServer Implementation:**  
Completed by name. Handles commands, channels, broadcasts, user sessions, threading, and idle shutdown.

**Requirement 3 – ChatClient Implementation:**  
Completed by name. Handles IRC-style input, connects to server, sends objects, listens for events, and prints output.

**Requirement 4 – Documentation & Demonstration:**  
Completed by both team members.


## GenAI Usage Disclosure
Certain portions of this project were generated with the assistance of ChatGPT.  
All generated content was reviewed, edited, and expanded by the project team.  
Below are the prompts and corresponding responses:
 - [Fill later]
 - [Fill later]

