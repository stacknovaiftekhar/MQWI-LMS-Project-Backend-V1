from django.contrib import admin
from .models import ContactInfo, SocialLink, WalletInfo, BankDetail


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Prevent adding if an instance already exists
        return not self.model.objects.exists()

    # Remove this method to allow deletion:
    # def has_delete_permission(self, request, obj=None):
    #     return False    # Prevent deletion


@admin.register(ContactInfo)
class ContactInfoAdmin(SingletonAdmin):
    list_display = ('name', 'email', 'phone', 'website')


@admin.register(SocialLink)
class SocialLinkAdmin(SingletonAdmin):
    list_display = ('facebook_page', 'facebook_group', 'whatsapp')


@admin.register(WalletInfo)
class WalletInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'number')


@admin.register(BankDetail)
class BankDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'account', 'bank', 'branch')