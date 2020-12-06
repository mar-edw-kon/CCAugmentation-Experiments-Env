import numpy as np
import CCAugmentation as cca
import CCAugmentation.transformations as ccat
from torch.utils.data import DataLoader, IterableDataset
import torchvision.transforms as torch_transforms
from datasets.SHHB.setting import cfg_data 


class CustomDataset(IterableDataset):
    def __init__(self, imgs_and_dms):
        IterableDataset.__init__(self)
        self.imgs_and_dms = imgs_and_dms
        self.img_transform = torch_transforms.Compose([
            torch_transforms.ToTensor()
        ])
    
    def __iter__(self):
        for img, dm in self.imgs_and_dms:
            yield self.img_transform(img.copy().astype('float32')), dm.copy().astype('float32') * 100.


def loading_data():
    train_pipeline = cca.Pipeline(
        cca.examples.loading.SHHLoader("/dataset/ShanghaiTech_0.1", "train", "B"),
        [
            cca.operations.Duplicate(4),ccat.Crop(None, None, 1/4, 1/4),
            ccat.Normalize("featurewise_centering", by_channel=True, means=[110.0426287,  113.97032411, 115.16945588]),
            ccat.Normalize("featurewise_std_normalization", by_channel=True, stds=[57.66114641, 58.53936174, 60.51085266])
        ]
    ).execute_generate()
    train_loader = DataLoader(CustomDataset(train_pipeline), batch_size=cfg_data.TRAIN_BATCH_SIZE, num_workers=1, drop_last=True)

    val_pipeline = cca.Pipeline(
        cca.examples.loading.SHHLoader("/dataset/ShanghaiTech_0.1", "test", "B"),
        [
            ccat.Normalize("featurewise_centering", by_channel=True, means=[110.0426287,  113.97032411, 115.16945588]),
            ccat.Normalize("featurewise_std_normalization", by_channel=True, stds=[57.66114641, 58.53936174, 60.51085266])     
        ]
    ).execute_generate()
    val_loader = DataLoader(CustomDataset(val_pipeline), batch_size=cfg_data.VAL_BATCH_SIZE, num_workers=1, drop_last=False)
    
    return train_loader, val_loader, lambda x: x # restore_trans...
