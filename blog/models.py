from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from .utils import compress_and_optimize_image


# Create your models here.


def validate_image_size(image):
    """Validates image size to ensure it doesn't exceed a specific limit."""
    filesize = image.file.size
    limit_mb = 10  # Max size in MB
    if filesize > limit_mb * 1024 * 1024:
        raise ValidationError(f"Max size of image is {limit_mb} MB")


class Tag(models.Model):
    caption = models.CharField(max_length=20, verbose_name="etiqueta")

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="nombre")
    last_name = models.CharField(max_length=100, verbose_name="apellido")
    email_address = models.EmailField(verbose_name="correo electrónico")
    image = models.ImageField(
        upload_to="authors",
        null=True,
        verbose_name="imagen",
        validators=[validate_image_size],
    )
    bio = models.TextField(
        validators=[MinLengthValidator(10)], null=True, verbose_name="biografía"
    )

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()

    def save(self, *args, **kwargs):
        if self.image:
            # Compress and optimize image before saving
            self.image = compress_and_optimize_image(self.image)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Autor"
        verbose_name_plural = "Autores"


class Post(models.Model):
    title = models.CharField(max_length=150, verbose_name="título")
    excerpt = models.CharField(max_length=200, null=True, verbose_name="resumen")
    date = models.DateField(auto_now=True, verbose_name="fecha")
    slug = models.SlugField(unique=True, db_index=True, verbose_name="slug")
    youtube_url = models.URLField(null=True, verbose_name="URL de YouTube")
    content = models.TextField(
        validators=[MinLengthValidator(10)], verbose_name="contenido"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name="autor",
    )
    tags = models.ManyToManyField(Tag, related_name="posts", verbose_name="etiquetas")

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def __str__(self):
        return self.title


class Comment(models.Model):
    user_name = models.CharField(max_length=100, verbose_name="nombre de usuario")
    user_email = models.EmailField(verbose_name="correo electrónico")
    text = models.TextField(max_length=400, verbose_name="comentario")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments", verbose_name="video"
    )

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"


# frequently asked questions


class FAQ(models.Model):
    question = models.CharField(max_length=100, verbose_name="pregunta")
    answer = models.TextField(max_length=400, verbose_name="respuesta")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Pregunta frecuente"
        verbose_name_plural = "Preguntas frecuentes"
