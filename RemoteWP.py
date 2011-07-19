'''
Class that embeds the remote xmlrpc invocations to get and set data on a wordpress instance.
It just incorporates the functions needed to get the basic data and set posts, comments and categories.
It is not meant to be complete.
'''

import xmlrpclib

class RemoteWP:
    def __init__(self, serviceUrl, usr, passwd):
        self.serviceUrl, self.usr, self.passwd = serviceUrl, usr, passwd
        self.server = xmlrpclib.ServerProxy(self.serviceUrl)

    def getTags(self, blogid=''):
        return self.server.wp.getTags(blogid, self.usr, self.passwd)
        
    def getCategories(self, blogid=''):
        return self.server.wp.getCategories(blogid, self.usr, self.passwd)
         
    def newCategory(self, name='Category name', slug='category_slug', description='Category description', blogid='', **kw):
        return self.server.wp.newCategory(blogid, self.usr, self.passwd, dict(kw, name=name, slug=slug, description=description))
        


    def getRecentPosts(self, count=5, blogid=''):
        return self.server.metaWeblog.getRecentPosts(blogid, self.usr, self.passwd, count)
        
    def getPost(self, id):
        return self.server.metaWeblog.getPost(id, self.usr, self.passwd)
        
    def newPost(self, title='Title used for test', description='this is a test post.', categories=(), publish=True, blogid='', **kw):
        return self.server.metaWeblog.newPost(blogid, self.usr, self.passwd, dict(kw, title=title, description=description, categories=categories), publish)

    def editPost(self, id, title='Title used for test', description='this is a test post.', categories=(), publish=True, **kw):
        return self.server.metaWeblog.editPost(id, self.usr, self.passwd, dict(kw, title=title, description=description, categories=categories), publish)
        
        
    # anonymous comment, with author name (url and email are optional)
    def newComment(self, postid, comment_parent_id=0, blogid=0, content='Comment content', author='Remote author', **kw):
        return self.server.wp.newComment(blogid, '', '', postid, dict(kw, comment_parent=comment_parent_id, content=content, author=author))

    def editComment(self, id, blogid=0, **kw):
        return self.server.wp.editComment(blogid, self.usr, self.passwd, id, dict(kw))
        
    def getComments(self, postid, blogid='', **kw):
        return self.server.wp.getComments(blogid, self.usr, self.passwd, dict(kw, post_id=postid))



    def list_categories(self):
        for c in self.getCategories():
            print '%(categoryId)s\t%(description)s\n%(categoryDescription)s'%c

    def list_posts(self, count=10):
        for p in self.getRecentPosts(count):
            print '%(postid)s\t%(title)s\n%(description)s'%p


    def __repr__(self):
        return 'RemoteWP(%s, %s, %s)'%(repr(self.serviceUrl), repr(self.usr), repr(self.passwd))
