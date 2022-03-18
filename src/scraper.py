
import discord
import sys
import getopt

scraper = discord.Client()
server_name = None
channel_name = None
num_queries = None

@scraper.event
async def on_ready():

    for server in scraper.guilds:
        if server.name == server_name:
            break
    else:
        print("didn't find server")
        return

    for channel in server.channels:
        if channel.name == channel_name:
            break
    else:
        print("didn't find channel")
        return

    messages = await channel.history(limit=num_queries).flatten()
    for message in messages:
        print(f"{message.author}: {message.content}")

def usage():
    """
    prints simple usage information
    """

    print("\ndiscord scraper")
    print("args:")
    print("-s {name of server} : required, name of server")
    print("\talias --server\n")
    print("-c {name of channel} : required, name of channel")
    print("\talias --file\n")
    print("-n {number of messages} : required, max 1000")
    print("\talias --num\n")
    print("-h : prints usage information")
    print("\talias --help\n")

def str_to_int_in_range(opt, arg, min, max):
    """
    converts string to int, min <= x < max
    exits if fail (for use in arg parsing)
    """

    msg = f"{opt} takes an integer between {min} and {max - 1}"

    try:
        arg = int(arg)
    except ValueError as err:
        print(msg)
        sys.exit(1)

    if arg < min or arg >= max:
        print(msg)
        sys.exit(1)

    return arg

def set_variables():
    global server_name
    global channel_name
    global num_queries
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:c:n:h", ["server=","channel=", "num=", "help="])
    except getopt.GetoptError as err:
        # print usage information and exit:
        print(err) # option arg not recognized
        usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-n", "--num"):
            num_queries = str_to_int_in_range(opt, arg, 1, 1001)
        elif opt in ("-s", "--server"):
            server_name = arg
        elif opt in ("-c", "--channel"):
            channel_name = arg
        elif opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            input(f"Unhandled option {arg}. Press ENTER to continue anyways")

    if server_name == None \
        or channel_name == None \
        or num_queries == None:
        usage()
        sys.exit(0)

def main():
    set_variables()
    token = input("token: ")
    scraper.run(token, bot=False)

if __name__ == "__main__":
    main()