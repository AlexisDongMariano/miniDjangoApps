from django.contrib import admin
from .models import Question, Choice


class ChoiceInLine(admin.TabularInline): #StackedInline is an option as well
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question', {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInLine]
    #add columns in the question list
    list_display = ('question_text', 'pub_date', 'was_published_recently') 
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)



# from django.contrib import admin

# from .models import Question
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'question_text']

# admin.site.register(Question, QuestionAdmin)