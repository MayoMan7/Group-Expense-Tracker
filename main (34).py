# a code for a discord bot that can help you and your friends manage your group expenses

from numpy import e
import jointbank
import discord
from discord.ext import commands
import matplotlib.pyplot as plt
from io import BytesIO
import json

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot("!", intents=intents)


@bot.command()
async def deposit(ctx, message: float):
  jointbank.read(ctx.guild.name)
  jointbank.deposit(ctx.author.name, message, ctx.guild.name)

  embed = discord.Embed(
      title="Deposit",
      description=f"{ctx.author.name} deposited ${round(message,2)}",
      color=0x00ff00)

  await ctx.send(embed=embed)


@bot.command()
async def expense(ctx, description: str, cost: float, receipt_url: str):
  jointbank.readEX(ctx.guild.name)
  jointbank.expense(ctx.guild.name, description, cost, receipt_url)

  embed = discord.Embed(
      title="Expense",
      description=(ctx.author.name + " recorded an expense of $" +
                   str(round(cost, 2)) + " for " + description),
      color=0xff0000)
  await ctx.send(embed=embed)


@bot.command()
async def show_all_users(ctx):
  data = jointbank.show_all_users(ctx.guild.name)

  if not data:
    await ctx.send("No users found.")
    return

  embed = discord.Embed(
      title="All Users",
      color=0x00ff00)  # Customize the title and color as needed

  for line in data:
    embed.add_field(name="", value=line, inline=False)

  await ctx.send(embed=embed)


@bot.command()
async def show_user(ctx, member: commands.MemberConverter):
  data = jointbank.show_all_users(ctx.guild.name, str(member))

  if not data:
    await ctx.send("No users found.")
    return

  embed = discord.Embed(
      title="Users", color=0x00ff00)  # Customize the title and color as needed

  for line in data:
    embed.add_field(name="", value=line, inline=False)

  await ctx.send(embed=embed)


@bot.command()
async def show_all_expenses(ctx):
  data = jointbank.show_all_expenses(ctx.guild.name)
  embed = discord.Embed(
      title="All Expenses",
      color=0x00ff00)  # Customize the title and color as needed

  for line in data:
    embed.add_field(name="Expense", value=line, inline=False)

  await ctx.send(embed=embed)


@bot.command()
async def show_expense(ctx, message: str):
  data = jointbank.show_all_expenses(ctx.guild.name, message)
  embed = discord.Embed(
      title="Expense",
      color=0x00ff00)  # Customize the title and color as needed

  embed.add_field(name="Expense", value=data, inline=False)

  await ctx.send(embed=embed)


@bot.command()
async def files(ctx):
  # Create an embed for the download links
  embed = discord.Embed(
      title="Downloadable Files",
      color=0x00ff00)  # Customize the title and color as needed

  # Upload the files to the channel and obtain links
  file_expenses = await ctx.send(file=discord.File(ctx.guild.name +
                                                   "_expenses.json"))
  file_accounts = await ctx.send(file=discord.File(ctx.guild.name +
                                                   "_accounts.json"))

  # Add the download links as fields in the embed
  embed.add_field(name="Expenses JSON",
                  value=f"[Download]({file_expenses.attachments[0].url})",
                  inline=False)
  embed.add_field(name="Accounts JSON",
                  value=f"[Download]({file_accounts.attachments[0].url})",
                  inline=False)

  await file_expenses.delete()
  await file_accounts.delete()
  # Send the embed
  await ctx.send(embed=embed)



@bot.command()
async def cmdhelp(ctx):
  embed = discord.Embed(
      title="Bot Commands and Usage",
      color=0x00ff00)  # Customize the title and color as needed

  embed.add_field(
      name="deposit",
      value=
      "Lets you keep track of the money you have paid or added\nArgument: <amount>",
      inline=False)
  embed.add_field(
      name="expense",
      value=
      "Lets you record expenses\nArguments: <'desc', cost, 'url'> (use double quotes)",
      inline=False)
  embed.add_field(name="show_all_users",
                  value="Lists all the users in the joint bank\nNo arguments",
                  inline=False)
  embed.add_field(
      name="show_user",
      value="Lists all the users in the joint bank\nArgument: <mention a user>",
      inline=False)
  embed.add_field(
      name="show_all_expenses",
      value="Lists all the expenses in the joint bank\nNo arguments",
      inline=False)
  embed.add_field(
      name="show_expense",
      value="Lists all the expenses in the joint bank\n<transaction_#>",
      inline=False)
  embed.add_field(name="files",
                  value="Lists all the files in the joint bank\nNo arguments",
                  inline=False)
  embed.add_field(
      name="bar",
      value="Creates a bar chart of user contributions\nArgument: no argument",
      inline=False)

  embed.add_field(
      name="bar_exp",
      value="Creates a bar chart of monthly exenses\nArgument: no argument",
      inline=False)

  embed.add_field(
      name="cmdhelp",
      value="Lists all the commands in the joint bank\nNo arguments",
      inline=False)

  await ctx.send(embed=embed)


@bot.command()
async def bar(ctx):
  contributions = jointbank.read(ctx.guild.name)

  # Extract user names and their contribution amounts
  user_names = list(contributions.keys())
  contribution_amounts = [
      contributions[user]["total_deposit"] for user in user_names
  ]

  # Create a bar chart with user contributions
  plt.figure(figsize=(10, 6))
  ax = plt.gca()
  ax.bar(user_names,
         contribution_amounts,
         color='midnightblue',
         edgecolor='darkorange')
  ax.set_xlabel('Users')
  ax.set_ylabel('Contribution ($)')
  ax.set_title('User Contributions Bar Chart')
  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)
  ax.yaxis.set_ticks_position('left')
  ax.xaxis.set_ticks_position('bottom')
  ax.yaxis.grid(color='gray', linestyle='--', linewidth=0.5)

  # Rotate user names on the x-axis for better readability
  plt.xticks(rotation=45, ha='right')

  # Convert the bar chart to an image
  buffer = BytesIO()
  plt.savefig(buffer, format='png')
  buffer.seek(0)

  # Create a Discord File from the image
  chart_file = discord.File(buffer, filename='user_contributions.png')

  # Create and send an embed containing the bar chart
  embed = discord.Embed(title='User Contributions Bar Chart', color=0x00ff00)
  embed.set_image(url='attachment://user_contributions.png'
                  )  # Use the same filename as above

  await ctx.send(file=chart_file, embed=embed)


@bot.command()
async def bar_exp(ctx):
  # Initialize dictionaries to store monthly spending
  expenses_data = jointbank.readEX(ctx.guild.name)
  monthly_spending = {}

  for transaction_id, transaction in expenses_data.items():
    date = transaction["date"]
    month = date.split('-')[1]  # Extract the month part of the date

    # Get the amount and add it to the corresponding month
    amount = float(transaction["ammount"]) if isinstance(
        transaction["ammount"], (float, int)) else 0.0
    if month in monthly_spending:
      monthly_spending[month] += amount
    else:
      monthly_spending[month] = amount

  # Sort the monthly spending by month
  months = sorted(monthly_spending.keys())
  spending = [monthly_spending[month] for month in months]

  # Create a bar chart with dark mode aesthetic
  plt.figure(figsize=(10, 6))
  ax = plt.gca()
  ax.bar(months, spending, color='midnightblue', edgecolor='darkorange')
  ax.set_xlabel('Months')
  ax.set_ylabel('Spending ($)')
  ax.set_title('Monthly Spending Bar Chart (Dark Mode)')
  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)
  ax.yaxis.set_ticks_position('left')
  ax.xaxis.set_ticks_position('bottom')
  ax.yaxis.grid(color='gray', linestyle='--', linewidth=0.5)

  # Convert the bar chart to an image
  buffer = BytesIO()
  plt.savefig(buffer, format='png')
  buffer.seek(0)

  # Create a Discord File from the image
  chart_file = discord.File(buffer, filename='bar_chart.png')

  # Create and send an embed containing the bar chart
  embed = discord.Embed(title='Monthly Spending Bar Chart')
  embed.set_image(
      url='attachment://bar_chart.png')  # Use the same filename as above

  await ctx.send(file=chart_file, embed=embed)


TOKEN = HIDDEN

bot.run(TOKEN)
