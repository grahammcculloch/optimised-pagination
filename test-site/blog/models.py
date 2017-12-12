from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Entry(models.Model):
    author = models.ForeignKey(
        on_delete=models.deletion.CASCADE, related_name='entries', to='blog.Author')
    category = models.ForeignKey(
        on_delete=models.deletion.CASCADE, related_name='entries', to='blog.Category')
    title = models.CharField(max_length=500)
    content = models.TextField()

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.title
