from src.drive_db import delete_logs

def main():
    warn_text = '''
 _    _  ___  ______ _   _ _____ _   _ _____ 
| |  | |/ _ \\ | ___ \\ \\ | |_   _| \\ | |  __ \\
| |  | / /_\\ \\| |_/ /  \\| | | | |  \\| | |  \\/
| |/\\| |  _  ||    /| . ` | | | | . ` | | __ 
\\  /\\  / | | || |\\ \\| |\\  |_| |_| |\\  | |_\\ \\
 \\/  \\/\\_| |_/\\_| \\_\\_| \\_/\\___/\\_| \\_/\\____/
    '''
    print(warn_text)
    usr = str()
    while usr.lower() != 'y':
        usr = str(input("Esata seguro que deséa ELIMINAR la Log DB (y/n): " ))
    delete_logs()

main()