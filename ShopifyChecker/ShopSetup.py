import json
import os

def get_user_input():
    """Prompt the user for configuration details."""
    config_data = {}
    print("Please enter the following configuration details:")
    config_data['api_key'] = input("API Key: ")
    config_data['api_secret'] = input("API Secret: ")
    config_data['other_setting'] = input("Other Setting: ")
    return config_data

def save_config_file(config_data, filename='config.json'):
    """Save the configuration data to a JSON file."""
    with open(filename, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print(f"Configuration saved to {filename}")

def update_gitignore(filename='.gitignore', entry='config.json'):
    """Add the configuration file to .gitignore if not already present."""
    if os.path.exists(filename):
        with open(filename, 'r') as gitignore_file:
            lines = gitignore_file.read().splitlines()
    else:
        lines = []

    if entry not in lines:
        lines.append(entry)
        with open(filename, 'w') as gitignore_file:
            gitignore_file.write('\n'.join(lines) + '\n')
        print(f"Added {entry} to {filename}")
    else:
        print(f"{entry} is already present in {filename}")

def main():
    config_data = get_user_input()
    save_config_file(config_data)
    update_gitignore()

if __name__ == "__main__":
    main()
