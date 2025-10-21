from django.contrib import admin
from qna.entity.models import Question, Answer

# admin.site.register(Question)
# admin.site.register(Answer)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'created_at')
    search_fields = ('subject',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass