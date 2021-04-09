class PopulationBatch:
    def __init__(self, directory, glob_pattern, fluor_channel_list, bin_trans=True, min_dist_pixels=10):
        from glob import glob
        import os
        from skimage.io import imread
        from skimage.filters import threshold_isodata
        from skimage.feature import peak_local_max
        from skimage.measure import label
        from skimage.transform import downscale_local_mean
        from skimage.segmentation import watershed
        from scipy.ndimage.morphology import distance_transform_edt
        import sys
        # add local directories to sys.path
        sys.path.append('unet')
        import unet.neural_network as nn
        from unet.segment import cell_merge, correct_artefacts

        # assign attributes
        self.directory = directory
        self.glob_pattern = glob_pattern
        self.fluor_channel_list = fluor_channel_list
        self.bin_trans = True
        self.min_dist_pixels = min_dist_pixels

        # generate masks
        glob_files = glob(os.path.join(directory, glob_pattern))
        self.glob_files = glob_files
        # the glob pattern should contain all trans image files to process
        mask_im_list = []
        fluor_list_list = [] #this will be a list of lists
        trans_im_list = []
        for i, file in enumerate(glob_files):
            print('Processing image ' + str(i+1) + ' of ' +str(len(glob_files)))
            im_trans = imread(file)
            trans_im_list.append(im_trans)
            if bin_trans:
                im_trans = downscale_local_mean(im_trans, (2,2))
            im_prediction = nn.prediction(im_trans, True)
            threshold_value = threshold_isodata(im_prediction)
            im_binary = im_prediction
            im_binary[im_binary > threshold_value] = 255
            im_binary[im_binary <= threshold_value] = 0
            im_distance_transform = distance_transform_edt(im_binary)
            im_peaks = peak_local_max(im_distance_transform, min_distance=min_dist_pixels, indices=False)
            im_label = label(im_peaks)
            im_watershed = watershed(-im_distance_transform, markers=im_label, mask=im_binary, connectivity=2)
            im_merged = cell_merge(im_watershed, im_prediction)
            im_correct = correct_artefacts(im_merged)
            mask_im_list.append(im_correct)
            # read in the fluor channels
            channel_im_list = []
            for channel_string in fluor_channel_list:
                channel_im = imread(file.replace('Trans', channel_string))
                channel_im_list.append(channel_im)

            fluor_list_list.append(channel_im_list)
        self.mask_im_list = mask_im_list
        self.fluor_list_list = fluor_list_list
        self.trans_im_list = trans_im_list








