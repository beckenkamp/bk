from flask import Flask, render_template, request
from flask_sse import sse

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/chat')
def chat():
    message = request.args.get('message').lower()
    channel = request.args.get('channel')

    print(channel)
    print(message)

    if 'link' in message:
        title = 'O que aprendi publicando um chatbot'
        image_url = ''
        description = 'A importância do feedback dos usuários'
        href = 'https://blog.mbeck.com.br/o-que-aprendi-publicando-um-chatbot-19f9ecc145e2'
        sse.publish({'title': title,
                     'image_url': image_url,
                     'description': description,
                     'href': href}, type='link', channel=channel)
    elif 'história' in message:
        sse.publish({"message": get_about()}, type='chat', channel=channel)
    elif 'tecnologia' in message:
        sse.publish({"message": get_techs()}, type='chat', channel=channel)
    else:
        sse.publish({"message": message}, type='chat', channel=channel)

    return "Message sent!"

def get_about():
    return """O cara começou a desenvolver
              profissinalmente em 2003 com PHP básico e alguns bancos de dados.
              Depois ele foi se virando com frontend e acabou virando
              fullstack na parada. Em 2014 resolveu que queria mesmo era
              trabalhar com Python e correu atrás... Hoje trabalha de fullstack
              web developer e anda fazendo um monte de chatbot para aprender!"""

def get_techs():
    return """Algumas das tecnologias que o Marcus trabalha são as seguintes:
              - Python
              - Django
              - Postgres
              - MongoDB
              - Flask
              - HTML/CSS
              - Javascript
              - AngularJS... e outras coisas por aí.
              """
