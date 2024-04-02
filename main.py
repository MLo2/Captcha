from flask import Flask, request, render_template_string
from captcha.image import ImageCaptcha
import random
import string
import base64
import io

app = Flask(__name__)

def generate_captcha():
    image = ImageCaptcha(width=280, height=90)
    letters = string.ascii_letters + string.digits
    captcha_text = ''.join(random.choice(letters) for i in range(6))
    data = io.BytesIO()
    image.write(captcha_text, data)
    data.seek(0)
    return captcha_text, data

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        user_captcha_response = request.form.get('captcha')
        correct_captcha = request.form.get('correct_captcha')
        if user_captcha_response == correct_captcha:
            message = 'كبتشاء صحيح!'
        else:
            message = 'كبتشاء خاطئ، حاول مرة أخرى.'

    captcha_text, data = generate_captcha()
    encoded_data = base64.b64encode(data.getvalue()).decode()
    html = f'''
    <h2>captcha</h2>
    <p>الرجاء إدخال النص الموجود في الصورة أدناه للمتابعة:</p>
    <img src="data:image/png;base64,{encoded_data}" /><br/>
    <form action="/" method="post">
        <input type="hidden" name="correct_captcha" value="{captcha_text}">
        <input type="text" name="captcha" placeholder="حط كود تحقق هنا">
        <button type="submit">Enter</button>
    </form>
    <p style="color:{'green' if message.startswith('كبتشاء صحيح') else 'red'};">{message}</p>
    '''
    return html

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=30000)