## What is Label Studio?

**Label Studio** is a versatile data annotation platform that supports various machine learning tasks such as:  
- Text classification  
- Image classification  
- Object detection  
- Named entity recognition (NER)  
- Audio transcription  
- Image segmentation  

## 🛠️ Installation

You can install Label Studio using pip:
pip install label-studio

To confirm installation:
label-studio --version

Label Studio will start a local server. Open your browser and go to:
http://localhost:8080

## Creating a New Project

1. Click on “Create Project”  
2. Enter a Project Name (e.g., Iris Flower Classification)  
3. Write an optional Project Description  
4. Choose a labeling interface template suitable for your task  
Example: Text classification, Image segmentation, Audio transcription, etc.  

## Uploading Data

After creating your project:
Click Import

Upload your dataset in one of the supported formats:  
CSV  
JSON  
Image files  
Plain text  
Each data item should follow a format compatible with the labeling configuration you select.  

## Performing Annotations

Once your data and label configuration are ready:  
Go to the Tasks tab  
Click on a task to open it  
Apply labels using the interface  
Use keyboard shortcuts to speed up annotation  

All work is auto-saved, and you can monitor progress within the dashboard.  

## Exporting Annotations

After completing the annotations:  
Click on Export  

Select the output format:  
JSON (recommended for structured data)  
CSV  
COCO (for object detection/image segmentation)  

Download the export file(s).  



