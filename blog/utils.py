from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError


def compress_and_optimize_image(image, max_width=800, max_height=800, quality=85):
    """
    Compresses and optimizes the image to reduce file size without significant loss of quality.
    :param image: The uploaded image to compress.
    :param max_width: The maximum width of the image.
    :param max_height: The maximum height of the image.
    :param quality: The compression quality (higher value = better quality).
    :return: InMemoryUploadedFile of the compressed and optimized image.
    """
    img = Image.open(image)

    # Resize the image while maintaining aspect ratio
    img.thumbnail(
        (max_width, max_height), Image.Resampling.LANCZOS
    )  # Use LANCZOS for high-quality resampling

    # Compress the image to reduce file size
    img_io = BytesIO()

    # Save the image in a highly compressed format (JPEG)
    img.save(
        img_io, format="JPEG", quality=quality, optimize=True
    )  # JPEG for better compression
    img_io.seek(0)

    # Return as an InMemoryUploadedFile to simulate an uploaded file
    return InMemoryUploadedFile(
        img_io, None, image.name, "image/jpeg", img_io.getbuffer().nbytes, None
    )


def validate_image_size(image):
    """Validates image size to ensure it doesn't exceed a specific limit."""
    filesize = image.file.size
    limit_mb = 10  # Max size in MB
    if filesize > limit_mb * 1024 * 1024:
        raise ValidationError(f"Max size of image is {limit_mb} MB")
