rm -rf public
hugo --gc --minify
scp -r public/images/* root@node:/data/mb-images
rm -rf public/images
scp -r public/img/* root@node:/data/mb-img
rm -rf public/img
scp -r public/* root@node:/data/mb
echo ‘上传到node服务器成功’
