from typing import Tuple

ai_icon_map = {
    "openai":"""<img class="_white" width="32" height="32" src="https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/light/openai.png"/>""",
    "ollama":"""<img class="_white" width="32" height="32" src="https://registry.npmmirror.com/@lobehub/icons-static-svg/latest/files/icons/Ollama.svg"/>""",
}

def message_container_template(message: Tuple[str, str]) -> str:
    role, content = message
    if role == "human":
        container_class = "user-container"
        message_class = "user-message"
        icon_class = "user-icon"
    else:
        container_class = "assistant-container"
        message_class = "assistant-message"
        icon_class = "assistant-icon"

    # SVG icons as inline content
    ai_svg = ai_icon_map["openai"]
    user_svg = """<img class="_white" width="32" height="32" src="https://img.icons8.com/fluency-systems-filled/50/gender-neutral-user.png" alt="gender-neutral-user"/>"""
    icon_content = user_svg if role == "human" else ai_svg
    
    return f"""<div class="chat-container {container_class}"><div class="{icon_class}">{icon_content}</div><div class="{message_class}">{content}</div></div>"""