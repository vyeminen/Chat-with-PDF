css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 30%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 500px;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://cdn.dribbble.com/userupload/10914741/file/original-7c497af15d65536103d0b53e85e08593.png?resize=752x" style="max-height: 70px; max-width: 60px; border-radius: 50%; ">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://e7.pngegg.com/pngimages/799/987/png-clipart-computer-icons-avatar-icon-design-avatar-heroes-computer-wallpaper.png " style="max-height: 70px; max-width: 60px; border-radius: 50%; ">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''