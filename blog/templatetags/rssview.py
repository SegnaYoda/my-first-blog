from django import template
import datetime
import feedparser



register=template.Library()


#@register.inclusion_tag('blog/rss-parsing.html')
@register.inclusion_tag('blog/tags-rss-parsing.html')
def get_rssfeed(feedrss_url, posts_to_show=5):
    feed = feedparser.parse(feedrss_url)
    post = []
    for i in range(posts_to_show):
            pub_date = feed['entries'][i].published_parsed
            published = datetime.date(pub_date[0], pub_date[1], pub_date[2] )
            post.append({
                        'title': feed['entries'][i].title,
                        'author': feed['entries'][i].author,
                        'link': feed['entries'][i].link,
                        'description': feed['entries'][i].description,
                        'date': published,
                        'photo': feed.entries[i].enclosures[0].href,
                        })
    print(post)
    
    return {'post': post }