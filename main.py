import discord
from discord.ext import commands
from datetime import timedelta
from config import TOKEN
import datetime

# colorama.init()

# <:hypesquad_balance:>

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

bot.remove_command('help')

# events

@bot.event
async def on_guild_join():
    guilds = await bot.fetch_guilds(limit = None).flatten()
    await bot.change_presence(status = discord.Status.online, activity= discord.Activity(name=f'за {len(guilds)} серверами.', type= discord.ActivityType.watching))


@bot.event
async def on_guild_remove():
    guilds = await bot.fetch_guilds(limit = None).flatten()
    await bot.change_presence(status = discord.Status.online, activity= discord.Activity(name=f'за {len(guilds)} серверами.', type= discord.ActivityType.watching))


@bot.event
async def on_ready():
    print('\033[32mБот запущен\033[0m')

    guilds = await bot.fetch_guilds(limit = None).flatten()
    await bot.change_presence(status = discord.Status.online, activity= discord.Activity(name=f'за {len(guilds)} серверами.', type= discord.ActivityType.watching))

    # 157 169 180
    result = {
        'roles': [],
        'users': []
    }

    for i in bot.guilds[0].roles:
        perms = {
            'view_channels': i.permissions.view_channel,
            'manage_channels': i.permissions.manage_channels,
            'manage_roles': i.permissions.manage_roles,
            'manage_emojis_and_stickers': i.permissions.manage_emojis_and_stickers,
            'view_audit_log': i.permissions.view_audit_log,
            'manage_webhooks': i.permissions.manage_webhooks,
            'manage_server': i.permissions.manage_guild,
            'create_invites': i.permissions.create_instant_invite,
            'change_nickname': i.permissions.change_nickname,
            'manage_nicknames': i.permissions.manage_nicknames,
            'kick_members': i.permissions.kick_members,
            'ban_members': i.permissions.ban_members,
            'moderate_members': i.permissions.moderate_members,
            'send_messages': i.permissions.send_messages,
            'send_message_in_threads': i.permissions.send_messages_in_threads,
            'create_public_threads': i.permissions.create_public_threads,
            'create_private_threads': i.permissions.create_private_threads,
            'embed_links': i.permissions.embed_links,
            'attach_files': i.permissions.attach_files,
            'add_reactions': i.permissions.add_reactions,
            'use_external_emojis': i.permissions.use_external_emojis,
            'use_external_stickers': i.permissions.use_external_stickers,
            'mentione_everyone': i.permissions.mention_everyone,
            'manage_messages': i.permissions.manage_messages,
            'manage_threads': i.permissions.manage_threads,
            'read_message_history': i.permissions.read_message_history,
            'send_tts_messages': i.permissions.send_tts_messages,
            'use_application_commands': i.permissions.use_application_commands,
            'connect_voice': i.permissions.connect,
            'speak': i.permissions.speak,
            'video': i.permissions.stream,
            'use_activities': i.permissions.start_embedded_activities,
            'use_voice_activation': i.permissions.use_voice_activation,
            'priority_speaker': i.permissions.priority_speaker,
            'mute_members': i.permissions.mute_members,
            'deafen_members': i.permissions.deafen_members,
            'move_members': i.permissions.move_members,
            'request_to_speak': i.permissions.request_to_speak,
            'manage_events': i.permissions.manage_events,
            'administrator': i.permissions.administrator
        }

        members = []

        for j in i.members:
            members.append(
                {
                    'nickname': str(j),
                    'id': j.id,
                    'is_bot': j.bot,
                    'status': str(j.status),
                    'created_at': j.created_at.timestamp(),
                    'joined_at': j.joined_at.timestamp(),
                    # 'public_flags': j.public_flags.all(),
                    # 'avatar_url': str(j.avatar.url)
                }
            )

        result['roles'].append(
            {
                'name': i.name,
                'id': i.id,
                'color': str(i.color),
                'created_at': i.created_at.timestamp(),
                'members': members,
                'permissions': perms
            }
        )
    
    # with open('data.json', 'w') as f:
    #     f.write(json.dumps(result))



# main

def get_user_info(user):
    embed = discord.Embed(title='Информация о пользователе', color=0x3498db)

    is_bot = 'Да' if user.bot else 'Нет'

    if str(user.status) == 'online':
        status = 'Онлайн'
    elif str(user.status) == 'idle':
        status = 'Неактивен'
    elif str(user.status) == 'dnd':
        status = 'Не беспокоить'
    else:
        status = 'Оффлайн'

    badges = []

    for i in user.public_flags.all():
        if discord.UserFlags.hypesquad_balance == i:
            badges.append('<:hypesquad_balance:1014078146565390356>')
        elif discord.UserFlags.hypesquad_bravery == i:
            badges.append('<:hypesquad_bravery:1014078147915952188>')
        elif discord.UserFlags.hypesquad_brilliance == i:
            badges.append('<:hypesquad_brilliance:1014078149467832390>')

    embed.set_thumbnail(url=user.avatar.url)

    embed.add_field(name='Тег', value=f'`{user}`', inline=True)
    embed.add_field(name='ID пользователя', value=f'`{user.id}`')
    embed.add_field(name='Бот', value=f'`{is_bot}`')
    embed.add_field(name='Статус', value=f'`{status}`')
    embed.add_field(name='Дата создания аккаунта',
                    value=f'<t:{int(user.created_at.timestamp())}:f>')
    embed.add_field(name='Дата присоединения к серверу',
                    value=f'<t:{int(user.joined_at.timestamp())}:f>')
    embed.add_field(name='Значки', value='   '.join(badges))

    return embed


@bot.slash_command(description="Получить информацию о выбранном пользователе")
async def userinfo(
    ctx,
    user: discord.Option(
        discord.Member,
        "Выберите пользователя, о котором хотите получить информацию") = None):
    if user == None:
        user = ctx.author

    result = get_user_info(user)

    await ctx.respond(embed=result, ephemeral=True)


# @bot.command(description="Получить информацию о выбранной роли")
@bot.slash_command(description="Получить информацию о выбранной роли")
async def roleinfo(ctx, role: discord.Role):
    embed = discord.Embed(title='Информация о роле',
                          # color=discord.Color.from_str(str(role.color))
                          )

    permissions = f'''{":white_check_mark:" if role.permissions.view_channel else "<:red_negative_cross_mark:1013892309986840586>"}  Просматривать каналы

{":white_check_mark:" if role.permissions.manage_channels else "<:red_negative_cross_mark:1013892309986840586>"}  Управлять каналами

{":white_check_mark:" if role.permissions.manage_roles else "<:red_negative_cross_mark:1013892309986840586>"}  Управлять ролями

{":white_check_mark:" if role.permissions.manage_emojis_and_stickers else "<:red_negative_cross_mark:1013892309986840586>"}  Управлять эмодзи и стикерами

{":white_check_mark:" if role.permissions.view_audit_log else "<:red_negative_cross_mark:1013892309986840586>"}  Просматривать журнал аудита

{":white_check_mark:" if role.permissions.manage_webhooks else "<:red_negative_cross_mark:1013892309986840586>"}  Управлять вебхуками

{":white_check_mark:" if role.permissions.manage_guild else "<:red_negative_cross_mark:1013892309986840586>"}  Управлять сервером

{":white_check_mark:" if role.permissions.ban_members else "<:red_negative_cross_mark:1013892309986840586>"}  Банить участников

{":white_check_mark:" if role.permissions.kick_members else "<:red_negative_cross_mark:1013892309986840586>"}  Выгонять участников

{":white_check_mark:" if role.permissions.moderate_members else "<:red_negative_cross_mark:1013892309986840586>"}  Отправлять участников подумать о своем поведении

{":white_check_mark:" if role.permissions.manage_channels else "<:red_negative_cross_mark:1013892309986840586>"}  Управлять каналами

{":white_check_mark:" if role.permissions.manage_messages else "<:red_negative_cross_mark:1013892309986840586>"}  Управлять сообщениями

{":white_check_mark:" if role.permissions.administrator else "<:red_negative_cross_mark:1013892309986840586>"}  Администратор'''

    mentionable = 'Да' if role.mentionable else 'Нет'

    # members = "\n".join([str(i) for i in role.members])

    embed.add_field(name='Название', value=f'`{role}`', inline=True)
    embed.add_field(name='Можно всем упоминать', value=f'`{mentionable}`')
    embed.add_field(name='Цвет', value=f'`{role.color}`')
    # embed.add_field(
    #     name='Участники',
    #     value=f'`{members}`'
    # )
    embed.add_field(name='Дата создания',
                    value=f'<t:{int(role.created_at.timestamp())}:f>')
    embed.add_field(name='Количество участников', value=f'`{len(role.members)}`')
    embed.add_field(name='Разрешения', value=f'{permissions}')
    embed.add_field(name='ID роли', value=f'`{role.id}`')

    await ctx.respond(embed=embed, ephemeral=True)


@bot.slash_command(description="Удаляет определенное количество сообщений")
async def clear(ctx, count):
    await ctx.channel.purge(limit=int(count))


@bot.slash_command()
async def timeout(ctx, member: discord.Member, minutes):
    await member.timeout_for(timedelta(minutes=int(minutes)))

    embed = discord.Embed(
        title='Тайм-аут',
        description=
        f':white_check_mark:  Участник {member.mention} отправлен подумать о своем поведении'
    )

    await ctx.respond(embed=embed)


@bot.event
async def on_message(message):
    if '@everyone' in message.content or '@here' in message.content:
        await message.channel.purge(limit=1)
    # else:
    #     print(f'{message.author.name} > {message.content}')


@bot.user_command(name="Информация о пользователе")
async def _userinfo(ctx, member: discord.Member):
    result = get_user_info(member)

    await ctx.respond(embed=result, ephemeral=True)


@bot.message_command(name="Информация о сообщении",
                     description="Получить информацию о выбранном сообщении")
async def messageinfo(ctx, message: discord.Message):
    embed = discord.Embed(title="Информация о сообщении", color=0x00ff00)

    embed.set_thumbnail(url=message.author.avatar.url)

    embed.add_field(name="Контент",
                    value=f'`{message.content.replace("`", "")}`')
    embed.add_field(name="ID сообщения", value=f'`{message.id}`')
    embed.add_field(name="Автор", value=message.author.mention)
    embed.add_field(name="Дата отправки",
                    value=f'<t:{int(message.created_at.timestamp())}:f>')

    await ctx.respond(embed=embed, ephemeral=True)


@bot.slash_command()
async def ban(ctx,
              user: discord.Option(
                  discord.Member,
                  "Выберите пользователя, которого хотите забанить"),
              reason="Причина не указана"):

    await user.ban(reason=reason)
    embed = discord.Embed(
        title='Бан',
        description=
        f':white_check_mark:  Успешно забанен пользователь {user.mention}',
        color=0x00ff00)

    await ctx.respond(embed=embed)


@bot.slash_command()
async def kick(ctx,
               user: discord.Option(
                   discord.Member,
                   "Выберите пользователя, которого хотите кикнуть"),
               reason="Причина не указана"):

    await user.kick(reason=reason)

    embed = discord.Embed(
        title='Кик',
        description=
        f':white_check_mark:  Успешно кикнут пользователь {user.mention}',
        color=0x00ff00)

    await ctx.respond(embed=embed)


@bot.slash_command()
async def owner_find(ctx):
    guild_owner = bot.get_user(int(ctx.guild.owner.id))
    await ctx.send(f'The owner of this server is: {guild_owner}')


@bot.slash_command()
async def serverinfo(ctx):
    member = len(ctx.guild.members)
    Roles = len(ctx.guild.roles)

    guild_owner = bot.get_user(int(ctx.guild.owner.id))

    embed = discord.Embed(color=0x3498db)

    embed.add_field(name='Владелец сервера', value=guild_owner.mention)
    embed.add_field(name='ID сервера', value=ctx.guild.id)
    embed.add_field(name='Дата создания', value=f'<t:{int(ctx.guild.created_at.timestamp())}:f>')
    embed.add_field(name='Количество участников', value=f'`{member}`')
    embed.add_field(name='Количество ролей', value=f'`{Roles}`')
    embed.set_thumbnail(url=ctx.guild.icon.url)
    embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.respond(embed=embed)



@bot.slash_command(name='join',aliases = ['summon']) # CREATING COMMAND "JOIN" WITH ALIAS SUMMON
async def _join(ctx, *, channel: discord.VoiceChannel = None): # TAKING ARGUMENT CHANNEL SO PPL CAN MAKE THE BOT JOIN A VOICE CHANNEL THAT THEY ARE NOT IN
    """Joins a voice channel."""

    destination = channel if channel else ctx.author.voice.channel # CHOOSING THE DESTINATION, MIGHT BE THE REQUESTED ONE, BUT IF NOT THEN WE PICK AUTHORS VOICE CHANNEL

    if ctx.voice_client: # CHECKING IF THE BOT IS PLAYING SOMETHING
        await ctx.voice_state.voice.move_to(destination) # IF THE BOT IS PLAYING WE JUST MOVE THE BOT TO THE DESTINATION
        return

    await destination.connect() # CONNECTING TO DESTINATION
    await ctx.respond(f"Succesfully joined the voice channel: {destination.name} ({destination.id}).")


bot.run(TOKEN)