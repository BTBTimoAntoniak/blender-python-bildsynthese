"""
{
    "info": {
        "year": "2020",
        "version": "1",
        "description": "Exported from roboflow.ai",
        "contributor": "Roboflow",
        "url": "https://app.roboflow.ai/datasets/hard-hat-sample/1",
        "date_created": "2000-01-01T00:00:00+00:00"
    },
    "licenses": [
        {
            "id": 1,
            "url": "https://creativecommons.org/publicdomain/zero/1.0/",
            "name": "Public Domain"
        }
    ],
    "categories": [
        {
            "id": 0,
            "name": "Workers",
            "supercategory": "none"
        },
        {
            "id": 1,
            "name": "head",
            "supercategory": "Workers"
        },
        {
            "id": 2,
            "name": "helmet",
            "supercategory": "Workers"
        },
        {
            "id": 3,
            "name": "person",
            "supercategory": "Workers"
        }
    ],
    "images": [
        {
            "id": 0,
            "license": 1,
            "file_name": "0001.jpg",
            "height": 275,
            "width": 490,
            "date_captured": "2020-07-20T19:39:26+00:00"
        }
    ],
    "annotations": [
        {
            "id": 0,
            "image_id": 0,
            "category_id": 2,
            "bbox": [
                45,
                2,
                85,
                85
            ],
            "area": 7225,
            "segmentation": [],
            "iscrowd": 0
        },
        {
            "id": 1,
            "image_id": 0,
            "category_id": 2,
            "bbox": [
                324,
                29,
                72,
                81
            ],
            "area": 5832,
            "segmentation": [],
            "iscrowd": 0
        }
    ]
}
"""

import datetime
import json
import os
import re

info = {
    "year": "2025",
    "version": "1",
    "description": "Dataset from Blender-Generated Boxes",
    "contributor": "BTB GmbH",
    "date_created": datetime.datetime.now().isoformat(sep=" ", timespec="seconds"),
}

licenses = [
    {
        "id": 1,
        "url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "name": "Public Domain",
    }
]


class CocoJsonBuilder:
    def __init__(self):
        self.info = info
        self.licenses = licenses
        self.images = []
        self.annotations = []
        self.categories = []
        self._next_img_id = 1
        self._next_ann_id = 1

    def set_categories(self, categories):
        self.categories = [
            {"id": i, "name": name, "supercategory": "none"}
            for i, name in enumerate(categories, start=1)
        ]

    def get_cat_id_by_name(self, name):
        return next((c["id"] for c in self.categories if c["name"] == name), None)

    def add_annotated_image(self, annImg):
        new_img_id = self._next_img_id
        self.images.append(
            {
                "id": new_img_id,
                "license": 1,
                "file_name": annImg.file_name,
                "height": annImg.height,
                "width": annImg.width,
                "date_captured": annImg.date_captured,
            }
        )

        self._next_img_id = new_img_id + 1

        for ann in annImg.annotations:
            ann["id"] = self._next_ann_id
            ann["image_id"] = new_img_id
            ann["category_id"] = self.get_cat_id_by_name(ann["category_id"])
            self.annotations.append(ann)
            self._next_ann_id += 1

    def export_self_to_cocojson(self, dir):
        path = os.path.join(dir, "coco.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "info": self.info,
                    "licenses": self.licenses,
                    "categories": self.categories,
                    "images": self.images,
                    "annotations": self.annotations,
                },
                f,
                indent=2,
            )


class AnnotatedImage:
    def __init__(self, file_name="", height=0, width=0):
        self.file_name = file_name
        self.height = height
        self.width = width
        self.date_captured = datetime.datetime.now().isoformat(
            sep=" ", timespec="seconds"
        )
        self.annotations = []

    def add_annotation(self, bbox, name):
        if not isinstance(bbox, (list, tuple)):
            raise TypeError("bbox must be a list or tuple of 4 numbers")

        self.annotations.append(
            {
                "id": None,
                "image_id": None,
                "category_id": extract_cat(name),
                "bbox": bbox,
                "area": bbox[2] * bbox[3],  # width * height
                "segmentation": [],
                "iscrowd": 0,
            }
        )


def extract_cat(text):
    if not isinstance(text, str):
        return None
    return text.split(".", 1)[0]
