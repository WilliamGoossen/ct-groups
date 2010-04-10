""" urls.py for ct_groups app

"""

from django.conf.urls.defaults import *
from ct_groups.models import CTGroup
from ct_groups.forms import CTPageForm
from ct_groups.views import blog_new_post, blog_post_edit, group_detail, group_edit, group_note, \
    remove_editor, make_editor
from ct_groups.decorators import group_perm

blog_view = group_perm('blog', 'r')
blog_edit = group_perm('blog', 'w')
group_access = group_perm('group', 'r')
group_write = group_perm('group', 'w')

wiki_args = {'group_slug_field': 'slug', 'group_qs': CTGroup.objects.all(), 'ArticleFormClass': CTPageForm }

urlpatterns = patterns('',
    url(r'^$', 'django.views.generic.list_detail.object_list', 
        dict(queryset=CTGroup.objects.all(), 
        paginate_by=400,
        template_name='ct_groups/ct_groups_index.html' ), name="groups"),    

    url(r'^(?P<group_slug>[^/]+)/edit/$', group_access(group_edit), name="group-edit"),    
    url(r'^(?P<group_slug>[^/]+)/note/$', group_write(group_note), name="group-note"),    
    url(r'^(?P<group_slug>[^/]+)/remove-editor/(?P<object_id>[^/]+)/$', group_write(remove_editor), \
        name="group-remove-editor"),    
    url(r'^(?P<group_slug>[^/]+)/make-editor/(?P<object_id>[^/]+)/$', group_write(make_editor), \
        name="group-make-editor"),    

    url(r'^(?P<group_slug>[^/]+)/blog/new-post/', blog_edit(blog_new_post), name='blog-new-post'),
    url(r'^(?P<group_slug>[^/]+)/blog/edit/(?P<slug>[^/]+)', blog_edit(blog_post_edit), name='blog-new-post'),
    url(r'^(?P<group_slug>[^/]+)/wiki/', include('ct_groups.wiki_urls'), wiki_args),
    # url(r'^groups/(?P<group_slug>[^/]+)/wiki/', wiki_views.article_list, wiki_args, name='wiki_index'),

    url(r'^(?P<group_slug>[^/]+)/$', group_access(group_detail), name='group'),

    # url(r'^(?P<slug>[^/]+)/$', 'django.views.generic.list_detail.object_detail', 
    #     dict(queryset=CTGroup.objects.all(), 
    #     template_name='ct_groups/ct_groups_detail.html' ), name="group"),    
    url(r'^join/(?P<object_id>\d+)/$', 'ct_groups.views.join', name="join-group"),
    url(r'^leave/(?P<object_id>\d+)/$', 'ct_groups.views.leave', name="leave-group"),
    # (r'^(?P<object_id>\d+)/comments/$', 'clintemplate.workgroups.views.comments'),
    
)
