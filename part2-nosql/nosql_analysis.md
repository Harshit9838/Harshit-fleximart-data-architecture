# NoSQL Database Analysis – MongoDB for FlexiMart

## Section A: Limitations of RDBMS (Relational Databases)

Relational databases like MySQL work well for structured and uniform data, but they struggle when handling highly diverse product catalogs. In FlexiMart’s case, different products have different attributes. For example, laptops require fields such as RAM, processor, and storage, while shoes need size, color, and material. In a relational schema, this leads to many nullable columns or the creation of multiple specialized tables, increasing complexity and redundancy.

Frequent schema changes are another limitation. Every time a new product type with new attributes is introduced, the database schema must be altered using `ALTER TABLE` operations. These changes can be costly, time-consuming, and risky in production environments, especially when the dataset grows large.

Storing customer reviews is also inefficient in an RDBMS. Reviews naturally form a one-to-many relationship with products and often include nested information such as ratings, comments, and timestamps. Representing this structure in relational tables requires additional tables and joins, which increases query complexity and reduces performance for read-heavy operations.

---

## Section B: Benefits of NoSQL (MongoDB)

MongoDB addresses these challenges through its flexible, document-based data model. Products are stored as JSON-like documents, allowing each product to have its own structure. A laptop document can include technical specifications like RAM and processor, while a shoe document can store size and color, all without enforcing a fixed schema.

MongoDB also supports embedded documents, making it ideal for storing customer reviews directly inside product documents. Reviews can be stored as an array of sub-documents, which improves read performance by eliminating the need for joins and enabling faster retrieval of product and review data together.

Additionally, MongoDB is designed for horizontal scalability. It supports sharding, which allows data to be distributed across multiple servers. This makes MongoDB well-suited for handling large and rapidly growing product catalogs, high traffic, and evolving data models, all while maintaining good performance and availability.

---

## Section C: Trade-offs of Using MongoDB

One major disadvantage of MongoDB compared to MySQL is weaker support for complex transactions. While MongoDB supports transactions, they are generally more limited and less efficient than those in relational databases, which can be a concern for strict financial or order-processing systems.

Another drawback is data consistency and enforcement of constraints. MongoDB does not enforce strong schemas or foreign key relationships by default, which places more responsibility on the application layer to ensure data integrity. This can lead to inconsistent data if proper validation is not implemented.
