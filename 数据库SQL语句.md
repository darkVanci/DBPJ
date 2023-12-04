# 建库

```sql
CREATE DATABASE IF NOT EXISTS OnlineShoppingComparison;
```

# 建表

```sql
## 管理员
CREATE TABLE IF NOT EXISTS Admin(

                                    ID INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户唯一标识',

                                    Username VARCHAR(20) NOT NULL UNIQUE COMMENT '账户名',

                                    Password VARCHAR(20) NOT NULL COMMENT '密码'

);

## 用户表

CREATE TABLE IF NOT EXISTS User (
                                    ID INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户唯一标识',
                                    Username VARCHAR(20) NOT NULL UNIQUE COMMENT '账户名',
                                    Password VARCHAR(20) NOT NULL COMMENT '密码',
                                    Name VARCHAR(30) NOT NULL COMMENT '姓名',
                                    Age INT NOT NULL COMMENT '年龄',
                                    Gender CHAR(1) NOT NULL COMMENT '性别',
                                    Phone VARCHAR(15) NOT NULL COMMENT '电话'
);

## 商家表

CREATE TABLE IF NOT EXISTS Merchant (
                                        ID INT AUTO_INCREMENT PRIMARY KEY COMMENT '商家唯一标识',
                                        Username VARCHAR(50) NOT NULL UNIQUE COMMENT '账户名',
                                        Password VARCHAR(50) NOT NULL COMMENT '密码',
                                        Name VARCHAR(30) NOT NULL COMMENT '名称',
                                        Address VARCHAR(50) NOT NULL COMMENT '地址'
);

## 商品元信息表

CREATE TABLE IF NOT EXISTS ProductInformation (
                                                  ID INT AUTO_INCREMENT PRIMARY KEY COMMENT '商品唯一标识',
                                                  Name VARCHAR(100) NOT NULL COMMENT '名称',
                                                  Category VARCHAR(100) NOT NULL COMMENT '类别',
                                                  Origin VARCHAR(100) NOT NULL COMMENT '产地',
                                                  ProductionDate DATE NOT NULL COMMENT '生产日期'
);

## 上架商品表

CREATE TABLE IF NOT EXISTS Product(

                                      ID INT AUTO_INCREMENT PRIMARY KEY COMMENT '唯一标识',

                                      ProductInformationId INT NOT NULL COMMENT '商品信息ID',

                                      MerchantId INT NOT NULL COMMENT '商家ID',

                                      PlatformID INT  NOT NULL COMMENT '平台ID',

                                      Price DECIMAL(10, 2) NOT NULL COMMENT '价格',

                                      Information VARCHAR(100) COMMENT '描述'

);

## 商品历史价格表

CREATE TABLE IF NOT EXISTS HistoryPrice(

                                           ID INT AUTO_INCREMENT PRIMARY KEY COMMENT '唯一标识',

                                           ProductInformationId INT NOT NULL COMMENT '商品信息ID',

                                           MerchantId INT NOT NULL COMMENT '商家ID',

                                           PlatformID INT  NOT NULL COMMENT '平台ID',

                                           Price DECIMAL(10, 2) NOT NULL COMMENT '价格',

                                           PriceDate TIMESTAMP NOT NULL COMMENT '记录价格的日期和时间'

);

## 用户收藏的商品

CREATE TABLE UserWithProduct(

                                ID INT AUTO_INCREMENT PRIMARY KEY COMMENT '唯一标识',

                                UserId INT NOT NULL COMMENT '用户ID',

                                ProductInformationId INT NOT NULL COMMENT '商品ID',

                                PriceLowerLimit DECIMAL(10, 2) NOT NULL COMMENT '价格下限'

);

## 用户消息列表

CREATE TABLE message(

                        ID INT AUTO_INCREMENT PRIMARY KEY COMMENT '唯一标识',

                        UserId INT NOT NULL COMMENT '用户ID',

                        ProductInformationId INT NOT NULL COMMENT '商品信息ID',

                        MerchantId INT NOT NULL COMMENT '商家ID',

                        PlatformID INT  NOT NULL COMMENT '平台ID',

                        Price DECIMAL(10, 2) NOT NULL COMMENT '价格'

);

## 平台表

CREATE TABLE Platform(

                         ID INT AUTO_INCREMENT PRIMARY KEY COMMENT '唯一标识',

                         Name VARCHAR(30) NOT NULL COMMENT '平台名'

)
```

# 触发器实现数据联动

## 商家上架商品后，自动将数据填入商品历史价格表

```sql
DELIMITER //

CREATE TRIGGER after_product_insert
AFTER INSERT ON Product
FOR EACH ROW
BEGIN
    -- 将新上架的商品数据插入到商品历史价格表
    INSERT INTO HistoryPrice (ProductInformationId, MerchantId, PlatformID, Price, PriceDate)
    VALUES (NEW.ProductInformationId, NEW.MerchantId, NEW.PlatformID, NEW.Price, NOW());
END;

DELIMITER ;

```



## 上架商品修改价格后，自动查询用户收藏商品，若满足价格下限发送消息

```sql
DELIMITER //

CREATE TRIGGER after_product_price_update
AFTER UPDATE ON Product
FOR EACH ROW
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_userId INT;
    DECLARE cur CURSOR FOR 
        SELECT UserId
        FROM UserWithProduct
        WHERE ProductInformationId = NEW.ProductInformationId AND PriceLowerLimit >= NEW.Price;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- 当价格下降时
    IF NEW.Price < OLD.Price THEN
        -- 检查是否有用户收藏了这个商品并且新价格低于或等于其设置的价格下限
        OPEN cur;
        read_loop: LOOP
            FETCH cur INTO v_userId;
            IF done THEN
                LEAVE read_loop;
            END IF;

            -- 向 message 表插入消息
            INSERT INTO message (UserId, ProductInformationId, MerchantId, PlatformID, Price)
            VALUES (v_userId, NEW.ProductInformationId, NEW.MerchantId, NEW.PlatformID, NEW.Price);
        END LOOP read_loop;
        CLOSE cur;
    END IF;
END;

DELIMITER ;

```

## 删除商家后，自动删除该商家上架的商品

```sql
DELIMITER //

CREATE TRIGGER before_merchant_delete
BEFORE DELETE ON Merchant
FOR EACH ROW
BEGIN
    -- 删除与被删除商家相关联的所有商品记录
    DELETE FROM Product WHERE MerchantId = OLD.ID;
END;

DELIMITER ;
```

## 删除用户后，自动删除该用户收藏的商品，以及该用户的消息

```sql
DELIMITER //

CREATE TRIGGER before_user_delete
BEFORE DELETE ON User
FOR EACH ROW
BEGIN
    -- 删除该用户收藏的所有商品记录
    DELETE FROM UserWithProduct WHERE UserId = OLD.ID;

    -- 删除该用户的所有消息
    DELETE FROM message WHERE UserId = OLD.ID;
END;

DELIMITER ;
```
