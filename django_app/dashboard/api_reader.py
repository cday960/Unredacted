import os
from dotenv import load_dotenv
import markdown


load_dotenv()


API_INFO_PATH = str(os.getenv("API_INFO_PATH"))
print(f"API info path: {API_INFO_PATH}")


def get_endpoint_html():
    html_content = None
    with open(API_INFO_PATH, 'r') as api_file:
        md_content = api_file.read()
        html_content = markdown.markdown(md_content, output_format='html')
    return html_content
