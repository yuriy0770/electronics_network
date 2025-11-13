from django.contrib import admin
from django.utils.html import format_html
from .models import NetworkNode, Contact, Product


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'country', 'city', 'street', 'house_number', 'network_node']
    list_filter = ['country', 'city']
    search_fields = ['email', 'country', 'city']

    def network_node(self, obj):
        try:
            node = obj.networknode
            url = f"/admin/electronics/networknode/{node.id}/change/"
            return format_html('<a href="{}">{}</a>', url, node.name)
        except NetworkNode.DoesNotExist:
            return "Не привязан"

    network_node.short_description = 'Звено сети'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'release_date']
    list_filter = ['release_date']
    search_fields = ['name', 'model']


class NetworkNodeInline(admin.StackedInline):
    model = NetworkNode
    extra = 0
    can_delete = False
    show_change_link = True
    fields = ['name', 'node_type', 'level', 'supplier', 'debt_to_supplier']
    readonly_fields = ['level']


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'get_node_type_display',
        'level',
        'supplier_link',
        'debt_to_supplier',
        'created_at',
        'contact_email',
        'contact_city'
    ]
    list_filter = ['node_type', 'level', 'contact__city']
    search_fields = ['name', 'contact__city', 'contact__country']
    readonly_fields = ['created_at', 'level', 'supplier_link']
    filter_horizontal = ['products']
    raw_id_fields = ['contact', 'supplier']

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'node_type', 'level')
        }),
        ('Контакты', {
            'fields': ('contact',)
        }),
        ('Бизнес информация', {
            'fields': ('supplier', 'supplier_link', 'debt_to_supplier', 'products')
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def contact_email(self, obj):
        return obj.contact.email

    contact_email.short_description = 'Email'

    def contact_city(self, obj):
        return obj.contact.city

    contact_city.short_description = 'Город'

    def supplier_link(self, obj):
        if obj.supplier:
            url = f"/admin/electronics/networknode/{obj.supplier.id}/change/"
            return format_html('<a href="{}" target="_blank">{}</a>', url, obj.supplier.name)
        return "-"

    supplier_link.short_description = 'Ссылка на поставщика'

    def clear_debt(self, request, queryset):
        updated_count = queryset.update(debt_to_supplier=0)
        self.message_user(
            request,
            f'Задолженность очищена для {updated_count} объектов'
        )

    clear_debt.short_description = "Очистить задолженность перед поставщиком"

    actions = [clear_debt]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('contact', 'supplier')
