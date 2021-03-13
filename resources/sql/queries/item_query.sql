SELECT 
/*
columns
*/

FROM bank
LEFT JOIN resource_items on bank.id = resource_items.id and bank.item_type = "resource"
LEFT JOIN equipable_items on bank.id = equipable_items.id and bank.item_type = "equipable"