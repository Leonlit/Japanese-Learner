import uuid, os

def generate_uuid_for_user_tts():
    unique_id = uuid.uuid4()
    return unique_id

def make_sure_directory_exists(directory):
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as err:
        print(err)
        return False