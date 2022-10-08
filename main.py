import discord, os, json, random, time, enum, requests, shutil, re
from discord import ChannelType, app_commands, ui
from PIL import Image
from io import BytesIO


import commands.basic

basic.__init__()

class aclient(discord.Client):

  def __init__(self):
    super().__init__(intents=discord.Intents.all())
    self.synced = False

  async def on_ready(self):
    print(f"We have logged in as {self.user}.")
    await client.change_presence(activity=discord.Game(name="racoon.drooler.tk"))


client = aclient()
tree = app_commands.CommandTree(client)


class location(enum.Enum):
  wallet = 1
  bank = 2


@client.event
async def on_message(message):
  if message.content == "!sync":
    if message.author.id == 644851108623417344:
      await client.wait_until_ready()
      if not client.synced:
        await tree.sync()
        client.synced = True
        print("Commands synced")
      else:
        print("Commands already synced")
    else:
      message.reply.send("Syncing is only permitted for owner of bot")


@client.event
async def on_guild_join(guild):
  if f"data/{guild.id}.json" == False:
    src_dir = os.getcwd()
    dest_dir = src_dir + "/data"
    src_file = os.path.join(src_dir, 'template.json')
    shutil.copy(src_file, dest_dir)
    dst_file = os.path.join(dest_dir, 'template.json')
    new_dst_file_name = os.path.join(dest_dir, f'{guild.id}.json')
    os.rename(dst_file, new_dst_file_name)
    os.chdir(dest_dir)
    with open(f'{guild.id}.json') as json_file:
      data = json.load(json_file)
      for member in guild.members:
        data["wallet"][str(member.id)] = 0
        data["bank"][str(member.id)] = 0
        with open(f"{guild.id}.json", "w") as f:
          json.dump(data, f, indent=4)

    json_file.close()



@client.event
async def on_member_join(user):
  dataJ = open(f"data/{user.guild.id}.json", "r")
  dataJf = json.load(dataJ)
  if dataJf["wallet"][str(user.id)] == False:
    with open(f"data/{user.guild.id}.json") as json_file:
      data = json.load(json_file)
      data["wallet"][str(user.id)] = 0
      data["bank"][str(user.id)] = 0
      with open(f"data/{user.guild.id}.json", "w") as f:
        json.dump(data, f, indent=4)


  dataJ.close()

@tree.command(name='help', description='U need help? Use this command')
async def slash(interaction: discord.Interaction):
  if(False):
    await interaction.response.send_message("This command is currently **unavailable**.", ephemeral=False)
  else:
    
    embedVar = discord.Embed(title="Help center", color=0x546e7a)
    embedVar.add_field(
    name="Commands",
    value=
    "\n**/ping** - Ping the bot\n**/avatar** - Display someones avatar\n**/gay** - Be gay or make someone else gay\n**/balance** - Check balance from any given user\n**/shop** - Buy some stuff\n**/work** - Work and get some cash\n**/deposit** - Put your money in your bank account\n**/withdraw** - Withdraw some money from the bank to buy things\n**/add-money** - Add money to any given user (admin)\n**/reset-money** - Reset money from any given user (admin)",
    inline=False)
    embedVar.add_field(
    name="Links",
    value=
    "\n**Homepage** - https://racoon.drooler.tk \n**Commands** - https://racoon.drooler.tk/commands \n**Creators** - https://racoon.drooler.tk/creators ",
    inline=False)
    await interaction.response.send_message(embed=embedVar, ephemeral=False)


@tree.command(name='ping', description='Ping the bot')
async def slash(interaction: discord.Interaction):
  if(False):
    await interaction.response.send_message("This command is currently **unavailable**.", ephemeral=False)
  else:
    await interaction.response.send_message("Pong!", ephemeral=False)


@tree.command(name='balance', description='Check balance from info given user')
async def slash(interaction: discord.Interaction, member: discord.Member = None): 
  if interaction.channel.type == ChannelType.private:
    await interaction.response.send_message("This command can not be used in **DM's.**", ephemeral=False)
  else:
    if(False):
      await interaction.response.send_message("This command is currently **unavailable**.", ephemeral=False)
    else:
      if member is None:
        member = interaction.user

      dataJ = open(f"data/{interaction.guild.id}.json", "r")
      dataJf = json.load(dataJ)

      embedVar = discord.Embed(title="",
                           description=f"Balance of {member}",
                           color=0x546e7a)
      embedVar.set_author(name=member,
                      url=member.display_avatar,
                      icon_url=member.display_avatar)
      embedVar.add_field(name="Wallet",
                     value=dataJf["wallet"][str(member.id)],
                     inline=False)
      embedVar.add_field(name="Bank",
                     value=dataJf["bank"][str(member.id)],
                     inline=False)
      embedVar.add_field(name="Total",
                     value=dataJf["bank"][str(member.id)] +
                     dataJf["wallet"][str(member.id)],
                     inline=False)
      await interaction.response.send_message(embed=embedVar, ephemeral=False)
      dataJ.close()


@tree.command(name='add-money', description='Add money to any user')
async def slash(interaction: discord.Interaction, amount: int, member: discord.Member, location: location): 
  if interaction.channel.type == ChannelType.private:
    await interaction.response.send_message("This command can not be used in **DM's.**", ephemeral=False)
  else:
    if(False):
      await interaction.response.send_message("This command is currently **unavailable**.", ephemeral=False)
    else:
      if interaction.user.guild_permissions.administrator == False:
        await interaction.response.send_message(
      "You're not an admin! Skill issue.", ephemeral=False)
      else:
        if location.lower() == "wallet":

          with open(f"data/{interaction.guild.id}.json") as json_file:
            data = json.load(json_file)
            data["wallet"][str(
              member.id)] = data["wallet"][str(member.id)] + amount
            with open(f"data/{interaction.guild.id}.json", "w") as f:
              json.dump(data, f, indent=4)

          json_file.close()

          await interaction.response.send_message(
          f"Added {amount} to {member}'s wallet.", ephemeral=False)

        elif location.lower() == "bank":

          with open(f"data/{interaction.guild.id}.json") as json_file:
            data = json.load(json_file)
            data["bank"][str(member.id)] = data["bank"][str(member.id)] + amount
            with open(f"data/{interaction.guild.id}.json", "w") as f:
              json.dump(data, f, indent=4)

          json_file.close()

          await interaction.response.send_message(
          f"Added {amount} to {member}'s bank.", ephemeral=False)

        else:
          await interaction.response.send_message(
        "That location doesnt exist! The options are `Wallet` and `Bank`.",
        ephemeral=False)


@tree.command(name='reset-money', description='Reset money from any give user')
async def slash(interaction: discord.Interaction, member: discord.Member): 
  if interaction.channel.type == ChannelType.private:
    await interaction.response.send_message("This command can not be used in **DM's.**", ephemeral=False)
  else:
    if(False):
      await interaction.response.send_message("This command is currently **unavailable**.", ephemeral=False)
    else:
      if interaction.user.guild_permissions.administrator == False:
        await interaction.response.send_message(
      "You're not an admin! Skill issue.", ephemeral=False)
      else:

        with open(f"data/{interaction.guild.id}.json") as json_file:
          data = json.load(json_file)
          data["wallet"][str(member.id)] = 0
          with open(f"data/{interaction.guild.id}.json", "w") as f:
            json.dump(data, f, indent=4)

        json_file.close()

        with open(f"data/{interaction.guild.id}.json") as json_file:
          data = json.load(json_file)
          data["bank"][str(member.id)] = 0
          with open(f"data/{interaction.guild.id}.json", "w") as f:
            json.dump(data, f, indent=4)

        json_file.close()

        await interaction.response.send_message(f"**{member}'s** money got reset.", ephemeral=False)


@tree.command(name='work', description='Work for some extra cash')
@app_commands.checks.cooldown(1, 1200.0, key=lambda i: (i.guild_id, i.user.id))
async def slash(interaction: discord.Interaction): 
  if interaction.channel.type == ChannelType.private:
    await interaction.response.send_message("This command can not be used in **DM's.**", ephemeral=False)
  else:
    if(False):
      await interaction.response.send_message("This command is currently **unavailable**.", ephemeral=False)
    else:
      workC = random.randint(600, 1200)
      with open(f"data/{interaction.guild.id}.json") as json_file:
        data = json.load(json_file)
        data["wallet"][str(
        interaction.user.id)] = data["wallet"][str(interaction.user.id)] + workC
        with open(f"data/{interaction.guild.id}.json", "w") as f:
          json.dump(data, f, indent=4)

      await interaction.response.send_message(
        f"You worked and got payed **{workC}** money.", ephemeral=False)

@tree.error
async def on_test_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        num = re.findall(r'\d+', str(error))
        await interaction.response.send_message(f"You need to wait **{str(int(int(num[0]) / 60))} minutes** before you can work again.", ephemeral=False)

@tree.command(name='deposit',
              description='Put some cash in the bank, be safe!')
async def slash(interaction: discord.Interaction, amount: int = None): 
  if interaction.channel.type == ChannelType.private:
    await interaction.response.send_message("This command can not be used in **DM's.**", ephemeral=False)
  else:
    if(False):
      await interaction.response.send_message("This command is currently **unavailable**.", ephemeral=False)
    else:

      dataJ = open(f"data/{interaction.guild.id}.json", "r")
      dataJf = json.load(dataJ)

      if amount is None:
        amount = dataJf["wallet"][str(interaction.user.id)]

      if amount <= dataJf["wallet"][str(interaction.user.id)]:
        with open(f"data/{interaction.guild.id}.json") as json_file:
          data = json.load(json_file)
          data["bank"][str(
            interaction.user.id)] = data["bank"][str(interaction.user.id)] + amount
          with open(f"data/{interaction.guild.id}.json", "w") as f:
            json.dump(data, f, indent=4)

          f.close()
        with open(f"data/{interaction.guild.id}.json") as json_file:
          data = json.load(json_file)
          data["wallet"][str(interaction.user.id)] = data["wallet"][str(
            interaction.user.id)] - amount
          with open(f"data/{interaction.guild.id}.json", "w") as f:
            json.dump(data, f, indent=4)
          f.close()
          await interaction.response.send_message(
        f"Deposited **{amount}** money in your bank.", ephemeral=False)
      else:
        await interaction.response.send_message(
      f"You dont have that much money, too broke.", ephemeral=False)



@tree.command(name='withdraw',
              description='Withdraw some cash from the bank, to buy things!')
async def slash(interaction: discord.Interaction, amount: int = None): 
  if interaction.channel.type == ChannelType.private:
    await interaction.response.send_message("This command can not be used in **DM's.**", ephemeral=False)
  else:
    if(False):
      await interaction.response.send_message("This command is currently **unavailable**.", ephemeral=False)
    else:

      dataJ = open(f"data/{interaction.guild.id}.json", "r")
      dataJf = json.load(dataJ)

      if amount is None:
        amount = dataJf["bank"][str(interaction.user.id)]

      if amount <= dataJf["bank"][str(interaction.user.id)]:
        with open(f"data/{interaction.guild.id}.json") as json_file:
          data = json.load(json_file)
          data["bank"][str(
            interaction.user.id)] = data["bank"][str(interaction.user.id)] - amount
          with open(f"data/{interaction.guild.id}.json", "w") as f:
            json.dump(data, f, indent=4)
            f.close()
        with open(f"data/{interaction.guild.id}.json") as json_file:
          data = json.load(json_file)
          data["wallet"][str(interaction.user.id)] = data["wallet"][str(
            interaction.user.id)] + amount
          with open(f"data/{interaction.guild.id}.json", "w") as f:
            json.dump(data, f, indent=4)

            f.close()
            await interaction.response.send_message(
          f"Withdrew **{amount}** money from your bank.", ephemeral=False)
      else:
        await interaction.response.send_message(
      f"You dont have that much money, too broke.", ephemeral=False)


@tree.command(name='shop', description='Buy things, pretty epic.')
async def slash(interaction: discord.Interaction): 
  if interaction.channel.type == ChannelType.private:
    await interaction.response.send_message("This command can not be used in **DM's.**", ephemeral=False)
  else:
    if(False):
      await interaction.response.send_message("This command is currently **unavailable**.", ephemeral=False)
    else:
      await interaction.response.send_message("The shop is currently **empty**.", ephemeral=False)


@tree.command(name='gay', description='Be gay or make someone else gay!')
async def slash(interaction: discord.Interaction,
                 member: discord.Member = None):
  if(False):
    await interaction.response.send_message("This command is currently **unavailable**.", ephemeral=False)
  else:
    if member is None:
      member = interaction.user
    if interaction.channel.type == ChannelType.private:
      if member != interaction.user:
        await interaction.response.send_message("You can not get someone else's avatar in **DM's.**", ephemeral=False)
      else:
        response = requests.get("https://racoon.drooler.tk/database/files/images/gay.png")
        gayer = Image.open(BytesIO(response.content))
        response = requests.get(member.display_avatar)
        imager = Image.open(BytesIO(response.content)).convert('RGB')
        sizer = imager.size
        gayer.thumbnail(sizer, Image.Resampling.LANCZOS)
        imager.paste(gayer, (0, 0), mask=gayer)
        imager.save("images/gay.png")

        await interaction.response.send_message(file=discord.File('images/gay.png'), ephemeral=False)

        time.sleep(0.2)

        os.remove('images/gay.png')
    else:
      response = requests.get("https://racoon.drooler.tk/database/files/images/gay.png")
      gayer = Image.open(BytesIO(response.content))
      response = requests.get(member.display_avatar)
      imager = Image.open(BytesIO(response.content)).convert('RGB')
      sizer = imager.size
      gayer.thumbnail(sizer, Image.Resampling.LANCZOS)
      imager.paste(gayer, (0, 0), mask=gayer)
      imager.save("images/gay.png")

      await interaction.response.send_message(file=discord.File('images/gay.png'), ephemeral=False)

      time.sleep(0.2)

      os.remove('images/gay.png')


client.run("MTAyMzYwMzIwMjE3MzcwMjIxNQ.GJlaNy.x7MzTzfQ2NszaLX3kSHFVkM-ZQU1qA-7_RlwLY")