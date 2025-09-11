import os
import json
import shutil
import frontmatter
import markdown
import jinja2
from datetime import datetime
from pathlib import Path

# CONFIGS
BLOGS_DIR = "blog"
OUTPUT_DIR = "dist"
TEMPLATES_DIR = "templates"
STATIC_DIR = "static"
INDEX_FILE = "index.json"

class BlogGenerator:
    def __init__(self):
        self.posts = []
        self.changed_posts = []
        self.removed_posts = []
        self.template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(TEMPLATES_DIR)
        )

    def load_old_indx(self):
        """Load previous index to detect changes"""
        old_indx_file = "index.json.old"
        if os.path.exists(old_indx_file):
            with open(old_indx_file, "r", encoding="utf-8") as f:
                try:
                    return {entry["slug"]: entry for entry in json.load(f)}
                except json.JSONDecodeError:
                    return {}
        return {}

    def build_incremental(self):
        """Build only changed posts"""
        print("🔄 Starting incremental build...")

        # Load current posts from index
        if not os.path.exists(INDEX_FILE):
            print("❌ index.json not found. Run generate_index.py first!")
            return

        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            posts_data = json.load(f)
        
        # Load old index for comparison
        old_indx = self.load_old_indx()

        # Find what changed
        current_slugs = {post["slug"] for post in posts_data}
        old_slugs = set(old_indx.keys())

        new_posts = []
        updated_posts = []

        for post_data in posts_data:
            slug = post_data["slug"]
            if slug not in old_indx:
                new_posts.append(slug)
                self.changed_posts.append(post_data)
            elif post_data["hash"] != old_indx[slug]["hash"]:
                updated_posts.append(slug)
                self.changed_posts.append(post_data)

        self.removed_posts = list(old_slugs - current_slugs)

        # Create output directory if it doesn't exist
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Build changed posts
        if self.changed_posts:
            print(f"📝 Building {len(self.changed_posts)} changed posts...")
            for post_data in self.changed_posts:
                self.build_post(post_data)
        else:
            print("⚡ No posts changed, skipping post builds")

        # Remove deleted posts
        if self.removed_posts:
            print(f"🗑️  Removing {len(self.removed_posts)} deleted posts...")
            for slug in self.removed_posts:
                post_file = os.path.join(OUTPUT_DIR, f"{slug}.html")
                if os.path.exists(post_file):
                    os.remove(post_file)

        # Always rebuild index page (it's fast and shows all posts)
        self.build_index_page(posts_data)

        # Copy static files if they don't exist or are newer
        self.copy_static_files()

        # Save current index as old index for next run
        if os.path.exists(INDEX_FILE):
            shutil.copy(INDEX_FILE, "index.json.old")

        print(f"✅ Incremental build complete!")
        print(f"   📊 New: {len(new_posts)}, Updated: {len(updated_posts)}, Removed: {len(self.removed_posts)}")

        return {
            "new": len(new_posts),
            "updated": len(updated_posts), 
            "removed": len(self.removed_posts),
            "total": len(posts_data)
        }

    def build_full(self):
        """Build all posts from scratch"""
        print("🔄 Starting full build...")

        # Load posts from index
        if not os.path.exists(INDEX_FILE):
            print("❌ index.json not found. Run generate_index.py first!")
            return

        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            posts_data = json.load(f)


        # Clear output directory
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)
        os.makedirs(OUTPUT_DIR)

        # Build all posts
        print(f"📝 Building {len(posts_data)} posts...")
        for post_data in posts_data:
            self.build_post(post_data)

        # Build index page
        self.build_index_page(posts_data)

        # Copy static files
        self.copy_static_files()

        # Save current index as old index
        if os.path.exists(INDEX_FILE):
            shutil.copy(INDEX_FILE, "index.json.old")

        print(f"✅ Full build complete! Built {len(posts_data)} posts.")

        return {"total": len(posts_data), "type": "full"}

    def build_post(self, post_data):
        """Build individual post"""
        slug = post_data["slug"]
        filepath = os.path.join(BLOGS_DIR, f"{slug}.md")

        if not os.path.exists(filepath):
            print(f"⚠️  Warning: {filepath} not found, skipping")
            return

        # Load and parse markdown
        post = frontmatter.load(filepath)

        # Convert markdown to HTML with extensions
        html_content = markdown.markdown(
            post.content,
            extensions=[
                'codehilite',
                'fenced_code', 
                'toc',
                'tables',
                'attr_list'
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'use_pygments': True
                }
            }
        )

        # Render template
        template = self.template_env.get_template("post.html")
        html = template.render(
            title=post_data["title"],
            date=post_data["date"],
            tags=post_data["tags"],
            content=html_content,
            summary=post_data["summary"],
            current_year=datetime.now().year
        )

        # Write output file
        output_file = os.path.join(OUTPUT_DIR, f"{slug}.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"   ✓ Built {slug}.html")

    def build_index_page(self, posts_data):
        """Build the main index page"""
        template = self.template_env.get_template("index.html")
        html = template.render(
            posts=posts_data,
            current_year=datetime.now().year
        )

        with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)

        print("   ✓ Built index.html")

    def copy_static_files(self):
        """Copy static assets"""
        if os.path.exists(STATIC_DIR):
            static_output = os.path.join(OUTPUT_DIR, "static")
            if os.path.exists(static_output):
                shutil.rmtree(static_output)
            shutil.copytree(STATIC_DIR, static_output)
            print("   ✓ Copied static files")
        else:
            print("   ℹ️  No static directory found, skipping")

def main():
    import sys

    generator = BlogGenerator()

    if len(sys.argv) > 1 and sys.argv[1] == "full":
        result = generator.build_full()
    else:
        result = generator.build_incremental()

    if result:
        print(f"\n🎉 Build completed successfully!")
        if "total" in result:
            print(f"📊 Total posts: {result['total']}")

if __name__ == "__main__":
    main()
