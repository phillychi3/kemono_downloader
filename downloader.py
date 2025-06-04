import requests
import zipfile
import fake_useragent
from progress.bar import IncrementalBar
import time
from pathlib import Path
from argparse import ArgumentParser


class KemonoDownloader:
    def __init__(self):
        self.ua = fake_useragent.UserAgent()
        self.headers = {"user-agent": self.ua.random}
        self.base_url = "https://kemono.su"
        self.api_base = "https://kemono.su/api/v1"
        self.delay = 1

    def parse_user_url(self, url):
        parts = url.replace(self.base_url, "").strip("/").split("/")
        if len(parts) >= 3 and parts[1] == "user":
            service = parts[0]
            user_id = parts[2]
            return service, user_id
        return None, None

    def parse_post_url(self, url):
        parts = url.replace(self.base_url, "").strip("/").split("/")
        if len(parts) >= 5 and parts[1] == "user" and parts[3] == "post":
            service = parts[0]
            user_id = parts[2]
            post_id = parts[4]
            return service, user_id, post_id
        return None, None, None

    def clean_filename(self, filename):
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, "")
        return filename.replace("\n", "").replace("\u3000", "").strip()

    def fetch_user_posts(self, service, user_id):
        api_url = f"{self.api_base}/{service}/user/{user_id}/posts-legacy"

        try:
            response = requests.get(api_url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API request failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"Request error: {e}")
            return None

    def fetch_post(self, service, user_id, post_id):
        api_url = f"{self.api_base}/{service}/user/{user_id}/post/{post_id}"

        try:
            response = requests.get(api_url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API request failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"Request error: {e}")
            return None

    def download_file(self, url, file_path):
        try:
            response = requests.get(url, headers=self.headers, stream=True)
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return True
            else:
                print(f"Download failed: {url} (status code: {response.status_code})")
                return False
        except Exception as e:
            print(f"Download error {url}: {e}")
            return False

    def download_posts(self, posts, folder, iszip, user_name=None):
        if not posts:
            print("No posts found")
            return

        if folder is False:
            if user_name:
                download_path = Path("downloads") / self.clean_filename(user_name)
            else:
                download_path = Path("downloads") / "unknown_user"
            download_path.mkdir(parents=True, exist_ok=True)
        else:
            download_path = Path(folder)

        for post in posts:
            post_title = self.clean_filename(post.get("title", "Untitled"))
            print(f"Processing post: {post_title}")

            zip_path = download_path / f"{post_title}.zip"
            folder_path = download_path / post_title

            if zip_path.exists() or folder_path.exists():
                print(f"{post_title} already exists, skipping")
                continue

            attachments = post.get("attachments", [])
            file_info = post.get("file", {})

            if not attachments and not file_info:
                print(f"{post_title} has no downloadable content")
                continue

            download_items = []

            for index, attachment in enumerate(attachments):
                if attachment.get("path"):
                    url = self.base_url + attachment["path"]
                    filename = attachment.get("name", attachment["path"].split("/")[-1])
                    download_items.append((url, filename))

            if file_info and file_info.get("path"):
                url = self.base_url + file_info["path"]
                filename = file_info.get("name", file_info["path"].split("/")[-1])
                download_items.append((url, filename))

            if not download_items:
                continue

            with IncrementalBar(
                f"Downloading {post_title}", max=len(download_items)
            ) as bar:
                if iszip:
                    with zipfile.ZipFile(zip_path, "w") as zf:
                        for url, filename in download_items:
                            try:
                                response = requests.get(url, headers=self.headers)
                                if response.status_code == 200:
                                    zf.writestr(filename, response.content)
                                else:
                                    print(f"Download failed: {filename}")
                            except Exception as e:
                                print(f"Download error {filename}: {e}")

                            bar.next()
                            time.sleep(self.delay)
                else:
                    folder_path.mkdir(exist_ok=True)
                    for url, filename in download_items:
                        file_path = folder_path / filename
                        self.download_file(url, file_path)
                        bar.next()
                        time.sleep(self.delay)

            print(f"Completed: {post_title}")

    def download_all(self, url, folder, iszip):
        service, user_id = self.parse_user_url(url)
        if not service or not user_id:
            print("Invalid URL format")
            return

        print(f"Fetching posts for {service} user {user_id}...")
        posts = self.fetch_user_posts(service, user_id)

        if not posts:
            print("Unable to fetch post data")
            return

        user_name = posts["props"]["artist"]["name"]

        self.download_posts(posts["results"], folder, iszip, user_name)
        print("All completed")

    def download_one(self, url, folder, iszip):
        service, user_id, post_id = self.parse_post_url(url)
        if not service or not user_id or not post_id:
            print("Invalid URL format")
            return

        print(f"Fetching {service} post {post_id}...")
        post = self.fetch_post(service, user_id, post_id)

        if not post:
            print("Unable to fetch post data")
            return

        self.download_posts([post], folder, iszip)
        print("Download completed")


def main():
    parser = ArgumentParser()
    parser.add_argument("url", help="Kemono URL")
    parser.add_argument("-z", "--zip", help="Save as ZIP file", action="store_true")
    parser.add_argument("-f", "--folder", help="Download folder", default=False)
    parser.add_argument(
        "-d", "--delay", help="Request delay (seconds)", type=float, default=1.0
    )
    args = parser.parse_args()

    if args.folder is False:
        Path("downloads").mkdir(exist_ok=True)

    downloader = KemonoDownloader()
    downloader.delay = args.delay

    if "post" in args.url:
        downloader.download_one(args.url, args.folder, args.zip)
    else:
        downloader.download_all(args.url, args.folder, args.zip)


if __name__ == "__main__":
    main()
