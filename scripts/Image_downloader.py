"""Download images from choosen gallery."""
import os

import bs4
import io
import PIL
import urllib


class DownloadImage:
    """
    Using this class you can download images from online gallery.

    You can download images from: Danbooru, Gelbooru and Safebooru.
    """

    def __init__(self, tags: str, panel_of_image: str, individual_image: str):
        self.tags = tags
        self.list_of_urls = []
        self.panel_of_image = panel_of_image
        self.individual_image = individual_image

    @property
    def description_image_with_tags(self) -> str:
        """Set tags."""
        return self._tags

    @description_image_with_tags.setter
    def description_image_with_tags(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("The tags to the images must be a string.")
        self._tags = value

    @description_image_with_tags.deleter
    def description_image_with_tags(self) -> None:
        del self._tags

    @property
    def description_image_panel(self) -> str:
        """Set panel indicators."""
        return self._panel_of_image

    @description_image_panel.setter
    def description_image_panel(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("The panel indicators must be a string.")
        self._panel_of_image = value

    @description_image_panel.deleter
    def description_image_panel(self) -> None:
        del self._panel_of_image

    @property
    def description_individual_image(self) -> str:
        """Set indicators of individual image."""
        return self._individual_image

    @description_individual_image.setter
    def description_individual_image(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("The individual image must be a string.")
        self._individual_image = value

    @description_individual_image.deleter
    def description_individual_image(self) -> None:
        del self._individual_image

    def fill_list_of_urls(self, number_of_page: int,
                          chosen_gallery: str) -> list[str]:
        """List of images links."""
        if chosen_gallery == 'Gelbooru':
            return [f'https://gelbooru.com/index.php?page=post&s=list&tags={self.tags}%pid={index}'
                    for index in range(0, number_of_page, 42)]
        elif chosen_gallery == 'Safebooru':
            return [f'https://safebooru.org/index.php?page=post&s=list&tags={self.tags}&pid={index}'
                    for index in range(0, number_of_page, 42)]
        elif chosen_gallery == 'Danbooru':
            return [f'https://danbooru.donmai.us/posts?page={index}&tags={self.tags}'
                    for index in range(number_of_page)][1:]

    def download_and_save_images(self, amount_of_pages: int, save_path: str,
                                 chosen_gallery: str) -> None:
        """Download images."""
        counter: int = 0
        list_of_urls = self.fill_list_of_urls(amount_of_pages, chosen_gallery)
        for item in list_of_urls:
            page = urllib.request.urlopen(item)
            page_soup = bs4.BeautifulSoup(page, 'html.parser')
            img_items = page_soup.find('div',
                                       {"class": f"{self.panel_of_image}"})
            img_div = img_items.find_all(class_=f"{self.individual_image}")
            for img in img_div:
                post_link_tag = img.find('a')
                if not post_link_tag:
                    continue
                post_href = post_link_tag.get('href')
                if chosen_gallery == 'Safebooru':
                    full_post_url = f"https://safebooru.org/{post_href}"
                elif chosen_gallery == 'Gelbooru':
                    full_post_url = f"https://gelbooru.org/{post_href}"
                elif chosen_gallery == 'Danbooru':
                    full_post_url = f"https://danbooru.org/{post_href}"
                post_page = urllib.request.urlopen(full_post_url)
                post_soup = bs4.BeautifulSoup(post_page, 'html.parser')
                full_img_tag = post_soup.find('img', id='image')
                if not full_img_tag:
                    continue
                full_img_url = full_img_tag.get('src')
                file_name = str(counter)
                if not os.path.isdir(save_path):
                    try:
                        os.makedirs(save_path, exist_ok=True)
                        print(f"Folder '{save_path}' was created automatically.")
                    except Exception as e:
                        raise ValueError(f"Failed to create folder '{save_path}': {e}")
                complete_path = os.path.join(save_path, file_name + ".jpeg")
                image_data = urllib.request.urlopen(full_img_url).read()
                image = PIL.Image.open(io.BytesIO(image_data))
                if image.mode != "RGB":
                    image = image.convert("RGB")
                image.save(complete_path, "JPEG")
                counter += 1
