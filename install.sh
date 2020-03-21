set -e
pip install pip -U -i  https://pypi.douban.com/simple
pip install -r requirements.txt -i  https://pypi.douban.com/simple
eval sed 's/1234567890XXXXXX/$1/' Authenticator_T.py > Authenticator.py
echo "python `pwd`/Authenticator.py &" >> ~/.bash_profile
source ~/.bash_profile
