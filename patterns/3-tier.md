### TODO:
- [ ] 想想更好的例子，体现更多特性
- [ ] class Data(object):和class Data():的区别

### Tips:
- str.title(): Return a titlecased version of the string where words start with an uppercase character and the remaining characters are lowercase.
- [attribute related special methods](../_topics/special_methods.md)

### Summary:
简单的MVC模式

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Data(object):
    products = {
        'milk': {'price': 1.50, 'quantity': 10},
        'eggs': {'price': 0.50, 'quantity': 100},
    }

    def __get__(self, obj, klas):
        print "Fetching from Data Stores"
        return {'products': self.products}


class BusinessLogic:
    data = Data()

    def product_list(self):
        return self.data["products"].keys()

    def product_info(self, product):
        return self.data["products"].get(product, None)


class UI:
    """ UI interaction class """

    def __init__(self):
        self.biz_logic = BusinessLogic()

    def get_product_list(self):
        print "PRODUCT LIST:"
        for product in self.biz_logic.product_list():
            print product
            # yield product
        print "END PRODUCT LIST"

    def get_product_info(self, product):
        product_info = self.biz_logic.product_info(product)
        if product_info:
            print "PRODUCT INFORMATION:"
            print "Name: %s Price: %.2f, Quantity: %d" % (product.title(), product_info.get('price', 0),
                product_info.get('quantity', 0))
        else:
            print "That product %s does not exist in the records" % product

def main():
    ui = UI()
    ui.get_product_list()
    ui.get_product_info('eggs')
    ui.get_product_info('eggx')

if __name__ == "__main__":
    main()
```