"""Decetcion Face in anime, manga pictures ."""

import glob
import os


import cv2
import numpy
import PIL


class DetectAnimeFace:
    """
    Using this class you can find faces in animated images.

    It provides methods: reading images from a folder,
    searching for faces and saving them to a given offerer.
    """

    def __init__(self, original_images_folder_path: str, model_path: str,
                 created_images_folder_path: str) -> None:
        self.original_images_directory = original_images_folder_path
        self.file_with_model = model_path
        self.created_images_directory = created_images_folder_path

    @property
    def original_images_directory(self) -> str:
        """Set value of path to the images folder."""
        return self._original_images_folder_path

    @original_images_directory.setter
    def original_images_directory(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("The path to the images folder must be a string.")
        if not os.path.isdir(value):
            raise ValueError(f"Folder '{value}' was not found.")
        self._original_images_folder_path = value

    @original_images_directory.deleter
    def original_images_directory(self) -> None:
        del self._original_images_folder_path

    @property
    def file_with_model(self) -> str:
        """Set value of path to the model."""
        return self._model_path

    @file_with_model.setter
    def file_with_model(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("The path to the model must be a string.")
        if not os.path.isfile(value):
            raise ValueError(f"The path '{value}' does not exist.")
        self._model_path = value

    @file_with_model.deleter
    def file_with_model(self) -> None:
        del self._model_path

    @property
    def created_images_directory(self) -> str:
        """Path where new images are saved."""
        return self._created_images_folder_path

    @created_images_directory.setter
    def created_images_directory(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("The path to the images folder must be a string")
        if not os.path.isdir(value):
            try:
                os.makedirs(value, exist_ok=True)
                print(f"Folder '{value}' was created automatically.")
            except Exception as e:
                raise ValueError(f"Failed to create folder '{value}': {e}")
        self._created_images_folder_path = value

    @created_images_directory.deleter
    def created_images_directory(self) -> None:
        del self._created_images_folder_path

    def load_images_from_folder(self) -> list[tuple[str, numpy.array]]:
        """Read images from folder and add to the list."""
        images: list[tuple[str, numpy.array]] = []
        for filename in glob.glob(self.original_images_directory + '/*'):
            image: numpy.array = cv2.imread(filename)
            images.append((filename, image))
        return images

    def lbp_anime_face_detect(self):
        """Use algorithm to detect faces and save images in folder."""
        new_size_of_image: tuple(int, int) = (500, 500)
        index: int = 0
        for _, image in enumerate(self.load_images_from_folder()):
            image_gray: numpy.array = cv2.cvtColor(image[1],
                                                   cv2.COLOR_BGR2GRAY)
            image_gray = cv2.equalizeHist(image_gray)
            face_cascade: numpy.array = cv2.CascadeClassifier(self.file_with_model)
            faces = face_cascade.detectMultiScale(image_gray)
            for x, y, w, h in faces:
                image_path = image[0]
                read_image = PIL.Image.open(image_path)
                part_image: PIL.Image = read_image.crop((x, y, (x+w), (y+h)))
                resized_image: PIL.Image = part_image.resize(new_size_of_image)
                resized_image.save(f'{self.created_images_directory}/{index}.png')
                index += 1
