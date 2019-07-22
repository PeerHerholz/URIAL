
from os.path import join as opj
from glob import glob
import numpy as np
import pandas as pd
import nibabel as nib

from dipy.align.imwarp import SymmetricDiffeomorphicRegistration
from dipy.align.imwarp import DiffeomorphicMap
from dipy.align.metrics import CCMetric
from dipy.align.imaffine import (transform_centers_of_mass, AffineMap, MutualInformationMetric, AffineRegistration)
from dipy.align.transforms import (TranslationTransform3D,RigidTransform3D, AffineTransform3D)

from nilearn import datasets
from nipype.algorithms.misc import PickAtlas
from nipype.pipeline import Node, Workflow

def img_reg(moving_img, target_img, reg='non-lin'):

    m_img = nib.load(moving_img)
    t_img = nib.load(target_img)

    m_img_data = m_img.get_data()
    t_img_data = t_img.get_data()

    m_img_affine = m_img.affine
    t_img_affine = t_img.affine

    identity = np.eye(4)
    affine_map = AffineMap(identity,
                           t_img_data.shape, t_img_affine,
                           m_img_data.shape, m_img_affine)

    m_img_resampled = affine_map.transform(m_img_data)

    c_of_mass = transform_centers_of_mass(t_img_data, t_img_affine,
                                          m_img_data, m_img_affine)

    tf_m_img_c_mass = c_of_mass.transform(m_img_data)

    nbins = 32
    sampling_prop = None
    metric = MutualInformationMetric(nbins, sampling_prop)

    level_iters = [10, 10, 5]
    sigmas = [3.0, 1.0, 0.0]
    factors = [4, 2, 1]

    affreg = AffineRegistration(metric=metric,
                                level_iters=level_iters,
                                sigmas=sigmas,
                                factors=factors)

    transform = TranslationTransform3D()
    params0 = None
    starting_affine = c_of_mass.affine
    translation = affreg.optimize(t_img_data, m_img_data, transform, params0,
                                  t_img_affine, m_img_affine,
                                  starting_affine=starting_affine)

    tf_m_img_translat = translation.transform(m_img_data)

    transform = RigidTransform3D()
    params0 = None
    starting_affine = translation.affine
    rigid = affreg.optimize(t_img_data, m_img_data, transform, params0,
                            t_img_affine, m_img_affine,
                            starting_affine=starting_affine)

    tf_m_img_rigid = rigid.transform(m_img_data)

    transform = AffineTransform3D()
    affreg.level_iters = [10, 10, 10]
    affine = affreg.optimize(t_img_data, m_img_data, transform, params0,
                             t_img_affine, m_img_affine,
                             starting_affine=rigid.affine)

    if reg is None or reg == 'non-lin':

        metric = CCMetric(3)
        level_iters = [10, 10, 5]
        sdr = SymmetricDiffeomorphicRegistration(metric, level_iters)

        mapping = sdr.optimize(t_img_data, m_img_data, t_img_affine,
                               m_img_affine, affine.affine)

        tf_m_img = mapping.transform(m_img_data)

    elif reg == 'affine':

        tf_m_img_aff = affine.transform(m_img_data)

    return tf_m_img



    metric = CCMetric(3)

    level_iters = [10, 10, 5]
    sdr = SymmetricDiffeomorphicRegistration(metric, level_iters)

    mapping = sdr.optimize(t_img_data, m_img_data, t_img_affine, m_img_affine, starting_affine=affine.affine)

    tf_m_img = mapping.transform(m_img_data)


def get_atlas_info(atlas, res=None):
    """
    Gather all information from a specified atlas, including the path to the atlas maps, as well as labels
    and their indexes.

    Parameters
    ----------
    atlas : str
        Atlas dataset to be downloaded through nilearn's dataset_fetch_atlas functionality.
    res: str
        Specific version of atlas to be downloaded. Only necessary for Harvard-Oxford and Talairach.
        Please check nilearns respective documentation at
        https://nilearn.github.io/modules/generated/nilearn.datasets.fetch_atlas_harvard_oxford.html or
        https://nilearn.github.io/modules/generated/nilearn.datasets.fetch_atlas_talairach.html

    Returns
    -------
    atlas_info_df : pandas dataframe
        A pandas dataframe containing information about the ROIs and their indexes included in a given atlas.
    atl_ds.maps : str
        Path to the atlas maps.

    Examples
    --------
    >>> get_atlas_info('aal')
    atlas_info_df
    atl_ds.maps
    """

    if atlas == 'aal':
        atl_ds = datasets.fetch_atlas_aal()

    elif atlas == 'harvard_oxford':
        if res is None:
            print('Please provide the specific version of the Harvard-Oxford atlas you would like to use.')
        else:
            atl_ds = datasets.fetch_atlas_harvard_oxford(res)

    elif atlas == 'destriuex':
        atl_ds = datasets.fetch_atlas_destrieux_2009()

    elif atlas == 'msdl':
        atl_ds = datasets.fetch_atlas_msdl()

    elif atlas == 'talairach':
        if res is None:
            print('Please provide the level of the Talairach atlas you would like to use.')
        else:
            atl_ds = datasets.fetch_atlas_talairach(level_name=res)

    elif atlas == 'pauli_2017':
            atl_ds = datasets.fetch_atlas_pauli_2017()

    index = []
    labels = []

    for ind, label in enumerate(atl_ds.labels):
        index.append(ind)
        if atlas == 'destriuex':
            labels.append(label[1])
        else:
            labels.append(label)

    atlas_info_df = pd.DataFrame({'index': index, 'label': labels})

    return atlas_info_df, atl_ds.maps

def get_atlas_rois(atlas, roi_idx, hemisphere, res=None, path=None):
    """
    Extract ROIs from a given atlas.

    Parameters
    ----------
    atlas : str
        Atlas dataset to be downloaded through nilearn's dataset_fetch_atlas functionality.
    roi_idx: list
        List of int of the ROI(s) you want to extract from the atlas. If not sure, use get_atlas_info.
    hemisphere: list
        List of str, that is hemispheres of the ROI(s) you want to extract. Can be ['left'], ['right'] or ['left', 'right'].
    res: str
        Specific version of atlas to be downloaded. Only necessary for Harvard-Oxford and Talairach.
        Please check nilearns respective documentation at
        https://nilearn.github.io/modules/generated/nilearn.datasets.fetch_atlas_harvard_oxford.html or
        https://nilearn.github.io/modules/generated/nilearn.datasets.fetch_atlas_talairach.html
    path: str
        Path to where the extracted ROI(s) will be saved to. If None, ROI(s) will be saved in the current
        working directory.

    Returns
    -------
    list_rois: list
        A list of the extracted ROIs.

    Examples
    --------
    >>> get_atlas_rois('aal', [1, 2, 3], ['left', 'right'], path='/home/urial/Desktop')
    list_rois
    """

    if atlas == 'aal':
        atl_ds = datasets.fetch_atlas_aal()

    elif atlas == 'harvard_oxford':
        if res is None:
            print('Please provide the specific version of the Harvard-Oxford atlas you would like to use.')
        else:
            atl_ds = datasets.fetch_atlas_harvard_oxford(res)

    elif atlas == 'destriuex':
        atl_ds = datasets.fetch_atlas_destrieux_2009()

    elif atlas == 'msdl':
        atl_ds = datasets.fetch_atlas_msdl()

    elif atlas == 'talairach':
        if res is None:
            print('Please provide the level of the Talairach atlas you would like to use.')
        else:
            atl_ds = datasets.fetch_atlas_talairach(level_name=res)

    elif atlas == 'pauli_2017':
            atl_ds = datasets.fetch_atlas_pauli_2017()

    if roi_idx is None:
        print('Please provide the indices of the ROIs you want to extract.')
    elif hemisphere is None:
        print('Please provide the hemisphere(s) from which you want to extract ROIs.')

    for label in roi_idx:
        for hemi in hemisphere:
            roi_ex = Node(PickAtlas(), name='roi_ex')
            roi_ex.inputs.atlas = atl_ds.maps
            roi_ex.inputs.labels = label
            roi_ex.inputs.hemi = hemi
            if path is None:
                roi_ex.inputs.output_file = '%s_%s_%s.nii.gz' % (atlas, str(label), hemi)
                roi_ex.run()
                list_rois = glob('%s_*.nii.gz' % atlas)
            elif path:
                roi_ex.inputs.output_file = opj(path, '%s_%s_%s.nii.gz' % (atlas, str(label), hemi))
                roi_ex.run()
                list_rois = glob(opj(path, '%s_*.nii.gz' % atlas))

    print('The following ROIs were extracted: ')
    print('\n'.join(map(str, list_rois)))

    return list_rois