

If you want to run this app on your local machine here are the few steps tht needs to be done:

$git clone https://github.com/ilijapet/musical_nft_thumbnails.git
$py -m venv env && source env/bin/activate
$pip install -r requirements.txt
$sudo service postgresql start
# install message broker
$sudo apt install rabbitmq-server
$sudo service rabbitmq-server start    
# create .env file ()
    STRIPE_SECRET_KEY=sk_test_51MybU0KtroSirNQXRLaaoWH3TnZIzuAa7clHUJ50mbj4HXxn7rjlTfkbJNGnx4EOMgY7sr9y4QcNBmZJewqrFVtF00OMqoO0Fu
    STRIPE_ENDPOINT=whsec_xxxxxxxxxxxxx
    DENIS_PASS=xxxxxxxxxxxxxx
    ETHEREUM_NETWORK=maticmum
    INFURA_PROVIDER=https://polygon-mumbai.infura.io/v3/xxxxxxxxxxxxxxxxxxxxx
    SIGNER_PRIVATE_KEY=xxxxxxx
    MUSIC_NFT_ADDRESS=0x1D33a553541606E98c74a61D1B8d9fff9E0fa138
    OWNER=0x273f4FCa831A7e154f8f979e1B06F4491Eb508B6
    DJANGO_SECRET_KEY='^&p@m*nhn#hg6ujgri2sppxr7t8o^mfp3bnj%1%2f72wcr+kkz'
$celery -A musical_nft worker -l info
$celery -A musical_nft beat --loglevel=info
$stripe listen --forward-to localhost:8000/webhook/
$python manage.py runserver


Step by step guide can be found on <a href="https://dev.to/ilija" > dev blog </a>
