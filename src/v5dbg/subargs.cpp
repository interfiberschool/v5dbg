#include "v5dbg/subargs.h"

std::vector<std::string> V5Dbg_ParseSubargs(const std::string &in)
{
    // Translated from debugger/subargs.py

    std::vector<std::string> parameters;
    std::string prev;

    int chunkCounter = 0;
    bool ignoreSep = false;

    int x = 0;

    for (char c : in)
    {
        if (c == ':' && !ignoreSep && !prev.empty())
        {
            // Push next parameter

            chunkCounter = 0;

            parameters.push_back(prev);

            prev.clear();

            x += 1;
            continue;
        }
        
        if (c == '[' && chunkCounter == 0 && !ignoreSep)
        {
            ignoreSep = true;
        }
        else if (c == ']' && x + 1 < in.size() && in[x + 1] == ':' && ignoreSep)
        {
            ignoreSep = false;
        }
        else if (c == ']' && x + 1 >= in.size() && ignoreSep)
        {
            ignoreSep = false;
        }
        else
        {
            prev += c;
        }

        x += 1;
        chunkCounter += 1;
    }

    if (!prev.empty())
        parameters.push_back(prev);

    return parameters;
}