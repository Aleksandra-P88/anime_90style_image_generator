"""Create description based on choosen image ."""
import glob
import os

import numpy
import PIL

import diffusers
import transfomers


class ImageToText:
    """
    Using this class you can generate description from images.

    It provides methods: reading images from a folder
    and create descriptions.
    """

    def __init__(self, original_images_folder_path: str, model_path: str,
                 choose_images_folder_path: str) -> None:
        self.original_images_directory = original_images_folder_path
        self.file_with_model = model_path
        self.choosen_images_directory = choose_images_folder_path

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
    def choosen_images_directory(self) -> str:
        """Path where texts are saved."""
        return self._choosen_images_folder_path

    @choosen_images_directory.setter
    def choosen_images_directory(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("The path to the folder must be a string")
        self._choosen_images_folder_path = value

    @choosen_images_directory.deleter
    def choosen_images_directory(self) -> None:
        del self._choosen_images_folder_path

    def read_images_from_folder(self) -> list[tuple[str, numpy.array]]:
        """Load images from which the text is created."""
        images: list[tuple[str, numpy.array]] = []
        for filename in glob.glob(self.original_images_director + '/*'):
            try:
                if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    print(f"Skipping non-image file: {filename}")
                    continue
                img = PIL.Image.open(filename).convert("RGB")
                images.append((filename, img))
            except Exception as e:
                print(f"Failed to load image {filename}: {e}")
        return images

    def create_text_from_image(self):
        """Genrate texts."""
        image_to_text = diffusers.pipeline("image-to-text",
                                           model=self.file_with_model)
        for filename, _ in self.read_image_from_folder():
            result = image_to_text(filename, max_new_tokens=50)
            generated_text = result[0]['generated_text']
            print(f"Generated text for {filename}: {generated_text}")
            base_filename = os.path.basename(filename)
            text_filename = os.path.splitext(base_filename)[0] + ".txt"
            text_file_path = os.path.join(self.new_folder_path, text_filename)
            with open(text_file_path, "w", encoding="utf-8") as text_file:
                text_file.write(generated_text)


if __name__ == "__main__":
    try:
        image = ImageToText('T_Sailor_Jupiter_test',
                            'Salesforce/blip-image-captioning-large',
                            'T_Sailor_Jupiter_test')
        list_of_image = image.read_images_from_folder()
        image.create_text_from_image()
    except ValueError as error:
        print("Erorr:", error)
