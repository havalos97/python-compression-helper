import base64
import subprocess
import os
import platform
import tempfile


class compression_helper:
  def __init__(self):
    self.extracted_executable = None
    self.base64_files = {
      "linux": "./execs/linux.b64",
      "darwin": "./execs/macos.b64",
      "windows": "./execs/win.b64"
    }

  def _read_base64_file(self, filename):
    with open(filename, "r") as file:
      return file.read()

  def _extract_executable(self):
    system = platform.system().lower()
    executable_name = "compressionhelper"
    base64_file = self.base64_files.get(system, "./execs/macos.b64")

    if system == "windows":
      executable_name = f"{executable_name}.exe"

    # Determine the path for the executable in the temp directory
    temp_dir = tempfile.gettempdir()
    self.extracted_executable = os.path.join(temp_dir, executable_name)

    # Check if the executable already exists
    if os.path.exists(self.extracted_executable):
      return

    executable_data = self._read_base64_file(base64_file)

    # Decode the base64 string
    executable_bytes = base64.b64decode(executable_data)
    
    # Write to a temporary file
    with open(self.extracted_executable, "wb") as executable_file:
      executable_file.write(executable_bytes)
    
    # Make the file executable
    os.chmod(self.extracted_executable, 0o755)

  def _ensure_executable_extracted(self):
    if not self.extracted_executable:
      self._extract_executable()

  def compress(self, strInput) -> str:
    self._ensure_executable_extracted()

    try:
      result = subprocess.run([self.extracted_executable, "compress", strInput], check=True, capture_output=True)
      return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
      print(f"Compression failed: {e.stderr.decode()}")

  def decompress(self, strInput) -> str:
    self._ensure_executable_extracted()

    try:
      result = subprocess.run([self.extracted_executable, "decompress", strInput], check=True, capture_output=True)
      return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
      print(f"Decompression failed: {e.stderr.decode()}")

# Example usage
if __name__ == "__main__":
  helper = compression_helper()
  compressed_data = helper.compress("HELLO WORLD")
  print(f"Compressed data: {compressed_data}")
  decompressed_data = helper.decompress(compressed_data)
  print(f"Decompressed data: {decompressed_data}")
