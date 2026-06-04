# Framework Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Internal Imports
from cave_app.storage_backends import PrivateMediaStorage, PublicMediaStorage
from cave_core.utils.validators import limit_upload_size


class Pages(models.Model):
    """
    Model for storing page types
    """

    name = models.CharField(
        _("Name"),
        max_length=128,
        help_text=_("Name of the page for display purposes"),
        unique=True,
    )
    url_name = models.SlugField(
        _("URL Name"),
        max_length=128,
        help_text=_("The url name for the page. Can only contain url encodable characters."),
        unique=True,
    )
    show = models.BooleanField(
        _("Show this page"),
        help_text=_("Should this page be showed"),
        default=True,
    )
    require_access = models.BooleanField(
        _("Require Access"),
        help_text=_("Require a user to have app access to see this page"),
        default=False,
    )

    def get_sections(self):
        """
        Gets all page section objects as a queryset for this page
        """
        return PageSections.objects.filter(show=True, page=self).order_by("-priority")

    # Metadata
    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    # Methods
    def __str__(self):
        return self.url_name


class PageSections(models.Model):
    """
    Model for storing page sections
    """

    page = models.ForeignKey(
        Pages,
        on_delete=models.CASCADE,
        verbose_name=_("Page"),
        help_text=_(
            "The page to assign this section to - Used in Page Sections to link a page to a section"
        ),
    )
    section_type = models.CharField(
        _("Section Type"),
        max_length=32,
        help_text=_("The section type to determine the type of section to display"),
        choices=[
            ("photo_only", "Photo Only"),
            ("video_only", "Video Only"),
            ("break", "Break"),
            ("photo_header", "Photo Header"),
            ("photo_header_left", "Photo Header Left"),
            ("photo_header_right", "Photo Header Right"),
            ("html_content", "HTML Content"),
            ("photo_quote", "Photo Quote"),
            ("photo_resource", "Photo Resource"),
            ("faq", "FAQ"),
        ],
        default="photo_only",
    )
    header = models.CharField(
        _("Header"),
        max_length=256,
        help_text=_(
            "Header for this section - Used in the `photo_header` (as the section title) and `photo_resource` (as the resource title) sections."
        ),
        default="",
        blank=True,
    )
    subheader = models.CharField(
        _("Subheader"),
        max_length=256,
        help_text=_(
            "Subheader for this section - Used in `photo_header` (as a subtitle), `photo_quote` (as the quote reference), and `faq` (as the question) sections."
        ),
        default="",
        blank=True,
    )
    content = models.TextField(
        _("Content"),
        max_length=8192,
        help_text=_(
            "Text content for this section - Renederd as HTML content in `faq` (as answer) and `html_content` (as content) sections. Rendered exactly as input (all characters escaped) for the `photo_header` (as section content) and `photo_quote` (as the quote) sections."
        ),
        default="",
        blank=True,
    )
    photo = models.ImageField(
        _("Photo Public"),
        upload_to="page_section_photos",
        help_text=_(
            "Photo for this section - Used in the `photo_only` (as the photo), `photo_header` (as the section photo), `faq` (as a quote photo) and `photo_resource` (as the resource photo) sections. Photos uploaded with this field are put in a public s3 bucket. Anyone with a link can access it."
        ),
        blank=True,
        storage=PublicMediaStorage(),
        # validators=[limit_upload_size(max_size_mb=5)]
    )
    photo_private = models.ImageField(
        _("Photo Private"),
        upload_to="page_section_photos",
        help_text=_(
            "Photo for this section if no public photo is specified - Used in the `photo_only` (as the photo), `photo_header` (as the section photo), `faq` (as a quote photo) and `photo_resource` (as the resource photo) sections. Photos uploaded to S3 with this field are put in S3 with restricted access. They require cave server access to get a secure (credentialed and temporary) link."
        ),
        blank=True,
        storage=PrivateMediaStorage(),
        # validators=[limit_upload_size(max_size_mb=5)]
    )
    link = models.URLField(
        _("Link"),
        max_length=256,
        help_text=_(
            "The page section link to make available - Used in the `photo_resource` (as the resource link - this overrides an uploaded file if it is present) section."
        ),
        blank=True,
    )
    video_embed_link = models.URLField(
        _("Video Embed Link"),
        max_length=256,
        help_text=_(
            "The page section video embed link to show in a 16:9 iFrame. Used in the `video_only` (as the video), `photo_header` (as a video at the bottom of the section) and `faq` (as a video after the answer) sections."
        ),
        blank=True,
    )
    file = models.FileField(
        _("File Public"),
        upload_to="page_section_resources",
        help_text=_(
            "The page section file to make available - Used to upload files for page sections - (i.e. photos, user info, forms, other applicable section content). Used in the `photo_resource` (as a file that can be downloaded - only used if `link` is not specified) section. Files uploaded with this field are put in a public s3 bucket. Anyone with a link can access it."
        ),
        blank=True,
        storage=PublicMediaStorage(),
    )
    file_private = models.FileField(
        _("File Private"),
        upload_to="page_section_resources",
        help_text=_(
            "The page section file to make available if a public file is not specified - Used to upload files for page sections - (i.e. photos, user info, forms, other applicable section content). Used in the `photo_resource` (as a file that can be downloaded - only used if `link` is not specified) section. Files uploaded to S3 with this field are put in S3 with restricted access. They require cave server access to get a secure (credentialed and temporary) link."
        ),
        blank=True,
        storage=PrivateMediaStorage(),
    )
    priority = models.IntegerField(
        _("Priority"),
        help_text=_(
            "Integer. A higher priority puts this section higher on the page - Used in pages to order sections"
        ),
        default=0,
    )
    show = models.BooleanField(
        _("Show"),
        default=True,
        help_text=(
            "Show this section - Used in Page Sections to enable/disable that section's visibility"
        ),
    )

    def clean(self):
        if self.photo:
            limit_upload_size(max_size_mb=5, upload=self.photo)
        if self.photo_private:
            limit_upload_size(max_size_mb=5, upload=self.photo_private)

    # Metadata
    class Meta:
        verbose_name = _("Page Section")
        verbose_name_plural = _("Page Sections")
        ordering = (
            "page",
            "-priority",
        )

    # Methods
    def __str__(self):
        return f"{self.id}"
