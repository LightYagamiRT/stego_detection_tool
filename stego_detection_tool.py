import subprocess
import os
import shutil

# Colors
class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# List of required packages
required_packages = ['steghide', 'exiftool', 'zsteg', 'binwalk', 'foremost', 'pngcheck', 'stegseek']

def check_required_packages():
    missing_packages = [package for package in required_packages if not is_package_installed(package)]
    return missing_packages

# Function to check if a package is installed
def is_package_installed(package):
    try:
        subprocess.check_output(['which', package])
        return True
    except subprocess.CalledProcessError:
        return False

# Function to install a package
def install_package(package):
    try:
        subprocess.check_call(['sudo', 'apt', 'install', package])
        return True
    except subprocess.CalledProcessError:
        return False

# Function to run strings and grep for potential flags
def run_strings_and_grep(filepath):
    if not is_package_installed('strings'):
        print("Package 'strings' is not installed.")
        install = input("Do you want to install it? (yes/no): ").lower()
        if install == 'yes':
            if install_package('strings'):
                print("Package 'strings' installed successfully.")
            else:
                print("Failed to install package 'strings'.")
        else:
            print("Aborted.")
            return
    try:
        strings_output = subprocess.check_output(['strings', filepath])
        grep_output = subprocess.check_output(['grep', '-i', 'CTF'], input=strings_output)
        return grep_output.decode()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode()}"

# Function to run strings and grep for potential flags
def run_strings_and_grep(filepath):
    try:
        strings_output = subprocess.check_output(['strings', filepath])
        grep_output = subprocess.check_output(['grep', '-i', 'CTF'], input=strings_output)
        return grep_output.decode()
    except subprocess.CalledProcessError as e:
        return f"{colors.FAIL}Error: {e.output.decode()}{colors.ENDC}"

# Function to run exiftool
def run_exiftool(filepath):
    try:
        output = subprocess.check_output(['exiftool', filepath])
        return output.decode()
    except subprocess.CalledProcessError as e:
        return f"{colors.FAIL}Error: {e.output.decode()}{colors.ENDC}"

# Function to run steghide
def run_steghide(filepath, passphrase=None):
    try:
        cmd = ['steghide', 'info']
        if passphrase:
            cmd.extend(['-p', passphrase])
        cmd.append(filepath)
        output = subprocess.check_output(cmd)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return f"{colors.FAIL}Error: {e.output.decode()}{colors.ENDC}"

# Function to run zsteg
def run_zsteg(filepath):
    try:
        output = subprocess.check_output(['zsteg', filepath])
        return output.decode()
    except subprocess.CalledProcessError as e:
        return f"{colors.FAIL}Error: {e.output.decode()}{colors.ENDC}"

# Function to run binwalk
def run_binwalk(filepath):
    try:
        output = subprocess.check_output(['binwalk', '-e', filepath])
        return output.decode()
    except subprocess.CalledProcessError:
        try:
            output = subprocess.check_output(['binwalk', '-dd', '.*', filepath])
            return output.decode()
        except subprocess.CalledProcessError as e:
            return f"{colors.FAIL}Error: {e.output.decode()}{colors.ENDC}"

# Function to run foremost
def run_foremost(filepath):
    try:
        output_dir = "foremost_output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output = subprocess.check_output(['foremost', '-t', 'jpg', '-o', output_dir, filepath])
        # Output audit.txt
        audit_txt_path = os.path.join(output_dir, "audit.txt")
        if os.path.exists(audit_txt_path):
            with open(audit_txt_path, 'r') as f:
                return f.read()
        return output.decode()
    except subprocess.CalledProcessError as e:
        return f"{colors.FAIL}Error: {e.output.decode()}{colors.ENDC}"

# Function to run pngcheck
def run_pngcheck(filepath):
    if not is_package_installed('pngcheck'):
        print("Package 'pngcheck' is not installed.")
        install = input("Do you want to install it? (yes/no): ").lower()
        if install == 'yes':
            if install_package('pngcheck'):
                print("Package 'pngcheck' installed successfully.")
            else:
                print("Failed to install package 'pngcheck'.")
        else:
            print("Aborted.")
            return

    try:
        output = subprocess.check_output(['pngcheck', filepath])
        return output.decode()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode()}"

# Function to run stegseek with or without brute force
def run_stegseek(filepath, brute_force=False):
    rockyou_path = "/usr/share/wordlists/rockyou.txt"
    if brute_force:
        print("\nBrute forcing with StegSeek using rockyou.txt...\n")
        try:
            output = subprocess.check_output(['stegseek', filepath, rockyou_path])
            return output.decode()
        except subprocess.CalledProcessError as e:
            error_message = e.output.decode()
            if "the file format" in error_message:
                return f"{colors.FAIL}Error: Stegseek does not support this file format.{colors.ENDC}"
            return f"{colors.FAIL}Error: {error_message}{colors.ENDC}"

# Function to clear outputs
def clear_outputs():
    shutil.rmtree("foremost_output", ignore_errors=True)

# Main function
def main():
    # Check if all required packages are installed
    missing_packages = check_required_packages()

    if missing_packages:
        print(f"{colors.FAIL}The following required packages are not installed:")
        for package in missing_packages:
            print(f"- {package}")
        install_all = input("Do you want to install all missing packages? (yes/no): ").lower()
        if install_all == 'yes':
            for package in missing_packages:
                if install_package(package):
                    print(f"{colors.OKGREEN}Package '{package}' installed successfully.{colors.ENDC}")
                else:
                    print(f"{colors.FAIL}Failed to install package '{package}'.{colors.ENDC}")
        else:
            print(f"{colors.WARNING}Aborted.{colors.ENDC}")
            return

    print(f"{colors.HEADER}"
	"""
                      ..:::::::::..
                  ..:::aad8888888baa:::..
              .::::d:?88888888888?::8b::::.
            .:::d8888:?88888888??a888888b:::.
          .:::d8888888a8888888aa8888888888b:::.
         ::::dP::::::::88888888888::::::::Yb::::
        ::::dP:::::::::Y888888888P:::::::::Yb::::
       ::::d8:::::::::::Y8888888P:::::::::::8b::::
      .::::88::::::::::::Y88888P::::::::::::88::::.
      :::::Y8baaaaaaaaaa88P:T:Y88aaaaaaaaaad8P:::::
      :::::::Y88888888888P::|::Y88888888888P:::::::
      ::::::::::::::::888:::|:::888::::::::::::::::
      `:::::::::::::::8888888888888b::::::::::::::'
       :::::::::::::::88888888888888::::::::::::::
        :::::::::::::d88888888888888:::::::::::::
         ::::::::::::88::88::88:::88::::::::::::
          `::::::::::88::88::88:::88::::::::::'
            `::::::::88::88::88:::88::::::::'
              `::::::88::88::88:::88::::::'
                 ``:::::::::::::::::::''
                      ``:::::::::''
	"""

          f"{colors.ENDC}")
    print(f"{colors.BOLD}Welcome to the Steganography Detection Tool!{colors.ENDC}")
    print(f"{colors.OKBLUE}Listing files in the current directory:{colors.ENDC}")
    print(subprocess.check_output(['ls']).decode())
    
    while True:
        filepath = input("Enter the path to the file: ")
        if os.path.exists(filepath):
            break
        else:
            print(f"{colors.FAIL}File not found. Please enter a valid path.{colors.ENDC}")
    
    print("Please select an option:")
    print("0. Run all tools")
    print("1. Run strings and grep")
    print("2. Run exiftool")
    print("3. Run steghide")
    print("4. Run zsteg")
    print("5. Run binwalk")
    print("6. Run foremost")
    print("7. Run pngcheck")
    print("8. Run stegseek")
    print("9. Clear outputs")
    print("10. Run Foremost directory")
    print("11. Exit")

    while True:
        option = input("Enter your choice (0-11): ")
        if option in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']:
            break
        else:
            print(f"{colors.FAIL}Invalid option. Please enter a number between 0 and 11.{colors.ENDC}")

    if option == '0':
        print("Running all tools...\n")

        print(f"{colors.BOLD}Strings and Grep:{colors.ENDC}")
        print(run_strings_and_grep(filepath))

        print(f"\n{colors.BOLD}Exiftool:{colors.ENDC}")
        print(run_exiftool(filepath))

        print(f"\n{colors.BOLD}Steghide:{colors.ENDC}")
        print(run_steghide(filepath))

        print(f"\n{colors.BOLD}Zsteg:{colors.ENDC}")
        print(run_zsteg(filepath))

        print(f"\n{colors.BOLD}Binwalk:{colors.ENDC}")
        print(run_binwalk(filepath))

        print(f"\n{colors.BOLD}Foremost:{colors.ENDC}")
        print(run_foremost(filepath))

        print(f"\n{colors.BOLD}Pngcheck:{colors.ENDC}")
        print(run_pngcheck(filepath))

        brute_force_input = input("\nDo you want to perform brute force with StegSeek? (yes/no): ").lower()
        if brute_force_input == 'yes' or brute_force_input == 'y':
            print(run_stegseek(filepath, brute_force=True))
        elif brute_force_input == 'no' or brute_force_input == 'n':
            print(run_stegseek(filepath))

    elif option == '1':
        print(f"{colors.BOLD}Running strings and grep...{colors.ENDC}\n")
        print(run_strings_and_grep(filepath))

    elif option == '2':
        print(f"{colors.BOLD}Running exiftool...{colors.ENDC}\n")
        print(run_exiftool(filepath))

    elif option == '3':
        print(f"{colors.BOLD}Running steghide...{colors.ENDC}\n")
        print(run_steghide(filepath))

    elif option == '4':
        print(f"{colors.BOLD}Running zsteg...{colors.ENDC}\n")
        print(run_zsteg(filepath))

    elif option == '5':
        print(f"{colors.BOLD}Running binwalk...{colors.ENDC}\n")
        print(run_binwalk(filepath))

    elif option == '6':
        print(f"{colors.BOLD}Running foremost...{colors.ENDC}\n")
        print(run_foremost(filepath))

    elif option == '7':
        print(f"{colors.BOLD}Running pngcheck...{colors.ENDC}\n")
        print(run_pngcheck(filepath))

    elif option == '8':
        print(f"{colors.BOLD}Running stegseek...{colors.ENDC}\n")
        brute_force_input = input("Do you want to perform brute force with StegSeek? (yes/no): ").lower()
        if brute_force_input == 'yes' or brute_force_input == 'y':
            print(run_stegseek(filepath, brute_force=True))

    elif option == '9':
        print(f"{colors.BOLD}Clearing outputs...{colors.ENDC}\n")
        clear_outputs()
        print(f"{colors.OKGREEN}Outputs cleared.{colors.ENDC}")

    elif option == '10':
        confirm = input("Are you sure you want to run Foremost's directory? This will generate a lot of output. (yes/no): ")
        if confirm.lower() == 'yes':
            print(f"{colors.BOLD}Running Foremost's directory...{colors.ENDC}\n")
            subprocess.call(["python", "foremost_output"])
        else:
            print(f"{colors.WARNING}Aborted.{colors.ENDC}")

    elif option == '11':
        print(f"{colors.OKBLUE}Exiting...{colors.ENDC}")
        clear_outputs()

if __name__ == "__main__":
    main()
