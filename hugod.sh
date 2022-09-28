rm -rf public
hugo --gc --minify
# scp -r public/images/* root@node:/data/images
rm -rf public/images
# scp -r public/img/* root@node:/data/img
rm -rf public/img
scp -r public/* root@node:/data/mb
echo ‘上传到node服务器成功’
rm -rf public
rm -rf mb
