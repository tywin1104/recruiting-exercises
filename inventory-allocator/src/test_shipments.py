import unittest
from shipments import InventoryAllocator


class InventoryAllocatorTest(unittest.TestCase):

    def test_exact_inventory_match(self):
        order = {'apple': 1}
        inventory_distribution = [{'name': 'owd', 'inventory': {'apple': 1}}]
        result = InventoryAllocator(order,
                                    inventory_distribution).fulfill_order()
        expected = [{'owd': {'apple': 1}}]
        self.assertCountEqual(result, expected)

    def test_empty_order(self):
        order = {}
        inventory_distribution = [{'name': 'owd', 'inventory': {'apple': 1}}]
        result = InventoryAllocator(order,
                                    inventory_distribution).fulfill_order()
        expected = []
        self.assertCountEqual(result, expected)

    def test_empty_inventory_distribution(self):
        order = {'apple': 1}
        inventory_distribution = []
        result = InventoryAllocator(order,
                                    inventory_distribution).fulfill_order()
        expected = []
        self.assertCountEqual(result, expected)

    def test_inventory_all_out_of_stock(self):
        order = {'apple': 1}
        inventory_distribution = inventory_distribution = [{
            'name': 'owd',
            'inventory': {
                'apple': 0,
                'banana': 30,
                'pie': 1
            }
        }, {
            'name': 'factory',
            'inventory': {
                'chocolate': 12,
                'pie': 10
            }
        }, {
            'name': 'factory',
            'inventory': {
                'apple': 0,
                'chocolate': 12,
                'pie': 10
            }
        }]
        result = InventoryAllocator(order,
                                    inventory_distribution).fulfill_order()
        expected = []
        self.assertCountEqual(result, expected)

    def test_empty_order_and_inventory(self):
        order = {}
        inventory_distribution = []
        result = InventoryAllocator(order,
                                    inventory_distribution).fulfill_order()
        expected = []
        self.assertCountEqual(result, expected)

    def test_not_enough_inventory_1(self):
        order = {'apple': 1}
        inventory_distribution = [{'name': 'owd', 'inventory': {'apple': 0}}]
        result = InventoryAllocator(order,
                                    inventory_distribution).fulfill_order()
        expected = []
        self.assertCountEqual(result, expected)

    def test_not_enough_inventory_2(self):
        order = {'banana': 30, 'pie': 13}
        inventory_distribution = [{
            'name': 'owd',
            'inventory': {
                'apple': 120,
                'banana': 30,
                'pie': 1
            }
        }, {
            'name': 'factory',
            'inventory': {
                'chocolate': 12,
                'pie': 10
            }
        }]
        result = InventoryAllocator(order,
                                    inventory_distribution).fulfill_order()
        expected = []
        self.assertCountEqual(result, expected)

    def test_zero_quantity_not_considered(self):
        order = {'banana': 30, 'pie': 13}
        inventory_distribution = [{
            'name': 'owd',
            'inventory': {
                'apple': 120,
                'banana': 30,
                'pie': 0
            }
        }, {
            'name': 'factory',
            'inventory': {
                'banana': 0,
                'chocolate': 12,
                'pie': 20
            }
        }]
        result = InventoryAllocator(order,
                                    inventory_distribution).fulfill_order()
        expected = [{"owd": {'banana': 30}}, {"factory": {"pie": 13}}]
        self.assertCountEqual(result, expected)

    def test_oreder_item_zero_quantity_not_considered(self):
        order = {'banana': 30, 'pie': 13, 'pencil': 0, 'book': 0}
        inventory_distribution = [{
            'name': 'owd',
            'inventory': {
                'apple': 120,
                'banana': 30,
                'pie': 10
            }
        }, {
            'name': 'factory',
            'inventory': {
                'banana': 30,
                'chocolate': 12,
                'pie': 20
            }
        }]
        result = InventoryAllocator(order,
                                    inventory_distribution).fulfill_order()
        expected = [{"owd": {'banana': 30, 'pie': 10}}, {"factory": {"pie": 3}}]
        self.assertCountEqual(result, expected)

    def test_missing_order_items(self):
        order = {'orange': 3}
        inventory_distribution = [{
            'name': 'warehouse1',
            'inventory': {
                'pineapple': 3
            }
        }, {
            'name': 'warehouse2',
            'inventory': {
                'pear': 2
            }
        }]
        result = InventoryAllocator(order,
                                    inventory_distribution).fulfill_order()
        expected = []
        self.assertCountEqual(result, expected)

    def test_order_allocated_from_different_warehouses(self):
        order = {'apple': 10}
        inventory_distribution = [
            {
                'name': 'owd',
                'inventory': {
                    'apple': 5
                }
            },
            {
                'name': 'dm',
                'inventory': {
                    'apple': 5
                }
            },
        ]
        result = InventoryAllocator(order,
                                    inventory_distribution).fulfill_order()
        expected = [{"dm": {'apple': 5}}, {"owd": {"apple": 5}}]
        self.assertCountEqual(result, expected)

    def test_order_fulfilled_entirely_by_cheapest_warehouse(self):
        order = {'banana': 10}
        inventory_distribution = [{
            'name': 'warehouse1',
            'inventory': {
                'apple': 20,
                'juice': 35
            }
        }, {
            'name': 'warehouse2',
            'inventory': {
                'apple': 50,
                'banana': 30,
            }
        }, {
            'name': 'warehouse3',
            'inventory': {
                'apple': 5,
            }
        }, {
            'name': 'warehouse4',
            'inventory': {
                'apple': 5,
                'strawberry': 1
            }
        }]
        result = InventoryAllocator(order,
                                    inventory_distribution).fulfill_order()

        expected = [{'warehouse2': {'banana': 10}}]
        self.assertCountEqual(result, expected)

    def test_skip_unused_warehouse(self):
        order = {'strawberry': 3, 'juice': 35, 'apple': 25}
        inventory_distribution = [{
            'name': 'warehouse1',
            'inventory': {
                'apple': 20,
                'juice': 35
            }
        }, {
            'name': 'warehouse2',
            'inventory': {
                'apple': 50,
                'banana': 30,
                'pear': 12,
                'strawberry': 2
            }
        }, {
            'name': 'warehouse3',
            'inventory': {
                'apple': 5,
            }
        }, {
            'name': 'warehouse4',
            'inventory': {
                'apple': 5,
                'strawberry': 1
            }
        }]
        result = InventoryAllocator(order,
                                    inventory_distribution).fulfill_order()

        # the order takes nothing from warehouse3, expect warehouse3 to not show up
        # in the shipping results
        expected = [{
            'warehouse1': {
                'juice': 35,
                'apple': 20
            }
        }, {
            'warehouse2': {
                'strawberry': 2,
                'apple': 5
            }
        }, {
            'warehouse4': {
                'strawberry': 1
            }
        }]
        self.assertCountEqual(result, expected)

    def test_complex_order(self):
        order = {'apple': 31, 'banana': 4, 'pie': 10, 'meat': 1}
        inventory_distribution = [{
            'name': 'warehouse1',
            'inventory': {
                'meat': 0,
                'apple': 17,
                'pear': 3,
                'peach': 9,
                'pie': 5
            }
        }, {
            'name': 'warehouse2',
            'inventory': {
                'box': 5,
                'onion': 14,
                'pie': 4,
                'banana': 5,
                'meat': 0,
                'strawberry': 2
            }
        }, {
            'name': 'warehouse3',
            'inventory': {
                'apple': 500,
                'meat': 0,
                'banna': 13,
                'pie': 1
            }
        }, {
            'name': 'warehouse4',
            'inventory': {
                'apple': 5,
                'strawberry': 1,
                'meat': 1
            }
        }]
        result = InventoryAllocator(order,
                                    inventory_distribution).fulfill_order()

        expected = [{
            'warehouse1': {
                'apple': 17,
                'pie': 5
            }
        }, {
            'warehouse2': {
                'pie': 4,
                'banana': 4
            }
        }, {
            'warehouse3': {
                'apple': 14,
                'pie': 1
            }
        }, {
            'warehouse4': {
                'meat': 1
            }
        }]
        self.assertCountEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
