# -*- coding: utf-8 -*-
import config
from RemoteWP import RemoteWP
from datetime import datetime

blog = RemoteWP(config.serviceUrl, config.usr, config.passwd)

# blog.newPost(title='Post RPC', description='Un post da remoto, col Pitone', categories=('Inserimenti remoti',), mt_keywords='xml, tags, prova', publish=False, dateCreated=datetime.strptime('20090417T08:43:12', '%Y%m%dT%H:%M:%S'))

# blog.newCategory(name='Inserimenti remoti', slug='inserimenti_remoti', description='Categorie di test per gli inserimenti remoti, da XMLRPC')

# blog.newComment(14, content='Un thread', author='Guglielmo Celata', author_email='guglielmo.celata@me.com', author_url='http://guglielmo.celata.com', comment_parent_id=3)

# blog.editComment(7, author='Guglielmo', status='hold')
# blog.editComment(7, status='approve')

print "categorie"
print "========="
blog.list_categories()

print "post"
print "===="
blog.list_posts()
