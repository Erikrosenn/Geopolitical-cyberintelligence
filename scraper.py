import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import os
from datetime import datetime
import re
import subprocess
import time

KEYWORDS = [
    "cyberattack", "ransomware", "malware", "hack", "espionage",
    "APT", "breach", "Russia", "Ukraine", "Iran", "China",
    "Lazarus", "NSA", "military", "DDoS", "North Korea", "cyber", "Europe", "European"
]

def get_article_content(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # The article text lives inside a <div class="articlebody">
        article_div = soup.find("div", class_="articlebody")
        if not article_div:
            return "Could not extract article content."
        
        # Grab all paragraph tags within the article body
        paragraphs = article_div.find_all("p")
        # Combine all paragraphs into one string
        full_text = "\n\n".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
        
        return full_text if full_text else "No content found."
    except Exception as e:
        print(f"Error fetching article content: {e}")
        return "Could not extract article content due to error."

# Load once at the top of your script
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    print("✓ Summarization model loaded successfully")
except Exception as e:
    print(f"Error loading summarization model: {e}")
    summarizer = None

def summarize_text(text):
    if not summarizer:
        return "Summary unavailable - model failed to load."
    
    try:
        # HuggingFace models max out at ~1024 tokens, so trim long articles
        if len(text) > 3000:
            text = text[:3000]
        
        if len(text.strip()) < 50:
            return "Article too short to summarize."
        
        summary = summarizer(text, max_length=150, min_length=40, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error during summarization: {e}")
        return "Summary generation failed."

def slugify(title):
    return re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')

def save_as_markdown(title, date_str, url, summary, full_content):
    try:
        filename = f"{date_str}/{slugify(title)}.md"
        os.makedirs(date_str, exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"---\n")
            f.write(f"title: \"{title}\"\n")
            f.write(f"date: {date_str}\n")
            f.write(f"source: {url}\n")
            f.write(f"tags: [cyber, geopolitics]\n")
            f.write(f"---\n\n")
            f.write(f"## TL;DR\n\n{summary}\n\n")
            f.write(f"## Full Article\n\n{full_content}")
        
        print(f"✓ Blog post saved: {filename}")
        return True
    except Exception as e:
        print(f"Error saving markdown file: {e}")
        return False

def git_push():
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"📰 Auto-update {datetime.now().strftime('%Y-%m-%d %H:%M')}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Blog posts pushed to GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git push failed: {e}")
        print("Make sure you're authenticated and have changes to commit.")

def main():
    url = "https://thehackernews.com/"
    
    try:
        print("🔍 Fetching articles from The Hacker News...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"❌ Failed to fetch main page: {e}")
        return
    
    # Try different possible selectors for article containers
    articles = soup.find_all("div", class_="body-post clear")
    if not articles:
        # Fallback selectors in case the site structure changed
        articles = soup.find_all("div", class_="body-post")
        if not articles:
            articles = soup.find_all("article")
    
    if not articles:
        print("❌ No articles found. The website structure may have changed.")
        return
    
    print(f"📄 Found {len(articles)} articles to check")
    
    matched_articles = 0
    saved_articles = 0
    
    for i, article in enumerate(articles):
        try:
            # Try different ways to find title and link
            title_elem = article.find("h2") or article.find("h1") or article.find("h3")
            link_elem = article.find("a")
            
            if not title_elem or not link_elem:
                continue
                
            title = title_elem.text.strip()
            link = link_elem.get("href", "")
            
            # Make sure link is absolute
            if link.startswith("/"):
                link = "https://thehackernews.com" + link
            
            if any(keyword.lower() in title.lower() for keyword in KEYWORDS):
                matched_articles += 1
                print(f"\n🎯 MATCH FOUND ({matched_articles})")
                print(f"TITLE: {title}")
                print(f"LINK: {link}")
                
                content = get_article_content(link)
                
                if content and content != "Could not extract article content.":
                    summary = summarize_text(content)
                    today = datetime.now().strftime("%Y-%m-%d")
                    
                    if save_as_markdown(title, today, link, summary, content):
                        saved_articles += 1
                        print(f"💾 TL;DR: {summary}")
                    
                    # Add small delay to be respectful
                    time.sleep(1)
                else:
                    print("⚠️ Could not extract article content")
                
                print("=" * 80)
            else:
                print(f"⏭️ Skipped: {title[:50]}..." if len(title) > 50 else f"⏭️ Skipped: {title}")
                
        except Exception as e:
            print(f"❌ Error processing article {i}: {e}")
            continue
    
    print(f"\n📊 Summary:")
    print(f"   - Articles checked: {len(articles)}")
    print(f"   - Keyword matches: {matched_articles}")
    print(f"   - Successfully saved: {saved_articles}")
    
    if saved_articles > 0:
        print("\n🚀 Pushing to GitHub...")
        git_push()
    else:
        print("\n📝 No articles saved, skipping git push.")

if __name__ == "__main__":
    main()