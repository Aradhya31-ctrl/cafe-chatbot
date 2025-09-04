import re

def detect_intent(q: str):
    s = q.lower().strip()
    if any(k in s for k in ["hour","time","open","close"]):
        return "hours"
    if any(k in s for k in ["price","cost","how much","₹","rs","rupee"]):
        return "price"
    if any(k in s for k in ["menu","items","list"]):
        return "menu"
    if any(k in s for k in ["suggest","recommend","what should i eat","meal"]):
        return "suggest"
    return "generic"

def rupee(n): 
    try:
        return f"₹{int(n)}"
    except:
        return f"₹{n}"
