# -*- coding: utf-8 -*-
import sys
from workflow import Workflow, ICON_WEB, web

DIR_AVATAR = './avatar/{author}.png'


def get_trending_repos():
    language = 'all'
    since = 'daily'
    base_url = 'https://github-trending-api.now.sh/repositories?language={language}&since={since}'
    avatar_url = 'https://github.com/{author}.png?size=40'
    req = web.get(base_url.format(language=language, since=since))
    req.raise_for_status()
    repos_json = req.json()

    for repo in repos_json:
        author = repo['author']
        # avatar = web.get(avatar_url.format(author=author), allow_redirects=True)
        # with open(DIR_AVATAR.format(author=author), 'w') as f:
        #     f.write(avatar.content)

    return repos_json


def main(wf):
    # repos = get_trending_repos()
    repos = wf.cached_data('posts', get_trending_repos, max_age=60 * 30)
    for repo in repos:
        # print(repo['description'])
        subtitle = '{description}'.format(
            description=repo['description'].encode('ascii', 'ignore').decode('ascii')
        )
        author = repo['author']
        wf.add_item(title=author + ' / ' + repo['name'],
                    subtitle=subtitle,
                    arg=repo['url'],
                    valid=True,
                    icon=DIR_AVATAR.format(author=author))

    # Send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))