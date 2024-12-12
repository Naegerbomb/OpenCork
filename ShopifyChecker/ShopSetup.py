import json
import os

def get_existing_config(filename='Ignored Files/ShopSetupConfig.json'):
    """Load existing configuration data from a JSON file if it exists."""
    if os.path.exists(filename):
        with open(filename, 'r') as config_file:
            return json.load(config_file)
    return {}

def get_user_input(existing_config):
    """Prompt the user for configuration details, using existing values if available."""
    config_data = existing_config.copy()
    print("Please enter the following configuration details (leave blank to keep existing values):")
    config_data['shop_name'] = input(f"Shop Name [{existing_config.get('shop_name', '')}]: ") or existing_config.get('shop_name', '')
    config_data['access_token'] = input(f"Admin API Access Token [{existing_config.get('access_token', '')}]: ") or existing_config.get('access_token', '')
    return config_data

def save_config_file(config_data, filename='Ignored Files/ShopSetupConfig.json'):
    """Save the configuration data to a JSON file."""
    with open(filename, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print(f"Configuration saved to {filename}")

def update_gitignore(filename='.gitignore', entry='Ignored Files/ShopSetupConfig.json'):
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
    existing_config = get_existing_config()
    config_data = get_user_input(existing_config)
    save_config_file(config_data)
    update_gitignore()

if __name__ == "__main__":
    main()
