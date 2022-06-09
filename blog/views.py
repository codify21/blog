from django.db import models
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date
from .models import Post
from django.views.generic import ListView,DetailView
from django.views import View
from .forms import CommentForm

# all_posts = [
#     {
#         "slug": "hike-in-the-mountains",
#         "image": "mountains.jpg",
#         "author": "Joey",
#         "date": date(2021, 7, 21),
#         "title": "Mountain Hiking",
#         "excerpt": "There's nothing like the views you get when hiking in the mountains! And I wasn't even prepared for what happened whilst I was enjoying the view!",
#         "content": """
#             Call me crazy or cliche or what ever..but there is no denying it. Maybe it’s that dose of fresh mountain air, the exercise or the litres of water I drink when I’m hiking, but I swear to you that after a visit to the mountains I feel enormously better.
          
#             It’s as if there is an energy source in those summits that you can tap into and feed off of. Getting out there literally fuels you and rebalances you; you will notably feel more calm and happy, and less irritable or anxious. There was never a time that I left the mountains without feeling refreshed, happy and inspired – ready to take on anything that came my way.
#             <h3>They serve as an opportunity for personal growth</h3>
#             Through challenging yourself, both physically and mentally, you grow. Through pushing yourself outside of your comfort zone and getting out there, you flourish. Through completing something you started and seeing it through to the end, you make progress
          
#         """
#     },
#     {
#         "slug": "programming-is-fun",
#         "image": "coding.jpg",
#         "author": "Chandler",
#         "date": date(2022, 3, 10),
#         "title": "Programming Is Great!",
#         "excerpt": "Did you ever spend hours searching that one error in your code? Yep - that's what happened to me yesterday...",
#         "content": """
#           This time spent without our devices allows us to just be in the moment and recognize the beauty of the little things. When was the last time you allowed yourself to let go of thoughts centred around emails and work or the “things” you want or “tasks” that must get done? 
          
#           When was the last time you stopped talking or thinking for long enough to really listen to the birds sing, or appreciate the smell of that earthy scent after the rain, or to gaze out on the landscape in front of you without ‘seeing right through it‘?  
          
#           We take these little moments all for granted – personally I found that spending time in the mountains reintroduced me to the value of the little things in life and the beauty of these tiny moments.
#         """
#     },
#     {
#         "slug": "into-the-woods",
#         "image": "woods.jpg",
#         "author": "Ross",
#         "date": date(2020, 8, 5),
#         "title": "Nature At Its Best",
#         "excerpt": "Nature is amazing! The amount of inspiration I get when walking in nature is incredible!",
#         "content": """
#           For many travellers, an African safari is a dream trip they have saved up to go on for years. Whether you are planning a honeymoon, are in retirement or a gap year, or seeking an African family safari, you will benefit from your trip being personally tailored to align with your dream and your pocket book.

#           Fortes Africa offers the ultimate customizability in safari packages. Regardless if you are traveling in a group or solo, or whether you are on a shoestring budget or seeking the epitome of luxury, you will be accommodated. Their ultimate goal is customer satisfaction, so you can literally go to them with your safari ideas and they will plan it according to your budget.
#         """
#     }
# ]

# def get_date(post):
#     return post['date']  # post.get('date')

# Create your views here.

# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]#[-3:0] slicing will not work (for that we can 
#     # use -date as given )
#     # sorted_posts =  sorted(all_posts, key = get_date)
#     # latest_posts = sorted_posts[-3:]
#     return render(request , "blog/index.html",{"posts":latest_posts})

class StartingPageView(ListView):
    template_name =  "blog/index.html"
    model = Post
    ordering = ["-date"] #can add multiple entried to sort one after another using "," -- ["-date","age",..]
    context_object_name = "posts" # {"posts":latest_posts}

    def get_queryset(self):
        queryset =  super().get_queryset()
        data = queryset[:3]
        return data
    

# def posts(request):
#     all_posts =  Post.objects.all()
#     return render(request , "blog/all-posts.html",{"all_posts":all_posts})

class AllPostsView(ListView):
    template_name =  "blog/all-posts.html"
    model = Post
    ordering = ["-date"] #can add multiple entries to sort one after another using "," -- ["-date","age",..]
    context_object_name = "all_posts"  # {"all_posts":all_posts}

   

# def post_detail(request,slug):
#     # all_posts =  Post.objects.all()
#     # identified_post = next(post for post in all_posts if post['slug'] == slug)
#     # identified_post = Post.objects.get(slug = slug)
#     identified_post = get_object_or_404(Post,slug=slug)
#     return render(request , "blog/post-detail.html",{
#         "post":identified_post,
#         "post_tags":identified_post.tags.all()
#         })

# class SinglePostView(DetailView):
#     template_name =  "blog/post-detail.html"
#     model = Post
  
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["post_tags"] = self.object.tags.all()
#         context["comment_form"] = CommentForm()
#         return context

class SinglePostView(View):

    def is_stored_post(self,request,post_id):

        stored_posts= request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        
        return is_saved_for_later

    def get(self,request,slug):
        post = get_object_or_404(Post,slug=slug)
        context = {
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":CommentForm(),
            "comments":post.comments.all().order_by("-id"), #comments(its coming from related name of Comment model )
            "saved_for_later":self.is_stored_post(request,post.id)  
            }
        return render(request , "blog/post-detail.html",context)

    def post(self,request,slug):
        comment_form = CommentForm(request.POST)
        post = get_object_or_404(Post,slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)#calling save will not hit database but create a new model instance
            # (in our case comment) then later we can manually call save
            comment.post = post  # comment.post --> post is a field for model Comment
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page",args=[slug]))
      
        context = {
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":comment_form,
            "comments":post.comments.all().order_by("-id"), #comments(its coming from related name of Comment model )
            "saved_for_later":self.is_stored_post(request,post.id)  
            }
        return render(request , "blog/post-detail.html",context)

class ReadLaterView(View):
    def get(self,request):
        stored_posts = request.session.get("stored_posts")
        trib={}

        if stored_posts is None or len(stored_posts)==0:
             trib["posts"]=[]
             trib["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            trib["posts"]=posts
                

        return render(request,"blog/stored-posts.html",trib)


    def post(self,request):
        stored_posts = request.session.get("stored_posts")#using get method coz it will not fail if there is no previous storedposts

        if stored_posts is None:
            stored_posts=[]

        post_id= int(request.POST["post-id"])#name =post-id in post_detail.html

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"]=stored_posts

        return HttpResponseRedirect("/posts")
