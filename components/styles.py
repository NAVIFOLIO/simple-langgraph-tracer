chat_container_style = """
<style>

.user-icon img, .assistant-icon img{
    filter: brightness(0) invert(1);
}

.chat-container {
    padding: 10px;
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin: 5px 0;
}
.user-message {
    background-color: #121212;
    color: #ffffff;
    padding: 15px;
    border-radius: 8px;
    margin: 0;
    max-width: 80%;
    order: 1;
    align-self: center;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 6px -1px, rgba(0, 0, 0, 0.06) 0px 2px 4px -1px;
}
.assistant-message {
    background-image: linear-gradient(to top, #f77062 0%, #fe5196 100%);
    color: #ffffff;
    padding: 15px;
    border-radius: 8px;
    margin: 0;
    max-width: 80%;
    order: 2;
    align-self: center;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 6px -1px, rgba(0, 0, 0, 0.06) 0px 2px 4px -1px;
}
.user-icon {
    width: 45px;
    height: 45px;
    border-radius: 8px;
    background-color: #3C3C3C;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    order: 2;
    flex-shrink: 0;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 6px -1px, rgba(0, 0, 0, 0.06) 0px 2px 4px -1px;
}
.assistant-icon {
    width: 45px;
    height: 45px;
    border-radius: 8px;
    background-color: #FA607C;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    order: 1;
    flex-shrink: 0;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 4px 6px -1px, rgba(0, 0, 0, 0.06) 0px 2px 4px -1px;
}

.user-container {
    justify-content: flex-end;
    align-items: center;
    padding-left: 20%;
}
.assistant-container {
    justify-content: flex-start;
    align-items: center;
    padding-right: 20%;
}
.message-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow-y: auto;
}
</style>
"""

tag_style="""
<style>
.tag{
    padding: 1px 4px;
    border-radius: 4px;
    font-size: 0.8rem;
    display: inline-flex;
    align-items: center;
    transition: all 0.2s ease;
    border: 1px solid rgba(99, 102, 241, 0.2);
    cursor: default;
    user-select: none;
    white-space: nowrap;
}
.tag_selected{
    background: #7f00ff;
    color: #ffffff;
}
.tag_not_selected{
    background: #A9A9A9;
    color: #787878;
}
</style>
"""

tags_area_style="""
<style>
.tag_area{
    color: #a8b2d1;
    padding: 2px 10px;
    border-radius: 50px;
    font-size: 0.85em;
    display: inline-flex;
    align-items: center;
    transition: all 0.2s ease;
    cursor: default;
    user-select: none;
    white-space: nowrap;
    margin-bottom: 10px
}

.tag_container{
    display: flex;
    flex-wrap: wrap;
    gap: 3px;
    align-items: center;
}
</style>
"""