# Sub argument parser
# Sub arguments are data included in the 3rd field of a message object.
# It extends upon the message parser but introduces ways for controlling of the processor 
# to disable argument pushing on ':' characters
# 
# Example 1 (BAD) :
# std::vector<int>:bob
# Arguments: std,:vector<int>,bob
# Example 2 (GOOD) :
# [std::vector<int>]:bob
# Arguments: std::vector<int>,bob

# Run the subarguments parser on 'buffer' and return the parsed list of parameters
def subargs_parse(buffer: str):
    parameters = [] # List of final parameters
    prev = "" # Current parameter we are assembling
    chunk_counter = 0 # Number of characters in the parameter object
    ignore_sep = False # Ignore ':' characters

    x = 0 

    for c in buffer:
        if c == ':' and not ignore_sep and len(prev) != 0:
            chunk_counter = 0

            parameters.append(prev)
            prev = ""

            x += 1
            continue

        if c == '[' and chunk_counter == 0 and not ignore_sep:
            ignore_sep = True
        elif c == ']' and x + 1 < len(buffer) and buffer[x + 1] == ':' and ignore_sep:
            ignore_sep = False
        elif c == ']' and x + 1 >= len(buffer) and ignore_sep:
            ignore_sep = False
        else:
            prev += c

        x += 1
        chunk_counter += 1
    
    if len(prev) > 0:
        parameters.append(prev)

    return parameters
