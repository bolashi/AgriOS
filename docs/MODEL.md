# Model integration

Model: https://huggingface.co/Daksh159/plant-disease-mobilenetv2

The backend downloads `mobilenetv2_plant.pth` at first start via huggingface_hub, builds torchvision MobileNetV2 with a Dropout(0.2) + Linear(1280,38) head, and applies Resize((224,224)), ToTensor, and ImageNet normalization. This follows the published model card.

**Important verification requirement:** The model repository's file listing currently does not contain the `class_names.json` mentioned in its README. The included `backend/app/services/class_names.json` is the standard alphabetical 38-class PlantVillage ImageFolder order, **not verified** against this author's original training class indices. If the original training mapping differs, displayed labels will be wrong even if model logits are correct. Obtain the author's exact class list and replace the file before relying on diagnoses. The model is not guaranteed perfect on field photographs.

The 14 crop dropdown entries are served by `/api/model/info`. The UI sends `crop_hint` to `/api/detect` and flags mismatches rather than relabeling predictions.
