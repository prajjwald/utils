#!/bin/bash

# Script to simplify chrooting into a Linux installation from a different system (or Live CD)

# can be overridden with the '-e' argument
EFIPART=/dev/sda1
# can be overridden with the '-r' argument
ROOTPART=/dev/sda2

BINDMOUNTS=( "/dev" "/dev/pts" "/proc" "/sys" )
MOUNT=1

usage() {
cat << EOF
Usage: $(basename $0) [-u] [-r rootpart] [-e efipart] [-h] DEST
   -h: display this help menu
   -u: unmount (default is mount)
   -r rootpart: root partition is rootpart instead of /dev/sda2
   -e efipart: efi partition is efipart instead of /dev/sda1
   DEST: destination to mount in
EOF
}

mountAndChroot() {
    [ -d ${DEST} ] || mkdir ${DEST} || exit -1;
    [ "$(ls -A ${DEST})" ] && { echo "${DEST} is not empty, exiting" && exit -1; } || echo "using ${DEST}"

    echo "Mounting and Chrooting into ${DEST}"

    mount ${ROOTPART} ${DEST}

    for bindmount in ${BINDMOUNTS[@]};
    do
        mount --bind ${bindmount} ${DEST}${bindmount}
    done

    mount ${EFIPART} ${DEST}/boot/efi

    echo "Chrooting into ${DEST}"
    chroot ${DEST}
}

umountAll() {
    echo "Unmounting..."
    # Unmount mounts in reverse order
    umount ${DEST}/boot/efi
    for (( i=${#BINDMOUNTS[@]}-1; i>=0;i--));
    do
        umount ${DEST}${BINDMOUNTS[i]};
    done
    umount ${DEST}
    echo "Done"
}

while getopts 'hur:e:' opt
do
    case ${opt} in
        'h') usage;exit;
            ;;
        'u') MOUNT=0
            ;;
        'r') ROOTPART=${OPTARG}
            ;;
        'e') EFIPART=${OPTARG}
            ;;
        *) usage; exit -1;
            ;;
    esac
done

shift $(( OPTIND - 1 ))
DEST=$1

[ -z "${DEST}" ] && { echo "No destination provided"; usage; exit -1; }

if [ ${MOUNT} -eq 1 ];
then
    mountAndChroot
else
    umountAll
fi
