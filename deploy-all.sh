sh hugod.sh $1
sh autod.sh $1
sh githubd.sh
python3 refresh_pages.py
echo '发布成功'
