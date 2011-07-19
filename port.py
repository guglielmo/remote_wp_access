# -*- coding: utf-8 -*-
import config
from RemoteWP import RemoteWP
from time import sleep
import MySQLdb
from datetime import datetime
from os import sys
blog = RemoteWP(config.serviceUrl, config.usr, config.passwd)

# connessione al DB con charset utf8, per non avere problemi con gli accenti
# http://tahpot.blogspot.com/2005/06/mysql-and-python-and-unicode.html
db = MySQLdb.connect("localhost","root","","op_openparlamento", init_command='SET NAMES utf8')
cursor = db.cursor(MySQLdb.cursors.DictCursor)
p_cursor = db.cursor(MySQLdb.cursors.DictCursor)


# creazione categoria openparlamento
blog.newCategory(name='Openparlamento', slug='openparlamento', description='Post che riguardano il progetto openparlamento')

# estrazione dei post da opp
posts_sql = "select * from sf_blog_post where is_published=1 order by published_at, created_at asc"
cursor.execute(posts_sql)
p_result_set = cursor.fetchall()

for p in p_result_set:
  print "%s, %s, %s" % (p['id'], p["title"], p["published_at"])
  
  # estrazione tag
  tags_sql = "select * from sf_blog_tag where sf_blog_post_id=%s"
  p_cursor.execute(tags_sql, (p['id']))
  t_result_set = p_cursor.fetchall()
  print "  ---"
  print "  Tag"
  print "  ---"
  tags = []
  for t in t_result_set:
    tags.append(t['tag'])
    print "  %s" % (t['tag'],)

  # inserimento post con tags nel blog via XML-RPC, categoria=openparlamento
  post_id = blog.newPost(title=p["title"], 
                         description=p["content"], 
                         categories=('Openparlamento',), 
                         mt_keywords=', '.join(tags),
                         dateCreated=p['created_at'],
                         publish=True)

  # estrazione commenti per il post
  comments_sql = "select * from sf_blog_comment where sf_blog_post_id=%s and is_moderated=0 order by created_at asc"
  p_cursor.execute(comments_sql, (p['id']))
  c_result_set = p_cursor.fetchall()
  print "  --------"
  print "  Commenti"
  print "  --------"
  for c in c_result_set:
    print "  %s, %s, %s (%s)" % (c["author_name"], c["author_email"], c["created_at"], c['sf_blog_post_id'])
    try:
      comment_id = blog.newComment(post_id, content=c['content'], 
                                   author=c['author_name'], author_email=c['author_email'])

      blog.editComment(comment_id, status='approve', date_created_gmt=c['created_at'])
    except:
      print "Unexpected error:", sys.exc_info()[0]

    # to remove throttle filtering (temprarily)
    # http://wordpress.org/support/topic/slow-down-cowboy-throttling-problems
  print " "

  

cursor.close()
