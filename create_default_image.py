from PIL import Image, ImageDraw, ImageFont
import os

# Create directory if it doesn't exist
os.makedirs('frontend/static/images', exist_ok=True)

# Create a blank image with a gray background
img = Image.new('RGB', (150, 150), color=(200, 200, 200))

# Get a drawing context
d = ImageDraw.Draw(img)

# Draw a simple silhouette
d.ellipse((35, 20, 115, 100), fill=(150, 150, 150))  # Head
d.rectangle((50, 100, 100, 140), fill=(150, 150, 150))  # Body

# Add text
d.text((40, 110), "No Image", fill=(50, 50, 50))

# Save the image
img.save('templates/static/images/default-profile.png')

print("Default profile image created successfully.")