import discord
import os
import requests

# https://api.nekosapi.com/v3/docs#operation/nekosapi_api_index

# Setting up intents
intents = discord.Intents.default()
intents.message_content = True  # Needed for reading message content
intents.dm_messages = True      # Needed for reading direct messages
intents.emojis_and_stickers = True
intents.invites = True

# Initializing the bot client
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    """This event runs when the bot successfully logs in."""
    print(f"Started Bot as {bot.user.name}")

@bot.event
async def on_message(message: discord.Message):
    # Print out the message sender and content for debugging
    print(f"{message.author.name}: {message.content}")

    # Ignore the bot's own messages
    if message.author == bot.user:
        return

    # Check if the message content matches the trigger commands
    if message.content.lower().strip() in (",image", ",img",",image nsfw", ",img nsfw"):
        print("GETTING...")

        # Determine if NSFW is requested

        print('nsfw' in message.content.lower())

        if 'nsfw' in message.content.lower():
            print("NSFW Requested")
            res = requests.get("https://api.nekosapi.com/v3/images/random?type=nsfw")
        else:
            print("SFW Requested")
            res = requests.get("https://api.nekosapi.com/v3/images/random")

        try:
            # Check if the request was successful (status code 200)
            if res.status_code != 200:
                print(f"Error: Received unexpected status code {res.status_code}")
                await message.channel.send(f"Sorry, the API returned an error: {res.status_code}")
                return

            # Debugging: Print the raw response content and status code
            print(f"API Response Status Code: {res.status_code}")
            # print("Raw API Response:", res.text)

            # Check if the response body is empty
            if not res.text.strip():
                print("Empty response received from the API.")
                await message.channel.send("Sorry, the API returned an empty response.")
                return

            # Try to parse the JSON response
            data = res.json()  # Assuming the response is JSON

            # Extract the image URL from the first item in the "items" list
            image_url = None
            if 'items' in data and len(data['items']) > 0:
                image_url = data['items'][0].get('image_url', None)

            if image_url:
                print("SENDING...")
                # Create an embed with the image
                embed = discord.Embed(title="Here is your image:", color=discord.Color.blue())
                embed.set_image(url=image_url)  # Embed the image directly
                await message.channel.send(embed=embed)
                print("sent")
            else:
                print("No valid image URL found in the response.")
                await message.channel.send("Sorry, no image was found!")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching neko image: {e}")
            await message.channel.send("Sorry, something went wrong while fetching the image!")

# Get the bot token from the environment variable
bot_token = os.getenv("KEY")
if bot_token:
    bot.run(bot_token)
else:
    print("ERROR: Discord bot token not found!")
