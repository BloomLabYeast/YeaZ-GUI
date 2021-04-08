class PopulationBatch:
    def __init__(self, directory, glob_pattern, fluor_channel_list, bin_trans=True):
        from glob import glob
        import os
        import skimage

        glob_files = glob(os.path.join(directory, glob_pattern))
        # the glob pattern should contain all trans image files to process
        for file in glob_files:
            im = skimage.io.imread(file)

