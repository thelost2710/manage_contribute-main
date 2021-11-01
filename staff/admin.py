from django.contrib import admin
from .models import User, Faculty, Term, Contribution, Document, Comment, Like, Type
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm

# Register your models here.
class UserAdmin(BaseUserAdmin):
	add_form = UserCreationForm
	list_display = ['username', 'first_name','last_name', 'Faculty']
	list_filter = ['Faculty']
	search_fields = ['username']
	fieldsets = BaseUserAdmin.fieldsets  +(
		(None, {
			'fields': ('Faculty', 'code')
		}),
		# ('Advanced options', {
		# 	'classes': ('collapse',),
		# 	'fields': ('registration_required', 'template_name'),
		# }),
	)
admin.site.register(User, UserAdmin)
class FacultyAdmin(admin.ModelAdmin):
	list_display = ['Name', 'Description']
	list_filter = ['Name']
	search_fields = ['Name']
admin.site.register(Faculty, FacultyAdmin)
class TermAdmin(admin.ModelAdmin):
	list_display = ['Name', 'Description','Closure_date','Final_Closure_date']
	list_filter = ['Name']
	search_fields = ['Name']
admin.site.register(Term, TermAdmin)
class ContributeAdmin(admin.ModelAdmin):
	list_display = ['Name', 'UserID']
	list_filter = ['Name']
	search_fields = ['Name']
	Readed = ['Name']
admin.site.register(Contribution, ContributeAdmin)
class DocumentAdmin(admin.ModelAdmin):
	list_display = ['Name', 'Description']
	list_filter = ['Name']
	search_fields = ['Name']
admin.site.register(Document, DocumentAdmin)
class CommentAdmin(admin.ModelAdmin):
	list_display = ['ContributeID']
	list_filter = ['UserID']
	search_fields = ['UserID']
admin.site.register(Comment, CommentAdmin)
class TypeAdmin(admin.ModelAdmin):
	list_display = ['Name']
	list_filter = ['Name']
	search_fields = ['Name']
admin.site.register(Type, TypeAdmin)