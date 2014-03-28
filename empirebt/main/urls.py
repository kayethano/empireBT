from django.conf.urls import patterns, include, url

urlpatterns = patterns('empirebt.main.views', 

        url(r'^authorization/tokenizer.json/$','tokenizer', name ="tokenizer"),
        url(r'^authorization/general.json/$','general_auth', name ="general_auth"),
        url(r'^authorization/chat_empire.json/$','chat_empire_auth', name ="chat_empire_auth"),


) 