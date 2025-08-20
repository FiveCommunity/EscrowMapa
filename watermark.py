import os
import argparse

def watermark(path, content):
    try:
        for current_folder, subfolders, files in os.walk(path):
            readme_path = os.path.join(current_folder, "READ_ME.txt")
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)
    except Exception:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a watermark in all folders")
    parser.add_argument("-d", "--directory", required=True, help="Target directory")
    args = parser.parse_args()

    content = """discord.gg/fivecommunity
    """
    watermark(args.directory, content)