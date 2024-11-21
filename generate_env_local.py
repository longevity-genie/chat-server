#!/usr/bin/env python3

import os
import sys
import json
import glob

def main():
    env_local_path = '.env.local'
    models_dir = 'models.d'
    temp_env_local_path = '.env.local.tmp'

    # Check if .env.local exists
    if not os.path.exists(env_local_path):
        print(f"Error: {env_local_path} does not exist.")
        sys.exit(1)

    # Read the existing .env.local file
    with open(env_local_path, 'r') as f:
        lines = f.readlines()

    # Remove existing MODELS variable (including multi-line definitions)
    new_lines = []
    skip = False
    for line in lines:
        stripped_line = line.strip()
        if not skip:
            if stripped_line.startswith('MODELS='):
                if '`' in stripped_line:
                    # Check if it's a single-line MODELS definition
                    if stripped_line.count('`') == 2:
                        continue  # Skip the entire line
                    else:
                        skip = True  # Start skipping lines
                else:
                    skip = True  # Start skipping lines
            else:
                new_lines.append(line)
        else:
            if '`' in stripped_line:
                skip = False  # Found closing backtick, stop skipping
            continue  # Skip lines within MODELS definition

    # Load and validate JSON files from models.d
    model_files = glob.glob(os.path.join(models_dir, '*.json'))
    models = []

    if not model_files:
        print(f"No JSON files found in {models_dir}.")
        sys.exit(1)

    for model_file in model_files:
        try:
            with open(model_file, 'r') as f:
                data = json.load(f)
                # Simple validation: check if 'displayName' field exists
                if 'displayName' not in data:
                    raise ValueError(f"'displayName' field missing in {model_file}")
                models.append(data)
        except Exception as e:
            print(f"Error loading {model_file}: {e}")
            sys.exit(1)

    # Write the updated .env.local file
    with open(temp_env_local_path, 'w') as f:
        f.writelines(new_lines)
        # Serialize the models list as a JSON string and add it to MODELS=
        models_json = json.dumps(models, ensure_ascii=False, indent=4)
        f.write("MODELS=`\n")
        f.write(f"{models_json}\n")
        f.write("`\n")

    # Replace the old .env.local with the new one
    os.replace(temp_env_local_path, env_local_path)

    # Output the list of models using 'displayName' field
    print("Models loaded successfully:")
    for model in models:
        print(f"- {model.get('displayName')}")

if __name__ == "__main__":
    main()
