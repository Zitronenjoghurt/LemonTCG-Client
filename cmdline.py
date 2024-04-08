import asyncio
from commands.setup_e2ee import setup_e2ee

COMMANDS = {
    "help": lambda: list_commands(),
    "setup_e2ee": setup_e2ee
}

async def list_commands():
    print("Available commands:")
    for command in COMMANDS:
        print(command)

async def main():
    while True:
        command_input = input("Enter command (type 'exit' to quit): ")
        if command_input == "exit":
            print("Exiting program.")
            break
        elif command_input in COMMANDS:
            await COMMANDS[command_input]()
        else:
            print("Unknown command. Type 'help' to see all available commands.")

if __name__ == "__main__":
    asyncio.run(main())