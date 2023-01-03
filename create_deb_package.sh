#!/bin/bash
# set -x

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo ${SCRIPT_DIR}

function create_package() {

    echo "============ Creating package ${PACKAGE} ============="

    cd ${SCRIPT_DIR}

    # Get package version
    VERSION=`grep 'Version' DEBIAN/control`
    VERSION_NUMBER=$(echo ${VERSION} | cut -d " " -f 2)
    echo ${VERSION_NUMBER}

    # Increment package version
    VERSION_MINOR=$(echo ${VERSION_NUMBER} | cut -d "." -f 2)
    #echo ${VERSION_MINOR}
    VERSION_INCREMENT=$((${VERSION_MINOR} + 1))
    NEW_VERSION="0.${VERSION_INCREMENT}"
    echo "The new version is ${NEW_VERSION}"
    
    # Update package version
    sed -i s/Version.*/"Version: ${NEW_VERSION}"/ DEBIAN/control

    # Set the prefix. This will install into the debian package as the root folder
    cd ${SCRIPT_DIR}/builddir && meson configure --prefix ${PACKAGE_BUILDDEB}
    cd ${SCRIPT_DIR}/builddir && meson configure --datadir usr/share

    cd ${SCRIPT_DIR}/builddir && meson install
    
    cd ${SCRIPT_DIR}

    # Create debian package
    #dpkg-deb --build --root-owner-group ${TARGET}
    echo "Building package"
    # Clear out .pyc
    py3clean ${PACKAGE_BUILDDEB}
    
    DEB="${SCRIPT_DIR}/../${M2_DEBS}/${PACKAGE}_${NEW_VERSION}-1.deb"
    dpkg-deb --build -Zgzip ${PACKAGE_BUILDDEB} $DEB 
    
    echo "Copying to latest"
    LATEST="${SCRIPT_DIR}/../${M2_DEBS}/latest/"
    
    cd ${LATEST}
    rm -rf ${PACKAGE}_*-1.deb
    cd ${SCRIPT_DIR}
    
    cp ${DEB} ${LATEST}
}


### M2 kiosk app
PACKAGE="m2-kiosk-app"
echo 
echo ${PACKAGE}
echo
PACKAGE_BUILDDEB="${SCRIPT_DIR}/../${PACKAGE}_builddeb"
M2_DEBS="m2-debs"

autopep8 --in-place --aggressive --max-line-length 100 m2-kiosk-app
autopep8 --recursive --in-place --aggressive --max-line-length 100 *.py

if git diff-index --quiet HEAD --; then
    # No changes
    echo 'No changes'
    git status
else
    create_package
    git commit -a --verbose
fi

