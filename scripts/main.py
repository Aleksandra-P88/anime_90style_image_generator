"""Script to run all functions."""

import const
import image_downloader
import image_to_text
import new_image_detect


def download_images_from_internet() -> None:
    """Download images."""
    try:
        downloadimage = image_downloader.DownloadImage(const.SAFEBOORU_TAGS,
                                                       const.SAFEBOORU_PANEL_OF_IMAGE,
                                                       const.SAFEBOORU_INDIVIDUAL_IMAGE)
        downloadimage.download_and_save_images(126,
                                               const.ORIGINAL_IMAGES_FOLDER_PATH,
                                               'Safebooru')
    except ValueError as error:
        print("Erorr when create download images:", error)


def detect_faces() -> None:
    """Detect face in anime images."""
    try:
        image = new_image_detect.DetectAnimeFace(const.ORIGINAL_IMAGES_FOLDER_PATH,
                                                 const.MODEL_PATH,
                                                 const.CREATED_IMAGES_FOLDER_PATH)
        image.load_images_from_folder()
        image.lbp_anime_face_detect()
    except ValueError as error:
        print("Erorr when create anime images:", error)


def text_from_image() -> None:
    """Create text files from images."""
    try:
        image = image_to_text.ImageToText(const.CREATED_IMAGES_FOLDER_PATH,
                                          const.IMAGE_TO_TEXT_MODEL,
                                          const.CREATED_IMAGES_FOLDER_PATH)
        image.create_text_from_image()
    except ValueError as error:
        print("Erorr when create text from images:", error)


if __name__ == "__main__":
    download_images_from_internet()
    detect_faces()
    text_from_image()
