def apartament_photo_path(instance, file_name):
    return f"apartaments/{instance.apartament.title}/{file_name}"


def photo_gallery_path(instance, file_name):
    return f"gallery/photo/{instance.subcategory.category.slug}/{instance.subcategory.slug}/{file_name}"
