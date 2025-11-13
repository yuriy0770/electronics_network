from rest_framework import serializers
from .models import NetworkNode, Contact, Product


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'email', 'country', 'city', 'street', 'house_number']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'release_date']


class NetworkNodeSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    products = ProductSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    node_type_display = serializers.CharField(source='get_node_type_display', read_only=True)

    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'node_type', 'node_type_display', 'contact',
            'products', 'supplier', 'supplier_name', 'debt_to_supplier',
            'created_at', 'level'
        ]
        read_only_fields = ['debt_to_supplier', 'created_at', 'level']


class NetworkNodeCreateUpdateSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()

    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'node_type', 'contact', 'products',
            'supplier', 'debt_to_supplier', 'created_at', 'level'
        ]
        read_only_fields = ['debt_to_supplier', 'created_at', 'level']

    def create(self, validated_data):
        contact_data = validated_data.pop('contact')
        products_data = validated_data.pop('products', [])

        contact = Contact.objects.create(**contact_data)
        network_node = NetworkNode.objects.create(contact=contact, **validated_data)

        network_node.products.set(products_data)
        return network_node

    def update(self, instance, validated_data):
        if 'debt_to_supplier' in validated_data:
            validated_data.pop('debt_to_supplier')

        contact_data = validated_data.pop('contact', None)

        if contact_data:
            contact_serializer = ContactSerializer(instance.contact, data=contact_data, partial=True)
            if contact_serializer.is_valid():
                contact_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance