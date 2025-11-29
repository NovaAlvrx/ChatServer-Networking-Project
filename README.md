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
| File | Description |
|------|-------------|
| `README.md` | Project documentation and protocol design |
| `protocol.py` | Shared functions for sending/receiving JSON objects |
| `server.py` | ChatServer implementation |
| `client.py` | ChatClient implementation |
| `main.py` | Entry point wrapper for running server or client |


## Running the Server
[Fill later]


## Requirements & Contribution Breakdown

**Requirement 1 – Object-Based Protocol Design:**  
Completed by name (this README section). Designed JSON schema, command-mapping, server events, and error format.

**Requirement 2 – ChatServer Implementation:**  
Completed by name. Handles commands, channels, broadcasts, user sessions, threading, and idle shutdown.

**Requirement 3 – ChatClient Implementation:**  

The ChatClient is a simple, text-based client that communicates with the ChatServer using the object-based JSON protocol defined above.

### Design

- Implemented in `client.py` in the class `ChatClient`.
- The client takes no command line arguments. It is started with:
  ```bash
  python3 client.py
## Example Session
$ python3 client.py
=== ChatClient ===
Commands:
  /connect <host> [port]
  /nick <name>
  /join <channel>
  /leave [channel]
  /list
  /quit
  /help

> /connect localhost 5000
[ERROR] Could not connect: [Errno 61] Connection refused   # (no server running yet)

> /nick Luna
[WARN] Not connected. Use /connect <host> [port].

Once a ChatServer is running, multiple ChatClient instances can connect, join the same channel, and exchange messages using the protocol.

**Requirement 4 – Documentation & Demonstration:**  
Completed by both team members.

## GenAI Usage Disclosure
Certain portions of this project were generated with the assistance of ChatGPT.  
All generated content was reviewed, edited, and expanded by the project team.  
Below are the prompts and corresponding responses:
 - [Fill later]
 - [Fill later]

