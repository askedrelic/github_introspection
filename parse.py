import re
import base64
import os

import requests
from github import Github

try:
    username        = os.environ['GITHUB_USERNAME']
    password        = os.environ['GITHUB_PASSWORD']
except KeyError, e:
    raise SystemExit('missing environment setting: %s' % e)

g = Github(username, password)

# most_watched = requests.get('https://github.com/languages/JavaScript/most_watched')
# list(set([x for x in re.findall('href="/(([a-zA-Z0-9_-]+)+)/(([a-zA-Z0-9_-]+)+)', most_watched.content) if 'languages' not in x[0]]))

popular_repos = []

lang_page = requests.get('https://github.com/languages')
popular_langs = list(set(re.findall('href="/languages/(.*?)"', lang_page.content)))

for lang in popular_langs:
    most_watched_lang_page = requests.get('https://github.com/languages/{0}/most_watched'.format(lang))
    repos = list(set([x for x in re.findall('href="/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_-]+)', most_watched_lang_page.content) if 'languages' not in x[0]]))
    print lang
    print repos
    for x in repos:
        popular_repos.append(x)

uniq_popular_repos = sorted((set(popular_repos)))

#len(popular_repos)
#1784~
#len(uniq_popular_repos)

repo_readmes = {}

for repo_name in uniq_popular_repos[0:10]:
    repo = g.get_repo('{0}/{1}'.format(repo_name[0],repo_name[1]))
    try:
        readme = repo.get_readme()
        repo_readmes[repo_name] = readme
    except:
        repo_readmes[repo_name] = 404

def write_readme_csv(repo_readmes):
    with open('github_readmes.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for k,v in repo_readmes.iteritems():
            if v == 404:
                writer.writerow(["%s/%s" % (k[0],k[1]), 404])
            else:
                writer.writerow(["%s/%s" % (k[0],k[1]), v.name, v.name.split('.')[-1].lower(), v.size])

def export_list_to_csv(filename, the_list):
    with open(filename + '.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for item in the_list:
            if (isinstance(the_list, basestring)):
                writer.writerow([item])
            else:
                writer.writerow([x for x in item])

def guess_readme_type(path):
    path = path.lower()
    if 'textile' in path:
        return 'textile'
    if 'md' or 'mdown' or 'markdown' in path:
        return 'markdown'
    if 



def find_markdown_headers(md):
    # convert ---=== to #s
    md = re.sub('^([\w\d -_!.]+)\n[=]+(?m)', r"# \1", md)
    md = re.sub('^([\w\d -_!.]+)\n[-]+(?m)', r"## \1", md)
    # TODO: fix IRC channels
    headers = re.findall('#.*', md)
    headers = [x.strip() for x in headers] 
    # headers.extend(re.findall('^([\w\d -_!.]+\n[-=]+)(?m)', md))
    # print headers
    return headers


# [(x[0], re.findall('#.*', base64.decodestring(x[1].content))) for x in repo_readmes.iteritems() if x[1] != 404]

# finding h1/h2s with ---===
# print [(x[0], re.findall('^(.*\n[-=]+)(?m)', base64.decodestring(x[1].content))) for x in repo_readmes.iteritems() if x[1] != 404]
# [(x[0], re.findall('^([\w\d -_!.]+\n[-=]+)(?m)', base64.decodestring(x[1].content))) for x in repo_readmes.iteritems() if x[1] != 404]
