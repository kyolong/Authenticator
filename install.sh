set -e
pwd=`pwd`
pip install pip -U -i  https://pypi.douban.com/simple
pip install -r requirements.txt -i  https://pypi.douban.com/simple
eval sed 's/1234567890XXXXXX/$1/' Authenticator_T.py > Authenticator.py

cnt=`grep "python $pwd/Authenticator.py &" ~/.bash_profile|wc -l`
if [ 1 -ne $cnt ] ;then
echo "python $pwd/Authenticator.py &" >> ~/.bash_profile
fi
source ~/.bash_profile