from DBFunctions import DBFunctions
import configparser
import logging

from telegram.ext import (
    Updater, 
    CommandHandler,
    MessageHandler,
    Filters
)

# Configuração
config = configparser.ConfigParser()
config.read_file(open('telegramBot/config.ini'))

# Conexão com a API do Telegram
updater = Updater(
    token = config['DEFAULT']['token'],
    use_context = True
)
dispatcher = updater.dispatcher

# Log padrão
logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

dados = DBFunctions()


def start(update, context):
    
    chatId = update.effective_chat.id
    
    # print('effective_chat: ', update.effective_chat)
    # print('effective_message: ', update.effective_message)
    # print('effective_user: ', update.effective_user)
    # print('chatId: ', chatId)

    saudacao = ''
    nome = ''

    if update.effective_chat.type == 'group':
        saudacao = 'grupo '
        nome = update.effective_chat.title
    else:
        nome = update.effective_chat.first_name

    texto = "Oi, " + saudacao + nome + "! Eu sou o EnergyBot.\n"
    texto += "\nFui criado como parte do projeto de TCC do Eduardo Ciscoto.\n"
    texto += "Meu objetivo é reunir dados sobre o fornecimento de energia elétrica, "
    texto += "gerados a partir de diferentes pontos da cidade, analisá-los e apresentar "
    texto += "informações sobre a qualidade do fornecimento as pessoas que quiserem interagir comigo.\n"
    texto += "\nEm breve disponibilizarei estas informações em forma de comandos para serem acessadas.\n"
    texto += "\nPor enquanto, estou em fase de desenvolvimento e testes...\n"
    texto += "\nEnvie /menu para conhecer as informações disponíveis até o momento."
    
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = texto
    )


# Função "Tensão média do dia de hoje"
def tensaoMediaHoje(update, context):
    
    mediaHoje = dados.todaysAvg()

    texto = "Tensão média de hoje (até o momento)\n"
    texto += "\nQuantidade de leituras: " + str(mediaHoje[0][1]) + "\n"
    texto += "Tensão média: " + str(round(mediaHoje[0][0])) + "V *\n"
    texto += "\n* Lembro que este valor está arredondado e pode não refletir "
    texto += "a realidade devido a imprecisão dos equipamentos de medição."
    
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = texto
    )


# Função "Última leitura realizada"
def agora(update, context):

    leitura = dados.now()
    
    texto = "Última leitura realizada:\n"
    texto += "\nData: {}".format(leitura[0])
    texto += "\nHora: {}".format(leitura[1])
    texto += "\nTensão na rede: {}\n".format(leitura[2])
    texto += "\n* Lembro que este valor está arredondado e pode não refletir "
    texto += "a realidade devido a imprecisão dos equipamentos de medição."
    
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = texto
    )


# Função "Última leitura realizada"
def menu(update, context):

    texto = 'Menu de informações\n'
    texto += '\n"/comando": "informação"'
    texto += '\n/start: boas-vindas;'
    texto += '\n/agora: última leitura realizada;'
    texto += '\n/tensaoMediaHoje: média calculada a partir das leituras de hoje até o momento;'
    texto += '\n/menu: informações disponíveis;'
    
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = texto
    )


# Função "Eco" (envia o que recebe)
def echo(update, context):
    
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = update.message.text
    )


# Trata comandos desconhecidos enviados pelo usuário
def unknown(update, context):
    chatId = update.effective_chat.id
    
    texto = "Desculpe. Não reconheci o comando enviado."
    
    context.bot.send_message(
        chat_id = chatId,
        text = texto
    )


# Handlers
start_handler = CommandHandler('start', start)
tensaoMediaHoje_handler = CommandHandler('tensaoMediaHoje', tensaoMediaHoje)
agora_handler = CommandHandler('agora', agora)
menu_handler = CommandHandler('menu', menu)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
help_handler = CommandHandler('help', start)
unknown_handler = MessageHandler(Filters.command, unknown)

# Passando os Handlers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(tensaoMediaHoje_handler)
dispatcher.add_handler(agora_handler)
dispatcher.add_handler(menu_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(unknown_handler)

# to run this program:
# updater.start_polling()
# to stop it:
# updater.stop()