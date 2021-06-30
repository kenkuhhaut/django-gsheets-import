from django.db import models




##
## Choices for literary form
##
class LiteraryForm(models.TextChoices):
    NOVEL = ('NL', 'Novel')
    POETRY = ('PT', 'Poem')
    DRAMA = ('DR', 'Drama')
    SHORT_STORY = ('ST', 'Short story')
    NOVELLA = ('NLA', 'Novella')




##
## Model for authors
##
class Author(models.Model):
    first_name = models.CharField(max_length = 50, help_text = "The author's first name (max. 50 characters)")
    last_name = models.CharField(max_length = 50, help_text = "The author's last name (max. 50 characters)")
    short_name = models.CharField(max_length = 30, unique=True, help_text = "A short name to uniquely identify the author (max. 30 characters)")
    date_of_birth = models.DateField(help_text = "The author's date of birth (YYYY-MM-DD)")

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)




##
## Model for works of literature
##
class Work(models.Model):
    title = models.CharField(max_length = 100, help_text = "The work's full title (max. 100 characters)")
    author = models.ForeignKey(Author, on_delete = models.PROTECT, help_text = "The work's primary author")
    publication_date = models.IntegerField(help_text = "The year in which the work was first published (YYYY; use negative numbers for B.C.)")
    form = models.CharField(max_length = 3, choices = LiteraryForm.choices, help_text = "Select the appropriate literary form from the list of options")
    wiki_link = models.URLField("wikipedia link", max_length = 200, help_text = "Link to the English-language Wikipedia page (max. 200 characters)", blank = True, null = True)

    def __str__(self):
        return self.title
