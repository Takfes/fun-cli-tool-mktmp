import importlib
import os
import subprocess
import sys

# List of packages to check for and install if missing - before creating the project
REQUIREMENTS = ['requests', 'argparse']

# List of folders to create inside the project folder
FOLDERS = ['app', 'src', 'data', 'docs', 'notebooks', 'tests']

# List of packages to install inside the virtual environment
PACKAGE_LIST = ['ipykernel', 'pre-commit', 'python-dotenv', 'black','isort','autopep8', 'pytest']

# Dictionary of files to download from Gist and write to the project folder
GIST_URLS = {
    '.vscode/settings.json': 'https://gist.githubusercontent.com/Takfes/f851ba72f994ec51c9bee09f1ba27417/raw/e1d409a341b042702342be18a07ea2236c701a44/settings.json',
    '.flake8': 'https://gist.githubusercontent.com/Takfes/f851ba72f994ec51c9bee09f1ba27417/raw/e1d409a341b042702342be18a07ea2236c701a44/.flake8',
    '.gitignore': 'https://gist.githubusercontent.com/Takfes/f851ba72f994ec51c9bee09f1ba27417/raw/6e49e0e52b539e0dc9be0f6b0f8673b3f894533a/.gitignore',
    'pyproject.toml': 'https://gist.githubusercontent.com/Takfes/f851ba72f994ec51c9bee09f1ba27417/raw/e1d409a341b042702342be18a07ea2236c701a44/pyproject.toml',
    'precommit-config.yaml': 'https://gist.githubusercontent.com/Takfes/f851ba72f994ec51c9bee09f1ba27417/raw/e1d409a341b042702342be18a07ea2236c701a44/.pre-commit-config.yaml',
    'start.sh': 'https://gist.githubusercontent.com/Takfes/f851ba72f994ec51c9bee09f1ba27417/raw/df2ecf222508121029ed23093f35de159798ed58/start.sh',
    'genreqs.sh': 'https://gist.githubusercontent.com/Takfes/f851ba72f994ec51c9bee09f1ba27417/raw/df2ecf222508121029ed23093f35de159798ed58/genreqs.sh'
}

def is_package_installed(package):
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'show', package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def install_missing_packages(packages):
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"Successfully installed {package}.")
            globals()[package] = importlib.import_module(package)
            print(f"Successfully imported {package}.")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}. Please install it manually.")

def check_dependencies(required_packages):
    missing_packages = []

    for package in required_packages:
        print(f"🔍 Checking for {package}...")
        if not is_package_installed(package):
            missing_packages.append(package)
            print(f"❌ {package} is not installed.")
        else:
            globals()[package] = importlib.import_module(package)
            print(f"Successfully imported {package}.")

    if missing_packages:
        print("🧩 The following packages are missing: " + ", ".join(missing_packages))
        choice = input("Do you want to attempt to install them now? (y/n): ").strip().lower()
        if choice == 'y':
            install_missing_packages(missing_packages)
        else:
            print("🚨 Please install the missing packages to proceed.")
            sys.exit(1)
    else:
        print("✅ All dependencies exist.")
        
def parse_user_input():
    import argparse
    parser = argparse.ArgumentParser(description='Project Creation Tool')
    # parser.add_argument('-n', '--name', type=str, help='Name of the project to create')
    parser.add_argument('name', type=str, help='Name of the project to create')
    args = parser.parse_args()
    if args.name is None:
        parser.error("❌ the following arguments are required: -n/--name")
    return parser.parse_args()

def create_and_cd_project_folder(project_name):
    print(f"📂 Creating project: {project_name}")
    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)

def create_folder_structure(folders):
    print("📂 Creating folder structure")
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        # Create a .gitkeep file in each folder
        with open(os.path.join(folder, '.gitkeep'), 'w') as file:
            pass  # Just create an empty file 

def create_virtualenv():
    print("🌍 Creating virtual environment...")
    subprocess.run(["virtualenv", "venv"], check=True)

def upgrade_pip():
    print("👍 Upgrading pip...")
    subprocess.run(["venv/bin/pip", "install", "--upgrade", "pip"], check=True)

def install_packages(packages):
    print("📦 Installing packages inside the virtual environment...")
    venv_python = './venv/bin/python'  # Path to the Python executable in the venv
    subprocess.run([venv_python, '-m', 'pip', 'install', *packages], check=True)

def download_and_write_file(gist_urls):
    import requests
    os.makedirs('.vscode', exist_ok=True)
    for file_path,gist_url in gist_urls.items():
        response = requests.get(gist_url)
        if response.status_code == 200:
            print(f'⬇️ Downloading {file_path} from {gist_url}')
            with open(file_path, 'w') as file:
                file.write(response.text)
        else:
            print(f"Failed to download file from {gist_url}")

def chmod_start():
    print("✅ chmod start.sh...")
    subprocess.run(["chmod", "+x", "start.sh"], check=True)

def generate_requirements_txt():
    print("🔨 Generating requirements.txt...")
    venv_python = './venv/bin/python'  # Path to the Python executable in the venv
    # Run pip freeze and capture the output
    pip_freeze_output = subprocess.run([venv_python, '-m', 'pip', 'freeze'], capture_output=True, text=True, check=True)
    # Filter the output and write to requirements.txt
    with open('requirements.txt', 'w') as requirements_file:
        for line in pip_freeze_output.stdout.splitlines():
            if '-e' not in line:  # Exclude lines with '-e'
                requirements_file.write(line + '\n')

def main():
    check_dependencies(REQUIREMENTS)
    project_name = parse_user_input().name
    create_and_cd_project_folder(project_name)
    create_folder_structure(FOLDERS)
    create_virtualenv()
    upgrade_pip()
    install_packages(PACKAGE_LIST)
    generate_requirements_txt()
    download_and_write_file(GIST_URLS)
    chmod_start()

if __name__ == '__main__':
    main()
