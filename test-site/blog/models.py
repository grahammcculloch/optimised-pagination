from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        app_label = 'blog'
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    class Meta:
        app_label = 'blog'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Category(models.Model):
    name = models.CharField(max_length=200)
    moderator = models.ForeignKey(Author, related_name="moderated_categories",
                                  null=True, blank=True, on_delete=models.deletion.SET_NULL)

    class Meta:
        app_label = 'blog'
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Entry(models.Model):
    author = models.ForeignKey(
        on_delete=models.deletion.CASCADE, related_name='entries', to='blog.Author')
    category = models.ForeignKey(
        on_delete=models.deletion.CASCADE, related_name='entries', to='blog.Category')
    title = models.CharField(max_length=500)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='entries')
    related_entries = models.ManyToManyField("self")

    class Meta:
        app_label = 'blog'
        verbose_name_plural = 'entries'
        ordering = ['title']

    def __str__(self):
        return self.title
