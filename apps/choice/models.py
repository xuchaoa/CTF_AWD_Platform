from django.db import models

# Create your models here.


class ChoiceLibrary(models.Model):
    '''
    选择题题库
    '''
    answer_choice = (
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
    )
    choice_question = models.TextField(null=True, verbose_name="题目描述")
    choice_a = models.TextField(null=True, verbose_name="选项A")
    choice_b = models.TextField(null=True, verbose_name="选项B")
    choice_c = models.TextField(null=True, verbose_name="选项C")
    choice_d = models.TextField(null=True, verbose_name="选项D")
    choice_answer = models.CharField(max_length=2, choices=answer_choice, verbose_name="正确答案")
    choice_score = models.IntegerField(default=2, verbose_name="分数")

    class Meta:
        verbose_name = '选择题题库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)