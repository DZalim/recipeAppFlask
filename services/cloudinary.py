import cloudinary
import cloudinary.uploader
from decouple import config
from werkzeug.exceptions import BadRequest


class CloudinaryService:
    def __init__(self):
        self.cloud_name = config("CLOUDINARY_CLOUD_NAME")
        self.api_key = config("CLOUDINARY_API_KEY")
        self.api_secret = config("CLOUDINARY_API_SECRET")

        cloudinary.config(
            cloud_name=self.cloud_name,
            api_key=self.api_key,
            api_secret=self.api_secret
        )

    @staticmethod
    def upload_photo(path, ext):
        try:
            response = cloudinary.uploader.upload(path, resource_type="image", format=ext, folder="flaskrecipes")
            return response["secure_url"]
        except Exception as e:
            raise BadRequest(f"Cloudinary is not available at the moment: {str(e)}")

    @staticmethod
    def extract_public_id(secure_url):

        """
        :param secure_url: https://res.cloudinary.com/<cloud_name>/image/upload/v<version>/<public_id>.<format>
        :return: public_id
        """

        parts = secure_url.split("/")
        last_two_parts = parts[-2:]  # ["flaskrecipes", "myphoto.jpg"]
        path_with_extensions = "/".join(last_two_parts)  # "flaskrecipes/myphoto.jpg"
        public_id = path_with_extensions.rsplit(".", 1)[0]  # "flaskrecipes/myphoto"

        return public_id

    def delete_photo(self, secure_url):
        public_id = self.extract_public_id(secure_url)
        try:
            response = cloudinary.uploader.destroy(public_id, invalidate=True, resource_type="image")
            return f"Successfully deleted photo with public ID: {public_id}"
        except Exception as e:
            raise BadRequest(f"Failed to delete photo: {str(e)}")
