import json

def pretty_print_messages(messages):
    output = ""
    for message in messages:
        if message["role"] != "assistant":
            continue
            
        output += f"**{message['sender']}**: "
        if message["content"]:
            output += message["content"]
            
        tool_calls = message.get("tool_calls") or []
        if len(tool_calls) > 1:
            output += "<br />"
        for tool_call in tool_calls:
            f = tool_call["function"]
            name, args = f["name"], f["arguments"]
            arg_str = json.dumps(json.loads(args)).replace(":", "=")
            output += f"{name}({arg_str[1:-1]})<br />"
            
    return output
