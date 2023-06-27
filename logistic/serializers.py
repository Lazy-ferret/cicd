from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']
    # настройте сериализатор для склада

    def _create_update_pos(self, stock_item, positions_list):
        for position in positions_list:
            StockProduct.objects.update_or_create(
                stock=stock_item,
                product=position['product'],
                defaults={'quantity': position['quantity'],
                            'price': position['price']},
            )

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(validated_data)

        self._create_update_pos(stock, positions)
        # for position in positions:
        #     StockProduct(stock=stock,
        #                  product=position['product'],
        #                  quantity=position['quantity'],
        #                  price=position['price']).save()

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions
        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        self._create_update_pos(stock, positions)
        # for position in positions:
        #     StockProduct.objects.update_or_create(
        #         stock=stock,
        #         product=position['product'],
        #         defaults={'quantity': position['quantity'],
        #                     'price': position['price']},
        #     )
        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock
