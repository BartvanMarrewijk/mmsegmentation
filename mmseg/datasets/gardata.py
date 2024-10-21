from mmseg.registry import DATASETS
# from .basesegdataset import BaseSegDataset
from mmseg.datasets import BaseSegDataset
from typing import Callable, Dict, List, Optional, Sequence, Union
import os.path as osp
import json

"""This is a custom made data loader for the GARdata structure. 
The default BaseSegDataset cannot deal with the different folder structure for both the
images and annotations. Therefore we have made this version, that works with our json structure.
"""

@DATASETS.register_module()
class GarData(BaseSegDataset):

    METAINFO = dict()

    def __init__(self,
                 img_suffix='.png',
                 seg_map_suffix='.png',
                 **kwargs) -> None:
        super().__init__(
            img_suffix=img_suffix, seg_map_suffix=seg_map_suffix, **kwargs)


    def load_data_list(self) -> List[dict]:
        """Load annotation from directory or annotation file.

        Returns:
            list[dict]: All data info of dataset.
        """
        data_list = []
        img_dir = self.data_prefix.get('img_path', None)
        ann_dir = self.data_prefix.get('seg_map_path', None)
        self.ann_file = osp.join(self.data_root, self.ann_file)
        if not osp.isdir(self.ann_file) and self.ann_file:
            assert osp.isfile(self.ann_file), \
                f'Failed to load `ann_file` {self.ann_file}'

            json_file = open(self.ann_file,"r")
            data = json.load(json_file)
            for x in data:

            # lines = mmengine.list_from_file(
            #     self.ann_file, backend_args=self.backend_args)
            # for line in lines:
            #     img_name = line.strip()
                data_info = dict(
                    img_path=osp.join(self.data_root, x["file_name"]))
            #     if ann_dir is not None:
            #         seg_map = img_name + self.seg_map_suffix
                data_info['seg_map_path'] = osp.join(self.data_root, x["sem_seg_file_name"])
                data_info['label_map'] = self.label_map
                data_info['reduce_zero_label'] = self.reduce_zero_label
                data_info['seg_fields'] = []
                data_list.append(data_info)
        # else:
        #     _suffix_len = len(self.img_suffix)
        #     for img in fileio.list_dir_or_file(
        #             dir_path=img_dir,
        #             list_dir=False,
        #             suffix=self.img_suffix,
        #             recursive=True,
        #             backend_args=self.backend_args):
        #         data_info = dict(img_path=osp.join(img_dir, img))
        #         if ann_dir is not None:
        #             seg_map = img[:-_suffix_len] + self.seg_map_suffix
        #             data_info['seg_map_path'] = osp.join(ann_dir, seg_map)
        #         data_info['label_map'] = self.label_map
        #         data_info['reduce_zero_label'] = self.reduce_zero_label
        #         data_info['seg_fields'] = []
        #         data_list.append(data_info)
        #     data_list = sorted(data_list, key=lambda x: x['img_path'])
        return data_list



