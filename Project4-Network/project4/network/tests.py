from django.test import TestCase
from network.models import *
# Create your tests here.
class PostTests(TestCase):

    def setUp(self):
        #Create users
        u1 = User.objects.create(username="u1")
        u2 = User.objects.create(username="u2")
        u3 = User.objects.create(username="u3")
        u4 = User.objects.create(username="u4")
        u5 = User.objects.create(username="u5")
        u6 = User.objects.create(username="u6")



        #Create posts
        p1 = Post.objects.create(user=u1,content="This is content for post 1")
        p2 = Post.objects.create(user=u2,content="This is content for post 2")
        p3 = Post.objects.create(user=u3,content="This is content for post 3")
        p4 = Post.objects.create(user=u4,content="This is content for post 4")
        p5 = Post.objects.create(user=u5,content="This is content for post 5")
        p6 = Post.objects.create(user=u1,content="This is content for post 6")
        p7 = Post.objects.create(user=u2,content="This is content for post 7")
        p8= Post.objects.create(user=u3,content="This is content for post 8")
        p9 = Post.objects.create(user=u1,content="This is content for post 9")
        p10 = Post.objects.create(user=u1,content="This is content for post 10")


        #Create following/followers 
        f1 = Following.objects.create(user=u1) #u2 follows u1
        f1.following_user.add(u2)
        f2 = Following.objects.create(user=u2) #u1 follows u2
        f2.following_user.add(u1)
        f3 = Following.objects.create(user=u1) #u3 follows u1
        f3.following_user.add(u3)
        f4 = Following.objects.create(user=u1)
        f4.following_user.add(u4)
        f5 = Following.objects.create(user=u2)
        f5.following_user.add(u3)

        #Create likes
        l1 = Liking.objects.create(user=u1)
        l1.post.add(p1)
        l2 = Liking.objects.create(user=u2)
        l2.post.add(p2)
        l3 = Liking.objects.create(user=u3)
        l3.post.add(p1)
        l4 = Liking.objects.create(user=u4)
        l4.post.add(p1)
        l5 = Liking.objects.create(user=u5)
        l5.post.add(p1)
        


    def test_post_number(self):
        """
        Checks whether user 1 has 2 posts and user 3 has 1 post only.
        """
        print(User.objects.all())
        t1 = User.objects.get(username="u1")
        self.assertEqual(t1.author.count(),4)
        t2 = User.objects.get(username = "u3")
        self.assertEqual(t2.author.count(),2)


    def test_initial_post_likes(self):
        """
        Checks if the posts are initialized to 0
        """
        t1 = Post.objects.get(content="This is content for post 1")
        self.assertEqual(t1.liked_post.count(),4)
        t2 = Post.objects.get(content="This is content for post 2")
        self.assertEqual(t2.liked_post.count(),1)


    def test_follower_following(self):
        """
        Checks if the user has the valid number of followers
        """

        t1 = User.objects.get(username="u1")
        self.assertEqual(t1.followed.count(),3)
        t2 = User.objects.get(username="u6")
        self.assertEqual(t2.followed.count(),0)

    
     
    