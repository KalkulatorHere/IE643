import pandas as pd

import pandas as pd

# Initialize lists to hold the file names and text
file_names = []
texts = []

# Read the sentences.txt file manually
with open('/kaggle/input/dataset-sentences/sentences.txt', 'r') as file:
    lines = file.readlines()
    # Use only 50% of the total lines
    lines = lines[:len(lines) // 2]
    
    for line in lines:
        # Skip comment lines
        if line.startswith('#'):
            continue
        
        # Split the line by whitespace
        parts = line.split()
        
        if len(parts) < 8:
            continue  # Skip lines that don't have enough parts
        
        # Extract file name and text
        file_name = parts[0]  # The first part is the file name
        text = parts[9]  # The 9th part is the transcription (after bounding box)
        
        # Replace | with space to get proper sentence
        text = text.replace('|', ' ')
        
        file_names.append(file_name)
        texts.append(text)

# Create a DataFrame
df = pd.DataFrame({'file_name': file_names, 'text': texts})


# Create a DataFrame
df = pd.DataFrame({'file_name': file_names, 'text': texts})

# Fix file names if needed (e.g., append 'g' if they end with 'jp')
df['file_name'] = df['file_name'].apply(lambda x: x + 'g' if x.endswith('jp') else x)

# Display the DataFrame
print(df.head())

df.to_csv('/kaggle/working/iam')



import pandas as pd
import os
from PIL import Image, ImageOps, ImageEnhance

# Load CSV files
crohme_csv_path = "/kaggle/input/dataset-sentences/img_data2/img_data2/labels_mathematical.csv"
iam_csv_path = "/kaggle/working/iam"
crohme_df = pd.read_csv(crohme_csv_path)
iam_df = pd.read_csv(iam_csv_path)

# Output directories
output_images_dir = "/kaggle/working/output"
os.makedirs(output_images_dir, exist_ok=True)
output_annotations_dir = "/kaggle/working/annotations"
os.makedirs(output_annotations_dir, exist_ok=True)

def enhance_crohme_image(image):
    """
    Enhance CROHME image by increasing contrast and thickness
    """
    # Convert to grayscale if not already
    if image.mode != 'L':
        image = image.convert('L')
    
    # Increase contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)  # Increase contrast by factor of 2
    
    # Apply threshold to make lines thicker
    threshold = 250 # Adjust this value to control thickness
    image = image.point(lambda x: 0 if x < threshold else 255, '1')
    
    # Convert back to RGB
    return image.convert('RGB')

# Process images for alignment and scaling
for i in range(len(crohme_df)):
    # Load rows from CROHME and IAM datasets
    crohme_row = crohme_df.iloc[i]
    iam_row = iam_df.iloc[i]
    
    # Get image paths
    crohme_image_path = os.path.join("/kaggle/input/dataset-sentences/img_data2/img_data2/", crohme_row['col'])
    iam_image_path = os.path.join("/kaggle/input/dataset-sentences/sentencessss/sentencessss", iam_row['file_name']+".png")
    crohme_label = crohme_row['label']  # LaTeX label for CROHME
    iam_text = iam_row['text']  # Sentence text for IAM
    
    # Load images
    crohme_image = Image.open(crohme_image_path)
    iam_image = Image.open(iam_image_path)
    
    # Scale CROHME image to 0.75 of its original size
    crohme_image = crohme_image.resize(
        (int(crohme_image.width * 0.75), int(crohme_image.height * 0.75))
    )
    
    # Enhance CROHME image
    crohme_image = enhance_crohme_image(crohme_image)
    
    # Create a blank canvas for combined image
    canvas_width = max(iam_image.width, crohme_image.width)
    canvas_height = iam_image.height + crohme_image.height
    combined_image = Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255))
    
    # Center IAM image on the canvas
    iam_x = (canvas_width - iam_image.width) // 2
    combined_image.paste(iam_image, (iam_x, 0))
    
    # Center CROHME image below IAM text
    crohme_x = (canvas_width - crohme_image.width) // 2
    combined_image.paste(crohme_image, (crohme_x, iam_image.height))
    
    # Save the combined image
    combined_image.save(os.path.join(output_images_dir, f"combined_{i}.png"))
    
    # Create LaTeX annotation
    latex_content = f"{iam_text}\n\n{'$$'+crohme_label+'$$'}"
    annotation_path = os.path.join(output_annotations_dir, f"merged_{i+1}.txt")
    with open(annotation_path, "w") as f:
        f.write(latex_content)

print("Image processing complete. Combined images saved.")