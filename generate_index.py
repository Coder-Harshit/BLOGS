import os
import json
import frontmatter
import hashlib
from datetime import datetime

BLOGS_DIR = "blog"
INDEX_FILE = "index.json"


def compute_file_hash(filepath):
    """Compute SHA256 hash of a file"""
    hsh = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8*1024):
            hsh.update(chunk)
    return hsh.hexdigest()


def generate_index():
    posts = []

    old_indx = {}
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="UTF-8") as f:
            try:
                old_indx = {entry["slug"]:entry for entry in json.load(f)}
            except json.JSONDecodeError:
                old_indx={}
    
    for filename in os.listdir(BLOGS_DIR):
        if filename.endswith(".md"):
            # its a blog
            filepath = os.path.join(BLOGS_DIR,filename)
            post = frontmatter.load(filepath)
            file_hash = compute_file_hash(filepath)
            slug = filename.rsplit(".",1)[0] #removing the extension

            posts.append({
                "slug": slug,
                "title": post.get("title","Untitled"),
                "date": post.get("date",str(datetime.now()).split(" ")[0]),
                "tags": post.get("tags",[]),
                "summary": post.get("summary",""),
                "hash": file_hash            
            })

            # SORTING: NEWEST FIRST
            posts.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)

            with open(INDEX_FILE,"w",encoding="utf-8") as file:
                json.dump(posts, file, indent=2)

            # Detect changes (new, updated, removed)
            new_posts = []
            updated_posts = []
            removed_posts = []

            current_slugs = {p["slug"] for p in posts}
            old_slugs = set(old_indx.keys())

            for p in posts:
                if p["slug"] not in old_indx:
                    new_posts.append(p["slug"])
                elif p["hash"] != old_indx[p["slug"]]["hash"]:
                    updated_posts.append(p["slug"])

            removed_posts = list(old_slugs - current_slugs)

            print("✅ index.json updated")
            if new_posts:
                print(f"🆕 New posts: {new_posts}")
            if updated_posts:
                print(f"✏️ Updated posts: {updated_posts}")
            if removed_posts:
                print(f"❌ Removed posts: {removed_posts}")


if __name__ == "__main__":
    generate_index()