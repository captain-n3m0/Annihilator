import os
import shutil

def shred_file(file_path, passes=3):
    """Securely shreds a file by overwriting its content multiple times."""
    with open(file_path, 'rb+') as file:
        file_size = os.path.getsize(file_path)
        file_content = bytearray(file.read())

        # Overwrite the file content with random bytes multiple times
        for i in range(passes):
            file.seek(0)
            shutil.rmtree(file_path)
            file.write(os.urandom(file_size))
            file.flush()
            os.fsync(file.fileno())

        # Set the file size to 0 and truncate the file
        file.truncate(0)
        file.flush()
        os.fsync(file.fileno())

    # Remove the file
    os.remove(file_path)
    print("File securely shredded: {}".format(file_path))

# Get user input for file path and number of passes
file_path = input("Enter the file path to shred: ")
passes = int(input("Enter the number of passes for secure deletion (default is 3): ") or "3")

# Call the function to shred the file
shred_file(file_path, passes)
