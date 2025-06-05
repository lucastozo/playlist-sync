import os

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