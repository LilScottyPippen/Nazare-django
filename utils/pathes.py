def apartment_photo_path(instance, file_name):
    return f"apartments/{instance.apartment.title}/{file_name}"


def photo_gallery_path(instance, file_name):
    return f"gallery/photo/{instance.subcategory.category.slug}/{instance.subcategory.slug}/{file_name}"


def photo_category_path(instance, file_name):
    return f"categories/{instance.name}/{file_name}"


def photo_subcategory_path(instance, file_name):
    return f"subcategories/{instance.slug}/{file_name}"


def photo_content_path(instance, file_name):
    return f"content{instance.slug}/{file_name}"