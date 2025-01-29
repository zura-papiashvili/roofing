from django.db import models
from django.core.validators import MinLengthValidator
from .utils import compress_and_optimize_image, validate_image_size


# Create your models here.


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
    access_type = models.CharField(
        max_length=20,
        choices=[("public", "Público"), ("private", "Privado")],
        default="public",
        verbose_name="tipo de acceso",
    )
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


#  content for pages
# Carousel model
class Carousel(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título")
    description = models.TextField(
        max_length=400, verbose_name="Descripción", blank=True, null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Carrusel"
        verbose_name_plural = "Carruseles"


# CarouselImage model
class CarouselImage(models.Model):
    carousel = models.ForeignKey(
        Carousel,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Carrusel",
    )
    image = models.ImageField(
        upload_to="carousel/images",
        verbose_name="Imagen",
        validators=[
            validate_image_size
        ],  # Replace with your actual image validator if needed
    )
    caption = models.CharField(
        max_length=200, verbose_name="Pie de foto", blank=True, null=True
    )

    url = models.URLField(max_length=200, verbose_name="URL", blank=True, null=True)

    def save(self, *args, **kwargs):
        # Compress and optimize image before saving
        self.image = compress_and_optimize_image(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Imagen de {self.carousel.title}"

    class Meta:
        verbose_name = "Imagen del Carrusel"
        verbose_name_plural = "Imágenes del Carrusel"


class RestrictedPage(models.Model):
    title = models.CharField(max_length=100, verbose_name="título")
    content = models.TextField(verbose_name="contenido")
    access_code = models.CharField(
        max_length=20, verbose_name="codigo de acceso", unique=True
    )  # The code for accessing the page

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Página para iniciados"
        verbose_name_plural = "Páginas para iniciados"
