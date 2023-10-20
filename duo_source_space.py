"""Prepare source spaces from individualized structural MRIs."""

import os
import os.path as op
import subprocess
import shutil
import mne

subjects_dir= '/storage/anat/subjects'


# get subjects that haven't been processed yet
subjects = sorted([s for s in os.listdir(subjects_dir)
            if s.startswith('duo') and not
            op.exists(op.join(subjects_dir, s, 'bem', f'{s}-oct-6-src.fif'))])
print(subjects)

preflood = 12
overwrite = True
n_jobs = 8
spacing = 'oct-6'

do_plots = False
do_surf = True

for subject in subjects:
    base_path = op.join(subjects_dir, subject)
    src_dir = op.join(base_path, 'bem')
    surf_name = op.join(src_dir, '%s-%s-src.fif' % (subject, spacing))
    bsurf_name = op.join(base_path, 'bem', '%s-5120-bem.fif' % subject)
    bsol_name = op.join(base_path, 'bem', '%s-5120-bem-sol.fif' % subject)
    print('Working on source space for subject %s.' % subject)

    assert op.exists(bsol_name)
    
    # set up source spaces
    if do_surf:
        surf = mne.setup_source_space(subject=subject,
                                      subjects_dir=subjects_dir,
                                      n_jobs=n_jobs, spacing=6)
        mne.write_source_spaces(surf_name, surf, overwrite=overwrite)

    if do_plots:
        # source space plot
        s_plot = mne.viz.plot_alignment(subject=subject,
                                        subjects_dir=subjects_dir,
                                        surfaces='white',
                                        coord_frame='head', src=surf)
