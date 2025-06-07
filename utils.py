import os
from config import TRACKING_FILE_NAME

def file_exists(file_path):
    return os.path.isfile(file_path)

def create_file(file_path, content=""):
    try:
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return True
    except Exception as e:
        print(e)
        return False
    
def delete_file(file_path):
    try:
        if file_exists(file_path):
            os.remove(file_path)
            return True
        else:
            return True
    except Exception as e:
        print(e)
        return False
    
def clear():
    os.system('cls') if os.name == 'nt' else os.system('clear')

def update_tracking_file(folder_path: str, youtube_urls: list[str]) -> bool:
    try:
        tracking_file_path = os.path.join(folder_path, TRACKING_FILE_NAME)
        
        with open(tracking_file_path, 'w', encoding='utf-8') as f:
            for url in youtube_urls:
                f.write(f"{url}\n")
        
        print(f"Updated tracking file with {len(youtube_urls)} URLs")
        return True
        
    except Exception as e:
        print(f"Error updating tracking file: {e}")
        return False