#!/bin/bash

dist_addons=config/dist_addons
my_addons=config/my_addons
dest_addons=config/openhab/addons

repo="romang"
image_name="openhab"
image_version="v2.1"
full_image_name="$repo/$image_name:$image_version"
export_image="${repo}_${image_name}_${image_version}"

die ()
{
    echo $1
    exit 1
}

update_config ()
{
    echo "Updating openhab configs"
    rm -rf openhab/configurations/*
    cp -r config/openhab/configurations/* openhab/configurations/
    echo "Updating openhab addons"
    rm -rf openhab/addons/*
    cp -r config/openhab/addons/* openhab/addons/
    cp -r config/openhab/start_debug.sh openhab/
}

update_runtime ()
{
        echo "Updating openhab distro"
	rm -rf distribution-*.zip
	rm -rf openhab
	wget https://github.com/openhab/openhab/releases/download/v1.6.2/distribution-1.6.2-runtime.zip
	unzip *runtime.zip -d openhab
}

update_addons ()
{
	echo "Updating addons"
	rm -rf $disct_addons
	mkdir $disct_addons
	wget https://github.com/openhab/openhab/releases/download/v1.6.2/distribution-1.6.2-addons.zip        
        unzip *addons.zip -d $disct_addons
}

process_addons ()
{
	rm -rf $dest_addons/*
	needed_addons=("org.openhab.binding.http" "org.openhab.binding.mqtt" "org.openhab.binding.ntp" "org.openhab.persistence.mysql")
	[[ -d $dest_addons ]] || die "There is no addons directory in production openhab path"
	for addon_mask in ${needed_addons[*]}
	do
	    addon=`ls ${dist_addons}/ | grep "$addon_mask"`
	    if [[ -f ${dist_addons}/$addon ]]
	    then
	        cmd="cp ${dist_addons}/$addon $dest_addons/"
	        echo $cmd
	        $cmd
	    fi
	    my_addon=`ls ${my_addons}/ | grep "$addon_mask"`
	    if [[ -f ${my_addons}/$my_addon ]]
	    then
	        cmd="cp ${my_addons}/$my_addon $dest_addons/"
	        echo $cmd
	        $cmd
	    fi
	done
}

if [[ $1 == "update_openhab" ]]
then
	update_runtime
	update_addons
	process_addons
	update_config
fi

if [[ $1 == "update_config" ]]
then
    update_config
fi

if [[ $1 == "docker_build" ]]
then
        cmd="sudo docker build --no-cache -t $full_image_name ."
        echo $cmd
	$cmd
fi

if [[ $1 == "docker_run" ]]
then
	cmd="sudo docker run -m 700m -p 443:8443 -p 1883:1883 -p 2812:2812 -t -i $full_image_name"
        echo $cmd
	$cmd
fi

if [[ $1 == "docker_export" ]]
then
	cmd="sudo docker save -o $export_image $full_image_name"
        echo $cmd
	$cmd
fi

if [[ $1 == "docker_import" ]]
then
	cmd="sudo docker load -i $export_image"
        echo $cmd
	$cmd
fi
