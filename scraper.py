import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta
import re
import subprocess
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import hashlib
from transformers import pipeline
import warnings
import shutil
from pathlib import Path

# Set environment variable to suppress Git warnings
os.environ['SUPPRESS_HANDLE_INHERITANCE_WARNING'] = '1'

KEYWORDS = [
    "cyberattack", "ransomware", "malware", "hack", "espionage",
    "APT", "breach", "Russia", "Ukraine", "Iran", "China",
    "Lazarus", "NSA", "military", "DDoS", "North Korea", "cyber", "Europe", "European",
    "security", "vulnerability", "exploit", "phishing", "trojan", "botnet", "NATO"
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

class HierarchicalOrganizer:
    """Manages hierarchical folder organization: Year/Month/Week/Day"""
    
    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.org_config_file = self.base_path / "organization_config.json"
        self.load_config()
    
    def load_config(self):
        """Load organization configuration"""
        if self.org_config_file.exists():
            try:
                with open(self.org_config_file, 'r') as f:
                    self.config = json.load(f)
            except:
                self.config = {}
        else:
            self.config = {}
        
        # Default config
        self.config.setdefault('days_per_week', 7)
        self.config.setdefault('weeks_per_month', 4)
        self.config.setdefault('created_weeks', {})
        self.config.setdefault('created_months', {})
    
    def save_config(self):
        """Save organization configuration"""
        try:
            with open(self.org_config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except:
            pass
    
    def get_week_number(self, date):
        """Get week number within the year"""
        return date.isocalendar()[1]
    
    def get_current_paths(self, date=None):
        """Get current hierarchical paths"""
        if date is None:
            date = datetime.now()
        
        year = date.strftime("%Y")
        month = date.strftime("%Y-%m")
        week = f"{year}-W{self.get_week_number(date):02d}"
        day = date.strftime("%Y-%m-%d")
        
        return {
            'year': year,
            'month': month,
            'week': week,
            'day': day,
            'year_path': self.base_path / year,
            'month_path': self.base_path / year / month,
            'week_path': self.base_path / year / month / week,
            'day_path': self.base_path / year / month / week / day
        }
    
    def get_storage_path(self, date=None):
        """Get the current storage path for new articles"""
        paths = self.get_current_paths(date)
        
        # Check if we need to reorganize
        self.check_and_reorganize()
        
        # Ensure current day path exists
        paths['day_path'].mkdir(parents=True, exist_ok=True)
        
        return str(paths['day_path'])
    
    def count_days_in_current_week(self, week_path):
        """Count days in current week"""
        if not week_path.exists():
            return 0
        
        day_count = 0
        for item in week_path.iterdir():
            if item.is_dir() and re.match(r'\d{4}-\d{2}-\d{2}', item.name):
                day_count += 1
        return day_count
    
    def count_weeks_in_current_month(self, month_path):
        """Count weeks in current month"""
        if not month_path.exists():
            return 0
        
        week_count = 0
        for item in month_path.iterdir():
            if item.is_dir() and re.match(r'\d{4}-W\d{2}', item.name):
                week_count += 1
        return week_count
    
    def create_week_summary(self, week_path):
        """Create a weekly summary from all daily TLDRs"""
        try:
            weekly_articles = []
            
            for day_dir in week_path.iterdir():
                if not day_dir.is_dir():
                    continue
                
                tldr_file = day_dir / f"{day_dir.name}_TLDR.md"
                if tldr_file.exists():
                    with open(tldr_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Extract articles from daily TLDR
                        articles = self.extract_articles_from_tldr(content, day_dir.name)
                        weekly_articles.extend(articles)
            
            if weekly_articles:
                week_summary_path = week_path / f"{week_path.name}_WEEKLY_SUMMARY.md"
                with open(week_summary_path, 'w', encoding='utf-8') as f:
                    f.write(f"# 📅 {week_path.name} Weekly CyberIntel Summary\n\n")
                    f.write(f"*Weekly compilation of {len(weekly_articles)} cybersecurity articles*\n\n")
                    
                    # Group by day
                    by_day = {}
                    for article in weekly_articles:
                        day = article['day']
                        if day not in by_day:
                            by_day[day] = []
                        by_day[day].append(article)
                    
                    for day in sorted(by_day.keys()):
                        f.write(f"## {day}\n\n")
                        for i, article in enumerate(by_day[day], 1):
                            f.write(f"### {i}. {article['title']}\n")
                            f.write(f"**Source:** {article['source']}\n")
                            f.write(f"**Summary:** {article['summary']}\n")
                            f.write(f"[🔗 Read more]({article['link']})\n\n")
                        f.write("---\n\n")
                
                print(f" Created weekly summary: {week_summary_path}")
                return True
        except Exception as e:
            print(f" Failed to create weekly summary: {e}")
            return False
    
    def create_month_summary(self, month_path):
        """Create a monthly summary from all weekly summaries"""
        try:
            monthly_stats = {
                'total_articles': 0,
                'sources': set(),
                'weeks': []
            }
            
            for week_dir in month_path.iterdir():
                if not week_dir.is_dir() or not week_dir.name.startswith(month_path.parent.name):
                    continue
                
                week_summary = week_dir / f"{week_dir.name}_WEEKLY_SUMMARY.md"
                if week_summary.exists():
                    with open(week_summary, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Count articles and sources
                        article_count = content.count('### ')
                        sources = re.findall(r'\*\*Source:\*\* ([^\n]+)', content)
                        
                        monthly_stats['total_articles'] += article_count
                        monthly_stats['sources'].update(sources)
                        monthly_stats['weeks'].append({
                            'week': week_dir.name,
                            'articles': article_count
                        })
            
            if monthly_stats['total_articles'] > 0:
                month_summary_path = month_path / f"{month_path.name}_MONTHLY_SUMMARY.md"
                with open(month_summary_path, 'w', encoding='utf-8') as f:
                    f.write(f"# 📊 {month_path.name} Monthly CyberIntel Report\n\n")
                    f.write(f"## Summary Statistics\n\n")
                    f.write(f"- **Total Articles:** {monthly_stats['total_articles']}\n")
                    f.write(f"- **Unique Sources:** {len(monthly_stats['sources'])}\n")
                    f.write(f"- **Weeks Covered:** {len(monthly_stats['weeks'])}\n\n")
                    
                    f.write(f"## Weekly Breakdown\n\n")
                    for week_data in monthly_stats['weeks']:
                        f.write(f"- **{week_data['week']}:** {week_data['articles']} articles\n")
                    
                    f.write(f"\n## Sources\n\n")
                    for source in sorted(monthly_stats['sources']):
                        f.write(f"- {source}\n")
                    
                    f.write(f"\n---\n*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
                
                print(f" Created monthly summary: {month_summary_path}")
                return True
        except Exception as e:
            print(f" Failed to create monthly summary: {e}")
            return False
    
    def extract_articles_from_tldr(self, content, day):
        """Extract article information from TLDR content"""
        articles = []
        
        # Split by article sections
        sections = re.split(r'## \d+\.', content)[1:]  # Skip the header
        
        for section in sections:
            try:
                lines = section.strip().split('\n')
                title = lines[0].strip()
                
                source = ""
                summary = ""
                link = ""
                
                for line in lines:
                    if line.startswith('**Source:**'):
                        source = line.replace('**Source:**', '').strip()
                    elif line.startswith('**TL;DR:**'):
                        summary = line.replace('**TL;DR:**', '').strip()
                    elif line.startswith('[🔗'):
                        link_match = re.search(r'\((.*?)\)', line)
                        if link_match:
                            link = link_match.group(1)
                
                if title and source and summary:
                    articles.append({
                        'title': title,
                        'source': source,
                        'summary': summary,
                        'link': link,
                        'day': day
                    })
            except:
                continue
        
        return articles
    
    def check_and_reorganize(self):
        """Check if reorganization is needed and perform it"""
        paths = self.get_current_paths()
        
        # Check if we need to create a weekly folder
        if paths['week_path'].exists():
            day_count = self.count_days_in_current_week(paths['week_path'])
            
            # If we have 7 days, create weekly summary
            if day_count >= self.config['days_per_week']:
                week_key = paths['week']
                if week_key not in self.config['created_weeks']:
                    if self.create_week_summary(paths['week_path']):
                        self.config['created_weeks'][week_key] = True
                        print(f" Week {paths['week']} completed with {day_count} days")
        
        # Check if we need to create a monthly folder
        if paths['month_path'].exists():
            week_count = self.count_weeks_in_current_month(paths['month_path'])
            
            # If we have 4+ weeks, create monthly summary
            if week_count >= self.config['weeks_per_month']:
                month_key = paths['month']
                if month_key not in self.config['created_months']:
                    if self.create_month_summary(paths['month_path']):
                        self.config['created_months'][month_key] = True
                        print(f"📊 Month {paths['month']} completed with {week_count} weeks")
        
        self.save_config()
    
    def get_legacy_daily_folders(self):
        """Find all legacy daily folders (YYYY-MM-DD format) in root"""
        legacy_folders = []
        
        for item in self.base_path.iterdir():
            if item.is_dir() and re.match(r'\d{4}-\d{2}-\d{2}', item.name):
                legacy_folders.append(item)
        
        return legacy_folders
    
    def migrate_legacy_structure(self):
        """Migrate existing YYYY-MM-DD folders to new hierarchical structure"""
        legacy_folders = self.get_legacy_daily_folders()
        
        if not legacy_folders:
            return
        
        print(f" Found {len(legacy_folders)} legacy folders to migrate...")
        
        for folder in legacy_folders:
            try:
                # Parse date from folder name
                date = datetime.strptime(folder.name, '%Y-%m-%d')
                paths = self.get_current_paths(date)
                
                # Create target directory structure
                paths['day_path'].parent.mkdir(parents=True, exist_ok=True)
                
                # Move folder to new location
                if not paths['day_path'].exists():
                    shutil.move(str(folder), str(paths['day_path']))
                    print(f" Migrated {folder.name} → {paths['day_path']}")
                else:
                    print(f" Target already exists for {folder.name}")
                    
            except Exception as e:
                print(f" Failed to migrate {folder.name}: {e}")
        
        print(" Migration completed!")

# Rest of the existing functions remain the same...
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

def save_as_markdown(title, storage_path, url, summary, full_content, source):
    """Save article as markdown in hierarchical structure"""
    try:
        filename = Path(storage_path) / f"{slugify(title)}.md"
        
        if filename.exists():
            return False
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"---\n"
                   f"title: \"{title}\"\n"
                   f"date: {datetime.now().strftime('%Y-%m-%d')}\n"
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

def scrape_source(source_name, config, debug=False):
    """Improved source scraping with better debugging"""
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
                
        except Exception as e:
            if debug:
                print(f" Error processing article: {e}")
            continue
    
    print(f" Found {len(articles_found)} relevant articles from {source_name}")
    return articles_found

def process_article(article, processed_articles, storage_path):
    """Process a single article with hierarchical storage"""
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
    
    if save_as_markdown(article['title'], storage_path, article['link'], summary, content, article['source']):
        processed_articles.add(url_hash)
        return {
            'title': article['title'],
            'source': article['source'],
            'link': article['link'],  
            'summary': summary
        }
    return None

def save_tldr_digest(tldr_list, storage_path):
    """Save TL;DR digest in hierarchical structure"""
    try:
        date_str = datetime.now().strftime("%Y-%m-%d")
        digest_path = Path(storage_path) / f"{date_str}_TLDR.md"
        
        with open(digest_path, "w", encoding="utf-8") as f:
            f.write(f"#  {date_str} CyberIntel TL;DR Digest\n\n")
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
                    
        print(f"Saved daily TL;DR digest with {len(tldr_list)} articles: {digest_path}")
    except Exception as e:
        print(f"Failed to save TL;DR digest: {e}")

def git_push():
    """Optimized git operations"""
    try:
        result = subprocess.run(["git", "status", "--porcelain"], 
                              capture_output=True, text=True, timeout=10)
        if not result.stdout.strip():
            print("No changes to commit")
            return
        
        subprocess.run(["git", "add", "."], check=True, timeout=10)
        subprocess.run(["git", "commit", "-m", f"Auto-update {datetime.now().strftime('%Y-%m-%d %H:%M')}"], 
                      check=True, timeout=15)
        subprocess.run(["git", "push", "origin", "main"], check=True, timeout=30)
        print(" Pushed to GitHub")
        
    except subprocess.TimeoutExpired:
        print("Git operation timed out")
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")

def main(debug=False, migrate=False):
    """Enhanced main function with hierarchical organization"""
    print(" Starting enhanced cybersecurity news scraper with hierarchical organization...")
    
    # Initialize hierarchical organizer
    organizer = HierarchicalOrganizer()
    
    # Migrate legacy structure if requested
    if migrate:
        organizer.migrate_legacy_structure()
    
    # Get current storage path
    storage_path = organizer.get_storage_path()
    print(f" Storing articles in: {storage_path}")
    
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
    print(f"🔍 Found {len(all_articles)} relevant articles in {scrape_time - start_time:.1f}s")
    
    if not all_articles:
        print("📭 No new articles found")
        save_tldr_digest([], storage_path)
        return
    
    successful_saves = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(process_article, article, processed_articles, storage_path)
            for article in all_articles
        ]
        
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            if result:
                successful_saves.append(result)
                print(f"[{i}/{len(all_articles)}] {result['source']}: {result['title'][:50]}...")
            else:
                print(f"[{i}/{len(all_articles)}]  Skipped article")
    
    # Save processed articles cache AFTER processing
    save_processed_articles(processed_articles)
    
    total_time = time.time() - start_time
    print(f"\n - SUMMARY ({total_time:.1f}s total):")
    print(f"   - Sources: {len(NEWS_SOURCES)}")
    print(f"   - Articles found: {len(all_articles)}")
    print(f"   - Successfully saved: {len(successful_saves)}")
    print(f"   - Storage path: {storage_path}")
    
    # Save daily digest
    save_tldr_digest(successful_saves, storage_path)
    
    # Check for reorganization after saving new content
    organizer.check_and_reorganize()
    
    if successful_saves or organizer.get_legacy_daily_folders():
        print("\n Pushing to GitHub...")
        git_push()
    else:
        print("\n No new articles saved, but digest created")

if __name__ == "__main__":
    import sys
    debug_mode = "--debug" in sys.argv
    migrate_mode = "--migrate" in sys.argv
    main(debug=debug_mode, migrate=migrate_mode)