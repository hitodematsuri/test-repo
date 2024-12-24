import re
import requests

repo_name="test-repo"

# 複数のRSSフィードURLをリストとして定義
FEED_URLS = [
    "http://chaos2ch.com/atom.xml",
    "https://hattatu-matome.ldblog.jp/atom.xml",
    "http://onecall2ch.com/atom.xml"
]

def remove_unwanted_tags_from_text(text, output_filename):
    """テキスト内の不要なタグを削除し、<link rel="self"> タグを更新"""
    # amazonやamznを含む<a>タグを削除
    text = re.sub(r'<a [^>]*href="[^"]*(amazon|amzn)[^"]*"[^>]*>.*?</a>', '', text)

    # <link rel="hub" href="http://pubsubhubbub.appspot.com"/> を削除
    text = re.sub(r'<link\s+rel="hub"\s+href="http://pubsubhubbub.appspot.com"\s*/>', '', text)
    
    # <link rel="self" href="***" /> を新しいURLに書き換え
    new_link = f'<link rel="self" href="https://hitodematsuri.github.io/{repo_name}/{output_filename}" />'
    text = re.sub(r'<link rel="self" href="[^"]*" />', new_link, text)
    
    return text

def fetch_and_process_rss():
    for index, feed_url in enumerate(FEED_URLS, start=1):
        # RSSフィードを取得
        response = requests.get(feed_url)
        if response.status_code != 200:
            print(f"Error fetching RSS feed from {feed_url}.")
            continue

        rss_content = response.text

        # 出力ファイル名を生成 (output01.xml, output02.xml, ...)
        output_file = f"output{str(index).zfill(2)}.xml"

        # 不要なタグを削除し、<link rel="self"> タグを更新
        cleaned_rss_content = remove_unwanted_tags_from_text(rss_content, output_file)

        # 新しいRSSをファイルとして保存
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_rss_content)

        print(f"RSS feed from {feed_url} processed and saved as {output_file}")

if __name__ == "__main__":
    fetch_and_process_rss()

