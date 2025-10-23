# Handles debugger -> debug server communication and various utils around messaging

from utils import find_server
from protocol import DebuggerMessage,DebuggerMessageType
import threading as thread
import subprocess


class DebugServer:
    waits: dict[DebuggerMessageType, thread.Condition]
    wait_results: dict[DebuggerMessageType, list[DebuggerMessage]]

    MESSAGE_TRACE_MAX = 100

    # Messages analyzed by get_msg_range, which automatically clears this.
    # NOTE: If get_msg_range is not called enough it will be auto cleaned by the message IO thread
    message_trace: list[DebuggerMessage]

    def __init__(self):
        self.server_path = find_server()
        print("  * Starting comms server from: " + self.server_path)

        self.proc = subprocess.Popen([self.server_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.waits = dict()
        self.wait_results = dict()
        self.message_trace = list()

        if self.proc.poll() != None:
            print("Failed to start and communicate with v5dbg comms server!")
            print("Exit data: " + self.proc.stderr.readline().decode())
            exit(-1)

        self.io = thread.Thread(target=self.io_thread)
        self.io.start()

        print("Waiting for program execution on target to begin....")
        self.wait_for(DebuggerMessageType.OPEN)

        print("Target has begun execution of a v5dbg compatible program!")

    # Return True if we are connected to the remote debug server
    def connected(self):
        return self.proc.poll() == None

    # Stockpile messages until msg_type is found
    # NOTE: This function blocks until completion, use carefully
    def get_msg_range(self, front: DebuggerMessageType, end: DebuggerMessageType):
        self.wait_for(end)

        # Copy all messages from message history

        trace_reversed = self.message_trace
        trace_reversed.reverse()

        end_index = 0
        front_index = 0

        # Find end index
        x = 0

        for t in trace_reversed:
            if t.msg_type == end:
                end_index = x # Keep improving until we find the latest
            
            x += 1
        
        x = 0

        for t in trace_reversed:
            if t.msg_type == front:
                front_index = x # Keep improving until we find the latest

            x += 1

        splice = trace_reversed[end_index:front_index + 1]
        splice.reverse()

        self.message_trace.clear() # Auto clear our message trace so we don't get confused with old messages when we get called again

        return splice


    # Wait for the next message of the given type to arrive
    def wait_for(self, msg_type: DebuggerMessageType, count: int = -1):
        if msg_type in self.waits:
            raise Exception("Thread already waiting for that message!")

        self.waits[msg_type] = thread.Condition()

        with self.waits[msg_type]:
            self.waits[msg_type].wait()

        self.waits.pop(msg_type)

        if count == -1:
            return self.wait_results[msg_type]
        elif count != len(self.wait_results[msg_type]):
            print("re-run wait_for to meet count")
            return self.wait_for(msg_type, count)
        elif count == len(self.wait_results[msg_type]):
            return self.wait_results[msg_type]

    # IO thread for reading messages from the debug server (remote)
    def io_thread(self):
        while self.proc.poll() == None:
            b = self.proc.stdout.readline()

            # First 6 bytes are useless to us as they only contain stream information
            data = b[6:].decode()
            if len(data) == 0:
                continue

            if data[0] != '%':
                continue

            msg = DebuggerMessage(data)

            if len(self.message_trace) + 1 > self.MESSAGE_TRACE_MAX:
                self.message_trace.clear()
            
            self.message_trace.append(msg)

            if msg.msg_type in self.waits:
                if not msg.msg_type in self.wait_results:
                    self.wait_results[msg.msg_type] = list()

                self.wait_results[msg.msg_type].append(msg)

                with self.waits[msg.msg_type]:
                    self.waits[msg.msg_type].notify_all()
