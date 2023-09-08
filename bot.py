# -*- coding: utf-8 -*-

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot
import os
import youtube_download
import asyncio
import qrCode_Generator
import pelandoWebScrapping
import time
import open_ai
import io, base64  # Add these imports to the top of the file


# Defina o token do bot
BOT_TOKEN = os.environ['BOT_TOKEN']

# Define a função principal para executar o bot do Discord
def run_discord_bot():
    # Configura as intenções do bot
    intents = discord.Intents.default()
    intents.message_content = True

    # Configura as intenções do bot
    client = discord.Client(intents=intents, activity=discord.Activity(type=discord.ActivityType.listening, name="música"), command_prefix='$')
    client = commands.Bot(command_prefix='$', intents=intents)
    client.command_prefix = '$'

    # Dicionário para manter as filas de música por servidor
    music_queues = {}

    # Dicionário para manter as filas de música por servidor
    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="música"))
        print("Calyx is ready.")

    # Dicionário para manter as filas de música por servidor
    @client.event
    async def on_message(message):
            if message.author == client.user:
                return
            
            print(message.content)
            
            if message.content.startswith('$'):
                await client.process_commands(message)
                return     

    # Comando para exibir a lista de comandos disponíveis
    @client.command()
    async def ajuda(ctx):
        embed = discord.Embed(
            title="Comandos Disponíveis:",
            description=(
                "1. $youtube <URL> - Gera um link de download para um vídeo do YouTube.\n"
                "2. $join - Conecta o bot a um canal de voz.\n"
                "3. $leave - Desconecta o bot de um canal de voz.\n"
                "4. $play <URL> - Toca música a partir de uma URL do YouTube.\n"
                "5. $skip - Pula a música atual.\n"
                "6. $pause - Pausa a reprodução de música.\n"
                "7. $qr <conteúdo> - Gera um código QR com o conteúdo especificado.\n"
                "8. $pelando <r/q> - Obtém promoções do Pelando (r para recentes, q para mais quentes).\n"
                "9. $gpt <texto> - Gera uma resposta usando GPT-3 com base no texto fornecido.\n"
                "10. $img <texto> - Gera uma imagem com base no texto fornecido."
            ),
            color=0x00ff00,
        )
        await ctx.send(embed=embed)

    # Comando para gerar um link de download de vídeo do YouTube
    @client.command()
    async def youtube(ctx, url):
        try:
            await ctx.send(f'{ctx.author.mention} Aguarde um momento... Link sendo gerado...')
            link = youtube_download.download_link(url)
            if type(link) == str:
                await ctx.send(f'{ctx.author.mention}, {link}')
                return
            embed = discord.Embed(title=f'{link[1]}', description=f'Link de download: {link[0]}\n\n {ctx.author.mention}', color=0x00ff00)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'{ctx.author.mention}, {e}')        

    # Comando para conectar o bot a um canal de voz
    @client.command()
    async def join(ctx):
        if ctx.author.voice:
            if ctx.guild.voice_client:
                if ctx.guild.voice_client.channel == ctx.author.voice.channel:
                    await ctx.send(f'{ctx.author.mention}, eu já estou conectado ao seu canal de voz.')
                    return
                else:
                    await ctx.guild.voice_client.disconnect()
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send(f'{ctx.author.mention}, você não está conectado a nenhum canal de voz.')

    # Comando para desconectar o bot de um canal de voz
    @client.command()
    async def leave(ctx):
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.channel == ctx.author.voice.channel:
                await ctx.guild.voice_client.disconnect()
                if ctx.guild.id in music_queues:
                    del music_queues[ctx.guild.id]
                await ctx.send(f'{ctx.author.mention}, eu me desconectei do seu canal de voz.')
                return
        await ctx.send(f'{ctx.author.mention}, eu não estou conectado ao seu canal de voz.')

    # Comando para tocar música a partir de uma URL do YouTube
    @client.command()
    async def play(ctx, url):
        try:
            if ctx.author.voice:
                if ctx.guild.voice_client:
                    if ctx.guild.voice_client.channel != ctx.author.voice.channel:
                        await ctx.guild.voice_client.disconnect()
                        if ctx.guild.id in music_queues:
                            del music_queues[ctx.guild.id]
                        await ctx.author.voice.channel.connect()
                else:
                    await ctx.author.voice.channel.connect()
            else:
                await ctx.send(f'{ctx.author.mention}, você não está conectado a nenhum canal de voz.')
                return

            await ctx.send(f'{ctx.author.mention} Aguarde um momento...')
            link = youtube_download.download_audio(url)

            if type(link) == str:
                await ctx.send(f'{ctx.author.mention}, {link}')
                return
            
            # Verifique se o servidor possui uma fila de música e crie uma se não existir.
            if ctx.guild.id not in music_queues:
                music_queues[ctx.guild.id] = []

            music_queues[ctx.guild.id].append(link)  # Adicione a música à fila.

            if ctx.guild.voice_client is None or not ctx.guild.voice_client.is_playing():
                await play_next(ctx)

        except Exception as e:
            await ctx.send(f'{ctx.author.mention}, {e}')

    # Função para tocar a próxima música da fila
    async def play_next(ctx):
        if ctx.guild.id in music_queues and len(music_queues[ctx.guild.id]) > 0:
            for i in range(0,len(music_queues[ctx.guild.id])):

                if i == 0 or ctx.guild.voice_client.is_playing():
                    await ctx.send(f'Tocando: {music_queues[ctx.guild.id][i][1]}')
                else:
                    await ctx.send(f'Musica adicionada na fila: {music_queues[ctx.guild.id][i][1]}')
                description = "Lista de músicas:\n"
                for i in range(0,len(music_queues[ctx.guild.id])):
                    if i == 0:
                        description += f'**{i+1} - {music_queues[ctx.guild.id][i][1]}**\n'
                    else:
                        description += f'{i+1} - {music_queues[ctx.guild.id][i][1]}\n'
                embed = discord.Embed(title=f'Lista de músicas', description=description, color=0x00ff00)
                await ctx.send(embed=embed)

            link = music_queues[ctx.guild.id].pop(0)  # Pegue a próxima música da fila.
            titulo = link[1]
            music_link = link[0]
            
            if ctx.guild.voice_client is None or not ctx.guild.voice_client.is_playing():
                ctx.voice_client.play(discord.FFmpegPCMAudio(music_link), after=lambda e: asyncio.run(play_next(ctx)))
        else:
            await ctx.send("Fila de música vazia.")

    # Função para tocar a próxima música da fila
    @client.command()
    async def skip(ctx):
        if ctx.guild.voice_client and ctx.guild.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Música pulada.")

    # Função para tocar a próxima música da fila
    @client.event
    async def on_voice_state_update(member, before, after):
        if before.channel is not None and after.channel is None:
            # Verifique se o bot estava em um canal de voz antes e ninguém está mais lá.
            if member.guild.voice_client is not None and not any(
                m.bot for m in member.guild.voice_client.channel.members
            ):
                await member.guild.voice_client.disconnect()
                del music_queues[member.guild.id]

    # Função para tocar a próxima música da fila
    @client.command()
    async def pause(ctx):
        if ctx.guild.voice_client:
            if ctx.guild.voice_client.is_playing():
                ctx.guild.voice_client.pause()
                await ctx.send(f'{ctx.author.mention}, a música foi pausada.')
            else:
                await ctx.send(f'{ctx.author.mention}, não há nenhuma música tocando.')
        else:
            await ctx.send(f'{ctx.author.mention}, eu não estou conectado ao seu canal de voz.')

    # Função para tocar a próxima música da fila
    @client.command()
    async def qr(ctx, content):
        try:
            timestamp = str(time.time())
            await qrCode_Generator.qr_generator(content, timestamp, ctx)
        except Exception as e:
            await ctx.send(f'{ctx.author.mention}, {e}')

    # Comando para obter promoções do Pelando (recentes ou mais quentes)
    @client.command()
    async def pelando(ctx, model_pelando):
        try:
            if model_pelando != 'r' and model_pelando != 'q':
                await ctx.send(f'{ctx.author.mention}, tipo inválido, use "$pelando r" para recentes e "$pelando q" para mais quentes, ou "$pelando" para mais quentes.')
                return
            
            await ctx.send(f'{ctx.author.mention} Aguarde um momento... Link sendo gerado...')
            retorno_pelando = await pelandoWebScrapping.get_promocao(model_pelando)
            embed = discord.Embed(title= 'Promoções Pelando' , description= f'{ctx.author.mention}\n\n{retorno_pelando}', color=0x00ff00)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'{ctx.author.mention}, {e}')

    # Comando para obter promoções do Pelando (recentes ou mais quentes)
    @client.command()
    async def gpt(ctx):
        try:
            content = ctx.message.content[5:]
            if content == '':
                await ctx.send(f'{ctx.author.mention}, por favor, digite algo.')
                return
            
            #colocar que o bot está digitando
            await ctx.typing()
            #chamar a função que gera o texto
            retorno_gpt = open_ai.get_response(content)
            #enviar o texto
            await ctx.send(f'{ctx.author.mention}\n\n{retorno_gpt}')
        except Exception as e:
            await ctx.send(f'{ctx.author.mention}, {e}')
            
    # Comando para obter promoções do Pelando (recentes ou mais quentes)
    @client.command()
    async def img(ctx):
        try:
            content = ctx.message.content[5:]
            if content == '':
                await ctx.send(f'{ctx.author.mention}, por favor, digite algo.')
                return
            
            await ctx.send(f'{ctx.author.mention} Aguarde um momento... imagem sendo gerada...')
            retorno_img = open_ai.genereate_image(content)
            file = discord.File(io.BytesIO(base64.b64decode(retorno_img)), filename='image.png')
            await ctx.send(file=file)
        except Exception as e:
            await ctx.send(f'{ctx.author.mention}, {e}')

    # Execute o bot com o token especificado
    client.run(BOT_TOKEN)
    
