# Framework Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Internal Imports
from cave_app.storage_backends import PrivateMediaStorage, PublicMediaStorage


class FileStorage(models.Model):
    """
    Model for storing arbitrary files for access by the api
    """

    name = models.CharField(_("name"), max_length=128, help_text=_("Name of the file"), unique=True)
    file_public = models.FileField(
        _("File Public"),
        upload_to="file_storage",
        help_text=_(
            "When hosted on a cloud service, files uploaded with this field are put in a public s3 / azure bucket. Anyone with a link can access it."
        ),
        blank=True,
        storage=PublicMediaStorage(),
    )
    file_private = models.FileField(
        _("File Private"),
        upload_to="file_storage",
        help_text=_(
            "When hosted on a cloud service, files uploaded to S3 with this field are put in S3 with restricted access. They require cave server access to get a secure (credentialed and temporary) link."
        ),
        blank=True,
        storage=PrivateMediaStorage(),
    )

    # Consider adding the following limit for file sizes
    # def clean(self):
    #     if self.file_public:
    #         limit_upload_size(max_size_mb=5, upload=self.file_public)
    #     if self.file_private:
    #         limit_upload_size(max_size_mb=5, upload=self.file_private)

    # Metadata
    class Meta:
        verbose_name = _("File Storage")
        verbose_name_plural = _("File Storage")
        ordering = ("name",)

    # Methods
    def __str__(self):
        return f"{self.name}"
