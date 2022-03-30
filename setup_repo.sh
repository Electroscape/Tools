# run script with args to configure git first time or without args to only clone repos
# ./setup_repo.sh 
# OR
# ./setup_repo user_me userme@email.com

PC_NAME=${1}
EMAIL_ADD=${2}
if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
else
    echo "$PC_NAME and $EMAIL_ADD"
    git config --global user.name "$PC_NAME";
    git config --global user.email "$EMAIL_ADD";
fi

cd ~
mkdir Electroscape
cd Electroscape

CNTX={users}; NAME={Electroscape}; PAGE=1
curl "https://api.github.com/$CNTX/$NAME/repos?page=$PAGE&per_page=100" |
  grep -e 'git_url*' |
  cut -d \" -f 4 |
  xargs -L1 git clone

for f in ~/Electroscape/*
do
    echo "Processing $f"
    cd $f
    repo=`basename "$f"`
    git remote set-url origin git@github.com:Electroscape/$repo.git
done