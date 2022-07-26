# -*- coding: utf-8 -*-

from django.contrib import admin
from adminsortable.admin import SortableAdmin

from .models import (
    CertificateOfCompetency, ClassificationSociety, Company, Department, Job, JobAttachment,
    JobSector, Location, MarineCertificate, OtherCertificate, Rank, RankGroup, Trade, Vessel,
    VesselType, VikingManagedCompany)


@admin.register(JobSector)
class JobSectorAdmin(SortableAdmin):
    search_fields = ('name',)
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'sector')
    list_filter = ('sector',)
    search_fields = ('name',)


@admin.register(VikingManagedCompany)
class VikingManagedCompanyAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    prepopulated_fields = {
        'slug': ('name',)
    }


@admin.register(RankGroup)
class RankGroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'department')


@admin.register(Rank)
class RankAdmin(SortableAdmin):
    list_display = ('name', 'rank_group')
    list_filter = ('rank_group',)
    ordering = ('name',)


@admin.register(CertificateOfCompetency)
class CertificateOfCompetencyAdmin(SortableAdmin):
    search_fields = ('name',)


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(MarineCertificate)
class MarineCertificateAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(OtherCertificate)
class OtherCertificateAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('certificate_type',)


@admin.register(Location)
class LocationAdmin(SortableAdmin):
    search_fields = ('name',)


@admin.register(ClassificationSociety)
class ClassificationSocietyAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(VesselType)
class VesselTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Vessel)
class VesselAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class JobAttachmentInline(admin.TabularInline):
    model = JobAttachment
    extra = 1


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    date_hierarchy = 'closes'
    list_editable = ('jobs_at_sea',)
    list_display = ('id', 'job_status', 'created', 'closes', 'jobs_at_sea')
    list_filter = ('jobs_at_sea', 'job_status', 'created', 'closes')
    search_fields = ['id']

    inlines = [
        JobAttachmentInline,
    ]
