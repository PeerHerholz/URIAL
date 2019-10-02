#Generate Dockerfile.

#!/bin/sh

 set -e

 # Generate Dockerfile.
generate_docker() {
  docker run --rm kaczmarj/neurodocker:0.5.0 generate docker \
             --base neurodebian:stretch-non-free \
             --pkg-manager apt \
             --miniconda \
                conda_install="python=3.6
                json
                glob
                numpy
                pandas
                seaborn
                nilearn
                dipy
                nistats
                nipype
                mne " \
                create_env='eegprep' \
                activate=true
}

generate_singularity() {
  docker run --rm kaczmarj/neurodocker:0.5.0 generate singularity \
            --base neurodebian:stretch-non-free \
            --pkg-manager apt \
            --miniconda \
               conda_install="python=3.6
               json
               glob
               numpy
               pandas
               seaborn
               nilearn
               dipy
               nistats
               nipype
               mne " \
               create_env='eegprep' \
               activate=true
}

# generate files
generate_docker > Dockerfile
generate_singularity > Singularity

# check if images should be build locally or not
if [ '$1' = 'local' ]; then
  if [ '$2' = 'docker' ]; then
    echo "docker image will be build locally"
    # build image using the saved files
    docker build -t eegprep:test .
  elif [ '$2' = 'singularity']; then
    echo "singularity image will be build locally"
    # build image using the saved files
    singularity build eegprep.simg Singularity
  elif [ '$2' = 'both' ]; then
    echo "docker and singularity images will be build locally"
    # build images using the saved files
    docker build -t eegprep:test .
    singularity build eegprep.simg Singularity
  elif [ -z "$2" ]; then
    echo "Please indicate which image should be build. You can choose from docker, singularity or both."
  fi
else
  echo "Image(s) won't be build locally."
fi
