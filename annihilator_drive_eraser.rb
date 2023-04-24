require 'securerandom'

def create_temp_file(file_path, size)
  # Creates a temporary file with random content
  File.open(file_path, 'wb') do |file|
    file.write(SecureRandom.bytes(size))
  end
end

def erase_drive(drive_path, passes=3)
  begin
    # Unmount the drive if it's mounted
    system('umount', drive_path)

    # Get the drive size
    drive_size = File.size(drive_path)

    # Calculate the file size for each pass
    file_size = drive_size / passes

    # Create and write temporary files to the drive with random data
    passes.times do
      (drive_size / file_size).times do
        temp_file_path = SecureRandom.hex(8)
        create_temp_file(temp_file_path, file_size)
        system('dd', "if=#{temp_file_path}", "of=#{drive_path}", 'bs=4M')
        File.delete(temp_file_path)
      end
    end

    # Fill the drive with zeros
    system('dd', 'if=/dev/zero', "of=#{drive_path}", 'bs=4M')

    # Use the shred command to overwrite the entire drive with random data
    system('shred', '-n', '1', '-s', drive_size.to_s, drive_path)

    puts "Drive securely erased: #{drive_path}"
  rescue StandardError => e
    puts "Failed to erase the drive: #{e}"
  end
end

# Get user input for drive path and number of passes
print "Enter the drive path to erase (e.g., /dev/sdb): "
drive_path = gets.chomp
print "Enter the number of passes for secure deletion (default is 3): "
passes = (gets.chomp.to_i).nonzero? || 3

# Call the function to erase the drive
erase_drive(drive_path, passes)
