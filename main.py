import discord
from discord.ext import commands
import os
import requests
import sympy
from dotenv import load_dotenv
import json
import google.generativeai as genai

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!",
                   description="Bot multifuncional para programadores", intents=intents)

genai.configure(api_key="chave da sua api")
model = genai.GenerativeModel("gemini-1.5-flash")
API_KEY = "chave da sua api"
GENAI_MODEL = 'gemini-1.5-flash'

# --------------------------------------------------------------------------------------------------
# Conexão do bot


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Bot conectado com sucesso como: {bot.user}')

# --------------------------------------------------------------------------------------------------
# Função para enviar mensagens grandes em partes


async def enviar_em_partes(ctx, texto, limite=2000):
    while texto:
        parte = texto[:limite]
        await ctx.send(parte)
        texto = texto[limite:]

# --------------------------------------------------------------------------------------------------
# Slash Command - Ping


@bot.tree.command(name="ping", description="Verifica a latência do bot")
async def ping(interact: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interact.response.send_message(f'Pong! Latência {latency}ms')


# --------------------------------------------------------------------------------------------------
# Comando do bot para perguntas
@bot.command()
async def perguntar(ctx, *, mensagem):
    await ctx.send("Processando sua mensagem, aguarde...")
    try:
        response = chat.send_message(mensagem)
        await enviar_em_partes(ctx, f"Resposta: {response.text}")
    except Exception as e:
        await ctx.send(f"Erro ao processar a mensagem: {e}")


# --------------------------------------------------------------------------------------------------
# Slash Command - Sobre


@bot.tree.command(name="sobre", description="Mostra informações sobre o bot")
async def sobre(interact: discord.Interaction):
    embed = discord.Embed(
        title='Olá! Me chamo Orion!',
        description=('Sou um bot projetado para programadores e entusiastas de tecnologia. Possuo funcionalidades que vão desde desafios de programação até na assistência na depuração de códigos. Sou o bot perfeito para comunidades que desejam explorar e aprimorar habilidades de programação, promovendo conhecimento e resolução de problemas de forma interativa e prátiva.'),
        color=discord.Color.purple()
    )
    embed.add_field(name='Comandos disponíveis',
                    value="`/ping`, `/sobre`, `!challenge`, `!codehelper`, `!explicar`, `!debug`", inline=False)
    embed.set_footer(text='Criado por Orion')
    await interact.response.send_message(embed=embed)

# --------------------------------------------------------------------------------------------------
# Comando Prefixado - Challenge


@bot.command(name="challenge")
async def challenge(ctx, linguagem: str, nivel: str):
    linguagem = linguagem.capitalize()
    nivel = nivel.lower()
    niveis_validos = ["fácil", "médio", "difícil"]

    if nivel not in niveis_validos:
        await ctx.send(f"Nível inválido. Escolha entre: {', '.join(niveis_validos)}")
        return

    await ctx.send(f"Gerando um desafio de programação em {linguagem} com nível {nivel}, aguarde...")
    try:
        prompt = f"Crie um desafio de programação em {
            linguagem} com nível de dificuldade {nivel}."
        response = chat.send_message(prompt)
        await enviar_em_partes(ctx, f"Desafio ({linguagem} - {nivel}): {response.text.strip()}")
    except Exception as e:
        await ctx.send(f"Erro ao gerar o desafio: {e}")

# --------------------------------------------------------------------------------------------------
# Comando Prefixado - Code Helper


@bot.command(name="codehelper")
async def codehelper(ctx, *, mensagem: str):
    await ctx.send("Processando sua solicitação de ajuda com código, aguarde...")
    try:
        prompt = f"Explique o seguinte problema de código e sugira melhorias: {
            mensagem}"
        response = chat.send_message(prompt)
        await enviar_em_partes(ctx, f"Resposta: {response.text.strip()}")
    except Exception as e:
        await ctx.send(f"Erro ao processar a solicitação: {e}")

# --------------------------------------------------------------------------------------------------
# Comando Prefixado - Explicar Código


@bot.command(name="explicar")
async def explicar(ctx, *, codigo: str):
    await ctx.send("Analisando e explicando o código, aguarde...")
    try:
        prompt = f"Explique o seguinte código detalhadamente: {codigo}"
        response = chat.send_message(prompt)
        await enviar_em_partes(ctx, f"Explicação: {response.text.strip()}")
    except Exception as e:
        await ctx.send(f"Erro ao processar a explicação: {e}")

# --------------------------------------------------------------------------------------------------
# Comando Prefixado - Debug Wizard


@bot.command(name="debug")
async def debug(ctx, *, codigo: str):
    await ctx.send("Analisando e depurando o código, aguarde...")
    try:
        prompt = f"Identifique e corrija os erros no seguinte código: {codigo}"
        response = chat.send_message(prompt)
        await enviar_em_partes(ctx, f"Debugging: {response.text.strip()}")
    except Exception as e:
        await ctx.send(f"Erro ao processar o debug: {e}")

# --------------------------------------------------------------------------------------------------
# Chat


def iniciar_chat():
    model = genai.GenerativeModel(GENAI_MODEL)
    return model.start_chat(
        history=[
            {"role": "user", "parts": "Hello"},
            {"role": "model", "parts": "Great to meet you. What would you like to know?"},
        ]
    )


chat = iniciar_chat()

bot.run(TOKEN)
