require 'securerandom'
require 'fileutils'

def shred_file(file_path, passes=3)
  # Get file size
  file_size = File.size(file_path)

  # Overwrite the file content with multiple overwriting patterns
  passes.times do |i|
    # Generate random bytes
    file_content = SecureRandom.bytes(file_size)

    # Write multiple overwriting patterns to the file
    patterns = [file_content, "\xFF" * file_size, "\x00" * file_size]
    File.open(file_path, 'wb') { |file| file.write(patterns[i % patterns.length]) }
  end

  # Set the file size to 0 and truncate the file
  File.truncate(file_path, 0)

  # Rename the file to a random name and wipe its metadata
  file_name, file_ext = File.split(file_path)
  random_name = SecureRandom.hex(16) + file_ext
  File.rename(file_path, random_name)
  File.utime(0, 0, random_name)

  # Remove the file
  FileUtils.rm_rf(random_name)
  puts "File securely shredded: #{file_path}"
end

# Get user input for file path and number of passes
print "Enter the file path to shred: "
file_path = gets.chomp
print "Enter the number of passes for secure deletion (default is 3): "
passes = (gets.chomp.empty? ? 3 : gets.chomp.to_i)

# Call the function to shred the file
shred_file(file_path, passes)
