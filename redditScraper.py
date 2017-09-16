import praw
import urllib
import time

url = 'https://www.reddit.com/r/NotTheOnion/comments/'

reddit = praw.Reddit(client_id='',
                     client_secret="", password='',
                     user_agent='bot2 by ', username='' ) #fill these in!

onion = reddit.subreddit("TheOnion")
posts = onion.top('all')
urls = []
for p in posts:
    print p.name,
    #time.sleep(2)
    urls.append(url+p.name[3:])

title_tag = '<title>'
end_title_tag = '</title>'
url_tag = "\"target_url\":"
url_tag_end = "\""
def find_title_url(reddit_url):
    u = urllib.urlopen(reddit_url)
    html_words = u.read()
    beg = html_words.find(title_tag) + len(title_tag)
    end = html_words.find(end_title_tag)
    title = html_words[beg:end]
    a = title.find(': TheOnion')
    title = title[:a].strip()
    if title.find("we're sorry") != -1:
        beg_u = html_words.find(url_tag) + len(url_tag) + 1
        end_u = html_words.find(url_tag_end,beg_u + 2)
        #print beg_u, end_u, html_words[beg_u + 1:end_u]
        onion_url = html_words[beg_u + 1:end_u]
    else:
        onion_url = None
    return (title, onion_url)


text_body_tag = '<div class="content-text">\n            <p>'
text_body_end = '</p>'
def url_to_story(onion_url):
    u = urllib.urlopen(onion_url)
    html_words = u.read()
    beg = html_words.find(text_body_tag) + len(text_body_tag)
    end = html_words.find(text_body_end,beg+1)
    return html_words[beg:end]

output_file = open('sample_articles_with_title.txt','a')
for i in range(len(urls)):
    print "%d of %d" % (i, len(urls))
    u = urls[i]
    print u, title
    title, onion_url = find_title_url(u)
    if onion_url != None:
        print title
        article = url_to_story(onion_url)
        output_file.write(title + '\n' + article + '\n')
    time.sleep(6)
output_file.close()