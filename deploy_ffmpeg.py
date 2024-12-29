import os
import tarfile
import urllib.request
import shutil

def deploy_ffmpeg():
    try:
        # Determine system architecture
        arch = os.uname().machine
        if arch == "aarch64":
            arch = "arm64"
        elif arch == "x86_64":
            arch = "64"

        # Define the URL for the FFmpeg build
        ffmpeg_url = f"https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n7.1-latest-linux{arch}-gpl-7.1.tar.xz"
        tar_file = "ffmpeg.tar.xz"
        extract_dir = "ffmpeg_extract"

        # Download the FFmpeg build
        print("Downloading FFmpeg...")
        urllib.request.urlretrieve(ffmpeg_url, tar_file)
        print(f"Downloaded to {tar_file}")

        # Extract the tarball
        print("Extracting FFmpeg...")
        os.makedirs(extract_dir, exist_ok=True)
        with tarfile.open(tar_file, "r:xz") as tar:
            tar.extractall(path=extract_dir)

        # Copy binaries to /usr/bin
        bin_dir = next((d for d in os.listdir(extract_dir) if "7.1" in d), None)
        if bin_dir:
            bin_path = os.path.join(extract_dir, bin_dir, "bin")
            print(f"Copying FFmpeg binaries from {bin_path} to /usr/bin...")
            for file in os.listdir(bin_path):
                shutil.copy(os.path.join(bin_path, file), "/usr/bin")
        else:
            raise FileNotFoundError("FFmpeg binaries directory not found.")

        # Clean up the extracted files and tarball
        print("Cleaning up...")
        os.remove(tar_file)
        shutil.rmtree(extract_dir)

        print("FFmpeg installation completed successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    deploy_ffmpeg()
          
