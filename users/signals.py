from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from wallet.models import Wallet

# @receiver(post_save, sender=Influencer)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == User.Role.INFLUENCER:
#         influencer = InfluencerProfile.objects.create(user=instance)
#         if instance.first_name or instance.last_name or instance.birthday:
#             influencer.first_name = instance.first_name
#             influencer.last_name = instance.last_name
#             influencer.birthday = instance.birthday
#             influencer.save()


# @receiver(post_save, sender=Brand)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == User.Role.BRAND:
#         brand = BrandProfile.objects.create(user=instance)
#         if instance.company_name or instance.contact_person:
#             brand.company_name = instance.company_name
#             brand.contact_person = instance.contact_person
#             brand.save()


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
