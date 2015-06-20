#!/bin/bash

while read album
do    
    echo -e "Will download album $album"
    google picasa get "$album" .
    pushd "$album"
    echo -e "Start to upload $album to Flickr"
    find -type f|sort|xargs -I{} flickr_upload {}
    popd
done < album_list.txt

echo 'Upload is done' | sendmail your@mail.address
