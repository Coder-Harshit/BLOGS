import os
import json
import frontmatter
from datetime import datetime

BLOGS_DIR = "blog"
INDEX_FILE = "index.json"


def generate_index():
    posts = []

    for filename in os.listdir(BLOGS_DIR):
        if filename.endswith(".md"):
            # its a blog
            filepath = os.path.join(BLOGS_DIR,filename)
            with open(filepath,"r",encoding="UTF-8") as file:
                post = frontmatter.load(file)

            posts.append({
                "slug": filename.split(".")[0], #removing the extension
                "title": post.get("title","Untitled"),
                "date": post.get("date",str(datetime.now()).split(" ")[0]),
                "tags": post.get("tags",[]),
                "summary": post.get("summary","")
            })

            posts.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True) #sorting (newest first)

            with open(INDEX_FILE,"w",encoding="utf-8") as file:
                json.dump(posts, file, indent=2)

            print(f"✅ `index.json` generated with {len(posts)} posts")

if __name__=='__main__':
    generate_index()