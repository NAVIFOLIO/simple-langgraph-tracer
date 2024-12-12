from typing import Dict, List

# def tags_template(options: List[str], selected: List[str]) -> str:
def tags_template(tag_visibility_options: Dict[str, bool]) -> str:
    widget_html = f"""<div class="tag_area"><div class="tag_container">"""
    
    for name, visible in tag_visibility_options.items():
        widget_html += (f"""<div class="tag tag_selected">{name}</div>"""
                        if visible else f"""<div class="tag tag_not_selected">{name}</div>""")
    
    widget_html += """</div></div>"""
    return widget_html