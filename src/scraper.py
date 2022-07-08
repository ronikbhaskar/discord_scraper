
import discord
import sys
import getopt
import csv

intents = discord.Intents.default()
intents.members = True

scraper = discord.Client(intents=intents)
server_name = None
channel_name = None
num_queries = None
out_file = None
member_file = None
role_file = None
channel_file = None

@scraper.event
async def on_ready():

    for server in scraper.guilds:
        if server.name == server_name:
            break
    else:
        print("didn't find server")
        return

    if role_file is not None:
        with open(role_file, "w", encoding="UTF8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID","role_name"])
            for role in server.roles:
                writer.writerow([role.id, role.name])

    if member_file is not None:
        with open(member_file, "w", encoding="UTF8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID","username","display_name"])
            for member in server.members:
                writer.writerow([member.id, member.name, member.display_name])

    if channel_file is not None:
        with open(channel_file, "w", encoding="UTF8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID","name"])
            for channel in server.channels:
                writer.writerow([channel.id, channel.name])

    for channel in server.channels:
        if channel.name == channel_name:
            break
    else:
        print("didn't find channel")
        return

    messages = await channel.history(limit=num_queries).flatten()

    with open(out_file, "a", encoding="UTF8") as f:
        for message in messages[::-1]:
            f.write(f"{message.author}: {message.content}\n")

    print("Finished scraping. You can end this process.")

def usage():
    """
    prints simple usage information
    """

    print("\ndiscord scraper")
    print("args:")
    print("-s {name of server} : required, name of server")
    print("\talias --server\n")
    print("-f {path to out file} : required, text file to save results")
    print("\talias --file\n")
    print("-c {name of channel} : required, name of channel")
    print("\talias --channel\n")
    print("-m {member data csv file} : optional, file to save mappings of ID, display name, and username")
    print("\talias --member-csv\n")
    print("-r {role data csv file} : optional, file to save mappings of ID, role name")
    print("\talias --role-csv\n")
    print("-l {channel data csv file} : optional, file to save mappings of ID, channel name")
    print("\talias --channel-csv\n")
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
    global out_file
    global member_file
    global role_file
    global channel_file
    
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "f:s:c:n:m:r:l:h", 
                  ["file=", "server=","channel=", "num=", "member-csv=", "role-csv=", "channel-csv=", "help"])
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
        elif opt in ("-f", "--file"):
            out_file = arg
        elif opt in ("-m", "--member-csv"):
            member_file = arg
        elif opt in ("-r", "--role-csv"):
            role_file = arg
        elif opt in ("-l", "--channel-csv"):
            channel_file = arg
        elif opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        else:
            input(f"Unhandled option {arg}. Press ENTER to continue anyways")

    if server_name == None \
        or channel_name == None \
        or num_queries == None \
        or out_file == None:
        usage()
        sys.exit(0)

def main():
    set_variables()
    print("Use this tool at your own risk.")
    token = input("token: ")
    scraper.run(token, bot=False)

if __name__ == "__main__":
    main()