#!/bin/sh
# UTCOM Backup scripts
# To easily backup UTCOM Project
# Author: TualatriX

set -e
set -x
 
REMOTE_PATH="$HOME/public_html/ubuntu-tweak.com"
PROJECT_NAME="utcom"
LOCAL_PATH="$HOME/Dropbox/$PROJECT_NAME-backup"
PRE=$PROJECT_NAME-`date +%F`
KERNEL=`uname -s`

export PATH=$HOME/Sources/tools/bin:$PATH
# ruby
[[ -s "$HOME/.rvm/scripts/rvm" ]] && . "$HOME/.rvm/scripts/rvm"  # This loads RVM into a shell session.
[[ -s "/etc/profile.d/rvm.sh" ]] && . "/etc/profile.d/rvm.sh"  # This loads RVM into a shell session.
 
if [ ! -e $LOCAL_PATH/$PROJECT_NAME ]
then
    mkdir -p $LOCAL_PATH/$PROJECT_NAME
fi


cd $REMOTE_PATH; tar cf - --exclude '.git' $PROJECT_NAME | gzip > $LOCAL_PATH/$PRE.tar.gz

cd $LOCAL_PATH

tar zxvf $PRE.tar.gz $PROJECT_NAME/$PROJECT_NAME/local_settings.py
touch $PROJECT_NAME/$PROJECT_NAME/__init__.py

cd $LOCAL_PATH/$PROJECT_NAME

if [ -f $PROJECT_NAME/local_settings.py ];then
    if [ $KERNEL = "Darwin" ]; then
        gsed -i '/global_setting/d' $PROJECT_NAME/local_settings.py
    elif [ $KERNEL = "Linux" ]; then
        sed -i '/global_setting/d' $PROJECT_NAME/local_settings.py
    fi

    DB_NAME=`python -c "import $PROJECT_NAME.local_settings;print $PROJECT_NAME.local_settings.DATABASES['default']['NAME']"`
    DB_USER=`python -c "import $PROJECT_NAME.local_settings;print $PROJECT_NAME.local_settings.DATABASES['default']['USER']"`
    DB_PASSWORD=`python -c "import $PROJECT_NAME.local_settings;print $PROJECT_NAME.local_settings.DATABASES['default']['PASSWORD']"`
    rm -r $PROJECT_NAME
else
    echo "Something wrong ..."
    exit 1
fi

cd $LOCAL_PATH

mysqldump -u${DB_USER} -p${DB_PASSWORD} $DB_NAME | gzip > $PRE.sql.gz

web-backup.rb $LOCAL_PATH/$PRE.tar.gz
web-backup.rb $LOCAL_PATH/$PRE.sql.gz
