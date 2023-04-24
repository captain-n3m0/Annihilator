import subprocess
import os
import random
import string

def create_temp_file(file_path, size):
    """Creates a temporary file with random content."""
    with open(file_path, 'wb') as file:
        # Generate random content for the file
        file_content = bytearray([random.randint(0, 255) for _ in range(size)])
        file.write(file_content)

def erase_drive(drive_path, passes=3):
    """Erases a drive completely by overwriting files with random data, filling with zeros, and using the shred command."""
    try:
        # Unmount the drive if it's mounted
        subprocess.check_call(['umount', drive_path])

        # Get the drive size
        drive_size = os.path.getsize(drive_path)

        # Calculate the file size for each pass
        file_size = drive_size // passes

        # Create and write temporary files to the drive with random data
        for i in range(passes):
            for j in range(drive_size // file_size):
                temp_file_path = ''.join(random.choice(string.ascii_letters) for _ in range(16))
                create_temp_file(temp_file_path, file_size)
                subprocess.check_call(['dd', 'if=' + temp_file_path, 'of=' + drive_path, 'bs=4M'])
                os.remove(temp_file_path)

        # Fill the drive with zeros
        subprocess.check_call(['dd', 'if=/dev/zero', 'of=' + drive_path, 'bs=4M'])

        # Use the shred command to overwrite the entire drive with random data
        subprocess.check_call(['shred', '-n', '1', '-s', str(drive_size), drive_path])

        print("Drive securely erased: {}".format(drive_path))
    except subprocess.CalledProcessError as e:
        print("Failed to erase the drive: {}".format(e))
    except Exception as ex:
        print("Error occurred: {}".format(ex))

# Get user input for drive path and number of passes
drive_path = input("Enter the drive path to erase (e.g., /dev/sdb): ")
passes = int(input("Enter the number of passes for secure deletion (default is 3): ") or "3")

# Call the function to erase the drive
erase_drive(drive_path, passes)
