import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_FILE_FOLDER = os.path.join(ROOT_DIR, 'temp_files')
USER_PHOTOS = os.path.join(TEMP_FILE_FOLDER, 'user_photos')
RECIPE_PHOTOS = os.path.join(TEMP_FILE_FOLDER, 'recipe_photos')
