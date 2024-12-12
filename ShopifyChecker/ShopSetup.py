import json
import os

def get_existing_config(filename='ShopSetupConfig.json'):
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
    config_data['api_key'] = input(f"API Key [{existing_config.get('api_key', '')}]: ") or existing_config.get('api_key', '')
    config_data['api_secret'] = input(f"API Secret [{existing_config.get('api_secret', '')}]: ") or existing_config.get('api_secret', '')
    config_data['other_setting'] = input(f"Other Setting [{existing_config.get('other_setting', '')}]: ") or existing_config.get('other_setting', '')
    return config_data

def save_config_file(config_data, filename='ShopSetupConfig.json'):
    """Save the configuration data to a JSON file."""
    with open(filename, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print(f"Configuration saved to {filename}")

def update_gitignore(filename='.gitignore', entry='ShopSetupConfig.json'):
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
