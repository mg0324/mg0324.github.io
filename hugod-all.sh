rm -rf public
hugo --gc --minify
#scp -r public/images/* root@hw:/data/mb/images
rm -rf public/images
#scp -r public/img/* root@hw:/data/mb/img
rm -rf public/img
rm -rf /data/mb/mb
cp -r public/* /data/mb/mb/
echo ‘目录更新成功’
rm -rf public
rm -rf mb
