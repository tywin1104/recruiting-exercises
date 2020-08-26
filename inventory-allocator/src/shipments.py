from collections import defaultdict


class InventoryAllocator:

    def __init__(self, order, inventory_distribution):
        self.order = order
        self.inventory_distribution = inventory_distribution
        self.total_inventory = defaultdict(int)
        self._load_inventory_items()

    def _load_inventory_items(self):
        for warehourse in self.inventory_distribution:
            inventory = warehourse['inventory']
            for item, quantity in inventory.items():
                self.total_inventory[item] += quantity

    def _enough_inventory(self):
        for item, order_quantity in self.order.items():
            if self.total_inventory[item] < order_quantity:
                return False
        return True

    def fulfill_order(self):
        """Fulfill the given order and compute best approach for shipments

        Fulfill the given order using provided inventory distribution data.
        Compute and return the most economicway for the order to be shipped.

        Returns:
            A list of dicts mapping warehouse names to the corresponding
            fulfilled inventory item and quantity for the given order.
            If the given order is not possible to fulfill due to insufficient
            inventory, will return an empty list.

            example:

            [{'warehouse1': {'apple': 17, 'pie': 5}},
             {'warehouse2': {'pie': 4,'banana': 4}}]
        """
        if not self._enough_inventory():
            return []

        shipments = []

        for warehouse in self.inventory_distribution:
            warehouse_name = warehouse['name']
            current_warehouse_shipment = defaultdict(int)

            for item in self.order:
                unfulfilled_quantity = self.order[item]
                if (unfulfilled_quantity == 0 or
                        item not in warehouse['inventory']):
                    continue

                quantity_to_fulfill = min(unfulfilled_quantity,
                                          warehouse['inventory'][item])
                # prevent inventory having item of quantity zero being added
                if quantity_to_fulfill > 0:
                    current_warehouse_shipment[item] += quantity_to_fulfill
                    self.order[item] -= quantity_to_fulfill

            if current_warehouse_shipment:
                shipments.append(
                    {warehouse_name: dict(current_warehouse_shipment)})

        return shipments
