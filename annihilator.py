import os
import random
import shutil

def shred_file(file_path, passes=3):
    """Securely shreds a file by overwriting its content multiple times."""
    file_size = os.path.getsize(file_path)

    # Overwrite the file content with multiple overwriting patterns
    for i in range(passes):
        with open(file_path, 'rb+') as file:
            # Generate random bytes using a cryptographically secure random number generator
            random_generator = random.SystemRandom() if os.name == 'posix' else random.Random()
            file_content = bytearray(random_generator.getrandbits(8) for _ in range(file_size))

            # Write multiple overwriting patterns to the file
            patterns = [bytearray(file_size), bytearray([0xFF] * file_size), bytearray([0x00] * file_size)]
            file.write(patterns[i % len(patterns)])
            file.flush()
            os.fsync(file.fileno())

    # Set the file size to 0 and truncate the file
    with open(file_path, 'wb') as file:
        file.truncate(0)
        file.flush()
        os.fsync(file.fileno())

    # Rename the file to a random name and wipe its metadata
    file_name, file_ext = os.path.splitext(file_path)
    random_name = ''.join(random.choice('0123456789ABCDEF') for _ in range(16)) + file_ext
    os.rename(file_path, random_name)
    os.utime(random_name, (0, 0))

    # Remove the file
    shutil.rmtree(random_name)
    print("File securely shredded: {}".format(file_path))

# Get user input for file path and number of passes
file_path = input("Enter the file path to shred: ")
passes = int(input("Enter the number of passes for secure deletion (default is 3): ") or "3")

# Call the function to shred the file
shred_file(file_path, passes)
