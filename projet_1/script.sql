-- 1) Nombre total de produits vendus par mois

SELECT DATE_FORMAT(orders.orderDate, '%Y-%m') AS orderMonth, 
       SUM(orderdetails.quantityOrdered) AS TotalProductsSold 
FROM orders  
INNER JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
INNER JOIN products ON orderdetails.productCode = products.productCode 
WHERE orders.status = 'Shipped' or 'Resolved' 
GROUP BY orderMonth;

-- 2) Nombre de commandes par mois
SELECT DATE_FORMAT(orders.orderDate, '%Y-%m') AS orderMonth, 
	   COUNT(*) AS totalOrders 
FROM orders 
WHERE orders.status = 'Shipped' or 'Resolved'
GROUP BY orderMonth;

-- 3) Montant total des ventes par mois
SELECT DATE_FORMAT(orders.orderDate, '%Y-%m') AS orderMonth,
	   SUM(priceEach * quantityOrdered) AS totalSales 
FROM orders 
INNER JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber 
WHERE orders.status = 'Shipped' or 'Resolved'
GROUP BY orderMonth;

-- 4) Nombre de références vendues par mois
SELECT DATE_FORMAT(orders.orderDate, '%Y-%m') AS orderMonth, 
	   products.productCode AS Ref, 
	   SUM(orderdetails.quantityOrdered) AS TotalQuantity 
FROM orders 
INNER JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber 
INNER JOIN products ON orderdetails.productCode = products.productCode 
WHERE orders.status = 'Shipped' or 'Resolved'
GROUP BY orderMonth, Ref
ORDER BY orderMonth, Ref;

-- 5) Nombre de produits vendus par catégories et par mois
SELECT DATE_FORMAT(orders.orderDate, '%Y-%m') AS orderMonth,
       products.productLine, 
       SUM(orderdetails.quantityOrdered) AS TotalProductsSold
FROM orders 
INNER JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
INNER JOIN products ON orderdetails.productCode = products.productCode 
WHERE orders.status = 'Shipped' or 'Resolved'
GROUP BY orderMonth, products.productLine
ORDER BY orderMonth, products.productLine;


-- 6) Nombre de produits vendus par catégories et pays de clients
SELECT DATE_FORMAT(orders.orderDate, '%Y') AS orderYear, 
	   products.productLine, 
	   customers.country,
       SUM(orderdetails.quantityOrdered) AS TotalProductsSold
FROM orders 
INNER JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
INNER JOIN products ON orderdetails.productCode = products.productCode 
INNER JOIN customers ON orders.customerNumber = customers.customerNumber
WHERE orders.status = 'Shipped' or 'Resolved'
GROUP BY customers.country, products.productLine, orderYear 
ORDER BY customers.country, TotalProductsSold DESC;


-- 7) Nombre de produits vendus par catégories et villes de bureaux
SELECT DATE_FORMAT(orders.orderDate, '%Y') AS orderYear, 
	   products.productLine, 
	   offices.city,
       SUM(orderdetails.quantityOrdered) AS TotalProductsSold
FROM orders 
INNER JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
INNER JOIN products ON orderdetails.productCode = products.productCode 
INNER JOIN customers ON orders.customerNumber = customers.customerNumber
INNER JOIN employees ON customers.salesRepEmployeeNumber = employees.employeeNumber
INNER JOIN offices ON employees.officeCode = offices.officeCode
WHERE orders.status = 'Shipped' or 'Resolved'
GROUP BY offices.city, products.productLine, orderYear 
ORDER BY offices.city, TotalProductsSold DESC;









