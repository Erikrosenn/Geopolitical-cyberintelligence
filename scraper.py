import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import re
import subprocess
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import hashlib
from transformers import pipeline
import warnings

# Set environment variable to suppress Git warnings
os.environ['SUPPRESS_HANDLE_INHERITANCE_WARNING'] = '1'

KEYWORDS = [
    "cyberattack", "ransomware", "malware", "hack", "espionage",
    "APT", "breach", "Russia", "Ukraine", "Iran", "China",
    "Lazarus", "NSA", "military", "DDoS", "North Korea", "cyber", "Europe", "European",
    "security", "vulnerability", "exploit", "phishing", "trojan", "botnet"
]


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none'
}


NEWS_SOURCES = {
    "thehackernews": {
        "url": "https://thehackernews.com/",
        "article_selectors": ["div.home-post-box", "div.pop-article", "div.clear"],
        "title_selectors": ["h2", "h3", "h1"],
        "link_selectors": ["a"],
        "content_selectors": ["div.articlebody", "div.post-body", "div.entry-content", ".content"],
        "base_url": "https://thehackernews.com"
    },
    "cyberscoop": {
        "url": "https://cyberscoop.com/",
        "article_selectors": ["article", "div.post", "div.article"],
        "title_selectors": ["h2", "h1", "h3"],
        "link_selectors": ["a"],
        "content_selectors": ["div.entry-content", "div.content", "div.post-content"],
        "base_url": "https://cyberscoop.com"
    },
}

# Global variables for lazy loading
_summarizer = None
_session = None

def get_session():
    """Lazy load requests session with connection pooling"""
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update(HEADERS)
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10, 
            pool_maxsize=20,
            max_retries=3
        )
        _session.mount('http://', adapter)
        _session.mount('https://', adapter)
    return _session

def get_summarizer():
    """Lazy load summarizer only when needed"""
    global _summarizer
    if _summarizer is None:
        try:
            print(" Loading summarization model (one-time setup)...")
            warnings.filterwarnings("ignore", category=FutureWarning)
            _summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            print(" Summarization model loaded")
        except ImportError as e:
            print(f" Transformers library issue: {e}")
            print(" Try: pip install --upgrade transformers torch")
            print(" Using simple text truncation instead")
            _summarizer = False
        except Exception as e:
            print(f" Could not load summarization model: {e}")
            print(" Using simple text truncation instead")
            _summarizer = False
    return _summarizer

@lru_cache(maxsize=100)
def get_article_hash(url):
    """Generate hash for URL to detect duplicates"""
    return hashlib.md5(url.encode()).hexdigest()[:8]

def load_processed_articles():
    """Load list of already processed articles"""
    cache_file = "processed_articles.json"
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_processed_articles(processed_set):
    """Save list of processed articles"""
    cache_file = "processed_articles.json"
    try:
        with open(cache_file, 'w') as f:
            json.dump(list(processed_set), f)
    except:
        pass

def simple_summarize(text, max_sentences=3):
    """Fast text summarization using sentence ranking"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if len(sentences) <= max_sentences:
        return text[:500] + "..." if len(text) > 500 else text
    
    scored_sentences = []
    for sentence in sentences[:10]:  
        score = sum(1 for keyword in KEYWORDS if keyword.lower() in sentence.lower())
        scored_sentences.append((score, sentence))
    
    
    scored_sentences.sort(key=lambda x: x[0], reverse=True)
    top_sentences = [s[1] for s in scored_sentences[:max_sentences]]
    
    return " ".join(top_sentences)

def clean_and_truncate_text(text, max_length=1500):
    """Clean and truncate text efficiently"""
    if not text:
        return ""
    text = ' '.join(text.split())
    return text[:max_length] if len(text) > max_length else text

def get_article_content(url, content_selectors, timeout=10):
    """Improved article content extraction with multiple selectors"""
    try:
        session = get_session()
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        
        article_div = None
        for selector in content_selectors:
            if selector.startswith('.'):
                article_div = soup.find(class_=selector[1:])
            elif selector.startswith('div.'):
                article_div = soup.find("div", class_=selector.replace("div.", ""))
            elif selector.startswith('div#'):
                article_div = soup.find("div", id=selector.replace("div#", ""))
            else:
                article_div = soup.select_one(selector)
            
            if article_div:
                break
        
        
        if not article_div:
            fallback_selectors = ["main", "article", ".content", ".post-content", ".entry-content"]
            for selector in fallback_selectors:
                if selector.startswith('.'):
                    article_div = soup.find(class_=selector[1:])
                else:
                    article_div = soup.find(selector)
                if article_div:
                    break
        
        if not article_div:
            return None
        
        
        paragraphs = article_div.find_all("p")
        if not paragraphs:
            text = article_div.get_text().strip()
            return text if len(text) > 100 else None
            
        full_text = "\n\n".join(p.get_text().strip() for p in paragraphs[:20] if p.get_text().strip())
        return full_text if len(full_text) > 100 else None
        
    except Exception as e:
        print(f" Error fetching {url}: {str(e)[:50]}...")
        return None

def summarize_text(text):
    """Smart summarization with fallback"""
    if not text or len(text.strip()) < 50:
        return "Article too short to summarize."
    
    summarizer = get_summarizer()
    
    if summarizer is False:
        return simple_summarize(text)
    
    try:
        cleaned_text = clean_and_truncate_text(text)
        summary = summarizer(cleaned_text, max_length=120, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f" Model summarization failed, using fallback: {str(e)[:30]}...")
        return simple_summarize(text)

def slugify(title):
    """Fast slugify function"""
    return re.sub(r'[^a-zA-Z0-9]+', '-', title.lower())[:50].strip('-')

def save_as_markdown(title, date_str, url, summary, full_content, source):
    """Optimized markdown saving"""
    try:
        os.makedirs(date_str, exist_ok=True)
        filename = f"{date_str}/{slugify(title)}.md"
        
        if os.path.exists(filename):
            return False
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"---\n"
                   f"title: \"{title}\"\n"
                   f"date: {date_str}\n"
                   f"source: {url}\n"
                   f"publisher: {source}\n"
                   f"tags: [cyber, geopolitics]\n"
                   f"---\n\n"
                   f"## TL;DR\n\n{summary}\n\n"
                   f"## Full Article\n\n{full_content}")
        
        return True
    except Exception as e:
        print(f" Error saving {title[:30]}...: {e}")
        return False

def debug_scraping(source_name, config):
    """Debug function to understand what's happening during scraping"""
    print(f"\n DEBUG: Scraping {source_name}...")
    
    try:
        session = get_session()
        response = session.get(config["url"], timeout=10)
        response.raise_for_status()
        print(f"✓ Successfully fetched {source_name} (Status: {response.status_code})")
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        articles_found = []
        for i, selector in enumerate(config["article_selectors"]):
            print(f"  Trying selector {i+1}: {selector}")
            
            if selector.startswith("div."):
                selector_class = selector.replace("div.", "")
                articles = soup.find_all("div", class_=selector_class)
            elif selector.startswith("article"):
                if "." in selector:
                    selector_class = selector.replace("article.", "")
                    articles = soup.find_all("article", class_=selector_class)
                else:
                    articles = soup.find_all("article")
            else:
                articles = soup.select(selector)
            
            print(f"    Found {len(articles)} elements")
            
            if articles:
                articles_found = articles
                print(f"    ✓ Using this selector")
                break
        
        if not articles_found:
            print("   No articles found with any selector, trying fallbacks...")
            articles_found = soup.find_all("article")[:15] or soup.find_all("div", class_="post")[:15]
            print(f"  Fallback found {len(articles_found)} articles")
        
        return articles_found, soup
        
    except Exception as e:
        print(f" Failed to fetch {source_name}: {e}")
        return [], None

def scrape_source(source_name, config, debug=False):
    """Improved source scraping with better debugging"""
    if debug:
        articles, soup = debug_scraping(source_name, config)
    else:
        print(f" Scraping {source_name}...")
        try:
            session = get_session()
            response = session.get(config["url"], timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f" Failed to fetch {source_name}: {e}")
            return []
        
        articles = []
        for selector in config["article_selectors"]:
            if selector.startswith("div."):
                selector_class = selector.replace("div.", "")
                articles = soup.find_all("div", class_=selector_class)
            elif selector.startswith("article"):
                if "." in selector:
                    selector_class = selector.replace("article.", "")
                    articles = soup.find_all("article", class_=selector_class)
                else:
                    articles = soup.find_all("article")
            else:
                articles = soup.select(selector)
            
            if articles:
                break
        
        if not articles:
            articles = soup.find_all("article")[:15] or soup.find_all("div", class_="post")[:15]
    
    print(f" Found {len(articles)} articles")
    
    articles_found = []
    processed_count = 0
    
    for article in articles[:15]:
        try:
            title_elem = None
            for title_selector in config["title_selectors"]:
                if title_selector.startswith("h"):
                    title_elem = article.find(title_selector)
                else:
                    title_elem = article.select_one(title_selector)
                if title_elem:
                    break
            
            link_elem = article.find("a")
            if not link_elem and title_elem:
                link_elem = title_elem.find("a") or title_elem.find_parent("a")
            
            if not title_elem or not link_elem:
                continue
                
            title = title_elem.get_text().strip()
            link = link_elem.get("href", "")
            
            if not title or not link:
                continue
            
            # Keyword check
            title_lower = title.lower()
            has_keyword = any(keyword.lower() in title_lower for keyword in KEYWORDS)
            
            if not has_keyword:
                content_snippet = ""
                snippet_elem = article.find("p") or article.find("div", class_="excerpt")
                if snippet_elem:
                    content_snippet = snippet_elem.get_text()[:200].lower()
                    has_keyword = any(keyword.lower() in content_snippet for keyword in KEYWORDS)
            
            if not has_keyword:
                continue
            
            # Fix relative URLs
            if link.startswith("/"):
                link = config["base_url"] + link
            elif not link.startswith("http"):
                link = f"{config['base_url']}/{link}"
            
            articles_found.append({
                "title": title,
                "link": link,
                "source": source_name,
                "content_selectors": config["content_selectors"]
            })
            
            processed_count += 1
            if debug:
                print(f"  ✓ Article {processed_count}: {title[:50]}...")
                
        except Exception as e:
            if debug:
                print(f" Error processing article: {e}")
            continue
    
    print(f"✓ Found {len(articles_found)} relevant articles from {source_name}")
    return articles_found

def process_article(article, processed_articles):
    """Process a single article (for parallel processing) - FIXED VERSION"""
    url_hash = get_article_hash(article['link'])
    if url_hash in processed_articles:
        return None
    
    content = get_article_content(article['link'], article['content_selectors'])
    if not content:
        return None
    
    # Only try to summarize if we have enough content
    if len(content.strip()) > 200:
        summary = summarize_text(content)
    else:
        summary = content[:200] + "..." if len(content) > 200 else content
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    if save_as_markdown(article['title'], today, article['link'], summary, content, article['source']):
        processed_articles.add(url_hash)
        # FIXED: Return all necessary data including the link
        return {
            'title': article['title'],
            'source': article['source'],
            'link': article['link'],  
            'summary': summary
        }
    return None

def save_tldr_digest(tldr_list, date_str):
    """Save all TLDRs into a daily digest markdown file - FIXED VERSION"""
    try:
        os.makedirs(date_str, exist_ok=True)
        digest_path = os.path.join(date_str, f"{date_str}_TLDR.md")
        with open(digest_path, "w", encoding="utf-8") as f:
            f.write(f"# 📰 {date_str} CyberIntel TL;DR Digest\n\n")
            f.write(f"*Auto-generated cybersecurity news digest*\n\n")
            
            if not tldr_list:
                f.write("No new articles found today.\n\n")
            else:
                for i, entry in enumerate(tldr_list, 1):
                    f.write(f"## {i}. {entry['title']}\n\n")
                    f.write(f"**Source:** {entry['source']}\n\n")
                    f.write(f"**TL;DR:** {entry['summary']}\n\n")
                    f.write(f"[🔗 Read full article]({entry['link']})\n\n")
                    f.write("---\n\n")
                    
        print(f" Saved daily TL;DR digest with {len(tldr_list)} articles: {digest_path}")
    except Exception as e:
        print(f" Failed to save TL;DR digest: {e}")

def git_push():
    """Optimized git operations"""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        
        
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True, timeout=10)
        if not result.stdout.strip():
            print(" No changes to commit")
            return
        
        subprocess.run(["git", "add", today], check=True, timeout=10)
        subprocess.run(["git", "commit", "-m", f"Auto-update {today}"], 
                      check=True, timeout=15)
        subprocess.run(["git", "push", "origin", "main"], check=True, timeout=30)
        print(" Pushed to GitHub")
        
    except subprocess.TimeoutExpired:
        print(" Git operation timed out")
    except subprocess.CalledProcessError as e:
        print(f" Git operation failed: {e}")

def main(debug=False):
    """FIXED main function"""
    print(" Starting improved cybersecurity news scraper...")
    get_summarizer()
    start_time = time.time()
    
    processed_articles = load_processed_articles()
    
    all_articles = []
    if debug:
        for name, config in NEWS_SOURCES.items():
            articles = scrape_source(name, config, debug=True)
            all_articles.extend(articles)
    else:
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_source = {
                executor.submit(scrape_source, name, config): name 
                for name, config in NEWS_SOURCES.items()
            }
            
            for future in as_completed(future_to_source):
                articles = future.result()
                all_articles.extend(articles)
    
    scrape_time = time.time()
    print(f" Found {len(all_articles)} relevant articles in {scrape_time - start_time:.1f}s")
    
    if not all_articles:
        print(" No new articles found")
        today = datetime.now().strftime("%Y-%m-%d")
        save_tldr_digest([], today)
        return
    
    successful_saves = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(process_article, article, processed_articles)
            for article in all_articles
        ]
        
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            if result:
                successful_saves.append(result)
                print(f"[{i}/{len(all_articles)}] {result['source']}: {result['title'][:50]}...")
            else:
                print(f"[{i}/{len(all_articles)}] Skipped article")
    
    # FIXED: Save processed articles cache AFTER processing
    save_processed_articles(processed_articles)
    
    total_time = time.time() - start_time
    print(f"\n - SUMMARY ({total_time:.1f}s total):")
    print(f"   - Sources: {len(NEWS_SOURCES)}")
    print(f"   - Articles found: {len(all_articles)}")
    print(f"   - Successfully saved: {len(successful_saves)}")
    
    today = datetime.now().strftime("%Y-%m-%d")
    save_tldr_digest(successful_saves, today)
    
    if successful_saves:
        print("\n Pushing to GitHub...")
        git_push()
    else:
        print("\n No new articles saved, but digest created")

if __name__ == "__main__":
    import sys
    debug_mode = "--debug" in sys.argv
    main(debug=debug_mode)