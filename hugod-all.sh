rm -rf public
hugo --gc --minify
scp -r public/images/* root@hw:/data/mb/images
rm -rf public/images
scp -r public/img/* root@hw:/data/mb/img
rm -rf public/img
scp -r public/* root@hw:/data/mb/mb
echo ‘上传到node服务器成功’
rm -rf public
rm -rf mb
