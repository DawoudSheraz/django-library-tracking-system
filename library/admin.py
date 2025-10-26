from django.contrib import admin


from library.models import Author, Book, Member, Loan

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Member)


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'member', 'loan_date', 'due_date', 'is_returned')
    readonly_fields = ('loan_date',)
    list_filter = ('is_returned', 'member__user__username', 'book__title')
    search_fields = ('book__title', 'member__user__username')
