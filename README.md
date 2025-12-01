# Group Chat Service Project
CSC 4350 Team Project

## Team Members
- **Luna Da Silva** - Panther ID: 002623889
- **Noah Alvarez** - Panther ID: 002635100

## Demo Video
Youtube Link: https://youtu.be/aGbGRNbinOE

## File & Folder Manifest
This project is composed of a server module and a client module that communicate using a JSON-based object protocol over TCP.

| Path | Description |
|------|-------------|
| **README.md** | Project documentation (this file) |
| **/server/** | Server module containing all server-side code |
| ├── `chat_server.py` | Main server executable (start server here) |
| ├── `client_handler.py` | Per-client thread logic and command handling |
| ├── `server_core.py` | Shared server state: nicks, channels, connections |
| ├── `protocol.py` | JSON encode/decode utilities (server-side) |
| ├── `utils.py` | Logging + colored text output (extra credit) |
| └── `server.log` | Auto-generated server activity log (extra credit) |
| **/client/** | Client module containing all client-side code |
| ├── `chat_client.py` | Requirement 3 client implementation (REPL, commands, JSON) |
| ├── `receiver_thread.py` | Background thread that receives server events asynchronously |
| └── `protocol.py` | JSON command builder (client-side) |

### How To Run
### **1. Start the Server**
- Open a terminal and type:
   cd server
   python3 chat_server.py
- Expected Outcome from Server:
<span style="color:green;">[SERVER] Listening on 5002...</span>
- This server supports:
-  Multiple clients via threading
-  Channel creation/join/leave
-  Nickname assignement
-  Broadcasting messages
**-  Graceful shutdown using Ctrl-C**
**- Logging connections, messages, and server events**
**- Thread limit and overload handling**

### **2. Start the Client(s)**
- Open a second terminal and type:
   cd client
   python3 chat_client.py
- Use the following commands inside client terminal:
     /connect localhost 5002
     /nick <name>
     /join <channel>
     /leave [channel]
     /list
     /quit
     /help

### **3. Start a second client (for multi-user testing)**
- Open a third terminal and type:
   cd client
   python3 chat_client.py
   /connect localhost 5002
   /nick YourName
   /join #general
   Hi!

 Both clients will now receive each other's messages.

 ## How we tested
 ### Connection Tests
 - We verified that multiple clients can connect to the server at the same time
 - <img width="315" height="32" alt="Screenshot 2025-11-30 at 18 27 42" src="https://github.com/user-attachments/assets/f1e5d769-d858-4557-ac44-144d45939274" />

 - Verified that more than 5 people joining would give max out error
 <img width="651" height="116" alt="Screenshot 2025-11-30 at 18 05 51" src="https://github.com/user-attachments/assets/35338c78-ad68-43eb-b859-4def3981460f" />
<img width="371" height="52" alt="Screenshot 2025-11-30 at 18 06 27" src="https://github.com/user-attachments/assets/78a5e9ef-9f91-4bdb-952a-fd15c632b99b" />

### Nickname Test
- After connecting to server, we typed in multiple tests to show the full functioning /nick command
<img width="259" height="99" alt="Screenshot 2025-11-30 at 18 31 19" src="https://github.com/user-attachments/assets/03dff0b1-3f20-4fbb-8378-7d964b5275e4" />

### Channel Tests
- Once nickname is set, user can join general chat by using /join function
<img width="248" height="46" alt="Screenshot 2025-11-30 at 18 34 35" src="https://github.com/user-attachments/assets/0d516f2f-16ad-4b6d-a05c-b221e5ef6c44" />

### Messaging Tests
- Another person can join the general chat and exchange messages amongst each other, showing log history for user in green text
<img width="655" height="166" alt="Screenshot 2025-11-30 at 18 40 39" src="https://github.com/user-attachments/assets/2651ce87-d3ca-4e25-acf7-d381557faaa2" />

### Graceful Disconnects
- Ctrl-C shuts down server for

### Logging Verification
- Server shows connection timestamps, channel joins, message logs, and server stops

## Observations & Reflections
- Designing a JSON-based object protocol requires careful planning for both commands and events.
- TCP streams require explicit message framing — in this project we used newline-delimited JSON.
- Concurrency with threads requires:
   - shared state (ServerCore)
   - locks (threading.Lock)
   - careful cleanup on disconnect
- Asynchronous receiving (ReceiverThread) improves client responsiveness significantly.

### Team Roles
- Luna
   - Integrated server JSON protocol with client commands
   - Implemented colored output for client (extra credit)
   - Added server logging + server.log (extra credit)
   - Added graceful Ctrl-C shutdown logic (extra credit)
   - Helped debug threading and connection issues
   - Wrote project documentation and demo notes
 
- Noah
   - Created ServerCore state manager
   - Implemented ClientHandler threading model
   - Built server-side protocol encoder/decoder
   - Designed channel structures, nicknames, and broadcasting logic
   - Ensured correctness of server concurrency behavior
   - Wrote AI disclosure document
