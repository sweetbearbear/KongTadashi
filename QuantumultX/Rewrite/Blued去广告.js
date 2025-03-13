# > Blued
hostname = social.blued.cn
# 主页推荐直播 
^https?:\/\/social\.blued\.cn\/users\/recommend url reject-dict
# 未登录时个人界面广告
^https?:\/\/social\.blued\.cn\/users\/no_auth\/benefit url reject-dict
# 登录后个人界面广告
^https?:\/\/social\.blued\.cn\/users\/.+\/more\/ios\?v=2 url script-response-body https://raw.githubusercontent.com/fmz200/wool_scripts/main/Scripts/blued.js
